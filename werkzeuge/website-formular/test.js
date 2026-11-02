// Prüft Code.gs ohne Google: Die Google-Dienste werden nachgebildet.
// Aufruf: node werkzeuge/website-formular/test.js   →   „ALLE TESTS OK“
"use strict";
const fs = require("fs");
const path = require("path");
const vm = require("vm");
const assert = require("assert");

const QUELLE = fs.readFileSync(path.join(__dirname, "Code.gs"), "utf8");

function umgebung() {
  const gesendet = [];
  const protokoll = [];
  const cache = new Map();
  const welt = {
    console: { error: (m) => protokoll.push(String(m)), log: (m) => protokoll.push(String(m)) },
    Date,
    JSON,
    Math,
    String,
    Number,
    Object,
    ContentService: {
      MimeType: { JSON: "JSON" },
      createTextOutput: (text) => ({ art: "text", text, setMimeType() { return this; } })
    },
    HtmlService: {
      createHtmlOutput: (html) => ({ art: "html", html, setTitle() { return this; }, addMetaTag() { return this; } })
    },
    MailApp: {
      fehler: null,
      sendEmail(an, betreff, text, optionen) {
        if (this.fehler) throw this.fehler;
        gesendet.push({ an, betreff, text, optionen });
      }
    },
    Session: { getEffectiveUser: () => ({ getEmail: () => "konto@example.org" }) },
    LockService: { getScriptLock: () => ({ waitLock() {}, releaseLock() {} }) },
    CacheService: {
      getScriptCache: () => ({ get: (k) => (cache.has(k) ? cache.get(k) : null), put: (k, v) => cache.set(k, v) })
    },
    Utilities: { formatDate: () => "01.01.2027 um 10:00 Uhr" }
  };
  vm.createContext(welt);
  vm.runInContext(QUELLE, welt, { filename: "Code.gs" });
  return { welt, gesendet, protokoll, cache };
}

function json(ausgabe) {
  assert.strictEqual(ausgabe.art, "text", "JSON-Antwort erwartet");
  return JSON.parse(ausgabe.text);
}

let anzahl = 0;
function test(name, fn) {
  fn();
  anzahl++;
  console.log("ok  " + name);
}

const gut = { art: "anfrage", Name: "Erika Muster", Telefon: "02041 123456", email: "erika@example.org", Stadt: "Bottrop", Nachricht: "Hallo,\nich suche Hilfe.", antwort: "json" };

test("Anfrage wird gesendet, Antwort-Adresse gesetzt", () => {
  const u = umgebung();
  const r = json(u.welt.doPost({ parameter: gut }));
  assert.deepStrictEqual(r, { ok: true, fehler: "" });
  assert.strictEqual(u.gesendet.length, 1);
  const m = u.gesendet[0];
  assert.strictEqual(m.an, "konto@example.org");
  assert.strictEqual(m.betreff, "Neue Anfrage über die Website: Erika Muster");
  assert.strictEqual(m.optionen.replyTo, "erika@example.org");
  assert.ok(m.text.includes("Stadt: Bottrop"));
  assert.ok(m.text.includes("Hallo,\nich suche Hilfe."));
});

test("Bewerbung bekommt eigenen Betreff und Wohnort", () => {
  const u = umgebung();
  const r = json(u.welt.doPost({ parameter: { art: "bewerbung", Name: "Max", email: "max@example.org", Wohnort: "Gladbeck", Nachricht: "Ich möchte mitarbeiten.", antwort: "json" } }));
  assert.strictEqual(r.ok, true);
  assert.ok(u.gesendet[0].betreff.startsWith("Neue Bewerbung über die Website"));
  assert.ok(u.gesendet[0].text.includes("Wohnort: Gladbeck"));
});

test("Falle für Programme: kein Versand, aber „ok“", () => {
  const u = umgebung();
  const r = json(u.welt.doPost({ parameter: Object.assign({}, gut, { _honey: "http://spam.example" }) }));
  assert.strictEqual(r.ok, true);
  assert.strictEqual(u.gesendet.length, 0);
});

test("Ohne Name: Fehlermeldung, kein Versand", () => {
  const u = umgebung();
  const r = json(u.welt.doPost({ parameter: Object.assign({}, gut, { Name: "   " }) }));
  assert.strictEqual(r.ok, false);
  assert.ok(r.fehler.includes("Namen"));
  assert.strictEqual(u.gesendet.length, 0);
});

test("Weder Telefon noch E-Mail: Fehlermeldung", () => {
  const u = umgebung();
  const r = json(u.welt.doPost({ parameter: Object.assign({}, gut, { Telefon: "", email: "" }) }));
  assert.strictEqual(r.ok, false);
  assert.strictEqual(u.gesendet.length, 0);
});

test("Telefon allein reicht", () => {
  const u = umgebung();
  const r = json(u.welt.doPost({ parameter: Object.assign({}, gut, { email: "" }) }));
  assert.strictEqual(r.ok, true);
  assert.strictEqual(u.gesendet[0].optionen.replyTo, undefined);
});

test("Telefon mit Zusatz („ab 18 Uhr“) wird angenommen", () => {
  const u = umgebung();
  const r = json(u.welt.doPost({ parameter: Object.assign({}, gut, { Telefon: "02041/123456 ab 18 Uhr" }) }));
  assert.strictEqual(r.ok, true);
});

test("Telefon mit zu wenig Ziffern: Fehlermeldung", () => {
  const u = umgebung();
  const r = json(u.welt.doPost({ parameter: Object.assign({}, gut, { Telefon: "123", email: "" }) }));
  assert.strictEqual(r.ok, false);
});

test("Kaputte E-Mail-Adresse: Fehlermeldung", () => {
  const u = umgebung();
  for (const falsch of ["erika@", "erika@example", "erika example.org", "a@b.c", "x@y.de\nBcc: z@q.de"]) {
    const r = json(u.welt.doPost({ parameter: Object.assign({}, gut, { email: falsch }) }));
    assert.strictEqual(r.ok, false, falsch);
  }
  assert.strictEqual(u.gesendet.length, 0);
});

test("Bewerbung ohne Text: Fehlermeldung", () => {
  const u = umgebung();
  const r = json(u.welt.doPost({ parameter: { art: "bewerbung", Name: "Max", email: "max@example.org", Nachricht: "", antwort: "json" } }));
  assert.strictEqual(r.ok, false);
});

test("Zeilenumbrüche und Steuerzeichen im Namen landen nicht im Betreff", () => {
  const u = umgebung();
  json(u.welt.doPost({ parameter: Object.assign({}, gut, { Name: "Erika\r\nBcc: boese@example.org\u0007" }) }));
  const b = u.gesendet[0].betreff;
  assert.ok(!/[\r\n\u0000-\u001f]/.test(b), b);
});

test("Zu lange Angaben werden gekürzt", () => {
  const u = umgebung();
  json(u.welt.doPost({ parameter: Object.assign({}, gut, { Name: "N".repeat(500), Nachricht: "x".repeat(9000) }) }));
  const m = u.gesendet[0];
  assert.ok(m.text.includes("Name: " + "N".repeat(120) + "\n"));
  assert.ok(!m.text.includes("x".repeat(4001)));
  assert.ok(m.betreff.length < 100);
});

test("Unbekannte Felder werden nicht übernommen", () => {
  const u = umgebung();
  json(u.welt.doPost({ parameter: Object.assign({}, gut, { Geheim: "nicht senden", _next: "https://example.org" }) }));
  assert.ok(!u.gesendet[0].text.includes("nicht senden"));
});

test("Mehr als 30 Nachrichten pro Stunde werden abgewiesen", () => {
  const u = umgebung();
  let r;
  for (let i = 0; i < 31; i++) r = json(u.welt.doPost({ parameter: gut }));
  assert.strictEqual(u.gesendet.length, 30);
  assert.strictEqual(r.ok, false);
});

test("Fehler beim Versand: freundliche Meldung, keine Inhalte im Protokoll", () => {
  const u = umgebung();
  u.welt.MailApp.fehler = Object.assign(new Error("Service invoked too many times: Erika Muster"), { name: "Exception" });
  const r = json(u.welt.doPost({ parameter: gut }));
  assert.strictEqual(r.ok, false);
  assert.ok(r.fehler.length > 10);
  assert.ok(u.protokoll.join(" ").indexOf("Erika") === -1, u.protokoll.join(" "));
});

test("Ohne JavaScript: einfache Seite, Eingaben werden nicht ungeprüft eingesetzt", () => {
  const u = umgebung();
  const a = u.welt.doPost({ parameter: Object.assign({}, gut, { antwort: undefined }) });
  assert.strictEqual(a.art, "html");
  assert.ok(a.html.includes("Vielen Dank"));
  assert.ok(a.html.includes('<base target="_top">'));
  const b = u.welt.doPost({ parameter: Object.assign({}, gut, { antwort: undefined, Name: "" }) });
  assert.ok(b.html.includes("noch nicht angekommen"));
  assert.ok(!b.html.includes("<script"));
});

test("Ohne Angaben (leerer Aufruf) stürzt nichts ab", () => {
  const u = umgebung();
  const a = u.welt.doPost(undefined);
  assert.strictEqual(a.art, "html");
  assert.strictEqual(u.gesendet.length, 0);
});

test("Aufruf im Browser (doGet) meldet Bereitschaft", () => {
  const u = umgebung();
  const r = json(u.welt.doGet());
  assert.strictEqual(r.ok, true);
  assert.strictEqual(r.dienst, "Website-Formular Alltagsfels");
});

console.log("\n" + anzahl + " Prüfungen – ALLE TESTS OK");
