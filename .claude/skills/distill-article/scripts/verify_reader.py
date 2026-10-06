"""驗證獨立讀者輸出（review-loop.md 關卡 2）。

用法：uv run python .claude/skills/distill-article/scripts/verify_reader.py <reader_copy.md> <reader.json> [--trap N ...]
--trap：陷阱題（卡上確實沒答案）的題號（1 起算，預設只有最後一題）。
        只有陷阱題可以答「卡上沒寫」；其他題答「沒寫」代表讀者漏看，算失敗。
- 主軸三題（論點、機制、證據）每題都要有「卡上真的存在」的引用；沒有就退回。答「卡上沒有」本身不通過主軸。
- 只能從卡回答的題目：答案不是「卡上沒寫」就必須有有效引用，否則算硬答，退回。
- 名詞問題只列為建議；blocks_core=true 的算退回。
結束碼：0 通過、1 退回。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import wikilib as W

NO_ANSWER = ("卡上沒寫", "卡上沒有", "卡上沒有寫")


def main(copy_path: str, reader_path: str, traps: list[int] | None = None) -> int:
    card_norm = W.normalize(Path(copy_path).read_text(encoding="utf-8"))
    data = json.loads(Path(reader_path).read_text(encoding="utf-8"))

    def valid_cites(cites: list[dict]) -> tuple[int, list[str]]:
        ok, bad = 0, []
        for c in cites or []:
            q = c.get("quote", "")
            if q and W.quote_in_text(q, card_norm):
                ok += 1
            else:
                bad.append(q[:30])
        return ok, bad

    rejects, notes = [], []
    for key, label in (("thesis", "論點"), ("mechanism", "機制"), ("evidence", "證據")):
        item = (data.get("core") or {}).get(key) or {}
        ans = item.get("answer", "")
        ok, bad = valid_cites(item.get("citations"))
        if any(n in ans for n in NO_ANSWER) and ok == 0:
            rejects.append(f"主軸「{label}」：讀者答卡上沒有")
        elif ok == 0:
            rejects.append(f"主軸「{label}」：沒有有效引用（引用不出來就算需要外部知識）")
        if bad:
            notes.append(f"主軸「{label}」有 {len(bad)} 筆引用不在卡上：{bad}")
    for t in data.get("terms", []):
        line = f"名詞 {t.get('term')}：{t.get('note','')[:60]}"
        if t.get("blocks_core"):
            rejects.append("名詞擋住主軸理解｜" + line)
        else:
            notes.append("名詞建議｜" + line)
    qs = data.get("card_only_questions", [])
    trap_set = set(traps or [len(qs)])
    for i, q in enumerate(qs, 1):
        ans = q.get("answer", "")
        ok, bad = valid_cites(q.get("citations"))
        said_none = any(n in ans for n in NO_ANSWER)
        if i in trap_set:
            if not said_none:
                rejects.append(f"陷阱題硬答：{q.get('q','')[:40]}｜答：{ans[:50]}")
        elif said_none:
            rejects.append(f"漏看（卡上有答案卻答沒寫）：{q.get('q','')[:40]}")
        elif ok == 0:
            rejects.append(f"硬答（沒有有效引用）：{q.get('q','')[:40]}｜答：{ans[:50]}")
        notes.append(f"題目：{q.get('q','')[:50]} → {'卡上沒寫' if said_none else ans[:60]}")

    print(f"== reader {data.get('card_id')}: {'退回' if rejects else '通過'}（退回 {len(rejects)}，備註 {len(notes)}）")
    for r in rejects:
        print("  退回", r)
    for n in notes:
        print("  備註", n)
    return 1 if rejects else 0


if __name__ == "__main__":
    args = sys.argv[3:]
    traps = [int(a) for a in args[1:]] if args and args[0] == "--trap" else None
    sys.exit(main(sys.argv[1], sys.argv[2], traps))
