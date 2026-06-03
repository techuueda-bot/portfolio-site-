# Portfolio Minimal

制作実績を掲載するための、最小構成の個人ポートフォリオサイトです。

## Live Site

https://techuueda-bot.github.io/portfolio-site-/

## 概要

Web制作、AI活用、文章表現を学びながら制作した架空ブランドサイトやサービスサイトを、作品として見せるためのポートフォリオです。
現在は「琥珀と青」「RO FIKA」「ポラーノワークス」を掲載しています。

## 構成

- Home
- Works
- Kohaku to Ao Detail
- RO FIKA Detail
- Polano Works Detail
- Footer

## 掲載作品

### 琥珀と青

架空の中華そば店を想定したブランドサイトです。
青い器と琥珀色の一杯を軸に、余白、縦書き、横スクロールを使って、静かな余韻のあるWeb表現を目指しました。

公開サイト：

https://techuueda-bot.github.io/kohaku-to-ao/

### RO FIKA

架空の小さな夏のカフェを題材にした1ページサイトです。
冷たい飲みものと焼き菓子をそばに、窓辺で静かにひと息つける時間をWeb上で表現しました。

ポートフォリオでは、Hero、Concept、Menu、Footer Info、スマホ表示のスクリーンショットを中心に掲載しています。
最初は雰囲気を重視したサイトでしたが、制作後半でマーケティング視点からMenuの価格帯やFooter Infoを追加し、「行けそう」「入りやすそう」という安心感も補強しました。

公開サイト：

https://techuueda-bot.github.io/rofika-portfolio-site/

GitHub：

https://github.com/techuueda-bot/rofika-portfolio-site

### ポラーノワークス

架空の就労継続支援B型事業所を題材にした、見学案内サイトです。
見学前に不安を感じている本人が、利用を急いで決めなくてもよいことを理解し、自分のペースで見学について相談できるようにすることを目的に設計しました。

本人向けの安心導線と、ご家族・支援機関向けの客観情報を分け、フォームは見学を確定する場所ではなく「見学について相談する」入口として構成しています。
必須項目を「お名前」と「連絡先」の2つに限定し、スマホでも入力負担が重く見えないように調整しています。

公開サイト：

https://techuueda-bot.github.io/polano-works-tour-guide/

GitHub：

https://github.com/techuueda-bot/polano-works-tour-guide

## 使用技術

- HTML
- CSS
- JavaScript

## ファイル構成

```text
portfolio-minimal/
├── index.html
├── style.css
├── script.js
├── README.md
└── assets/
    ├── screenshots/
    │   ├── kohaku-hero.png
    │   ├── kohaku-horizontal.png
    │   └── kohaku-menu.png
    └── projects/
        ├── rofika/
            ├── rofika-01-hero.png
            ├── rofika-02-concept-window.png
            ├── rofika-03-menu.png
            ├── rofika-04-fika-gallery.png
            ├── rofika-05-footer.png
            ├── rofika-mobile-01-hero.png
            ├── rofika-mobile-02-gallery.png
            └── rofika-mobile-03-info.png
        └── polano/
            ├── polano-01-first-view-pc.png
            ├── polano-02-contact-form-pc.png
            ├── polano-03-first-view-mobile.png
            └── polano-04-contact-fields-mobile.png
```

## ローカルでの確認方法

以下のコマンドで簡易サーバーを起動し、ブラウザで確認できます。

```bash
python3 -m http.server 8000
```

```text
http://localhost:8000
```

## 今後の拡張

- 他の制作物をWorksへ追加する
- スマホ実機での表示確認を続ける
