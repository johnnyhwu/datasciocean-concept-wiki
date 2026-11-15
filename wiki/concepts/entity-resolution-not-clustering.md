---
id: entity-resolution-not-clustering
title: 去重（entity resolution）不是分群（clustering）：兩者在有無標準答案、群數與群大小、錯誤可否回復上都不同；用 DBSCAN 去重不是必要的，「門檻加 union-find」能做到同樣的事，而且更好調、更好 debug
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: ragu
  article_title: "RAGU：一篇替 GraphRAG 量出天花板的論文"
  url: https://datasciocean.com/paper-intro/ragu/
  sections:
  - 前言
  - GraphRAG 在解什麼問題
  - Step 3：consolidation，論文的核心賣點
  - 觀念一：去重不是分群
  first_appearance: true
parent: null
related:
  - ragu-results-peeling-confounds
  - retrieval-recall-not-answer-quality
  - graph-vs-vector-clustering-modularity
  - small-extractor-saturation-not-scale
  - ragu-pipeline-two-stage-extraction-consolidation
  - sag-tradeoffs-price-paid
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 去重（entity resolution）跟分群（clustering）其實是兩種性質不同的任務；blog 對 RAGU 的評價是，DBSCAN 在這裡不是必要的，「門檻加 union-find」能做到同樣的事，而且更好調、更好 debug
  source_quotes:
  - "RAGU 用 DBSCAN 做去重看起來理所當然，但去重（entity resolution）跟分群（clustering）其實是兩種性質不同的任務："
  - "所以對 RAGU 的評價是：DBSCAN 在這裡不是必要的，「門檻加 union-find」能做到同樣的事，而且更好調、更好 debug。"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: RAGU 是 ITMO University 團隊的 GraphRAG 引擎（先請 LLM 把文件裡的實體跟關係抽出來建成知識圖）；它的核心賣點 consolidation 的論文描述只有三句話：EntitySummarizer 按 (name, type) 分組，對重複提及很多的實體套用 DBSCAN 分群加上 LLM 摘要，RelationSummarizer 比照辦理；abstract 稱之為 DBSCAN-backed deduplication
  source_quotes:
  - "RAGU 是 ITMO University 團隊在 2026 年 7 月[放上 arXiv](https://arxiv.org/abs/2607.11683)的 GraphRAG 引擎"
  - "GraphRAG 的解法是先請 LLM 把文件裡的實體（人、組織、產品）跟關係抽出來建成知識圖"
  - "論文對這一步的全部描述只有三句話：EntitySummarizer 按 (name, type) 分組，對重複提及很多的實體套用 DBSCAN 分群加上 LLM 摘要，RelationSummarizer 比照辦理。abstract 則稱之為 DBSCAN-backed deduplication。"
  qualifiers:
  - text: 論文敘述前後不一致：abstract 說 DBSCAN 用於跨名字去重，方法段讀起來卻像是先用 (name, type) 分好組、再在同一組內部做 DBSCAN，後者根本無法合併別名
    source_quote: "abstract 說 DBSCAN 用於跨名字去重，方法段讀起來卻像是先用 (name, type) 分好組、再在同一組內部做 DBSCAN。後者根本無法合併別名。"
  - text: blog 說論文的文字本身無法判定是哪一種，要確認只能翻原始碼
    source_quote: "論文的文字本身無法判定，要確認只能翻原始碼。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: 抽取出來的東西是「提及（mention）」，不是節點：同一個真實世界的實體，在不同 chunk 裡會各自產生獨立的 mention；blog 的例子是 9 個 chunk 產生的 9 筆 mention，直接建圖會得到 9 個節點，正確答案是 3 個
  source_quotes:
  - "要理解它在幹嘛，得先知道抽取出來的東西是「提及（mention）」，不是節點。同一個真實世界的實體，在 9 個 chunk 裡會產生 9 筆各自獨立的 mention："
  - "直接建圖會得到 9 個節點，正確答案是 3 個。"
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 3
  status: normal
- id: c4
  role: context
  text: DBSCAN 的規則是：在半徑 eps 內至少有 min_samples 個鄰居的點算核心點，核心點跟鄰居連成一群，連不上任何群的點標成 noise
  source_quotes:
  - "DBSCAN 的規則是，在半徑 `eps` 內至少有 `min_samples` 個鄰居的點算核心點，核心點跟鄰居連成一群，連不上任何群的點標成 noise。"
  anchor_type: 背景說明
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 分群沒有標準答案，分 3 群或 5 群都可能對，取決於用途，本質是無監督的結構發現；去重有標準答案（Bell Labs 跟 Bell Laboratories 就是同一個），本質是對每組 pair 做二元判斷：同一個？是／否
  source_quotes:
  - "有標準答案嗎 | 沒有。分 3 群或 5 群都可能對，取決於用途 | 有。\"Bell Labs\" 跟 \"Bell Laboratories\" 就是同一個"
  - "任務本質 | 無監督的結構發現 | 對每組 pair 做二元判斷：同一個？是/否"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 5
  status: normal
- id: c6
  role: mechanism
  text: blog 認為最關鍵的是群數跟群大小：分群是 k << n（1000 個客戶分 5 群）、群大，幾十到幾千；去重是 k ≈ n（10 萬個 mention 可能有 7 萬個實體）、群極小，多半 1～5；所有幾何式分群演算法的設計前提都是「少數幾個大群」，靠的是密度或距離的全域結構，而去重的真實結構是「幾萬個大小 1 到 3 的微群」，那個空間裡根本沒有全域結構可言
  source_quotes:
  - "群數相對於資料量 | k << n（1000 個客戶分 5 群） | k ≈ n（10 萬個 mention 可能有 7 萬個實體）"
  - "群的大小 | 大，幾十到幾千 | 極小，多半 1～5"
  - "最關鍵的是群數跟群大小那兩列。所有幾何式分群演算法的設計前提都是「少數幾個大群」，靠的是密度或距離的全域結構；而去重的真實結構是「幾萬個大小 1 到 3 的微群」，那個空間裡根本沒有全域結構可言。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: 分群只能用 silhouette 之類的代理指標評估，錯了換個分法重跑就好；去重可標註 pair，直接算 precision / recall，但誤合併不可逆，錯誤會傳到下游
  source_quotes:
  - "能不能評估 | 只能用 silhouette 之類的代理指標 | 可標註 pair，直接算 precision / recall"
  - "錯了的後果 | 換個分法重跑就好 | 誤合併不可逆，錯誤會傳到下游"
  anchor_type: 部落格判斷
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: 幾何式演算法在去重會退化：一個實體可能只有 2 個 mention，所以 min_samples 必須設到 2；而 min_samples=2 的 DBSCAN，數學上等價於「相似度門檻加上 connected components（union-find）」，也就是在去重所需的參數設定下，DBSCAN 會自動塌陷成 union-find，只是多背了一個難調的 eps
  source_quotes:
  - "**幾何式演算法在這裡會退化。** 去重時一個實體可能只有 2 個 mention，所以 `min_samples` 必須設到 2。而 `min_samples=2` 的 DBSCAN，數學上等價於「相似度門檻加上 connected components（union-find）」。也就是說，在去重所需的參數設定下，DBSCAN 會自動塌陷成 union-find，只是多背了一個難調的 `eps`。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 8
  status: normal
- id: c9
  role: mechanism
  text: 去重可以用「嵌不進向量空間」的訊號：型別必須相同（PERSON 絕不併 ORGANIZATION）是硬規則；還有編輯距離、縮寫展開（Bell Labs → Bell Laboratories）、有沒有共用 ID、URL、電話；特別重要的是，兩個名字出現在同一個 chunk 裡，幾乎確定是兩個不同實體，但在 embedding 空間裡它們反而更近，這個負向證據向量距離完全看不到
  source_quotes:
  - "**去重可以用「嵌不進向量空間」的訊號。** 分群演算法只能看向量距離，但去重最有用的訊號常常不是幾何的：型別必須相同（PERSON 絕不併 ORGANIZATION）是硬規則；編輯距離、縮寫展開（Bell Labs → Bell Laboratories）；有沒有共用 ID、URL、電話。最後還有一條特別重要——**兩個名字出現在同一個 chunk 裡，幾乎確定是兩個不同實體**，但在 embedding 空間裡它們反而更近。這個負向證據，向量距離完全看不到。"
  anchor_type: 部落格判斷
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: 錯誤代價不對稱：誤合併遠比漏合併嚴重，漏了頂多資訊分散，合錯了是事實層面的錯誤而且很難察覺；pairwise 框架可以直接把門檻調得保守一點，clustering 的參數（k、eps）跟這個代價沒有直接對應
  source_quotes:
  - "**錯誤代價不對稱。** 誤合併遠比漏合併嚴重：漏了頂多資訊分散，合錯了是事實層面的錯誤而且很難察覺。pairwise 框架可以直接把門檻調得保守一點，clustering 的參數（k、eps）跟這個代價沒有直接對應。"
  anchor_type: 部落格判斷
  importance: 10
  status: normal
- id: c11
  role: mechanism
  text: 實務上的標準去重流程整條都不是 clustering：先 Blocking，用便宜方式縮小候選對（同型別、首字母相同、BM25 top-k）；再對候選對算相似度（embedding cosine 或 fuzzy string）；相似度大於門檻就連一條邊；最後取 connected components（union-find），每個連通塊就是一個實體
  source_quotes:
  - "實務上的標準去重流程長這樣，注意它整條都不是 clustering："
  - "1. Blocking：用便宜方式縮小候選對（同型別、首字母相同、BM25 top-k）"
  - "2. 對候選對算相似度（embedding cosine 或 fuzzy string）"
  - "3. 相似度 > 門檻 → 連一條邊"
  - "4. 取 connected components（union-find）→ 每個連通塊 = 一個實體"
  anchor_type: 背景說明
  importance: 11
  status: normal
- id: c12
  role: qualifier
  text: 這個流程唯一的坑是鏈式蔓延：A≈B、B≈C，但 A 跟 C 完全不像，仍然會被併成一群；DBSCAN 也逃不掉，它的 density-reachable 本質上就是帶密度條件的 connected components
  source_quotes:
  - "唯一的坑是鏈式蔓延：A≈B、B≈C，但 A 跟 C 完全不像，仍然會被併成一群。（DBSCAN 也逃不掉，它的 density-reachable 本質上就是帶密度條件的 connected components。）"
  anchor_type: 部落格判斷
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: blog 認為選 DBSCAN 讓 abstract 好看（DBSCAN-backed deduplication 聽起來就是比 threshold-based merging 學術），但技術上沒有非它不可的理由
  source_quotes:
  - "選 DBSCAN 讓 abstract 好看（DBSCAN-backed deduplication 聽起來就是比 threshold-based merging 學術），但技術上沒有非它不可的理由。"
  anchor_type: 部落格判斷
  importance: 13
  status: normal
- id: c14
  role: evidence
  text: blog 指出 RAGU 這個 DBSCAN 去重機制最脆弱的地方，正好說明誤合併的風險：Alistair E. Ritchie 是 Dennis Ritchie 的父親，兩人的名字字串高度相似、描述也都跟貝爾實驗室有關，eps 稍微放寬，父子就被合併成同一個節點，而且下游沒有任何機制救得回來
  source_quotes:
  - "這個機制最脆弱的地方是 Alistair E. Ritchie，Dennis 的父親。兩人的名字字串高度相似、描述也都跟貝爾實驗室有關，`eps` 稍微放寬，父子就被合併成同一個節點，而且下游沒有任何機制救得回來。"
  qualifiers:
  - text: 論文敘述前後不一致：abstract 說 DBSCAN 用於跨名字去重，方法段讀起來卻像是先用 (name, type) 分好組、再在同一組內部做 DBSCAN，後者根本無法合併別名
    source_quote: "abstract 說 DBSCAN 用於跨名字去重，方法段讀起來卻像是先用 (name, type) 分好組、再在同一組內部做 DBSCAN。後者根本無法合併別名。"
  - text: blog 說論文的文字本身無法判定是哪一種，要確認只能翻原始碼
    source_quote: "論文的文字本身無法判定，要確認只能翻原始碼。"
  anchor_type: 部落格推論
  importance: 14
  status: normal
- id: c15
  role: evidence
  text: blog 的實務建議：想用 DBSCAN 的時候，先試 HDBSCAN；它是 DBSCAN 的階層式改良版，把 eps 這個參數拿掉（改成掃過所有 eps 值再挑最穩定的分群），只留 min_cluster_size；DBSCAN 最痛的兩點——eps 難調、資料密度不均時整組分群失效——它大致都解決了
  source_quotes:
  - "順帶附上一條實務建議：想用 DBSCAN 的時候，先試 HDBSCAN。它是 DBSCAN 的階層式改良版，把 `eps` 這個參數拿掉了（改成掃過所有 eps 值再挑最穩定的分群），只留 `min_cluster_size`，語意直觀很多。DBSCAN 最痛的兩點——`eps` 難調、資料密度不均時整組分群失效——它大致都解決了。"
  anchor_type: 部落格判斷
  importance: 15
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

- precision / recall：precision（精確率）是判為「同一個」的配對中真的是同一個的比例；recall（召回率）是真的是同一個的配對中被找出來的比例。
- connected components / union-find：把有邊相連的點歸成同一個連通塊；union-find 是計算連通塊的常用資料結構，反覆把相連的兩點所在集合合併。
- silhouette：分群品質的代理指標，比較每個點跟自己群內的距離與跟最近他群的距離。
- 編輯距離：把一個字串改成另一個字串最少要幾次插入、刪除或替換。
- BM25：經典的關鍵字檢索排序函數。
