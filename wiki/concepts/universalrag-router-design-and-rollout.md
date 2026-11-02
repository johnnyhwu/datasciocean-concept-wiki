---
id: universalrag-router-design-and-rollout
title: UniversalRAG 的 Router 做的是多選題，從 7 個「模態 × 粒度」路徑中選出組合，有訓練型與免訓練型兩種做法；企業私有數據可先用免訓練路由器加混合檢索冷啟動，累積日誌後再訓練專屬的路由器
type_hint: 方法
context_type: bound_to_source
sources:
- article: universal-rag
  article_title: "UniversalRAG 深度解析：破解多模態 RAG 偏見，提升異質數據的檢索能力"
  url: https://datasciocean.com/paper-intro/universal-rag/
  sections:
  - 前言
  - Granularity Mismatch
  - Efficiency & Scalability
  - 方法介紹：UniversalRAG 的核心架構
  - 模態與粒度的階層化組織
  - The Router
  - Router's Label Space
  - Training-based Router
  - Training-free Router
  - Generation
  - 從研究到實務的轉化
  first_appearance: true
parent: null
related:
  - universalrag-routing-over-unified-embedding
  - rag-planner-single-round-vs-agentic
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: UniversalRAG 的 Router 分析 Query 的意圖，從 7 個 Pathways 中選出最佳組合，它做的不是單選題而是多選題；Router 有訓練型與免訓練型兩種做法，blog 建議企業私有數據在初期先採用免訓練路由器並結合混合檢索，之後再訓練專屬於企業環境的輕量化路由器
  source_quotes:
  - "Router 的任務是分析 Query 的意圖，並從 7 個 Pathways 中選出最佳組合。"
  - "Router 並非做單選題，而是多選題。"
  - "實作細節: 訓練型 (Training-based) 與免訓練 (Training-free) Router 的具體作法。"
  - "初期 (冷啟動)：採用「免訓練路由器 (Prompt-based) 」並結合「混合檢索 (Hybrid Search) 」"
  - "後期 (優化期)：訓練專屬於企業環境的輕量化路由器"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 計數
  qualifiers:
  - text: 企業落地的分階段策略是 blog 面對企業內部私有數據總結出來的，不是論文在 Benchmark 上驗證過的做法
    source_quote: "雖然論文在 Benchmark 上表現優異，但面對企業內部的私有數據 (Private Data) ，我們總結出了一套更具溫度的落地策略"
  importance: 1
  status: normal
- id: c2
  role: context
  text: UniversalRAG 是 KAIST 團隊提出的多模態 RAG 框架；它不需要一個萬能的向量空間來容納所有資料，而是用一個「指揮中心」Router 來決定去哪裡找資料，整個流程分為 Routing、Targeted Retrieval 與 Generation 三個階段
  source_quotes:
  - "我們得先認識這篇由 KAIST 團隊所提出的作品: UniversalRAG: Retrieval-Augmented Generation over Corpora of Diverse Modalities and Granularities"
  - "我們不需要一個萬能的向量空間來容納所有資料，而是需要一個萬能的指揮中心 (Router) 來決定去哪裡找資料。"
  - "整個流程可以分為三個階段：Routing、Targeted Retrieval 與 Generation。"
  anchor_type: 設計參數
  importance: 2
  status: normal
  figures:
  - file: figures/universal-rag/figure1.png
    article: universal-rag
    src: figure1.png
    caption: UniversalRAG 與傳統 RAG 策略的對比。我們可以看到 UniversalRAG 透過 Router 動態地將查詢引導至最適合的模態與粒度組合。
    sha256: 831b5cca08729e9feb93df9259d11f38cb8f5bcbea52061266ab7fa3c6c559b8
- id: c3
  role: context
  text: 檢索粒度（數據的大小或長度）對生成品質有決定性的影響：太細碎（例如極短的句子）雖然精準，但往往遺漏回答複雜邏輯問題所需的上下文；太粗略（例如為了回答一個 10 秒鐘的動作問題，卻抓取整段兩小時的影片）會引入大量無關雜訊、干擾生成，且極度浪費計算資源；現有的 RAG 系統通常固定在某一種檢索單位，缺乏靈活調整的能力
  source_quotes:
  - "作者精確地指出了目前 RAG 系統在邁向「通用化」道路上所遭遇的三大核心挑戰。"
  - "數據的「大小」或「長度」——也就是檢索粒度 (Granularity) ，對生成品質有著決定性的影響"
  - "太細碎 (Too Fine-grained)：例如檢索一個極短的句子。這雖然精準，但往往會遺漏回答複雜邏輯問題所需的上下文環境 (Context) 。"
  - "太粗略 (Too Coarse-grained)：例如為了回答一個 10 秒鐘的動作問題，卻抓取了整段兩小時的影片。這會引入大量無關雜訊，干擾模型生成，且極度浪費計算資源。"
  - "現有的 RAG 系統通常固定在某一種檢索單位 (如 Paragraph-level) ，缺乏靈活調整的能力。"
  anchor_type: 原作者解讀
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: Router 的 7 個選項是一組 Modality-Granularity Pair：None（直接回答，不需檢索）、Paragraph（文字細粒度）、Document（文字粗粒度，適合多跳推理）、Table（結構化表格）、Image（靜態影像）、Clip（影片細粒度，定位特定動作）、Video（影片粗粒度，理解長時序劇情）；None 以外的六個選項，各對應一個依模態與粒度解耦的索引
  source_quotes:
  - "並從 7 個 Pathways 中選出最佳組合。"
  - "它會從以下這組 Modality-Granularity Pair 中挑選："
  - "None: 直接回答，不需檢索。"
  - "Paragraph: 文字 - 細粒度。"
  - "Document: 文字 - 粗粒度。"
  - "Table: 結構化表格。"
  - "Image: 靜態影像。"
  - "Clip: 影片 - 細粒度。"
  - "Video: 影片 - 粗粒度。"
  - "文字模態：分為 Paragraph (段落級) 與 Document (文件級，適合多跳推理) 。"
  - "影片模態：分為 Clip (短片段，定位特定動作) 與 Video (整部影片，理解長時序劇情) 。"
  - "UniversalRAG 建議將資料庫根據模態與粒度進行「解耦」"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 2
  status: normal
- id: c5
  role: mechanism
  text: 訓練型 Router（Training-based Router）是在有固定硬體資源且追求極速時採用：微調輕量化模型，例如 Qwen3-VL-2B
  source_quotes:
  - "當我們有固定的硬體資源且追求極速時，會採用微調 (Fine-tuning) 輕量化模型 (如 Qwen3-VL-2B) 的做法。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 3
  status: normal
- id: c6
  role: mechanism
  text: 因為現實數據缺乏標籤，作者利用 Inductive Bias 自動生成訓練標籤，例如來自 WebQA 的問題自動標記為 Paragraph+Image
  source_quotes:
  - "自動標籤生成：因為現實數據缺乏標籤，作者利用了 Inductive Bias。例如，來自 WebQA 的問題自動標記為 Paragraph+Image。"
  anchor_type: 設計參數
  importance: 4
  status: normal
- id: c7
  role: mechanism
  text: 訓練型 Router 把路由當成多標籤分類問題：對模型輸出的每個類別的邏輯值做 Sigmoid 轉換得到機率，用二元交叉熵（Binary Cross-Entropy）計算總損失；推論時只要某類別的機率超過閾值 τ = 0.8，該路徑就會被啟動
  source_quotes:
  - "這是一個多標籤分類問題。我們對模型輸出的每個類別 \\( i \\) 的邏輯值 \\( z_i \\) 進行 Sigmoid 轉換得到機率 \\( \\hat{y}_i \\)"
  - "接著使用 二元交叉熵 (Binary Cross-Entropy) 來計算總損失"
  - "在推論時，只要機率超過閾值 \\(\\tau = 0.8\\)，該路徑就會被啟動。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 3
  status: normal
- id: c8
  role: mechanism
  text: 免訓練型 Router（Training-free Router）直接透過 Prompt Engineering 讓強大的 LLM 進行路由決策；blog 認為這對企業私有數據（OOD）特別有效
  source_quotes:
  - "這對於我們討論過的企業私有數據 (OOD) 特別有效。我們直接透過 Prompt Engineering 讓強大的 LLM"
  - "進行決策。"
  - "初期 (冷啟動)：採用「免訓練路由器 (Prompt-based) 」"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c9
  role: mechanism
  text: 免訓練型 Router 的 Prompt 設計邏輯在於「意圖識別」：問題涉及「比較、加總、數值」就引導至 Table，涉及「外觀、顏色、結構」就引導至 Image，並透過 Few-shot 範例教會模型處理複雜意圖（例如 Paragraph+Clip）
  source_quotes:
  - "這個 Prompt 的設計邏輯在於 「意圖識別」："
  - "如果問題涉及「比較、加總、數值」，引導至 Table。"
  - "如果涉及「外觀、顏色、結構」，引導至 Image。"
  - "透過 Few-shot 範例教會模型處理複雜意圖 (例如：Paragraph+Clip) 。"
  anchor_type: 設計參數
  importance: 4
  status: normal
  figures:
  - file: figures/universal-rag/figure8.png
    article: universal-rag
    src: figure8.png
    caption: 論文中設計的 Prompt Template。它透過對比式的範例教導 LLM 區分『段落』與『文件』，以及如何使用『+』號組合多個模態。
    sha256: c95cc08e8c5e64f2f05f714354b2e71cb7f21d3e21856210f220d7c2f55bde7b
- id: c10
  role: mechanism
  text: Router 決定路徑（例如 Paragraph+Image）後，系統同時去對應的庫（如文字段落庫和影像庫）並行檢索最相關的 Top-K 證據，把找回來的文字碎片與影像特徵同時餵給多模態大模型（LVLM），由它根據多模態證據綜合推理、給出最終答案
  source_quotes:
  - "一旦 Router 決定了路徑 (例如：Paragraph+Image) ，系統會："
  - "並行檢索：同時去文字段落庫和影像庫中搜尋最相關的 Top-K 證據。"
  - "證據整合：將找回來的文字碎片與影像特徵同時餵給多模態大模型 (LVLM) 。"
  - "生成回答：模型根據多模態證據進行綜合推理，給出最終答案。"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c11
  role: evaluation
  text: blog 的實務觀察：在企業私有數據場景中，Table（結構化）與 Text（非結構化）的界線往往很模糊；如果不能明確區分數據類型、並針對性地選擇檢索粒度，就會陷入「檢索回來的資料牛頭不對馬嘴」或「檢索速度慢到無法使用」的泥沼
  source_quotes:
  - "在企業私有數據場景中，Table (結構化) 與 Text (非結構化) 的界線往往很模糊。如果我們不能明確地區分數據類型，並針對性地選擇檢索粒度，就會陷入「檢索回來的資料牛頭不對馬嘴」或「檢索速度慢到無法使用」的泥沼。"
  anchor_type: 部落格判斷
  importance: 5
  status: normal
- id: c12
  role: evaluation
  text: blog 對企業實作的建議：在初期資料標籤不足時，可以先採用混合檢索（Hybrid Search），並把 Router 的閾值調低（例如設為 0.5），讓系統進入「多路檢索」狀態以確保召回率
  source_quotes:
  - "在初期資料標籤不足時，可以先採用 Hybrid Search (混合檢索)，並調低 Router 的閾值 (例如設為 0.5) ，讓系統進入「多路檢索」狀態以確保召回率。"
  - "在推論時，只要機率超過閾值 \\(\\tau = 0.8\\)，該路徑就會被啟動。"
  anchor_type: 部落格判斷
  comparison_target: 論文訓練型 Router 的閾值 τ = 0.8
  importance: 4
  status: pending_author_confirmation
- id: c13
  role: evaluation
  text: blog 針對企業私有數據總結的三階段落地策略：初期（冷啟動）採用免訓練路由器（Prompt-based）並結合混合檢索，確保系統的穩定性與召回率；中期（積累期）利用 Teacher LLM 對真實的 User Logs 進行自動化標記，區分出 Table、Text 與 Image 的使用邊界；後期（優化期）訓練專屬於企業環境的輕量化路由器
  source_quotes:
  - "初期 (冷啟動)：採用「免訓練路由器 (Prompt-based) 」並結合「混合檢索 (Hybrid Search) 」，確保系統的穩定性與召回率。"
  - "中期 (積累期)：利用 Teacher LLM 對真實的 User Logs 進行自動化標記，區分出 Table、Text 與 Image 的使用邊界。"
  - "後期 (優化期)：訓練專屬於企業環境的輕量化路由器，實現真正的「UniversalRAG」形態。"
  qualifiers:
  - text: 這套策略是 blog 面對企業內部私有數據總結出來的，不是論文在 Benchmark 上驗證過的做法
    source_quote: "雖然論文在 Benchmark 上表現優異，但面對企業內部的私有數據 (Private Data) ，我們總結出了一套更具溫度的落地策略"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

- 召回率（recall）：所有該被找回的相關資料中，實際被找回的比例。
- Sigmoid：把任意實數壓到 0 到 1 之間的函數，常用來把模型輸出轉成機率。
- 二元交叉熵（Binary Cross-Entropy）：衡量預測機率與 0／1 真值標籤差距的損失函數；多標籤分類時每個類別各算一次。
- Top-K：依相關度排序後取前 K 筆。
- OOD（out-of-distribution）：與模型訓練資料分布不同的資料。
