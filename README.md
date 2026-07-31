# Tetsuhisa Ueda ポートフォリオ

公開先: https://techuueda-bot.github.io/portfolio-site-/ （リポジトリ `techuueda-bot/portfolio-site-`）

架空の店や施設を題材につくった5つのWebサイトを見せるためのサイト。
コンセプトは **「器が、作品の色を着る」** ——
このサイト自体は無彩色の暗室に徹し、色・書体・質感はすべて作品側から借りる。
スクロールで作品セクションに入ると、画面全体がその作品のトークンに切り替わる。

---

## 1. ローカルで見る

```bash
python3 -m http.server 5190 --directory /Users/uedatetsuhisa/Documents/Codex/portfolio-site
```

Claude Code から開くときは `.claude/launch.json` の `portfolio-site` を使う（ポート5190）。

---

## 2. どこを触れば何が変わるか

| 変えたいもの | 触るファイル |
|---|---|
| 器の色（暗室の黒・文字・罫線） | `assets/css/style.css` の `:root` 内 `--shell-*` |
| 各作品のテーマ色・書体 | `assets/js/works.js` の `theme`（トップの染まり方が変わる） |
| トップの本文・見出し | `index.html`（直接編集） |
| 下層ページの本文・共通パーツ | `_tools/build_pages.py` を編集 → `python3 _tools/build_pages.py` で再生成 |
| ヒーローで浮かぶ5枚の位置 | `index.html` の `.hero__plane` の `--x / --y / --z / --rot` |
| 展示のスクロール量 | `assets/css/style.css` の `.exhibit { height: 300svh }` |

**下層ページのHTMLを直接編集してもよいが、ヘッダー・フッター・メタなどの共通部分を
変えるときは必ず `_tools/build_pages.py` を直して再生成すること。**
直接編集すると11ページ分の手作業になり、必ずどこかがズレる。

---

## 3. 作品を追加する

1. `_tools/recapture.py` の `WORKS` に slug と URL を足して実行
   → `assets/img/works/<slug>/` に cover / cover-2x / cover-sp / strip-pc-*.webp ができる
   （実行結果に出る `strip.pc.h` の値を控える）
2. `assets/js/works.js` に1件追加（`theme` は対象サイトのCSS変数から引く）
3. `index.html` に Index の行1つと、展示セクション1つを複製して追加
4. `_tools/build_pages.py` の `WORKS` に1件追加 → 実行（一覧と詳細ページができる）
5. `python3 <skill>/scripts/generate_sitemap.py . https://techuueda-bot.github.io/portfolio-site-` で sitemap 更新
6. QAを通す（下記4）

---

## 4. 公開前にやること

### ① お問い合わせフォームを接続する（必須）

**現状、フォームは送信できない状態で止めてある。**
`contact/index.html` の `action` が `https://formspree.io/f/{FORM_ID}` のままだと、
送信ボタンが無効化され「送信先が未設定」と画面に出る。
送ったつもりで消える事故を防ぐための意図的な仕様。

1. https://formspree.io/ でアカウントを作り（**上田さんご自身で**）、新しいフォームを作成
2. 発行されるエンドポイント（`https://formspree.io/f/xxxxxxxx`）をコピー
3. `contact/index.html` の `action` を差し替える
4. 公開後、**必ず自分で1通テスト送信して受信を確認する**

無料枠は月50件。超えると受信されなくなるので、増えてきたら有料プランかGoogleフォームへ。
通知先メールアドレスはFormspreeの管理画面で変える。

### ② チェックリスト

- [ ] フォームの `action` を差し替えた／テスト送信して受信できた
- [ ] OGPが正しく出るか（https://cards-dev.twitter.com/validator などで確認）
- [ ] 旧アンカー `#kohaku` `#rofika` `#polano` が新しい位置へ飛ぶか（`assets/js/main.js` の `initLegacyAnchors`）
- [ ] Search Console に `sitemap.xml` を送信
- [x] `about/index.html` の名前表記・肩書き・地域（2026-07-31確定、下記「未確定事項」参照）

### ③ 公開する

`main` を直接書き換えず、作業ブランチを切ってから差し替える。

```bash
cd /Users/uedatetsuhisa/Documents/Codex/portfolio-site
git init -b renewal-2026-07
git remote add origin https://github.com/techuueda-bot/portfolio-site-.git
git add -A && git commit -m "全面改修: 5作品の展示サイトへ"
git push -u origin renewal-2026-07
```

GitHub上でPull Requestを作って中身を確認してから `main` にマージする。
マージすると GitHub Pages が自動で更新される（Settings → Pages が「main / (root)」であることを確認）。

**旧サイトのファイルは残さず入れ替える**（`index.html` `style.css` `script.js` `assets/` を全置換）。
心配なら、置き換える前に `git tag old-site` を打っておけば元に戻せる。

---

## 5. 未確定事項（上田さんに確認したいこと）

- **名前の表記**: `Tetsuhisa Ueda` のローマ字で確定（2026-07-31、漢字表記はしない方針）。
- **肩書き・地域**: 「Web制作 / 鹿児島」で確定（2026-07-31）。
- **経歴**: 「非エンジニア／AIに触れ始めて8か月」を反映済み（2026-07-31）。もっと詳しく書きたくなったら `about/index.html` の該当段落を足す。

未確定事項はすべて解消済み（2026-07-31）。

---

## 6. 実装メモ（あとで自分が読むため）

- **モーション停止**: 全員フル演出が既定。OSで「視差効果を減らす」にしている人にだけ
  右下に停止ボタンが出て、押したときだけ静止する（`assets/css/style.css` 末尾 + `main.js` の `initMotionStop`）。
- **ヒーローはCSS 3D**。Three.jsを入れると約600KB増えるのに対し、
  perspective + translateZ で同じ奥行きが出せるので外部ライブラリなし。JSが切れても静止画として成立する。
- **モバイルの展示は静止**。スマホ版の実ページは最大24,000px あり、
  短い窓を高速で送っても余白しか映らないため、端末枠にファーストビューを1枚置く方式にした。
  帯が流れるのは 768px 以上。
- **404.htmlだけCSSをインラインで持っている**。GitHub Pagesは404を任意の深さのURLで返すため、
  相対パスでもルート絶対パスでも壊れるケースがある。外部依存をなくして回避している。
- **画像は 1.3MB**。strip は WebP q72・幅1000px、7000pxごとにタイル分割
  （モバイルSafariの画像デコード上限対策）。

## 7. QA

```bash
python3 ~/.claude/skills/web-production/scripts/qa_check.py .
python3 ~/.claude/skills/web-production/scripts/visual_qa.py . --out /tmp/vqa
```

直近の結果: qa_check FAIL 0 / WARN 0、visual_qa FAIL 0 / WARN 36。
残っているWARNは「実寸より拡大されている」系で、対象はすべて**サイトのスクリーンショット**。
2倍ディスプレイでの等倍表示には足りないが、写真ではなく画面の画なので実害はないと判断した。
2倍に上げると画像が約4倍（5MB超）になり、表示速度のほうが割に合わない。
