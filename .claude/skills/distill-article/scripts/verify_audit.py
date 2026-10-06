"""驗證對證者輸出並彙整退回清單（引用由程式驗證）。

用法：uv run python .claude/skills/distill-article/scripts/verify_audit.py <card.md> <auditor.json>
        [--only c1,c3]      只看指定主張（補審改動的主張時用）
        [--copy <auditor-copy.md>]   對證者拿到的卡副本；引用必須出自這份副本（引用副本以外的 blog 原文
                                     代表對證者越界讀了 blog，列入備註）
- 對證者引用的 blog 原文必須逐字出現在 blog，否則該筆判定一律視為「找不到」。
- 判定為「完全支持」但沒有引用的，視為「找不到」。
- 分級（references/review-loop.md「分級退回」）：
    擋下（blocker）：判定為「不支持／找不到」、引用捏造、或固定錯誤屬於
        數字對不上、範圍被放大、因果說得比原文強、夾帶blog沒有的判斷、限定條件掉了、舉例變成唯一，
        或「錨點類型標錯」且卡上標的是「官方宣稱」（Stage 2 的主詞規則依賴它）。
    只記錄（minor）：主張與來源措辭不同、來源沒涵蓋主張的每個成分、限定詞沒定義、
        其他錨點類型邊界、主張互核矛盾、審查者自己的引用錯誤。
  有 blocker 才整張卡退回；minor 只列在備註。
結束碼：0 全部通過、1 有退回項目。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import wikilib as W

VERDICTS = {"完全支持", "部分支持", "不支持", "找不到"}
BLOCKER_ERRORS = {"數字對不上", "範圍被放大", "因果說得比原文強", "夾帶blog沒有的判斷",
                  "限定條件掉了", "舉例變成唯一"}
FIXED_ERRORS = {
    "數字對不上", "範圍被放大", "舉例變成唯一", "錨點類型標錯", "限定條件掉了",
    "夾帶blog沒有的判斷", "因果說得比原文強", "限定詞沒定義", "來源沒涵蓋主張的每個成分",
    "主張與來源措辭不同", "其他",
}


def main(card_path: str, audit_path: str, only_ids: list[str] | None = None, copy_path: str | None = None) -> int:
    params = W.load_params()
    copy_norm = W.normalize(Path(copy_path).read_text(encoding="utf-8")) if copy_path else None
    card = W.parse_card(Path(card_path))
    audit = json.loads(Path(audit_path).read_text(encoding="utf-8"))
    slugs = [s["article"] for s in card.front.get("sources", [])]
    blogs = [W.load_blog(s, params) for s in slugs]
    norms = [b.full_norm for b in blogs]

    def in_blog(q: str) -> bool:
        return bool(q) and any(W.quote_in_text(q, n) for n in norms)

    rejects: list[str] = []   # blocker
    notes: list[str] = []     # minor 與備註
    audited = {c["claim_id"]: c for c in audit.get("claims", [])}
    pending_ids = {c["id"] for c in card.claims if c.get("status") == "pending_author_confirmation"}
    claim_by_id = {c["id"]: c for c in card.claims}
    only = set(only_ids) if only_ids else None
    for c in card.claims:
        cid = c["id"]
        if only is not None and cid not in only:
            continue
        entry = audited.get(cid)
        if not entry:
            rejects.append(f"[{cid}] 對證者沒有審這條主張")
            continue
        blockers, minors = [], []
        if not entry.get("atoms"):
            blockers.append("沒有拆出任何原子主張")
        for a in entry.get("atoms", []):
            v = a.get("verdict")
            q = a.get("blog_quote", "")
            txt = a.get("text", "")[:40]
            if v not in VERDICTS:
                blockers.append(f"判定值非法：{v!r}")
                continue
            if q and not in_blog(q):
                minors.append(f"審查者引用未逐字出現在 blog（審查者的錯，需人眼確認）：{q[:30]!r}… 原判定 {v}")
                continue
            if q and copy_norm is not None and not W.quote_in_text(q, copy_norm):
                minors.append(f"審查者引用了卡副本以外的 blog 原文（越界讀 blog？）：{q[:30]!r}")
            if v == "完全支持" and not q:
                minors.append(f"判完全支持但沒有引用：{txt!r}")
            elif "anchor" in a.get("text", "").lower() or "錨點" in a.get("text", ""):
                # 錨點類型的邊界爭議：只有卡標「官方宣稱」時才擋（Stage 2 主詞規則依賴它）
                if v != "完全支持":
                    if claim_by_id[cid].get("anchor_type") == "官方宣稱":
                        blockers.append(f"錨點類型 {v}（卡標官方宣稱）：{txt!r}")
                    else:
                        minors.append(f"錨點類型 {v}：{txt!r}｜{a.get('note','')[:60]}")
            elif v in ("不支持", "找不到"):
                blockers.append(f"{v}：{txt!r}｜{a.get('note','')[:80]}")
            elif v == "部分支持":
                minors.append(f"部分支持：{txt!r}｜{a.get('note','')[:80]}")
        for e in entry.get("errors", []):
            if e not in FIXED_ERRORS:
                notes.append(f"[{cid}] 錯誤類別不在固定清單：{e!r}")
            elif e in BLOCKER_ERRORS:
                blockers.append(f"固定錯誤：{e}")
            elif e == "錨點類型標錯" and claim_by_id[cid].get("anchor_type") == "官方宣稱":
                blockers.append("固定錯誤：錨點類型標錯（卡標官方宣稱）")
            else:
                minors.append(f"固定錯誤：{e}")
        if blockers and cid in pending_ids:
            minors.extend(f"（pending，不擋）{b}" for b in blockers)
            blockers = []
        if blockers:
            rejects.append(f"[{cid}] " + "；".join(blockers))
        if minors:
            notes.append(f"[{cid}] minor：" + "；".join(minors))

    for x in audit.get("cross_claim_conflicts", []):
        notes.append(f"主張互核（minor）{x.get('claims')}：{x.get('note','')[:100]}")
    for x in audit.get("blog_internal_contradictions", []):
        qs = x.get("quotes", [])
        bad = [q for q in qs if not in_blog(q)]
        flag = "（含未逐字的引用，需人工確認）" if bad else ""
        notes.append(f"blog 內部矛盾{flag}：{x.get('description','')[:120]} 相關主張 {x.get('related_claims')}")
    for r in audit.get("recalculations", []):
        notes.append(f"重算 [{r.get('claim_id')}] {r.get('expression')} = {r.get('result')}")
    for g in audit.get("card_gaps", []):
        notes.append(f"卡漏掉：{g.get('description','')[:100]}")

    print(f"== {card.path.name}: {'退回' if rejects else '通過'}（blocker {len(rejects)}，備註 {len(notes)}）")
    for r in rejects:
        print("  BLOCKER", r)
    for n in notes:
        print("  備註", n)
    return 1 if rejects else 0


if __name__ == "__main__":
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1].split(",")
    cp = sys.argv[sys.argv.index("--copy") + 1] if "--copy" in sys.argv else None
    sys.exit(main(sys.argv[1], sys.argv[2], only, cp))
