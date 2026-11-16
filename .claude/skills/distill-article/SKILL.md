---
name: distill-article
description: 把 DataSci Ocean 的一篇 blog 文章提煉成觀念卡（Stage 1）並寫進 wiki/。使用者要「處理一篇文章」「提煉觀念」「建觀念卡」「審卡」「blog 改了要重審」時使用。涵蓋挖候選、篩選與合併、寫卡（含主張附圖）、程式檢查、對證者與讀者審查迴圈、全文審查、去重與放行。不處理 IG 或 Threads 貼文（那是另一個 repo：datasciocean-social-media）。
---

# distill-article：blog 文章 → 觀念卡

輸入一篇 blog 文章（`blog/` submodule 裡的 markdown），輸出 `wiki/concepts/` 裡一到數張觀念卡。一篇通常 4～5 張，這是量級不是目標。

## 開始前（每次都做）

1. 先做 CLAUDE.md「每次開始前」的兩件事（更新 blog submodule、環境）。腳本一律 `uv run python .claude/skills/distill-article/scripts/<name>.py`。
2. 讀 `docs/card-format.md`（契約）、`wiki/index.md`（看已有哪些觀念）、`config/background-terms.md`、`config/params.yaml`。
3. 用 `blog/content/posts/*/<slug>/index.zh-tw.md` 找文章；文章的小節標題文字就是 `sources.sections` 要填的值。

## 流程

```
[1] 讀文章 → [2] 挖候選 → [3] 篩選與合併 → [3.5] 提案定案（記進報告，不等人）
 → [4] 建限定條件對照檔 → 寫卡 → 自檢 → [5] 程式檢查（加 --claim-count）
 → [6] 對證者迴圈 → [7] 讀者迴圈 → [8] 全文審查 → [9] 去重與關係 → [10] 寫入 wiki、報告
```

**卡檔案放哪**：寫卡時就放在 `wiki/concepts/<id>.md`（不 commit；`validate_card.py` 要在這裡檢查 `related`）。「寫入 wiki」指全部通過後重建 `wiki/index.md` 並更新 `docs/status.md`，不是移動檔案。

**依序審查、不同時改**：對證者通過才給讀者，讀者通過才做全文審查；任何一關改了主張，改動的主張回到對證者補審（`references/review-loop.md`）。**併卡一律在審查開始前完成**，審查開始後不再併卡。

| 步驟 | 做什麼 | 細節在 |
|---|---|---|
| 2–3.5 | 依優先順序挖候選；五個篩選測試；合併規則 R1–R6；**提案定案**（id、一句話論點、主要錨點、合併或淘汰理由、圖與表的範圍檢查），記進完成報告，直接寫卡。提案階段不看主張數 | `references/mining-and-filtering.md` |
| 4 | 先在 scratchpad 建 `review/limits.md`（整篇 blog 的打折、例外、反駁、概括數字），再寫卡；寫完逐列對照檔並自檢；主張用得到的 blog 圖就附上（`copy_figure.py`） | `references/card-writing.md`（對照檔與自檢見 §11，附圖見 §12） |
| 5 | `validate_card.py <card.md> --claim-count`：結構、引文逐字、附圖、主張數 10 到 20，直到 PASS | `docs/card-format.md` §8 |
| 6 | 對證者：只看「卡加引用與所在段落」，附圖的主張另外看圖核對 | `references/review-loop.md`、`references/auditor-prompt.md` |
| 7 | 獨立讀者：只看移除引用與附圖的卡 | `references/review-loop.md`、`references/reader-prompt.md` |
| 8 | 全文審查：整篇 blog 讀一次，審這篇的所有卡 | `references/final-audit-prompt.md` |
| 9–10 | 去重、關係（`add_related.py`）、寫入、報告 | `references/release.md` |

派發審查者的訊息範本、暫存路徑、固定成本與合併補審：`references/dispatch-templates.md`。

## 誰做決定（2026-11-15 起）

人挑好文章之後，撰寫者**一路做到寫入 wiki**，中間的判斷自己做，不停下來問；只有下面「嚴重的問題」才停。自己做的每個決定都寫進完成報告（`references/release.md` §3），讓人事後推翻。

**撰寫者自己決定，照預設做法處理，事後報告：**

| 事項 | 預設做法 |
|---|---|
| 提案（哪些觀念要寫、合併或淘汰） | 照 `mining-and-filtering.md` 的規則定案就寫卡，提案清單放進完成報告 |
| 去重與關係 | 照 `release.md` §1 判斷；同篇互設 `related`，與既有卡只設 `related` |
| blog 內部矛盾（含圖與文字對不上） | 照 `card-writing.md` §10：真矛盾標 `pending_author_confirmation`，措辭瑕疵用限定條件 resolve |
| 新增或變動的 `pending_author_confirmation` | 照上一列標，報告列出 |
| 非基本的通用知識詞 | 不用自己的知識補（CLAUDE.md 規則 1 不變）：改寫成不依賴它、取 blog 的說法，或不收那條主張；很基本的詞照 `card-writing.md` §7 補在「名詞補充」 |
| 審查者與撰寫者的爭議 | 撰寫者仍不能反駁審查者：照審查者的意見改，改不了就刪掉那條或標 pending，取保守的一邊 |
| 全文審查第 2 輪之後要不要跑第 3 輪、跨卡矛盾的處理 | 照 `review-loop.md` 關卡 3 的條件判斷 |

**嚴重的問題，停下來問人：**

- 輪數用完仍有 blocker（不降低標準、不自動放行）。
- 主軸（thesis）本身要標 pending，或 blog 的問題大到整張卡撐不住。
- 要改動其他文章的既有卡的主張（例如判為「重複」、要合併進既有卡）；只加 `related` 不算。
- 任何 `author_confirmed`（只有作者能確認）。
- 要改契約（`docs/card-format.md`）、`config/background-terms.md` 或流程腳本才走得下去。
- 撰寫者判斷某件事風險高、做錯會汙染 wiki，而上面的預設做法不適用。

## 腳本（`scripts/`）

| 腳本 | 用途 |
|---|---|
| `validate_card.py` | 結構驗證加引文逐字比對、附圖檢查（不指定檔案時驗全部卡並查孤兒圖）；`--claim-count` 另查主張數 |
| `copy_figure.py` | 把 blog 的一張圖複製進 `wiki/figures/<article>/`，印出可貼進主張 `figures` 的 YAML（`--indent N` 對齊縮排） |
| `make_auditor_copy.py` | 產生對證者版卡（`--only` 只審改動的主張） |
| `verify_audit.py` | 驗證對證者 JSON：引用逐字、分級、附圖的 figure_checks |
| `claim_fingerprints.py` | 主張指紋：`save` 存已通過的、`diff` 列出新增或改過的 |
| `make_reader_copy.py` | 產生讀者版卡（移除引用、參考文獻與附圖，保留「名詞補充」） |
| `verify_reader.py` | 驗證讀者 JSON |
| `verify_final_audit.py` | 驗證全文審查 JSON |
| `add_related.py` | 雙向寫入 `related`（`--mesh` 兩兩互設） |
| `build_index.py` | 產生 `wiki/index.md`（不手改） |
| `wikilib.py` | 共用：卡解析、blog 載入、正規化、逐字比對 |

改了任何腳本或審查流程，跑 `uv run python tests/test_stage1_programs.py`（見 `references/regression-tests.md`）。
