"""產生「獨立讀者」看的卡副本（只看卡，不看 blog，也沒有引用與參考文獻）。

保留：id、title、context_type、claims 的 id／role／text／anchor_type／comparison_target／status／importance
      與 qualifiers 的文字。
拿掉：sources（url、小節名）、source_quotes 與 qualifiers 的 source_quote（引用與參考文獻）、
      numeric_kind／numeric_reason／confirmation 等內部欄位。
讀者只能引用主張的 text 與限定條件的 text。

用法：uv run python .claude/skills/distill-article/scripts/make_reader_copy.py <card.md> <out.md>
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

import wikilib as W

DROP_CLAIM_KEYS = {"numeric_kind", "numeric_reason", "confirmation", "source_quotes"}


def main(card_path: str, out_path: str) -> None:
    card = W.parse_card(Path(card_path))
    front = {k: card.front[k] for k in ("id", "title", "context_type") if k in card.front}
    claims = []
    for c in card.claims:
        d = {k: v for k, v in c.items() if k not in DROP_CLAIM_KEYS}
        if d.get("qualifiers"):
            d["qualifiers"] = [{"text": q.get("text")} for q in d["qualifiers"]]
        claims.append(d)
    text = (
        "# 觀念卡（讀者版）\n\n```yaml\n"
        + yaml.safe_dump({"card": front, "claims": claims}, allow_unicode=True, sort_keys=False)
        + "```\n"
    )
    Path(out_path).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
