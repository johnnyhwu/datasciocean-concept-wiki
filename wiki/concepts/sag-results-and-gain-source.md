---
id: sag-results-and-gain-source
title: SAG 的績效大頭來自 SQL 檢索管線，不是超邊本身，也不是強 embedding；而且越難的資料集領先 HippoRAG 2 越多
type_hint: 發現
context_type: bound_to_source
sources:
- article: sag
  article_title: "SAG：拋開離線知識圖譜，查詢時用 SQL 連事件"
  url: https://datasciocean.com/paper-intro/sag/
  sections:
  - 前言
  - 什麼是「潛在超邊」
  - 為什麼 4 跳的推論只需要 1 跳的檢索
  - GraphRAG：結構有了，但代價很大
  - Step 1：雙軌種子檢索
  - Step 2：查詢時動態擴展
  - 刻意不做實體對齊
  - 主結果：越難的資料集領先越多
  - 消融一：事件結構值多少
  - 對 embedding 品質的依賴度
  - 這套架構會在哪裡咬你
  first_appearance: true
parent: null
related:
- sag-latent-hyperedge-one-hop
- sag-tradeoffs-price-paid
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 論文的招牌是超邊，但績效的大頭其實來自管線設計；SAG 的結構收益主要來自字串精確匹配的 SQL JOIN，跟 embedding 品質基本無關
  source_quotes:
  - "換句話說，論文的招牌是超邊，但績效的大頭其實來自管線設計。"
  - "SAG 的結構收益主要來自字串精確匹配的 SQL JOIN，跟 embedding 品質基本無關。"
  qualifiers:
  - text: 別名對齊的壓力被推遲到線上，交給向量的模糊匹配去處理
    source_quote: "別名對齊的壓力被推遲到線上，交給向量的模糊匹配去處理。"
  - text: 線上的種子預算（超過 50 就依向量相似度排序，只留 Top 50）與實體剪枝（前線實體超過 50 個時計算它們跟 query 的向量相似度，只留 Top 50）也都靠向量相似度排序
    source_quote: "超過 50 就依向量相似度排序，只留 Top 50 進到下一步"
  - text: 實體剪枝也靠向量相似度：前線實體超過 50 個時，計算它們跟 query 的向量相似度，只留 Top 50
    source_quote: "前線實體超過 50 個時，計算它們跟 query 的向量相似度，強制只留 Top 50"
  - text: 支持這個論點的三元組消融是在 MuSiQue 上做的
    source_quote: "事件層級索引 vs. 三元組拆解索引的消融比較（MuSiQue）"
    source: figure_caption
  - text: 支持這個論點的換 embedding 實驗是在 MuSiQue 上做的
    source_quote: "換上 NV-Embed-v2 之後，SAG 與 HippoRAG 2 在 MuSiQue 上的表現"
    source: figure_caption
  anchor_type: 部落格判斷
  importance: 1
  status: normal
  figures:
  - file: figures/sag/table2.png
    article: sag
    src: table2.png
    caption: 表二 — 事件層級索引 vs. 三元組拆解索引的消融比較（MuSiQue）。（來源：原始論文）
    sha256: d866d220c485d0177af1a764b8f0f32174a2bbbb918b946d36d211fd3bddea92
  - file: figures/sag/table4.png
    article: sag
    src: table4.png
    caption: 表四 — 換上 NV-Embed-v2 之後，SAG 與 HippoRAG 2 在 MuSiQue 上的表現。（來源：原始論文）
    sha256: 6f513f36a3eaa9b2da132bd5db7d9c285a2962d889aceecf667b03a7722ca4ba
- id: c2
  role: context
  text: SAG（SQL-Retrieval Augmented Generation）論文提出的折衷方案：線下不建圖，只把每個 chunk 轉成一個保留完整語意的「事件」加上一組實體標籤，寫進標準 SQL 資料庫；線上查詢時再用 SQL JOIN 把共用實體的事件動態串起來；圖只在查詢的那一瞬間存在，查完就丟
  source_quotes:
  - "SAG（SQL-Retrieval Augmented Generation）這篇論文提出的折衷方案很直接：線下不建圖，只把每個 chunk 轉成一個保留完整語意的「事件」加上一組實體標籤，寫進標準 SQL 資料庫；線上查詢時再用 SQL JOIN 把共用實體的事件動態串起來。 圖只在查詢的那一瞬間存在，查完就丟。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: HippoRAG 屬於 GraphRAG 這類方法：在線下用 LLM 抽三元組、建全域知識圖譜，並用 Personalized PageRank 在圖上傳分數
  source_quotes:
  - "為了補上結構，GraphRAG、HippoRAG 這類方法在線下用 LLM 抽三元組、建全域知識圖譜。"
  - "像 HippoRAG 用 Personalized PageRank 在圖上傳分數"
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: context
  text: 主結果比較三個多跳資料集：MuSiQue 最難（4 跳且經反事實過濾）、HotpotQA 是 2 跳（橋樑與比較型問題）、2WikiMultiHopQA 是長實體鏈（含罕見橋樑）；主要對照是 HippoRAG 2，兩者用同一個 BGE-Large embedding
  source_quotes:
  - "重點看跟 HippoRAG 2 的差距（兩者用同一個 BGE-Large embedding）"
  - "MuSiQue | 最難，4 跳且經反事實過濾"
  - "HotpotQA | 2 跳，橋樑與比較型問題"
  - "2WikiMultiHopQA | 長實體鏈，含罕見橋樑"
  qualifiers:
  - text: blog 另一處說的是 MuSiQue 裡「有些」問題在二元圖譜上要跳 4 次，不是每一題都是 4 跳
    source_quote: "MuSiQue 裡有些問題在二元圖譜上要跳 4 次才到得了答案"
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 4
  status: normal
- id: c5
  role: evidence
  text: MuSiQue 上 SAG 的 Recall@2 / Recall@5 是 64.1 / 80.0，HippoRAG 2 是 49.5 / 65.1，領先近 15 個百分點
  source_quotes:
  - "MuSiQue | 最難，4 跳且經反事實過濾 | 64.1 / 80.0 | 49.5 / 65.1"
  - "MuSiQue 上領先近 15 個百分點"
  anchor_type: 實驗結果
  comparison_target: HippoRAG 2（兩者用同一個 BGE-Large embedding）
  importance: 5
  status: normal
  figures:
  - file: figures/sag/table1.png
    article: sag
    src: table1.png
    caption: 表一 — 統一底層設定（BGE-Large-EN-v1.5 + Qwen3.6-Flash）下，SAG 與各 baseline 的 Recall@2/5 對照。（來源：原始論文）
    sha256: fd536520d6a38edaab34825817238bbf37f404975140cec5cfe967909f1eb276
- id: c6
  role: evaluation
  text: MuSiQue 是最考驗連結能力的一組：它有 4 步邏輯鏈，還經過反事實過濾防止單步語意作弊
  source_quotes:
  - "而且這是最考驗連結能力的一組——它有 4 步邏輯鏈，還經過反事實過濾防止單步語意作弊。"
  qualifiers:
  - text: blog 另一處說的是 MuSiQue 裡「有些」問題在二元圖譜上要跳 4 次，不是每一題都是 4 跳
    source_quote: "MuSiQue 裡有些問題在二元圖譜上要跳 4 次才到得了答案"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 6
  status: normal
- id: c7
  role: evaluation
  text: MuSiQue 的領先支持了論文的機制主張：用 SQL 做確定性的局部超邊鏈接，比在全域圖上跑 PageRank 擴散更能保住深層證據
  source_quotes:
  - "這支持了論文的機制主張：用 SQL 做確定性的局部超邊鏈接，比在全域圖上跑 PageRank 擴散更能保住深層證據。"
  anchor_type: 部落格判斷
  importance: 7
  status: normal
- id: c8
  role: evidence
  text: HotpotQA 上 SAG 的 Recall@2 / Recall@5 是 91.6 / 96.5，HippoRAG 2 是 78.4 / 94.4：Recall@5 的差距縮到 2.1 個百分點，Recall@2 上 SAG 還是領先 13.2 個百分點
  source_quotes:
  - "HotpotQA | 2 跳，橋樑與比較型問題 | 91.6 / 96.5 | 78.4 / 94.4"
  - "HotpotQA 只有 2 跳，圖傳播的衰減效應本來就弱，所以 Recall@5 的差距縮到 2.1 個百分點。但 Recall@2 上 SAG 還是領先 13.2 個百分點"
  anchor_type: 實驗結果
  comparison_target: HippoRAG 2（兩者用同一個 BGE-Large embedding）
  importance: 8
  status: normal
  figures:
  - file: figures/sag/table1.png
    article: sag
    src: table1.png
    caption: 表一 — 統一底層設定（BGE-Large-EN-v1.5 + Qwen3.6-Flash）下，SAG 與各 baseline 的 Recall@2/5 對照。（來源：原始論文）
    sha256: fd536520d6a38edaab34825817238bbf37f404975140cec5cfe967909f1eb276
- id: c9
  role: mechanism
  text: HotpotQA 只有 2 跳，圖傳播的衰減效應本來就弱，所以 SAG 在 Recall@5 上的領先縮小
  source_quotes:
  - "HotpotQA 只有 2 跳，圖傳播的衰減效應本來就弱，所以 Recall@5 的差距縮到 2.1 個百分點。"
  anchor_type: 部落格推論
  comparison_target: HippoRAG 2（兩者用同一個 BGE-Large embedding）
  importance: 9
  status: normal
- id: c10
  role: evaluation
  text: HotpotQA 的 Recall@2 上，SAG 比 HippoRAG 2 領先 13.2 個百分點：把最關鍵的證據排到最前面這件事，SAG 比較穩
  source_quotes:
  - "重點看跟 HippoRAG 2 的差距（兩者用同一個 BGE-Large embedding）"
  - "但 Recall@2 上 SAG 還是領先 13.2 個百分點——把最關鍵的證據排到最前面這件事，它比較穩。"
  anchor_type: 部落格判斷
  comparison_target: HippoRAG 2（兩者用同一個 BGE-Large embedding）
  importance: 10
  status: normal
- id: c11
  role: evidence
  text: 2WikiMultiHopQA 是 SAG 唯一輸的一格：SAG 的 Recall@2 領先（82.3 對 76.6），Recall@5 卻落後（88.0 對 90.4）
  source_quotes:
  - "2WikiMultiHopQA | 長實體鏈，含罕見橋樑 | 82.3 / 88.0 | 76.6 / 90.4"
  - "2Wiki 是唯一輸的一格，而且輸得很有意思。 SAG 的 Recall@2 領先（82.3 對 76.6），Recall@5 卻落後（88.0 對 90.4）。"
  anchor_type: 實驗結果
  comparison_target: HippoRAG 2（兩者用同一個 BGE-Large embedding）
  importance: 11
  status: normal
  figures:
  - file: figures/sag/table1.png
    article: sag
    src: table1.png
    caption: 表一 — 統一底層設定（BGE-Large-EN-v1.5 + Qwen3.6-Flash）下，SAG 與各 baseline 的 Recall@2/5 對照。（來源：原始論文）
    sha256: fd536520d6a38edaab34825817238bbf37f404975140cec5cfe967909f1eb276
- id: c12
  role: evidence
  text: 把 SAG 強行拆成三元組來跑，Recall@5 從 80.0% 掉到 77.1%；就算拆成三元組，77.1% 依然大幅贏過 HippoRAG 2 的 65.1%
  source_quotes:
  - "作者把 SAG 強行拆成三元組來跑，Recall@5 從 80.0% 掉到 77.1%。"
  - "就算拆成三元組，77.1% 依然大幅贏過 HippoRAG 2 的 65.1%"
  qualifiers:
  - text: 這個消融（完整事件對三元組）是在 MuSiQue 上做的
    source_quote: "事件層級索引 vs. 三元組拆解索引的消融比較（MuSiQue）"
    source: figure_caption
  anchor_type: 實驗結果
  comparison_target: 完整事件版的 SAG（80.0%）與 HippoRAG 2（65.1%）
  importance: 12
  status: normal
  figures:
  - file: figures/sag/table2.png
    article: sag
    src: table2.png
    caption: 表二 — 事件層級索引 vs. 三元組拆解索引的消融比較（MuSiQue）。（來源：原始論文）
    sha256: d866d220c485d0177af1a764b8f0f32174a2bbbb918b946d36d211fd3bddea92
- id: c13
  role: evaluation
  text: SAG 這套 SQL 檢索管線本身就有系統性優勢，跟用不用超邊無關
  source_quotes:
  - "也就是說，SAG 這套 SQL 檢索管線本身就有系統性優勢，跟用不用超邊無關"
  qualifiers:
  - text: 這個判斷依據的三元組消融是在 MuSiQue 上做的
    source_quote: "事件層級索引 vs. 三元組拆解索引的消融比較（MuSiQue）"
    source: figure_caption
  anchor_type: 部落格判斷
  importance: 13
  status: normal
  figures:
  - file: figures/sag/table2.png
    article: sag
    src: table2.png
    caption: 表二 — 事件層級索引 vs. 三元組拆解索引的消融比較（MuSiQue）。（來源：原始論文）
    sha256: d866d220c485d0177af1a764b8f0f32174a2bbbb918b946d36d211fd3bddea92
  - file: figures/sag/table1.png
    article: sag
    src: table1.png
    caption: 表一 — 統一底層設定（BGE-Large-EN-v1.5 + Qwen3.6-Flash）下，SAG 與各 baseline 的 Recall@2/5 對照。（來源：原始論文）
    sha256: fd536520d6a38edaab34825817238bbf37f404975140cec5cfe967909f1eb276
- id: c14
  role: mechanism
  text: 保留完整事件另外帶來 2.9 個百分點，因為一個事件記錄的是 N 元關係，不必像三元組那樣經歷多次 JOIN 走訪，也就少掉每一跳的剪枝損失
  source_quotes:
  - "保留完整事件另外帶來 2.9 個百分點，因為一個事件記錄的是 N 元關係，不必像三元組那樣經歷多次 JOIN 走訪，也就少掉每一跳的剪枝損失。"
  qualifiers:
  - text: 這個消融（完整事件對三元組）是在 MuSiQue 上做的
    source_quote: "事件層級索引 vs. 三元組拆解索引的消融比較（MuSiQue）"
    source: figure_caption
  anchor_type: 部落格推論
  comparison_target: 拆成三元組的 SAG（Recall@5 77.1%）
  importance: 14
  status: normal
  figures:
  - file: figures/sag/table2.png
    article: sag
    src: table2.png
    caption: 表二 — 事件層級索引 vs. 三元組拆解索引的消融比較（MuSiQue）。（來源：原始論文）
    sha256: d866d220c485d0177af1a764b8f0f32174a2bbbb918b946d36d211fd3bddea92
- id: c15
  role: evidence
  text: 把 embedding 從 BGE-Large 換成更強的 NV-Embed-v2，HippoRAG 2 的 Recall@5 從 65.1 升到 74.6（+9.5），SAG 從 80.0 升到 81.7（+1.7）
  source_quotes:
  - "把 embedding 從 BGE-Large 換成更強的 NV-Embed-v2："
  - "HippoRAG 2 | 65.1 | 74.6 | +9.5"
  - "SAG | 80.0 | 81.7 | +1.7"
  qualifiers:
  - text: 這個換 embedding 的實驗是在 MuSiQue 上做的
    source_quote: "換上 NV-Embed-v2 之後，SAG 與 HippoRAG 2 在 MuSiQue 上的表現"
    source: figure_caption
  anchor_type: 實驗結果
  comparison_target: 換模型之前（BGE-Large）的同一個系統
  importance: 15
  status: normal
  figures:
  - file: figures/sag/table4.png
    article: sag
    src: table4.png
    caption: 表四 — 換上 NV-Embed-v2 之後，SAG 與 HippoRAG 2 在 MuSiQue 上的表現。（來源：原始論文）
    sha256: 6f513f36a3eaa9b2da132bd5db7d9c285a2962d889aceecf667b03a7722ca4ba
- id: c16
  role: mechanism
  text: HippoRAG 的多跳極度依賴向量打分（圖上節點的初始分數就是向量相似度給的），模型一弱，誤差會沿著傳播路徑放大
  source_quotes:
  - "HippoRAG 的多跳極度依賴向量打分（圖上節點的初始分數就是向量相似度給的），模型一弱，誤差會沿著傳播路徑放大"
  anchor_type: 部落格推論
  importance: 16
  status: normal
- id: c17
  role: evaluation
  text: 用比較弱、比較便宜的 embedding 模型，SAG 依然維持得住多步檢索的水準
  source_quotes:
  - "用比較弱、比較便宜的 embedding 模型，SAG 依然維持得住多步檢索的水準。"
  qualifiers:
  - text: 別名對齊的壓力被推遲到線上，交給向量的模糊匹配去處理
    source_quote: "別名對齊的壓力被推遲到線上，交給向量的模糊匹配去處理。"
  - text: 線上的種子預算（超過 50 就依向量相似度排序，只留 Top 50）與實體剪枝（前線實體超過 50 個時計算它們跟 query 的向量相似度，只留 Top 50）也都靠向量相似度排序
    source_quote: "超過 50 就依向量相似度排序，只留 Top 50 進到下一步"
  - text: 實體剪枝也靠向量相似度：前線實體超過 50 個時，計算它們跟 query 的向量相似度，只留 Top 50
    source_quote: "前線實體超過 50 個時，計算它們跟 query 的向量相似度，強制只留 Top 50"
  - text: 這個判斷依據的換 embedding 實驗是在 MuSiQue 上做的
    source_quote: "換上 NV-Embed-v2 之後，SAG 與 HippoRAG 2 在 MuSiQue 上的表現"
    source: figure_caption
  anchor_type: 部落格判斷
  importance: 17
  status: normal
  figures:
  - file: figures/sag/table4.png
    article: sag
    src: table4.png
    caption: 表四 — 換上 NV-Embed-v2 之後，SAG 與 HippoRAG 2 在 MuSiQue 上的表現。（來源：原始論文）
    sha256: 6f513f36a3eaa9b2da132bd5db7d9c285a2962d889aceecf667b03a7722ca4ba
- id: c18
  role: qualifier
  text: 同一個實體在不同 chunk 裡寫法不同，而這些寫法在向量空間裡又沒近到 0.9 的門檻時，SQL 就會把它們當成兩個完全無關的索引點，跨文件的連結密度因此被人為降低
  source_quotes:
  - "如果同一個實體在不同 chunk 裡寫法不同"
  - "而這些寫法在向量空間裡又沒近到 0.9 的門檻，SQL 就會把它們當成兩個完全無關的索引點，跨文件的連結密度因此被人為降低。"
  qualifiers:
  - text: 0.9 是 Step 1 路徑 A 用實體向量索引擴充別名集合時的相似度門檻
    source_quote: "拿去實體向量索引做相似度搜尋（門檻 0.9 以上）擴充出別名集合"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 18
  status: normal
- id: c19
  role: context
  text: SAG 借用超圖（hypergraph）裡的超邊（hyperedge）：一條超邊可以同時包含任意數量的節點；在 SAG 中，一個 chunk 對應一個保留完整語意的事件，以及一組跟它綁定的實體集合，這個「事件 ↔ 實體集合」的綁定關係本身就定義了一條超邊
  source_quotes:
  - "SAG 借用的是超圖（hypergraph）裡的超邊（hyperedge）——一條超邊可以同時包含任意數量的節點。"
  - "在 SAG 中，一個 chunk 對應一個保留完整語意的事件 e，以及一組跟它綁定的實體集合。"
  - "這個「事件 ↔ 實體集合」的綁定關係，本身就定義了一條超邊。"
  anchor_type: 設計參數
  importance: 3
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

以下是很基本的通用詞，blog 沒有解釋，由撰寫者以一般知識補充；它們不是卡上的主張，不能當作 blog 的說法引用。

- **Recall@K**：在前 K 筆檢索結果中，找回了多少比例的應被找回的內容；Recall@2、Recall@5 分別看前 2 筆、前 5 筆。
- **embedding**：把文字轉成向量，讓語意相近的文字在向量空間裡距離也近。
- **PageRank**：一種在圖上依連結結構傳播分數、計算節點重要度的演算法；Personalized 版本從指定的起始節點出發傳播。
- **chunk**：把長文件切成的一小段文字，是檢索的基本單位。
- **SQL JOIN**：把兩張資料表中欄位值相同的列配對串接起來的操作。
