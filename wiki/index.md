# 觀念庫索引（程式產生，不手改）

| id | 一句話論點 | parent | related | status |
|---|---|---|---|---|
| bradley-terry-pairwise-preference | Bradley-Terry model 的核心假設是每個項目都有一個看不見的「實力值」，而比較結果只是這個實力值的機率反映，不是絕對保證；它是 RLHF 領域最廣泛採用的偏好模型 | - | persona-d2s-training-design-flaws, decision-transformer-reward-conditioning | active |
| cascade-complementary-errors | 這個串接設計能成立的前提，是兩個判官錯在不同的題：如果第一階段錯的題，強判官大多答對，轉出去就能補回來；但兩邊都錯的題，怎麼轉都修不回來 | - | jev-cascade-overview | active |
| cascade-threshold-and-failure-mode | 串接的門檻 τ 是第一階段判官、強判官、任務三者的函數，換任何一個都要用自己的標註資料重選；門檻選對時，好的串接設計失敗時是把成本推高，而不是把錯誤放行 | - | jev-cascade-overview | active |
| claude-code-agentic-loop-and-tools | Claude Code 以 CLI(以及 SDK)行程的形式運作，其核心其實只有一個原語：一個能呼叫工具、觀察結果、並決定下一步該做什麼的 LLM——如此反覆，直到它自己判斷任務已經完成 | - | claude-code-extension-and-context, claude-code-permission-blast-radius | active |
| claude-code-extension-and-context | Claude Code 的摘要、範圍化委派、專案設定檔這三個機制單獨拿出來看都不算新穎，真正讓它們成為「Harness」而非單純「功能」的，是它們能自動彼此組合；結語也說，包含 Skills、Hooks、MCP 在內的這些機制單獨拿出來看都不算特殊技術，真正讓它能運作的，是它們被設計成可以彼此組合 | - | claude-code-agentic-loop-and-tools, claude-code-permission-blast-radius | active |
| claude-code-permission-blast-radius | 一個能無人看管地執行任意 shell 指令、修改檔案的 Agent，需要一層不能單純仰賴模型「每次都猜對」的安全機制；目標不是讓 Agent 完全不可能犯錯，而是讓犯錯的代價變得低廉且可逆，使迴圈得以持續運作，而不需要人類在每一次失誤時都出手介入 | - | claude-code-agentic-loop-and-tools, claude-code-extension-and-context | active |
| confidence-three-metrics | 評估一個會給信心的分類器，要分三件事看：準確度看判決對不對；AUROC 只看 q 的順序；Brier 與 NLL 看 q 的數字大小；而溫度縮放（一種校準）只動數字這一件，二選一時不動排序與判決 | - | jev-cascade-overview | active |
| decision-transformer-reward-conditioning | Decision Transformer 的提案是把強化學習（RL）問題重新包裝成序列預測問題，用 GPT 式的監督學習訓練，完全不估計價值函數、不做 bootstrapping；訓練時是「觀察別人怎麼走、最後拿多少分，學會兩者的關聯」，使用時是「你先設定想要的分數，模型回推該怎麼走」 | - | persona-d2s-training-design-flaws, bradley-terry-pairwise-preference | active |
| jev-cascade-overview | 用 JEV 的最大標籤機率 q 當信心，沿著「有把握就採用、沒把握就轉給 GPT-6」分流，在答案能從文字讀出的任務上又準又省，在難任務與新任務上，門檻選對時準確度不掉、但省得有限 | - | confidence-three-metrics, cascade-complementary-errors, judge-readable-vs-derive, cascade-threshold-and-failure-mode | active |
| judge-readable-vs-derive | 判官的工作是比對，不是從頭解題：答案能直接從文字讀出，小模型就夠；需要自己重新推導才知道對錯，小模型就不及；而且判官沒有證據可核對時，仍然會給一個很有把握的答案 | - | jev-cascade-overview | active |
| persona-d2s-task-and-pipeline | Persona-Aware-D2S 把受眾（專家／非專家）和長度（長版／短版）變成模型的輸入條件，讓同一份文件長出四種投影片內容；它的貢獻主要在這個任務定義與對應的平行資料集，方法本身是現成技術的拼裝 | - | persona-d2s-training-design-flaws, persona-d2s-what-to-borrow | active |
| persona-d2s-training-design-flaws | Persona-Aware-D2S 的訓練設計有站不住腳的地方：訓練資料規模很小、reward model 沒做容量消融、四種 persona 各訓一個模型的架構無法隨 persona 維度擴展；偏好微調的關鍵細節也沒有交代，效果並非無條件的提升 | - | persona-d2s-task-and-pipeline, persona-d2s-what-to-borrow, decision-transformer-reward-conditioning, bradley-terry-pairwise-preference | active |
| persona-d2s-what-to-borrow | Persona-Aware-D2S 可以直接借鑑的是兩個不需要訓練的部分：Stage 2 第一步的兩段式檢索，以及 Stage 3 的摘要重排，遷移成本接近零；但章節過濾的篩選不可逆，摘要重排的證據樣本偏小、評分者也不是獨立第三方 | - | persona-d2s-task-and-pipeline, persona-d2s-training-design-flaws | active |
| rag-narrow-waist | 窄腰的價值不在於「統一」這件事本身好看，而在於腰以上和腰以下可以各自獨立演化，互不干擾 | - | rrf-rank-fusion, rag-planner-single-round-vs-agentic, retrieval-reasoning-decoupling | active |
| rag-planner-single-round-vs-agentic | Planner 負責路由，不負責思考夠不夠：LLM 被用來動態決定「這次該用哪些工具」，但整條處理線是決策一次、平行執行一次、synthesis 一次，沒有「證據不夠、回頭再查一輪」的迴圈，本質上是單輪 pipeline，不是 agentic loop | - | retrieval-reasoning-decoupling, rrf-rank-fusion, rag-narrow-waist | active |
| retrieval-reasoning-decoupling | 檢索與推理必須解耦：把推理徹底移出檢索路徑，只在管線末端的單次 synthesis 發生，才能同時解決「跨領域難共用」與「新資料類型要重複開發」這兩個問題 | - | rag-planner-single-round-vs-agentic, rag-narrow-waist | active |
| rrf-rank-fusion | RRF 最核心的巧思在於它只用「名次」不用「分數」：名次是所有檢索器都天然具備、而且天然可以互相比較的整數，這一招直接繞開了「分數尺度不可比」這個難題，不需要正規化，也就沒有正規化帶來的飄移問題 | - | slack-vector-failure-orthogonal-signals, rag-narrow-waist, rag-planner-single-round-vs-agentic | active |
| skillopt-batch-evidence-minibatch | 如果讓優化器只對單一失敗的執行軌跡做出反應，它往往會對造成那次失敗的特定雜訊過度擬合；SkillOpt 刻意用大批次（一批 40 個任務），提供足夠的統計份量去分辨「系統性的弱點」與「單一的偶發狀況」 | - | skillopt-overview, skillopt-bounded-edit-budget | active |
| skillopt-blind-acceptance-gate | SkillOpt 整套設計裡最重要的工程紀律是資料隔離：優化器只能看到訓練集 D_tr 的執行軌跡，候選技能必須在它完全看不到的 D_sel 上，平均分數嚴格大於目前技能才被接受，平手不算 | - | skillopt-overview, skillopt-bounded-edit-budget, skillopt-epoch-level-control | active |
| skillopt-bounded-edit-budget | 合併完成之後，提案的修改數量可能還是遠超過一次套用的安全上限；SkillOpt 用編輯預算 L_t 來限制單一步驟能套用多少修改，這是學習率在文字空間裡的直接對應。一次套用太多修改，就跟梯度下降時踩了太大的步伐一樣，技能文件可能因此陷入不穩定的狀態，並丟失先前辛苦累積下來的教訓 | - | skillopt-overview, skillopt-batch-evidence-minibatch, skillopt-blind-acceptance-gate | active |
| skillopt-epoch-level-control | 逐步的修改在設計上本來就是短視的，每一步都只針對最近這一批任務做出反應；為了抓住更長時程的退步，SkillOpt 加入第二層、比較慢的控制迴圈，每個 Epoch 才跑一次，而不是每個 Step 都跑 | - | skillopt-overview, skillopt-blind-acceptance-gate | active |
| skillopt-overview | blog 總結 SkillOpt 真正主張的，是一種思維上的轉變：提示詞/技能的迭代，不該是黑盒子式的試錯，而應該是一套真正的優化管線，擁有深度學習領域早已視為理所當然的紀律——用成批的證據取代單一的軼事、用有界的步伐取代不受約束的重寫、用真正盲測的驗證切分取代憑感覺判斷，再加上一個較長時程的機制，防止短期的補丁侵蝕掉先前學到的教訓 | - | skillopt-batch-evidence-minibatch, skillopt-bounded-edit-budget, skillopt-blind-acceptance-gate, skillopt-epoch-level-control | active |
| slack-distillation-and-bursting | 如果原始資料形式差異很大，該問的不是「要不要摘要」，而是「有沒有一個固定 schema，能把這些異質資料收斂成一致格式」 | - | slack-vector-failure-orthogonal-signals, rag-narrow-waist | active |
| slack-vector-failure-orthogonal-signals | Cerebras 沒有隨便疊加幾種常見訊號了事，而是先精確診斷每種失效的根因，再找一個訊號的數學性質剛好不受那個根因影響 | - | slack-distillation-and-bursting, rrf-rank-fusion | active |
