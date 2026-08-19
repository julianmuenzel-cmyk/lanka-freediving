(function () {
  'use strict';

  var nav = document.getElementById('nav');
  if (nav) {
    function onScroll() {
      nav.classList.toggle('scrolled', window.scrollY > 40);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  var toggle = document.getElementById('navToggle');
  var links = document.getElementById('navLinks');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      toggle.classList.toggle('active');
      links.classList.toggle('open');
    });
    links.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        toggle.classList.remove('active');
        links.classList.remove('open');
      });
    });
  }

  var page = document.body.dataset.page;
  if (page) {
    var activeLink = document.querySelector('[data-nav="' + page + '"]');
    if (activeLink) {
      activeLink.classList.add('active');
    }
  }

  var revealEls = document.querySelectorAll('.reveal, .reveal-stagger');
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    revealEls.forEach(function (el) {
      el.classList.add('visible');
    });
  }

  var form = document.getElementById('contactForm');
  var success = document.getElementById('formSuccess');
  if (form && success) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      form.querySelectorAll('.form__input, .form__select, .form__textarea, .btn').forEach(function (el) {
        el.style.display = 'none';
      });
      success.classList.add('show');
    });
  }

  var notifyForm = document.getElementById('notifyForm');
  var notifySuccess = document.getElementById('notifySuccess');
  if (notifyForm && notifySuccess) {
    notifyForm.addEventListener('submit', function (e) {
      e.preventDefault();
      notifyForm.querySelectorAll('.form__input, .btn').forEach(function (el) {
        el.style.display = 'none';
      });
      notifySuccess.classList.add('show');
    });
  }

  var faqItems = document.querySelectorAll('.faq__item');
  faqItems.forEach(function (item) {
    var question = item.querySelector('.faq__question');
    if (!question) return;
    question.addEventListener('click', function () {
      var isOpen = item.classList.contains('is-open');
      faqItems.forEach(function (other) {
        other.classList.remove('is-open');
      });
      if (!isOpen) {
        item.classList.add('is-open');
      }
    });
  });
})();
