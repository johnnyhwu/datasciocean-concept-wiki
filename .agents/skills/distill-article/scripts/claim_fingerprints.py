"""主張指紋：判斷哪些主張是「新增或改過的」，只重審它們。

用法：
  uv run python .agents/skills/distill-article/scripts/claim_fingerprints.py save <accepted.json> <card.md> --snapshot <aud.md>.fp.json [--blockers c1,c2]
      把「送審時」未被擋下的主張指紋存進 accepted.json（累加）。--blockers 的主張不存。
      --snapshot 是 make_auditor_copy.py 寫出的快照：存的是送審當下的版本，所以審完先改卡再 save 也不會把改過的主張誤存成通過。
      不給 --snapshot 時退回用卡的現況（只適合卡在審完後完全沒動過），並印出警告。
  uv run python .agents/skills/distill-article/scripts/claim_fingerprints.py diff <accepted.json> <card.md>
      印出這張卡需要審的 claim id（指紋不在 accepted.json 裡的）。
指紋涵蓋：role、text、source_quotes、anchor_type、comparison_target、qualifiers、status、numeric_*、figures（含 sha256，所以換圖會觸發重審）。
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import wikilib as W

KEYS = ("role", "text", "source_quotes", "anchor_type", "comparison_target",
        "qualifiers", "status", "numeric_kind", "numeric_reason", "figures")


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
        if "--snapshot" in argv:
            snap = json.loads(Path(argv[argv.index("--snapshot") + 1]).read_text())
            for cid, f in snap.items():
                if cid not in blockers:
                    acc.add(f)
            changed = [c["id"] for c in card.claims if c["id"] in snap and fp(c) != snap[c["id"]]]
            if changed:
                print(f"# 送審後改過、不會被當成通過：{','.join(changed)}", file=sys.stderr)
        else:
            print("WARN 沒給 --snapshot：用卡的現況存指紋；審完後改過的主張會被誤存成通過", file=sys.stderr)
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
