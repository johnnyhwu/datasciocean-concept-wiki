---
id: slack-vector-failure-orthogonal-signals
title: 純向量搜尋在對話資料上會失效：先診斷根因，再找不受該根因影響的訊號，且疊加的訊號失效模式必須正交
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
  - article: cerebras-rag
    article_title: "拆解 Cerebras 企業知識庫 RAG：窄腰設計、檢索推理解耦與 Pipeline 的邊界"
    url: https://datasciocean.com/paper-intro/cerebras-rag/
    sections:
      - 前言
      - 為什麼純向量搜尋接不住 Slack 對話
      - 三種失效模式
      - IDF 與 BM25 的關係
    first_appearance: true
parent: null
related:
  - slack-distillation-and-bursting
  - rrf-rank-fusion
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: "Cerebras 沒有隨便疊加幾種常見訊號了事，而是先精確診斷每種失效的根因，再找一個訊號的數學性質剛好不受那個根因影響"
    source_quotes:
      - "Cerebras 沒有隨便疊加幾種常見訊號了事，而是先精確診斷每種失效的根因，再找一個訊號的數學性質剛好不受那個根因影響"
    anchor_type: 部落格判斷
    importance: 1
    status: normal
  - id: c2
    role: context
    text: "Cerebras 內部知識庫系統「Cerebras Knowledge」每天處理超過 15,000 次查詢，資料橫跨 Slack、Wiki、程式碼倉庫、Jira，服務對象還包含自動化流程與 AI agent，不只是人類"
    source_quotes:
      - "Cerebras 在 2026 年 7 月發表了一篇部落格文章，介紹他們內部知識庫系統「Cerebras Knowledge」的架構——這系統每天處理超過 15,000 次查詢，資料橫跨 Slack、Wiki、程式碼倉庫、Jira，服務對象還包含自動化流程與 AI agent，不只是人類。"
    anchor_type: 官方宣稱
    numeric_kind: non_comparative
    numeric_reason: 計數
    importance: 2
    status: normal
  - id: c3
    role: context
    text: "純向量搜尋在 Slack 訊息這種資料上有很具體的失效模式，所以文章花了不少篇幅講 Slack 訊息怎麼被處理"
    source_quotes:
      - "文章花了不少篇幅講 Slack 訊息怎麼被處理，原因是純向量搜尋在這種資料上有三種很具體的失效模式。"
    anchor_type: 部落格判斷
    importance: 3
    status: normal
  - id: c4
    role: mechanism
    text: "embedding 的壓縮過程對「這段話有多少實際資訊」不敏感，只捕捉語意的方向，所以一句廢話跟一句乾貨，只要語意方向都跟查詢接近，分數可能非常相近，向量搜尋分不出「這句話語意相關」跟「這句話有料」的差別"
    source_quotes:
      - "embedding 的壓縮過程對「這段話有多少實際資訊」不敏感，只捕捉語意的方向。這代表一句廢話跟一句乾貨，只要語意方向都跟查詢接近，分數可能非常相近——向量搜尋分不出「這句話語意相關」跟「這句話有料」的差別。"
    anchor_type: 部落格判斷
    importance: 4
    status: normal
  - id: c5
    role: mechanism
    text: "短訊息在 cosine 相似度計算上會系統性佔便宜：短訊息的向量方向比較集中明確，而長訊息因為包含多個子主題，向量其實是好幾個語意方向的加權平均，方向被稀釋掉了"
    source_quotes:
      - "短訊息在 cosine 相似度計算上會系統性佔便宜。原因是短訊息的向量方向比較集中明確，而長訊息因為包含多個子主題，向量其實是好幾個語意方向的加權平均，方向被稀釋掉了。"
    anchor_type: 部落格判斷
    importance: 5
    status: normal
  - id: c6
    role: evaluation
    text: "短訊息佔便宜這件事，不是換一個 embedding 模型就能解決的問題，是這種表示法本身的特性"
    source_quotes:
      - "這不是換一個 embedding 模型就能解決的問題，是這種表示法本身的特性。"
    anchor_type: 部落格判斷
    importance: 6
    status: normal
  - id: c7
    role: mechanism
    text: "上下文依賴：單獨一句「that fixed it」脫離對話脈絡完全沒有意義，這也解釋了為什麼處理單位要選在整個討論串（thread）的層級，而不是單一則訊息"
    source_quotes:
      - "第三種是上下文依賴——單獨一句「that fixed it」脫離對話脈絡完全沒有意義，這也解釋了為什麼處理單位要選在整個討論串（thread）的層級，而不是單一則訊息。"
    anchor_type: 部落格判斷
    importance: 7
    status: normal
  - id: c8
    role: anchor
    text: "文章把失效模式對應到不受該根因影響的訊號：語意方向掩蓋內容價值，對應 IDF（詞彙稀有度），因為直接算詞彙稀有度、跟向量幾何無關；短訊息佔便宜，對應全文搜尋，因為是精確 token 匹配、不受長短影響；上下文依賴，對應處理單位選 thread，因為保留完整對話脈絡"
    source_quotes:
      - "語意方向掩蓋內容價值 | IDF（詞彙稀有度） | 直接算詞彙稀有度，跟向量幾何無關"
      - "短訊息佔便宜 | 全文搜尋 | 精確 token 匹配，不受長短影響"
      - "上下文依賴 | 處理單位選 thread | 保留完整對話脈絡"
    anchor_type: 部落格判斷
    importance: 8
    status: normal
  - id: c9
    role: anchor
    text: "表中另一列是「答案會過期」，對應的訊號是 age decay，因為它直接讀 timestamp、跟語意無關"
    source_quotes:
      - "答案會過期 | Age decay | 直接讀 timestamp，跟語意無關"
    anchor_type: 部落格判斷
    importance: 9
    status: normal
  - id: c10
    role: mechanism
    text: "兩種訊號要疊加才有意義，前提是它們的失效模式必須「正交」；如果兩種訊號對同一種輸入都會失效，疊加根本沒解決任何問題，只是把同一個弱點算兩次"
    source_quotes:
      - "兩種訊號要疊加才有意義，前提是它們的失效模式必須「正交」。如果兩種訊號對同一種輸入都會失效，疊加根本沒解決任何問題，只是把同一個弱點算兩次。"
    anchor_type: 部落格判斷
    importance: 10
    status: normal
  - id: c11
    role: anchor
    text: "IDF 本來就是 BM25 內部的一個組成零件，Cerebras 把這個零件單獨抽出來，另外當一個獨立訊號使用；文章裡的「full-text search」對應到 sparse retrieval（BM25）那一路，IDF 則是額外抽出來、跨所有路都能用的品質訊號"
    source_quotes:
      - "簡單說，IDF 本來就是 BM25 內部的一個組成零件，Cerebras 把這個零件單獨抽出來，另外當一個獨立訊號使用。文章裡講的「full-text search」對應到大家熟悉的 sparse retrieval（BM25）那一路；IDF 則是額外抽出來、跨所有路都能用的品質訊號。"
    anchor_type: 部落格考證
    importance: 11
    status: normal
  - id: c12
    role: anchor
    text: "BM25 是完整的 sparse 排序函數，輸出一份排名，用途是完整的 sparse retrieval 那一路；文章裡的 IDF 用法是單一加權訊號或品質閘門，輸出一個乘數用來調整其他訊號，用途是額外壓低「語意接近但全是廢話詞」的結果"
    source_quotes:
      - "角色 | 完整的 sparse 排序函數 | 單一加權訊號/品質閘門"
      - "輸出 | 一份排名 | 一個乘數，用來調整其他訊號"
      - "用途 | 完整的 sparse retrieval 那一路 | 額外壓低「語意接近但全是廢話詞」的結果"
    anchor_type: 部落格考證
    importance: 12
    status: normal
  - id: c13
    role: evaluation
    text: "即使系統已經在做 BM25 加向量的混合檢索，把 IDF 額外抽出來當獨立的過濾或加權訊號，專門壓低「語意上很接近查詢、但全是廢話詞」的結果，在處理對話型資料時特別好用；BM25 排名本身不會主動幫你濾掉那些在向量檢索裡浮上來的廢話，兩者不衝突，可以疊加使用"
    source_quotes:
      - "如果系統已經在做 BM25 加向量的混合檢索，IDF 其實已經隱含在 BM25 內部了，但把 IDF 額外再抽出來當一個獨立的過濾或加權訊號，拿來專門壓低「語意上很接近查詢、但全是廢話詞」的結果，在處理對話型資料時特別好用——像 Slack 這種充滿社交填充語的資料，BM25 排名本身不會主動幫你濾掉那些在向量檢索裡浮上來的廢話，但一個獨立的 IDF 閘門可以額外做這件事，兩者不衝突，可以疊加使用。"
    qualifiers:
      - text: 這是作者在處理對話型資料（像 Slack 這種充滿社交填充語的資料）時的實務心得
        source_quote: "在處理對話型資料時特別好用——像 Slack 這種充滿社交填充語的資料"
    anchor_type: 部落格判斷
    importance: 13
    status: normal
```
