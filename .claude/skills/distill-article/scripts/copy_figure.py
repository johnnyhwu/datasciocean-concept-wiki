"""把 blog 文章裡的一張圖複製進 wiki/figures/<article>/，並印出可貼進主張 `figures` 欄位的 YAML。

用法：uv run python .claude/skills/distill-article/scripts/copy_figure.py <article-slug> <src> [--indent N]
      src 是 blog 內文 `{{< image src="…" >}}` 裡的檔名（例如 figure3.png）。
      --indent N：印出的 YAML 每行縮排 N 個空格。貼進卡裡的主張時，填主張 `text` 同層的縮排
      （主張寫成 `- id: c1` 的清單項目時，是 2；主張在 `claims:` 底下縮排 2 時，是 4），可以直接貼不必手動對齊。

- 圖只能來自 blog 內文用 image shortcode 引用的圖（featuredImage 不算）。
- 已存在且內容不同的檔案會被覆寫（blog 改了圖的情況），並提醒附這張圖的主張要重審。
- caption 與 sha256 由程式取得，不手抄；validate_card.py 會驗證兩者。
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import yaml

import wikilib as W


def main(slug: str, src: str, indent: int = 0) -> int:
    params = W.load_params()
    blog = W.load_blog(slug, params)
    images = W.blog_images(blog)
    img = next((i for i in images if i["src"] == src), None)
    if img is None:
        print(f"ERROR blog 內文沒有引用 {src!r}。這篇文章引用的圖：{[i['src'] for i in images]}")
        return 1
    if ".." in Path(src).parts:
        print(f"ERROR 不合法的 src：{src!r}")
        return 1
    ext = Path(src).suffix.lower()
    if ext not in set(params["wiki"]["figure_extensions"]):
        print(f"ERROR 副檔名 {ext!r} 不在 wiki.figure_extensions 內")
        return 1
    original = blog.path.parent / src
    if not original.is_file():
        print(f"ERROR blog 資料夾裡找不到 {original}")
        return 1
    size_kb = original.stat().st_size / 1024
    if size_kb > params["wiki"]["figure_max_kb"]:
        print(f"ERROR {src} 有 {size_kb:.0f} KB，超過 wiki.figure_max_kb={params['wiki']['figure_max_kb']}")
        return 1

    rel = f"figures/{slug}/{src}"
    dest = W.WIKI_DIR / rel
    digest = W.sha256_of(original)
    if dest.exists() and W.sha256_of(dest) != digest:
        print(f"WARN 覆寫既有檔案（內容不同）：{rel}。附這張圖的主張要重審。")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(original, dest)

    snippet = {"figures": [{"file": rel, "article": slug, "src": src, "caption": img["caption"], "sha256": digest}]}
    print(f"copied {rel}（{size_kb:.0f} KB）；圖在 blog 小節：{img['section'] or '（無標題）'}；alt：{img['alt']}")
    print("貼進主張（與 text 同層）：")
    pad = " " * indent
    dumped = yaml.safe_dump(snippet, allow_unicode=True, sort_keys=False, width=10_000).rstrip()
    print("\n".join(pad + line for line in dumped.splitlines()))
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    indent = 0
    if "--indent" in args:
        i = args.index("--indent")
        try:
            indent = int(args[i + 1])
        except (IndexError, ValueError):
            print(__doc__)
            sys.exit(2)
        del args[i:i + 2]
    if len(args) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(args[0], args[1], indent))
