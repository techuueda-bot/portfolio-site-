/* main.js — スターター基盤
   構成: reveal / ヘッダー状態 / ハンバーガー / フォーム検証 / モーション停止
   GSAP等を足す場合もこのファイルの仕組みは残す(削除禁止箇所はコメント参照) */

document.addEventListener("DOMContentLoaded", () => {
  initLegacyAnchors();
  initReveal();
  initHeader();
  initNav();
  initForm();
  initMotionStop();
});

/* ---- 旧サイトのアンカーを新しい位置へ送る ----
   旧サイトは1ページ構成で #kohaku / #rofika / #polano を使っていた。
   GitHub Pagesは301を返せないため、ここで受けて移動させる。
   リンクを外部に貼られている可能性があるので消さないこと。 */
function initLegacyAnchors() {
  const MAP = {
    "#kohaku": "#kohaku-to-ao",
    "#rofika": "#ro-fika",
    "#polano": "#polano-works",
    "#works": "#work-index",
    "#home": "",
  };
  const next = MAP[location.hash];
  if (next === undefined) return;
  const target = next ? document.querySelector(next) : null;
  history.replaceState(null, "", location.pathname + next);
  if (target) {
    // レイアウト確定を待ってから移動する(sticky区間の高さが効くため)
    requestAnimationFrame(() => target.scrollIntoView());
  } else {
    window.scrollTo(0, 0);
  }
}

/* ---- スクロールリビール(.js-reveal に .is-inview を付与) ---- */
function initReveal() {
  const targets = document.querySelectorAll(".js-reveal");
  if (!targets.length) return;
  if (!("IntersectionObserver" in window)) {
    targets.forEach((el) => el.classList.add("is-inview"));
    return;
  }
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add("is-inview");
          io.unobserve(e.target); // 一度きり。繰り返すならこの行を消す
        }
      });
    },
    { rootMargin: "0px 0px -12% 0px" }
  );
  targets.forEach((el) => io.observe(el));
}

/* ---- ヘッダー: スクロールで背景を付ける ---- */
function initHeader() {
  const header = document.querySelector(".site-header");
  if (!header) return;
  const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 40);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
}

/* ---- ハンバーガー(aria-expanded連動。a11y構造は削除禁止) ---- */
function initNav() {
  const btn = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".global-nav");
  if (!btn || !nav) return;
  btn.addEventListener("click", () => {
    const open = nav.classList.toggle("is-open");
    btn.setAttribute("aria-expanded", String(open));
    btn.setAttribute("aria-label", open ? "メニューを閉じる" : "メニューを開く");
    document.body.style.overflow = open ? "hidden" : "";
  });
  nav.querySelectorAll("a").forEach((a) =>
    a.addEventListener("click", () => {
      nav.classList.remove("is-open");
      btn.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    })
  );
}

/* ---- フォーム: 送信前検証+ハニーポット+二重送信防止 ----
   送信手段(action)は references/forms.md で決めて実装する */
function initForm() {
  const form = document.querySelector(".js-contact-form");
  if (!form) return;

  // 送信先が未設定のまま公開されると、送ったつもりで消える事故になる。
  // プレースホルダのままなら送信を止めて、その旨をその場に出す。
  if (form.getAttribute("action").indexOf("{FORM_ID}") !== -1) {
    const notice = document.createElement("p");
    notice.className = "form__error";
    notice.setAttribute("role", "status");
    notice.style.minHeight = "auto";
    notice.textContent =
      "現在このフォームは送信先が未設定のため、送信できません。設定方法は README.md をご覧ください。";
    form.appendChild(notice);
    const submit = form.querySelector('[type="submit"]');
    if (submit) {
      submit.disabled = true;
      submit.textContent = "送信できません（未設定）";
    }
    form.addEventListener("submit", (e) => e.preventDefault());
    return;
  }

  const showError = (field, msg) => {
    const err = form.querySelector(`[data-error-for="${field.id}"]`);
    field.setAttribute("aria-invalid", msg ? "true" : "false");
    if (err) err.textContent = msg;
  };

  const validators = {
    name: (v) => (v.trim() ? "" : "お名前を入力してください"),
    email: (v) =>
      /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim())
        ? ""
        : "メールアドレスの形式が正しくありません",
    message: (v) => (v.trim() ? "" : "お問い合わせ内容を入力してください"),
  };

  form.addEventListener("submit", (e) => {
    // ハニーポット(削除禁止): botが埋めたら静かに中断
    const hp = form.querySelector(".form__hp input");
    if (hp && hp.value) {
      e.preventDefault();
      return;
    }
    let firstBad = null;
    Object.keys(validators).forEach((id) => {
      const field = form.querySelector(`#${id}`);
      if (!field) return;
      const msg = validators[id](field.value);
      showError(field, msg);
      if (msg && !firstBad) firstBad = field;
    });
    if (firstBad) {
      e.preventDefault();
      firstBad.focus();
      return;
    }
    // 二重送信防止
    const btn = form.querySelector('[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.textContent = "送信しています…";
    }
  });
}

/* ---- モーション停止(SKILL.mdのポリシー実装。削除禁止) ----
   reduced-motion環境にのみボタンが表示され(CSS側)、押した場合だけ全停止 */
function initMotionStop() {
  const btn = document.querySelector(".motion-stop");
  if (!btn) return;
  btn.addEventListener("click", () => {
    const off = document.documentElement.classList.toggle("is-motion-off");
    btn.textContent = off ? "アニメーションを再生する" : "アニメーションを停止する";
    // GSAP使用時はここで gsap.globalTimeline.paused(off) 等も呼ぶ
  });
}
