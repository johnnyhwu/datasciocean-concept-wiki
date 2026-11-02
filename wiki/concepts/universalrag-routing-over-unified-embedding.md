---
id: universalrag-routing-over-unified-embedding
title: 與其強行把所有模態對齊到同一個向量空間，不如先用 Router 在語意層級決定去哪個庫查，讓每種數據在自己最擅長的索引空間裡被檢索
type_hint: 方法
context_type: bound_to_source
sources:
- article: universal-rag
  article_title: "UniversalRAG 深度解析：破解多模態 RAG 偏見，提升異質數據的檢索能力"
  url: https://datasciocean.com/paper-intro/universal-rag/
  sections:
  - 前言
  - Modality Limitation
  - Modality Gap in Embedding Space
  - Efficiency & Scalability
  - 方法介紹：UniversalRAG 的核心架構
  - 模態與粒度的階層化組織
  - 為什麼這套方法有效？
  - 實驗結果
  - 全方位的性能領先
  - 成功跨越 Modality Gap
  - Scalability
  - Routing 是解決模態鴻溝的銀彈
  - 效率與準確度的雙贏
  first_appearance: true
parent: null
related:
  - universalrag-router-design-and-rollout
  - retrieval-reasoning-decoupling
  - rag-narrow-waist
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: UniversalRAG 的核心思維是：與其強行將所有模態對齊到同一個混亂的向量空間，不如建立一個聰明的 Router，實現「先診斷、後抓藥」的精準檢索；它成功的關鍵在於解耦，不追求一個萬能的向量空間，而是讓每種數據在自己最擅長的索引空間裡被檢索
  source_quotes:
  - "UniversalRAG 的核心思維是: 與其強行將所有模態對齊到同一個混亂的向量空間，不如建立一個聰明的「Router  (Router) 」，實現「先診斷、後抓藥」的精準檢索。"
  - "UniversalRAG 成功的關鍵在於 「解耦 (Decoupling) 」。它不追求一個萬能的向量空間，而是追求一個萬能的「指揮中心 (Router) 」，讓每種數據在自己最擅長的索引空間裡被檢索。"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
  figures:
  - file: figures/universal-rag/figure1.png
    article: universal-rag
    src: figure1.png
    caption: UniversalRAG 與傳統 RAG 策略的對比。我們可以看到 UniversalRAG 透過 Router 動態地將查詢引導至最適合的模態與粒度組合。
    sha256: 831b5cca08729e9feb93df9259d11f38cb8f5bcbea52061266ab7fa3c6c559b8
- id: c2
  role: context
  text: UniversalRAG 是 KAIST 團隊提出的 RAG 框架，處理的是由不同模態（文字、表格、圖片、影片）與不同粒度組成的語料庫；它把檢索過程從「單一空間搜尋」轉變為「動態路徑選擇」，整個流程分為 Routing、Targeted Retrieval 與 Generation 三個階段
  source_quotes:
  - "我們得先認識這篇由 KAIST 團隊所提出的作品: UniversalRAG: Retrieval-Augmented Generation over Corpora of Diverse Modalities and Granularities"
  - "UniversalRAG 的設計核心在於將檢索過程從「單一空間搜尋」轉變為「動態路徑選擇」。整個流程可以分為三個階段：Routing、Targeted Retrieval 與 Generation。"
  - "文字模態"
  - "表格模態"
  - "影像模態"
  - "影片模態"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: 大多數傳統的 RAG 系統僅限於純文本檢索；近期有些研究延伸到影像或影片，但通常僅操作於單一模態的特定語料庫，因此無法回答需要「跨模態證據」的問題
  source_quotes:
  - "大多數傳統的 RAG 系統僅限於純文本檢索。雖然近期有些研究延伸到了影像或影片，但它們通常僅操作於單一模態的特定語料庫。"
  - "如果系統只能處理單一模態，就無法回答那些需要「跨模態證據」的問題。"
  anchor_type: 背景說明
  importance: 4
  status: normal
- id: c4
  role: mechanism
  text: 最直觀的多模態做法，是用 CLIP 這樣的多模態編碼器把文字、圖片和影片全部映射到同一個向量空間（Unified Embedding Space）做相似度檢索，但這會導致嚴重的模態偏見：資料點傾向於根據「模態」而非「語意」聚集，文字查詢與文字資料的距離，往往比它與語意更相關的影像資料還要近；blog 把這種檢索偏見稱為 Modality Gap
  source_quotes:
  - "最直觀的方法是使用如 CLIP 這樣的多模態編碼器，將文字、圖片和影片全部映射到同一個向量空間進行相似度檢索 (Unified Embedding Space) 。然而，這會導致嚴重的模態偏見。"
  - "在向量空間中，資料點傾向於根據「模態」而非「語意」進行聚集。這意味著文字查詢與文字資料的距離，往往比它與語意更相關的影像資料還要近。"
  - "如何透過 Modality-aware Routing 避開檢索偏見 (Modality Gap)"
  anchor_type: 原作者解讀
  importance: 3
  status: normal
  figures:
  - file: figures/universal-rag/figure2.png
    article: universal-rag
    src: figure2.png
    caption: 統一嵌入空間的 t-SNE 可視化圖。我們可以看到不同模態 (文字、影像、影片) 形成了明顯的分離簇，這就是所謂的 Modality Gap，它會導致檢索時的偏向性。
    sha256: 4dfd03eba39cbcc3f02f13e0d1168e8e8310061aa810e944d3653a538f4e52e7
- id: c5
  role: mechanism
  text: 模態偏見的後果：輸入一個文字問題時，系統會因為模態相近而優先抓取文字內容，即便最正確的答案其實藏在圖片或影片裡
  source_quotes:
  - "當我們輸入一個文字問題時，系統會因為模態相近而優先抓取文字內容，即便最正確的答案其實藏在圖片或影片裡。"
  anchor_type: 原作者解讀
  importance: 4
  status: normal
- id: c6
  role: mechanism
  text: UniversalRAG 把資料庫根據模態與粒度「解耦」成多個索引（文字分段落級與文件級、獨立的表格索引、影像索引、影片分短片段與整部影片），確保每個資料庫都能使用最適合該模態的編碼器，避開強行對齊產生的模態鴻溝
  source_quotes:
  - "UniversalRAG 建議將資料庫根據模態與粒度進行「解耦」"
  - "文字模態：分為 Paragraph (段落級) 與 Document (文件級，適合多跳推理) 。"
  - "表格模態：獨立的 Table 索引，專門處理結構化數據。"
  - "影像模態：Image 索引，保留原始視覺特徵。"
  - "影片模態：分為 Clip (短片段，定位特定動作) 與 Video (整部影片，理解長時序劇情) 。"
  - "這樣的組織方式確保了每個資料庫都能使用最適合該模態的編碼器 (Encoder) ，避開了強行對齊產生的模態鴻溝。"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c7
  role: mechanism
  text: blog 認為這套方法有效，是因為路由機制是在「語義層級」做決策：過去把問題和圖片放在一起算相似度，文字問題天生就比較親近文字資料；當 Router 說「這題要看圖」，系統就只會去影像庫裡搜尋，徹底切斷了模態之間的互相干擾
  source_quotes:
  - "UniversalRAG 的優雅之處在於它解決了「模態偏見」。"
  - "過去的方法是把問題和圖片放在一起算相似度，但文字問題天生就比較親近文字資料。而 UniversalRAG 的路由機制是在 「語義層級」 做決策。當 Router 說「這題要看圖」，系統就只會去影像庫裡搜尋，徹底切斷了模態之間的互相干擾。"
  anchor_type: 部落格推論
  importance: 3
  status: normal
- id: c8
  role: evidence
  text: 實驗顯示，像 GME 或 VLM2Vec 這類將所有模態擠在一起的模型，在檢索時表現出極強的「文字偏見」：即便問題需要影像或影片證據，它們仍傾向於抓取文字；UniversalRAG 的路由器則能根據問題意圖分配檢索路徑
  source_quotes:
  - "像 GME 或 VLM2Vec 這類將所有模態擠在一起的模型，在檢索時表現出極強的「文字偏見」——即便問題需要影像或影片證據，它們仍傾向於抓取文字。"
  - "UniversalRAG 的路由器能精準地根據問題意圖分配檢索路徑。"
  anchor_type: 實驗結果
  importance: 2
  status: normal
  figures:
  - file: figures/universal-rag/figure4.png
    article: universal-rag
    src: figure4.png
    caption: 模態選擇分布圖。我們可以看到 Unified Embedding 方法嚴重偏向文字，而 UniversalRAG (最右側) 能根據需求平衡地選擇影像與影片模態。
    sha256: e568b5f73c1eda187ac94abbf113b421e9df2f51741b12eff06c9128e2e0f26e
- id: c9
  role: evaluation
  text: blog 認為這個模態選擇的對比證明了「先路由、再檢索」能有效繞過模態鴻溝，讓正確的證據被召回
  source_quotes:
  - "這證明了 「先路由、再檢索」 能有效繞過模態鴻溝，讓正確的證據被召回。"
  anchor_type: 部落格判斷
  importance: 5
  status: normal
  figures:
  - file: figures/universal-rag/figure4.png
    article: universal-rag
    src: figure4.png
    caption: 模態選擇分布圖。我們可以看到 Unified Embedding 方法嚴重偏向文字，而 UniversalRAG (最右側) 能根據需求平衡地選擇影像與影片模態。
    sha256: e568b5f73c1eda187ac94abbf113b421e9df2f51741b12eff06c9128e2e0f26e
- id: c10
  role: evidence
  text: 作者在 10 個涵蓋不同模態與粒度的基準測試上評估；blog 的描述是，無論是單純的文字查詢、圖文結合，還是複雜的影片分析，UniversalRAG 的表現都顯著優於單一模態的 RAG 以及傳統的統一嵌入空間方法
  source_quotes:
  - "作者在 10 個涵蓋不同模態與粒度的基準測試 (Benchmarks) 上進行了廣泛評估。"
  - "無論是單純的文字查詢、圖文結合，還是複雜的影片分析，UniversalRAG 的表現都顯著優於單一模態的 RAG 以及傳統的統一嵌入空間方法。"
  anchor_type: 實驗結果
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 4
  status: pending_author_confirmation
  figures:
  - file: figures/universal-rag/table1.png
    article: universal-rag
    src: table1.png
    caption: Table 1 展示了 UniversalRAG 在 10 個不同數據集上的表現。無論是使用訓練型還是免訓練型路由器，UniversalRAG 幾乎在所有指標上都優於基基準模型 (Baselines) 。
    sha256: 0ecae6a7dc7066ed571174fb98ab1a653340a96d8f08eb3f8b6314da025037c4
- id: c11
  role: context
  text: 效率也是問題：試圖建立一個包含所有模態、所有粒度的「超級索引庫」時，檢索延遲會隨資料量 N 的增加而增長，在處理千萬級別以上的企業數據時，搜尋成本與速度將成為不可忽視的負擔
  source_quotes:
  - "當我們試圖建立一個包含所有模態、所有粒度的「超級索引庫」時，檢索延遲會隨著資料量 \\(N\\) 的增加而線性或對數增長。在處理千萬級別以上的企業數據時，搜尋成本與速度將成為不可忽視的負擔。"
  anchor_type: 原作者解讀
  importance: 5
  status: normal
- id: c12
  role: mechanism
  text: 在 UniversalRAG 中，因為路由器先行過濾掉了無關的庫，實際搜尋的範圍縮小到了 1/k，blog 稱之為子線性（Sub-linear）的延遲
  source_quotes:
  - "Sub-linear Latency：在傳統 RAG 中，隨著資料庫 \\(N\\) 的增加，搜尋時間通常會線性或對數增長。但在 UniversalRAG 中，因為路由器先行過濾掉了無關的庫，實際搜尋的範圍縮小到了 \\(1/k\\)。"
  anchor_type: 原作者解讀
  comparison_target: 傳統 RAG 隨資料庫 N 增加而通常線性或對數增長的搜尋時間
  importance: 3
  status: pending_author_confirmation
  figures:
  - file: figures/universal-rag/figure5.png
    article: universal-rag
    src: figure5.png
    caption: 檢索延遲隨語料庫規模變化的趨勢。可以看到 UniversalRAG 在大規模數據下展現了極佳的擴展性。
    sha256: f0ed8f5ae72455921c06bf383439f0f0c984196f10d712a43ecc96f3446b20b5
- id: c13
  role: evidence
  text: 當資料規模達到千萬（10M）甚至億級時，UniversalRAG 的延遲遠低於統一檢索方法；blog 據此認為路由器的開銷在大規模場景下是完全值得的
  source_quotes:
  - "當資料規模達到千萬 (10M) 甚至億級時，UniversalRAG 的延遲遠低於統一檢索方法。這意味著路由器的開銷在大規模場景下是完全值得的。"
  anchor_type: 實驗結果
  comparison_target: 統一檢索方法
  importance: 3
  status: normal
  figures:
  - file: figures/universal-rag/figure5.png
    article: universal-rag
    src: figure5.png
    caption: 檢索延遲隨語料庫規模變化的趨勢。可以看到 UniversalRAG 在大規模數據下展現了極佳的擴展性。
    sha256: f0ed8f5ae72455921c06bf383439f0f0c984196f10d712a43ecc96f3446b20b5
- id: c14
  role: evaluation
  text: blog 的結論是：透過「先診斷、後抓藥」的策略，增加一個輕量級的路由器不僅不會拖慢系統，反而能在大規模語料庫下實現「子線性」的延遲增長，為工業界部署超大規模 RAG 系統提供了實質的信心
  source_quotes:
  - "UniversalRAG 透過「先診斷、後抓藥」的策略，證明了增加一個輕量級的路由器"
  - "不僅不會拖慢系統，反而能在大規模語料庫下實現「子線性」的延遲增長。這為我們在工業界部署超大規模 RAG 系統提供了實質的信心。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: blog 說的延遲優勢，是指資料規模達到千萬（10M）甚至億級時的情況
    source_quote: "當資料規模達到千萬 (10M) 甚至億級時，UniversalRAG 的延遲遠低於統一檢索方法。"
  importance: 4
  status: pending_author_confirmation
- id: c15
  role: evaluation
  text: blog 的結論是：強行對齊會帶來偏見；透過在語意層級進行路由，讓每種數據保留其最原始、最專精的表示方式，反而能獲得更公平、更準確的檢索結果，這種解耦的思想是解決複雜多模態問題的關鍵
  source_quotes:
  - "但 UniversalRAG 告訴我們：強行對齊會帶來偏見。透過在語意層級進行路由，讓每種數據保留其最原始、最專精的表示方式，反而能獲得更公平、更準確的檢索結果。這種「解耦 (Decoupling) 」的思想，是解決複雜多模態問題的關鍵。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c16
  role: evaluation
  text: blog 指出同樣的解耦哲學也出現在 MRAG 將時間推理與語意檢索解耦的做法中，只是套用在不同的異質性維度上
  source_quotes:
  - "同樣的哲學也出現在 MRAG 將時間推理與語意檢索解耦的做法中，只是套用在不同的異質性維度上。"
  anchor_type: 部落格判斷
  importance: 6
  status: normal
```
