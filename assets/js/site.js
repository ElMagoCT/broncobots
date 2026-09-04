/* ===========================================================
   Brophy Broncobots — site behavior

   Everything here is progressive enhancement. With JS off you get a
   normal, readable static page: no pinned tracks, no dead space, and
   every robot figure sits in its resting pose.

   Two scroll mechanisms:
     [data-rig] on .rig-track  -> pinned scrubber (tall track, sticky stage)
     [data-rig] on anything else -> inline figure, costs zero extra height
   Both feed a 0..1 progress into a named handler in RIGS.
   =========================================================== */
(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.add('js');

  var REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (REDUCED) root.classList.add('reduced');

  /* ---------------- helpers ---------------- */
  function clamp(v, a, b) { return v < (a || 0) ? (a || 0) : v > (b === undefined ? 1 : b) ? (b === undefined ? 1 : b) : v; }
  function lerp(a, b, t) { return a + (b - a) * t; }
  /* map v from [i0,i1] into 0..1, clamped */
  function seg(v, i0, i1) { return clamp((v - i0) / (i1 - i0), 0, 1); }
  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }
  function easeInOut(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function part(r, name) { return r.querySelector('[data-part="' + name + '"]'); }
  function parts(r, name) { return r.querySelectorAll('[data-part="' + name + '"]'); }
  function xf(el, s) { if (el) el.setAttribute('transform', s); }
  function attr(el, k, v) { if (el) el.setAttribute(k, v); }
  function txt(el, s) { if (el && el.textContent !== s) el.textContent = s; }
  function opa(el, v) { if (el) el.style.opacity = v; }
  function show(el, on) { if (el) el.style.opacity = on ? 1 : 0; }

  /* Draw a path in as p goes 0->1 */
  function draw(el, p) {
    if (!el) return;
    var L = el.__len || (el.__len = (el.getTotalLength ? el.getTotalLength() : 100));
    el.style.strokeDasharray = L;
    el.style.strokeDashoffset = L * (1 - clamp(p, 0, 1));
  }
  /* Move a marker along a path at 0..1 */
  function along(pathEl, t) {
    if (!pathEl || !pathEl.getPointAtLength) return { x: 0, y: 0 };
    var L = pathEl.__len || (pathEl.__len = pathEl.getTotalLength());
    return pathEl.getPointAtLength(L * clamp(t, 0, 1));
  }
  /* Quadratic bezier point — used for ball arcs */
  function qbez(p0, p1, p2, t) {
    var u = 1 - t;
    return { x: u * u * p0.x + 2 * u * t * p1.x + t * t * p2.x,
             y: u * u * p0.y + 2 * u * t * p1.y + t * t * p2.y };
  }
  function lit(nodes, n) {
    for (var i = 0; i < nodes.length; i++) nodes[i].classList.toggle('on', i < n);
  }

  /* ===========================================================
     RIG HANDLERS — one per page, all sharing the same parts
     vocabulary so they read as one machine shop.
     =========================================================== */
  var RIGS = {

    /* ---- HOME: robot drives in, elevates a hood, spins up a
       flywheel and shoots a ball through the goal. ---- */
    shooter: function (r, p) {
      var drive = easeOut(seg(p, 0, .16));
      xf(part(r, 'bot'), 'translate(' + lerp(-260, 0, drive) + ',0)');

      var aim = easeInOut(seg(p, .16, .34));
      xf(part(r, 'turret'), 'rotate(' + lerp(-4, -48, aim) + ' 372 232)');

      /* flywheel spins faster as it charges, keeps spinning after */
      var spin = seg(p, .22, .44);
      r.__spin = (r.__spin || 0) + spin * 26;
      xf(part(r, 'wheel'), 'rotate(' + (r.__spin % 360) + ' 398 206)');
      var chg = parts(r, 'charge');
      lit(chg, Math.round(spin * chg.length));

      /* ball flight */
      var fly = seg(p, .44, .74);
      var ball = part(r, 'ball');
      if (ball) {
        if (fly <= 0) { attr(ball, 'cx', 402); attr(ball, 'cy', 196); opa(ball, p > .3 ? 1 : .35); }
        else {
          var pt = qbez({ x: 402, y: 196 }, { x: 620, y: -40 }, { x: 812, y: 150 }, fly);
          attr(ball, 'cx', pt.x); attr(ball, 'cy', pt.y); opa(ball, 1);
        }
      }
      draw(part(r, 'arc'), seg(p, .44, .74));
      show(part(r, 'swish'), fly > .92);

      /* score */
      var scored = p > .72;
      txt(part(r, 'score'), scored ? '3' : '0');
      show(part(r, 'goalflash'), scored && p < .86);

      /* recoil + LEDs */
      var leds = parts(r, 'led');
      lit(leds, scored ? leds.length : Math.round(seg(p, .1, .6) * leds.length));
      txt(part(r, 'status'), p < .16 ? 'DRIVING' : p < .34 ? 'AIMING' : p < .44 ? 'SPIN-UP' : p < .72 ? 'SHOT AWAY' : 'SCORED');
    },

    /* ---- TEAMS: three robots rise to show relative scale ---- */
    scale: function (r, p) {
      ['fll', 'ftc', 'frc'].forEach(function (k, i) {
        var t = easeOut(seg(p, i * .13, i * .13 + .5));
        var g = part(r, 'bot-' + k);
        if (g) {
          var base = +g.getAttribute('data-base-y') || 0;
          xf(g, 'translate(0,' + lerp(70, 0, t) + ')');
          g.style.opacity = t;
        }
        draw(part(r, 'dim-' + k), seg(p, .2 + i * .13, .7 + i * .13));
        var lb = part(r, 'lbl-' + k);
        if (lb) lb.style.opacity = seg(p, .3 + i * .13, .6 + i * .13);
      });
      draw(part(r, 'floor-line'), seg(p, 0, .35));
    },

    /* ---- FRC: three-stage elevator telescopes up and places
       a game piece on the high goal. ---- */
    lift: function (r, p) {
      var s1 = easeInOut(seg(p, .08, .34));
      var s2 = easeInOut(seg(p, .26, .54));
      var s3 = easeInOut(seg(p, .46, .72));
      xf(part(r, 'stage1'), 'translate(0,' + lerp(0, -108, s1) + ')');
      xf(part(r, 'stage2'), 'translate(0,' + lerp(0, -104, s2) + ')');
      xf(part(r, 'stage3'), 'translate(0,' + lerp(0, -96, s3) + ')');

      /* carriage rides the top stage */
      var carry = lerp(0, -308, (s1 * 108 + s2 * 104 + s3 * 96) / 308);
      xf(part(r, 'carriage'), 'translate(0,' + carry + ')');

      /* claw opens, piece drops onto the goal */
      var open = seg(p, .72, .84);
      xf(part(r, 'jaw-l'), 'rotate(' + lerp(0, -34, open) + ' 404 118)');
      xf(part(r, 'jaw-r'), 'rotate(' + lerp(0, 34, open) + ' 452 118)');
      var drop = easeOut(seg(p, .82, .96));
      var piece = part(r, 'piece');
      if (piece) xf(piece, 'translate(' + lerp(0, 96, drop) + ',' + (carry + lerp(0, 44, drop * drop)) + ')');
      show(part(r, 'placed'), p > .95);

      /* chain travel */
      var ch = part(r, 'chain');
      if (ch) ch.style.strokeDashoffset = -(p * 160);
      txt(part(r, 'height'), Math.round(lerp(0, 78, (s1 + s2 + s3) / 3)) + ' in');
      var st = parts(r, 'stagelbl');
      lit(st, s3 > .1 ? 3 : s2 > .1 ? 2 : s1 > .1 ? 1 : 0);
    },

    /* ---- FTC: robot starts inside the 18-inch cube, then
       unfolds an arm out beyond it, which is the actual rule. ---- */
    cube: function (r, p) {
      /* cube wireframe draws itself */
      var edges = parts(r, 'cube-edge');
      for (var i = 0; i < edges.length; i++) draw(edges[i], seg(p, i * .012, i * .012 + .14));
      draw(part(r, 'cube-dim'), seg(p, .1, .26));
      var cl = part(r, 'cube-lbl'); if (cl) cl.style.opacity = seg(p, .14, .26);

      /* "legal at start" stamp */
      show(part(r, 'stamp-legal'), p > .2 && p < .46);

      /* arm unfolds: shoulder, then elbow, then intake spins */
      /* shoulder pivots at the chassis, elbow at the tip of the lower arm */
      var sh = easeInOut(seg(p, .34, .58));
      var el = easeInOut(seg(p, .48, .74));
      xf(part(r, 'arm-lower'), 'rotate(' + lerp(-95, 42, sh) + ' 300 268)');
      xf(part(r, 'arm-upper'), 'rotate(' + lerp(165, 8, el) + ' 300 152)');

      var spin = seg(p, .6, 1);
      r.__isp = (r.__isp || 0) + spin * 22;
      xf(part(r, 'intake'), 'rotate(' + (r.__isp % 360) + ' 0 0)');

      /* the arm crosses the cube boundary — call it out */
      show(part(r, 'stamp-expand'), p > .62);
      var ob = part(r, 'outside'); if (ob) ob.style.opacity = seg(p, .58, .74);
      draw(part(r, 'reach-dim'), seg(p, .66, .9));
      opa(part(r, 'reach-lbl'), seg(p, .68, .88));

      txt(part(r, 'phase'), p < .2 ? 'INSPECTION' : p < .46 ? 'MATCH START' : p < .7 ? 'DEPLOYING' : 'SCORING');
    },

    /* ---- FLL: LEGO robot drives the mission table while the
       block program assembles alongside it. ---- */
    mission: function (r, p) {
      var path = part(r, 'route');
      draw(path, p);
      var bot = part(r, 'bot');
      if (bot && path) {
        var pt = along(path, p);
        var pt2 = along(path, clamp(p + .012, 0, 1));
        var ang = Math.atan2(pt2.y - pt.y, pt2.x - pt.x) * 180 / Math.PI;
        xf(bot, 'translate(' + pt.x + ',' + pt.y + ') rotate(' + ang + ')');
      }
      /* missions complete as the robot passes them */
      var ms = parts(r, 'mission');
      for (var i = 0; i < ms.length; i++) {
        var on = p > (i + 1) / (ms.length + 1);
        ms[i].classList.toggle('done', on);
        ms[i].style.opacity = on ? 1 : .4;
      }
      /* code blocks slide in */
      var bl = parts(r, 'block');
      for (var j = 0; j < bl.length; j++) {
        var t = easeOut(seg(p, j * .18, j * .18 + .3));
        xf(bl[j], 'translate(' + lerp(-150, 0, t) + ',0)');
        bl[j].style.opacity = t;
      }
      txt(part(r, 'count'), Math.min(ms.length, Math.floor(p * (ms.length + 1))) + '/' + ms.length);
    },

    /* ---- ABOUT: the creed as a working gear train ---- */
    gears: function (r, p) {
      var a = p * 300;
      xf(part(r, 'g1'), 'rotate(' + a + ' 132 168)');
      xf(part(r, 'g2'), 'rotate(' + (-a * 0.72) + ' 300 168)');
      xf(part(r, 'g3'), 'rotate(' + (a * 0.55) + ' 462 168)');
      var lb = parts(r, 'gearlbl');
      lit(lb, Math.ceil(seg(p, .05, .8) * 3));
      for (var i = 0; i < lb.length; i++) lb[i].style.opacity = seg(p, .05 + i * .2, .3 + i * .2);
      draw(part(r, 'belt'), seg(p, .1, .7));
    },

    /* ---- LEADERSHIP: control hub sends signal down each wire ---- */
    signal: function (r, p) {
      var ws = parts(r, 'sigwire');
      for (var i = 0; i < ws.length; i++) draw(ws[i], seg(p, i * .09, i * .09 + .4));
      var ns = parts(r, 'signode');
      for (var j = 0; j < ns.length; j++) {
        var on = p > (j * .09 + .34);
        ns[j].classList.toggle('on', on);
        ns[j].style.opacity = on ? 1 : .45;
      }
      var hub = part(r, 'hub');
      if (hub) hub.style.opacity = lerp(.5, 1, seg(p, 0, .2));
      txt(part(r, 'count'), Math.min(ns.length, Math.round(seg(p, .3, .95) * ns.length)) + '/' + ns.length);
    },

    /* ---- RESULTS: alliance scoreboard fills in ---- */
    board: function (r, p) {
      var red = Math.round(easeOut(seg(p, .1, .8)) * 98);
      var blue = Math.round(easeOut(seg(p, .1, .8)) * 76);
      txt(part(r, 'red'), red);
      txt(part(r, 'blue'), blue);
      attr(part(r, 'bar-red'), 'width', Math.max(0, red * 3.1));
      attr(part(r, 'bar-blue'), 'width', Math.max(0, blue * 3.1));
      var rows = parts(r, 'brow');
      for (var i = 0; i < rows.length; i++) {
        var t = seg(p, .15 + i * .12, .45 + i * .12);
        rows[i].style.opacity = t;
        xf(rows[i], 'translate(' + lerp(-24, 0, easeOut(t)) + ',0)');
      }
      show(part(r, 'winner'), p > .84);
    },

    /* ---- PARENTS: a real 2:30 match clock, scrubbed ---- */
    matchclock: function (r, p) {
      var total = 150;                 /* 2:30 in seconds */
      var left = Math.round(total * (1 - clamp(p, 0, 1)));
      var m = Math.floor(left / 60), s = left % 60;
      txt(part(r, 'time'), m + ':' + (s < 10 ? '0' : '') + s);

      var ring = part(r, 'ring');
      if (ring) {
        var L = ring.__len || (ring.__len = ring.getTotalLength());
        ring.style.strokeDasharray = L;
        ring.style.strokeDashoffset = L * clamp(p, 0, 1);
      }

      /* phases: auto 0-30s, teleop 30-120s, endgame 120-150s */
      var elapsed = total * clamp(p, 0, 1);
      var phase = elapsed < 30 ? 0 : elapsed < 120 ? 1 : 2;
      var names = ['AUTONOMOUS', 'DRIVER-CONTROLLED', 'ENDGAME'];
      txt(part(r, 'phase'), names[phase]);
      var segs = parts(r, 'pseg');
      for (var i = 0; i < segs.length; i++) segs[i].classList.toggle('on', i <= phase);

      /* robot drives; driver appears at teleop; climbs at endgame */
      var bot = part(r, 'bot');
      var x = phase === 0 ? lerp(0, 120, elapsed / 30)
            : phase === 1 ? lerp(120, 300, (elapsed - 30) / 90)
            : 300;
      var climb = phase === 2 ? easeInOut((elapsed - 120) / 30) : 0;
      xf(bot, 'translate(' + x + ',' + lerp(0, -76, climb) + ')');
      show(part(r, 'driver'), phase >= 1);
      show(part(r, 'auto-path'), phase === 0);
      draw(part(r, 'auto-path'), seg(p, 0, .2));
      show(part(r, 'bar-climb'), phase === 2);
      txt(part(r, 'note'), phase === 0 ? 'No driver input allowed'
        : phase === 1 ? 'Two students per robot' : 'Highest-value scoring');
    },

    /* ---- SUPPORT: sponsorship as power distribution ---- */
    power: function (r, p) {
      var tr = parts(r, 'trace');
      for (var i = 0; i < tr.length; i++) {
        draw(tr[i], seg(p, i * .12, i * .12 + .45));
        tr[i].style.strokeDashoffset = (tr[i].style.strokeDashoffset || 0);
      }
      var ld = parts(r, 'loadnode');
      for (var j = 0; j < ld.length; j++) {
        var on = p > j * .12 + .38;
        ld[j].classList.toggle('on', on);
        ld[j].style.opacity = on ? 1 : .42;
      }
      var v = Math.round(lerp(0, 12.4, easeOut(seg(p, .05, .6))) * 10) / 10;
      txt(part(r, 'volts'), v.toFixed(1) + 'V');
      var bat = parts(r, 'cell');
      lit(bat, Math.round(seg(p, .05, .6) * bat.length));
    },

    /* ---- CALENDAR: a robot drives the season, month by month ---- */
    track: function (r, p) {
      draw(part(r, 'rail'), p);
      var path = part(r, 'rail');
      var bot = part(r, 'bot');
      if (bot && path) {
        var pt = along(path, p);
        xf(bot, 'translate(' + pt.x + ',' + pt.y + ')');
      }
      var ms = parts(r, 'month');
      for (var i = 0; i < ms.length; i++) {
        var on = p > i / ms.length;
        ms[i].classList.toggle('on', on);
        ms[i].style.opacity = on ? 1 : .38;
      }
      var lbls = ['AUG', 'SEP', 'OCT', 'NOV', 'DEC', 'JAN', 'FEB', 'MAR', 'APR', 'MAY'];
      txt(part(r, 'now'), lbls[Math.min(lbls.length - 1, Math.floor(p * lbls.length))]);
    },

    /* ---- BULLETIN: diagnostic panel boots up ---- */
    status: function (r, p) {
      var rows = parts(r, 'srow');
      for (var i = 0; i < rows.length; i++) {
        var on = p > i / (rows.length + 1);
        rows[i].classList.toggle('on', on);
        rows[i].style.opacity = on ? 1 : .3;
      }
      var sc = part(r, 'scan');
      if (sc) attr(sc, 'y', lerp(28, 210, (p * 2) % 1));
      txt(part(r, 'pct'), Math.round(clamp(p, 0, 1) * 100) + '%');
    },

    /* ---- DOCUMENTS: inspection checklist ticks off ---- */
    checklist: function (r, p) {
      var cs = parts(r, 'tick');
      for (var i = 0; i < cs.length; i++) draw(cs[i], seg(p, i * .13, i * .13 + .22));
      var rows = parts(r, 'crow');
      for (var j = 0; j < rows.length; j++) rows[j].style.opacity = p > j * .13 ? 1 : .45;
      var done = 0;
      for (var k = 0; k < cs.length; k++) if (p > k * .13 + .2) done++;
      txt(part(r, 'count'), done + '/' + cs.length);
      show(part(r, 'passed'), done === cs.length);
    },

    /* ---- LINKS: PCB traces light up to each pad ---- */
    traces: function (r, p) {
      var tr = parts(r, 'trace');
      for (var i = 0; i < tr.length; i++) draw(tr[i], seg(p, i * .1, i * .1 + .4));
      var pads = parts(r, 'pad');
      for (var j = 0; j < pads.length; j++) pads[j].classList.toggle('on', p > j * .1 + .3);
    },

    /* ---- 404: a wheel comes off ---- */
    wheeloff: function (r, p) {
      xf(part(r, 'wheel'), 'translate(' + p * 300 + ',0) rotate(' + p * 720 + ' 0 0)');
      xf(part(r, 'bot'), 'rotate(' + p * 9 + ' 160 180) translate(0,' + p * 12 + ')');
      opa(part(r, 'spark'), p > .12 && p < .5 ? 1 : 0);
    }
  };

  /* ===========================================================
     Engine — one rAF loop, only for rigs near the viewport
     =========================================================== */
  var live = [];
  var rigEls = [].slice.call(document.querySelectorAll('[data-rig]'));

  rigEls.forEach(function (el) {
    var name = el.getAttribute('data-rig');
    if (!RIGS[name]) return;
    el.__fn = RIGS[name];
    el.__pinned = el.classList.contains('rig-track');
    el.__steps = el.querySelector('.rig-steps');
    if (el.__steps) el.__stepEls = [].slice.call(el.__steps.querySelectorAll('li'));
  });

  function progressOf(el) {
    var r = el.getBoundingClientRect(), vh = window.innerHeight;
    if (el.__pinned) {
      var span = r.height - vh;
      return span > 0 ? clamp(-r.top / span, 0, 1) : (r.top < vh / 2 ? 1 : 0);
    }
    /* inline: 0 as it enters from the bottom, 1 as it leaves the top */
    return clamp((vh - r.top) / (vh + r.height), 0, 1);
  }

  function tick() {
    for (var i = 0; i < live.length; i++) {
      var el = live[i];
      var p = progressOf(el);
      try { el.__fn(el, p); } catch (e) { /* never let one rig break the page */ }
      if (el.__stepEls) {
        var n = el.__stepEls.length;
        for (var j = 0; j < n; j++) {
          var on = p >= (j / n) * .92;
          if (on) el.__stepEls[j].setAttribute('data-on', '');
          else el.__stepEls[j].removeAttribute('data-on');
        }
      }
    }
    if (live.length) requestAnimationFrame(tick);
    else running = false;
  }
  var running = false;
  function kick() { if (!running && live.length) { running = true; requestAnimationFrame(tick); } }

  if (rigEls.length) {
    if ('IntersectionObserver' in window) {
      var rio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          var i = live.indexOf(en.target);
          if (en.isIntersecting && i < 0) live.push(en.target);
          else if (!en.isIntersecting && i > -1) live.splice(i, 1);
        });
        kick();
      }, { rootMargin: '120px 0px' });
      rigEls.forEach(function (el) { if (el.__fn) rio.observe(el); });
    } else {
      live = rigEls.filter(function (el) { return el.__fn; });
      kick();
    }
    /* Paint one frame immediately so nothing starts blank */
    rigEls.forEach(function (el) {
      if (!el.__fn) return;
      try { el.__fn(el, progressOf(el)); } catch (e) {}
    });
  }

  /* ===========================================================
     Mobile nav
     =========================================================== */
  var burger = document.querySelector('.burger');
  var scrim = document.querySelector('.scrim');
  function closeNav() { document.body.classList.remove('nav-open'); if (burger) burger.setAttribute('aria-expanded', 'false'); }
  if (burger) burger.addEventListener('click', function () {
    var open = document.body.classList.toggle('nav-open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  if (scrim) scrim.addEventListener('click', closeNav);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeNav(); });

  [].forEach.call(document.querySelectorAll('.nav .navbtn'), function (btn) {
    btn.addEventListener('click', function (e) {
      if (window.matchMedia('(min-width: 1121px)').matches) return;
      e.preventDefault();
      var li = btn.parentNode, was = li.classList.contains('open');
      [].forEach.call(document.querySelectorAll('.nav li.open'), function (o) { o.classList.remove('open'); });
      if (!was) li.classList.add('open');
    });
  });

  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 6); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ===========================================================
     Reveal — with a fail-safe so content can never stay hidden
     =========================================================== */
  var revs = document.querySelectorAll('.rev');
  if (revs.length) {
    if ('IntersectionObserver' in window && !REDUCED) {
      var io = new IntersectionObserver(function (en) {
        en.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
      }, { rootMargin: '0px 0px -6% 0px', threshold: .05 });
      [].forEach.call(revs, function (el) { io.observe(el); });
      setTimeout(function () { [].forEach.call(revs, function (el) { el.classList.add('in'); }); }, 2500);
    } else {
      [].forEach.call(revs, function (el) { el.classList.add('in'); });
    }
  }

  /* ---- Count-up numbers ---- */
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length && 'IntersectionObserver' in window && !REDUCED) {
    var cio = new IntersectionObserver(function (en) {
      en.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target, target = parseFloat(el.getAttribute('data-count'));
        var suf = el.getAttribute('data-suffix') || '', st = null;
        (function run(ts) {
          if (st === null) st = ts;
          var t = Math.min((ts - st) / 1000, 1);
          el.textContent = Math.round(target * easeOut(t)).toLocaleString() + suf;
          if (t < 1) requestAnimationFrame(run);
        })(performance.now());
        cio.unobserve(el);
      });
    }, { threshold: .4 });
    [].forEach.call(counters, function (el) { cio.observe(el); });
  }

  /* ===========================================================
     Interactive widgets
     =========================================================== */

  /* Chip switchers.
       data-chips="<figure selector>"   -> highlights [data-module] inside it
       data-panels="<panels selector>"  -> shows the matching [data-panel]
     The two live in different containers, so they are addressed separately. */
  [].forEach.call(document.querySelectorAll('[data-chips]'), function (group) {
    var figure = document.querySelector(group.getAttribute('data-chips'));
    var panelScope = group.getAttribute('data-panels')
      ? document.querySelector(group.getAttribute('data-panels'))
      : figure;
    if (!figure && !panelScope) return;
    var chips = [].slice.call(group.querySelectorAll('.chip'));
    function select(key) {
      chips.forEach(function (c) { c.setAttribute('aria-selected', c.getAttribute('data-key') === key ? 'true' : 'false'); });
      if (panelScope) {
        [].forEach.call(panelScope.querySelectorAll('[data-panel]'), function (pn) {
          pn.hidden = pn.getAttribute('data-panel') !== key;
        });
      }
      if (figure) {
        [].forEach.call(figure.querySelectorAll('[data-module]'), function (m) {
          m.classList.toggle('sel', m.getAttribute('data-module') === key);
        });
      }
    }
    chips.forEach(function (c) {
      c.addEventListener('click', function () { select(c.getAttribute('data-key')); });
    });
    var first = chips.filter(function (c) { return c.getAttribute('aria-selected') === 'true'; })[0] || chips[0];
    if (first) select(first.getAttribute('data-key'));
  });

  /* Manual scrubbers: <input type=range data-scrub="#rigId"> drives a rig by hand */
  [].forEach.call(document.querySelectorAll('[data-scrub]'), function (input) {
    var target = document.querySelector(input.getAttribute('data-scrub'));
    if (!target || !target.__fn) return;
    var i = live.indexOf(target);
    if (i > -1) live.splice(i, 1);           /* hand control to the slider */
    var apply = function () {
      var p = (+input.value) / 100;
      try { target.__fn(target, p); } catch (e) {}
      var out = document.querySelector(input.getAttribute('data-scrub') + '-out');
      if (out) out.textContent = Math.round(p * 100) + '%';
    };
    input.addEventListener('input', apply);
    apply();
  });

  /* ---- Countdown ---- */
  var cd = document.querySelector('[data-countdown]');
  if (cd) {
    var when = new Date(cd.getAttribute('data-countdown'));
    var render = function () {
      if (isNaN(when.getTime())) { cd.textContent = 'see the calendar'; return; }
      var diff = when - new Date();
      if (diff <= 0) { cd.textContent = 'happening now'; return; }
      var d = Math.floor(diff / 864e5), h = Math.floor(diff % 864e5 / 36e5), mm = Math.floor(diff % 36e5 / 6e4);
      cd.textContent = (d ? d + 'd ' : '') + h + 'h ' + mm + 'm';
    };
    render(); setInterval(render, 30000);
  }

  /* ---- Placeholder forms ---- */
  [].forEach.call(document.querySelectorAll('form[data-placeholder-form]'), function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var n = form.querySelector('.form-result');
      if (!n) { n = document.createElement('div'); n.className = 'form-result note gold mt2'; form.appendChild(n); }
      n.innerHTML = '<h4>Not wired up yet</h4><p>This form is a placeholder &mdash; nothing was sent. ' +
        'Point it at Netlify Forms, a Google Form, or the team inbox before launch.</p>';
      n.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });
})();
