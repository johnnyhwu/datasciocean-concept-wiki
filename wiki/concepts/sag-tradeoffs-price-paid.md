---
id: sag-tradeoffs-price-paid
title: SAG 的簡潔與寫入吞吐是用三個代價換的：固定剪枝預算漏掉罕見實體、不做實體對齊稀釋跨文件連結、只支援 append-only 不支援更新
type_hint: 判斷
context_type: bound_to_source
sources:
- article: sag
  article_title: "SAG：拋開離線知識圖譜，查詢時用 SQL 連事件"
  url: https://datasciocean.com/paper-intro/sag/
  sections:
  - 前言
  - GraphRAG：結構有了，但代價很大
  - 刻意不做實體對齊
  - Step 1：雙軌種子檢索
  - Step 2：查詢時動態擴展
  - 主結果：越難的資料集領先越多
  - 這套架構會在哪裡咬你
  - 結論
  first_appearance: true
parent: null
related:
- sag-latent-hyperedge-one-hop
- sag-results-and-gain-source
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: SAG 的代價很清楚：固定剪枝預算會漏掉長尾罕見實體，不做別名合併會稀釋跨文件連結密度，而且目前還處理不了知識的更新與失效；這些都是為了換取系統簡潔性與寫入吞吐量而付的帳
  source_quotes:
  - "代價也很清楚：固定剪枝預算會漏掉長尾罕見實體，不做別名合併會稀釋跨文件連結密度，而且目前還處理不了知識的更新與失效。這些都是為了換取系統簡潔性與寫入吞吐量而付的帳"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
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
  role: mechanism
  text: SAG 設了剪枝預算 50：前線實體超過 50 個時，計算它們跟 query 的向量相似度，強制只留 Top 50，避免高頻通用字撈回海量無關事件
  source_quotes:
  - "如果前線裡混進「2014年」這種高頻通用字，下一步會撈回海量無關事件。所以系統設了剪枝預算 50——前線實體超過 50 個時，計算它們跟 query 的向量相似度，強制只留 Top 50。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 目前的剪枝策略是拿實體向量跟 query 算相似度來排序，但深層推論鏈裡的關鍵橋樑實體常常同時具備「語料庫裡很罕見」跟「跟原始問題語意相關性很低」兩個特徵，正好是最容易被擠出 50 個預算的那種
  source_quotes:
  - "剪枝預算會漏掉罕見實體。 這是 2Wiki 那格輸掉的直接原因。目前的剪枝策略是拿實體向量跟 query 算相似度來排序，但深層推論鏈裡的關鍵橋樑實體常常同時具備「語料庫裡很罕見」跟「跟原始問題語意相關性很低」兩個特徵，正好是最容易被擠出 50 個預算的那種。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 5
  status: normal
- id: c6
  role: evidence
  text: 2Wiki 那格輸掉（Recall@5 是 SAG 88.0 對 HippoRAG 2 的 90.4）的直接原因，是固定 50 的剪枝預算：2Wiki 含有極長、出現頻率極低的實體鏈，當某個橋樑實體在整個語料庫裡很罕見、跟原始問題的語意相關性又低時，很容易在擴展階段被高頻通用實體擠出 50 個名額之外，鏈就斷了
  source_quotes:
  - "重點看跟 HippoRAG 2 的差距（兩者用同一個 BGE-Large embedding）"
  - "資料集 | 推論難度 | SAG (R@2/R@5) | HippoRAG 2 (R@2/R@5)"
  - "Recall@5 卻落後（88.0 對 90.4）。原因就是前面那個固定 50 的剪枝預算：2Wiki 含有極長、出現頻率極低的實體鏈，當某個橋樑實體在整個語料庫裡很罕見、跟原始問題的語意相關性又低時，它很容易在擴展階段被高頻通用實體擠出 50 個名額之外，鏈就斷了。"
  anchor_type: 部落格推論
  comparison_target: HippoRAG 2（兩者用同一個 BGE-Large embedding）
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: 反觀 HippoRAG 的全域 PageRank，靠全圖傳播反而到得了這些低頻節點
  source_quotes:
  - "反觀 HippoRAG 的全域 PageRank，靠全圖傳播反而到得了這些低頻節點。"
  qualifiers:
  - text: 同一篇另一處說，HippoRAG 用 Personalized PageRank 在圖上傳分數時，跳數一多，遠端目標節點的分數會被阻尼係數壓得很低、深層答案排不上來；這裡說的是全圖傳播能到得了低頻節點
    source_quote: "跳數一多，遠端目標節點的分數會被阻尼係數（damping factor）壓得很低，深層答案排不上來"
  anchor_type: 部落格推論
  importance: 7
  status: normal
- id: c8
  role: evaluation
  text: 剪枝預算漏掉罕見實體的可能改法：引入類似 IDF（逆向文件頻率）的權重，或對實體做頻率分層，給低頻實體專屬的擴展額度
  source_quotes:
  - "可能的改法是引入類似 IDF（逆向文件頻率）的權重，或對實體做頻率分層，給低頻實體專屬的擴展額度。"
  anchor_type: 部落格判斷
  importance: 8
  status: normal
- id: c9
  role: context
  text: 傳統知識圖譜線下最沉重的負擔是實體對齊與消歧：判斷「馬克·祖克柏」「祖克柏」「Mark Zuckerberg」是不是同一個人，對齊失敗，圖就斷了
  source_quotes:
  - "傳統知識圖譜線下最沉重的負擔是實體對齊與消歧：判斷「馬克·祖克柏」「祖克柏」「Mark Zuckerberg」是不是同一個人。對齊失敗，圖就斷了。"
  anchor_type: 背景說明
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: SAG 線下完全不做全域實體對齊，只做去空白、統一大小寫這種極輕量的字面清洗
  source_quotes:
  - "SAG 的選擇很務實——線下完全不做全域實體對齊，只做去空白、統一大小寫這種極輕量的字面清洗。"
  anchor_type: 設計參數
  importance: 10
  status: normal
- id: c11
  role: mechanism
  text: SAG 敢這樣做，是因為在 SAG 裡承載語意價值的是事件，實體只是「連線指引」；別名對齊的壓力被推遲到線上，交給向量的模糊匹配去處理
  source_quotes:
  - "它敢這樣做，是因為在 SAG 裡承載語意價值的是事件，實體只是「連線指引」。別名對齊的壓力被推遲到線上，交給向量的模糊匹配去處理。"
  anchor_type: 部落格推論
  importance: 11
  status: normal
- id: c12
  role: evaluation
  text: 不做實體對齊換來很大的工程紅利：線下處理完全擺脫全域圖譜鎖的限制，寫入是獨立的、吞吐量高的、真正無痛的 append-only
  source_quotes:
  - "這個取捨換來的工程紅利很大：線下處理完全擺脫全域圖譜鎖的限制，寫入是獨立的、吞吐量高的、真正無痛的 append-only。"
  anchor_type: 部落格判斷
  importance: 12
  status: normal
- id: c13
  role: mechanism
  text: 如果同一個實體在不同 chunk 裡寫法不同（例如 Meta 對 Facebook、祖克柏對 Zuckerberg），而這些寫法在向量空間裡又沒近到 0.9 的門檻，SQL 就會把它們當成兩個完全無關的索引點，跨文件的連結密度因此被人為降低
  source_quotes:
  - '線下不對齊換來了無鎖的高吞吐寫入，但如果同一個實體在不同 chunk 裡寫法不同（"Meta" 對 "Facebook"、「祖克柏」對 "Zuckerberg"），而這些寫法在向量空間裡又沒近到 0.9 的門檻，SQL 就會把它們當成兩個完全無關的索引點，跨文件的連結密度因此被人為降低。'
  qualifiers:
  - text: 0.9 是 Step 1 路徑 A 用實體向量索引擴充別名集合時的相似度門檻
    source_quote: "拿去實體向量索引做相似度搜尋（門檻 0.9 以上）擴充出別名集合"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 13
  status: normal
- id: c14
  role: evaluation
  text: 在不破壞線下獨立性的前提下，可以加一張輕量的實體別名表，用背景非同步的方式慢慢聚合
  source_quotes:
  - "SAG 的折衷做法會是在不破壞線下獨立性的前提下，加一張輕量的實體別名表，用背景非同步的方式慢慢聚合。"
  anchor_type: 部落格判斷
  importance: 14
  status: normal
- id: c15
  role: mechanism
  text: 目前只支援 append-only，不支援更新：SAG 的設計對象是唯讀文件庫的增量追加，但 Agent 長期記憶體的知識是會變的（使用者偏好改變、工作狀態從「未完成」變「已完成」、歷史事實被修正）
  source_quotes:
  - "目前只支援 append-only，不支援更新。 SAG 的設計對象是唯讀文件庫的增量追加，但 Agent 長期記憶體的知識是會變的：使用者偏好改變、工作狀態從「未完成」變「已完成」、歷史事實被修正。"
  anchor_type: 部落格推論
  importance: 15
  status: normal
- id: c16
  role: mechanism
  text: 當資料庫裡同時存在互相衝突的新舊事件時，現在的索引沒有原生機制判斷哪一個才是最新有效的
  source_quotes:
  - "當資料庫裡同時存在互相衝突的新舊事件時，現在的索引沒有原生機制判斷哪一個才是最新有效的。"
  anchor_type: 部落格推論
  importance: 16
  status: normal
- id: c17
  role: evaluation
  text: 要往支援更新的方向走，schema 得補上時間戳記、生效標記與事件依賴鏈，讓檢索路徑能自動濾掉已被覆蓋的舊資訊
  source_quotes:
  - "要往這個方向走，schema 得補上時間戳記、生效標記與事件依賴鏈，讓檢索路徑能自動濾掉已被覆蓋的舊資訊。"
  anchor_type: 部落格判斷
  importance: 17
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

以下是很基本的通用詞，blog 沒有解釋，由撰寫者以一般知識補充；它們不是卡上的主張，不能當作 blog 的說法引用。

- **Recall@K**：在前 K 筆檢索結果中，找回了多少比例的應被找回的內容；Recall@5 看前 5 筆。
- **Top-K**：排序後取前 K 筆結果。
- **PageRank**：一種在圖上依連結結構傳播分數、計算節點重要度的演算法；Personalized 版本從指定的起始節點出發傳播。
- **chunk**：把長文件切成的一小段文字，是檢索的基本單位。
- **append-only**：只新增資料，不修改、不刪除既有資料。
- **IDF（逆向文件頻率）**：一個詞出現在越少文件裡，權重越高，用來突顯罕見詞。
