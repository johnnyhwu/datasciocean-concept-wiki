# 去重、關係、放行

## 1. 去重與關係

寫卡後、放行前，比對 `wiki/index.md`，對每張新卡提議關係：

| 關係 | 做法 |
|---|---|
| 重複 | 不新建卡，把新來源追加到既有卡的 `sources` |
| 實例 | 新建卡並設 `parent`（由下往上長：同類累積兩三個實例後才建上層觀念） |
| 相關 | 設 `related`（無方向、雙向各寫一邊） |
| 全新 | 新建卡，不設關係 |

**提議由人確認後才寫入**，判斷錯誤會汙染整個 wiki。同一篇文章提煉出的卡之間，第一次實跑採用：概覽卡與其餘各卡互設 `related`，不設 `parent`。

## 2. 放行與寫入

- 三關審查都通過、且沒有下列任何一項待人處理，就**直接寫入 wiki，不等人放行**（使用者 2026-10-04 核准）：
  - 去重或關係提議、
  - 通用知識詞（背景詞清單以外、blog 也沒解釋）、
  - 爭議條目、
  - 輪數用完仍有 blocker、
  - 新增或變動的 `pending_author_confirmation`、任何 `author_confirmed`、
  - 全文審查的「交人裁決」項目（跨卡矛盾、blog 內部矛盾）。
- 有上列任何一項：先把這些項目整理成一份簡短清單問人，人回覆後再寫入。
- 寫入前最後跑一次 `validate_card.py`（全部卡）與 `build_index.py`。
- 人確認的通用知識詞，若是一般性詞彙，加進 `config/background-terms.md`；MTok、rubric 這類在卡上只是引文單位或名稱標籤的，不加。

寫入後，Stage 2 在另一個 repo（`datasciocean-social-media`）更新 submodule 才看得到新卡；本 repo 不知道、也不該知道 Stage 2 的狀態。要讓下游看到，需要在本 repo commit 並 push（commit 與 push 由人決定時機）。

## 3. 完成報告（給人看）

人只看**卡本身**加一份簡短報告，不需要看審查過程：

- 新增了哪些卡（id、一句話論點、主張數）、關聯到哪些既有卡；
- 三關審查的結果摘要（對證者與讀者各幾輪、blocker 有哪些已修、全文審查結果）；
- pending 與 author_confirmed 清單（含 blog 矛盾的具體內容，供人決定要不要修 blog）；
- 通用知識詞與去重關係的處理結果；
- 審查的 token 用量（subagent 回報的 usage 加總，按對證者、讀者、全文審查分開）——第一次實跑後成本是主要痛點，每次都量，累積到 `docs/stage1-token-usage.md`。表格欄位：類別、subagent 個數、token、占比；另列「沒採用結果的 subagent」（重複派發、被併掉的卡的審查等）與哪些地方花得不合理。

## 4. blog 改了之後

blog 更新（`git submodule update --remote` 後文章有變）時：
1. 對受影響的卡跑 `validate_card.py`，引文不再逐字出現的主張會被擋下。
2. 引文仍在、但上下文可能變了的主張，用 `make_auditor_copy.py` 重新產生副本，派對證者重審，必要時再跑全文審查。
3. 改動後的卡照常過讀者與全文審查（只在主張內容變動時）。
