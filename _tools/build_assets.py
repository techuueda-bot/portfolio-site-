"""キャプチャ原本 → 公開用アセット。

- strip: 実物が縦に流れる帯。長すぎるとモバイルSafariがデコードを落とすので
  MAX_TILE_H で縦に分割し、HTML側で隙間なく積む。
- cover: 一覧カード・OGP・WebGLテクスチャ用のファーストビュー。
- 各作品の地色/アクセントを画像からサンプリングして works-colors.json に出す。
"""
import json
import pathlib
from collections import Counter

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

SRC = pathlib.Path("/Users/uedatetsuhisa/Documents/Codex/portfolio-site/_source-captures")
DST = pathlib.Path("/Users/uedatetsuhisa/Documents/Codex/portfolio-site/assets/img/works")

STRIP_W = {"pc": 1000, "sp": 560}
MAX_TILE_H = 7000
COVER_W = 1440
COVER_RATIO = 900 / 1440  # ファーストビューの比率

SLUGS = [
    "kohaku-to-ao",
    "polano-works",
    "ro-fika",
    "yodaka-no-hoshi",
    "asanoha-nursery",
]


def save_strip(src_png, out_dir, prefix, target_w):
    """幅を揃えて縮小し、必要ならタイル分割してWebPで書き出す。"""
    im = Image.open(src_png).convert("RGB")
    w, h = im.size
    new_h = round(h * target_w / w)
    im = im.resize((target_w, new_h), Image.LANCZOS)

    tiles = []
    y = 0
    idx = 0
    while y < new_h:
        bottom = min(y + MAX_TILE_H, new_h)
        tile = im.crop((0, y, target_w, bottom))
        name = f"{prefix}-{idx}.webp"
        tile.save(out_dir / name, "WEBP", quality=72, method=5)
        tiles.append(
            {"src": name, "w": target_w, "h": bottom - y}
        )
        y = bottom
        idx += 1
    return {"w": target_w, "h": new_h, "tiles": tiles}


def sample_colors(im):
    """ファーストビューから地色と、最も彩度の高い色(=アクセント)を拾う。"""
    small = im.resize((160, 100), Image.LANCZOS).convert("RGB")
    px = list(small.getdata())

    base = Counter((r // 12, g // 12, b // 12) for r, g, b in px).most_common(1)[0][0]
    base_hex = "#%02x%02x%02x" % tuple(min(255, c * 12 + 6) for c in base)

    def vividness(c):
        r, g, b = c
        mx, mn = max(c), min(c)
        if mx == 0:
            return 0
        sat = (mx - mn) / mx
        # 明るすぎ・暗すぎは背景寄りなので落とす
        lum = mx / 255
        return sat * (1 - abs(lum - 0.6))

    accent = max(Counter(px).most_common(400), key=lambda kv: vividness(kv[0]) * (kv[1] ** 0.25))[0]
    accent_hex = "#%02x%02x%02x" % accent

    lum = sum(base) / 3
    return base_hex, accent_hex, "dark" if lum < 128 else "light"


def main():
    colors = {}
    for slug in SLUGS:
        out = DST / slug
        out.mkdir(parents=True, exist_ok=True)
        print(f"[{slug}]", flush=True)

        info = {}
        for label in ("pc", "sp"):
            src = SRC / slug / f"{slug}-{label}.png"
            info[label] = save_strip(src, out, f"strip-{label}", STRIP_W[label])
            n = len(info[label]["tiles"])
            print(f"  strip-{label}: {info[label]['w']}x{info[label]['h']} / {n}タイル", flush=True)

        # cover(ファーストビュー)
        pc = Image.open(SRC / slug / f"{slug}-pc.png").convert("RGB")
        fv = pc.crop((0, 0, pc.width, round(pc.width * COVER_RATIO)))
        cover = fv.resize((COVER_W, round(COVER_W * COVER_RATIO)), Image.LANCZOS)
        cover.save(out / "cover.webp", "WEBP", quality=82, method=5)
        cover.save(out / "cover.jpg", "JPEG", quality=84, optimize=True, progressive=True)

        sp = Image.open(SRC / slug / f"{slug}-sp.png").convert("RGB")
        sp_fv = sp.crop((0, 0, sp.width, round(sp.width * 844 / 390)))
        sp_fv.resize((560, round(560 * 844 / 390)), Image.LANCZOS).save(
            out / "cover-sp.webp", "WEBP", quality=82, method=5
        )

        base_hex, accent_hex, scheme = sample_colors(fv)
        colors[slug] = {
            "sampledBase": base_hex,
            "sampledAccent": accent_hex,
            "scheme": scheme,
            "strip": info,
        }
        print(f"  base={base_hex} accent={accent_hex} scheme={scheme}", flush=True)

    (DST / "strips.json").write_text(
        json.dumps(colors, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    total = sum(f.stat().st_size for f in DST.rglob("*") if f.is_file())
    print(f"\n[done] 合計 {total/1024/1024:.1f} MB", flush=True)


if __name__ == "__main__":
    main()
