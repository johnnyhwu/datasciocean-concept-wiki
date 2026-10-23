# 目前狀態

每次實跑後更新這份；CLAUDE.md 只放連結，不放會過期的數字。token 用量另記在 `stage1-token-usage.md`。

## 觀念庫

- 共 24 張卡，尚未 commit：
  - `jev-as-a-judge`（2026-10-06，第二次實跑）：5 張。
  - `skillopt`（2026-10-10，第三次實跑）：5 張（`skillopt-overview`、`skillopt-batch-evidence-minibatch`、`skillopt-bounded-edit-budget`、`skillopt-blind-acceptance-gate`、`skillopt-epoch-level-control`），2 條 pending（概覽卡 c9、編輯預算卡 c4）。
  - `persona-aware-d2s`（2026-10-12，第四次實跑）：5 張（`persona-d2s-task-and-pipeline`、`persona-d2s-training-design-flaws`、`persona-d2s-what-to-borrow`、`decision-transformer-reward-conditioning`、`bradley-terry-pairwise-preference`），5 條 pending（Bradley-Terry 卡 c11：blog 算 2.53，重算為 2.58；what-to-borrow 卡 c3、c10：blog 稱「高 recall」但 recall 只有 78.89%；what-to-borrow 卡 c16 與 training-design-flaws 卡 c15：blog 對摘要重排證據「紮實」與「統計效力偏低」前後不一）。Decision Transformer 與 Bradley-Terry 是 `standalone_classic`。
  - `claude-code`（2026-10-12，第五次實跑；ai-concept 概念解說型文章，無實驗數字）：3 張（`claude-code-agentic-loop-and-tools` 18 條、`claude-code-extension-and-context` 20 條、`claude-code-permission-blast-radius` 15 條），5 條 pending（loop 卡 c12、c15、c16：blog 稱「精簡的通用工具」又要「優先專用、窄用途工具」；權限卡 c9、c13：「完全自主執行」模式 vs「任何模式下」危險動作預設要確認）。擴充卡 c16（CLAUDE.md 稱「專案層級」又說「Org-level」）與權限卡 c12（讀檔「幾乎所有模式」自動核准 vs「每個非瑣碎動作都先詢問」）經人檢視後改回 normal（2026-10-12）。提案階段 5 張，人同意後併成 3 張。同篇三張卡互設 `related`。
  - `cerebras-rag`（2026-10-23，第六次實跑；論文導讀型，無實驗數字）：6 張（`rag-narrow-waist` 19 條、`slack-vector-failure-orthogonal-signals` 13 條、`slack-distillation-and-bursting` 14 條、`rrf-rank-fusion` 17 條、`rag-planner-single-round-vs-agentic` 17 條、`retrieval-reasoning-decoupling` 17 條），0 條 pending。提案階段 8 張，人要求精簡後併成 6 張。審查者共列出 31 條 blog 措辭層級張力，依人 2026-10-23 的新指示：措辭瑕疵由撰寫者用限定條件 resolve（`rag-narrow-waist` c6 綁 Projects 對 source 做範圍過濾、`slack-distillation-and-bursting` c4 綁 bursting 另行 embed 且須過門檻、`retrieval-reasoning-decoupling` c1/c8 綁「作者自己推導」與 SQL 例外），其餘判為說法層級、讀 blog 說得通而改回 normal。已知但留在 normal 的張力（供人推翻）：窄腰「至少三次」對「四次」；「三種失效模式」對表格四列；「三道門檻」第三項是加分；RRF 缺席「不加分也不扣分」對「變成懲罰」；IDF 在 RRF 卡稱檢索器、在向量失效卡稱乘數；decoupling「只在末端壓縮一次」對寫入端 distillation 的有損壓縮（兩者在不同階段）。同篇六張卡互設 `related`。
- 第一次實跑的 6 張卡（`jev-overview`）留在 `tests/fixtures/concepts/` 當測試資料，完整歷史在 git。

## 流程現況

- 對證者只看引文與段落 → 讀者看移除引用的卡 → 全文審查每篇一次。
- 2026-10-06 加入：寫卡前先給人看提案（提案階段不看主張數）→ 合併後檢查每張卡 10 到 20 條主張（`validate_card.py --claim-count`）→ 審查開始後不再併卡；補審合併成一個 subagent；只動限定條件不重跑讀者。
- 2026-10-10（第三次實跑後）：同一篇文章共用的脈絡連同限定條件複製到每張卡；圖說裡才有的比較對象或範圍在提案階段先標出；脈絡主張描述本文方法時標「設計參數」；來自 blog 措辭的跨卡矛盾交人決定後不再擋第 3 輪判斷。
- 2026-10-12（第四次實跑）：使用者核准「很基本的通用詞（temperature、top-K、top-p、recall 等）blog 沒解釋時，撰寫者可用一般知識補充，不必問」；補充放在卡 yaml 區塊外的「名詞補充（通用知識，非 blog 內容）」小節，不是主張；這次新詞不加進背景詞清單。
- 2026-10-12（第四次實跑後）：審查者列出的 blog 內部矛盾（含措辭層級）一律先標 pending；卡可有「名詞補充」小節（`make_reader_copy.py` 會附給讀者）；數字檢查略過名稱標籤、新增「計數」豁免；`verify_reader.py` 不再把有引用的完整作答誤判為漏看；論文導讀型文章的慣例切法寫進 `mining-and-filtering.md`；移除盲挖者與第一次實跑（舊流程）的成本估算。
- 2026-10-23（第六次實跑後）：審查者列出的 blog 矛盾分兩類——真矛盾（數字、事實對不上）標 pending；措辭瑕疵由撰寫者用 `qualifiers` resolve 並補審改動的主張（`card-writing.md` §10、`release.md`、`SKILL.md` 同步改）。起因是這次一律 pending 累積 31 條。
