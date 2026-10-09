"""Notes（私の思考）ページ生成。

head / header / footer などの共通パーツは build_pages.py のものをそのまま使う。
原稿は notes_data.py。記事を足したらこのスクリプトを実行する。

  python3 _tools/build_notes.py           # 公開分だけ生成
  python3 _tools/build_notes.py --drafts  # 下書きも noindex で生成（確認用。コミットしない）

生成されるページ:
  notes/                     カテゴリ一覧 + 新着
  notes/<カテゴリ>/          カテゴリ別の記事一覧
  notes/<カテゴリ>/<記事>/   記事
"""
import html
import sys

from build_pages import BASE, NAME, crumbs, footer, head, header, page_header, write
from notes_data import CATEGORIES, NOTES

CAT = {c["slug"]: c for c in CATEGORIES}


def esc(s):
    return html.escape(s, quote=True)


def dotted(date):
    return date.replace("-", ".")


def check(n):
    """記事の型が崩れていたら生成前に止める。出典なしの記事は出さない。"""
    for key in ("slug", "cat", "title", "date", "conclusion", "points", "thoughts", "sources"):
        if not n.get(key):
            sys.exit(f"[notes] {n.get('slug', '?')}: {key} が空です")
    if n["cat"] not in CAT:
        sys.exit(f"[notes] {n['slug']}: 不明なカテゴリ {n['cat']}")
    for s in n["sources"]:
        if not (s.get("title") and s.get("url")):
            sys.exit(f"[notes] {n['slug']}: 出典には title と url が必要です")


def rows(notes, rel):
    """記事一覧の行。トップの Index と同じ見た目を使う。"""
    if not notes:
        return '\n        <p class="lead js-reveal">まだ記事はありません。</p>'
    items = "".join(f"""
          <li class="index-row">
            <a href="{rel}notes/{n['cat']}/{n['slug']}/">
              <span class="index-row__no">{dotted(n['date'])}</span>
              <span class="index-row__name">{esc(n['title'])}</span>
              <span class="index-row__kind">{esc(CAT[n['cat']]['name'])}</span>
            </a>
          </li>""" for n in notes)
    return f"""
        <ul class="index-list index-list--notes js-reveal">{items}
        </ul>"""


# ---------- Notes トップ ----------
def build_index(notes):
    rel = "../"
    cats = "".join(f"""
          <a class="approach__item note-cat js-reveal" data-delay="{i % 4}" href="{c['slug']}/">
            <p class="approach__no">{c['no']} / {c['en']}</p>
            <h3 class="approach__title">{c['name']}</h3>
            <p class="approach__body">{c['desc']}</p>
            <p class="note-cat__count">{sum(n['cat'] == c['slug'] for n in notes)} 記事</p>
          </a>""" for i, c in enumerate(CATEGORIES))

    body = (
        head(rel, f"Notes｜{NAME}",
             "YouTubeからの学び、創作の考え、論文の知見、経営と金融。読んだり観たりつくったりしながら考えたことを、出典とともに残しています。",
             f"{BASE}/notes/", "p-notes")
        + header(rel, "notes")
        + "\n  <main>"
        + page_header("Notes", "私の思考",
                      "観たもの、読んだもの、つくったものから考えたことを置いていく場所です。受け取ったものには必ず出典を添えます。")
        + crumbs(rel, [("Notes", None)])
        + f"""
    <section class="section section--tight">
      <div class="container">
        <div class="approach">{cats}
        </div>

        <div class="section-head js-reveal" style="margin-top:var(--section-pad)">
          <span class="section-head__en">Latest</span>
          <h2 class="section-head__title">新着</h2>
        </div>{rows(notes[:10], rel)}
      </div>
    </section>
  </main>
"""
        + footer(rel)
    )
    write("notes/index.html", body)


# ---------- カテゴリ別一覧 ----------
def build_category(c, notes):
    rel = "../../"
    body = (
        head(rel, f"{c['name']}｜Notes｜{NAME}", c["desc"], f"{BASE}/notes/{c['slug']}/", "p-notes")
        + header(rel, "notes")
        + "\n  <main>"
        + page_header(c["en"], c["name"], c["desc"])
        + crumbs(rel, [("Notes", f"{rel}notes/"), (c["name"], None)])
        + f"""
    <section class="section section--tight">
      <div class="container">{rows(notes, rel)}
      </div>
    </section>
  </main>
"""
        + footer(rel)
    )
    write(f"notes/{c['slug']}/index.html", body)


# ---------- 記事 ----------
def build_note(n, siblings):
    rel = "../../../"
    c = CAT[n["cat"]]
    i = siblings.index(n)
    # 一覧は新しい順なので、前の記事 = 1つ古い記事
    older = siblings[i + 1] if i + 1 < len(siblings) else None
    newer = siblings[i - 1] if i > 0 else None

    def block(en, title, inner):
        return f"""
        <div class="detail-block js-reveal">
          <p class="section-head__en">{en}</p>
          <h2>{title}</h2>{inner}
        </div>"""

    points = "".join(f"\n            <li>{esc(p)}</li>" for p in n["points"])
    thoughts = "".join(f"\n          <p>{esc(p)}</p>" for p in n["thoughts"])
    nexts = "".join(f"\n            <li>{esc(p)}</li>" for p in n.get("next", []))
    def source(s):
        sub = " / ".join(esc(s[k]) for k in ("by", "where") if s.get(k))
        sub = f'<br><span class="note-source__by">{sub}</span>' if sub else ""
        return f"""
            <div>
              <dt class="fact-list__key">{esc(s.get('kind', '出典'))}</dt>
              <dd><a href="{esc(s['url'])}" target="_blank" rel="noopener noreferrer">{esc(s['title'])}</a>{sub}</dd>
            </div>"""

    sources = "".join(source(s) for s in n["sources"])

    blocks = (
        block("Points", "要点", f'\n          <ul class="note-points">{points}\n          </ul>')
        + block("Thoughts", "私の考え", thoughts)
        + (block("Next", "次に試すこと", f'\n          <ul class="note-points">{nexts}\n          </ul>') if nexts else "")
        + block("Sources", "出典", f'\n          <dl class="fact-list">{sources}\n          </dl>')
    )

    tags = " / ".join(esc(t) for t in n.get("tags", [])) or "—"
    nav = [
        f'<a href="{rel}notes/{c["slug"]}/{older["slug"]}/">← {esc(older["title"])}</a>' if older else "<span></span>",
        f'<a href="{rel}notes/{c["slug"]}/{newer["slug"]}/">{esc(newer["title"])} →</a>' if newer else "<span></span>",
    ]

    body = (
        head(rel, f"{esc(n['title'])}｜{NAME}", esc(n["conclusion"]),
             f"{BASE}/notes/{c['slug']}/{n['slug']}/", "p-note", "article", noindex=n.get("draft", False))
        + header(rel, "notes")
        + "\n  <main>"
        + page_header(c["en"], esc(n["title"]))
        + crumbs(rel, [("Notes", f"{rel}notes/"), (c["name"], f"{rel}notes/{c['slug']}/"), (esc(n["title"]), None)])
        + f"""
    <section class="section section--tight">
      <div class="container--narrow">
        <dl class="detail-meta">
          <div class="detail-meta__row"><dt class="detail-meta__key">Category</dt><dd class="detail-meta__val">{c['name']}</dd></div>
          <div class="detail-meta__row"><dt class="detail-meta__key">Date</dt><dd class="detail-meta__val"><time datetime="{n['date']}">{dotted(n['date'])}</time></dd></div>
          <div class="detail-meta__row"><dt class="detail-meta__key">Tags</dt><dd class="detail-meta__val">{tags}</dd></div>
        </dl>

        <div class="note-conclusion js-reveal">
          <p class="section-head__en">Conclusion</p>
          <p class="note-conclusion__text">{esc(n['conclusion'])}</p>
        </div>
{blocks}

        <nav class="work-nav" aria-label="前後の記事">
          {nav[0]}
          {nav[1]}
        </nav>
      </div>
    </section>
  </main>
"""
        + footer(rel)
    )
    write(f"notes/{c['slug']}/{n['slug']}/index.html", body)


def main():
    drafts = "--drafts" in sys.argv
    for n in NOTES:
        check(n)
    public = sorted((n for n in NOTES if not n.get("draft")), key=lambda n: n["date"], reverse=True)

    print("[notes]", flush=True)
    build_index(public)
    for c in CATEGORIES:
        in_cat = [n for n in public if n["cat"] == c["slug"]]
        build_category(c, in_cat)
        for n in in_cat:
            build_note(n, in_cat)
    if drafts:
        for n in NOTES:
            if n.get("draft"):
                build_note(n, [n])
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
