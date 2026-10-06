"""觀念卡驗證（結構驗證 + 來源原文逐字比對；規則見 docs/card-format.md §8）。

用法：uv run python .claude/skills/distill-article/scripts/validate_card.py [card.md ...]
      不給參數則驗證 wiki/concepts/ 全部
結束碼：0 通過（可能有 HINT）、1 有 ERROR。
HINT 不退回，交給對證者（主張數字不在來源原文）。
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

        # HINT：主張數字不在來源原文
        qnorm = "".join(W.normalize(q) for q in quote_texts if isinstance(q, str))
        qnums = set(W.numbers_in("".join(str(q) for q in quote_texts)))
        for n in W.numbers_in(text):
            if n not in qnums:
                hint.append(f"{tag} 主張數字 {n} 不在來源原文（交對證者重點檢查）")

    return err, hint


def main(argv: list[str]) -> int:
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
    for card in cards:
        err, hint = check_card(card, all_ids, params, blogs)
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
