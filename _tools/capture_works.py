"""公開済み5作品のフルページキャプチャ + デザイントークン抽出。

出力: OUT/{slug}/{slug}-pc.png, {slug}-sp.png と tokens.json
"""
import json
import pathlib
import time

from playwright.sync_api import sync_playwright

OUT = pathlib.Path(
    "/Users/uedatetsuhisa/Documents/Codex/portfolio-site/_source-captures"
)

WORKS = [
    ("kohaku-to-ao", "https://techuueda-bot.github.io/kohaku-to-ao/"),
    ("polano-works", "https://techuueda-bot.github.io/polano-works-tour-guide/"),
    ("ro-fika", "https://techuueda-bot.github.io/rofika-portfolio-site/"),
    ("yodaka-no-hoshi", "https://techuueda-bot.github.io/yodaka-no-hoshi-udon/"),
    ("asanoha-nursery", "https://techuueda-bot.github.io/asanoha-nursery-hp/"),
]

# 器が作品の色を着るために、実サイトから計算値で吸い出す
PROBE = """() => {
  const cs = getComputedStyle(document.documentElement);
  const bs = getComputedStyle(document.body);
  const names = [];
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules; } catch (e) { continue; }
    for (const rule of rules || []) {
      if (!rule.style) continue;
      for (const prop of rule.style) {
        if (prop.startsWith('--')) names.push(prop);
      }
    }
  }
  const vars = {};
  for (const n of new Set(names)) {
    const v = cs.getPropertyValue(n).trim();
    if (v) vars[n] = v;
  }
  const h1 = document.querySelector('h1');
  return {
    title: document.title,
    description: (document.querySelector('meta[name=description]') || {}).content || '',
    bodyBg: bs.backgroundColor,
    bodyColor: bs.color,
    bodyFont: bs.fontFamily,
    h1Text: h1 ? h1.innerText.trim() : '',
    h1Font: h1 ? getComputedStyle(h1).fontFamily : '',
    h1Color: h1 ? getComputedStyle(h1).color : '',
    cssVars: vars,
    scrollHeight: document.documentElement.scrollHeight,
  };
}"""


def settle(page):
    """遅延リビールを全部発火させてからキャプチャする。"""
    page.wait_for_timeout(1500)
    height = page.evaluate("document.body.scrollHeight")
    step = 600
    for y in range(0, height + step, step):
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(120)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(900)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tokens = {}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for slug, url in WORKS:
            d = OUT / slug
            d.mkdir(parents=True, exist_ok=True)
            print(f"[capture] {slug} <- {url}", flush=True)

            for label, vw, vh, scale in (("pc", 1440, 900, 2), ("sp", 390, 844, 3)):
                ctx = browser.new_context(
                    viewport={"width": vw, "height": vh},
                    device_scale_factor=scale,
                    locale="ja-JP",
                )
                page = ctx.new_page()
                try:
                    page.goto(url, wait_until="networkidle", timeout=60000)
                except Exception as e:  # networkidleに来ない実装がある
                    print(f"  ! {label} networkidle timeout: {e}", flush=True)
                    page.goto(url, wait_until="load", timeout=60000)
                settle(page)

                if label == "pc":
                    tokens[slug] = {"url": url, **page.evaluate(PROBE)}

                path = d / f"{slug}-{label}.png"
                page.screenshot(path=str(path), full_page=True)
                print(f"  -> {path.name}", flush=True)
                ctx.close()
                time.sleep(0.3)

        browser.close()

    (OUT / "tokens.json").write_text(
        json.dumps(tokens, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"[done] {OUT / 'tokens.json'}", flush=True)


if __name__ == "__main__":
    main()
