---
id: ragu-pipeline-two-stage-extraction-consolidation
title: RAGU 的六個步驟裡，跟 Microsoft GraphRAG、LightRAG 的差別只有 Step 3 的 consolidation，而且沒有 ablation；Step 2 的兩階段抽取（先定死合法實體、再讓 LLM 選）是可以單獨拿走用的 pattern，但受 schema 覆蓋限制
type_hint: 方法
context_type: bound_to_source
sources:
- article: ragu
  article_title: "RAGU：一篇替 GraphRAG 量出天花板的論文"
  url: https://datasciocean.com/paper-intro/ragu/
  sections:
  - 前言
  - GraphRAG 在解什麼問題
  - 方法：六個步驟，原創的只有一格
  - Step 2：兩階段抽取，把生成變成選擇題
  - Step 3：consolidation，論文的核心賣點
  - 實驗：把混淆變因一層層剝掉
  - 工程面：這篇論文最紮實的部分
  - 結論
  first_appearance: true
parent: null
related:
  - ragu-results-peeling-confounds
  - retrieval-recall-not-answer-quality
  - entity-resolution-not-clustering
  - graph-vs-vector-clustering-modularity
  - small-extractor-saturation-not-scale
  - multihop-vector-vs-graphrag-pain-points
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: RAGU 的六個步驟跟 Microsoft GraphRAG、LightRAG 相比，差別只有 Step 3（去重與摘要，consolidation）這一格，其他每一格都是既有做法，而論文從頭到尾沒有做「有 Step 3 vs 沒 Step 3」的 ablation；blog 認為它的兩階段 typed extraction 是個可以單獨拿走用的好 pattern
  source_quotes:
  - "跟 Microsoft GraphRAG、LightRAG 相比，差別只有 Step 3 這一格，其他每一格都是既有做法。"
  - "Step 3  Deduplication & Summarization  ★ 這篇唯一的原創處"
  - "**論文從頭到尾沒有做「有 Step 3 vs 沒 Step 3」的 ablation**"
  - "它的兩階段 typed extraction 是個可以單獨拿走用的好 pattern"
  qualifiers:
  - text: 論文用的 NEREL schema 來自一套俄語新聞語料的標註體系，論文自己在 Bias 段承認換語言或換領域可能要重新設計 schema
    source_quote: "論文用的 NEREL schema 有 29 種實體型別、49 種關係型別，來自一套俄語新聞語料的標註體系。論文自己在 Bias 段承認換語言或換領域可能要重新設計 schema"
  - text: blog 指出 schema 覆蓋不足時，LLM 被迫在既有型別裡挑一個最接近的，就會挑錯（NEREL 沒有 CREATOR_OF 這類關係）
    source_quote: "這是 schema 覆蓋不足的典型症狀：NEREL 裡沒有 `CREATOR_OF` 這類關係，LLM 被迫在 49 個型別裡挑一個最接近的，就挑錯了。"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
  figures:
  - file: figures/ragu/figure2.png
    article: ragu
    src: figure2.png
    caption: 圖二 — RAGU 的端到端索引流程。三層儲存（圖資料庫、key-value store、向量庫）都是可抽換的。（來源：原始論文 Figure 2）
    sha256: 0494c68435f9f2259fe394ed0ce7ebaa81ed3cef14728f21fc4ca2d9b8148cf3
- id: c2
  role: context
  text: RAGU 是 ITMO University 團隊在 2026 年 7 月放上 arXiv 的 GraphRAG 引擎，開源；論文的主張是把知識圖的「抽取」跟「整併」拆成兩個階段，圖會更乾淨，檢索也會更完整
  source_quotes:
  - "RAGU 是 ITMO University 團隊在 2026 年 7 月[放上 arXiv](https://arxiv.org/abs/2607.11683)的 GraphRAG 引擎"
  - "兩者都開源"
  - "論文的主張是：把知識圖的「抽取」跟「整併」拆成兩個階段，圖會更乾淨，檢索也會更完整。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 日期
  importance: 2
  status: normal
- id: c3
  role: context
  text: GraphRAG 的解法是先請 LLM 把文件裡的實體（人、組織、產品）跟關係抽出來建成知識圖，檢索時可以沿著圖上的邊走；RAGU 認為現有系統的問題之一是一次性抽完就建圖，產生大量重複與噪音實體，沒有跨 chunk 整併的機制
  source_quotes:
  - "GraphRAG 的解法是先請 LLM 把文件裡的實體（人、組織、產品）跟關係抽出來建成知識圖，檢索時可以沿著圖上的邊走。"
  - "RAGU 認為現有系統有三個問題：一次性抽完就建圖，產生大量重複與噪音實體，沒有跨 chunk 整併的機制"
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 流程依序是 Chunking、Entity & Relation Extraction（兩階段、有 schema 約束）、Deduplication & Summarization（把重複、別名、噪音的實體與關係洗成乾淨版）、Graph Construction、Community Detection（Leiden）、Community Summarization
  source_quotes:
  - "Step 1  Chunking"
  - "Step 2  Entity & Relation Extraction   ← 兩階段、有 schema 約束"
  - "Entities & Relations（很髒：重複、別名、噪音）"
  - "Step 3  Deduplication & Summarization  ★ 這篇唯一的原創處"
  - "Entities & Relations（乾淨版）"
  - "Step 4  Graph Construction"
  - "Step 5  Community Detection（Leiden）"
  - "Step 6  Community Summarization"
  anchor_type: 設計參數
  importance: 4
  status: normal
  figures:
  - file: figures/ragu/figure2.png
    article: ragu
    src: figure2.png
    caption: 圖二 — RAGU 的端到端索引流程。三層儲存（圖資料庫、key-value store、向量庫）都是可抽換的。（來源：原始論文 Figure 2）
    sha256: 0494c68435f9f2259fe394ed0ce7ebaa81ed3cef14728f21fc4ca2d9b8148cf3
- id: c5
  role: mechanism
  text: blog 認為「先洗再建圖」在原理上說得通：社群偵測是看圖的連接結構在分群，如果同一個實體被拆成三個節點（「Dennis Ritchie」/「Ritchie」/「D. Ritchie」），本來該集中的 3 條邊會被分散成 1+1+1，這個節點在結構上就變得不重要，可能被分進錯的社群，甚至變成孤立點；抽取階段的噪音會經過社群偵測放大成結構性錯誤，而且下游修不回來
  source_quotes:
  - "「先洗再建圖」在原理上是說得通的。社群偵測是看圖的連接結構在分群，如果同一個實體被拆成三個節點（「Dennis Ritchie」/「Ritchie」/「D. Ritchie」），本來該集中的 3 條邊會被分散成 1+1+1，這個節點在結構上就變得不重要，可能被分進錯的社群，甚至變成孤立點。換句話說，抽取階段的噪音會經過社群偵測放大成結構性錯誤，而且下游修不回來。"
  qualifiers:
  - text: 在論文挑出來的 Dennis Ritchie demo 中，圖上的邊錯了，多跳問答仍答對，因為檢索回來的是原始 chunk 文字，不是只有那條錯誤的邊
    source_quote: "因為檢索回來的是原始 chunk 文字，不是只有那條錯誤的邊"
  - text: 論文自陳的限制之一：抽取模型太弱時引入的結構噪音，consolidation 也救不回來
    source_quote: "抽取模型太弱時引入的結構噪音，consolidation 也救不回來。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 5
  status: normal
- id: c6
  role: evaluation
  text: 論文缺了一個關鍵 ablation：附錄的組態實驗只測了 ICL（要不要在 prompt 裡放範例）、validation、抽取模型大小三個開關，唯獨沒測它自己的核心賣點；所以 consolidation 究竟帶來多少 gain，論文只有跟 LightRAG 的跨系統比較，而兩者的差異遠不只 Step 3
  source_quotes:
  - "附錄的組態實驗只測了 ICL（in-context learning，要不要在 prompt 裡放範例）、validation、抽取模型大小三個開關，唯獨沒測它自己的核心賣點。所以 consolidation 究竟帶來多少 gain，論文只有跟 LightRAG 的跨系統比較，而兩者的差異遠不只 Step 3。"
  anchor_type: 部落格判斷
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: Step 2 的抽取被拆成兩趟 LLM 呼叫：第一趟從 chunk 抽實體、用 NEREL schema 驗證型別，產出已驗證的實體集合 E；第二趟把 chunk 加上 E 拿去抽關係，約束是每個關係的 source_entity 與 target_entity 必須是 E 裡面已驗證過的名字
  source_quotes:
  - "抽取被拆成兩趟 LLM 呼叫："
  - "Stage 1: chunk → 抽實體 → 用 NEREL schema 驗證型別"
  - "產出已驗證的實體集合 E = {e1, e2, ...}"
  - "Stage 2: chunk + E → 抽關係"
  - "約束：每個關係的 source_entity 與 target_entity"
  - "必須是 E 裡面已驗證過的名字"
  anchor_type: 設計參數
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: 兩階段抽取解決的是懸空的邊：單次抽取時，LLM 常在關係裡寫出實體清單裡不存在的名字（實體抽到「Bell Laboratories」，關係卻寫「Bell Labs」，邊就指向一個不存在的節點）；兩階段先把「有哪些節點」定死，第二階段就從開放式生成變成封閉集合上的選擇題
  source_quotes:
  - "它解決的是懸空的邊。單次抽取時，LLM 常在關係裡寫出實體清單裡不存在的名字——實體抽到「Bell Laboratories」，關係卻寫「Bell Labs」，邊就指向一個不存在的節點。兩階段先把「有哪些節點」定死，第二階段就從開放式生成變成封閉集合上的選擇題。"
  anchor_type: 部落格推論
  importance: 8
  status: normal
- id: c9
  role: evaluation
  text: blog 認為這個 pattern 可以脫離 GraphRAG 單獨用：任何時候要 LLM 產生「指向既有事物」的輸出，先把合法選項定死，再讓它選
  source_quotes:
  - "這個 pattern 可以脫離 GraphRAG 單獨用：任何時候要 LLM 產生「指向既有事物」的輸出，先把合法選項定死，再讓它選。"
  qualifiers:
  - text: 論文用的 NEREL schema 來自一套俄語新聞語料的標註體系，論文自己在 Bias 段承認換語言或換領域可能要重新設計 schema
    source_quote: "論文用的 NEREL schema 有 29 種實體型別、49 種關係型別，來自一套俄語新聞語料的標註體系。論文自己在 Bias 段承認換語言或換領域可能要重新設計 schema"
  - text: blog 指出 schema 覆蓋不足時，LLM 被迫在既有型別裡挑一個最接近的，就會挑錯（NEREL 沒有 CREATOR_OF 這類關係）
    source_quote: "這是 schema 覆蓋不足的典型症狀：NEREL 裡沒有 `CREATOR_OF` 這類關係，LLM 被迫在 49 個型別裡挑一個最接近的，就挑錯了。"
  anchor_type: 部落格判斷
  importance: 9
  status: normal
- id: c10
  role: qualifier
  text: 論文用的 NEREL schema 有 29 種實體型別、49 種關係型別，來自一套俄語新聞語料的標註體系；論文自己在 Bias 段承認換語言或換領域可能要重新設計 schema
  source_quotes:
  - "論文用的 NEREL schema 有 29 種實體型別、49 種關係型別，來自一套俄語新聞語料的標註體系。論文自己在 Bias 段承認換語言或換領域可能要重新設計 schema"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 10
  status: normal
- id: c11
  role: evidence
  text: 論文挑出來的 demo：一段 Dennis Ritchie 的文字抽出 8 條關係，論文展示其中 5 條，前兩條（Dennis Ritchie 到 C Programming Language、到 Unix Operating System，關係都是 WORKS_AS）是錯的——原文說 Ritchie 創造了 C 語言，WORKS_AS 的語意是「擔任某職位」；blog 指出這還是論文自己挑出來展示的最佳案例，5 條裡錯 2 條
  source_quotes:
  - "那段 Dennis Ritchie 的文字抽出 8 條關係，論文展示其中 5 條："
  - "Dennis Ritchie | C Programming Language | WORKS_AS"
  - "Dennis Ritchie | Unix Operating System | WORKS_AS"
  - "前兩條是錯的。原文說 Ritchie 創造了 C 語言，`WORKS_AS` 的語意是「擔任某職位」，完全不對。"
  - "而這還是論文自己挑出來展示的最佳案例，5 條裡錯 2 條。"
  anchor_type: 部落格考證
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 11
  status: normal
- id: c12
  role: mechanism
  text: blog 認為這是 schema 覆蓋不足的典型症狀：NEREL 裡沒有 CREATOR_OF 這類關係，LLM 被迫在 49 個型別裡挑一個最接近的，就挑錯了
  source_quotes:
  - "這是 schema 覆蓋不足的典型症狀：NEREL 裡沒有 `CREATOR_OF` 這類關係，LLM 被迫在 49 個型別裡挑一個最接近的，就挑錯了。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 12
  status: normal
- id: c13
  role: evidence
  text: 圖錯了，答案卻對了：後面的多跳問答還是答對了「Ritchie 創造了 C 語言」，因為檢索回來的是原始 chunk 文字，不是只有那條錯誤的邊；blog 認為這說明圖在這裡的作用主要是「找到相關段落」，最終答案還是 LLM 從原文讀出來的
  source_quotes:
  - "有意思的是，後面的多跳問答還是答對了「Ritchie 創造了 C 語言」，因為檢索回來的是原始 chunk 文字，不是只有那條錯誤的邊。這反過來說明圖在這裡的作用主要是「找到相關段落」，最終答案還是 LLM 從原文讀出來的。"
  anchor_type: 部落格推論
  importance: 13
  status: normal
- id: c14
  role: mechanism
  text: Step 3 處理的是「提及（mention）」：同一個真實世界的實體在不同 chunk 裡會產生各自獨立的 mention；blog 描述的第一層是便宜的做法，字串完全相同、型別也相同的合成一組，純 hash 比對、零 LLM 呼叫，在 blog 的例子裡 9 筆 mention 變 6 組（正確答案是 3 個實體）；字串比對抓得到重複，抓不到別名
  source_quotes:
  - "要理解它在幹嘛，得先知道抽取出來的東西是「提及（mention）」，不是節點。同一個真實世界的實體，在 9 個 chunk 裡會產生 9 筆各自獨立的 mention："
  - "直接建圖會得到 9 個節點，正確答案是 3 個。"
  - "第一層是便宜的做法：字串完全相同、型別也相同的合成一組。純 hash 比對，零 LLM 呼叫，9 筆變 6 組。"
  - "**字串比對抓得到重複，抓不到別名。**"
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 14
  status: normal
- id: c15
  role: mechanism
  text: blog 描述的第二層才是貴的：把每一組當成一個點丟進 embedding 空間跑 DBSCAN（在半徑 eps 內至少有 min_samples 個鄰居的點算核心點，核心點跟鄰居連成一群，連不上任何群的點標成 noise），合完之後再讓 LLM 把該群所有描述融成一段 canonical 描述；DBSCAN 決定合誰，LLM 決定合出來長什麼樣
  source_quotes:
  - "第二層才是貴的：把每一組當成一個點丟進 embedding 空間跑 DBSCAN。DBSCAN 的規則是，在半徑 `eps` 內至少有 `min_samples` 個鄰居的點算核心點，核心點跟鄰居連成一群，連不上任何群的點標成 noise。合完之後再讓 LLM 把該群所有描述融成一段 canonical 描述。所以這一層同時做兩件事：DBSCAN 決定合誰，LLM 決定合出來長什麼樣。"
  qualifiers:
  - text: 論文敘述前後不一致：abstract 說 DBSCAN 用於跨名字去重，方法段讀起來卻像是先用 (name, type) 分好組、再在同一組內部做 DBSCAN，後者根本無法合併別名
    source_quote: "abstract 說 DBSCAN 用於跨名字去重，方法段讀起來卻像是先用 (name, type) 分好組、再在同一組內部做 DBSCAN。後者根本無法合併別名。"
  - text: blog 說論文的文字本身無法判定是哪一種，要確認只能翻原始碼
    source_quote: "論文的文字本身無法判定，要確認只能翻原始碼。"
  anchor_type: 部落格考證
  importance: 15
  status: normal
- id: c16
  role: evaluation
  text: blog 認為這個機制最脆弱的地方是 Alistair E. Ritchie（Dennis 的父親）：兩人的名字字串高度相似、描述也都跟貝爾實驗室有關，eps 稍微放寬，父子就被合併成同一個節點，而且下游沒有任何機制救得回來
  source_quotes:
  - "這個機制最脆弱的地方是 Alistair E. Ritchie，Dennis 的父親。兩人的名字字串高度相似、描述也都跟貝爾實驗室有關，`eps` 稍微放寬，父子就被合併成同一個節點，而且下游沒有任何機制救得回來。"
  qualifiers:
  - text: 論文敘述前後不一致：abstract 說 DBSCAN 用於跨名字去重，方法段讀起來卻像是先用 (name, type) 分好組、再在同一組內部做 DBSCAN，後者根本無法合併別名
    source_quote: "abstract 說 DBSCAN 用於跨名字去重，方法段讀起來卻像是先用 (name, type) 分好組、再在同一組內部做 DBSCAN。後者根本無法合併別名。"
  - text: blog 說論文的文字本身無法判定是哪一種，要確認只能翻原始碼
    source_quote: "論文的文字本身無法判定，要確認只能翻原始碼。"
  anchor_type: 部落格推論
  importance: 16
  status: normal
- id: c17
  role: evaluation
  text: 第二層只有「重複提及很多」的實體才會啟動，因為每個 cluster 至少一次 LLM 呼叫；blog 認為這個取捨合理，但論文沒討論它的代價：只出現一兩次的實體永遠不會被 consolidate，而多跳問答的關鍵橋樑實體常常正好是低頻的，這可能是 RAGU 在 MuSiQue 上落後的原因之一
  source_quotes:
  - "第二層還有一道門檻：只有「重複提及很多」的實體才會啟動，因為每個 cluster 至少一次 LLM 呼叫"
  - "這個取捨合理，但論文沒討論它的代價——只出現一兩次的實體永遠不會被 consolidate，而多跳問答的關鍵橋樑實體常常正好是低頻的。這可能是 RAGU 在 MuSiQue 上落後的原因之一：consolidation 優化的是高頻主幹，多跳推理靠的是低頻支線。"
  anchor_type: 部落格推論
  importance: 17
  status: normal
- id: c18
  role: evaluation
  text: 論文另外有三件事沒交代：embedding 的對象到底是實體名稱、描述、還是名稱加描述加來源 chunk（這直接決定能不能合併「Bell Labs」跟「Bell Laboratories」）；eps 跟 min_samples 怎麼設（DBSCAN 對 eps 極度敏感）；「many duplicate mentions」的門檻是多少
  source_quotes:
  - "論文另外有三件事沒交代：embedding 的對象到底是實體名稱、描述、還是名稱加描述加來源 chunk（這直接決定能不能合併「Bell Labs」跟「Bell Laboratories」）；`eps` 跟 `min_samples` 怎麼設（DBSCAN 對 eps 極度敏感，這是整個機制最需要調的旋鈕）；「many duplicate mentions」的門檻是多少。"
  anchor_type: 部落格判斷
  importance: 18
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

- 別名：同一個實體的不同寫法（例如全名、縮寫、簡稱）。
