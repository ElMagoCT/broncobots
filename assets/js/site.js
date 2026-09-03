/* Brophy Broncobots — site behavior
   Progressive enhancement only: every page works with JS disabled. */
(function () {
  'use strict';

  /* ---- Mobile nav ---- */
  var burger = document.querySelector('.burger');
  var scrim = document.querySelector('.scrim');
  function closeNav() { document.body.classList.remove('nav-open'); if (burger) burger.setAttribute('aria-expanded', 'false'); }
  if (burger) {
    burger.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
  if (scrim) scrim.addEventListener('click', closeNav);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeNav(); });

  /* ---- Dropdowns: click to toggle on touch / narrow screens ---- */
  Array.prototype.forEach.call(document.querySelectorAll('.nav .navbtn'), function (btn) {
    btn.addEventListener('click', function (e) {
      if (window.matchMedia('(min-width: 1081px)').matches) return; // hover handles it
      e.preventDefault();
      var li = btn.parentNode;
      var wasOpen = li.classList.contains('open');
      Array.prototype.forEach.call(document.querySelectorAll('.nav li.open'), function (o) { o.classList.remove('open'); });
      if (!wasOpen) li.classList.add('open');
    });
  });

  /* ---- Header shadow on scroll ---- */
  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---- Scroll reveal ---- */
  var revealables = document.querySelectorAll('.reveal');
  if (revealables.length) {
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
      Array.prototype.forEach.call(revealables, function (el) { io.observe(el); });
      // Fail-safe: never leave content invisible. If the observer has not fired
      // (background tab, odd embedding context, slow load), just show everything.
      setTimeout(function () {
        Array.prototype.forEach.call(revealables, function (el) { el.classList.add('in'); });
      }, 2500);
    } else {
      Array.prototype.forEach.call(revealables, function (el) { el.classList.add('in'); });
    }
  }

  /* ---- Count-up stats ---- */
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length && 'IntersectionObserver' in window &&
      !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, target = parseFloat(el.getAttribute('data-count'));
        var suffix = el.getAttribute('data-suffix') || '';
        var start = null, dur = 1100;
        function tick(ts) {
          if (start === null) start = ts;
          var p = Math.min((ts - start) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(target * eased).toLocaleString() + suffix;
          if (p < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
        cio.unobserve(el);
      });
    }, { threshold: 0.4 });
    Array.prototype.forEach.call(counters, function (el) { cio.observe(el); });
  }

  /* ---- Next-meeting countdown (calendar page) ---- */
  var cd = document.querySelector('[data-countdown]');
  if (cd) {
    var when = new Date(cd.getAttribute('data-countdown'));
    var render = function () {
      var diff = when - new Date();
      if (isNaN(when.getTime())) { cd.textContent = 'See the calendar below'; return; }
      if (diff <= 0) { cd.textContent = 'Happening now'; return; }
      var d = Math.floor(diff / 864e5),
          h = Math.floor(diff % 864e5 / 36e5),
          m = Math.floor(diff % 36e5 / 6e4);
      cd.textContent = (d ? d + 'd ' : '') + h + 'h ' + m + 'm';
    };
    render();
    setInterval(render, 30000);
  }

  /* ---- Gallery / roster filters ---- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-filter-group]'), function (group) {
    var buttons = group.querySelectorAll('[data-filter]');
    var targetSel = group.getAttribute('data-filter-group');
    var items = document.querySelectorAll(targetSel + ' [data-tags]');
    Array.prototype.forEach.call(buttons, function (b) {
      b.addEventListener('click', function () {
        Array.prototype.forEach.call(buttons, function (x) { x.classList.remove('btn'); x.classList.add('btn', 'ghost', 'sm'); });
        b.classList.remove('ghost');
        var f = b.getAttribute('data-filter');
        Array.prototype.forEach.call(items, function (it) {
          var tags = it.getAttribute('data-tags') || '';
          it.style.display = (f === 'all' || tags.indexOf(f) > -1) ? '' : 'none';
        });
      });
    });
  });

  /* ---- Placeholder forms: no backend yet ---- */
  Array.prototype.forEach.call(document.querySelectorAll('form[data-placeholder-form]'), function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var note = form.querySelector('.form-result');
      if (!note) {
        note = document.createElement('div');
        note.className = 'form-result callout gold mt2';
        form.appendChild(note);
      }
      note.innerHTML = '<h4>Not wired up yet</h4><p>This form is a placeholder. Nothing was sent. ' +
        'Point it at a real handler (Netlify Forms, a Google Form, or the team inbox) before launch.</p>';
      note.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });
})();
