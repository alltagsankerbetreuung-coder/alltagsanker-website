// Alltagsfels – kleine Helfer für alle Seiten

// Aktuelles Jahr im Fußbereich
document.querySelectorAll(".year").forEach(function (el) {
  el.textContent = new Date().getFullYear();
});

// Menü auf dem Handy auf- und zuklappen
var toggle = document.querySelector(".nav-toggle");
var nav = document.getElementById("hauptmenue");
if (toggle && nav) {
  toggle.addEventListener("click", function () {
    var open = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!open));
    nav.classList.toggle("is-open", !open);
  });
}

// Inhalte beim Scrollen sanft einblenden
var items = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window) {
  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
  );
  items.forEach(function (el) {
    observer.observe(el);
  });
} else {
  items.forEach(function (el) {
    el.classList.add("is-visible");
  });
}
