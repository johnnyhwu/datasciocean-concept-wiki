---
id: multihop-vector-vs-graphrag-pain-points
title: 多步推論檢索的兩種現有做法各有各的痛：向量檢索沒有邏輯約束而且會斷鏈，GraphRAG 有結構但代價很大
type_hint: 判斷
context_type: evidence_from_single_source
sources:
- article: sag
  article_title: "SAG：拋開離線知識圖譜，查詢時用 SQL 連事件"
  url: https://datasciocean.com/paper-intro/sag/
  sections:
  - 前言
  - 向量檢索：沒有邏輯約束，而且會斷鏈
  - GraphRAG：結構有了，但代價很大
  first_appearance: true
parent: null
related:
- sag-latent-hyperedge-one-hop
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 多步推論（multi-hop）是 RAG 系統最難落地的一塊：純向量檢索只看語意相似度，推理走到一半常常斷鏈；GraphRAG 這類做法能建立關聯，但線下建置成本高，資料一直進來的時候更難維護
  source_quotes:
  - "多步推論（multi-hop）一直是 RAG 系統最難落地的一塊。純向量檢索只看語意相似度，推理走到一半常常斷鏈；GraphRAG 這類做法能建立關聯，但要在線下把文本拆成三元組、做實體對齊、算全域分數，建置成本高，資料一直進來的時候更是難維護。"
  anchor_type: 背景說明
  importance: 1
  status: normal
- id: c2
  role: context
  text: 傳統的 dense retrieval 本質上就是語意相似度匹配：切塊、映射到向量空間、查詢時回傳 Top-K
  source_quotes:
  - "傳統的 dense retrieval 本質上就是語意相似度匹配：切塊、映射到向量空間、查詢時回傳 Top-K。"
  anchor_type: 背景說明
  importance: 2
  status: normal
- id: c3
  role: context
  text: GraphRAG、HippoRAG 這類方法為了補上結構，在線下用 LLM 抽三元組、建全域知識圖譜
  source_quotes:
  - "為了補上結構，GraphRAG、HippoRAG 這類方法在線下用 LLM 抽三元組、建全域知識圖譜。"
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: context
  text: SAG（SQL-Retrieval Augmented Generation）論文提出的折衷方案：線下不建圖，只把每個 chunk 轉成一個保留完整語意的「事件」加上一組實體標籤，寫進標準 SQL 資料庫；線上查詢時再用 SQL JOIN 把共用實體的事件動態串起來
  source_quotes:
  - "SAG（SQL-Retrieval Augmented Generation）這篇論文提出的折衷方案很直接：線下不建圖，只把每個 chunk 轉成一個保留完整語意的「事件」加上一組實體標籤，寫進標準 SQL 資料庫；線上查詢時再用 SQL JOIN 把共用實體的事件動態串起來。"
  anchor_type: 設計參數
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 推論鏈裡扮演橋樑的中間證據，字面和語意常常跟原始問題八竿子打不著；單靠向量距離，這種關鍵跳板在第一步就被過濾掉了
  source_quotes:
  - "第三，也是最要命的一點——推論鏈裡扮演橋樑的中間證據，字面和語意常常跟原始問題八竿子打不著。"
  - "單靠向量距離，這種關鍵跳板在第一步就被過濾掉了。"
  anchor_type: 背景說明
  importance: 5
  status: normal
- id: c6
  role: anchor
  text: 你問「某公司創辦人的母校在哪」，中間那段講創辦人學歷的文字可能完全沒提到公司名
  source_quotes:
  - "你問「某公司創辦人的母校在哪」，中間那段講創辦人學歷的文字可能完全沒提到公司名。"
  anchor_type: 部落格舉例
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: 向量檢索建立不了顯式的實體關聯：查詢一旦涉及時間限制、特定角色或多步依賴，向量相似度只能找到「讀起來很像」的段落，還原不了實體之間明確的邏輯鏈
  source_quotes:
  - "第一，它建立不了顯式的實體關聯。查詢一旦涉及時間限制、特定角色或多步依賴，向量相似度只能找到「讀起來很像」的段落，還原不了實體之間明確的邏輯鏈。"
  anchor_type: 背景說明
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: 誤差會沿著推理鏈放大：Agent 做序列式檢索時，第一步只要因為相似度不夠高而稍微偏掉，後面每一步都是在錯的基礎上繼續，最後整條路徑徹底斷掉
  source_quotes:
  - "第二，誤差會沿著推理鏈放大。Agent 做序列式檢索時，第一步只要因為相似度不夠高而稍微偏掉，後面每一步都是在錯的基礎上繼續，最後整條路徑徹底斷掉。"
  anchor_type: 背景說明
  importance: 8
  status: normal
- id: c9
  role: mechanism
  text: 語意破碎化：知識圖譜把關係限制成 (主體, 關係, 客體) 的二元組，但現實世界的事件多半是 N 元關係，牽涉多方、時間、地點；硬拆成幾條獨立三元組，原始上下文就沒了
  source_quotes:
  - "知識圖譜把關係限制成 (主體, 關係, 客體) 的二元組，但現實世界的事件多半是 N 元關係，牽涉多方、時間、地點。硬拆成幾條獨立三元組，原始上下文就沒了。"
  anchor_type: 背景說明
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: 增量更新是工程災難：真實系統的資料是持續寫入的，圖譜要維持正確，新文件進來時往往得重跑實體抽取、實體對齊、關係正規化，甚至重算全域節點權重（例如 PageRank），這個成本讓即時增量更新幾乎不可行
  source_quotes:
  - "真實系統的資料是持續寫入的。圖譜要維持正確，新文件進來時往往得重跑實體抽取、實體對齊、關係正規化，甚至重算全域節點權重（例如 PageRank）。這個成本讓即時增量更新幾乎不可行。"
  anchor_type: 背景說明
  importance: 10
  status: normal
- id: c11
  role: mechanism
  text: 論文指出一個很諷刺的現象：線下花大錢建出來的複雜圖結構，線上查詢時常常又退化成對「圖節點」或「社群摘要」做扁平的向量相似度匹配，結構根本沒發揮約束作用
  source_quotes:
  - "論文指出一個很諷刺的現象——線下花大錢建出來的複雜圖結構，線上查詢時常常又退化成對「圖節點」或「社群摘要」做扁平的向量相似度匹配，結構根本沒發揮約束作用。"
  anchor_type: 原作者解讀
  importance: 11
  status: normal
- id: c12
  role: mechanism
  text: 像 HippoRAG 用 Personalized PageRank 在圖上傳分數，跳數一多，遠端目標節點的分數會被阻尼係數（damping factor）壓得很低，深層答案排不上來
  source_quotes:
  - "分數衰減與雜訊放大：像 HippoRAG 用 Personalized PageRank 在圖上傳分數，跳數一多，遠端目標節點的分數會被阻尼係數（damping factor）壓得很低，深層答案排不上來"
  anchor_type: 背景說明
  importance: 12
  status: normal
- id: c13
  role: mechanism
  text: 圖裡的高頻中心節點（hub nodes）會把訊號往無關的地方擴散，雜訊分數反而升高
  source_quotes:
  - "同時圖裡的高頻中心節點（hub nodes）會把訊號往無關的地方擴散，雜訊分數反而升高。"
  anchor_type: 背景說明
  importance: 13
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

以下是很基本的通用詞，blog 沒有解釋，由撰寫者以一般知識補充；它們不是卡上的主張，不能當作 blog 的說法引用。

- **Top-K**：排序後取前 K 筆結果。
- **PageRank**：一種在圖上依連結結構傳播分數、計算節點重要度的演算法；Personalized 版本從指定的起始節點出發傳播。
