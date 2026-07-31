/* stage.js — トップページの見せ場。
   1. ローディング(0.8秒で抜ける)
   2. 暗室ヒーロー: 5面の視差 + Indexホバーで該当作品が手前に来る
   3. 展示: 実物の帯をスクロールで送り、画面全体を作品の色に染める

   モーション停止時(html.is-motion-off)は transform を書かない。
   CSS側で !important による打ち消しもしてあるが、JSでも書き込みを止める。 */

(function () {
  "use strict";

  var root = document.documentElement;
  var WORKS = window.WORKS || [];
  var bySlug = {};
  WORKS.forEach(function (w) { bySlug[w.slug] = w; });

  var motionOff = function () { return root.classList.contains("is-motion-off"); };

  /* ---------- 1. ローディング ---------- */
  function initLoader() {
    var loader = document.getElementById("loader");
    if (!loader) return;
    var done = function () {
      setTimeout(function () { loader.classList.add("is-done"); }, 800);
    };
    if (document.readyState === "complete") done();
    else window.addEventListener("load", done);
    // 画像待ちで永久に残らないよう保険をかける
    setTimeout(function () { loader.classList.add("is-done"); }, 2600);
  }

  /* ---------- 2. 暗室ヒーロー ---------- */
  function initHero() {
    var field = document.getElementById("hero-field");
    if (!field) return;
    var planes = Array.prototype.slice.call(field.querySelectorAll(".hero__plane"));

    // 奥行きに応じて霞ませる(手前=くっきり、奥=沈む)
    planes.forEach(function (p) {
      var z = parseFloat(p.style.getPropertyValue("--z")) || 0;
      var depth = Math.min(1, Math.abs(z) / 1100);
      p.style.setProperty("--plane-blur", (depth * 3.2).toFixed(2) + "px");
      p.style.setProperty("--plane-opacity", (0.85 - depth * 0.42).toFixed(2));
    });

    var tx = 0, ty = 0, cx = 0, cy = 0, raf = null;

    function loop() {
      cx += (tx - cx) * 0.06;
      cy += (ty - cy) * 0.06;
      field.style.transform = "rotateY(" + cx.toFixed(3) + "deg) rotateX(" + cy.toFixed(3) + "deg)";
      raf = Math.abs(tx - cx) > 0.01 || Math.abs(ty - cy) > 0.01 ? requestAnimationFrame(loop) : null;
    }

    function kick() {
      if (motionOff()) return;
      if (!raf) raf = requestAnimationFrame(loop);
    }

    window.addEventListener("pointermove", function (e) {
      if (motionOff()) return;
      var nx = e.clientX / window.innerWidth - 0.5;
      var ny = e.clientY / window.innerHeight - 0.5;
      tx = nx * 9;
      ty = -ny * 6;
      kick();
    }, { passive: true });

    // Indexの行にホバー/フォーカスすると、その作品だけが手前に出る
    var rows = document.querySelectorAll("#work-index .index-row");
    Array.prototype.forEach.call(rows, function (row) {
      var slug = row.dataset.slug;
      var work = bySlug[slug];
      var link = row.querySelector("a");
      if (!link) return;
      if (work) link.style.setProperty("--index-accent", work.theme.accent);

      var enter = function () {
        planes.forEach(function (p) {
          var hit = p.dataset.slug === slug;
          p.classList.toggle("is-front", hit);
          p.style.setProperty("--z-boost", hit ? "1" : "0");
          if (!motionOff()) {
            p.style.transform =
              "translate3d(calc(-50% + var(--x) * 1px), calc(-50% + var(--y) * 1px), calc(var(--z) * 1px + " +
              (hit ? 520 : 0) + "px)) rotateY(" + (hit ? "0deg" : "var(--rot)") + ")";
          }
        });
      };
      var leave = function () {
        planes.forEach(function (p) {
          p.classList.remove("is-front");
          p.style.transform = "";
        });
      };
      link.addEventListener("pointerenter", enter);
      link.addEventListener("focus", enter);
      link.addEventListener("pointerleave", leave);
      link.addEventListener("blur", leave);
    });
  }

  /* ---------- 3. 展示 ---------- */

  // モバイルは帯を流さない。
  // スマホ版の実ページは2万px超あり、短い窓を高速で送ると余白しか映らないうえ、
  // 画像も重い。モバイルでは端末枠にファーストビューを1枚だけ置く。
  var isNarrow = window.matchMedia("(max-width: 767px)").matches;

  function mountStrip(section) {
    var work = bySlug[section.dataset.slug];
    var holder = section.querySelector("[data-strip]");
    if (!work || !holder || holder.dataset.mounted) return;
    holder.dataset.mounted = "1";

    var frame = section.querySelector(".viewport");
    var base = "assets/img/works/" + work.slug + "/";

    if (isNarrow) {
      if (frame) frame.classList.add("viewport--sp");
      var cover = document.createElement("img");
      cover.src = base + "cover-sp.webp";
      cover.alt = work.name + "のスマートフォン表示";
      cover.width = 560;
      cover.height = 1212;
      cover.loading = "lazy";
      cover.decoding = "async";
      holder.appendChild(cover);
      return; // ratio を持たせない = 送りの対象外
    }

    var strip = work.strip.pc;
    strip.tiles.forEach(function (file, i) {
      var img = document.createElement("img");
      img.src = base + file;
      img.alt = i === 0 ? work.name + "のページ全体" : "";
      img.width = strip.w;
      img.loading = "lazy";
      img.decoding = "async";
      holder.appendChild(img);
    });
    holder.dataset.ratio = String(strip.h / strip.w);
  }

  function initExhibits() {
    var sections = Array.prototype.slice.call(document.querySelectorAll(".js-exhibit"));
    if (!sections.length) return;

    // 帯は近づいてから積む(初期表示を軽くする)
    var mounter = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            mountStrip(e.target);
            mounter.unobserve(e.target);
          }
        });
      },
      { rootMargin: "120% 0px" }
    );
    sections.forEach(function (s) { mounter.observe(s); });

    // 画面をどの作品の色に染めるか
    var shell = {
      bg: "#0a0b0d", ink: "#e8e6e1", accent: "#8b8a86",
      display: 'var(--font-display)',
    };
    var current = null;

    function paint(theme) {
      if (current === theme) return;
      current = theme;
      root.style.setProperty("--stage-bg", theme.bg);
      root.style.setProperty("--stage-ink", theme.ink);
      root.style.setProperty("--stage-accent", theme.accent);
      root.style.setProperty("--stage-display", theme.display);
      root.dataset.stageScheme = theme.scheme || "dark";
    }

    // 帯の送りと配色の切り替えを1本のrAFにまとめる
    var ticking = false;
    function update() {
      ticking = false;
      var vh = window.innerHeight;
      var active = null;

      sections.forEach(function (section) {
        var rect = section.getBoundingClientRect();
        // stickyが効いている区間 = セクションが画面をまたいでいる間
        var span = rect.height - vh;
        if (span <= 0) return;
        var p = Math.min(1, Math.max(0, -rect.top / span));

        if (rect.top <= vh * 0.5 && rect.bottom >= vh * 0.5) active = section;

        if (motionOff()) return;
        var holder = section.querySelector("[data-strip]");
        if (!holder || !holder.dataset.ratio) return;
        var screen = section.querySelector(".viewport__screen");
        if (!screen) return;
        var stripH = screen.clientWidth * parseFloat(holder.dataset.ratio);
        var travel = Math.max(0, stripH - screen.clientHeight);
        // 上下に少し余韻を残す(端で張り付いて見えないように)
        var eased = Math.min(1, Math.max(0, (p - 0.08) / 0.84));
        holder.style.transform = "translate3d(0," + (-travel * eased).toFixed(1) + "px,0)";
      });

      if (active) {
        var w = bySlug[active.dataset.slug];
        if (w) paint(w.theme);
      } else {
        paint(shell);
      }
    }

    function onScroll() {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    update();
  }

  function boot() {
    initLoader();
    initHero();
    initExhibits();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
