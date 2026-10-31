"""雙向寫入 `related`：不手改卡的 frontmatter（手改容易縮排錯、漏寫另一邊）。

用法：
  uv run python .claude/skills/distill-article/scripts/add_related.py <hub-id> <id> [<id> ...]
      hub 與每個 id 互設 related（例如新卡連到既有卡）。
  uv run python .claude/skills/distill-article/scripts/add_related.py --mesh <id> <id> [<id> ...]
      列出的卡兩兩互設（例如同一篇文章的卡）。
已存在的連結不重複加；沿用該卡原本的清單縮排（沒有既有項目時用兩格）。只改 related，其餘文字不動。
"""
from __future__ import annotations

import itertools
import re
import sys
from pathlib import Path

import yaml

import wikilib as W

_FRONT = re.compile(r"^---\n(.*?)\n---\n", re.S)
# related 鍵本身加上它的區塊清單項目（含縮排或不縮排的「- 」）
_RELATED = re.compile(r"^related:[^\n]*\n(?:[ \t]*- [^\n]*\n)*", re.M)


def card_path(cid: str) -> Path:
    return W.CARDS_DIR / f"{cid}.md"


def add_links(path: Path, new: list[str]) -> list[str]:
    """把 new 裡還沒有的 id 加進這張卡的 related，回傳實際加入的。"""
    text = path.read_text(encoding="utf-8")
    m = _FRONT.match(text)
    if not m:
        raise ValueError(f"{path.name}：缺少 YAML frontmatter")
    front_text = m.group(1) + "\n"
    current = (yaml.safe_load(front_text) or {}).get("related") or []
    added = [i for i in new if i not in current and i != path.stem]
    if not added:
        return []
    block = _RELATED.search(front_text)
    if not block:
        raise ValueError(f"{path.name}：frontmatter 沒有 related 鍵")
    item = re.search(r"^([ \t]*)- ", block.group(0), re.M)
    indent = item.group(1) if item else "  "
    lines = "".join(f"{indent}- {i}\n" for i in current + added)
    new_front = front_text[:block.start()] + "related:\n" + lines + front_text[block.end():]
    if (yaml.safe_load(new_front) or {}).get("related") != current + added:
        raise ValueError(f"{path.name}：改寫後 related 解析不符，未寫入")
    path.write_text("---\n" + new_front + text[m.end(1) + 1:], encoding="utf-8")
    return added


def main(argv: list[str]) -> int:
    mesh = "--mesh" in argv
    ids = [a for a in argv if a != "--mesh"]
    if len(ids) < 2:
        print(__doc__)
        return 2
    missing = [i for i in ids if not card_path(i).exists()]
    if missing:
        print("找不到卡：" + ", ".join(missing))
        return 1
    pairs = list(itertools.combinations(ids, 2)) if mesh else [(ids[0], i) for i in ids[1:]]
    links: dict[str, list[str]] = {}
    for a, b in pairs:
        links.setdefault(a, []).append(b)
        links.setdefault(b, []).append(a)
    for cid, new in links.items():
        added = add_links(card_path(cid), new)
        print(f"{cid}: " + (("+ " + ", ".join(added)) if added else "（已存在，未改）"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
