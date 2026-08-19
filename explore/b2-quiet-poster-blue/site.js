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
