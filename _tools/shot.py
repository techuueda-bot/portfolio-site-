"""確認用: 指定スクロール位置のスクリーンショットを撮る。

使い方: python3 shot.py <出力先ディレクトリ> [幅] [高さ]
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/shots")
W = int(sys.argv[2]) if len(sys.argv) > 2 else 1440
H = int(sys.argv[3]) if len(sys.argv) > 3 else 900
URL = "http://127.0.0.1:5190/"

# (ラベル, セレクタ, セレクタ位置からのオフセット px)。セレクタなしはページ絶対位置
SPOTS = [
    ("01-hero", None, 0),
    ("02-index", "#work-index", -160),
    ("03-kohaku-start", "#kohaku-to-ao", 200),
    ("04-kohaku-mid", "#kohaku-to-ao", 900),
    ("05-yodaka-mid", "#yodaka-no-hoshi", 900),
    ("06-polano-mid", "#polano-works", 900),
    ("07-rofika-mid", "#ro-fika", 900),
    ("08-asanoha-mid", "#asanoha-nursery", 900),
    ("09-approach", ".approach", -220),
    ("10-cta", ".cta", -160),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": W, "height": H}, device_scale_factor=2, locale="ja-JP")
        page = ctx.new_page()
        errors = []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append("pageerror: " + str(e)))

        page.goto(URL, wait_until="networkidle", timeout=60000)
        page.add_style_tag(content="html{scroll-behavior:auto !important}")
        page.wait_for_timeout(1600)

        for label, sel, off in SPOTS:
            if sel:
                top = page.evaluate(
                    "sel => document.querySelector(sel).getBoundingClientRect().top + window.scrollY", sel
                )
                y = max(0, top + off)
            else:
                y = off
            page.evaluate("y => window.scrollTo(0, y)", y)
            page.wait_for_timeout(900)
            page.screenshot(path=str(OUT / f"{W}-{label}.png"))
            print(f"  {W}-{label}.png  (y={int(y)})", flush=True)

        # 横スクロール事故の検査
        overflow = page.evaluate(
            "() => document.documentElement.scrollWidth - document.documentElement.clientWidth"
        )
        print(f"[{W}px] 横はみ出し: {overflow}px", flush=True)
        print(f"[{W}px] コンソールエラー: {errors if errors else 'なし'}", flush=True)
        b.close()


if __name__ == "__main__":
    main()
