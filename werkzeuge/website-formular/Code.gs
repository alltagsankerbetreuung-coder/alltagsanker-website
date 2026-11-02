/**
 * Alltagsfels – Website-Formular
 *
 * Nimmt Anfragen (kontakt.html) und Bewerbungen (mitarbeiten.html) von der
 * Website entgegen und schickt sie als E-Mail an das Google-Konto, unter dem
 * dieses Skript bereitgestellt ist. Es speichert nichts dauerhaft und schreibt
 * keine Inhalte in Protokolle.
 *
 * Bereitstellen (einmalig, Anleitung in LIESMICH.md):
 *   Bereitstellen → Neue Bereitstellung → Typ „Web-App“
 *   Ausführen als: „Ich“   ·   Zugriff: „Jeder“
 *
 * Diese Datei ist öffentlich auf GitHub. Hier gehören keine Passwörter hinein.
 */

var VERSION = "2026-11-01";

// Leer lassen: Die Nachrichten gehen an das eigene Konto.
// Sonst eine Adresse eintragen, z. B. "kontakt@alltagsfels.de".
var EMPFAENGER = "";

var WEBSITE = "https://alltagsfels.de";
var HOECHSTENS_PRO_STUNDE = 30; // Schutz gegen Massen-Einsendungen

// Erlaubte Felder und ihre größte Länge (wie in den Formularen der Website)
var FELDER = {
  Name: 120,
  Telefon: 40,
  email: 254,
  Stadt: 80,
  Wohnort: 80,
  Nachricht: 4000
};

var MELDUNG_FEHLER = "Ihre Nachricht konnte gerade nicht gesendet werden.";

/** Formular wurde abgeschickt. */
function doPost(e) {
  var p = (e && e.parameter) || {};
  var alsJson = p.antwort === "json";
  try {
    // Falle für Programme: Das unsichtbare Feld füllt kein Mensch aus.
    // So tun, als hätte es geklappt, aber nichts senden.
    if (p._honey) return antwort_(alsJson, true);

    var art = p.art === "bewerbung" ? "bewerbung" : "anfrage";
    var d = {};
    Object.keys(FELDER).forEach(function (feld) {
      d[feld] = saeubern_(p[feld], FELDER[feld], feld === "Nachricht");
    });

    if (!d.Name) return antwort_(alsJson, false, "Bitte geben Sie Ihren Namen an.");
    if (!d.Telefon && !d.email) {
      return antwort_(alsJson, false, "Bitte geben Sie Ihre Telefonnummer oder Ihre E-Mail-Adresse an.");
    }
    if (d.email && !emailOk_(d.email)) {
      return antwort_(alsJson, false, "Bitte prüfen Sie Ihre E-Mail-Adresse.");
    }
    if (d.Telefon && (d.Telefon.match(/[0-9]/g) || []).length < 5) {
      return antwort_(alsJson, false, "Bitte prüfen Sie Ihre Telefonnummer.");
    }
    if (art === "bewerbung" && !d.Nachricht) {
      return antwort_(alsJson, false, "Bitte schreiben Sie uns ein paar Sätze über sich.");
    }
    if (zuViele_()) {
      return antwort_(alsJson, false, "Gerade kommen sehr viele Nachrichten an. Bitte versuchen Sie es später noch einmal.");
    }

    senden_(art, d);
    return antwort_(alsJson, true);
  } catch (fehler) {
    // Nur die Fehlerart protokollieren, nie die Inhalte des Formulars
    console.error("Website-Formular: " + (fehler && fehler.name ? fehler.name : "Fehler"));
    return antwort_(alsJson, false, MELDUNG_FEHLER);
  }
}

/** Aufruf im Browser: zeigt, ob das Formular bereit ist (zum Testen nach dem Bereitstellen). */
function doGet() {
  return ContentService.createTextOutput(
    JSON.stringify({ ok: true, dienst: "Website-Formular Alltagsfels", version: VERSION })
  ).setMimeType(ContentService.MimeType.JSON);
}

/** Text bereinigen: Steuerzeichen entfernen, kürzen. Zeilenumbrüche nur in der Nachricht. */
function saeubern_(wert, laenge, mehrzeilig) {
  if (wert === undefined || wert === null) return "";
  var s = String(wert).replace(/\r\n?/g, "\n");
  s = mehrzeilig
    ? s.replace(/[\u0000-\u0009\u000B-\u001F\u007F-\u009F\u2028\u2029]/g, "")
    : s.replace(/[\u0000-\u001F\u007F-\u009F\u2028\u2029]+/g, " ");
  s = s.trim();
  if (mehrzeilig) s = s.replace(/\n{4,}/g, "\n\n\n");
  return s.length > laenge ? s.slice(0, laenge) : s;
}

function emailOk_(adresse) {
  return /^[^\s@<>()\[\]\\,;:"]+@[^\s@<>()\[\]\\,;:"]+\.[^\s@<>()\[\]\\,;:"]{2,}$/.test(adresse);
}

/** Höchstens HOECHSTENS_PRO_STUNDE Nachrichten pro Stunde annehmen. */
function zuViele_() {
  var sperre = LockService.getScriptLock();
  sperre.waitLock(10000);
  try {
    var speicher = CacheService.getScriptCache();
    var schluessel = "anzahl-" + Math.floor(Date.now() / 3600000);
    var anzahl = Number(speicher.get(schluessel) || 0) + 1;
    speicher.put(schluessel, String(anzahl), 3700);
    return anzahl > HOECHSTENS_PRO_STUNDE;
  } finally {
    sperre.releaseLock();
  }
}

function senden_(art, d) {
  var an = EMPFAENGER || Session.getEffectiveUser().getEmail();
  var titel = art === "bewerbung" ? "Neue Bewerbung über die Website" : "Neue Anfrage über die Website";
  var ort = art === "bewerbung" ? d.Wohnort : d.Stadt;
  var zeit = Utilities.formatDate(new Date(), "Europe/Berlin", "dd.MM.yyyy 'um' HH:mm 'Uhr'");
  var text = [
    titel,
    "",
    "Name: " + d.Name,
    "Telefon: " + (d.Telefon || "–"),
    "E-Mail: " + (d.email || "–"),
    (art === "bewerbung" ? "Wohnort: " : "Stadt: ") + (ort || "–"),
    "",
    art === "bewerbung" ? "Über sich:" : "Nachricht:",
    d.Nachricht || "–",
    "",
    "––",
    "Gesendet über das Formular auf " + WEBSITE + " am " + zeit + ".",
    art === "bewerbung"
      ? "Bewerbungen ohne Einstellung spätestens 6 Monate nach der Absage löschen."
      : "Bitte löschen, wenn die Anfrage erledigt ist und kein Vertrag daraus wird."
  ].join("\n");
  var optionen = { name: "Website Alltagsfels" };
  if (d.email && emailOk_(d.email)) optionen.replyTo = d.email;
  MailApp.sendEmail(an, titel + ": " + d.Name.slice(0, 60), text, optionen);
}

/** Antwort für die Website (JSON) oder eine einfache Seite, wenn JavaScript aus ist. */
function antwort_(alsJson, ok, fehler) {
  if (alsJson) {
    return ContentService.createTextOutput(
      JSON.stringify({ ok: ok, fehler: ok ? "" : fehler || MELDUNG_FEHLER })
    ).setMimeType(ContentService.MimeType.JSON);
  }
  var titel = ok ? "Vielen Dank. Ihre Nachricht ist bei uns angekommen." : "Ihre Nachricht ist leider noch nicht angekommen.";
  var text = ok
    ? "Wir melden uns persönlich bei Ihnen."
    : (fehler || MELDUNG_FEHLER) + " Bitte gehen Sie zurück und versuchen Sie es noch einmal, oder schreiben Sie uns eine E-Mail.";
  var seite =
    '<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><base target="_top">' +
    "<style>body{margin:0;padding:2rem 1rem;background:#fbf6ee;color:#26221e;" +
    "font:1.25rem/1.5 Verdana,system-ui,sans-serif}main{max-width:34rem;margin:0 auto}" +
    "h1{color:#2b3328;font:600 1.75rem/1.25 Georgia,serif}a{color:#80561f;font-weight:600}</style>" +
    "</head><body><main><h1>" + html_(titel) + "</h1><p>" + html_(text) + "</p>" +
    '<p><a href="' + html_(WEBSITE) + '/">Zurück zur Website von Alltagsfels</a></p></main></body></html>';
  return HtmlService.createHtmlOutput(seite)
    .setTitle("Alltagsfels")
    .addMetaTag("viewport", "width=device-width, initial-scale=1");
}

function html_(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}
