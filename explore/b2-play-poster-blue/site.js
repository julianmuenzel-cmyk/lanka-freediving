(function () {
  var toggle = document.getElementById("nav-toggle");
  var menu = document.getElementById("nav-menu");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (toggle && menu) {
    function closeMenu() {
      toggle.setAttribute("aria-expanded", "false");
      menu.classList.remove("is-open");
    }
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      menu.classList.toggle("is-open", !open);
    });
    menu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        if (window.matchMedia("(max-width: 767px)").matches) closeMenu();
      });
    });
  }

  document.querySelectorAll("form").forEach(function (form) {
    var success = form.parentElement && form.parentElement.querySelector(".form-success");
    if (!success) success = document.getElementById("form-success");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      form.hidden = true;
      if (success) success.hidden = false;
    });
  });

  if (reduce) {
    document.querySelectorAll(".jam-blob animate").forEach(function (el) { el.remove(); });
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("is-in"); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-in");
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
})();

  (function mountDirectionSwitch() {
    var path = window.location.pathname;
    var keys = ["a-record-sleeve-blue", "b2-play-poster-blue", "a-record-sleeve", "b2-play-poster"];
    var current = null;
    for (var i = 0; i < keys.length; i++) {
      if (path.indexOf("/" + keys[i]) !== -1) { current = keys[i]; break; }
    }
    if (!current) return;
    var ocean = current.indexOf("blue") !== -1;
    var sleeveId = ocean ? "a-record-sleeve-blue" : "a-record-sleeve";
    var playId = ocean ? "b2-play-poster-blue" : "b2-play-poster";
    var sleeveHref = path.split(current).join(sleeveId);
    var playHref = path.split(current).join(playId);
    if (sleeveHref.charAt(sleeveHref.length - 1) !== "/" && sleeveHref.indexOf(".", sleeveHref.lastIndexOf("/")) === -1) sleeveHref += "/";
    if (playHref.charAt(playHref.length - 1) !== "/" && playHref.indexOf(".", playHref.lastIndexOf("/")) === -1) playHref += "/";
    var isSleeve = current.indexOf("a-record-sleeve") === 0;
    var nav = document.createElement("nav");
    nav.className = "dir-switch";
    nav.setAttribute("aria-label", "Switch homepage direction");
    nav.innerHTML =
      '<a href="' + sleeveHref + '"' + (isSleeve ? ' aria-current="true"' : "") + ">Sleeve</a>" +
      '<a href="' + playHref + '"' + (!isSleeve ? ' aria-current="true"' : "") + ">B2 Play</a>";
    document.body.appendChild(nav);
  })();

