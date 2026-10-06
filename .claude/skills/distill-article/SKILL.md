---
name: distill-article
description: 把 DataSci Ocean 的一篇 blog 文章提煉成觀念卡（Stage 1）並寫進 wiki/。使用者要「處理一篇文章」「提煉觀念」「建觀念卡」「審卡」「blog 改了要重審」時使用。涵蓋挖候選、篩選與合併、寫卡、程式檢查、對證者與讀者審查迴圈、全文審查、去重與放行。不處理 IG 或 Threads 貼文（那是另一個 repo：datasciocean-social-media）。
---

# distill-article：blog 文章 → 觀念卡

輸入一篇 blog 文章（`blog/` submodule 裡的 markdown），輸出 `wiki/concepts/` 裡一到數張觀念卡。一篇通常 5～6 張，這是量級不是目標。卡的格式契約在 `docs/card-format.md`，開始前先讀它。

## 開始前（每次都做）

1. `git submodule update --remote`（blog 要是最新的）。
2. `uv sync`（環境全在 repo 內：`.venv/`、`.uv-cache/`；缺才跑）。腳本一律 `uv run python .claude/skills/distill-article/scripts/<name>.py`。
3. 讀 `docs/card-format.md`、`wiki/index.md`（看已有哪些觀念）、`config/background-terms.md`、`config/params.yaml`。
4. 用 `blog/content/posts/*/<slug>/index.zh-tw.md` 找文章；文章的小節標題文字就是 `sources.sections` 要填的值。

## 流程

```
[1] 讀文章 → [2] 挖候選 → [3] 篩選與合併 → [3.5] 給人看提案（人刪、併、改）→ [4] 寫卡
 → [5] 程式檢查（合併後加 --claim-count）→ [6] 對證者迴圈（最多 5 輪）→ [7] 讀者迴圈（最多 5 輪）
 → [8] 全文審查（每篇一次）→ [9] 去重與關係 → [10] 放行、寫入 wiki、更新 index
```

審查**依序**進行，不同時改：對證者先把卡的每條主張對到原文，通過後才給讀者，讀者通過後才做全文審查。任何一關讓卡的主張變動，後面的關要重來（只重審改動的主張，見 `references/review-loop.md`）。

**併卡一律在審查開始前完成。** 提案確認、卡寫完、主張數檢查通過之後才進 [6]；審查開始後不再併卡（審完才併，審查就白做了）。

| 步驟 | 做什麼 | 細節在 |
|---|---|---|
| 2–3 | 依優先順序挖候選；五個篩選測試；合併規則 R1–R5 | `references/mining-and-filtering.md` |
| 3.5 | **給人看提案**（id、一句話論點、主要錨點、合併或淘汰理由），等人回覆才寫卡。**提案階段不看主張數**，避免為湊數而偏頗 | `references/mining-and-filtering.md` |
| 4 | 寫卡：主張盡量用 blog 的字、引文涵蓋每個成分、比較對象、限定條件（寫卡前先做自檢清單）、脈絡主張 | `references/card-writing.md` |
| 5 | `validate_card.py <card.md>`：結構與引文逐字比對，直到 PASS。合併完成後再加 `--claim-count`，每張卡主張數須在 10 到 20 | `docs/card-format.md` §8 |
| 6 | 對證者：只看「卡加引用與參考文獻」，不讀整篇 blog | `references/review-loop.md`、`references/auditor-prompt.md` |
| 7 | 獨立讀者：只看移除引用的卡 | `references/review-loop.md`、`references/reader-prompt.md` |
| 8 | 全文審查：整篇 blog 讀一次，審這篇的所有卡 | `references/final-audit-prompt.md` |
| 9–10 | 去重、關係、放行、報告 | `references/release.md` |

## 必須停下來問人的情況

不確定就問，不自己決定。至少包括：

- **寫卡前的提案清單**（哪些觀念要寫、哪些合併或淘汰），人確認後才寫卡。
- 去重與關係提議（重複、實例、相關、全新）。
- blog 內部矛盾怎麼處理（預設：不修 blog，卡用保守寫法，有矛盾的主張標 `pending_author_confirmation`）。
- 背景詞清單以外、blog 也沒解釋的「通用知識」詞。
- 審查者與撰寫者的爭議條目（撰寫者不能反駁審查者，只能標爭議）。
- 輪數用完仍有 blocker。
- 新增或變動的 `pending_author_confirmation` 主張；任何 `author_confirmed`。

以上都沒有、且三關都通過 → 直接寫入 wiki，不必等人放行（使用者 2026-10-04 核准）。完成後給人一份報告（`references/release.md` §3）。

## 腳本（`scripts/`）

| 腳本 | 用途 |
|---|---|
| `validate_card.py` | 結構驗證加引文逐字比對（可一次驗全部卡）；`--claim-count` 另查主張數（只在合併階段用） |
| `make_auditor_copy.py` | 產生對證者版卡：主張後標 [n]，卡尾參考文獻與引文所在段落（`--only` 只審改動的主張） |
| `verify_audit.py` | 驗證對證者 JSON：引用逐字、分級（blocker 與 minor）、pending 不擋 |
| `claim_fingerprints.py` | 主張指紋：`save` 存已通過的、`diff` 列出新增或改過的 |
| `make_reader_copy.py` | 產生讀者版卡（移除引用與參考文獻） |
| `verify_reader.py` | 驗證讀者 JSON：主軸三題都要有卡上引用；陷阱題可答「卡上沒寫」，其餘不行 |
| `verify_final_audit.py` | 驗證全文審查 JSON：斷章取義、限定條件掉了、跨卡矛盾、blog 矛盾 |
| `build_index.py` | 產生 `wiki/index.md`（程式產生，不手改） |
| `wikilib.py` | 共用：卡解析、blog 載入、正規化、逐字比對 |

改了任何腳本或審查流程，跑 `uv run python tests/test_stage1_programs.py`（見 `references/regression-tests.md`）。

## 派發 subagent 的做法

- 審查者提示詞放在 `references/`，派發訊息只給提示詞路徑與變數（檔案路徑），不要貼全文。審查者是獨立的：看不到撰寫者推理、看不到其他卡、看不到上一輪結果。
- 每輪都用**全新** subagent。
- 並行上限 20。一次派不完就分批；派完用檔案數核對「應到／實到」（我曾漏發而不自知）。
- **每個 subagent 約有 38k token 的固定成本**（讀提示詞與檔案），即使只審 1 條主張。補審時把同一輪、同一張卡（甚至多張卡）的改動併成**一個** subagent，依序審各份副本、各寫各的 JSON；不要一條主張派一個。
- 審查產出（JSON、卡副本、指紋檔）放暫存目錄（本次工作的 scratchpad），不放進 repo。
- 修改卡的人是撰寫者（你），審查者只指出問題、不給改寫版本。
