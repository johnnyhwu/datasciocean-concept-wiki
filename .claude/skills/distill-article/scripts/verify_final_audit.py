"""驗證「全文審查」輸出並彙整（引用由程式驗證）。

全文審查：整篇 blog 只讀一次，一個審查者同時審這篇文章提煉出的所有卡，專抓
「引文以外」的問題：斷章取義、限定條件掉了、錨點歸屬、跨卡矛盾、blog 內部矛盾、卡漏掉的重點。

用法：uv run python .claude/skills/distill-article/scripts/verify_final_audit.py <final.json> <card.md> [<card.md> ...]
分級（沿用 verify_audit.py 的原則）：
  擋下（blocker）：type 為「斷章取義」「限定條件掉了」，或「錨點歸屬錯」且該主張標「官方宣稱」。
  交人裁決（escalate）：跨卡矛盾、blog 內部矛盾（卡要不要用保守寫法由人決定）。
  只記錄（minor）：卡漏掉重點、其他錨點邊界、pending 主張的問題、審查者引用錯誤。
結束碼：0 通過、1 有 blocker、2 沒有 blocker 但有要交人裁決的項目。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import wikilib as W

BLOCKER_TYPES = {"斷章取義", "限定條件掉了"}
ALL_TYPES = BLOCKER_TYPES | {"錨點歸屬錯", "卡漏掉重點", "其他"}


def main(final_path: str, card_paths: list[str]) -> int:
    params = W.load_params()
    cards = {W.parse_card(Path(p)).front["id"]: W.parse_card(Path(p)) for p in card_paths}
    slugs = sorted({s["article"] for c in cards.values() for s in c.front.get("sources", [])})
    norms = [W.load_blog(s, params).full_norm for s in slugs]
    data = json.loads(Path(final_path).read_text(encoding="utf-8"))

    def in_blog(q: str) -> bool:
        return bool(q) and any(W.quote_in_text(q, n) for n in norms)

    claim = lambda cid, kid: next((x for x in cards[cid].claims if x["id"] == kid), None) if cid in cards else None
    blockers, escalate, notes = [], [], []

    for f in data.get("findings", []):
        t, cid = f.get("type"), f.get("card_id")
        tag = f"[{cid}:{','.join(f.get('claim_ids', []))}] {t}"
        if t not in ALL_TYPES:
            notes.append(f"{tag}：類別不在固定清單")
            continue
        bq = f.get("blog_quote", "")
        if t != "卡漏掉重點" and not in_blog(bq):
            notes.append(f"{tag}：審查者引用未逐字出現在 blog（審查者的錯，需人眼確認）：{bq[:30]!r}")
            continue
        targets = [claim(cid, k) for k in f.get("claim_ids", [])]
        if targets and all(x is not None and x.get("status") == "pending_author_confirmation" for x in targets):
            notes.append(f"{tag}（pending，不擋）：{f.get('note','')[:80]}")
            continue
        if t in BLOCKER_TYPES or (t == "錨點歸屬錯" and any(x and x.get("anchor_type") == "官方宣稱" for x in targets)):
            blockers.append(f"{tag}｜{f.get('note','')[:100]}｜blog：{bq[:40]!r}")
        else:
            notes.append(f"{tag}：{f.get('note','')[:100]}")

    for x in data.get("cross_card_conflicts", []):
        escalate.append(f"跨卡矛盾 {x.get('items')}：{x.get('note','')[:120]}")
    for x in data.get("blog_internal_contradictions", []):
        bad = [q for q in x.get("quotes", []) if not in_blog(q)]
        flag = "（含未逐字的引用，需人工確認）" if bad else ""
        escalate.append(f"blog 內部矛盾{flag}：{x.get('description','')[:120]} 相關 {x.get('related')}")

    print(f"== 全文審查 {slugs}: {'退回' if blockers else ('交人裁決' if escalate else '通過')}"
          f"（blocker {len(blockers)}，交人 {len(escalate)}，備註 {len(notes)}）")
    for b in blockers:
        print("  BLOCKER", b)
    for e in escalate:
        print("  交人", e)
    for n in notes:
        print("  備註", n)
    return 1 if blockers else (2 if escalate else 0)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2:]))
