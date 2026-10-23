---
id: slack-distillation-and-bursting
title: embed 之前先把異質原始資料正規化成固定 schema，並在寫入時撈回有價值的旁枝訊息、擋掉低價值的
type_hint: 方法
context_type: evidence_from_single_source
sources:
  - article: cerebras-rag
    article_title: "拆解 Cerebras 企業知識庫 RAG：窄腰設計、檢索推理解耦與 Pipeline 的邊界"
    url: https://datasciocean.com/paper-intro/cerebras-rag/
    sections:
      - 前言
      - Distillation：先正規化再 Embed
      - Bursting：把離群但有價值的旁枝訊息撈回來
    first_appearance: true
parent: null
related:
  - slack-vector-failure-orthogonal-signals
  - rag-narrow-waist
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: "如果原始資料形式差異很大，該問的不是「要不要摘要」，而是「有沒有一個固定 schema，能把這些異質資料收斂成一致格式」"
    source_quotes:
      - "如果原始資料形式差異很大，該問的不是「要不要摘要」，而是「有沒有一個固定 schema，能把這些異質資料收斂成一致格式」。"
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
    text: "Distillation 是在真正把文字丟進向量模型之前的處理：不直接 embed 原始的討論串文字，而是先讓 LLM 讀完整條 thread，抽出四樣結構化資料——一句話問題、摘要、解決方案、系統與程式碼參照——正規化成一致格式之後才拿去 embed"
    source_quotes:
      - "在真正把文字丟進向量模型之前，系統還做了一步叫 distillation 的處理：不直接 embed 原始的討論串文字，而是先讓 LLM 讀完整條 thread，抽出四樣結構化資料——一句話問題、摘要、解決方案、系統與程式碼參照——正規化成一致格式之後才拿去 embed。"
    anchor_type: 設計參數
    importance: 3
    status: normal
  - id: c4
    role: anchor
    text: "原始文字則另外走 Postgres 的全文索引，保持可以被字面搜尋到，但不進向量空間"
    source_quotes:
      - "原始文字則另外走 Postgres 的全文索引，保持可以被字面搜尋到，但不進向量空間。"
    qualifiers:
      - text: bursting 另外會把同一個作者連續發的訊息，前面加上這條 thread 的主題後單獨 embed 一次，但每個 burst 必須通過三道品質門檻才會留下
        source_quote: "把「同一個作者連續發的訊息」單獨抓出來，前面加上這條 thread 的主題當作上下文，單獨 embed 一次。但不是每個 burst 都值得留：必須通過三道品質門檻"
    anchor_type: 設計參數
    importance: 4
    status: normal
  - id: c5
    role: mechanism
    text: "embedding 品質高度依賴輸入文字的形式一致性；如果直接把長短、參與人數差異極大的原始文字拿去 embed，產生的向量在「什麼代表這個文件」這件事上根本無法互相比較"
    source_quotes:
      - "embedding 品質高度依賴輸入文字的形式一致性。"
      - "如果直接把這些長短、參與人數差異極大的原始文字拿去 embed，產生的向量在「什麼代表這個文件」這件事上根本無法互相比較。"
    anchor_type: 部落格判斷
    importance: 5
    status: normal
  - id: c6
    role: anchor
    text: "舉例來說，一條討論串可能有 2 個人講 3 句話，也可能有 10 個人吵了 50 則訊息還離題"
    source_quotes:
      - "一條討論串可能有 2 個人講 3 句話，也可能有 10 個人吵了 50 則訊息還離題"
    anchor_type: 部落格舉例
    numeric_kind: non_comparative
    numeric_reason: 示範題
    importance: 6
    status: normal
  - id: c7
    role: evidence
    text: "文章提到，討論串正規化成一致格式之後，準確率有實測上的顯著提升，但沒有附上具體數字"
    source_quotes:
      - "文章裡提到，討論串正規化成一致格式之後，準確率有實測上的顯著提升——雖然沒有附上具體數字，但這個方向本身已經被驗證過，不是憑空的設計偏好。"
    qualifiers:
      - text: 文章沒有附上具體數字
        source_quote: "雖然沒有附上具體數字"
    anchor_type: 官方宣稱
    importance: 7
    status: normal
  - id: c8
    role: evaluation
    text: "文章用的詞是「normalized」而不是「summarized」，強調的重點是讓向量在同一個表示空間裡語意一致，而不只是把文字弄短"
    source_quotes:
      - "這裡文章用的詞是「normalized」而不是「summarized」，強調的重點是讓向量在同一個表示空間裡語意一致，而不只是把文字弄短。"
    anchor_type: 部落格判斷
    importance: 8
    status: normal
  - id: c9
    role: mechanism
    text: "Distillation 是有損壓縮，重要的旁枝訊息可能因為不在主線問答脈絡裡而被摘要忽略掉；系統用 bursting 補救：把「同一個作者連續發的訊息」單獨抓出來，前面加上這條 thread 的主題當作上下文，單獨 embed 一次"
    source_quotes:
      - "不過 distillation 是有損壓縮，重要的旁枝訊息可能因為不在主線問答脈絡裡而被摘要忽略掉。系統用一個叫 bursting 的機制補救：把「同一個作者連續發的訊息」單獨抓出來，前面加上這條 thread 的主題當作上下文，單獨 embed 一次。"
    anchor_type: 設計參數
    importance: 9
    status: normal
  - id: c10
    role: anchor
    text: "不是每個 burst 都值得留，必須通過三道品質門檻：IDF 要 ≥ 4.0（確保含有稀有詞，不是純廢話）、長度要 ≥ 200 字元（確保內容量足以撐起一個有意義的向量）、有 reaction 加分（用社交訊號間接驗證這則訊息有價值）"
    source_quotes:
      - "但不是每個 burst 都值得留：必須通過三道品質門檻——IDF 要 ≥ 4.0（確保含有稀有詞，不是純廢話）、長度要 ≥ 200 字元（確保內容量足以撐起一個有意義的向量）、有 reaction 加分（用社交訊號間接驗證這則訊息有價值）。"
    anchor_type: 設計參數
    numeric_kind: non_comparative
    numeric_reason: 定義
    importance: 10
    status: normal
  - id: c11
    role: anchor
    text: "舉個具體例子：一條有 4 位發言者、5 則訊息的討論串，最後可能產生 1 筆討論串層級的 distillation 產物，加上 N 筆通過品質門檻的 burst，全部寫進同一張 embeddings table，靠 metadata 標記類型是 slack_thread 還是 slack_burst；沒通過門檻的 burst（比如純粹的社交填充語）則完全不會被 embed"
    source_quotes:
      - "舉個具體例子：一條有 4 位發言者、5 則訊息的討論串，最後可能產生「1 筆討論串層級的 distillation 產物，加上 N 筆通過品質門檻的 burst」，全部寫進同一張 embeddings table，靠 metadata 標記類型是 `slack_thread` 還是 `slack_burst`。沒通過門檻的 burst（比如純粹的社交填充語）則完全不會被 embed。"
    anchor_type: 部落格舉例
    numeric_kind: non_comparative
    numeric_reason: 示範題
    importance: 11
    status: normal
  - id: c12
    role: evaluation
    text: "與其等資料進了系統之後，靠後段昂貴的 rerank 去補救垃圾資料排太前面，不如在寫入時就用低成本規則先過濾一批；寫入時過濾是一次性成本，rerank 卻是每次查詢都要付的成本，越早把噪音擋掉，長期越省"
    source_quotes:
      - "與其等資料進了系統之後，靠後段昂貴的 rerank 去補救垃圾資料排太前面，不如在寫入時就用低成本規則先過濾一批。寫入時過濾是一次性成本，rerank 卻是每次查詢都要付的成本——越早把噪音擋掉，長期越省。"
    anchor_type: 部落格判斷
    importance: 12
    status: normal
  - id: c13
    role: anchor
    text: "Contextual Retrieval 的核心主張是為每個 chunk 生成一段客製化的上下文前綴，避免脫離語境的孤立片段"
    source_quotes:
      - "Contextual Retrieval 的核心主張是為每個 chunk 生成一段客製化的上下文前綴，避免脫離語境的孤立片段。"
    anchor_type: 外部研究引用
    importance: 13
    status: normal
  - id: c14
    role: evaluation
    text: "Bursting 其實是 Contextual Retrieval 同一個原理的輕量版本：不用為每個 burst 都跑一次 LLM 去生成上下文，直接把整條討論串的主題貼上去當前綴，用便宜很多的方式達到類似的效果"
    source_quotes:
      - "熟悉 Anthropic 的 Contextual Retrieval 的人可能會覺得 bursting 有點眼熟。"
      - "Bursting 其實是同一個原理的輕量版本：不用為每個 burst 都跑一次 LLM 去生成上下文，直接把整條討論串的主題貼上去當前綴，用便宜很多的方式達到類似的效果。"
    anchor_type: 部落格判斷
    importance: 14
    status: normal
```
