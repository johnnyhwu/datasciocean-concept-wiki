---
id: graph-vs-vector-clustering-modularity
title: 圖分群跟向量分群是兩種不同的「像」：向量分群看語意相似、給你「分類」，圖分群（Leiden 最大化 modularity）看結構相關、給你「主題」；社群內部語意差很多是設計目的，不是缺陷
type_hint: 方法
context_type: standalone_classic
sources:
- article: ragu
  article_title: "RAGU：一篇替 GraphRAG 量出天花板的論文"
  url: https://datasciocean.com/paper-intro/ragu/
  sections:
  - 前言
  - GraphRAG 在解什麼問題
  - Step 2：兩階段抽取，把生成變成選擇題
  - Step 3：consolidation，論文的核心賣點
  - 觀念二：圖分群跟向量分群，是兩種不同的「像」
  - 第二層：NaiveRAG 才是照妖鏡
  first_appearance: true
parent: null
related:
  - ragu-results-peeling-confounds
  - retrieval-recall-not-answer-quality
  - entity-resolution-not-clustering
  - small-extractor-saturation-not-scale
  - ragu-pipeline-two-stage-extraction-consolidation
  - sag-latent-hyperedge-one-hop
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 社群偵測就是分群，只是輸入是圖而不是向量，差別在用什麼定義「像」：向量分群（k-means / DBSCAN）的「像」是向量距離近（語意相似），會分到一起的是同類的東西；圖分群（Leiden）的「像」是連得多（結構相關），會分到一起的是有關係的東西；向量分群給你「分類」，圖分群給你「主題」
  source_quotes:
  - "社群偵測就是分群，只是輸入是圖而不是向量。差別在用什麼定義「像」："
  - "| 向量分群（k-means / DBSCAN） | 圖分群（Leiden）"
  - "「像」的定義 | 向量距離近（語意相似） | 連得多（結構相關）"
  - "會分到一起的 | 同類的東西 | 有關係的東西"
  - "向量分群給你「分類」，圖分群給你「主題」。"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: 這個觀念出自 blog 對 RAGU（ITMO University 團隊的 GraphRAG 引擎）的解析；GraphRAG 先請 LLM 把文件裡的實體跟關係抽出來建成知識圖，RAGU 在建圖後的社群偵測步驟用的是 Hierarchical Leiden，這部分跟 Microsoft GraphRAG 相同
  source_quotes:
  - "RAGU 是 ITMO University 團隊在 2026 年 7 月[放上 arXiv](https://arxiv.org/abs/2607.11683)的 GraphRAG 引擎"
  - "GraphRAG 的解法是先請 LLM 把文件裡的實體（人、組織、產品）跟關係抽出來建成知識圖"
  - "Step 5 的社群偵測用的是 Hierarchical Leiden，這部分跟 Microsoft GraphRAG 相同。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: Leiden 的目標函數叫 modularity（模組度，記作 Q），白話講就是：這一群內部的邊，比隨機亂連的情況多出多少？
  source_quotes:
  - "它的目標函數叫 **modularity（模組度，記作 Q）**，白話講就是："
  - "這一群內部的邊，比隨機亂連的情況多出多少？"
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 要跟隨機比，是因為光看「內部邊很多」會被高連接度的節點騙——一個連了 100 條邊的節點，跟誰都會有很多內部邊；所以要扣掉「純粹因為它度數高、本來就該有的邊數」
  source_quotes:
  - "為什麼要跟隨機比？因為光看「內部邊很多」會被高連接度的節點騙——一個連了 100 條邊的節點，跟誰都會有很多內部邊。所以要扣掉「純粹因為它度數高、本來就該有的邊數」："
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 公式是 Q = Σ_c [ e_c/m − (d_c / 2m)^2 ]，m 是全圖總邊數、e_c 是社群 c 內部的邊數、d_c 是社群 c 裡所有節點的度數總和；前項是實際觀察到的內部邊比例，後項是隨機連線下的期望內部邊比例；後項的平方是因為隨機連一條邊時，一端落在社群 c 的機率是度數佔比 d_c/2m，兩端都落在 c 就是平方
  source_quotes:
  - "Q = Σ_c [ e_c/m  −  (d_c / 2m)^2 ]"
  - "m   = 全圖總邊數"
  - "e_c = 社群 c 內部的邊數"
  - "d_c = 社群 c 裡所有節點的度數總和"
  - "前項 = 實際觀察到的內部邊比例"
  - "後項 = 隨機連線下的期望內部邊比例"
  - "後項的平方是這樣來的：隨機連一條邊時，一端落在社群 c 的機率是度數佔比 `d_c/2m`，兩端都落在 c 就是平方。"
  anchor_type: 數學推導
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 5
  status: normal
- id: c6
  role: anchor
  text: blog 拿論文自己的 demo 實算：一段關於 Dennis Ritchie 的文字建出的圖，Dennis Ritchie 連向 C 語言、Unix、過世日期 Oct 12, 2011 與 70（過世時的年齡），並經由唯一的橋連到父親 Alistair E. Ritchie，再串成 Alistair → Bell Laboratories → Murray Hill → New Jersey 的鏈；總邊數 m = 8，度數是 Dennis 5、Alistair 2、Bell Labs 2、Murray Hill 2、其餘各 1
  source_quotes:
  - "拿論文自己的 demo 實算一次會更有感。那段 Ritchie 文字建出來的圖是這樣（圖裡的 `70` 是 Ritchie 過世時的年齡，也是抽出來的節點之一）："
  - "C語言   Unix   Oct 12,2011   70"
  - "Dennis Ritchie"
  - "|                  ← 唯一的橋"
  - "Alistair E. Ritchie"
  - "Bell Laboratories"
  - "Murray Hill"
  - "New Jersey"
  - "總邊數 `m = 8`，度數是 Dennis 5、Alistair 2、Bell Labs 2、Murray Hill 2、其餘各 1。"
  - "這個機制最脆弱的地方是 Alistair E. Ritchie，Dennis 的父親。"
  - "Dennis Ritchie | October 12, 2011 | DATE_OF_DEATH"
  anchor_type: 部落格考證
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 6
  status: normal
  figures:
  - file: figures/ragu/figure4.png
    article: ragu
    src: figure4.png
    caption: 圖三 — 從 Ritchie 段落建出的知識圖，Leiden 把它切成兩個社群：Ritchie 的專業成就，以及貝爾實驗室的地理叢集。（來源：原始論文 Figure 4）
    sha256: db78da326fd8b40ea5a07972439a7b20c862f008e2c71cd181290876d43ab6cb
- id: c7
  role: anchor
  text: 實算結果：社群 1 = {Dennis, C 語言, Unix, Oct12, 70}，e_1 = 4、d_1 = 9，貢獻 4/8 − (9/16)^2 = 0.500 − 0.316 = 0.184；社群 2 = {Alistair, Bell Labs, Murray Hill, New Jersey}，e_2 = 3、d_2 = 7，貢獻 3/8 − (7/16)^2 = 0.375 − 0.191 = 0.184；Q = 0.367；對照組全部塞成一群是 8/8 − (16/16)^2 = 0
  source_quotes:
  - "社群 1 = {Dennis, C語言, Unix, Oct12, 70}"
  - "e_1 = 4，d_1 = 9"
  - "4/8 − (9/16)^2 = 0.500 − 0.316 = 0.184"
  - "社群 2 = {Alistair, Bell Labs, Murray Hill, New Jersey}"
  - "e_2 = 3，d_2 = 7"
  - "3/8 − (7/16)^2 = 0.375 − 0.191 = 0.184"
  - "Q = 0.367"
  - "對照組：全部塞成一群"
  - "8/8 − (16/16)^2 = 0"
  comparison_target: 全部塞成一群（Q = 0）
  anchor_type: 數學推導
  importance: 7
  status: normal
  figures:
  - file: figures/ragu/figure4.png
    article: ragu
    src: figure4.png
    caption: 圖三 — 從 Ritchie 段落建出的知識圖，Leiden 把它切成兩個社群：Ritchie 的專業成就，以及貝爾實驗室的地理叢集。（來源：原始論文 Figure 4）
    sha256: db78da326fd8b40ea5a07972439a7b20c862f008e2c71cd181290876d43ab6cb
- id: c8
  role: mechanism
  text: 0.367 大於 0，所以切成兩群比不切好；Alistair 跟 Dennis 之間那條橋被犧牲成跨社群的邊，換來兩邊各自的內聚度，這就是演算法在做的權衡
  source_quotes:
  - "0.367 大於 0，所以切成兩群比不切好。Alistair 跟 Dennis 之間那條橋被犧牲成跨社群的邊，換來兩邊各自的內聚度——這就是演算法在做的權衡。"
  comparison_target: 不切、全部塞成一群（Q = 0）
  anchor_type: 數學推導
  importance: 8
  status: normal
- id: c9
  role: qualifier
  text: Q 的理論上限是 1，實務上 0.3 到 0.7 表示有明顯的社群結構
  source_quotes:
  - "（Q 的理論上限是 1，實務上 0.3 到 0.7 表示有明顯的社群結構。）"
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: Louvain 是貪婪法，反覆做兩件事：把節點移到能讓 Q 增加最多的鄰居社群，然後把每個社群壓縮成超級節點、在更小的圖上再跑一次，後者就是 hierarchical 的來源；Leiden 是 Louvain 的修正版，補上一個 refinement 步驟保證社群內部連通、順便收斂更快
  source_quotes:
  - "演算法本身，Louvain 是貪婪法，反覆做兩件事：把節點移到能讓 Q 增加最多的鄰居社群，然後把每個社群壓縮成超級節點、在更小的圖上再跑一次，後者就是 hierarchical 的來源。Leiden 是 Louvain 的修正版，補上一個 refinement 步驟保證社群內部連通、順便收斂更快"
  anchor_type: 背景說明
  importance: 10
  status: normal
- id: c11
  role: anchor
  text: 同一張 Ritchie 圖用兩種分法：向量分群按語意會得到 {Dennis Ritchie, Alistair E. Ritchie}（都是人）、{C 語言, Unix}（都是軟體）、{Murray Hill, New Jersey}（都是地名）、{Oct 12 2011, 70}（都是數值）；圖分群按結構會得到 {Dennis, C 語言, Unix, Oct12, 70}（都跟 Ritchie 這個主題有關）與 {Alistair, Bell Labs, Murray Hill, NJ}（都跟貝爾實驗室這個地點有關）
  source_quotes:
  - "向量分群的結果（按語意）:"
  - "群 A = {Dennis Ritchie, Alistair E. Ritchie}   ← 都是人"
  - "群 B = {C語言, Unix}                            ← 都是軟體"
  - "群 C = {Murray Hill, New Jersey}                ← 都是地名"
  - "群 D = {Oct 12 2011, 70}                        ← 都是數值"
  - "圖分群的結果（按結構）:"
  - "群 1 = {Dennis, C語言, Unix, Oct12, 70}         ← 都跟 Ritchie 這個主題有關"
  - "群 2 = {Alistair, Bell Labs, Murray Hill, NJ}   ← 都跟貝爾實驗室這個地點有關"
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 11
  status: normal
  figures:
  - file: figures/ragu/figure4.png
    article: ragu
    src: figure4.png
    caption: 圖三 — 從 Ritchie 段落建出的知識圖，Leiden 把它切成兩個社群：Ritchie 的專業成就，以及貝爾實驗室的地理叢集。（來源：原始論文 Figure 4）
    sha256: db78da326fd8b40ea5a07972439a7b20c862f008e2c71cd181290876d43ab6cb
- id: c12
  role: evaluation
  text: blog 認為對 RAG 來說要的是圖分群給的「主題」：使用者問「Dennis Ritchie 是誰」，你希望一次撈到他的作品、死亡日期、年齡，這些東西語意上八竿子打不著，但共同構成一個可以被摘要的主題
  source_quotes:
  - "對 RAG 來說要的是後者：使用者問「Dennis Ritchie 是誰」，你希望一次撈到他的作品、死亡日期、年齡，這些東西語意上八竿子打不著，但共同構成一個可以被摘要的主題。"
  anchor_type: 部落格判斷
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: 所以「一個社群內部語意差很多」不是缺陷，是設計目的；blog 認為 GraphRAG 的整個價值主張就建立在這裡：知識圖的邊帶著語意向量看不見的關聯資訊，社群偵測是把它變現的方式
  source_quotes:
  - "所以「一個社群內部語意差很多」不是缺陷，是設計目的。GraphRAG 的整個價值主張就建立在這裡：知識圖的邊帶著語意向量看不見的關聯資訊，社群偵測是把它變現的方式。"
  qualifiers:
  - text: 同一篇 blog 在 RAGU 自己的對照裡量到，整套 GraphRAG（含 Leiden 分群、社群摘要）相對於純向量檢索的淨貢獻只有 1.2 到 4.3 pp
    source_quote: "整套 GraphRAG——兩階段抽取、DBSCAN consolidation、Leiden 分群、社群摘要——相對於純向量檢索的淨貢獻，就是這 1.2 到 4.3 pp。"
  anchor_type: 部落格判斷
  importance: 13
  status: normal
- id: c14
  role: evaluation
  text: RAGU 同一條 pipeline 裡用了兩種「像」：Step 3 的 consolidation 用語意相似度，處理同一個東西的不同寫法；Step 5 的社群偵測用結構相關性，處理不同東西之間的關聯；用途完全不同
  source_quotes:
  - "一個好記的對照是，RAGU 同一條 pipeline 裡用了兩種「像」——Step 3 的 consolidation 用語意相似度（同一個東西的不同寫法），Step 5 的社群偵測用結構相關性（不同東西之間的關聯）。用途完全不同。"
  qualifiers:
  - text: 論文敘述前後不一致：abstract 說 DBSCAN 用於跨名字去重，方法段讀起來卻像是先用 (name, type) 分好組、再在同一組內部做 DBSCAN，後者根本無法合併別名
    source_quote: "abstract 說 DBSCAN 用於跨名字去重，方法段讀起來卻像是先用 (name, type) 分好組、再在同一組內部做 DBSCAN。後者根本無法合併別名。"
  - text: blog 說論文的文字本身無法判定是哪一種，要確認只能翻原始碼
    source_quote: "論文的文字本身無法判定，要確認只能翻原始碼。"
  anchor_type: 部落格判斷
  importance: 14
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

- 度數（degree）：一個節點連出去的邊數。
- k-means：把每個點分到最近的 k 個中心之一、反覆更新中心的向量分群演算法。
