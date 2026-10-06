"""產生「對證者」看的卡副本：主張後標 [n] 引用，卡尾是參考文獻與引文所在的 blog 段落。

對證者不再讀整篇 blog，只讀這份。引文與段落都由程式從 blog 逐字抽出，所以「引文真的在 blog」
由程式保證，對證者只負責判斷「主張是否被這些原文完整支持」。

用法：
  uv run python .claude/skills/distill-article/scripts/make_auditor_copy.py <card.md> <out.md>
        [--only c1,c3]      只審這些主張；其他主張只列文字供互核，不附引用
        [--context paragraph|quote]   引文帶出所在段落（預設，取 params 的 stage1.auditor_context）
                            或只給引文本身（最省，但對證者看不到前後句）
        [--neighbors N]     paragraph 模式下，每個引文段落前後各多帶 N 段（預設 0）

這份副本看不到的東西（由「全文審查」補）：blog 其他段落的矛盾、卡漏掉的重點、
跨卡矛盾、引文前後段落對範圍的限定。
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

import wikilib as W

HIDE_CLAIM_KEYS = {"source_quotes", "importance"}


@dataclass
class Block:
    heading: str
    raw: str
    norm: str


def split_blocks(body: str) -> list[Block]:
    """依空行與標題把 blog 內文切成段落（程式碼區塊與表格各自成一段）。"""
    blocks: list[Block] = []
    heading = ""
    buf: list[str] = []
    in_code = False

    def flush():
        nonlocal buf
        raw = "\n".join(buf).strip("\n")
        if raw.strip():
            blocks.append(Block(heading, raw, W.normalize(raw)))
        buf = []

    for line in body.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            buf.append(line)
            continue
        if in_code:
            buf.append(line)
            continue
        m = re.match(r"^(#{1,6})\s+(.*\S)\s*$", line)
        if m:
            flush()
            heading = m.group(2)
            continue
        if not line.strip():
            flush()
            continue
        buf.append(line)
    flush()
    return blocks


def locate(blocks: list[Block], quote: str) -> list[int] | None:
    """引文每個片段（依序）落在哪些段落；找不到回傳 None。"""
    concat = "".join(b.norm for b in blocks)
    starts, pos = [], 0
    for b in blocks:
        starts.append(pos)
        pos += len(b.norm)

    def block_of(offset: int) -> int:
        lo = 0
        for i, s in enumerate(starts):
            if s <= offset:
                lo = i
            else:
                break
        return lo

    hit: list[int] = []
    cursor = 0
    frags = W.quote_fragments(quote)
    if not frags:
        return None
    for f in frags:
        k = concat.find(f, cursor)
        if k == -1:
            return None
        for i in range(block_of(k), block_of(k + len(f) - 1) + 1):
            if i not in hit:
                hit.append(i)
        cursor = k + len(f)
    return hit


def main(card_path: str, out_path: str, only: set[str] | None, neighbors: int, context: str | None) -> int:
    params = W.load_params()
    context = context or params["stage1"].get("auditor_context", "paragraph")
    assert context in ("paragraph", "quote"), context
    card = W.parse_card(Path(card_path))
    slugs = [s["article"] for s in card.front.get("sources", [])]
    blogs = [W.load_blog(s, params) for s in slugs]
    block_sets = [split_blocks(b.body) for b in blogs]

    ref_no: dict[str, int] = {}      # 引文字串 -> 編號
    ref_blocks: dict[int, list[tuple[int, int]]] = {}   # 編號 -> [(blog 序, 段落序)]
    para_no: dict[tuple[int, int], int] = {}            # (blog 序, 段落序) -> P 編號
    warnings: list[str] = []

    def cite(quote: str) -> int:
        if quote in ref_no:
            return ref_no[quote]
        n = len(ref_no) + 1
        ref_no[quote] = n
        found: list[tuple[int, int]] = []
        for bi, blocks in enumerate(block_sets):
            idx = locate(blocks, quote)
            if idx is not None:
                for i in idx:
                    for j in range(max(0, i - neighbors), min(len(blocks), i + neighbors + 1)):
                        if (bi, j) not in found:
                            found.append((bi, j))
                break
        if not found:
            warnings.append(f"[{n}] 在段落切分後找不到（請先跑 validate_card.py）：{quote[:30]!r}")
        ref_blocks[n] = found
        for key in found:
            para_no.setdefault(key, len(para_no) + 1)
        return n

    def marks(quotes: list[str]) -> str:
        return "".join(f"[{cite(q)}]" for q in quotes)

    lines = [
        "# 觀念卡（對證者版）", "",
        f"- 標題：{card.front.get('title')}",
        f"- context_type：{card.front.get('context_type')}", "",
        "每條主張後面的 [n] 是引用編號，對應卡尾的參考文獻。參考文獻是 blog 的逐字原文（程式抽出，已驗證）。", "",
        "## 主張", "",
    ]
    others: list[dict] = []
    for c in card.claims:
        if only is not None and c["id"] not in only:
            others.append(c)
            continue
        head = f"[{c['id']}] role={c['role']}｜anchor_type={c['anchor_type']}｜status={c['status']}"
        lines.append(head)
        lines.append(f"  主張：{c['text']} {marks(c.get('source_quotes', []))}")
        for k in ("comparison_target", "numeric_kind", "numeric_reason"):
            if c.get(k):
                lines.append(f"  {k}：{c[k]}")
        if c.get("confirmation"):
            lines.append(f"  作者確認：{c['confirmation']}")
        for q in c.get("qualifiers") or []:
            lines.append(f"  限定條件：{q.get('text')} {marks([q['source_quote']]) if q.get('source_quote') else ''}")
        lines.append("")
    if others:
        lines += ["## 其他主張（已通過先前審查，只供主張互核，不必逐條審）", ""]
        for c in others:
            lines.append(f"- [{c['id']}] {c['text']}")
        lines.append("")

    lines += ["## 參考文獻（blog 原文，逐字）", ""]
    for q, n in sorted(ref_no.items(), key=lambda x: x[1]):
        if context == "paragraph":
            where = "、".join(f"P{para_no[k]}" for k in ref_blocks[n]) or "（找不到段落）"
            lines.append(f"[{n}] 「{q}」→ 見 {where}")
        else:
            lines.append(f"[{n}] 「{q}」")
    if context == "paragraph":
        lines += ["", "## 引文所在的 blog 段落（原文，含 markdown 標記）", ""]
        for key, p in sorted(para_no.items(), key=lambda x: x[1]):
            b = block_sets[key[0]][key[1]]
            lines += [f"### P{p}（小節：{b.heading or '（無標題）'}）", "", b.raw, ""]
    Path(out_path).write_text("\n".join(lines), encoding="utf-8")
    shown = len(only) if only is not None else len(card.claims)
    print(f"wrote {out_path}：審 {shown}/{len(card.claims)} 條主張，{len(ref_no)} 條引文，"
          f"{len(para_no) if context == 'paragraph' else 0} 個段落（{context}），約 {len(''.join(lines))} 字")
    for w in warnings:
        print("WARN", w)
    return 1 if warnings else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    only = set(a[a.index("--only") + 1].split(",")) if "--only" in a else None
    nb = int(a[a.index("--neighbors") + 1]) if "--neighbors" in a else 0
    ctx = a[a.index("--context") + 1] if "--context" in a else None
    sys.exit(main(a[0], a[1], only, nb, ctx))
