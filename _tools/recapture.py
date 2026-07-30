"""カバー画像とストリップの取り直し。

capture_works.py はリビール発火のためにページを上から下までスクロールしてから
撮っていたが、スクロール連動アニメーションを持つサイト(ポラーノワークス)は
先頭に戻したときに途中状態で固まる。そこで:

  - cover : 新規ロード直後のファーストビューをそのまま撮る(スクロールしない)
  - strip : full_page でビューポートを全高に伸ばして一括で撮る
            (伸ばした時点で IntersectionObserver がまとめて発火する)
"""
import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

Image.MAX_IMAGE_PIXELS = None

OUT = pathlib.Path("/Users/uedatetsuhisa/Documents/Codex/portfolio-site/assets/img/works")
TMP = pathlib.Path("/private/tmp/claude-501/-Users-uedatetsuhisa-Documents-Codex/2bf3fd0a-d433-4a7a-806a-85385241fad6/scratchpad/recap")

WORKS = {
    "kohaku-to-ao": "https://techuueda-bot.github.io/kohaku-to-ao/",
    "yodaka-no-hoshi": "https://techuueda-bot.github.io/yodaka-no-hoshi-udon/",
    "polano-works": "https://techuueda-bot.github.io/polano-works-tour-guide/",
    "ro-fika": "https://techuueda-bot.github.io/rofika-portfolio-site/",
    "asanoha-nursery": "https://techuueda-bot.github.io/asanoha-nursery-hp/",
}

MAX_TILE_H = 7000
COVER_RATIO = 900 / 1440


def save_tiles(src_png, out_dir, prefix, target_w):
    im = Image.open(src_png).convert("RGB")
    new_h = round(im.height * target_w / im.width)
    im = im.resize((target_w, new_h), Image.LANCZOS)
    tiles, y, i = [], 0, 0
    while y < new_h:
        bottom = min(y + MAX_TILE_H, new_h)
        im.crop((0, y, target_w, bottom)).save(
            out_dir / f"{prefix}-{i}.webp", "WEBP", quality=72, method=5
        )
        tiles.append(bottom - y)
        y, i = bottom, i + 1
    return new_h, tiles


def main(slugs):
    TMP.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for slug in slugs:
            url = WORKS[slug]
            d = OUT / slug
            d.mkdir(parents=True, exist_ok=True)
            print(f"[{slug}]", flush=True)

            # --- cover: ファーストビューを、触らずに撮る ---
            ctx = b.new_context(viewport={"width": 1440, "height": 900},
                                device_scale_factor=2, locale="ja-JP")
            pg = ctx.new_page()
            pg.goto(url, wait_until="load", timeout=60000)
            pg.wait_for_timeout(4000)          # ロード演出が終わるまで待つ
            fv = TMP / f"{slug}-fv.png"
            pg.screenshot(path=str(fv))        # full_page にしない
            ctx.close()

            im = Image.open(fv).convert("RGB")
            im.resize((1440, round(1440 * COVER_RATIO)), Image.LANCZOS).save(
                d / "cover.webp", "WEBP", quality=82, method=5)
            im.resize((2160, round(2160 * COVER_RATIO)), Image.LANCZOS).save(
                d / "cover-2x.webp", "WEBP", quality=78, method=5)
            print(f"  cover / cover-2x", flush=True)

            # --- strip(PC): full_page で一括 ---
            ctx = b.new_context(viewport={"width": 1440, "height": 900},
                                device_scale_factor=2, locale="ja-JP")
            pg = ctx.new_page()
            pg.goto(url, wait_until="load", timeout=60000)
            pg.wait_for_timeout(4500)
            full = TMP / f"{slug}-pc.png"
            pg.screenshot(path=str(full), full_page=True)
            ctx.close()
            h, tiles = save_tiles(full, d, "strip-pc", 1000)
            print(f"  strip-pc 1000x{h} / {len(tiles)}タイル", flush=True)

            # --- cover-sp: モバイルの端末枠に置く1枚 ---
            # スマホ版の帯は作らない。実ページが2万px超あり、短い窓を高速で送ると
            # 余白しか映らないため、モバイルはファーストビューの静止表示にしている。
            ctx = b.new_context(viewport={"width": 390, "height": 844},
                                device_scale_factor=3, locale="ja-JP")
            pg = ctx.new_page()
            pg.goto(url, wait_until="load", timeout=60000)
            pg.wait_for_timeout(4000)
            fvsp = TMP / f"{slug}-sp-fv.png"
            pg.screenshot(path=str(fvsp))
            ctx.close()

            imsp = Image.open(fvsp).convert("RGB")
            imsp.resize((560, round(560 * imsp.height / imsp.width)), Image.LANCZOS).save(
                d / "cover-sp.webp", "WEBP", quality=82, method=5)
            print(f"  cover-sp", flush=True)
            print(f"  >> works.js の strip.pc.h を {h} に合わせること", flush=True)

        b.close()

    total = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(f"[done] 画像合計 {total/1024/1024:.2f} MB", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or list(WORKS))
