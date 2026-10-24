---
id: sag-sql-vector-llm-division-and-funnel
title: SAG 不是發明更強的模型，而是重新分配職責：SQL 做確定性關聯、向量做語意模糊擴展、LLM 只做高價值的聯合判斷，並用一串固定預算把 LLM 要看的量壓下來
type_hint: 方法
context_type: bound_to_source
sources:
- article: sag
  article_title: "SAG：拋開離線知識圖譜，查詢時用 SQL 連事件"
  url: https://datasciocean.com/paper-intro/sag/
  sections:
  - 前言
  - SAG 的設計哲學：讓每個元件只做它最擅長的事
  - 線下階段：把文件變成可 JOIN 的索引
  - 線上階段：雙軌種子、SQL 擴展、LLM 決選
  - Step 1：雙軌種子檢索
  - Step 2：查詢時動態擴展
  - Step 3：粗篩加 LLM 雙軌決選
  first_appearance: true
parent: null
related:
- sag-latent-hyperedge-one-hop
- retrieval-reasoning-decoupling
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: SAG 的核心不是發明更強的模型，而是重新分配檢索管線裡的職責：SQL 資料庫負責確定性關聯，向量資料庫負責語意模糊擴展，LLM 負責高價值的聯合判斷
  source_quotes:
  - "SAG 的核心不是發明更強的模型，而是重新分配檢索管線裡的職責。三個元件分工分得很死："
  - "SQL 資料庫 | 確定性關聯（filtering & joining）"
  - "向量資料庫 | 語意模糊擴展"
  - "LLM | 高價值的聯合判斷"
  anchor_type: 設計參數
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
  role: mechanism
  text: SQL 資料庫負責確定性關聯（filtering & joining）：它不懂語意，但「A 是否等於 B」的精確比對是確定的，而且串聯時不衰減、天然支援併發與 append-only 寫入
  source_quotes:
  - "SQL 資料庫 | 確定性關聯（filtering & joining） | 它不懂語意，但「A 是否等於 B」的精確比對是毫秒級、100% 確定，而且串聯時不衰減、天然支援併發與 append-only 寫入"
  qualifiers:
  - text: 線上 Step 2 有全域剪枝預算：前線實體超過 50 個時，只留跟 query 向量相似度最高的 Top 50，所以多跳串聯不是完全沒有損失
    source_quote: "前線實體超過 50 個時，計算它們跟 query 的向量相似度，強制只留 Top 50"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 向量資料庫負責語意模糊擴展：專門處理別名、同義詞、錯字、換句話說，當實體與事件的容錯安全網
  source_quotes:
  - "向量資料庫 | 語意模糊擴展 | 專門處理別名、同義詞、錯字、換句話說，當實體與事件的容錯安全網"
  anchor_type: 設計參數
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: LLM 只用在線下抽事件與實體，以及線上對壓縮過的候選集做 joint assessment
  source_quotes:
  - "LLM | 高價值的聯合判斷 | 只用在線下抽事件與實體，以及線上對壓縮過的候選集做 joint assessment"
  qualifiers:
  - text: 線上 Step 1 的路徑 A 也用輕量 LLM 從問題裡抽出實體
    source_quote: "先用輕量 LLM 從問題裡抽出實體，拿去實體向量索引做相似度搜尋（門檻 0.9 以上）擴充出別名集合"
  anchor_type: 設計參數
  importance: 5
  status: normal
- id: c6
  role: mechanism
  text: 向量檢索不拿來做多步推論，LLM 也不拿來走圖；多步推論交給 SQL，LLM 只在候選集已經縮到 100 個以內時才出場
  source_quotes:
  - "這裡的關鍵取捨是：向量檢索不拿來做多步推論，LLM 也不拿來走圖。多步推論交給 SQL，LLM 只在候選集已經縮到 100 個以內時才出場"
  qualifiers:
  - text: 線上 Step 1 的路徑 A 也用輕量 LLM 從問題裡抽出實體，那一步發生在候選集形成之前
    source_quote: "先用輕量 LLM 從問題裡抽出實體，拿去實體向量索引做相似度搜尋（門檻 0.9 以上）擴充出別名集合"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 6
  status: normal
- id: c7
  role: evaluation
  text: 整套系統的 token 消耗跟 API 成本因此壓得很低
  source_quotes:
  - "多步推論交給 SQL，LLM 只在候選集已經縮到 100 個以內時才出場，整套系統的 token 消耗跟 API 成本因此壓得很低。"
  qualifiers:
  - text: 線上 Step 1 的路徑 A 也用輕量 LLM 從問題裡抽出實體，那一步發生在候選集形成之前
    source_quote: "先用輕量 LLM 從問題裡抽出實體，拿去實體向量索引做相似度搜尋（門檻 0.9 以上）擴充出別名集合"
  anchor_type: 部落格判斷
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: 線上完全不走全域圖譜，三個步驟跑完就出答案
  source_quotes:
  - "線上完全不走全域圖譜，三個步驟跑完就出答案。"
  anchor_type: 設計參數
  importance: 8
  status: normal
- id: c9
  role: mechanism
  text: Step 1 路徑 A（實體引導的 SQL 檢索）：先用輕量 LLM 從問題裡抽出實體，拿去實體向量索引做相似度搜尋（門檻 0.9 以上）擴充出別名集合，再用 SQL 的 OR 邏輯，精確撈出關聯到其中任何一個實體的事件
  source_quotes:
  - "路徑 A（實體引導的 SQL 檢索）：先用輕量 LLM 從問題裡抽出實體，拿去實體向量索引做相似度搜尋（門檻 0.9 以上）擴充出別名集合"
  - "再用 SQL 的 OR 邏輯，精確撈出關聯到其中任何一個實體的事件。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: Step 1 路徑 B（純事件向量檢索）：把問題轉成向量，直接在事件向量庫裡撈相似度大於門檻 τ（預設 0.4）的事件；兩條路取聯集去重，B 的存在是為了保底，預防 A 的實體提取漏接
  source_quotes:
  - "路徑 B（純事件向量檢索）：同時把問題轉成向量，直接在事件向量庫裡撈相似度大於門檻 τ（預設 0.4）的事件。"
  - "兩條路取聯集去重。B 的存在是為了保底，預防 A 的實體提取漏接。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 10
  status: normal
  figures:
  - file: figures/sag/figure2.png
    article: sag
    src: figure2.png
    caption: 圖二 — SAG 的整體架構。上半部是線下攝取，下半部是線上檢索。（來源：原始論文）
    sha256: 9db14423e02bf3416e0a93908df0f2f8ff9cf663a8666313924e6dfea64bb6d2
- id: c11
  role: mechanism
  text: 種子預算 K_seed = 50：合併之後超過 50 就依向量相似度排序，只留 Top 50 進到下一步；這個機制可以想成水庫放水，上游不管來多少水，閘門開度是固定的，下游的處理量才控制得住
  source_quotes:
  - "合併之後有一道總管閥門：種子預算 K_seed = 50。超過 50 就依向量相似度排序，只留 Top 50 進到下一步。"
  - "這個機制可以想成水庫放水——上游不管來多少水，閘門開度是固定的，下游的處理量才控制得住。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 11
  status: normal
- id: c12
  role: mechanism
  text: Step 2 是「反向收集實體 → 正向撈回事件」的批次 SQL：把種子事件綁定的實體全部提出來，組成一個實體前線集合，再用批次 JOIN 撈回所有新關聯的事件，跟種子事件合併成候選池，這批事件交織出來的網絡就是那個臨時的局部超圖
  source_quotes:
  - "SAG 用的是「反向收集實體 → 正向撈回事件」的批次 SQL"
  - "把種子事件綁定的實體全部提出來，組成一個實體前線集合。"
  - "撈回所有新關聯的事件，跟種子事件合併成候選池。"
  - "這批事件當下交織出來的網絡，就是那個臨時的局部超圖。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 12
  status: normal
  figures:
  - file: figures/sag/figure2.png
    article: sag
    src: figure2.png
    caption: 圖二 — SAG 的整體架構。上半部是線下攝取，下半部是線上檢索。（來源：原始論文）
    sha256: 9db14423e02bf3416e0a93908df0f2f8ff9cf663a8666313924e6dfea64bb6d2
- id: c13
  role: mechanism
  text: 全域剪枝預算 50：前線實體超過 50 個時，計算它們跟 query 的向量相似度，強制只留 Top 50，避免高頻通用字（例如「2014年」）撈回海量無關事件
  source_quotes:
  - "如果前線裡混進「2014年」這種高頻通用字，下一步會撈回海量無關事件。所以系統設了剪枝預算 50——前線實體超過 50 個時，計算它們跟 query 的向量相似度，強制只留 Top 50。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 13
  status: normal
- id: c14
  role: mechanism
  text: Step 3 先做向量粗篩：算所有候選事件跟 query 的相似度，截取 Top 100，這是個工程妥協，用便宜的方式把 LLM 要看的量壓到可負擔範圍
  source_quotes:
  - "先做向量粗篩：算所有候選事件跟 query 的相似度，截取 Top 100。這是個工程妥協——用便宜的方式把 LLM 要看的量壓到可負擔範圍。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 14
  status: normal
- id: c15
  role: mechanism
  text: Step 3 路徑 A（LLM 結構化精選）：把這 100 個事件一起送進推理 LLM，做聯合評估（joint assessment），通盤考量哪些事件「組合起來」能構成一條多跳推論鏈，挑出最關鍵的 5 個，還原成對應的原始 chunk
  source_quotes:
  - "路徑 A（LLM 結構化精選）：把這 100 個事件一起送進推理 LLM，做聯合評估（joint assessment）——通盤考量哪些事件「組合起來」能構成一條多跳推論鏈，挑出最關鍵的 5 個，還原成對應的原始 chunk。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 15
  status: normal
- id: c16
  role: evaluation
  text: 聯合評估跟便宜的 pointwise reranker 有本質差異：pointwise 是一個一個打分，看不到事件之間的互補關係；joint assessment 看得到
  source_quotes:
  - "這跟便宜的 pointwise reranker 有本質差異：pointwise 是一個一個打分，看不到事件之間的互補關係；joint assessment 看得到。"
  anchor_type: 部落格判斷
  importance: 16
  status: normal
- id: c17
  role: mechanism
  text: Step 3 路徑 B（直接語意檢索）：拿問題向量直接去原始 chunk 向量庫撈相似度最高的 5 個；兩路聯集去重，輸出 Top 10 給生成模組
  source_quotes:
  - "拿問題向量直接去原始 chunk 向量庫撈相似度最高的 5 個。"
  - "兩路聯集去重，輸出 Top 10。"
  - "最終給生成模組的 10 個 chunk"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 17
  status: normal
  figures:
  - file: figures/sag/figure2.png
    article: sag
    src: figure2.png
    caption: 圖二 — SAG 的整體架構。上半部是線下攝取，下半部是線上檢索。（來源：原始論文）
    sha256: 9db14423e02bf3416e0a93908df0f2f8ff9cf663a8666313924e6dfea64bb6d2
- id: c18
  role: evaluation
  text: 雙軌決選設計的用意是互補：結構路徑負責召回「需要跨文件拼湊、字面相似度低」的邏輯證據，語意路徑負責召回「跟問題高度相關」的直球證據
  source_quotes:
  - "這個雙軌設計的用意是互補：結構路徑負責召回「需要跨文件拼湊、字面相似度低」的邏輯證據，語意路徑負責召回「跟問題高度相關」的直球證據。"
  anchor_type: 部落格判斷
  importance: 18
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

以下是很基本的通用詞，blog 沒有解釋，由撰寫者以一般知識補充；它們不是卡上的主張，不能當作 blog 的說法引用。

- **chunk**：把長文件切成的一小段文字，是檢索的基本單位。
- **SQL JOIN**：把兩張資料表中欄位值相同的列配對串接起來的操作。
- **Top-K**：排序後取前 K 筆結果。
- **reranker**：檢索出候選之後，再用另一個模型重新排序。
