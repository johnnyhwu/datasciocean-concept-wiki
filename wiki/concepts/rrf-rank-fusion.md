---
id: rrf-rank-fusion
title: RRF 只用名次不用分數，繞開分數尺度不可比的難題；但它「獎勵共識」的機制在某一路完全缺席時會失靈
type_hint: 方法
context_type: evidence_from_single_source
sources:
  - article: cerebras-rag
    article_title: "拆解 Cerebras 企業知識庫 RAG：窄腰設計、檢索推理解耦與 Pipeline 的邊界"
    url: https://datasciocean.com/paper-intro/cerebras-rag/
    sections:
      - 前言
      - 多路檢索排完名之後，怎麼變成一份排序
      - RRF：只看名次，不看分數
      - 融合排序之後的收尾：去重、Rerank、補回上下文
    first_appearance: true
parent: null
related:
  - slack-vector-failure-orthogonal-signals
  - rag-narrow-waist
  - rag-planner-single-round-vs-agentic
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: "RRF 最核心的巧思在於它只用「名次」不用「分數」：名次是所有檢索器都天然具備、而且天然可以互相比較的整數，這一招直接繞開了「分數尺度不可比」這個難題，不需要正規化，也就沒有正規化帶來的飄移問題"
    source_quotes:
      - "RRF 最核心的巧思在於：它只用「名次」不用「分數」。名次是所有檢索器都天然具備、而且天然可以互相比較的整數，這一招直接繞開了「分數尺度不可比」這個難題，不需要正規化，也就沒有正規化帶來的飄移問題。"
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
    text: "系統同時用好幾種檢索器（向量搜尋、全文搜尋、IDF 加權等）打同一個查詢，但不同檢索器的分數完全沒辦法直接比較：BM25 的分數範圍不固定，cosine 相似度卻落在 -1 到 1 之間，單位、尺度、分布形狀都不一樣，加起來沒有意義"
    source_quotes:
      - "系統同時用好幾種檢索器打同一個查詢（向量搜尋、全文搜尋、IDF 加權等），但這帶來一個直接的麻煩：不同檢索器的分數完全沒辦法直接比較。BM25 的分數範圍不固定，cosine 相似度卻落在 -1 到 1 之間，單位、尺度、分布形狀都不一樣，加起來沒有意義。"
    anchor_type: 背景說明
    numeric_kind: non_comparative
    numeric_reason: 定義
    importance: 3
    status: normal
  - id: c4
    role: mechanism
    text: "常見的解法是把每種分數都正規化到 0 到 1 之間再加權相加，但正規化依賴「這批結果裡的最大值、最小值是多少」，同一份文件在不同查詢批次裡的相對權重會因此飄移不定"
    source_quotes:
      - "常見的解法是把每種分數都正規化到 0 到 1 之間再加權相加，但這也有陷阱：正規化依賴「這批結果裡的最大值、最小值是多少」，同一份文件在不同查詢批次裡的相對權重會因此飄移不定。"
    anchor_type: 背景說明
    numeric_kind: non_comparative
    numeric_reason: 定義
    importance: 4
    status: normal
  - id: c5
    role: mechanism
    text: "RRF 的公式是 RRFscore(d) = Σ weight_i / (k + rank_i(d))，對所有檢索器加總；如果某個檢索器根本沒撈到這份文件，那一項貢獻就是 0，不加分也不扣分"
    source_quotes:
      - "RRFscore(d) = Σ  weight_i / (k + rank_i(d))"
      - "如果某個檢索器根本沒撈到這份文件，那一項貢獻就是 0——不加分也不扣分。"
    anchor_type: 設計參數
    numeric_kind: non_comparative
    numeric_reason: 定義
    importance: 5
    status: normal
  - id: c6
    role: anchor
    text: "Cerebras 的 RRF 設定 k = 60（這個平滑常數來自 Cormack 等人在 2009 年那篇論文的建議值），weight 預設是 1.0"
    source_quotes:
      - "其中 k = 60（這個平滑常數來自 Cormack 等人在 2009 年那篇論文的建議值），weight 預設是 1.0。"
    anchor_type: 設計參數
    numeric_kind: non_comparative
    numeric_reason: 定義
    importance: 6
    status: normal
  - id: c7
    role: mechanism
    text: "k 越大，頭部名次之間的分數差距被壓得越平，系統越傾向讓「多路都上榜、分數慢慢累積」贏過「單路衝到第一名」，也就是偏好共識勝過單一強訊號；k 越小，第一名拿到的獎勵越懸殊，系統越傾向相信單一檢索器給出的強烈信號"
    source_quotes:
      - "k 越大，頭部名次之間的分數差距被壓得越平，系統越傾向讓「多路都上榜、分數慢慢累積」贏過「單路衝到第一名」——也就是偏好共識勝過單一強訊號；k 越小，第一名拿到的獎勵越懸殊，系統越傾向相信單一檢索器給出的強烈信號。"
    anchor_type: 部落格判斷
    importance: 7
    status: normal
  - id: c8
    role: evaluation
    text: "選 k=60，等於 Cerebras 選擇了「寧可相信多個獨立訊號的共識，也不要被單一路的巧合命中牽著走」"
    source_quotes:
      - "選 k=60，等於 Cerebras 選擇了「寧可相信多個獨立訊號的共識，也不要被單一路的巧合命中牽著走」。"
    anchor_type: 部落格判斷
    numeric_kind: non_comparative
    numeric_reason: 定義
    importance: 8
    status: normal
  - id: c9
    role: anchor
    text: "如果 A 文件在兩路檢索裡都排第三名，B 文件在一路排第一名、另一路卻只排到第八名，算出來的 RRF 分數常常是 A 贏：一份「兩邊都還算穩定」的文件，可能贏過一份「單邊很強但另一邊普通」的文件"
    source_quotes:
      - "如果 A 文件在兩路檢索裡都排第三名，B 文件在一路排第一名、另一路卻只排到第八名，算出來的 RRF 分數常常是 A 贏——一份「兩邊都還算穩定」的文件，可能贏過一份「單邊很強但另一邊普通」的文件。"
    anchor_type: 部落格舉例
    importance: 9
    status: normal
  - id: c10
    role: mechanism
    text: "RRF 排序純粹是統計融合，不理解查詢的實際語意；reranker（一種 cross-encoder 模型）會把查詢跟每一份候選文件逐一配對，直接輸出相關性分數，能做到 RRF 做不到的語意層面判斷"
    source_quotes:
      - "RRF 排序純粹是統計融合，不理解查詢的實際語意，而 reranker 會把查詢跟每一份候選文件逐一配對，直接輸出相關性分數，能做到 RRF 做不到的語意層面判斷。"
      - "第二個是讓 reranker（一種 cross-encoder 模型）出馬"
    anchor_type: 設計參數
    importance: 10
    status: normal
  - id: c11
    role: anchor
    text: "融合排序算完之後，還有去重跟限額（同一份文件常被切成好幾個 chunk，限制同一份文件最多貢獻幾筆進候選集合，避免佔滿名額、讓資訊來源的多樣性下降），以及 rerank 之後的補回上下文（拿到最終 top 10 後，如果贏家是某份文件裡的一個 section，額外撈回相鄰的兩個 section 一起呈現，避免 chunking 把前提條件或注意事項切到隔壁 chunk）"
    source_quotes:
      - "融合排序算完之後，還有三個收尾動作。第一個是去重跟限額：同一份文件常常被切成好幾個 chunk，如果好幾個 chunk 都排進候選集合前段，會佔滿名額，讓資訊來源的多樣性下降，做法是限制同一份文件最多貢獻幾筆進候選集合。"
      - "最後一個收尾動作是補回上下文：拿到最終 top 10 之後，如果贏家是某份文件裡的一個 section，系統會額外撈回相鄰的兩個 section 一起呈現，避免 chunking 把前提條件或注意事項切到隔壁 chunk 而遺失掉。這個動作只發生在 rerank 之後、只對最終要呈現的少量結果做，避免在候選階段就浪費資源。"
    anchor_type: 設計參數
    numeric_kind: non_comparative
    numeric_reason: 計數
    importance: 11
    status: normal
  - id: c12
    role: mechanism
    text: "整條處理線是「漸進昂貴」：越後面的步驟，單次呼叫成本越高，所以前面用便宜的步驟（RRF 融合、去重限額）盡量把候選集合縮小，把最貴的運算（synthesis）留給少量高信心的候選"
    source_quotes:
      - "整條處理線其實是「漸進昂貴」：越後面的步驟，單次呼叫成本越高。所以前面用便宜的步驟（RRF 融合、去重限額）盡量把候選集合縮小，把最貴的運算（synthesis）留給少量高信心的候選。"
    anchor_type: 部落格判斷
    importance: 12
    status: normal
  - id: c13
    role: evaluation
    text: "RRF「獎勵共識」的機制隱含一個假設：每一路都至少「看得到」正確答案，只是排名高低不同；一旦正確答案在某一路完全缺席，RRF 對那一路的貢獻是 0，「共識」機制反而變成「懲罰」，正確答案只靠單路分數撐著，可能輸給一份兩路都排名普通、但兩路都有出現的雜訊文件"
    source_quotes:
      - "RRF「獎勵共識」的機制隱含一個假設——每一路都至少「看得到」正確答案，只是排名高低不同。一旦正確答案在某一路完全缺席（連候選都沒進去），RRF 對那一路的貢獻是 0，「共識」機制反而變成「懲罰」，正確答案只靠單路分數撐著，可能輸給一份兩路都排名普通、但兩路都有出現的雜訊文件。"
    anchor_type: 部落格判斷
    numeric_kind: non_comparative
    numeric_reason: 定義
    importance: 13
    status: normal
  - id: c14
    role: anchor
    text: "作者做投影片檢索時遇過這個弱點：每頁投影片先用 VLM（視覺語言模型）產生文字摘要再拿去 embed，搭配混合檢索；常出現正確答案那一頁在向量檢索排第一名，但全文搜尋完全沒撈到它（反過來也會發生），融合完之後正確答案排名反而不好；暫時的權宜解法是「永遠保留向量跟全文各自的第一名」"
    source_quotes:
      - "RRF 用久了會踩到一個結構性弱點，我自己在做投影片檢索時遇過。場景是這樣的：每頁投影片先用 VLM（視覺語言模型）產生文字摘要，再拿去 embed，搭配混合檢索。常出現的狀況是，正確答案的那一頁在向量檢索排第一名，但全文搜尋完全沒撈到它（反過來的情況也會發生）。融合完之後，正確答案排名反而不好。暫時的權宜解法是「永遠保留向量跟全文各自的第一名」。"
    anchor_type: 部落格舉例
    importance: 14
    status: normal
  - id: c15
    role: evaluation
    text: "投影片場景特別容易踩到這個問題，因為向量跟全文兩路共用同一個不穩定的中介來源：VLM 生成摘要時用詞不穩定，同一張圖可能寫「revenue growth」，也可能寫「sales increase」，導致對字面詞彙敏感的全文搜尋容易完全掛零；兩路訊號源頭一致，破壞了「訊號要正交」這個前提"
    source_quotes:
      - "投影片場景特別容易踩到這個問題，因為向量跟全文兩路**共用同一個不穩定的中介來源**——VLM 生成摘要時用詞不穩定，同一張圖可能寫「revenue growth」，也可能寫「sales increase」，導致全文搜尋這種對字面詞彙敏感的方法容易因為用詞不巧而完全掛零。兩路訊號源頭一致，正好破壞了前面提到「訊號要正交」這個前提。"
    anchor_type: 部落格判斷
    importance: 15
    status: normal
  - id: c16
    role: evaluation
    text: "解法可以由淺到深疊著用：先把各路的召回深度拉深（比如拉到 top 50 到 100），因為很多「單路缺席」其實是候選在截斷線之外被切掉；再修正表示層讓兩路訊號源頭不同——全文搜尋不該只索引 VLM 摘要，應該額外加入投影片頁面的原始文字（OCR 抽出的標題、bullet、圖表標籤）"
    source_quotes:
      - "解法可以由淺到深疊著用：先把各路的召回深度拉深（比如拉到 top 50 到 100），很多「單路缺席」其實是候選在截斷線之外被切掉，拉深召回可以把它撈回來，而且 RRF 對深處名次的貢獻本來就小，不容易引入額外噪音。再往下，可以修正表示層讓兩路訊號源頭不同——全文搜尋不該只索引 VLM 摘要，應該額外加入投影片頁面的原始文字（OCR 抽出的標題、bullet、圖表標籤），原始文字用詞穩定，不受 VLM 選詞不穩定的影響。"
    anchor_type: 部落格判斷
    numeric_kind: non_comparative
    numeric_reason: 示範題
    importance: 16
    status: normal
  - id: c17
    role: evaluation
    text: "最根本的做法是讓 reranker 補 RRF 的結構弱點：各路拉深召回後取聯集（不只信 RRF 分數），交給 cross-encoder 重新逐一打分，reranker 對查詢跟文件直接配對評估，不管來源路數，只要正確答案進了聯集就有機會被排到最前面，天生免疫「單路缺席」的問題"
    source_quotes:
      - "最根本的做法是讓 reranker 補 RRF 的結構弱點：各路拉深召回後取聯集（不只信 RRF 分數），交給 cross-encoder 重新逐一打分——reranker 對查詢跟文件直接配對評估，不管來源路數，只要正確答案進了聯集就有機會被排到最前面，天生免疫「單路缺席」的問題。"
    anchor_type: 部落格判斷
    importance: 17
    status: normal
```

## 名詞補充（通用知識，非 blog 內容）

- RRF：Reciprocal Rank Fusion 的縮寫。
- 召回（recall）：檢索階段「撈回多少相關文件」的能力；「召回深度」指每一路檢索往下撈到第幾名。
- OCR：光學文字辨識，把圖片中的文字抽成可處理的文字。
