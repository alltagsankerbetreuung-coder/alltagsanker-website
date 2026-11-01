// Alltagsfels – kleine Helfer für alle Seiten.
// Alle Inhalte sind auch ohne JavaScript sichtbar. Dieses Skript ergänzt nur
// Menü, Schriftgröße, Drucken und die Formular-Anzeige.

// Zeichen für die Sicherung im Kopf der Seiten: Skript ist geladen
window.alltagsfelsBereit = true;

// Aktuelles Jahr im Fußbereich
document.querySelectorAll(".year").forEach(function (el) {
  el.textContent = new Date().getFullYear();
});

// Menü auf- und zuklappen (solange die volle Navigation nicht in eine Zeile passt)
var kopf = document.querySelector(".kopf");
var menueKnopf = document.querySelector(".menue-knopf");
var menue = document.getElementById("hauptmenue");
function menueIstOffen() {
  return !!menueKnopf && menueKnopf.getAttribute("aria-expanded") === "true";
}
function menueSetzen(offen, fokusZurueck) {
  if (!menueKnopf || !menue) return;
  if (offen && kopf) {
    // Die Fläche beginnt direkt unter dem Kopf und reicht bis zum unteren Rand
    var unten = Math.max(0, Math.round(kopf.getBoundingClientRect().bottom));
    document.documentElement.style.setProperty("--menue-oben", unten + "px");
  }
  menueKnopf.setAttribute("aria-expanded", String(offen));
  menue.classList.toggle("ist-offen", offen);
  document.documentElement.classList.toggle("menue-offen", offen);
  if (offen) {
    var erster = menue.querySelector("a");
    if (erster) erster.focus();
  } else if (fokusZurueck) {
    menueKnopf.focus();
  }
}
if (menueKnopf && menue) {
  menueKnopf.addEventListener("click", function () {
    menueSetzen(!menueIstOffen(), false);
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && menueIstOffen()) {
      menueSetzen(false, true);
    }
  });
  menue.addEventListener("click", function (event) {
    if (event.target.closest("a")) menueSetzen(false, false);
  });
  // Verlässt der Fokus Menü und Menü-Knopf, schließt das Menü
  [menue, menueKnopf].forEach(function (el) {
    el.addEventListener("focusout", function (event) {
      var ziel = event.relatedTarget;
      if (!menueIstOffen() || !ziel) return;
      if (!menue.contains(ziel) && ziel !== menueKnopf) menueSetzen(false, false);
    });
  });
  // Wird der Knopf unsichtbar (breiteres Fenster), Menü schließen
  window.addEventListener("resize", function () {
    if (menueIstOffen() && menueKnopf.offsetParent === null) menueSetzen(false, false);
  });
}

// Kopf beim Scrollen schmaler, mit Haarlinie
if (kopf) {
  var kopfPruefen = function () {
    kopf.classList.toggle("ist-klein", window.scrollY > 48);
  };
  kopfPruefen();
  window.addEventListener("scroll", kopfPruefen, { passive: true });
}

// Schalter „Schrift größer“: Stufen 1 bis 3, gespeichert, wenn der Browser es erlaubt
var schriftKnoepfe = document.querySelectorAll("[data-schrift]");
function schriftSetzen(stufe) {
  var html = document.documentElement;
  html.classList.remove("schrift-2", "schrift-3");
  if (stufe === "2" || stufe === "3") html.classList.add("schrift-" + stufe);
  schriftKnoepfe.forEach(function (knopf) {
    knopf.setAttribute("aria-pressed", String(knopf.getAttribute("data-schrift") === stufe));
  });
  if (menueIstOffen() && menueKnopf.offsetParent === null) menueSetzen(false, false);
}
if (schriftKnoepfe.length) {
  var gespeichert = "1";
  try {
    gespeichert = localStorage.getItem("alltagsfels-schrift") || "1";
  } catch (e) {}
  schriftSetzen(gespeichert);
  schriftKnoepfe.forEach(function (knopf) {
    knopf.addEventListener("click", function () {
      var stufe = knopf.getAttribute("data-schrift");
      schriftSetzen(stufe);
      try {
        localStorage.setItem("alltagsfels-schrift", stufe);
      } catch (e) {}
    });
  });
}

// „Seite ausdrucken“ – mit data-drucken="id" nur dieser Abschnitt (plus Kontakt im Fuß)
var druckZiel = null;
function druckTeilAufheben() {
  document.documentElement.classList.remove("druck-teil");
  if (druckZiel) druckZiel.classList.remove("druck-ziel");
  druckZiel = null;
}
document.querySelectorAll("[data-drucken]").forEach(function (knopf) {
  knopf.addEventListener("click", function () {
    var id = knopf.getAttribute("data-drucken");
    var abschnitt = id ? document.getElementById(id) : null;
    if (abschnitt) {
      druckZiel = abschnitt;
      abschnitt.classList.add("druck-ziel");
      document.documentElement.classList.add("druck-teil");
    }
    window.print();
    // Manche Browser feuern „afterprint“ nicht zuverlässig
    setTimeout(druckTeilAufheben, 1000);
  });
});
window.addEventListener("afterprint", druckTeilAufheben);

// Beim Drucken alle Antworten der Fragen zeigen, danach wie vorher
var geschlosseneFragen = [];
window.addEventListener("beforeprint", function () {
  geschlosseneFragen = Array.prototype.filter.call(document.querySelectorAll("details"), function (d) {
    return !d.open;
  });
  geschlosseneFragen.forEach(function (d) { d.open = true; });
});
window.addEventListener("afterprint", function () {
  geschlosseneFragen.forEach(function (d) { d.open = false; });
  geschlosseneFragen = [];
});

// Formulare: Telefon oder E-Mail prüfen, Nachricht senden, doppeltes Absenden verhindern.
// Die Nachricht geht an das eigene Website-Formular im Google-Konto der Firma
// (Adresse steht im action-Attribut, Anleitung in werkzeuge/website-formular/).
// Ohne JavaScript schickt der Browser das Formular ganz normal ab.
var FORMULAR_FEHLT = "FORMULAR-NOCH-NICHT-EINGERICHTET";

function knopfSetzen(button, wartet) {
  if (!button) return;
  if (wartet) {
    if (!button.dataset.label) button.dataset.label = button.lastChild.textContent;
    button.disabled = true;
    button.setAttribute("aria-busy", "true");
    button.lastChild.textContent = " Wird gesendet …";
  } else {
    button.disabled = false;
    button.removeAttribute("aria-busy");
    if (button.dataset.label) button.lastChild.textContent = button.dataset.label;
  }
}

document.querySelectorAll("form.contact-form").forEach(function (form) {
  var mail = form.querySelector('input[type="email"]');
  var telefon = form.querySelector('input[type="tel"]');
  var fehler = form.querySelector(".erreichbar-fehler");
  var sendeFehler = form.querySelector(".senden-fehler");
  var sendeGrund = form.querySelector(".senden-grund");
  var button = form.querySelector('button[type="submit"]');

  function erreichbarPruefen() {
    if (!mail || !telefon || !fehler) return true;
    var ok = mail.value.trim() !== "" || telefon.value.trim() !== "";
    fehler.hidden = ok;
    [mail, telefon].forEach(function (feld) {
      if (ok) feld.removeAttribute("aria-invalid");
      else feld.setAttribute("aria-invalid", "true");
    });
    return ok;
  }
  [mail, telefon].forEach(function (feld) {
    if (feld) feld.addEventListener("input", function () {
      if (fehler && !fehler.hidden) erreichbarPruefen();
    });
  });

  function sendenFehlgeschlagen(grund) {
    knopfSetzen(button, false);
    if (!sendeFehler) return;
    if (sendeGrund) sendeGrund.textContent = grund || "";
    sendeFehler.hidden = false;
    sendeFehler.focus();
  }

  form.addEventListener("submit", function (event) {
    if (!erreichbarPruefen()) {
      event.preventDefault();
      (telefon || mail).focus();
      return;
    }
    if (button && button.disabled) {
      event.preventDefault();
      return;
    }
    if (sendeFehler) sendeFehler.hidden = true;
    // Sehr alte Browser: normal absenden, das Formular-Programm zeigt dann selbst eine Danke-Seite
    if (!window.fetch || !window.URLSearchParams || !window.FormData) {
      knopfSetzen(button, true);
      return;
    }
    event.preventDefault();
    knopfSetzen(button, true);
    if (form.action.indexOf(FORMULAR_FEHLT) !== -1) {
      sendenFehlgeschlagen("Das Formular wird gerade eingerichtet.");
      return;
    }
    var daten = new URLSearchParams(new FormData(form));
    daten.set("antwort", "json");
    fetch(form.action, { method: "POST", body: daten, credentials: "omit", referrerPolicy: "origin" })
      .then(function (antwort) {
        if (!antwort.ok) throw new Error("HTTP " + antwort.status);
        return antwort.json();
      })
      .then(function (ergebnis) {
        if (ergebnis && ergebnis.ok === true) {
          window.location.href = new URL(form.getAttribute("data-danke") || "danke.html", window.location.href).href;
        } else {
          sendenFehlgeschlagen(ergebnis && typeof ergebnis.fehler === "string" ? ergebnis.fehler : "");
        }
      })
      .catch(function () {
        sendenFehlgeschlagen("");
      });
  });
});

// Nach dem Zurückblättern den Senden-Knopf wieder freigeben
window.addEventListener("pageshow", function (event) {
  if (!event.persisted) return;
  document.querySelectorAll("form.contact-form button[type=\"submit\"]").forEach(function (button) {
    knopfSetzen(button, false);
  });
});

// Danke-Seite: Nach einer Bewerbung (danke.html?bewerbung) die passenden Schritte zeigen
(function () {
  var kunden = document.getElementById("weiter-kunden");
  var bewerbung = document.getElementById("weiter-bewerbung");
  if (!kunden || !bewerbung) return;
  if (/(^|[?&])bewerbung(=|&|$)/.test(window.location.search)) {
    kunden.hidden = true;
    bewerbung.hidden = false;
  }
})();
