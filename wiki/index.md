# 觀念庫索引（程式產生，不手改）

| id | 一句話論點 | parent | related | status |
|---|---|---|---|---|
| cascade-complementary-errors | 這個串接設計能成立的前提，是兩個判官錯在不同的題：如果第一階段錯的題，強判官大多答對，轉出去就能補回來；但兩邊都錯的題，怎麼轉都修不回來 | - | jev-cascade-overview | active |
| cascade-threshold-and-failure-mode | 串接的門檻 τ 是第一階段判官、強判官、任務三者的函數，換任何一個都要用自己的標註資料重選；門檻選對時，好的串接設計失敗時是把成本推高，而不是把錯誤放行 | - | jev-cascade-overview | active |
| confidence-three-metrics | 評估一個會給信心的分類器，要分三件事看：準確度看判決對不對；AUROC 只看 q 的順序；Brier 與 NLL 看 q 的數字大小；而溫度縮放（一種校準）只動數字這一件，二選一時不動排序與判決 | - | jev-cascade-overview | active |
| jev-cascade-overview | 用 JEV 的最大標籤機率 q 當信心，沿著「有把握就採用、沒把握就轉給 GPT-6」分流，在答案能從文字讀出的任務上又準又省，在難任務與新任務上，門檻選對時準確度不掉、但省得有限 | - | confidence-three-metrics, cascade-complementary-errors, judge-readable-vs-derive, cascade-threshold-and-failure-mode | active |
| judge-readable-vs-derive | 判官的工作是比對，不是從頭解題：答案能直接從文字讀出，小模型就夠；需要自己重新推導才知道對錯，小模型就不及；而且判官沒有證據可核對時，仍然會給一個很有把握的答案 | - | jev-cascade-overview | active |
| skillopt-batch-evidence-minibatch | 如果讓優化器只對單一失敗的執行軌跡做出反應，它往往會對造成那次失敗的特定雜訊過度擬合；SkillOpt 刻意用大批次（一批 40 個任務），提供足夠的統計份量去分辨「系統性的弱點」與「單一的偶發狀況」 | - | skillopt-overview, skillopt-bounded-edit-budget | active |
| skillopt-blind-acceptance-gate | SkillOpt 整套設計裡最重要的工程紀律是資料隔離：優化器只能看到訓練集 D_tr 的執行軌跡，候選技能必須在它完全看不到的 D_sel 上，平均分數嚴格大於目前技能才被接受，平手不算 | - | skillopt-overview, skillopt-bounded-edit-budget, skillopt-epoch-level-control | active |
| skillopt-bounded-edit-budget | 合併完成之後，提案的修改數量可能還是遠超過一次套用的安全上限；SkillOpt 用編輯預算 L_t 來限制單一步驟能套用多少修改，這是學習率在文字空間裡的直接對應。一次套用太多修改，就跟梯度下降時踩了太大的步伐一樣，技能文件可能因此陷入不穩定的狀態，並丟失先前辛苦累積下來的教訓 | - | skillopt-overview, skillopt-batch-evidence-minibatch, skillopt-blind-acceptance-gate | active |
| skillopt-epoch-level-control | 逐步的修改在設計上本來就是短視的，每一步都只針對最近這一批任務做出反應；為了抓住更長時程的退步，SkillOpt 加入第二層、比較慢的控制迴圈，每個 Epoch 才跑一次，而不是每個 Step 都跑 | - | skillopt-overview, skillopt-blind-acceptance-gate | active |
| skillopt-overview | blog 總結 SkillOpt 真正主張的，是一種思維上的轉變：提示詞/技能的迭代，不該是黑盒子式的試錯，而應該是一套真正的優化管線，擁有深度學習領域早已視為理所當然的紀律——用成批的證據取代單一的軼事、用有界的步伐取代不受約束的重寫、用真正盲測的驗證切分取代憑感覺判斷，再加上一個較長時程的機制，防止短期的補丁侵蝕掉先前學到的教訓 | - | skillopt-batch-evidence-minibatch, skillopt-bounded-edit-budget, skillopt-blind-acceptance-gate, skillopt-epoch-level-control | active |
