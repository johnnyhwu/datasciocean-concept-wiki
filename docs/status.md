# 目前狀態

每次實跑後更新這份；CLAUDE.md 只放連結，不放會過期的數字。token 用量另記在 `stage1-token-usage.md`。

## 觀念庫

- 共 29 張卡，尚未 commit：
  - `jev-as-a-judge`（2026-10-06，第二次實跑）：5 張。
  - `skillopt`（2026-10-10，第三次實跑）：5 張（`skillopt-overview`、`skillopt-batch-evidence-minibatch`、`skillopt-bounded-edit-budget`、`skillopt-blind-acceptance-gate`、`skillopt-epoch-level-control`），2 條 pending（概覽卡 c9、編輯預算卡 c4）。
  - `persona-aware-d2s`（2026-10-12，第四次實跑）：5 張（`persona-d2s-task-and-pipeline`、`persona-d2s-training-design-flaws`、`persona-d2s-what-to-borrow`、`decision-transformer-reward-conditioning`、`bradley-terry-pairwise-preference`），5 條 pending（Bradley-Terry 卡 c11：blog 算 2.53，重算為 2.58；what-to-borrow 卡 c3、c10：blog 稱「高 recall」但 recall 只有 78.89%；what-to-borrow 卡 c16 與 training-design-flaws 卡 c15：blog 對摘要重排證據「紮實」與「統計效力偏低」前後不一）。Decision Transformer 與 Bradley-Terry 是 `standalone_classic`。
  - `claude-code`（2026-10-12，第五次實跑；ai-concept 概念解說型文章，無實驗數字）：3 張（`claude-code-agentic-loop-and-tools` 18 條、`claude-code-extension-and-context` 20 條、`claude-code-permission-blast-radius` 15 條），5 條 pending（loop 卡 c12、c15、c16：blog 稱「精簡的通用工具」又要「優先專用、窄用途工具」；權限卡 c9、c13：「完全自主執行」模式 vs「任何模式下」危險動作預設要確認）。擴充卡 c16（CLAUDE.md 稱「專案層級」又說「Org-level」）與權限卡 c12（讀檔「幾乎所有模式」自動核准 vs「每個非瑣碎動作都先詢問」）經人檢視後改回 normal（2026-10-12）。提案階段 5 張，人同意後併成 3 張。同篇三張卡互設 `related`。
  - `cerebras-rag`（2026-10-23，第六次實跑；論文導讀型，無實驗數字）：6 張（`rag-narrow-waist` 19 條、`slack-vector-failure-orthogonal-signals` 13 條、`slack-distillation-and-bursting` 14 條、`rrf-rank-fusion` 17 條、`rag-planner-single-round-vs-agentic` 17 條、`retrieval-reasoning-decoupling` 17 條），0 條 pending。提案階段 8 張，人要求精簡後併成 6 張。審查者共列出 31 條 blog 措辭層級張力，依人 2026-10-23 的新指示：措辭瑕疵由撰寫者用限定條件 resolve（`rag-narrow-waist` c6 綁 Projects 對 source 做範圍過濾、`slack-distillation-and-bursting` c4 綁 bursting 另行 embed 且須過門檻、`retrieval-reasoning-decoupling` c1/c8 綁「作者自己推導」與 SQL 例外），其餘判為說法層級、讀 blog 說得通而改回 normal。已知但留在 normal 的張力（供人推翻）：窄腰「至少三次」對「四次」；「三種失效模式」對表格四列；「三道門檻」第三項是加分；RRF 缺席「不加分也不扣分」對「變成懲罰」；IDF 在 RRF 卡稱檢索器、在向量失效卡稱乘數；decoupling「只在末端壓縮一次」對寫入端 distillation 的有損壓縮（兩者在不同階段）。同篇六張卡互設 `related`。
  - `sag`（2026-10-23，第七次實跑；論文導讀型，第一次附圖）：5 張（`multihop-vector-vs-graphrag-pain-points` 13 條、`sag-latent-hyperedge-one-hop` 16 條、`sag-sql-vector-llm-division-and-funnel` 18 條、`sag-results-and-gain-source` 19 條、`sag-tradeoffs-price-paid` 17 條），0 條 pending。提案階段 7 張，人要求整併後成 5 張。附圖 6 張（`wiki/figures/sag/`）、11 筆主張附圖，對證者全部判「一致」。三組消融的資料集範圍（MuSiQue）只在圖說，已用「來源：圖說」的限定條件帶進卡（`sag-latent-hyperedge-one-hop` c14、c15；`sag-results-and-gain-source` c1、c12、c13、c14、c15、c17）。blog 前言「9 個指標拿 8 個第一」對不上表一，卡上沒寫這條（待人決定要不要通知作者）。以下 blog 前後說法的張力都已用限定條件 resolve，供人推翻：「跟 embedding 品質基本無關」對別名對齊、種子預算、剪枝都靠向量相似度（`sag-results-and-gain-source` c1、c17、c18）；「LLM 只用在線下與決選」對 Step 1 用 LLM 抽實體（`sag-sql-vector-llm-division-and-funnel` c3、c5、c6、c7）；PageRank 前說跳數多會衰減、後說到得了低頻節點（`sag-tradeoffs-price-paid` c7）；MuSiQue「有些問題」要跳 4 次對整個資料集寫成 4 跳（`sag-results-and-gain-source` c4、c6）；「每一步都能被 SQL 重現」對線上有向量粗篩（`sag-latent-hyperedge-one-hop` c16）；「完全沒有提升 Recall@1」對 35.7 → 36.2（`sag-latent-hyperedge-one-hop` c14，原文括號「等於沒動」一併帶進）。已知未收進卡：全文檢索引擎不在線上三步內。關係（`related`）已寫入並重建 `wiki/index.md`（2026-10-24）；另外 `retrieval-reasoning-decoupling` 加了一筆 `related`。
- 第一次實跑的 6 張卡（`jev-overview`）留在 `tests/fixtures/concepts/` 當測試資料，完整歷史在 git。

## 流程現況

流程本身見 `.claude/skills/distill-article/SKILL.md`。對證者只看引文與段落 → 讀者看移除引用的卡 → 全文審查每篇一次。下面只記各次實跑後的流程變更（細節已寫進 skill）：

- 2026-10-06：寫卡前先給人看提案（不看主張數）→ 合併後檢查每張卡 10 到 20 條主張 → 審查開始後不再併卡；補審合併成一個 subagent；只動限定條件不重跑讀者。
- 2026-10-10：同篇文章共用的脈絡連同限定條件複製到每張卡；圖說裡才有的比較對象或範圍在提案階段先標出。
- 2026-10-12：很基本的通用詞由撰寫者補在「名詞補充」小節，不必問；數字檢查略過名稱標籤並新增「計數」豁免；論文導讀型文章的慣例切法寫進 `mining-and-filtering.md`。
- 2026-10-23：blog 矛盾分兩類——真矛盾標 pending，措辭瑕疵由撰寫者用 `qualifiers` resolve（起因：一律 pending 累積 31 條）。
- 2026-10-23（附圖）：主張可附 blog 的圖作參考（`figures`，`wiki/figures/`）。圖不是證據；對證者看圖核對有沒有矛盾，要寫出圖上位置與讀到的內容；讀者看不到圖。契約變了，下游要依 `docs/guideline-for-downstream.md` 同步。
- 2026-10-24（契約調整，下游要同步）：錨點「部落格推論」的定義擴充為「blog 對原因或機制的解釋或推測，論文沒有實測驗證，不論有沒有明標」；限定條件可加 `source: figure_caption`，引文取自這條主張自己附圖的圖說，只限範圍（資料集、模型組、設定）；`verify_audit` 拿圖說判「完全支持」會擋下。兩項都寫進 `docs/guideline-for-downstream.md` §9。
- 2026-10-24（第一次附圖實跑後）：對證者讀圖 11 筆全判一致，成本差距小（見 `stage1-token-usage.md`）；人的抽查尚待。新增 `references/dispatch-templates.md`（四種審查者與合併補審的派發範本）；讀者提示詞改讀 `config/background-terms.md`、變數列補齊；寫卡自檢補三項（絕對詞逐條對例外、重複的比較對象與範圍每條都帶引文、標題不能當引文）；提案階段新增必做的「圖與表的範圍檢查」；`copy_figure.py` 加 `--indent`；名稱標籤略過「Step N」；刪除 skill 內散落的實跑歷史註記，並把論文導讀型文章的切法改成一般性指引（不再固定 3 張）。
