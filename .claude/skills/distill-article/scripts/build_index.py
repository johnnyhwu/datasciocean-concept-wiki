"""產生 wiki/index.md：id | 一句話論點 | parent | related | status。
index.md 由程式產生，不手改。去重與系列規劃都只讀這份，不需要打開每張卡。
用法：uv run python .claude/skills/distill-article/scripts/build_index.py
"""
from __future__ import annotations

import wikilib as W


def main() -> None:
    lines = ["# 觀念庫索引（程式產生，不手改）", "",
             "| id | 一句話論點 | parent | related | status |", "|---|---|---|---|---|"]
    for c in W.load_all_cards():
        thesis = next(x["text"] for x in c.claims if x["role"] == "thesis")
        rel = ", ".join(c.front.get("related") or []) or "-"
        lines.append(f"| {c.front['id']} | {thesis} | {c.front.get('parent') or '-'} | {rel} | {c.front.get('status')} |")
    (W.ROOT / "wiki" / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote wiki/index.md ({len(lines) - 4} cards)")


if __name__ == "__main__":
    main()
