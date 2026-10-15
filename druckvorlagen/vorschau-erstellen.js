// Erstellt die zwei Vorschaubilder in druckvorlagen/vorschau/ aus den aktuellen Vorlagen.
// Aufruf (aus dem Hauptordner):  node druckvorlagen/vorschau-erstellen.js
// Braucht das Programm "Playwright" mit Chromium.
// Für das Word-Beispiel zusätzlich LibreOffice ("soffice") und "pdftoppm" (Poppler).
// Fehlen diese, wird das gespeicherte Bild vorschau/teile/word-beispiel.png verwendet.

const fs = require("fs");
const os = require("os");
const path = require("path");
const { pathToFileURL } = require("url");
const { execFileSync } = require("child_process");
let chromium;
try {
  ({ chromium } = require("playwright"));
} catch (e) {
  ({ chromium } = require("/opt/node-tools/node_modules/playwright"));
}

const QUELLEN = path.join(__dirname, "quellen");
const SIGNATUR = path.join(__dirname, "email-signatur", "signatur-julian-wehner.html");
const WORD_DOCX = path.join(__dirname, "word", "alltagsfels-briefvorlage.docx");
const ZIEL = path.join(__dirname, "vorschau");
const WORD_BILD = path.join(ZIEL, "teile", "word-beispiel.png");

const alsDataUrl = (inhalt, typ) => `data:${typ};base64,${inhalt.toString("base64")}`;

// Nimmt alle Elemente einer Seite, die zur Auswahl passen, als Bild auf.
// Der Ausschnitt wird auf ganze Bildpunkte nach innen gerundet, sonst blitzt am Rand
// eine Linie der Nachbarseite durch (die Seiten liegen in mm, also nicht auf ganzen Pixeln).
async function aufnehmen(page, datei, auswahl, zusatz = "") {
  await page.goto(pathToFileURL(datei).href + zusatz, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  const dpr = await page.evaluate(() => window.devicePixelRatio);
  const innen = (wert, runden) => runden(wert * dpr) / dpr;
  const bilder = [];
  for (const element of await page.locator(auswahl).all()) {
    const r = await element.boundingBox(); // Seite ist nicht gescrollt: Fenster- = Seitenkoordinaten
    const x = innen(r.x, Math.ceil);
    const y = innen(r.y, Math.ceil);
    const clip = { x, y, width: innen(r.x + r.width, Math.floor) - x, height: innen(r.y + r.height, Math.floor) - y };
    bilder.push({ src: alsDataUrl(await page.screenshot({ fullPage: true, clip }), "image/png"), breite: clip.width });
  }
  if (!bilder.length) throw new Error(`Nichts gefunden: ${auswahl} in ${datei}`);
  return bilder;
}

// Word-Vorlage: docx -> PDF (LibreOffice) -> PNG (pdftoppm). Sonst gespeichertes Bild.
function wordBeispiel() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "alltagsfels-word-"));
  try {
    // Schriften aus druckvorlagen/schriften/ für LibreOffice bereitstellen (Linux/fontconfig)
    const fontsConf = path.join(tmp, "fonts.conf");
    fs.writeFileSync(
      fontsConf,
      `<?xml version="1.0"?>\n<fontconfig>\n` +
        `  <include ignore_missing="yes">/etc/fonts/fonts.conf</include>\n` +
        `  <dir>${path.join(__dirname, "schriften")}</dir>\n` +
        `  <cachedir>${path.join(tmp, "fontcache")}</cachedir>\n</fontconfig>\n`
    );
    const env = { ...process.env, FONTCONFIG_FILE: fontsConf };
    const argumente = [
      "--headless", "--norestore",
      "-env:UserInstallation=" + pathToFileURL(path.join(tmp, "profil")).href,
      "--convert-to", "pdf", "--outdir", tmp, WORD_DOCX,
    ];
    const programme = ["soffice", "libreoffice", "/Applications/LibreOffice.app/Contents/MacOS/soffice"];
    let ok = false;
    for (const programm of programme) {
      try {
        execFileSync(programm, argumente, { env, stdio: "ignore", timeout: 120000 });
        ok = true;
        break;
      } catch (e) {
        if (e.code !== "ENOENT") throw e;
      }
    }
    if (!ok) throw new Error("LibreOffice nicht gefunden");
    const pdf = path.join(tmp, path.basename(WORD_DOCX, ".docx") + ".pdf");
    execFileSync("pdftoppm", ["-png", "-f", "1", "-l", "1", "-singlefile", "-scale-to-x", "1100", "-scale-to-y", "-1", pdf, path.join(tmp, "word")], { stdio: "ignore" });
    fs.mkdirSync(path.dirname(WORD_BILD), { recursive: true });
    fs.copyFileSync(path.join(tmp, "word.png"), WORD_BILD);
    console.log("Word-Beispiel neu erstellt:", path.relative(process.cwd(), WORD_BILD));
  } catch (e) {
    if (!fs.existsSync(WORD_BILD)) throw new Error("Word-Beispiel fehlt und LibreOffice/pdftoppm geht nicht: " + e.message);
    console.log("LibreOffice/pdftoppm nicht verfügbar (" + e.message + ") – nehme gespeichertes Word-Beispiel.");
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
  return alsDataUrl(fs.readFileSync(WORD_BILD), "image/png");
}

// Übersichtsseite im Stil der Vorschau: Beige, Überschrift, nummerierte Bereiche, leichte Schatten
function uebersicht(breite, titel, inhalt) {
  const schrift = alsDataUrl(fs.readFileSync(path.join(QUELLEN, "schriften", "atkinson-hyperlegible-latin-700-normal.woff2")), "font/woff2");
  return `<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8" /><style>
  @font-face { font-family: "Atkinson Hyperlegible"; src: url(${schrift}) format("woff2"); font-weight: 700; }
  * { box-sizing: border-box; }
  html, body { margin: 0; background: #f0e8dd; }
  body { width: ${breite}px; padding: 34px 40px 52px; font-family: "Atkinson Hyperlegible", Arial, sans-serif; font-weight: 700; color: #1f1b17; }
  h1 { font-size: 33px; line-height: 1.2; color: #173a66; margin: 0 0 36px; }
  h2 { font-size: 24px; line-height: 1.2; margin: 0 0 12px; }
  .reihe { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; align-items: start; margin-bottom: 56px; }
  .reihe:last-child { margin-bottom: 0; }
  .paar { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }
  .paar h3 { font-size: 19px; line-height: 1.2; color: #5b5047; margin: 0 0 8px; }
  img { display: block; width: 100%; }
  .schatten { box-shadow: 8px 8px 0 rgba(110, 90, 65, .22); }
  /* Word-Seite (A4 ohne Beschnitt) mit 3 mm weißem Rand, damit sie so groß wirkt wie das Briefpapier */
  .word { background: #fff; padding: calc(100% * 3 / 216); }
  .signatur { display: inline-block; background: #fff; padding: 26px 40px 34px 22px; }
</style></head><body><h1>${titel}</h1>${inhalt}</body></html>`;
}

const bild = (b, klasse = "schatten") => `<img class="${klasse}" src="${b.src}" alt="" />`;
const bereich = (ueberschrift, html) => `<div><h2>${ueberschrift}</h2>${html}</div>`;

async function speichern(browser, breite, html, name) {
  const page = await browser.newPage({ viewport: { width: breite, height: 600 }, deviceScaleFactor: 1 });
  await page.setContent(html, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: path.join(ZIEL, name), fullPage: true });
  await page.close();
  console.log("fertig:", name);
}

(async () => {
  const wordSrc = wordBeispiel();
  const browser = await chromium.launch();
  // doppelte Auflösung, damit die Teile im Übersichtsbild scharf sind
  const page = await browser.newPage({ viewport: { width: 1400, height: 1200 }, deviceScaleFactor: 2 });

  const [aussen, innen] = await aufnehmen(page, path.join(QUELLEN, "flyer.html"), ".spread", "?bogen");
  const [julianVorne, julianHinten, dominikVorne, dominikHinten] = await aufnehmen(page, path.join(QUELLEN, "visitenkarten.html"), "section.karte");
  const [brief] = await aufnehmen(page, path.join(QUELLEN, "briefpapier.html"), "section.seite");
  const [infoblatt] = await aufnehmen(page, path.join(QUELLEN, "partner-infoblatt.html"), "section.seite");
  const [aushang] = await aufnehmen(page, path.join(QUELLEN, "aushang.html"), "section.seite");
  const [signatur] = await aufnehmen(page, SIGNATUR, "body > table");
  await page.close();

  const karten = (vorne, hinten) =>
    `<div class="paar"><div><h3>vorne</h3>${bild(vorne)}</div><div><h3>hinten</h3>${bild(hinten)}</div></div>`;

  await speichern(browser, 1706, uebersicht(1706, "Druckvorlagen 1/2: Flyer und Visitenkarten",
    `<div class="reihe">
      ${bereich("1 Flyer – Außenseite (Seite 4 | Seite 1)", bild(aussen))}
      ${bereich("1 Flyer – Innenseite (Seite 2 | Seite 3)", bild(innen))}
    </div>
    <div class="reihe">
      ${bereich("2 Visitenkarte Julian Wehner", karten(julianVorne, julianHinten))}
      ${bereich("2 Visitenkarte Dominik Vogel", karten(dominikVorne, dominikHinten))}
    </div>`), "vorschau-flyer-visitenkarten.png");

  await speichern(browser, 1218, uebersicht(1218, "Druckvorlagen 2/2: Briefpapier, Word, Infoblatt, Aushang, Signatur",
    `<div class="reihe">
      ${bereich("3 Briefpapier (PDF)", bild(brief))}
      ${bereich("3 Word-Vorlage (Beispiel)", `<div class="word schatten">${bild({ src: wordSrc }, "")}</div>`)}
    </div>
    <div class="reihe">
      ${bereich("4 Partner-Infoblatt", bild(infoblatt))}
      ${bereich("5 Aushang", bild(aushang))}
    </div>
    <div>
      ${bereich("6 E-Mail-Signatur", `<div class="signatur schatten"><img src="${signatur.src}" alt="" style="width:${signatur.breite}px" /></div>`)}
    </div>`), "vorschau-brief-infoblatt-aushang-signatur.png");

  await browser.close();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
