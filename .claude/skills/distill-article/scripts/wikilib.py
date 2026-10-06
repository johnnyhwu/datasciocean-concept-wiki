"""共用函式：專案路徑、參數、卡片解析、blog 正規化與逐字比對。

契約文件：docs/card-format.md；流程：.claude/skills/distill-article/。
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import yaml


def project_root() -> Path:
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / "CLAUDE.md").exists() and (parent / "config").exists():
            return parent
    raise RuntimeError("找不到專案根目錄（需有 CLAUDE.md 與 config/）")


ROOT = project_root()


def load_params() -> dict:
    return yaml.safe_load((ROOT / "config" / "params.yaml").read_text(encoding="utf-8"))


# ---------------------------------------------------------------- blog 文章

def blog_path(slug: str, params: dict | None = None) -> Path:
    params = params or load_params()
    base = ROOT / params["blog"]["root"] / "content" / "posts"
    hits = sorted(base.glob(f"*/{slug}/{params['blog']['source_file']}"))
    if len(hits) != 1:
        raise FileNotFoundError(f"slug={slug!r} 找到 {len(hits)} 篇：{hits}")
    return hits[0]


def strip_front_matter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


_QUOTE_MARKS = "“”\"'‘’「」『』"
_SHORTCODE = re.compile(r"\{\{[<%].*?[>%]\}\}")


def normalize(text: str) -> str:
    """去 markdown 標記、統一全半形標點與空白（docs/card-format.md §8）。兩邊（blog 與引用）用同一個函式。"""
    t = unicodedata.normalize("NFKC", text)
    t = _SHORTCODE.sub("", t)
    lines = []
    for line in t.splitlines():
        s = line.strip()
        if re.fullmatch(r"\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?", s):
            continue  # 表格分隔列
        if s.startswith("|"):
            s = s.strip("|")  # 表格列去頭尾線
        s = re.sub(r"^(#{1,6}\s+|>\s*|[-*+]\s+|\d+\.\s+)", "", s)  # 標題、引用、清單記號
        lines.append(s)
    t = "\n".join(lines)
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)  # 連結只留文字
    t = t.replace("**", "").replace("__", "").replace("`", "")
    t = re.sub(r"(?<!\w)\*(?=\S)|(?<=\S)\*(?!\w)", "", t)  # 斜體星號
    for ch in _QUOTE_MARKS:
        t = t.replace(ch, "")
    t = re.sub(r"\s+", "", t)  # 統一空白：全部去除
    return t


@dataclass
class Section:
    title: str
    level: int
    body_norm: str  # 此小節自己的文字（不含子小節）正規化後的全文
    title_norm: str = ""


@dataclass
class Blog:
    slug: str
    path: Path
    full_norm: str
    title: str = ""
    body: str = ""  # 去掉 front matter 的原始 markdown
    sections: list[Section] = field(default_factory=list)


def load_blog(slug: str, params: dict | None = None) -> Blog:
    path = blog_path(slug, params)
    raw = path.read_text(encoding="utf-8")
    body = strip_front_matter(raw)
    fm = re.match(r"^---\n(.*?)\n---", raw, re.S)
    fm_title = str((yaml.safe_load(fm.group(1)) or {}).get("title", "")) if fm else ""
    lines = body.splitlines()
    heads = []  # (line_idx, level, title)
    in_code = False
    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{2,6})\s+(.*\S)\s*$", line)
        if m:
            heads.append((i, len(m.group(1)), m.group(2)))
    secs = []
    for idx, (i, level, title) in enumerate(heads):
        # 只算小節自己的文字（到下一個任何層級的標題為止），不含子小節，
        # 這樣 sources.sections 才能精確對應引用位置
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
        sec_text = "\n".join(lines[i + 1:end])
        secs.append(Section(title=title, level=level, body_norm=normalize(sec_text),
                            title_norm=normalize(title)))
    return Blog(slug=slug, path=path, full_norm=normalize(body), title=fm_title, body=body, sections=secs)


_ELLIPSIS = re.compile(r"…+|\.{3,}")


def quote_fragments(quote: str) -> list[str]:
    """引用中的「…」代表省略；每個片段都必須逐字出現且依序。"""
    return [f for f in (normalize(p) for p in _ELLIPSIS.split(quote)) if f]


def quote_in_text(quote: str, text_norm: str) -> bool:
    pos = 0
    frags = quote_fragments(quote)
    if not frags:
        return False
    for f in frags:
        k = text_norm.find(f, pos)
        if k == -1:
            return False
        pos = k + len(f)
    return True


def find_sections(blog: Blog, title: str) -> list[Section]:
    """同名小節可能有多個（blog 實際存在），全部回傳。"""
    tn = normalize(title)
    return [s for s in blog.sections if s.title_norm == tn]


_NUM = re.compile(r"\d+(?:[.,]\d+)*")


def numbers_in(text: str) -> list[str]:
    t = unicodedata.normalize("NFKC", text)
    return [n.replace(",", "") for n in _NUM.findall(t)]


# ---------------------------------------------------------------- 卡片

@dataclass
class Card:
    path: Path
    front: dict
    claims: list[dict]
    errors: list[str] = field(default_factory=list)


_FENCE = re.compile(r"```ya?ml\s*\n(.*?)\n```", re.S)


def parse_card(path: Path) -> Card:
    """卡 = YAML frontmatter + 一個含 `claims:` 的 ```yaml 區塊（標題「## 主張」）。"""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return Card(path, {}, [], ["缺少 YAML frontmatter"])
    front = yaml.safe_load(m.group(1)) or {}
    claims: list[dict] = []
    errors: list[str] = []
    found = False
    for fence in _FENCE.finditer(m.group(2)):
        data = yaml.safe_load(fence.group(1)) or {}
        if isinstance(data, dict) and "claims" in data:
            found = True
            claims = data.get("claims") or []
    if not found:
        errors.append("找不到含 claims 的 ```yaml 區塊")
    return Card(path, front, claims, errors)


def load_all_cards() -> list[Card]:
    return [parse_card(p) for p in sorted((ROOT / "wiki" / "concepts").glob("*.md"))]
