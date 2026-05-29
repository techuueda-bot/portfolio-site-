# Portfolio Minimal

「琥珀と青」を制作実績として掲載する、最小構成の個人ポートフォリオサイトです。

## Live Site

https://techuueda-bot.github.io/portfolio-site-/

## 概要

Web制作、AI活用、Instagram投稿、デザイン、文章制作の学習内容を、作品として見せるための1ページ構成のポートフォリオです。

現時点では作品を増やしすぎず、「琥珀と青」をきれいに見せることを優先しています。

## 構成

- Hero
- About
- Works
- Work Detail：琥珀と青
- Footer

## 掲載作品

### 琥珀と青

架空の中華そば店を想定したブランドサイトです。

青い器と琥珀色の一杯を軸に、余白、縦書き、横スクロールを使って、静かな余韻のあるWeb表現を目指しました。

公開サイト：

https://techuueda-bot.github.io/kohaku-to-ao/

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
    │   ├── kohaku-menu.png
    │   ├── portfolio-01-hero.png
    │   ├── portfolio-02-horizontal-kohaku.png
    │   ├── portfolio-03-menu.png
    │   └── portfolio-04-season-note.png
```

## ローカルでの確認方法

このフォルダで以下を実行します。

```bash
python3 -m http.server 8000
```

ブラウザで以下を開きます。

```text
http://localhost:8000
```

## 今後の拡張

- Works に作品カードを追加
- 同一ページ内で作品詳細を追加
- スマホ実機での表示確認
