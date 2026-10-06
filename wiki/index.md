# 觀念庫索引（程式產生，不手改）

| id | 一句話論點 | parent | related | status |
|---|---|---|---|---|
| cascade-complementary-errors | 這個串接設計能成立的前提，是兩個判官錯在不同的題：如果第一階段錯的題，強判官大多答對，轉出去就能補回來；但兩邊都錯的題，怎麼轉都修不回來 | - | jev-cascade-overview | active |
| cascade-threshold-and-failure-mode | 串接的門檻 τ 是第一階段判官、強判官、任務三者的函數，換任何一個都要用自己的標註資料重選；門檻選對時，好的串接設計失敗時是把成本推高，而不是把錯誤放行 | - | jev-cascade-overview | active |
| confidence-three-metrics | 評估一個會給信心的分類器，要分三件事看：準確度看判決對不對；AUROC 只看 q 的順序；Brier 與 NLL 看 q 的數字大小；而溫度縮放（一種校準）只動數字這一件，二選一時不動排序與判決 | - | jev-cascade-overview | active |
| jev-cascade-overview | 用 JEV 的最大標籤機率 q 當信心，沿著「有把握就採用、沒把握就轉給 GPT-6」分流，在答案能從文字讀出的任務上又準又省，在難任務與新任務上，門檻選對時準確度不掉、但省得有限 | - | confidence-three-metrics, cascade-complementary-errors, judge-readable-vs-derive, cascade-threshold-and-failure-mode | active |
| judge-readable-vs-derive | 判官的工作是比對，不是從頭解題：答案能直接從文字讀出，小模型就夠；需要自己重新推導才知道對錯，小模型就不及；而且判官沒有證據可核對時，仍然會給一個很有把握的答案 | - | jev-cascade-overview | active |
