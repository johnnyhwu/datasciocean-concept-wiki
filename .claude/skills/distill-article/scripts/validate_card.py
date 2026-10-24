"""觀念卡驗證（結構驗證 + 來源原文逐字比對；規則見 docs/card-format.md §8）。

用法：uv run python .claude/skills/distill-article/scripts/validate_card.py [--claim-count] [card.md ...]
      不給參數則驗證 wiki/concepts/ 全部
      --claim-count：另外檢查每張卡的主張數是否在 params 的 wiki.card_claim_range 內（含 pending 主張）。
                     只在「合併階段」（提案確認、合併完成之後）加這個旗標；挖卡與提案階段不要用，
                     避免為了湊主張數而把卡寫大。預設不檢查。
      不給參數時另查 wiki/figures/ 有沒有沒被任何主張引用的圖（孤兒圖）。
結束碼：0 通過（可能有 HINT）、1 有 ERROR。
HINT 不退回，交給對證者（主張數字不在來源原文、附圖不在 sources.sections 的小節內）。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import wikilib as W

ROLES = {"thesis", "context", "mechanism", "anchor", "evidence", "evaluation", "qualifier"}
CLAIM_STATUS = {"normal", "pending_author_confirmation", "author_confirmed"}
CONTEXT_TYPES = {"bound_to_source", "evidence_from_single_source", "standalone_classic"}
CARD_STATUS = {"active", "retired"}


FIGURE_KEYS = ("file", "article", "src", "caption", "sha256")


def check_figures(c: dict, tag: str, slugs: set[str], blogs: dict, params: dict,
                  section_norms: set[str], err: list[str], hint: list[str]) -> None:
    """主張的 figures：參考圖（docs/card-format.md §4.2）。圖不是證據，這裡只驗「圖真的來自 blog、沒被動過」。"""
    figs = c.get("figures")
    if figs is None:
        return
    if not isinstance(figs, list) or not all(isinstance(f, dict) for f in figs):
        err.append(f"{tag} figures 必須是物件清單")
        return
    if len(figs) > params["wiki"]["figure_max_per_claim"]:
        err.append(f"{tag} 附圖 {len(figs)} 張，超過每條主張上限 {params['wiki']['figure_max_per_claim']}")
    for f in figs:
        missing = [k for k in FIGURE_KEYS if not f.get(k)]
        if missing:
            err.append(f"{tag} figures 項目缺少 {missing}")
            continue
        label = f"{tag} 圖 {f['file']}"
        if f["article"] not in slugs:
            err.append(f"{label}：article={f['article']!r} 不在這張卡的 sources 內")
            continue
        blog = blogs.get(f["article"])
        if blog is None:
            continue  # blog 不存在，sources 檢查已報錯
        src = f["src"]
        if f["file"] != f"figures/{f['article']}/{src}" or ".." in Path(src).parts:
            err.append(f"{label}：file 必須是 figures/{f['article']}/{src}")
            continue
        ext = Path(src).suffix.lower()
        if ext not in set(params["wiki"]["figure_extensions"]):
            err.append(f"{label}：副檔名 {ext!r} 不在 wiki.figure_extensions 內")
        img = next((i for i in W.blog_images(blog) if i["src"] == src), None)
        if img is None:
            err.append(f"{label}：blog 內文沒有 image shortcode 引用 {src!r}")
            continue
        if W.normalize(f["caption"]) != W.normalize(img["caption"]):
            err.append(f"{label}：caption 與 blog 的圖說不一致")
        if img["section"] and section_norms and W.normalize(img["section"]) not in section_norms:
            hint.append(f"{label}：圖所在小節 {img['section']!r} 不在 sources.sections 內（交對證者判斷相關性）")
        original = blog.path.parent / src
        copy = W.WIKI_DIR / f["file"]
        if not original.is_file():
            err.append(f"{label}：blog 資料夾裡找不到原圖 {src!r}")
        elif W.sha256_of(original) != f["sha256"]:
            err.append(f"{label}：blog 的原圖已改變（sha256 不符）：重跑 copy_figure.py，看過新圖後，附這張圖的主張要重審")
        if not copy.is_file():
            err.append(f"{label}：wiki 裡沒有這個檔案（用 copy_figure.py 複製）")
            continue
        if W.sha256_of(copy) != f["sha256"]:
            err.append(f"{label}：wiki 裡的圖與記錄的 sha256 不符（被改過？重跑 copy_figure.py）")
        if copy.stat().st_size > params["wiki"]["figure_max_kb"] * 1024:
            err.append(f"{label}：超過 {params['wiki']['figure_max_kb']} KB")


def orphan_figures(cards: list[W.Card]) -> list[str]:
    """wiki/figures/ 裡沒有被任何主張引用的檔案。"""
    used = {f.get("file") for card in cards for c in card.claims for f in (c.get("figures") or []) if isinstance(f, dict)}
    root = W.WIKI_DIR / "figures"
    if not root.is_dir():
        return []
    found = {p.relative_to(W.WIKI_DIR).as_posix() for p in root.rglob("*") if p.is_file() and p.name != ".DS_Store"}
    return sorted(found - used)


def check_card(card: W.Card, all_ids: set[str], params: dict, blogs: dict) -> tuple[list[str], list[str]]:
    err: list[str] = list(card.errors)
    hint: list[str] = []
    f = card.front

    # ---- frontmatter
    if f.get("id") != card.path.stem:
        err.append(f"frontmatter id={f.get('id')!r} 與檔名 {card.path.stem!r} 不一致")
    for k in ("id", "title", "context_type", "sources", "status"):
        if not f.get(k):
            err.append(f"frontmatter 缺少 {k}")
    if f.get("context_type") not in CONTEXT_TYPES:
        err.append(f"context_type 不在 {sorted(CONTEXT_TYPES)}")
    if f.get("status") not in CARD_STATUS:
        err.append(f"status 不在 {sorted(CARD_STATUS)}")
    for k in ("parent", "related"):
        refs = f.get(k) or []
        refs = [refs] if isinstance(refs, str) else refs
        for r in refs:
            if r not in all_ids:
                err.append(f"{k} 指向不存在的觀念：{r}")

    # ---- sources 與 blog
    sources = f.get("sources") or []
    allowed_sections: list[W.Section] = []
    slugs = {s.get("article") for s in sources}
    for s in sources:
        slug = s.get("article")
        for k in ("article", "article_title", "url", "sections", "first_appearance"):
            if k not in s:
                err.append(f"sources 項目缺少 {k}")
        if not slug:
            continue
        try:
            blog = blogs.setdefault(slug, W.load_blog(slug, params))
        except FileNotFoundError as e:
            err.append(f"blog 文章不存在：{e}")
            continue
        if s.get("article_title") and W.normalize(str(s["article_title"])) != W.normalize(blog.title):
            err.append(f"sources[{slug}].article_title 與 blog 標題不一致：{s['article_title']!r} ≠ {blog.title!r}")
        secs = s.get("sections") or []
        if not secs:
            err.append(f"sources[{slug}].sections 不得為空")
        for t in secs:
            found = W.find_sections(blog, t)
            if not found:
                err.append(f"來源段落不存在於 blog：{t!r}")
            allowed_sections.extend(found)

    # ---- claims 結構
    claims = card.claims
    if not claims:
        err.append("沒有任何 claim")
    ids = [c.get("id") for c in claims]
    if len(set(ids)) != len(ids):
        err.append("claim id 卡內重複")
    roles = [c.get("role") for c in claims]
    if roles.count("thesis") != 1:
        err.append(f"thesis 必須恰好一條（目前 {roles.count('thesis')}）")
    if roles.count("context") < 1:
        err.append("至少需要一條 role=context 的主張（這是什麼）")

    all_blog_norms = [b.full_norm for b in blogs.values()]
    section_norms = {W.normalize(t) for s in sources for t in (s.get("sections") or [])}
    anchor_types = set(params["wiki"]["anchor_types"])

    for c in claims:
        cid = c.get("id", "?")
        tag = f"[{cid}]"
        for k in ("id", "role", "text", "source_quotes", "anchor_type", "importance", "status"):
            if c.get(k) in (None, "", []):
                err.append(f"{tag} 缺少 {k}")
        if c.get("role") not in ROLES:
            err.append(f"{tag} role={c.get('role')!r} 不在 {sorted(ROLES)}")
        if c.get("status") not in CLAIM_STATUS:
            err.append(f"{tag} status={c.get('status')!r} 不在 {sorted(CLAIM_STATUS)}")
        if c.get("anchor_type") not in anchor_types:
            err.append(f"{tag} anchor_type={c.get('anchor_type')!r} 不在清單內")
        if not isinstance(c.get("importance"), int) or c.get("importance", 0) < 1:
            err.append(f"{tag} importance 必須是 >=1 的整數")
        if c.get("role") == "thesis" and c.get("importance") != 1:
            err.append(f"{tag} thesis 的 importance 必須是 1")
        if c.get("status") == "author_confirmed":
            if not (c.get("confirmation") or {}).get("date"):
                err.append(f"{tag} author_confirmed 必須有 confirmation.date")

        # 含數字必有 comparison_target（否則必須是 pending）
        text = str(c.get("text", ""))
        # 名稱類標籤數字（Stage 3、D2S、第 3 點…）不算「含數字」，檢查前先刪掉（params.yaml: numeric_label_patterns）
        for pat in params["wiki"].get("numeric_label_patterns", []):
            text = re.sub(pat, "", text)
        if re.search(r"\d", text) and not c.get("comparison_target"):
            if c.get("numeric_kind") == "non_comparative":
                reason = c.get("numeric_reason")
                if reason not in set(params["wiki"]["non_comparative_reasons"]):
                    err.append(f"{tag} numeric_reason={reason!r} 不在允許清單")
                hit = [p for p in params["wiki"]["comparative_number_patterns"] if re.search(p, text)]
                if hit:
                    err.append(f"{tag} 主張含比較性數字寫法（{hit}），不得標 non_comparative")
                else:
                    hint.append(f"{tag} 數字豁免（{reason}）：請對證者確認「真的不是比較數字」")
            elif c.get("status") != "pending_author_confirmation":
                err.append(f"{tag} 主張含數字但沒有 comparison_target，且狀態不是 pending_author_confirmation"
                           "（非比較數字請標 numeric_kind: non_comparative 與 numeric_reason）")

        # 來源原文逐字（含：落在 sources.sections 之內）
        quotes = c.get("source_quotes") or []
        quote_texts = list(quotes)
        for q in c.get("qualifiers") or []:
            if not q.get("text") or not q.get("source_quote"):
                err.append(f"{tag} qualifiers 項目需有 text 與 source_quote")
            elif q.get("source") is not None:
                # 來源是圖說：限定「範圍、資料集、設定」用，引文必須逐字出現在這條主張自己附的圖的圖說
                if q["source"] != "figure_caption":
                    err.append(f"{tag} qualifiers 的 source 只能是 figure_caption：{q['source']!r}")
                elif not any(W.quote_in_text(q["source_quote"], W.normalize(f.get("caption", "")))
                             for f in (c.get("figures") or []) if isinstance(f, dict)):
                    err.append(f"{tag} 限定條件標明來源是圖說，但引文未逐字出現在這條主張自己附的圖的圖說：{q['source_quote'][:40]!r}…")
            else:
                quote_texts.append(q["source_quote"])
        for q in quote_texts:
            if not isinstance(q, str) or not q.strip():
                err.append(f"{tag} source_quotes 含空值")
                continue
            if not any(W.quote_in_text(q, n) for n in all_blog_norms):
                err.append(f"{tag} 來源原文未逐字出現在 blog：{q[:40]!r}…")
            elif allowed_sections and not any(W.quote_in_text(q, s.body_norm) for s in allowed_sections):
                err.append(f"{tag} 來源原文不在 sources.sections 列出的小節內：{q[:40]!r}…")

        check_figures(c, tag, slugs, blogs, params, section_norms, err, hint)
        if re.search(r"如圖|見圖|下圖|上圖|[如見上下]表(?!現)", str(c.get("text", ""))):
            hint.append(f"{tag} 主張文字有指向圖表的字眼（如圖、見表…）：主張必須不看圖也讀得懂，請改寫或確認")

        # HINT：主張數字不在來源原文
        qnorm = "".join(W.normalize(q) for q in quote_texts if isinstance(q, str))
        qnums = set(W.numbers_in("".join(str(q) for q in quote_texts)))
        for n in W.numbers_in(text):
            if n not in qnums:
                hint.append(f"{tag} 主張數字 {n} 不在來源原文（交對證者重點檢查）")

    return err, hint


def check_claim_count(card: W.Card, params: dict) -> list[str]:
    """主張數必須在 wiki.card_claim_range 內（含 pending 主張）。只在合併階段用 --claim-count 啟用。"""
    lo, hi = params["wiki"]["card_claim_range"]
    n = len(card.claims)
    if n < lo:
        return [f"主張數 {n} 少於下限 {lo}：考慮與相鄰觀念合併，不要為了湊數硬加主張"]
    if n > hi:
        return [f"主張數 {n} 超過上限 {hi}：考慮拆卡，或刪掉重複與次要的主張"]
    return []


def main(argv: list[str]) -> int:
    count_check = "--claim-count" in argv
    argv = [a for a in argv if a != "--claim-count"]
    params = W.load_params()
    cards = [W.parse_card(Path(a)) for a in argv] if argv else W.load_all_cards()
    all_cards = W.load_all_cards()
    all_ids = {c.front.get("id") for c in all_cards} | {c.front.get("id") for c in cards}
    dup = [i for i in all_ids if [c.front.get("id") for c in all_cards].count(i) > 1]
    blogs: dict = {}
    failed = False
    for d in dup:
        print(f"ERROR 全 wiki id 重複：{d}")
        failed = True
    if not argv:
        for o in orphan_figures(all_cards):
            print(f"ERROR 孤兒圖（沒有任何主張引用）：{o}")
            failed = True
    for card in cards:
        err, hint = check_card(card, all_ids, params, blogs)
        if count_check:
            err += check_claim_count(card, params)
        status = "FAIL" if err else "PASS"
        print(f"== {card.path.name}: {status}  (ERROR {len(err)}, HINT {len(hint)})")
        for e in err:
            print(f"  ERROR {e}")
        for h in hint:
            print(f"  HINT  {h}")
        failed |= bool(err)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
