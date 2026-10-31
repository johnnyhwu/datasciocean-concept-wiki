# 去重、關係、放行

## 1. 去重與關係

寫卡後、放行前，比對 `wiki/index.md`，對每張新卡提議關係：

| 關係 | 做法 |
|---|---|
| 重複 | 不新建卡，把新來源追加到既有卡的 `sources` |
| 實例 | 新建卡並設 `parent`（由下往上長：同類累積兩三個實例後才建上層觀念） |
| 相關 | 設 `related`（無方向、雙向各寫一邊） |
| 全新 | 新建卡，不設關係 |

**提議由人確認後才寫入**，判斷錯誤會汙染整個 wiki。同一篇文章提煉出的卡之間：互設 `related`、不設 `parent`；有概覽或核心卡時，以它為中心與其餘各卡互設，其餘卡之間視關聯加設。

`related` 用 `add_related.py` 寫，不手改：`add_related.py --mesh <id>...`（同篇兩兩互設）、`add_related.py <hub> <id>...`（hub 與各卡互設）。

## 2. 放行與寫入

- 三關審查都通過、且 `SKILL.md`「必須停下來問人的情況」沒有任何一項待處理，就**直接寫入 wiki，不等人放行**。
- 有待處理項目：先整理成一份簡短清單問人，人回覆後再寫入（重建 index、更新 `docs/status.md`）。blog 內部矛盾不必等回覆：照 `card-writing.md` §10 先處理，列在清單裡供人推翻。
- 寫入前最後跑一次 `validate_card.py`（全部卡，不指定檔案：連同 `wiki/figures/` 的孤兒圖一起查）與 `build_index.py`。
- 人確認的通用知識詞，若是一般性詞彙，加進 `config/background-terms.md`；MTok、rubric 這類在卡上只是引文單位或名稱標籤的，不加。

下游要等人 commit 並 push 後才看得到新卡。

## 3. 完成報告（給人看）

人只看**卡本身**加一份簡短報告，不需要看審查過程：

- 新增了哪些卡（id、一句話論點、主張數）、關聯到哪些既有卡；
- 三關審查的結果摘要（對證者與讀者各幾輪、blocker 有哪些已修、全文審查結果）；
- pending 與 author_confirmed 清單（含 blog 矛盾的具體內容，供人決定要不要修 blog）；
- 通用知識詞與去重關係的處理結果；
- 附圖清單（哪條主張附了哪張圖、為什麼有幫助），供人刪減；
- 審查的 token 用量（subagent 回報的 usage 加總，按對證者、讀者、全文審查分開）——成本是主要痛點，每次都量，累積到 `docs/stage1-token-usage.md`。表格欄位：類別、subagent 個數、token、占比；另列「沒採用結果的 subagent」與哪些地方花得不合理；全文審查抓到的「限定條件掉了」，記下它屬於 `limits.md` 的哪一類、為什麼漏掉（用來改進對照檔的類型清單）。

## 4. blog 改了之後

blog 更新（`git submodule update --remote` 後文章有變）時：
1. 對受影響的卡跑 `validate_card.py`，引文不再逐字出現的主張會被擋下。
2. blog 換了附圖的原圖：`validate_card.py` 會報「blog 的原圖已改變」。重跑 `copy_figure.py <article> <src>` 取得新圖與新 sha256，自己看過新圖，更新主張的 `figures`；指紋含 sha256，`claim_fingerprints.py diff` 會列出這些主張，交對證者重審。blog 刪掉或改名了那張圖，就移除主張的 `figures` 和 `wiki/figures/` 裡的檔案（孤兒圖會被擋下）。
3. 引文仍在、但上下文可能變了的主張，用 `make_auditor_copy.py` 重新產生副本，派對證者重審，必要時再跑全文審查。
4. 改動後的卡照常過讀者與全文審查（只在主張內容變動時）。
