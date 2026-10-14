// Alltagsfels – kleine Helfer für alle Seiten.
// Alle Inhalte sind auch ohne JavaScript sichtbar. Dieses Skript ergänzt nur
// Menü, Schriftgröße, Drucken und die Formular-Anzeige.

// Zeichen für die Sicherung im Kopf der Seiten: Skript ist geladen
window.alltagsfelsBereit = true;

// Aktuelles Jahr im Fußbereich
document.querySelectorAll(".year").forEach(function (el) {
  el.textContent = new Date().getFullYear();
});

// Menü unter 1024 px auf- und zuklappen
var menueKnopf = document.querySelector(".menue-knopf");
var menue = document.getElementById("hauptmenue");
function menueSetzen(offen) {
  if (!menueKnopf || !menue) return;
  menueKnopf.setAttribute("aria-expanded", String(offen));
  menue.classList.toggle("ist-offen", offen);
}
if (menueKnopf && menue) {
  menueKnopf.addEventListener("click", function () {
    menueSetzen(menueKnopf.getAttribute("aria-expanded") !== "true");
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && menueKnopf.getAttribute("aria-expanded") === "true") {
      menueSetzen(false);
      menueKnopf.focus();
    }
  });
  menue.addEventListener("click", function (event) {
    if (event.target.closest("a")) menueSetzen(false);
  });
}

// Kopf beim Scrollen schmaler, mit Haarlinie
var kopf = document.querySelector(".kopf");
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

// „Seite ausdrucken“
document.querySelectorAll("[data-drucken]").forEach(function (knopf) {
  knopf.addEventListener("click", function () {
    window.print();
  });
});

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

// Formulare: Antwort-Adresse setzen und doppeltes Absenden verhindern
document.querySelectorAll("form.contact-form").forEach(function (form) {
  form.addEventListener("submit", function () {
    var mail = form.querySelector('input[type="email"]');
    var replyto = form.querySelector(".replyto");
    if (mail && replyto) {
      replyto.value = mail.value;
    }
    var button = form.querySelector('button[type="submit"]');
    if (button) {
      button.dataset.label = button.lastChild.textContent;
      button.disabled = true;
      button.setAttribute("aria-busy", "true");
      button.lastChild.textContent = " Wird gesendet …";
    }
  });
});

// Nach dem Zurückblättern den Senden-Knopf wieder freigeben
window.addEventListener("pageshow", function (event) {
  if (!event.persisted) return;
  document.querySelectorAll("form.contact-form button[disabled]").forEach(function (button) {
    button.disabled = false;
    button.removeAttribute("aria-busy");
    button.lastChild.textContent = button.dataset.label || button.lastChild.textContent;
  });
});
