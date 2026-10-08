// Erstellt alle PDFs in druckvorlagen/pdf/ aus den HTML-Vorlagen in druckvorlagen/quellen/.
// Aufruf (aus dem Hauptordner):  node druckvorlagen/pdf-erstellen.js
// Nur bestimmte Vorlagen:  node druckvorlagen/pdf-erstellen.js flyer
// Braucht das Programm "Playwright" mit Chromium.

const path = require("path");
const { execFileSync } = require("child_process");
let chromium;
try {
  ({ chromium } = require("playwright"));
} catch (e) {
  ({ chromium } = require("/opt/node-tools/node_modules/playwright"));
}

const QUELLEN = path.join(__dirname, "quellen");
const ZIEL = path.join(__dirname, "pdf");

// Datei, Zusatz zur Adresse, PDF-Name, Breite, Höhe (jeweils mit 3 mm Beschnitt), Seiten
const AUFTRAEGE = [
  ["flyer.html", "", "flyer-a5-einzelseiten.pdf", "154mm", "216mm"],
  ["flyer.html", "?bogen", "flyer-a4-quer-druckbogen.pdf", "303mm", "216mm"],
  ["visitenkarten.html", "", "visitenkarte-julian-wehner.pdf", "91mm", "61mm", "1-2"],
  ["visitenkarten.html", "", "visitenkarte-dominik-vogel.pdf", "91mm", "61mm", "3-4"],
  ["briefpapier.html", "", "briefpapier-a4.pdf", "216mm", "303mm"],
  ["partner-infoblatt.html", "", "partner-infoblatt-a4.pdf", "216mm", "303mm"],
  ["aushang.html", "", "aushang-a4-abreisszettel.pdf", "216mm", "303mm"],
];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const filter = process.argv[2] || "";
  for (const [datei, zusatz, name, breite, hoehe, seiten] of AUFTRAEGE) {
    if (filter && !name.includes(filter)) continue;
    const url = "file://" + path.join(QUELLEN, datei) + zusatz;
    await page.goto(url, { waitUntil: "load" });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({
      path: path.join(ZIEL, name),
      width: breite,
      height: hoehe,
      printBackground: true,
      margin: { top: 0, right: 0, bottom: 0, left: 0 },
      pageRanges: seiten || "",
    });
    // exaktes Format, Endformat und Beschnitt eintragen
    execFileSync("python3", [path.join(__dirname, "pdf-zuschneiden.py"), path.join(ZIEL, name), parseFloat(breite), parseFloat(hoehe)].map(String));
    console.log("fertig:", name);
  }
  await browser.close();
})();
