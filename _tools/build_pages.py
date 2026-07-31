"""下層ページ生成。

共通パーツ(head/header/footer)をここで一元管理し、全ページへ展開する。
multipage-guide.md の「1箇所直したら全ページに反映」を、手作業ではなく
このスクリプトで担保する。ページ本文の修正は生成後のHTMLを直接編集してよいが、
共通パーツを変えるときは必ずここを直して再生成する。
"""
import pathlib

SITE = pathlib.Path("/Users/uedatetsuhisa/Documents/Codex/portfolio-site")
BASE = "https://techuueda-bot.github.io/portfolio-site-"
NAME = "Tetsuhisa Ueda"

FONTS = (
    "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400"
    "&family=JetBrains+Mono:wght@400;500&family=Noto+Serif+JP:wght@500"
    "&family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Zen+Old+Mincho:wght@600&display=swap"
)

WORKS = [
    {
        "strip_h": 7000, "sp_note": "丼の写真を画面幅いっぱいに残したまま、予約ボタンを親指の届く位置に置き直しました。", "slug": "kohaku-to-ao", "no": "01", "name": "琥珀と青",
        "kind": "架空の中華そば店 / 鹿児島",
        "copy": "雨上がりに、心を整える一杯。",
        "live": "https://techuueda-bot.github.io/kohaku-to-ao/",
        "repo": "https://github.com/techuueda-bot/kohaku-to-ao",
        "role": "企画 / デザイン / 実装 / 原稿",
        "tech": "HTML / CSS / JavaScript",
        "pages": "1ページ",
        "desc": "架空の中華そば店「琥珀と青」のブランドサイト。深い青の器と琥珀色のスープを軸に、予約を急がせない導線で設計しました。",
        "blocks": [
            ("課題", "決めきらない人を、追い出さない",
             "写真の力が強い題材です。ここで言葉まで強く押すと、広告のようになって店の空気が消えます。「今すぐ予約させる」ではなく、「今度行ってみようか」と思ったまま閉じてもらえる状態を目標に置きました。"),
            ("設計", "二色と、短い言葉だけに絞る",
             "色は深い青と琥珀の2色に固定し、湯気の立つ丼を画面いっぱいに置きました。文字は丼の邪魔をしない量まで削っています。予約ボタンの文言は「席の予約を相談する」。確定ではなく相談だと分かる言い方にしました。上部には常時「PORTFOLIO DEMO 架空店舗のため、予約情報は送信されません」の帯を出し、架空であることを隠していません。"),
            ("学んだこと", "写真が強いほど、文字は減らす",
             "最初はコピーをもっと入れていましたが、削るほど写真が効きました。強い素材があるときの自分の仕事は、足すことではなく引くことでした。"),
        ],
    },
    {
        "strip_h": 4495, "sp_note": "縦書きの見出しは折らずに縮め、下層4ページへの導線をフッターにまとめました。", "slug": "yodaka-no-hoshi", "no": "02", "name": "よだかの星 手打ちうどん",
        "kind": "架空の手打ちうどん店 / 花巻",
        "copy": "湯気の向こうに、一番星が見える一杯を。",
        "live": "https://techuueda-bot.github.io/yodaka-no-hoshi-udon/",
        "repo": "https://github.com/techuueda-bot/yodaka-no-hoshi-udon",
        "role": "企画 / デザイン / 実装 / 原稿",
        "tech": "HTML / CSS / JavaScript",
        "pages": "5ページ（トップ / お品書き / こだわり / アクセス / お問い合わせ）",
        "desc": "架空の手打ちうどん店「よだかの星」のサイト。写真を1枚も使わず、縦書きと余白と星図だけで店の実在感を立てました。下層4ページ構成です。",
        "blocks": [
            ("課題", "写真がないまま、店を実在させる",
             "この題材には使える写真がありませんでした。フリー素材の丼を借りてくると、どこの店でもない顔になります。写真を使わずに「ここにしかない店」をつくれるかが出発点でした。"),
            ("設計", "文字と余白だけで、世界のほうを立てる",
             "宮沢賢治の『よだかの星』を下敷きにし、縦書きの見出しと星図のSVG、巨大な一文字を背景に置く構成にしました。イラストは意図的に描いていません。実物の代わりにベクター画像を置くと、途端にクリップアートの安っぽさが出るからです。紙のグレインと手彫り風の印章だけを質感として足しています。"),
            ("学んだこと", "「寂しい」の答えは、動きではなく情報",
             "途中で画面が寂しく感じられ、演出を足したくなりました。実際に効いたのは、お知らせ・地図・曜日ごとの営業帯といった情報を先に充填することでした。動きはそのあとで足すほうが、結果的に少ない量で済みます。"),
        ],
    },
    {
        "strip_h": 7000, "sp_note": "道順の写真とフォームを縦一列にして、迷わず最後まで進めるようにしました。", "slug": "polano-works", "no": "03", "name": "ポラーノワークス",
        "kind": "架空の就労継続支援B型事業所 / 見学案内",
        "copy": "見学だけでも、大丈夫です。",
        "live": "https://techuueda-bot.github.io/polano-works-tour-guide/",
        "repo": "https://github.com/techuueda-bot/polano-works-tour-guide",
        "role": "企画 / 情報設計 / デザイン / 実装 / 原稿",
        "tech": "HTML / CSS / JavaScript",
        "pages": "1ページ + フォーム",
        "desc": "架空の就労継続支援B型事業所の見学案内サイト。目的を「利用開始」ではなく「見学前の不安軽減」に置き直して設計しました。",
        "blocks": [
            ("課題", "読む人は、たいてい不安を抱えている",
             "このサイトを開くのは、本人か、その家族か、支援者です。多くの場合、まだ利用を決めていません。決めていない人に決定を迫るページは、そのまま閉じられます。"),
            ("設計", "目的を「利用開始」から下ろす",
             "サイトの目的を「見学前の不安をほどくこと」に置き直しました。FAQ、見学の流れ、写真で見る道順、と段階的に進み、最後に相談フォームが来ます。フォームの必須項目は「お名前」と「連絡先」の2つだけ。自由記入欄は任意だと明記し、メール希望の人には電話しないことを画面上で約束しています。"),
            ("学んだこと", "必須項目を1つ減らすのが、いちばん効いた",
             "配慮を文章で説明するより、入力欄を1つ消すほうが速く伝わります。やさしさは、言葉より先にフォームの仕様に出ると思いました。"),
        ],
    },
    {
        "strip_h": 7000, "sp_note": "Galleryを2列、Footer Infoを1列に落とし、横スクロールを出さずに情報量を保っています。", "slug": "ro-fika", "no": "04", "name": "RO FIKA",
        "kind": "架空の夏のカフェ",
        "copy": "ひとりの午後に、光る小さな休憩。",
        "live": "https://techuueda-bot.github.io/rofika-portfolio-site/",
        "repo": "https://github.com/techuueda-bot/rofika-portfolio-site",
        "role": "企画 / デザイン / 実装 / 原稿",
        "tech": "HTML / CSS / JavaScript",
        "pages": "1ページ",
        "desc": "架空の小さな夏のカフェ「RO FIKA」のブランドサイト。世界観だけで終わらせないよう、あとから実用情報を足しました。",
        "blocks": [
            ("課題", "きれいなだけのカフェサイトになりかけた",
             "最初の版は、光と余白と大きなロゴタイプで雰囲気は出ていました。ただ読み返すと、値段も席数も分からない。「きれいですね」で終わって、行く理由が生まれていませんでした。"),
            ("設計", "雰囲気を壊さずに、実用を足す",
             "巨大なセリフ体のロゴタイプと窓辺の光はそのまま残し、Menuに価格帯を、フッターに営業時間・場所・席数・支払い方法・Instagramを整理して追加しました。Galleryにはあえて動きを付けず、写真の空気感と表示の安定を優先しています。"),
            ("学んだこと", "「おしゃれ」と「入れそう」は別の指標",
             "この2つは同時に測らないと片方に寄ります。以後、雰囲気を作り込んだあとで必ず「で、行けるか?」を自分に聞くようにしました。"),
        ],
    },
    {
        "strip_h": 6910, "sp_note": "「見学・空き状況を相談する」を画面上部に固定し、どこまで読んでも相談に行けるようにしました。", "slug": "asanoha-nursery", "no": "05", "name": "あさのは保育園",
        "kind": "架空の企業主導型保育園 / 鹿児島",
        "copy": "はじめて預ける朝を、少し軽くする。",
        "live": "https://techuueda-bot.github.io/asanoha-nursery-hp/",
        "repo": "https://github.com/techuueda-bot/asanoha-nursery-hp",
        "role": "企画 / 情報設計 / デザイン / 実装 / 原稿",
        "tech": "HTML / CSS / JavaScript",
        "pages": "1ページ + フォーム",
        "desc": "架空の企業主導型保育園のサイト。0〜2歳を預ける家庭の不安から逆算し、5作品でいちばん導線に時間をかけました。",
        "blocks": [
            ("課題", "制度が分かりにくいと、問い合わせが止まる",
             "企業主導型保育は「自分が対象になるのか」が分かりにくい制度です。そこが分からないままだと、見学の連絡まで進みません。分からなさが、そのまま離脱の理由になります。"),
            ("設計", "制度の説明より先に、うちの場合に答える",
             "「使える可能性を、見学前に一緒に確認できます。」を独立したセクションにして、勤務先が提携している場合・していない場合・地域枠・空き状況の4つを並べました。ヘッダーには「見学・空き状況を相談する」を常設し、どこまで読んでも相談に行けるようにしています。"),
            ("学んだこと", "5作品でいちばん、見た目の作業が少なかった",
             "時間の大半は文言と順番の検討に使い、装飾はほとんど足していません。成果を狙うサイトでは、それが正しい配分だと分かりました。"),
        ],
    },
]
BY = {w["slug"]: w for w in WORKS}


def head(rel, title, desc, url, page_class, ogtype="website", noindex=False, base=None):
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ""
    # base は 404.html 専用。どの深さのURLで表示されても資産を引けるようにする
    base_tag = f'\n  <base href="{base}">' if base else ""
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">{base_tag}
  <title>{title}</title>
  <meta name="description" content="{desc}">{robots}
  <meta property="og:type" content="{ogtype}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{BASE}/assets/img/common/ogp.jpg">
  <meta property="og:site_name" content="{NAME} Portfolio">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="{rel}favicon.ico">
  <link rel="apple-touch-icon" href="{rel}assets/img/common/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">
  <link rel="stylesheet" href="{rel}assets/css/style.css">
</head>
<body class="{page_class}">

  <div class="stage" aria-hidden="true"></div>
"""


def header(rel, current):
    def mark(key):
        return ' aria-current="page"' if current == key else ""

    return f"""
  <header class="site-header">
    <a class="site-header__logo" href="{rel}">{NAME}</a>
    <button class="nav-toggle" aria-expanded="false" aria-label="メニューを開く" aria-controls="global-nav">
      <span></span><span></span><span></span>
    </button>
    <nav class="global-nav" id="global-nav" aria-label="グローバルナビゲーション">
      <ul>
        <li><a href="{rel}"{mark('top')}>Top</a></li>
        <li><a href="{rel}works/"{mark('works')}>Works</a></li>
        <li><a href="{rel}about/"{mark('about')}>About</a></li>
        <li><a href="{rel}contact/"{mark('contact')}>Contact</a></li>
      </ul>
    </nav>
  </header>
"""


def footer(rel):
    return f"""
  <footer class="site-footer">
    <div class="container site-footer__inner">
      <p><small>&copy; 2026 {NAME}</small></p>
      <ul class="site-footer__nav">
        <li><a href="{rel}works/">Works</a></li>
        <li><a href="{rel}about/">About</a></li>
        <li><a href="{rel}contact/">Contact</a></li>
        <li><a href="{rel}privacy/">Privacy</a></li>
        <li><a href="https://github.com/techuueda-bot" target="_blank" rel="noopener noreferrer">GitHub</a></li>
      </ul>
    </div>
  </footer>

  <button class="motion-stop">アニメーションを停止する</button>
  <script src="{rel}assets/js/main.js" defer></script>
</body>
</html>
"""


def crumbs(rel, trail):
    """trail: [(ラベル, href or None)] 最後の要素が現在地"""
    items = [f'<li><a href="{rel}">トップ</a></li>']
    for label, href in trail[:-1]:
        items.append(f'<li><a href="{href}">{label}</a></li>')
    items.append(f'<li aria-current="page">{trail[-1][0]}</li>')
    return f"""
    <div class="breadcrumb">
      <div class="container">
        <ol>
          {"".join(items)}
        </ol>
      </div>
    </div>
"""


def page_header(en, title, lead=""):
    lead_html = f'\n        <p class="page-header__lead js-reveal" data-delay="2">{lead}</p>' if lead else ""
    return f"""
    <div class="page-header">
      <div class="container">
        <p class="page-header__en js-reveal">{en}</p>
        <h1 class="page-header__title js-reveal" data-delay="1">{title}</h1>{lead_html}
      </div>
    </div>
"""


def write(path, body):
    p = SITE / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    print("  " + path, flush=True)


# ---------- Works 一覧 ----------
def build_works_index():
    rel = "../"
    cards = []
    for w in WORKS:
        cards.append(f"""
          <li class="work-card js-reveal">
            <a href="{w['slug']}/">
              <div class="work-card__thumb">
                <img src="{rel}assets/img/works/{w['slug']}/cover.webp" alt="{w['name']}のファーストビュー" width="1440" height="900" loading="lazy" decoding="async">
              </div>
              <p class="work-card__no">Work {w['no']}</p>
              <p class="work-card__name">{w['name']}</p>
              <p class="work-card__kind">{w['kind']}</p>
            </a>
          </li>""")

    body = (
        head(rel, f"Works｜{NAME}",
             "架空の店や施設を題材につくった5つのWebサイトの一覧です。中華そば店、手打ちうどん店、就労継続支援事業所、カフェ、保育園。",
             f"{BASE}/works/", "p-works")
        + header(rel, "works")
        + "\n  <main>"
        + page_header("Works", "制作したサイト",
                      "すべて自主制作、題材はすべて架空です。企画・原稿・デザイン・実装までひとりで通しています。")
        + crumbs(rel, [("Works", None)])
        + f"""
    <section class="section section--tight">
      <div class="container">
        <ul class="work-grid">{"".join(cards)}
        </ul>
      </div>
    </section>
  </main>
"""
        + footer(rel)
    )
    write("works/index.html", body)


# ---------- Works 詳細 ----------
def build_work_detail(i, w):
    rel = "../../"
    prev_w = WORKS[i - 1] if i > 0 else None
    next_w = WORKS[i + 1] if i < len(WORKS) - 1 else None

    blocks = "".join(f"""
        <div class="detail-block js-reveal">
          <p class="section-head__en">{en}</p>
          <h2>{title}</h2>
          <p>{text}</p>
        </div>""" for en, title, text in w["blocks"])

    nav = []
    nav.append(f'<a href="{rel}works/{prev_w["slug"]}/">← {prev_w["name"]}</a>' if prev_w else "<span></span>")
    nav.append(f'<a href="{rel}works/{next_w["slug"]}/">{next_w["name"]} →</a>' if next_w else "<span></span>")

    body = (
        head(rel, f"{w['name']}｜{NAME}", w["desc"], f"{BASE}/works/{w['slug']}/", "p-work", "article")
        + header(rel, "works")
        + "\n  <main>"
        + page_header(f"Work {w['no']}", w["name"], w["copy"])
        + crumbs(rel, [("Works", f"{rel}works/"), (w["name"], None)])
        + f"""
    <section class="section section--tight">
      <div class="container">
        <figure class="detail-hero js-reveal">
          <img src="{rel}assets/img/works/{w['slug']}/cover.webp"
               srcset="{rel}assets/img/works/{w['slug']}/cover.webp 1440w, {rel}assets/img/works/{w['slug']}/cover-2x.webp 2160w"
               sizes="(max-width: 1228px) 100vw, 1180px"
               alt="{w['name']}のファーストビュー" width="1440" height="900" loading="eager" decoding="async">
        </figure>

        <dl class="detail-meta">
          <div class="detail-meta__row"><dt class="detail-meta__key">Type</dt><dd class="detail-meta__val">{w['kind']}</dd></div>
          <div class="detail-meta__row"><dt class="detail-meta__key">Role</dt><dd class="detail-meta__val">{w['role']}</dd></div>
          <div class="detail-meta__row"><dt class="detail-meta__key">Tech</dt><dd class="detail-meta__val">{w['tech']}</dd></div>
          <div class="detail-meta__row"><dt class="detail-meta__key">Pages</dt><dd class="detail-meta__val">{w['pages']}</dd></div>
        </dl>
{blocks}

        <div class="detail-shots js-reveal">
          <figure>
            <img src="{rel}assets/img/works/{w['slug']}/cover-sp.webp" alt="{w['name']}のスマートフォン表示" width="560" height="1212" loading="lazy" decoding="async">
            <figcaption>Mobile</figcaption>
          </figure>
          <p class="detail-shots__note">スマートフォンでは、{w['sp_note']}</p>
        </div>

        <div class="exhibit__links" style="margin-top:40px">
          <a href="{w['live']}" target="_blank" rel="noopener noreferrer">公開サイトを見る</a>
          <a href="{w['repo']}" target="_blank" rel="noopener noreferrer">GitHub</a>
        </div>

        <nav class="work-nav" aria-label="前後の作品">
          {nav[0]}
          {nav[1]}
        </nav>
      </div>
    </section>
  </main>
"""
        + footer(rel)
    )
    write(f"works/{w['slug']}/index.html", body)


# ---------- About ----------
def build_about():
    rel = "../"
    body = (
        head(rel, f"About｜{NAME}",
             "Web制作をしている上田です。架空の店や施設を題材に、企画・原稿・デザイン・実装までひとりで通してつくっています。できることと、つくるときに決めていることをまとめました。",
             f"{BASE}/about/", "p-about")
        + header(rel, "about")
        + "\n  <main>"
        + page_header("About", "つくっている人",
                      "架空の店や施設を題材に、企画・原稿・デザイン・実装までひとりで通してつくっています。")
        + crumbs(rel, [("About", None)])
        + f"""
    <section class="section section--tight">
      <div class="container">
        <div class="profile">
          <div class="js-reveal">
            <h2 class="section-head__title" style="font-size:clamp(22px,3vw,30px)">{NAME}</h2>
            <p style="margin-top:16px;opacity:.7;font-size:14.5px">Web制作 / 鹿児島</p>
            <p style="margin-top:6px;opacity:.5;font-size:13px">非エンジニア / AIと歩んで8か月</p>
          </div>
          <div class="js-reveal" data-delay="1">
            <p>エンジニアとしての教育は受けていません。AIに触れ始めて8か月、ここまでをかたちにしました。動かない、崩れるといったつまずきは、逃げずにAIと一緒に一つずつ潰しています。</p>
            <p style="margin-top:1.4em">掲載している5つのサイトは、すべて自主制作です。題材はすべて架空で、実在の店舗・施設ではありません。デザインカンプを先に作らず、原稿を書きながらコードで詰めていく進め方をしています。</p>
            <p style="margin-top:1.4em">共通しているのは、読む人がまだ何も決めていない段階に立っていることです。予約するか、見学に行くか、子どもを預けるか。決めていない人に決定を迫るページは、そのまま閉じられてしまいます。だから、急がせない言葉と余白の取り方をいちばん考えます。</p>
            <p style="margin-top:1.4em">1つ前につくったサイトの配色や構成は、次に持ち越しません。5つが似ていないのは、そこだけは崩さなかったからです。</p>
          </div>
        </div>

        <div class="section-head js-reveal" style="margin-top:var(--section-pad)">
          <span class="section-head__en">Can do</span>
          <h2 class="section-head__title">できること</h2>
        </div>
        <dl class="fact-list js-reveal">
          <div><dt class="fact-list__key">企画・設計</dt><dd>サイトの目的決め、サイトマップ、ページ構成、導線設計</dd></div>
          <div><dt class="fact-list__key">原稿</dt><dd>キャッチコピー、本文、UXライティング、フォームの文言</dd></div>
          <div><dt class="fact-list__key">デザイン</dt><dd>配色・タイポグラフィの設計、レスポンシブ、モーション設計</dd></div>
          <div><dt class="fact-list__key">実装</dt><dd>HTML / CSS / JavaScript、フォーム、アクセシビリティ対応</dd></div>
          <div><dt class="fact-list__key">公開まわり</dt><dd>GitHub Pages への公開、OGP・構造化データ・sitemap、計測タグの設置</dd></div>
        </dl>

        <div class="section-head js-reveal" style="margin-top:var(--section-pad)">
          <span class="section-head__en">Note</span>
          <h2 class="section-head__title">お断り</h2>
        </div>
        <p class="lead js-reveal">掲載している店舗名・施設名・住所・メニュー・料金・人物は、すべて架空です。制作物の見本として作成したもので、実在の団体とは関係ありません。写真素材はライセンスの範囲内で使用しています。</p>

        <p class="js-reveal" style="margin-top:48px">
          <a class="button" href="{rel}contact/">お問い合わせ</a>
        </p>
      </div>
    </section>
  </main>
"""
        + footer(rel)
    )
    write("about/index.html", body)


# ---------- Contact ----------
def build_contact():
    rel = "../"
    body = (
        head(rel, f"Contact｜{NAME}",
             "お仕事のご相談、制作物へのご感想はこちらからお送りください。お名前・メールアドレス・内容の3項目だけでお送りいただけます。",
             f"{BASE}/contact/", "p-contact")
        + header(rel, "contact")
        + "\n  <main>"
        + page_header("Contact", "お問い合わせ",
                      "お仕事のご相談も、制作物への感想だけでも構いません。数日以内にお返事します。")
        + crumbs(rel, [("Contact", None)])
        + f"""
    <section class="section section--tight">
      <div class="container--narrow">
        <!-- 送信手段: Formspree。公開前に action の {{FORM_ID}} を自分のフォームIDに差し替える。
             差し替えるまではメールソフトが開く mailto にフォールバックする(README参照)。 -->
        <form class="form js-contact-form"
              action="https://formspree.io/f/{{FORM_ID}}"
              method="POST" novalidate>

          <div class="form__field">
            <label for="name">お名前<span class="required">必須</span></label>
            <input type="text" id="name" name="name" autocomplete="name" required aria-describedby="name-error">
            <p class="form__error" id="name-error" data-error-for="name" aria-live="polite"></p>
          </div>

          <div class="form__field">
            <label for="email">メールアドレス<span class="required">必須</span></label>
            <input type="email" id="email" name="email" autocomplete="email" inputmode="email" required aria-describedby="email-error">
            <p class="form__error" id="email-error" data-error-for="email" aria-live="polite"></p>
          </div>

          <div class="form__field">
            <label for="message">お問い合わせ内容<span class="required">必須</span></label>
            <textarea id="message" name="message" rows="8" required aria-describedby="message-error"></textarea>
            <p class="form__error" id="message-error" data-error-for="message" aria-live="polite"></p>
          </div>

          <!-- ハニーポット: 削除禁止(スパム対策) -->
          <div class="form__hp" aria-hidden="true">
            <label>この欄は入力しないでください<input type="text" name="company_url" tabindex="-1" autocomplete="off"></label>
          </div>

          <input type="hidden" name="_subject" value="ポートフォリオサイトからのお問い合わせ">
          <input type="hidden" name="_next" value="{BASE}/contact/thanks/">

          <p class="form__privacy">ご入力いただいた内容は、お返事のためだけに使用します。詳しくは<a href="{rel}privacy/">プライバシーポリシー</a>をご覧ください。</p>

          <div>
            <button class="button" type="submit">送信する</button>
          </div>
        </form>
      </div>
    </section>
  </main>
"""
        + footer(rel)
    )
    write("contact/index.html", body)


def build_thanks():
    rel = "../../"
    body = (
        head(rel, f"送信しました｜{NAME}", "お問い合わせを送信しました。",
             f"{BASE}/contact/thanks/", "p-thanks", noindex=True)
        + header(rel, "contact")
        + "\n  <main>"
        + page_header("Thank you", "送信しました",
                      "お問い合わせありがとうございます。内容を確認のうえ、数日以内にご返信します。")
        + crumbs(rel, [("Contact", f"{rel}contact/"), ("送信しました", None)])
        + f"""
    <section class="section section--tight">
      <div class="container--narrow">
        <p class="js-reveal">迷惑メールフォルダに振り分けられることがあります。数日待っても届かない場合は、お手数ですがもう一度お送りください。</p>
        <p class="js-reveal" data-delay="1" style="margin-top:40px">
          <a class="button" href="{rel}">トップへ戻る</a>
        </p>
      </div>
    </section>
  </main>
"""
        + footer(rel)
    )
    write("contact/thanks/index.html", body)


# ---------- Privacy ----------
def build_privacy():
    rel = "../"
    body = (
        head(rel, f"プライバシーポリシー｜{NAME}",
             "お問い合わせフォームでお預かりする個人情報の取り扱いについて記載しています。",
             f"{BASE}/privacy/", "p-privacy")
        + header(rel, "")
        + "\n  <main>"
        + page_header("Privacy", "プライバシーポリシー")
        + crumbs(rel, [("プライバシーポリシー", None)])
        + f"""
    <section class="section section--tight">
      <div class="container--narrow">
        <div class="detail-block js-reveal" style="margin-top:0">
          <h2>取得する情報</h2>
          <p>お問い合わせフォームから、お名前・メールアドレス・お問い合わせ内容をお預かりします。これ以外の情報は取得しません。</p>
        </div>
        <div class="detail-block js-reveal">
          <h2>利用目的</h2>
          <p>お預かりした情報は、お問い合わせへの返信のためだけに使用します。広告配信やメールマガジンの送付には使用しません。</p>
        </div>
        <div class="detail-block js-reveal">
          <h2>第三者への提供</h2>
          <p>ご本人の同意がある場合、または法令に基づく場合を除き、第三者へ提供することはありません。フォームの送信には外部サービス（Formspree）を利用しており、送信内容は同サービスを経由します。</p>
        </div>
        <div class="detail-block js-reveal">
          <h2>アクセス解析</h2>
          <p>本サイトではアクセス解析ツールを使用していません。導入した場合は、本ページに追記します。</p>
        </div>
        <div class="detail-block js-reveal">
          <h2>お問い合わせ</h2>
          <p>本ポリシーに関するご質問は、<a href="{rel}contact/">お問い合わせフォーム</a>よりご連絡ください。</p>
        </div>
        <p class="js-reveal" style="margin-top:48px;font-size:13px;opacity:.6">制定日: 2026年7月31日</p>
      </div>
    </section>
  </main>
"""
        + footer(rel)
    )
    write("privacy/index.html", body)


# ---------- 404 ----------
def build_404():
    """404だけは外部ファイルに依存させない。

    GitHub Pagesのプロジェクトページでは、404.htmlが `/works/foo/bar/` のような
    任意の深さのURLで表示される。相対パスだとCSSもリンクも深さによって壊れ、
    ルート絶対パスだとローカル確認が壊れる。どちらの事故も起きないよう、
    このページはCSSをインラインで持ち、リンクは絶対URLで書く。
    """
    body = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ページが見つかりません｜{NAME}</title>
  <meta name="description" content="お探しのページは見つかりませんでした。">
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{BASE}/404.html">
  <link rel="icon" href="{BASE}/favicon.ico">
  <link rel="apple-touch-icon" href="{BASE}/assets/img/common/apple-touch-icon.png">
  <style>
    /* 404は外部CSSを読まない(表示されるURLの深さが読めないため)。
       値はstyle.cssのトークンと揃えてあるので、器の色を変えたらここも直す。 */
    *, *::before, *::after {{ box-sizing: border-box; }}
    body {{
      margin: 0; min-height: 100svh;
      display: grid; place-content: center; justify-items: start;
      padding: 32px clamp(24px, 6vw, 80px);
      background: #0a0b0d; color: #e8e6e1;
      font-family: "Hiragino Kaku Gothic ProN", "Yu Gothic", sans-serif;
      line-height: 1.9; letter-spacing: .02em;
      overflow-wrap: anywhere;
    }}
    .en {{
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 11px; letter-spacing: .3em; color: #8b8a86; margin: 0 0 12px;
    }}
    h1 {{ font-size: clamp(26px, 5vw, 44px); line-height: 1.4; margin: 0 0 20px; }}
    p {{ margin: 0; max-width: 34em; }}
    .muted {{ color: #8b8a86; font-size: 15px; }}
    ul {{ list-style: none; padding: 0; margin: 40px 0 0; display: flex; flex-wrap: wrap; gap: 24px; }}
    a {{
      color: inherit; text-decoration: none;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 12px; letter-spacing: .12em;
      border-bottom: 1px solid #8b8a86; padding-bottom: 4px;
    }}
    a:hover {{ opacity: .7; }}
    a:focus-visible {{ outline: 2px solid #e8e6e1; outline-offset: 3px; }}
  </style>
</head>
<body>
  <p class="en">404 Not Found</p>
  <h1>ページが見つかりません</h1>
  <p class="muted">アドレスが変わったか、削除された可能性があります。お探しのものが作品ページであれば、一覧から辿れます。</p>
  <ul>
    <li><a href="{BASE}/">トップへ</a></li>
    <li><a href="{BASE}/works/">作品一覧へ</a></li>
    <li><a href="{BASE}/contact/">お問い合わせ</a></li>
  </ul>
</body>
</html>
"""
    write("404.html", body)


def main():
    print("[pages]", flush=True)
    build_works_index()
    for i, w in enumerate(WORKS):
        build_work_detail(i, w)
    build_about()
    build_contact()
    build_thanks()
    build_privacy()
    build_404()
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
