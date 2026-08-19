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
    document.querySelectorAll(".reveal").forEach(function (el) { el.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });
  }

  (function mountDirectionSwitch() {
    var path = window.location.pathname;
    var sleeveId = "a-record-sleeve";
    var quietId = "b2-quiet-poster";
    function isExplore(id) {
      var needle = "/" + id;
      var i = path.indexOf(needle);
      if (i === -1) return false;
      var after = path.charAt(i + needle.length);
      return after === "" || after === "/";
    }
    var inSleeveExplore = isExplore(sleeveId);
    var inQuietExplore = isExplore(quietId);
    var sleeveHref;
    var quietHref;
    var isSleeve;
    if (inSleeveExplore || inQuietExplore) {
      var current = inSleeveExplore ? sleeveId : quietId;
      sleeveHref = path.split(current).join(sleeveId);
      quietHref = path.split(current).join(quietId);
      isSleeve = inSleeveExplore;
    } else {
      var isQuiet = path === "/quiet" || path.indexOf("/quiet/") === 0;
      var rest = isQuiet ? path.replace(/^\/quiet/, "") : path;
      if (!rest) rest = "/";
      sleeveHref = rest;
      quietHref = rest === "/" ? "/quiet/" : "/quiet" + rest;
      isSleeve = !isQuiet;
    }
    function withSlash(href) {
      if (href === "/") return href;
      if (href.charAt(href.length - 1) !== "/" && href.indexOf(".", href.lastIndexOf("/")) === -1) return href + "/";
      return href;
    }
    sleeveHref = withSlash(sleeveHref);
    quietHref = withSlash(quietHref);
    var nav = document.createElement("nav");
    nav.className = "dir-switch";
    nav.setAttribute("aria-label", "Switch site design");
    nav.innerHTML =
      '<a href="' + sleeveHref + '"' + (isSleeve ? ' aria-current="true"' : "") + ">Sleeve</a>" +
      '<a href="' + quietHref + '"' + (!isSleeve ? ' aria-current="true"' : "") + ">Quiet</a>";
    document.body.appendChild(nav);
  })();

})();
