"""Stage 1 程式檢查的回歸測試：故意做壞的卡，程式必須抓到；正確的卡必須通過（測誤殺）。

用法（repo 根目錄）：uv run python tests/test_stage1_programs.py
範圍：validate_card（結構與逐字比對）、make_auditor_copy（引文都能定位）、verify_audit 與
verify_final_audit（分級規則）。審查者（subagent）本身的嚴格度不在這裡測，見
.claude/skills/distill-article/references/regression-tests.md。
修改任何程式檢查或審查流程後，要重跑這份。
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# 測試用的卡放在 tests/fixtures/concepts/（wiki/concepts/ 是真實觀念庫，可能是空的）
os.environ["DSO_CARDS_DIR"] = str(ROOT / "tests" / "fixtures" / "concepts")
sys.path.insert(0, str(ROOT / ".claude/skills/distill-article/scripts"))

import make_auditor_copy as MAC  # noqa: E402
import validate_card as VC  # noqa: E402
import verify_audit as VA  # noqa: E402
import verify_final_audit as VF  # noqa: E402
import wikilib as W  # noqa: E402

PARAMS = W.load_params()
CARDS = {c.front["id"]: c for c in W.load_all_cards()}
ALL_IDS = set(CARDS)
GOOD = CARDS["schema-valid-not-correct"]
fails: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    print(("PASS " if ok else "FAIL ") + name + (f"  {detail}" if detail and not ok else ""))
    if not ok:
        fails.append(name)


def mutated(fn) -> W.Card:
    c = copy.deepcopy(GOOD)
    fn(c)
    return c


def errors_of(card: W.Card) -> str:
    err, _ = VC.check_card(card, ALL_IDS, PARAMS, {})
    return "\n".join(err)


def claim(card: W.Card, cid: str) -> dict:
    return next(c for c in card.claims if c["id"] == cid)


# ---------------------------------------------------------------- 1. validate_card：壞卡要被擋
def other_section_quote() -> str:
    """一段真實存在於 blog、但不在 GOOD 列出的小節內的引文。"""
    blog = W.load_blog("jev-overview", PARAMS)
    allowed = [s for t in GOOD.front["sources"][0]["sections"] for s in W.find_sections(blog, t)]
    for card in CARDS.values():
        for c in card.claims:
            for q in c.get("source_quotes", []):
                if W.quote_in_text(q, blog.full_norm) and not any(W.quote_in_text(q, s.body_norm) for s in allowed):
                    return q
    raise RuntimeError("找不到小節外的引文")


def num_claim(c: W.Card) -> None:
    x = claim(c, "c1")
    x["text"] += "，快 25 倍"
    x.pop("comparison_target", None)


BAD = [
    ("數字主張沒有比較對象", num_claim, "沒有 comparison_target"),
    ("沒有脈絡主張", lambda c: claim(c, "c2").update(role="mechanism"), "至少需要一條 role=context"),
    ("兩條 thesis", lambda c: claim(c, "c2").update(role="thesis"), "thesis 必須恰好一條"),
    ("來源原文是捏造的", lambda c: claim(c, "c1").update(source_quotes=["這句話 blog 裡根本沒有出現過的捏造出處"]), "未逐字出現在 blog"),
    ("來源原文不在列出的小節內", lambda c: claim(c, "c1").update(source_quotes=[other_section_quote()]), "不在 sources.sections"),
    ("豁免數字卻含倍數", lambda c: (claim(c, "c1").update(text="快 25 倍", numeric_kind="non_comparative", numeric_reason="規格上限"),
                              claim(c, "c1").pop("comparison_target", None)), "比較性數字寫法"),
    ("豁免理由不在清單", lambda c: (claim(c, "c1").update(text="上限是 8 個", numeric_kind="non_comparative", numeric_reason="隨便"),
                              claim(c, "c1").pop("comparison_target", None)), "numeric_reason"),
    ("author_confirmed 沒有日期", lambda c: claim(c, "c1").update(status="author_confirmed"), "confirmation.date"),
    ("錨點類型不在清單", lambda c: claim(c, "c1").update(anchor_type="亂寫"), "不在清單內"),
    ("thesis 重要度不是 1", lambda c: claim(c, "c1").update(importance=2), "importance 必須是 1"),
    ("缺 article_title", lambda c: c.front["sources"][0].pop("article_title"), "缺少 article_title"),
    ("article_title 與 blog 不符", lambda c: c.front["sources"][0].update(article_title="別篇文章"), "article_title 與 blog 標題不一致"),
    ("來源小節不存在", lambda c: c.front["sources"][0].update(sections=["不存在的小節標題"]), "來源段落不存在"),
    ("related 指向不存在的觀念", lambda c: c.front.update(related=["no-such-concept"]), "指向不存在的觀念"),
    ("frontmatter id 與檔名不符", lambda c: c.front.update(id="other-id"), "與檔名"),
    ("claim id 重複", lambda c: claim(c, "c2").update(id="c1"), "claim id 卡內重複"),
    ("沒有任何 claim", lambda c: c.claims.clear(), "沒有任何 claim"),
]
for name, fn, expect in BAD:
    out = errors_of(mutated(fn))
    check(f"validate 擋下：{name}", expect in out, f"預期含 {expect!r}，實際：{out[:200]!r}")

for cid, card in CARDS.items():
    check(f"validate 放行（測誤殺）：{cid}", not errors_of(card), errors_of(card)[:200])

# ---------------------------------------------------------------- 2. make_auditor_copy：每條引文都定位得到
for cid, card in CARDS.items():
    blogs = [W.load_blog(s["article"], PARAMS) for s in card.front["sources"]]
    sets = [MAC.split_blocks(b.body) for b in blogs]
    bad = []
    for c in card.claims:
        for q in list(c.get("source_quotes", [])) + [x["source_quote"] for x in c.get("qualifiers") or [] if x.get("source_quote")]:
            hit = [MAC.locate(bs, q) for bs in sets]
            if not any(h for h in hit):
                bad.append(f"{c['id']}:{q[:20]}")
    check(f"auditor copy 引文都能定位到段落：{cid}", not bad, str(bad[:3]))

with tempfile.TemporaryDirectory() as d:
    out = Path(d) / "a.md"
    with contextlib.redirect_stdout(io.StringIO()):
        MAC.main(str(GOOD.path), str(out), {"c1"}, 0, "paragraph")
    text = out.read_text(encoding="utf-8")
    check("auditor copy --only：其他主張只列文字、不附引用", "## 其他主張" in text and text.count("主張：") == 1)
    with contextlib.redirect_stdout(io.StringIO()):
        MAC.main(str(GOOD.path), str(out), None, 0, "quote")
    check("auditor copy quote 模式沒有段落區塊", "## 引文所在的 blog 段落" not in out.read_text(encoding="utf-8"))
    check("auditor copy 不洩漏 sources 的 url", "datasciocean.com" not in text)


# ---------------------------------------------------------------- 3. verify_audit 分級
def audit_json(card: W.Card, tweak=None) -> dict:
    claims = []
    for c in card.claims:
        claims.append({"claim_id": c["id"], "errors": [],
                       "atoms": [{"text": c["text"][:20], "verdict": "完全支持", "blog_quote": c["source_quotes"][0], "note": ""}]})
    data = {"card_id": card.front["id"], "claims": claims, "recalculations": [], "cross_claim_conflicts": [],
            "blog_internal_contradictions": [], "card_gaps": []}
    if tweak:
        tweak(data)
    return data


def run_audit(data: dict, copy_path: str | None = None) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "a.json"
        p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = VA.main(str(GOOD.path), str(p), None, copy_path)
        return rc, buf.getvalue()


def first_atom(d, cid="c1"):
    return next(c for c in d["claims"] if c["claim_id"] == cid)["atoms"][0]


def claim_entry(d, cid):
    return next(c for c in d["claims"] if c["claim_id"] == cid)


rc, _ = run_audit(audit_json(GOOD))
check("verify_audit：全部完全支持 → 通過", rc == 0)
rc, out = run_audit(audit_json(GOOD, lambda d: first_atom(d).update(verdict="不支持")))
check("verify_audit：不支持 → 擋下", rc == 1 and "BLOCKER" in out)
rc, _ = run_audit(audit_json(GOOD, lambda d: claim_entry(d, "c1").update(errors=["數字對不上"])))
check("verify_audit：數字對不上 → 擋下", rc == 1)
rc, _ = run_audit(audit_json(GOOD, lambda d: claim_entry(d, "c1").update(errors=["主張與來源措辭不同"])))
check("verify_audit：措辭不同 → 只記錄不擋（測誤殺）", rc == 0)
rc, _ = run_audit(audit_json(GOOD, lambda d: first_atom(d).update(verdict="部分支持", note="x")))
check("verify_audit：部分支持 → 只記錄不擋", rc == 0)
rc, out = run_audit(audit_json(GOOD, lambda d: first_atom(d).update(blog_quote="blog 沒有的捏造引用", verdict="不支持")))
check("verify_audit：審查者的捏造引用 → 列備註、不擋卡", rc == 0 and "審查者引用未逐字" in out)
rc, _ = run_audit(audit_json(GOOD, lambda d: d["claims"].pop()))
check("verify_audit：漏審一條主張 → 擋下", rc == 1)
rc, _ = run_audit(audit_json(GOOD, lambda d: claim_entry(d, "c7").update(atoms=[{"text": "x", "verdict": "找不到", "blog_quote": "", "note": ""}])))
check("verify_audit：pending 主張的問題不擋（測誤殺）", rc == 0)
rc, _ = run_audit(audit_json(GOOD, lambda d: (claim_entry(d, "c3")["atoms"][0].update(text="錨點類型：官方宣稱", verdict="不支持"))))
check("verify_audit：卡標官方宣稱而錨點類型被判不支持 → 擋下", rc == 1)
rc, _ = run_audit(audit_json(GOOD, lambda d: (claim_entry(d, "c6")["atoms"][0].update(text="錨點類型：社群評論", verdict="不支持"))))
check("verify_audit：其他錨點邊界爭議 → 只記錄（測誤殺）", rc == 0)

with tempfile.TemporaryDirectory() as d:
    cp = Path(d) / "copy.md"
    with contextlib.redirect_stdout(io.StringIO()):
        MAC.main(str(GOOD.path), str(cp), {"c1"}, 0, "paragraph")
    data = audit_json(GOOD)
    claim_entry(data, "c3")["atoms"][0]["blog_quote"] = claim(GOOD, "c4")["source_quotes"][0]  # 真的 blog 原文，但不在 c1 的副本內
    data["claims"] = [c for c in data["claims"] if c["claim_id"] in ("c1", "c3")]
    with tempfile.TemporaryDirectory() as d2:
        p = Path(d2) / "a.json"
        p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            VA.main(str(GOOD.path), str(p), ["c1", "c3"], str(cp))
        check("verify_audit --copy：引用副本以外的原文 → 列備註", "越界" in buf.getvalue())


# ---------------------------------------------------------------- 4. verify_final_audit 分級
def run_final(data: dict) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "f.json"
        p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = VF.main(str(p), [str(GOOD.path)])
        return rc, buf.getvalue()


REAL_Q = claim(GOOD, "c1")["source_quotes"][0]
base = {"article": "jev-overview", "findings": [], "cross_card_conflicts": [], "blog_internal_contradictions": []}
rc, _ = run_final(base)
check("final audit：沒有發現 → 通過", rc == 0)
rc, out = run_final({**base, "findings": [{"card_id": GOOD.front["id"], "claim_ids": ["c1"], "type": "斷章取義", "blog_quote": REAL_Q, "note": "x"}]})
check("final audit：斷章取義（引文真實）→ 擋下", rc == 1 and "BLOCKER" in out)
rc, out = run_final({**base, "findings": [{"card_id": GOOD.front["id"], "claim_ids": ["c1"], "type": "斷章取義", "blog_quote": "捏造的原文", "note": "x"}]})
check("final audit：審查者引用不逐字 → 只記錄", rc == 0)
rc, _ = run_final({**base, "findings": [{"card_id": GOOD.front["id"], "claim_ids": ["c7"], "type": "限定條件掉了", "blog_quote": REAL_Q, "note": "x"}]})
check("final audit：pending 主張的問題不擋（測誤殺）", rc == 0)
rc, _ = run_final({**base, "findings": [{"card_id": GOOD.front["id"], "claim_ids": ["c1"], "type": "卡漏掉重點", "blog_quote": REAL_Q, "note": "x"}]})
check("final audit：卡漏掉重點 → 只記錄", rc == 0)
rc, _ = run_final({**base, "cross_card_conflicts": [{"items": [], "note": "x"}]})
check("final audit：跨卡矛盾 → 交人裁決（exit 2）", rc == 2)
rc, _ = run_final({**base, "blog_internal_contradictions": [{"description": "x", "quotes": [REAL_Q], "related": []}]})
check("final audit：blog 內部矛盾 → 交人裁決（exit 2）", rc == 2)

print(f"\n{'全部通過' if not fails else f'{len(fails)} 項失敗：' + '; '.join(fails)}")
sys.exit(1 if fails else 0)
