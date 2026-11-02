// Alltagsfels – läuft ganz am Anfang, noch bevor die Seite gezeichnet wird.
// Setzt die gespeicherte Schriftgröße („Schrift größer“), damit nichts springt,
// und markiert, dass JavaScript läuft. Lädt script.js nicht innerhalb von
// 3 Sekunden, wird die Markierung wieder entfernt: Dann bleibt alles ohne
// Extras sichtbar und bedienbar.
(function (d) {
  d.classList.add("js");
  try {
    var s = localStorage.getItem("alltagsfels-schrift");
    if (s === "2" || s === "3") d.classList.add("schrift-" + s);
  } catch (e) {}
  setTimeout(function () {
    if (!window.alltagsfelsBereit) d.classList.remove("js");
  }, 3000);
})(document.documentElement);
