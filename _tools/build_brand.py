"""favicon / apple-touch-icon / OGP を生成する。

マークはサイトの見せ場と同じ「ブラウザ枠」。3つのドットと画面枠だけで組む。
OGPの文字は欧文のみ(この環境に日本語の正しい字形を持つフォントが無く、
GB字形で日本語を刻むと誤った漢字が出るため)。
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

Image.MAX_IMAGE_PIXELS = None

SITE = pathlib.Path("/Users/uedatetsuhisa/Documents/Codex/portfolio-site")
COMMON = SITE / "assets" / "img" / "common"
WORKS_IMG = SITE / "assets" / "img" / "works"

SHELL = (10, 11, 13)
INK = (232, 230, 225)
MUTED = (139, 138, 134)

SLUGS = ["kohaku-to-ao", "yodaka-no-hoshi", "polano-works", "ro-fika", "asanoha-nursery"]


def mark(size):
    """ブラウザ枠のマーク。小さいサイズでも潰れないよう線幅を size 比で決める。"""
    s = size * 4  # 4倍で描いて縮小(アンチエイリアス)
    im = Image.new("RGBA", (s, s), SHELL + (255,))
    d = ImageDraw.Draw(im)

    pad = round(s * 0.17)
    box = (pad, round(s * 0.22), s - pad, s - round(s * 0.22))
    lw = max(2, round(s * 0.045))
    radius = round(s * 0.06)
    d.rounded_rectangle(box, radius=radius, outline=INK, width=lw)

    # クロム部分の区切り線
    chrome_y = box[1] + round((box[3] - box[1]) * 0.3)
    d.line([(box[0], chrome_y), (box[2], chrome_y)], fill=INK, width=lw)

    # 3つのドット
    r = max(1, round(s * 0.022))
    cy = (box[1] + chrome_y) // 2
    for i in range(3):
        cx = box[0] + round(s * 0.075) + i * round(s * 0.075)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=INK)

    return im.resize((size, size), Image.LANCZOS)


def load_font(size, bold=False):
    for path in (
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
    ):
        p = pathlib.Path(path)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size, index=1 if (bold and path.endswith(".ttc")) else 0)
            except Exception:
                continue
    return ImageFont.load_default()


def spaced(text, gap):
    return (" " * gap).join(list(text))


def build_ogp():
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), SHELL)
    d = ImageDraw.Draw(im)

    # 作品のカバーを奥行き風に敷く(右側)
    covers = []
    for slug in SLUGS:
        c = Image.open(WORKS_IMG / slug / "cover.webp").convert("RGB")
        covers.append(c)

    x, y = 612, 96
    for i, c in enumerate(covers):
        w = 300 - i * 26
        h = round(w * c.height / c.width)
        thumb = c.resize((w, h), Image.LANCZOS)
        shadow = Image.new("RGB", (w + 8, h + 8), (0, 0, 0))
        im.paste(shadow, (x + i * 62 + 4, y + i * 74 + 4))
        im.paste(thumb, (x + i * 62, y + i * 74))

    # 左側を沈めて文字を読ませる
    veil = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(veil)
    for i in range(W):
        # x=0で不透明、x=700あたりで透明へ
        a = max(0, min(255, int(255 * (1 - i / 700.0))))
        vd.line([(i, 0), (i, H)], fill=a)
    im.paste(Image.new("RGB", (W, H), SHELL), (0, 0), veil)

    d = ImageDraw.Draw(im)
    d.text((72, 214), spaced("TETSUHISA UEDA", 1), font=load_font(38, bold=True), fill=INK)
    d.text((72, 286), "WEB PORTFOLIO", font=load_font(21), fill=MUTED)
    d.line([(72, 344), (150, 344)], fill=MUTED, width=2)
    d.text((72, 372), "Five fictional brands.", font=load_font(27), fill=INK)
    d.text((72, 410), "No two alike.", font=load_font(27), fill=INK)

    m = mark(56)
    im.paste(m, (72, 96), m)

    im.save(COMMON / "ogp.jpg", "JPEG", quality=88, optimize=True, progressive=True)
    print("  ogp.jpg", im.size)


def main():
    COMMON.mkdir(parents=True, exist_ok=True)

    ico = mark(256)
    ico.save(SITE / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("  favicon.ico")

    mark(180).convert("RGB").save(COMMON / "apple-touch-icon.png", "PNG")
    print("  apple-touch-icon.png")

    build_ogp()


if __name__ == "__main__":
    main()
