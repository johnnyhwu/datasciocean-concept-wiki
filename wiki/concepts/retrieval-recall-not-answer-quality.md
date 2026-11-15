---
id: retrieval-recall-not-answer-quality
title: 檢索指標好不等於答案好：Evidence Recall 只測該撈的撈到沒有、不測多撈進來的雜訊，只盯 recall 類指標會把系統推向「撈更多」，最終答案品質可能不動甚至下降
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: ragu
  article_title: "RAGU：一篇替 GraphRAG 量出天花板的論文"
  url: https://datasciocean.com/paper-intro/ragu/
  sections:
  - 前言
  - GraphRAG 在解什麼問題
  - 方法：六個步驟，原創的只有一格
  - 實驗：把混淆變因一層層剝掉
  - 第三層：所謂的 cross-over 是誰在動
  - 觀念三：檢索指標好，不等於答案好
  - 值得帶走的五件事
  first_appearance: true
parent: null
related:
  - ragu-results-peeling-confounds
  - entity-resolution-not-clustering
  - graph-vs-vector-clustering-modularity
  - small-extractor-saturation-not-scale
  - ragu-pipeline-two-stage-extraction-consolidation
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 檢索指標好不等於答案好：Evidence Recall 只測「該撈的撈到沒有」，完全不測「不該撈的有沒有撈進來」；只盯著 recall 類指標（撈回率、hit rate）會系統性地把系統推向「撈更多」，而最終答案品質可能不動甚至下降，所以至少要同時看 context precision，最好直接看 end-to-end 的答案指標
  source_quotes:
  - "關鍵在於，Evidence Recall 只測「該撈的撈到沒有」，完全不測「不該撈的有沒有撈進來」。"
  - "只盯著 recall 類指標（撈回率、hit rate）會系統性地把系統推向「撈更多」，而最終答案品質可能不動甚至下降。至少要同時看 context precision，最好直接看 end-to-end 的答案指標。"
  qualifiers:
  - text: blog 說優化 recall 跟優化最終正確率互相拉扯，是在 factoid 任務上
    source_quote: "這個觀念脫離這篇論文也成立：優化 recall 跟優化最終正確率，在 factoid 任務上是互相拉扯的。"
  - text: blog 也說在 Creative Generation 這類需要廣泛相關材料的任務，多餘材料是資產、有利於高 recall
    source_quote: "多餘材料是 | 干擾 | 資產"
  - text: 在 RAGU 這篇論文裡，Precision（撈到的相關材料除以全部撈到的材料）沒有人測
    source_quote: "Precision = 撈到的相關材料 / 全部撈到的材料    ← 沒有人測"
  - text: 論文列出 Context Relevancy 這個指標，但全篇沒有任何一個數值
    source_quote: "但它在所有表格與圖裡全部沒有出現，全篇沒有任何一個數值"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: 這個觀念的來源是 RAGU：ITMO University 團隊的 GraphRAG 引擎；GraphRAG 先請 LLM 把文件裡的實體跟關係抽出來建成知識圖，檢索時可以沿著圖上的邊走；RAGU 的主張是把知識圖的「抽取」跟「整併」拆成兩個階段，圖會更乾淨，檢索也會更完整；它的核心賣點 consolidation 是 Step 3（Deduplication & Summarization，去重與摘要）
  source_quotes:
  - "RAGU 是 ITMO University 團隊在 2026 年 7 月[放上 arXiv](https://arxiv.org/abs/2607.11683)的 GraphRAG 引擎"
  - "GraphRAG 的解法是先請 LLM 把文件裡的實體（人、組織、產品）跟關係抽出來建成知識圖，檢索時可以沿著圖上的邊走。"
  - "論文的主張是：把知識圖的「抽取」跟「整併」拆成兩個階段，圖會更乾淨，檢索也會更完整。"
  - "Step 3  Deduplication & Summarization  ★ 這篇唯一的原創處"
  - "**論文從頭到尾沒有做「有 Step 3 vs 沒 Step 3」的 ablation**。附錄的組態實驗只測了 ICL（in-context learning，要不要在 prompt 裡放範例）、validation、抽取模型大小三個開關，唯獨沒測它自己的核心賣點。所以 consolidation 究竟帶來多少 gain"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: 論文的指標中，ER（Evidence Recall）測檢索階段撈回了多少比例的相關材料，只評檢索；AC（Answer Correctness）由 LLM-judge 判斷答案語意上對不對，Cov（Coverage）測有沒有涵蓋所有該講的重點，這兩個評最終答案
  source_quotes:
  - "AC | Answer Correctness | 答案語意上對不對（LLM-judge）"
  - "Cov | Coverage | 有沒有涵蓋所有該講的重點"
  - "ER | Evidence Recall | 檢索階段撈回了多少比例的相關材料"
  - "其中 ER 只評檢索，AC / Cov / Faith 評最終答案"
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: Recall 是撈到的相關材料除以全部相關材料，ER 測的就是這個；Precision 是撈到的相關材料除以全部撈到的材料，blog 指出在 RAGU 這篇論文裡沒有人測，ER 只測 recall、不測 precision
  source_quotes:
  - "Recall    = 撈到的相關材料 / 全部相關材料      ← ER 測這個"
  - "Precision = 撈到的相關材料 / 全部撈到的材料    ← 沒有人測"
  - "ER 只測 recall、不測 precision。"
  anchor_type: 背景說明
  importance: 4
  status: normal
- id: c5
  role: anchor
  text: 有一組數字是真的：Creative Generation 層級的 Coverage 是 LightRAG 3.9、HippoRAG 2 34.7、RAGU 57.4；blog 認為 RAGU 對 HippoRAG 2 的 22.7 pp Coverage 差距不是雜訊，也不是格式造成的
  source_quotes:
  - "有一組數字是真的。Creative Generation 的 Coverage：LightRAG 3.9、HippoRAG 2 34.7、RAGU 57.4。"
  - "22.7 pp 的 Coverage 差距不是雜訊，也不是格式造成的"
  comparison_target: HippoRAG 2（34.7）與 LightRAG（3.9）的 Coverage
  anchor_type: 實驗結果
  importance: 5
  status: normal
- id: c6
  role: evidence
  text: RAGU 的 Evidence Recall 在四個難度層級上分別是 82.4 / 74.5 / 74.8 / 53.1，blog 說四格都高過 LightRAG 與 HippoRAG 2
  source_quotes:
  - "RAGU 的 Evidence Recall 在四個難度上分別是 82.4 / 74.5 / 74.8 / 53.1，四格都高過 LightRAG 與 HippoRAG 2。"
  comparison_target: LightRAG 與 HippoRAG 2 的 Evidence Recall
  anchor_type: 實驗結果
  importance: 6
  status: pending_author_confirmation
  figures:
  - file: figures/ragu/figure3.png
    article: ragu
    src: figure3.png
    caption: 圖四 — 依任務複雜度呈現的 cross-over。(a) 是 Answer Correctness，(b) 是 Evidence Recall。（來源：原始論文 Figure 3）
    sha256: bc2a410d1ff16f1acd80d16f5563cd590c6c40f4f5a5943f445c5d860f8d83a7
- id: c7
  role: evidence
  text: blog 指出整篇論文最值得想清楚的張力：如果 RAGU 檢索到更完整的證據，為什麼最終答案正確率反而輸？例如 Fact Retrieval 層級的 AC，RAGU 54.2、HippoRAG 2 72.4
  source_quotes:
  - "但這就引出整篇論文最值得想清楚的張力：**如果 RAGU 檢索到更完整的證據，為什麼最終答案正確率反而輸？**"
  - "任務 | LightRAG | HippoRAG 2 | RAGU"
  - "Fact Retrieval | 26.2 | **72.4** | 54.2"
  comparison_target: HippoRAG 2（Fact Retrieval 的 AC）
  qualifiers:
  - text: 這組 AC 是 GraphRAG-Bench Medical 的難度層級，都用 Meno-Lite-0.1（RAGU 附帶的抽取模型）建圖
    source_quote: "GraphRAG-Bench Medical 上四個難度層級的 AC（都用 Meno-Lite-0.1 建圖）："
  - text: AC 是單一 judge 模型的單次評分，論文沒有 error bar、也沒有人工驗證 judge 準確度
    source_quote: "AC 是單一 judge 模型的單次評分，論文沒有 error bar、也沒有人工驗證 judge 準確度，個位數 pp 的差距不宜當結論。"
  anchor_type: 部落格判斷
  importance: 7
  status: normal
- id: c8
  role: evidence
  text: blog 舉例說明 recall 高與 precision 低可以同時發生：HippoRAG 2 的 context 是 3 段相關，ER = 3/4 = 0.75、precision = 3/3 = 1.00；RAGU 的 context 是 4 段相關加 4 段雜訊，ER = 4/4 = 1.00、precision = 4/8 = 0.50
  source_quotes:
  - "兩者可以同時發生："
  - "HippoRAG 2 的 context:  [相關][相關][相關]"
  - "→ ER = 3/4 = 0.75    precision = 3/3 = 1.00"
  - "RAGU 的 context:        [相關][相關][相關][相關][雜訊][雜訊][雜訊][雜訊]"
  - "→ ER = 4/4 = 1.00    precision = 4/8 = 0.50"
  comparison_target: 兩個示範 context 互相比較（HippoRAG 2 對 RAGU）
  anchor_type: 部落格舉例
  importance: 8
  status: normal
- id: c9
  role: mechanism
  text: blog 推論 RAGU 撈到的不是「更正確的資訊」，是「更完整但濃度更低的資訊」，而且這是設計必然：consolidation 把同一實體的所有提及合併起來，LocalSearch 又從實體擴展到關係、再擴展到 chunk，整條路線的傾向就是多撈
  source_quotes:
  - "**RAGU 撈到的不是「更正確的資訊」，是「更完整但濃度更低的資訊」。** 而且這不是意外，是設計必然：consolidation 把同一實體的所有提及合併起來，LocalSearch 又從實體擴展到關係、再擴展到 chunk，整條路線的傾向就是多撈。"
  qualifiers:
  - text: Precision（撈到的相關材料除以全部撈到的材料）在這篇論文裡沒有人測
    source_quote: "Precision = 撈到的相關材料 / 全部撈到的材料    ← 沒有人測"
  anchor_type: 部落格推論
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: blog 認為多撈會傷害答案的前兩個機制：一是干擾項，factoid 問題只有一個正確答案，context 裡多塞幾段語意相關但答案不同的材料，LLM 挑錯的機率就上升；二是 lost in the middle，長 context 裡模型對開頭結尾敏感、中間容易被忽略，「答案在 context 裡」跟「模型會用到它」是兩回事，ER 測前者、AC 測後者
  source_quotes:
  - "多撈為什麼實際上會傷害答案，有三個機制。第一是干擾項：factoid 問題只有一個正確答案，context 裡多塞幾段語意相關但答案不同的材料，LLM 挑錯的機率就上升。第二是 lost in the middle，長 context 裡模型對開頭結尾敏感、中間容易被忽略，「答案在 context 裡」跟「模型會用到它」是兩回事，ER 測前者、AC 測後者。"
  qualifiers:
  - text: Precision 在這篇論文裡沒有人測
    source_quote: "Precision = 撈到的相關材料 / 全部撈到的材料    ← 沒有人測"
  anchor_type: 部落格推論
  importance: 10
  status: normal
- id: c11
  role: mechanism
  text: blog 認為第三個機制是任務性質決定誰吃虧：Fact Retrieval 需要一個精確的事實，多餘材料是干擾，有利於高 precision；Creative Generation 需要廣泛的相關材料，多餘材料是資產，有利於高 recall
  source_quotes:
  - "第三是任務性質決定誰吃虧："
  - "| Fact Retrieval | Creative Generation"
  - "需要 | 一個精確的事實 | 廣泛的相關材料"
  - "多餘材料是 | 干擾 | 資產"
  - "有利於 | 高 precision | 高 recall"
  anchor_type: 部落格推論
  importance: 11
  status: normal
- id: c12
  role: mechanism
  text: blog 認為這才是 cross-over（論文的敘事：任務越難 RAGU 越強，最後反超 HippoRAG 2；blog 拆解為 RAGU 在最難的一格追過 HippoRAG 2）的真正機制：RAGU 不是在難任務上變聰明，而是一路用同一種策略（多撈），這個策略在簡單任務上是負擔、在合成類任務上才變成優勢
  source_quotes:
  - "論文最漂亮的敘事是 cross-over：任務越難，RAGU 越強，最後反超 HippoRAG 2。"
  - "RAGU 的表現對任務難度不敏感，HippoRAG 2 敏感，所以在最難的一格被追過。"
  - "這才是 cross-over 的真正機制。RAGU 不是在難任務上變聰明，而是它一路用同一種策略（多撈），這個策略在簡單任務上是負擔、在合成類任務上才變成優勢。"
  qualifiers:
  - text: Precision 在這篇論文裡沒有人測
    source_quote: "Precision = 撈到的相關材料 / 全部撈到的材料    ← 沒有人測"
  - text: 最難那格 RAGU 贏的是 59.0 對 56.9，2.1 pp，blog 說落在 LLM-judge 的雜訊範圍內
    source_quote: "何況最後那格贏的是 59.0 對 56.9，2.1 pp，落在 LLM-judge 的雜訊範圍內。"
  - text: AC 是單一 judge 模型的單次評分，論文沒有 error bar、也沒有人工驗證 judge 準確度，blog 提醒個位數 pp 的差距不宜當結論
    source_quote: "AC 是單一 judge 模型的單次評分，論文沒有 error bar、也沒有人工驗證 judge 準確度，個位數 pp 的差距不宜當結論。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: 論文只用一句話帶過這件事：HippoRAG 2 在 Evidence Recall 較低的情況下仍然贏得 factoid AC，反映的是它鏈式走訪在單一事實查詢上的 precision；blog 認為方向是對的，但沒有任何數據支持
  source_quotes:
  - "論文只用一句話帶過這件事：HippoRAG 2 在 Evidence Recall 較低的情況下仍然贏得 factoid AC，反映的是它鏈式走訪在單一事實查詢上的 precision。方向是對的，但沒有任何數據支持。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 13
  status: normal
- id: c14
  role: evaluation
  text: blog 指出最關鍵的缺口：論文列出使用的指標時包含了 Context Relevancy，正好就是回答這個問題需要的那個數字，但它在所有表格與圖裡全部沒有出現，全篇沒有任何一個數值，論文也沒有說明原因
  source_quotes:
  - "而最關鍵的缺口在這裡——**論文列出使用的指標時包含了 Context Relevancy，正好就是回答這個問題需要的那個數字，但它在所有表格與圖裡全部沒有出現，全篇沒有任何一個數值**，論文也沒有說明原因。"
  anchor_type: 部落格判斷
  importance: 14
  status: normal
- id: c15
  role: mechanism
  text: blog 認為 Coverage 的差距確實支持論文的機制假說：consolidation 讓圖更完整、更連通，撈得回更多相關材料
  source_quotes:
  - "它確實支持論文的機制假說：consolidation 讓圖更完整、更連通，撈得回更多相關材料。"
  qualifiers:
  - text: 論文從頭到尾沒有做「有 Step 3（consolidation）vs 沒 Step 3」的 ablation
    source_quote: "論文從頭到尾沒有做「有 Step 3 vs 沒 Step 3」的 ablation"
  - text: consolidation 究竟帶來多少 gain，論文只有跟 LightRAG 的跨系統比較，而兩者的差異遠不只 Step 3
    source_quote: "所以 consolidation 究竟帶來多少 gain，論文只有跟 LightRAG 的跨系統比較，而兩者的差異遠不只 Step 3。"
  - text: 在 blog 的指標說明裡，Coverage 屬於評最終答案的指標，ER 才是只評檢索的指標
    source_quote: "其中 ER 只評檢索，AC / Cov / Faith 評最終答案"
  anchor_type: 部落格推論
  importance: 15
  status: normal
- id: c16
  role: evaluation
  text: blog 認為這個觀念脫離這篇論文也成立：優化 recall 跟優化最終正確率，在 factoid 任務上是互相拉扯的；它會改變你調系統時盯哪個儀表板，而且跟 GraphRAG 完全無關
  source_quotes:
  - "這個觀念脫離這篇論文也成立：優化 recall 跟優化最終正確率，在 factoid 任務上是互相拉扯的。"
  - "這條會改變你調系統時盯哪個儀表板，而且跟 GraphRAG 完全無關。"
  anchor_type: 部落格判斷
  importance: 16
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

- factoid 問題：答案是單一、簡短事實（人名、日期、地名）的問題。
- hit rate：檢索評估指標，指相關材料至少有一筆出現在撈回結果裡的查詢比例。
