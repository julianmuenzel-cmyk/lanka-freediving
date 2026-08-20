(function () {
  var toggle = document.getElementById("nav-toggle");
  var menu = document.getElementById("nav-menu");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var small = window.matchMedia("(max-width: 767px)").matches;
  if (reduce || small) {
    document.querySelectorAll(".jam-blob animate").forEach(function (el) { el.remove(); });
  }

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

  (function mountOceanCall() {
    var path = window.location.pathname;
    if (/\/contact\/?$/.test(path) || /\/contact\/index\.html$/.test(path)) return;
    try {
      if (sessionStorage.getItem("lf-ocean-calling") === "hung") return;
    } catch (e) { /* private mode */ }

    function siteRoot() {
      var ids = ["a-record-sleeve", "b2-quiet-poster"];
      for (var i = 0; i < ids.length; i++) {
        var needle = "/" + ids[i];
        var idx = path.indexOf(needle);
        if (idx === -1) continue;
        var after = path.charAt(idx + needle.length);
        if (after === "" || after === "/") return path.slice(0, idx + needle.length) + "/";
      }
      if (path === "/quiet" || path.indexOf("/quiet/") === 0) return "/quiet/";
      return "/";
    }
    function artSrc() {
      var explore = path.indexOf("/explore/");
      if (explore !== -1) return path.slice(0, explore) + "/explore/assets/shell-phone-sleeve.png";
      return "/assets/shell-phone-sleeve.png";
    }

    var root = document.createElement("div");
    root.className = "ocean-call";
    root.id = "ocean-call";
    root.hidden = true;
    root.innerHTML =
      '<div class="ocean-call-card" role="dialog" aria-modal="true" aria-labelledby="ocean-call-title" tabindex="-1">' +
        '<button type="button" class="ocean-call-close" aria-label="Hang up">&times;</button>' +
        '<div class="ocean-call-top"><p class="ocean-call-kicker">Ring ring</p></div>' +
        '<div class="ocean-call-body">' +
          '<img class="ocean-call-art" src="' + artSrc() + '" width="712" height="823" alt="">' +
          '<h2 class="ocean-call-title" id="ocean-call-title">Hey — the ocean is calling</h2>' +
          '<p class="ocean-call-pick">Pick up.</p>' +
          '<div class="ocean-call-actions">' +
            '<a class="btn btn-solid" href="' + siteRoot() + 'contact/">Contact us</a>' +
            '<a class="btn" href="https://wa.me/940000000000" target="_blank" rel="noopener">WhatsApp</a>' +
          "</div>" +
        "</div>" +
      "</div>";
    document.body.appendChild(root);

    var card = root.querySelector(".ocean-call-card");
    var closeBtn = root.querySelector(".ocean-call-close");
    var lastFocus = null;

    function focusables() {
      return Array.prototype.slice.call(card.querySelectorAll("a, button"));
    }
    function open() {
      lastFocus = document.activeElement;
      root.hidden = false;
      document.documentElement.classList.add("ocean-call-open");
      document.body.style.overflow = "hidden";
      card.focus();
    }
    function close() {
      root.hidden = true;
      document.documentElement.classList.remove("ocean-call-open");
      document.body.style.overflow = "";
      try { sessionStorage.setItem("lf-ocean-calling", "hung"); } catch (e) { /* ignore */ }
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    closeBtn.addEventListener("click", close);
    root.addEventListener("click", function (e) {
      if (!card.contains(e.target)) close();
    });
    document.addEventListener("keydown", function (e) {
      if (root.hidden) return;
      if (e.key === "Escape") {
        e.preventDefault();
        close();
        return;
      }
      if (e.key !== "Tab") return;
      var items = focusables();
      if (!items.length) return;
      var first = items[0];
      var last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    });

    window.setTimeout(open, reduce ? 400 : 1800);
  })();

})();
