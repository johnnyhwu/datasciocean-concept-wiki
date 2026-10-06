# 觀念庫索引（程式產生，不手改）

| id | 一句話論點 | parent | related | status |
|---|---|---|---|---|
| confound-three-questions | 任何效能對比數字出現之前，先問三個問題：分母怎麼選的、評測方法本身有沒有讓某一方吃虧、參考答案的選擇會不會系統性偏袒某一方 | - | jev-overview, efficiency-accuracy-error-cost, schema-valid-not-correct | active |
| decompose-narrow-and-shallow | 把判斷拆成小題丟給單次前向傳播的模型時，不能只拆到主題夠窄，還要拆到每個子問題本身夠淺，也就是不需要中間推理草稿就能直接判斷 | - | jev-overview | active |
| efficiency-accuracy-error-cost | 拿準確率換效率划不划算，完全取決於任務對「錯一次的代價」有多敏感；做輕量方案對重量級方案的選擇前，先問這裡錯一次的代價有多高 | - | jev-overview, confound-three-questions | active |
| honest-probability-training | RLHF 讓 token 機率變得過度自信，是因為優化目標本身就沒有把校準放進去；適當計分規則（proper scoring rule）則是反過來，讓誠實報告真實機率的期望分數最高 | - | jev-overview | active |
| jev-overview | Jev 想補的是傳統分類器與直接呼叫 LLM 之間的空隙：要 LLM 的彈性，又要分類器的速度、成本與型別安全，外加可信賴的機率 | - | schema-valid-not-correct, confound-three-questions, honest-probability-training, decompose-narrow-and-shallow, efficiency-accuracy-error-cost | active |
| schema-valid-not-correct | 「不會幻覺」只保證輸出格式合法，不保證答案正確 | - | jev-overview, confound-three-questions | active |
