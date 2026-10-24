"""Stage 1 程式檢查的回歸測試：故意做壞的卡，程式必須抓到；正確的卡必須通過（測誤殺）。

用法（repo 根目錄）：uv run python tests/test_stage1_programs.py
範圍：validate_card（結構與逐字比對）、主張附圖（copy_figure、validate_card 的 figures 檢查、孤兒圖、指紋）、
make_auditor_copy（引文都能定位）、make_reader_copy、verify_reader、verify_audit 與 verify_final_audit（分級規則）。審查者（subagent）本身的嚴格度不在這裡測，見
.claude/skills/distill-article/references/regression-tests.md。
修改任何程式檢查或審查流程後，要重跑這份。
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
import os
import re
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
# 測試用的卡放在 tests/fixtures/concepts/（wiki/concepts/ 是真實觀念庫，可能是空的）
os.environ["DSO_CARDS_DIR"] = str(ROOT / "tests" / "fixtures" / "concepts")
sys.path.insert(0, str(ROOT / ".claude/skills/distill-article/scripts"))

import claim_fingerprints as CF  # noqa: E402
import copy_figure as CP  # noqa: E402
import make_auditor_copy as MAC  # noqa: E402
import make_reader_copy as MRC  # noqa: E402
import validate_card as VC  # noqa: E402
import verify_audit as VA  # noqa: E402
import verify_final_audit as VF  # noqa: E402
import verify_reader as VR  # noqa: E402
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

# ---------------------------------------------------------------- 1b. 主張數檢查（只在合併階段用 --claim-count）
class _FakeCard:
    def __init__(self, n: int) -> None:
        self.claims = [{}] * n


lo, hi = PARAMS["wiki"]["card_claim_range"]
check("claim-count：低於下限 → 擋下", any("少於下限" in e for e in VC.check_claim_count(_FakeCard(lo - 1), PARAMS)))
check("claim-count：高於上限 → 擋下", any("超過上限" in e for e in VC.check_claim_count(_FakeCard(hi + 1), PARAMS)))
check("claim-count：下限與上限本身放行（測誤殺）", not VC.check_claim_count(_FakeCard(lo), PARAMS) and not VC.check_claim_count(_FakeCard(hi), PARAMS))
_over = next((c for c in CARDS.values() if len(c.claims) > hi), None)
if _over is not None:
    with contextlib.redirect_stdout(io.StringIO()):
        rc_default = VC.main([str(_over.path)])
        rc_count = VC.main(["--claim-count", str(_over.path)])
    check("claim-count：預設不檢查，加 --claim-count 才擋（旗標有接上）", rc_default == 0 and rc_count == 1)
else:
    check("claim-count：fixtures 內需有一張超過上限的卡來測旗標", False)

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


# ---------------------------------------------------------------- 5. 數字檢查：名稱標籤與「計數」豁免
def label_claim(c: W.Card) -> None:
    x = claim(c, "c1")
    x["text"] = "Stage 3 與 D2S 的第 2 點，挑戰 5 見 §1，Step 2 的做法"
    x.pop("comparison_target", None)
    x.pop("numeric_kind", None)


def label_with_ratio(c: W.Card) -> None:
    x = claim(c, "c1")
    x["text"] = "Stage 3 快 25 倍"
    x.pop("comparison_target", None)
    x.pop("numeric_kind", None)


def count_claim(c: W.Card) -> None:
    x = claim(c, "c1")
    x["text"] = "訓練樣本有 80 筆"
    x.update(numeric_kind="non_comparative", numeric_reason="計數")
    x.pop("comparison_target", None)


def count_with_ratio(c: W.Card) -> None:
    x = claim(c, "c1")
    x["text"] = "訓練樣本有 80 筆，快 25 倍"
    x.update(numeric_kind="non_comparative", numeric_reason="計數")
    x.pop("comparison_target", None)


check("數字檢查：Stage 3、Step 2、D2S、第 2 點、挑戰 5、§1 這類名稱標籤不算含數字（測誤殺）",
      "沒有 comparison_target" not in errors_of(mutated(label_claim)))
check("數字檢查：名稱標籤旁邊有倍數仍擋下", "沒有 comparison_target" in errors_of(mutated(label_with_ratio)))
e = errors_of(mutated(count_claim))
check("數字檢查：「計數」豁免放行（測誤殺）", "不在允許清單" not in e and "比較性" not in e and "沒有 comparison_target" not in e)
check("數字檢查：「計數」豁免含倍數仍擋下", "比較性數字寫法" in errors_of(mutated(count_with_ratio)))


# ---------------------------------------------------------------- 6. make_reader_copy 與 verify_reader
def reader_copy_text(extra: str = "") -> str:
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "card.md"
        src.write_text(GOOD.path.read_text(encoding="utf-8") + extra, encoding="utf-8")
        out = Path(d) / "reader.md"
        MRC.main(str(src), str(out))
        return out.read_text(encoding="utf-8")


NOTES = "\n## 名詞補充（通用知識，非 blog 內容）\n\n- **recall**：所有真正相關的內容中，被找出來的比例。\n"
t = reader_copy_text(NOTES)
check("make_reader_copy：附上「名詞補充」小節", "名詞補充" in t and "被找出來的比例" in t)
check("make_reader_copy：仍不洩漏引文與參考文獻", "source_quotes" not in t and "source_quote" not in t)
check("make_reader_copy：沒有名詞補充的卡不多出內容", "名詞補充" not in reader_copy_text())


def run_reader(qa: list[tuple[str, str, list]], traps=None) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as d:
        copy_p = Path(d) / "reader.md"
        MRC.main(str(GOOD.path), str(copy_p))
        q1 = claim(GOOD, "c1")["text"]
        cite = [{"claim_id": "c1", "quote": q1}]
        data = {"card_id": GOOD.front["id"],
                "core": {k: {"answer": "x", "citations": cite} for k in ("thesis", "mechanism", "evidence")},
                "terms": [],
                "card_only_questions": [{"q": q, "answer": a, "citations": (cite if use else [])} for q, a, use in qa]}
        p = Path(d) / "r.json"
        p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = VR.main(str(copy_p), str(p), traps)
        return rc, buf.getvalue()


rc, _ = run_reader([("題一", "有答案", True), ("陷阱", "卡上沒寫", False)], [2])
check("verify_reader：有引用作答、陷阱題答沒寫 → 通過", rc == 0)
rc, _ = run_reader([("題一", "答案如下。另外卡上沒有說明某個細節。", True), ("陷阱", "卡上沒寫", False)], [2])
check("verify_reader：有引用的完整作答，順帶寫「卡上沒有說明…」→ 通過（測誤殺）", rc == 0)
rc, out = run_reader([("題一", "卡上沒寫", False), ("陷阱", "卡上沒寫", False)], [2])
check("verify_reader：專屬題答「卡上沒寫」→ 漏看，退回", rc == 1 and "漏看" in out)
rc, out = run_reader([("題一", "有答案", True), ("陷阱", "硬答一個", False)], [2])
check("verify_reader：陷阱題硬答 → 退回", rc == 1 and "陷阱題硬答" in out)


# ---------------------------------------------------------------- 7. 主張附圖（figures）
FIG_SLUG = "adaptive-chunking"


def pick_figure_card_parts() -> tuple[dict, str, str]:
    """從 blog 的圖挑出一張 + 它所在小節裡一句沒有數字的純文字，當測試卡的引文。"""
    blog = W.load_blog(FIG_SLUG, PARAMS)
    for img in W.blog_images(blog):
        if not img["section"]:
            continue
        lines = blog.body.splitlines()
        start = next((i for i, ln in enumerate(lines) if re.match(rf"^#{{2,6}}\s+{re.escape(img['section'])}\s*$", ln)), None)
        for ln in lines[start + 1:] if start is not None else []:
            if ln.startswith("#"):
                break
            t = ln.strip()
            if 15 <= len(t) <= 120 and not re.search(r"[\d*\[\]`|>{}!#-]", t) and "$" not in t:
                return img, img["section"], t
    raise RuntimeError(f"{FIG_SLUG} 找不到適合的圖與引文（blog 改動過？調整 FIG_SLUG）")


def write_card_file(card: W.Card, path: Path) -> None:
    path.write_text("---\n" + yaml.safe_dump(card.front, allow_unicode=True, sort_keys=False) + "---\n\n## 主張\n\n```yaml\n"
                    + yaml.safe_dump({"claims": card.claims}, allow_unicode=True, sort_keys=False) + "```\n", encoding="utf-8")


_fig_img, _fig_section, _fig_quote = pick_figure_card_parts()
_fig_blog = W.load_blog(FIG_SLUG, PARAMS)
_real_wiki = W.WIKI_DIR
with tempfile.TemporaryDirectory() as _tmp:
    W.WIKI_DIR = Path(_tmp) / "wiki"
    with contextlib.redirect_stdout(io.StringIO()) as _out:
        rc_copy = CP.main(FIG_SLUG, _fig_img["src"])
    _snippet = yaml.safe_load(_out.getvalue().split("貼進主張（與 text 同層）：\n", 1)[1])["figures"][0]
    _dest = W.WIKI_DIR / _snippet["file"]
    check("copy_figure：複製成功、sha256 與 blog 原圖一致",
          rc_copy == 0 and _dest.is_file() and W.sha256_of(_dest) == _snippet["sha256"] == W.sha256_of(_fig_blog.path.parent / _fig_img["src"]))
    with contextlib.redirect_stdout(io.StringIO()):
        rc_missing = CP.main(FIG_SLUG, "no-such-figure.png")
    check("copy_figure：blog 沒引用的檔名 → 擋下", rc_missing == 1)
    with contextlib.redirect_stdout(io.StringIO()) as _out4:
        CP.main(FIG_SLUG, _fig_img["src"], indent=4)
    _lines = _out4.getvalue().split("貼進主張（與 text 同層）：\n", 1)[1].splitlines()
    _snip4 = yaml.safe_load("\n".join(_lines))
    check("copy_figure --indent：每行縮排 4 格，仍是合法 YAML 且內容不變",
          all(ln.startswith("    ") for ln in _lines) and _snip4["figures"][0]["sha256"] == _snippet["sha256"])

    def fig_card(figs=None, status="normal") -> W.Card:
        front = {"id": "figure-test", "title": "附圖測試", "context_type": "evidence_from_single_source",
                 "sources": [{"article": FIG_SLUG, "article_title": _fig_blog.title, "url": "x",
                              "sections": [_fig_section], "first_appearance": True}],
                 "parent": None, "related": [], "status": "active"}
        base = {"text": _fig_quote, "source_quotes": [_fig_quote], "anchor_type": "部落格判斷", "status": "normal"}
        claims = [{"id": "c1", "role": "thesis", "importance": 1, **base, "status": status},
                  {"id": "c2", "role": "context", "importance": 2, **base}]
        if figs is not None:
            claims[0]["figures"] = figs
        return W.Card(Path("figure-test.md"), front, claims)

    def fig_errors(card: W.Card) -> str:
        err, _ = VC.check_card(card, ALL_IDS | {"figure-test"}, PARAMS, {})
        return "\n".join(err)

    good_fig = [dict(_snippet)]
    check("validate 放行（測誤殺）：附圖的主張", not fig_errors(fig_card(good_fig)), fig_errors(fig_card(good_fig))[:300])
    check("validate 放行（測誤殺）：沒有附圖的主張", not fig_errors(fig_card()))

    def with_fig(**kw):
        return fig_card([{**_snippet, **kw}])

    def lacks(k):
        return fig_card([{kk: v for kk, v in _snippet.items() if kk != k}])

    BAD_FIG = [
        ("figures 不是物件清單", fig_card(["x"]), "figures 必須是物件清單"),
        ("figures 超過每條主張張數上限", fig_card([dict(_snippet)] * (PARAMS["wiki"]["figure_max_per_claim"] + 1)), "超過每條主張上限"),
        ("figures 缺 sha256", lacks("sha256"), "缺少"),
        ("figures 缺 caption", lacks("caption"), "缺少"),
        ("figures 的 article 不在 sources", with_fig(article="jev-overview", file="figures/jev-overview/" + _snippet["src"]), "不在這張卡的 sources"),
        ("figures 的 file 路徑與 article／src 不符", with_fig(file="figures/other/" + _snippet["src"]), "file 必須是"),
        ("figures 的 src 不是 blog 引用的圖", with_fig(src="no-such.png", file=f"figures/{FIG_SLUG}/no-such.png"), "沒有 image shortcode"),
        ("figures 的 caption 與 blog 不一致", with_fig(caption=_snippet["caption"] + "（被改過）"), "caption 與 blog 的圖說不一致"),
        ("figures 的副檔名不在白名單", with_fig(src="x.exe", file=f"figures/{FIG_SLUG}/x.exe"), "副檔名"),
        ("figures 的 sha256 與 blog 原圖不符（blog 改了圖）", with_fig(sha256="0" * 64), "blog 的原圖已改變"),
        ("figures 的 sha256 與 wiki 內的圖不符", with_fig(sha256="0" * 64), "wiki 裡的圖與記錄的 sha256 不符"),
    ]
    for name, fc, expect in BAD_FIG:
        out = fig_errors(fc)
        check(f"validate 擋下：{name}", expect in out, f"預期含 {expect!r}，實際：{out[:200]!r}")

    _backup = _dest.read_bytes()
    _dest.write_bytes(_backup + b"tampered")
    check("validate 擋下：wiki 內的圖被改過", "wiki 裡的圖與記錄的 sha256 不符" in fig_errors(fig_card(good_fig)))
    _dest.unlink()
    check("validate 擋下：wiki 內沒有圖檔", "wiki 裡沒有這個檔案" in fig_errors(fig_card(good_fig)))
    _dest.write_bytes(_backup)

    check("孤兒圖：被主張引用的圖不算孤兒（測誤殺）", not VC.orphan_figures([fig_card(good_fig)]))
    stray = W.WIKI_DIR / "figures" / FIG_SLUG / "stray.png"
    stray.write_bytes(b"x")
    check("孤兒圖：沒被任何主張引用的圖 → 抓到", VC.orphan_figures([fig_card(good_fig)]) == [f"figures/{FIG_SLUG}/stray.png"])
    stray.unlink()

    # 指紋：換圖要觸發重審
    _dangling = fig_card(good_fig)
    _dangling.claims[0]["text"] = "如圖所示，" + _fig_quote
    _, _h = VC.check_card(_dangling, ALL_IDS | {"figure-test"}, PARAMS, {})
    check("validate HINT：主張文字有「如圖」這類指向圖的字眼", any("指向圖表" in h for h in _h))
    _ok = fig_card(good_fig)
    _ok.claims[0]["text"] = "在測試集上表現最好，" + _fig_quote
    _, _h2 = VC.check_card(_ok, ALL_IDS | {"figure-test"}, PARAMS, {})
    check("validate HINT：「上表現」不誤判成「上表」（測誤殺）", not any("指向圖表" in h for h in _h2))
    c_plain, c_fig = fig_card().claims[0], fig_card(good_fig).claims[0]
    c_new = fig_card([{**_snippet, "sha256": "1" * 64}]).claims[0]
    check("指紋：附圖與否、換圖都會改變指紋", len({CF.fp(c_plain), CF.fp(c_fig), CF.fp(c_new)}) == 3)

    # 審查副本
    card_path = Path(_tmp) / "figure-test.md"
    write_card_file(fig_card(good_fig), card_path)
    aud = Path(_tmp) / "aud.md"
    with contextlib.redirect_stdout(io.StringIO()):
        MAC.main(str(card_path), str(aud), None, 0, "paragraph")
    aud_text = aud.read_text(encoding="utf-8")
    check("auditor copy：列出參考圖的絕對路徑與 blog 圖說", str(_dest) in aud_text and _snippet["caption"][:10] in aud_text)
    check("auditor copy：列出卡上的 file 值（供審查者填 figure_checks）", f"file={_snippet['file']}" in aud_text)
    check("auditor copy：圖說標明不能當支持依據", "不能當主張的支持依據" in aud_text)
    rd = Path(_tmp) / "reader.md"
    MRC.main(str(card_path), str(rd))
    check("reader copy：不含附圖", "figures" not in rd.read_text(encoding="utf-8") and _snippet["file"] not in rd.read_text(encoding="utf-8"))

    # verify_audit 的 figure_checks
    def run_fig_audit(tweak=None, status="normal") -> tuple[int, str]:
        card = fig_card(good_fig, status=status)
        write_card_file(card, card_path)
        data = audit_json(card)
        data["claims"][0]["figure_checks"] = [{"file": _snippet["file"], "verdict": "一致", "location": "圖左上角", "read": "三個方塊", "note": ""}]
        if tweak:
            tweak(data)
        p = Path(_tmp) / "a.json"
        p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = VA.main(str(card_path), str(p), None, None)
        return rc, buf.getvalue()

    def fig_check(d):
        return d["claims"][0]["figure_checks"][0]

    rc, out = run_fig_audit()
    check("verify_audit 附圖：一致且寫出位置與內容 → 通過（測誤殺）", rc == 0, out[:200])
    rc, out = run_fig_audit(lambda d: fig_check(d).update(file=str(W.WIKI_DIR / _snippet["file"])))
    check("verify_audit 附圖：審查者填圖檔完整路徑也接受（測誤殺）", rc == 0, out[:200])
    rc, out = run_fig_audit(lambda d: d["claims"][0].update(figure_checks=None))
    check("verify_audit 附圖：figure_checks 為 null → 視為漏核、不當掉", rc == 1 and "沒有核對附圖" in out)
    rc, out = run_fig_audit(lambda d: d["claims"][0].pop("figure_checks"))
    check("verify_audit 附圖：沒有核對附圖 → 擋下", rc == 1 and "沒有核對附圖" in out)
    for v in ("矛盾", "不相關", "看不清"):
        rc, out = run_fig_audit(lambda d, v=v: fig_check(d).update(verdict=v))
        check(f"verify_audit 附圖：{v} → 擋下", rc == 1 and f"附圖{v}" in out)
    rc, out = run_fig_audit(lambda d: fig_check(d).update(location=""))
    check("verify_audit 附圖：一致但沒寫位置 → 擋下", rc == 1 and "沒有寫出圖上位置" in out)
    rc, out = run_fig_audit(lambda d: fig_check(d).update(verdict="差不多"))
    check("verify_audit 附圖：判定值非法 → 擋下", rc == 1 and "判定值非法" in out)
    rc, out = run_fig_audit(lambda d: fig_check(d).update(verdict="矛盾"), status="pending_author_confirmation")
    check("verify_audit 附圖：pending 主張的圖問題不擋（測誤殺）", rc == 0)

    # 圖說當限定條件的來源（只限範圍、資料集、設定；引文必須在這條主張自己附圖的圖說裡）
    _cap_frag = _snippet["caption"][:14]

    def cap_card(source="figure_caption", quote=None, figs=True) -> W.Card:
        card = fig_card(good_fig if figs else None)
        q = {"text": "範圍：這張圖說交代的設定", "source_quote": quote if quote is not None else _cap_frag}
        if source is not None:
            q["source"] = source
        card.claims[0]["qualifiers"] = [q]
        return card

    check("validate 放行（測誤殺）：限定條件引用這條主張自己附圖的圖說", not fig_errors(cap_card()), fig_errors(cap_card())[:300])
    check("validate 擋下：標明來源是圖說，但引文不在圖說裡",
          "未逐字出現在這條主張自己附的圖的圖說" in fig_errors(cap_card(quote="這句話不在任何圖說裡面的句子")))
    check("validate 擋下：標明來源是圖說，但這條主張沒有附圖",
          "未逐字出現在這條主張自己附的圖的圖說" in fig_errors(cap_card(figs=False)))
    check("validate 擋下：qualifier 的 source 不是 figure_caption", "source 只能是 figure_caption" in fig_errors(cap_card(source="blog")))
    check("validate 擋下：沒標來源的限定條件，引文是圖說（圖說不在 blog 引文範圍）",
          "未逐字出現在 blog" in fig_errors(cap_card(source=None)))
    check("指紋：限定條件的來源欄位改變會改變指紋", CF.fp(cap_card().claims[0]) != CF.fp(cap_card(source=None).claims[0]))

    write_card_file(cap_card(), card_path)
    with contextlib.redirect_stdout(io.StringIO()):
        MAC.main(str(card_path), str(aud), None, 0, "paragraph")
    check("auditor copy：圖說來源的限定條件標明「來源：這條主張附圖的圖說」", "來源：這條主張附圖的圖說" in aud.read_text(encoding="utf-8"))

    def run_cap_audit(tweak) -> tuple[int, str]:
        card = cap_card()
        data = audit_json(card)
        data["claims"][0]["figure_checks"] = [{"file": _snippet["file"], "verdict": "一致", "location": "圖左上角", "read": "三個方塊", "note": ""}]
        tweak(data)
        p = Path(_tmp) / "cap-audit.json"
        p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = VA.main(str(card_path), str(p), None, None)
        return rc, buf.getvalue()

    rc, out = run_cap_audit(lambda d: None)
    check("verify_audit：圖說來源的限定條件、其餘照常 → 通過（測誤殺）", rc == 0, out[:200])
    rc, out = run_cap_audit(lambda d: d["claims"][0]["atoms"][0].update(blog_quote=_cap_frag))
    check("verify_audit：只引用圖說就判完全支持 → 擋下（圖說不能撐主張）", rc == 1 and "只引用了圖說" in out, out[:200])
    rc, out = run_cap_audit(lambda d: d["claims"][0]["atoms"][0].update(blog_quote=_cap_frag, verdict="部分支持"))
    check("verify_audit：引用圖說但判部分支持 → 只記錄不擋", rc == 0 and "引用的是圖說" in out, out[:200])

    def run_cap_final(quote: str) -> tuple[int, str]:
        p = Path(_tmp) / "cap-final.json"
        p.write_text(json.dumps({"article": FIG_SLUG, "cross_card_conflicts": [], "blog_internal_contradictions": [],
                                 "findings": [{"card_id": "figure-test", "claim_ids": ["c1"], "type": "限定條件掉了",
                                               "blog_quote": quote, "note": "x"}]}, ensure_ascii=False), encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = VF.main(str(p), [str(card_path)])
        return rc, buf.getvalue()

    rc, out = run_cap_final(_cap_frag)
    check("verify_final_audit：審查者引用圖說也算 blog 原文（成立的發現會擋）", rc == 1 and "BLOCKER" in out, out[:200])
    rc, out = run_cap_final("捏造的圖說內容")
    check("verify_final_audit：引用不在 blog 也不在圖說 → 只記錄", rc == 0, out[:200])
    W.WIKI_DIR = _real_wiki

print(f"\n{'全部通過' if not fails else f'{len(fails)} 項失敗：' + '; '.join(fails)}")
sys.exit(1 if fails else 0)
