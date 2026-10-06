"""主張指紋：判斷哪些主張是「新增或改過的」，只重審它們（第一次實跑後與人討論採用）。

用法：
  uv run python .claude/skills/distill-article/scripts/claim_fingerprints.py save <accepted.json> <card.md> [--blockers c1,c2]
      把這張卡「未被擋下」的主張指紋存進 accepted.json（累加）。--blockers 的主張不存。
  uv run python .claude/skills/distill-article/scripts/claim_fingerprints.py diff <accepted.json> <card.md>
      印出這張卡需要審的 claim id（指紋不在 accepted.json 裡的）。
指紋涵蓋：role、text、source_quotes、anchor_type、comparison_target、qualifiers、status、numeric_*。
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import wikilib as W

KEYS = ("role", "text", "source_quotes", "anchor_type", "comparison_target",
        "qualifiers", "status", "numeric_kind", "numeric_reason")


def fp(claim: dict) -> str:
    payload = json.dumps({k: claim.get(k) for k in KEYS}, ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def main(argv: list[str]) -> int:
    cmd, acc_path, card_path = argv[0], Path(argv[1]), Path(argv[2])
    card = W.parse_card(card_path)
    acc = set(json.loads(acc_path.read_text())) if acc_path.exists() else set()
    if cmd == "save":
        blockers = set()
        if "--blockers" in argv:
            blockers = set(argv[argv.index("--blockers") + 1].split(","))
        for c in card.claims:
            if c["id"] not in blockers:
                acc.add(fp(c))
        acc_path.write_text(json.dumps(sorted(acc)))
        print(f"saved {len(acc)} fingerprints")
    elif cmd == "diff":
        need = [c["id"] for c in card.claims if fp(c) not in acc]
        print(",".join(need))
        print(f"# {card.path.name}: {len(need)}/{len(card.claims)} 條需要審", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
