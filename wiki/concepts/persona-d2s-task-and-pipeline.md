---
id: persona-d2s-task-and-pipeline
title: 把受眾與長度變成模型的輸入條件，同一份文件就能長出不同的投影片；Persona-Aware-D2S 的貢獻在任務定義與資料集，方法是現成技術的拼裝
type_hint: 方法
context_type: bound_to_source
sources:
- article: persona-aware-d2s
  article_title: "拆解 Persona-Aware-D2S：同一份文件，怎麼依受眾和長度長出不同簡報"
  url: https://datasciocean.com/paper-intro/persona-aware-d2s/
  sections:
  - 前言
  - 這個任務為什麼值得被重新定義
  - 先把符號講清楚
  - Stage 1：生成帶 persona 的投影片大綱
  - 監督微調（SFT-F）
  - Stage 2：抽出每張投影片該放的內容
  - Stage 3：摘要與邏輯重排
  - Decision Transformer：把強化學習包裝成序列預測
  - 效果如何：端到端評測
  - 論文自己承認的限制
  - 論文沒提、但我認為存在的問題
  - 工程落地：哪些該抄，哪些別碰
  - 結論
  first_appearance: true
parent: null
related:
  - persona-d2s-training-design-flaws
  - persona-d2s-what-to-borrow
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: Persona-Aware-D2S 把受眾（專家／非專家）和長度（長版／短版）變成模型的輸入條件，讓同一份文件長出四種投影片內容；它的貢獻主要在這個任務定義與對應的平行資料集，方法本身是現成技術的拼裝
  source_quotes:
  - 把「同一份文件，依受眾（專家／非專家）和長度（長版／短版）生成四種投影片內容」這件事變成一個定義清楚的任務，並建立了對應的平行資料集。
  - 這篇論文的貢獻主要在任務定義與資料集，方法本身是現成技術的拼裝
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  qualifiers:
  - text: 實作上是為四種 persona 組合各訓練一個獨立模型，而不是訓練單一條件式模型
    source_quote: 但實作上是為四種 persona 組合各訓練一個獨立模型，而不是訓練單一條件式模型。
  importance: 1
  status: normal
- id: c2
  role: context
  text: 市面上的「文件轉投影片」（document-to-slides，簡稱 D2S）系統幾乎都是單一輸出：文件丟進去，吐出來的永遠是同一份大綱
  source_quotes:
  - 但市面上的「文件轉投影片」（document-to-slides，以下簡稱 D2S）系統幾乎都是單一輸出：文件丟進去，吐出來的永遠是同一份大綱。
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 2
  status: normal
- id: c3
  role: context
  text: EACL 2024 的 Persona-Aware-D2S 把「受眾是不是專家」「簡報要長還是短」變成模型的輸入條件，讓同一份文件長出四種版本的投影片內容；blog 稱這四種版本對應四種 persona 組合
  source_quotes:
  - EACL 2024 的 Persona-Aware-D2S 想補上這個缺口。它把「受眾是不是專家」「簡報要長還是短」變成模型的輸入條件，讓同一份文件長出四種版本的投影片內容
  - 受眾背景：專家 / 非專家
  - 簡報長度：長 / 短
  - 分別對應四種 persona 組合
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  qualifiers:
  - text: 實作上是為四種 persona 組合各訓練一個獨立模型，而不是訓練單一條件式模型
    source_quote: 但實作上是為四種 persona 組合各訓練一個獨立模型，而不是訓練單一條件式模型。
  importance: 3
  status: normal
- id: c4
  role: context
  text: 講給同領域的研究者聽，會直接跳進模型架構；講給業務主管聽，得先講清楚這東西能解決什麼問題，架構細節反而是干擾
  source_quotes:
  - 講給同領域的研究者聽，你會直接跳進模型架構；講給業務主管聽，你得先講清楚這東西能解決什麼問題，架構細節反而是干擾。
  anchor_type: 部落格舉例
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 方法是三階段 pipeline：大綱生成 → 內容抽取 → 摘要與重排；前兩階段用監督微調（SFT）加上借自 Decision Transformer 的輕量偏好微調（reward-conditioning）
  source_quotes:
  - 三階段 pipeline（大綱生成 → 內容抽取 → 摘要與重排），前兩階段用監督微調加上借自 Decision Transformer 的輕量偏好微調（reward-conditioning）
  anchor_type: 設計參數
  importance: 5
  status: normal
- id: c6
  role: context
  text: 輕量偏好微調借用 Decision Transformer 的「reward-conditioned generation」這個訓練技巧：把 reward 當條件塞進輸入，用監督學習訓練，藉此繞開 PPO（RLHF 主流的強化學習演算法）那套基礎設施的複雜度
  source_quotes:
  - 它只借用了「reward-conditioned generation」這個訓練技巧——把 reward 當條件塞進輸入，用監督學習訓練，藉此繞開 PPO 的基礎設施複雜度。
  - 訓練上用 SFT 搭配一種借自 Decision Transformer 的輕量偏好微調，繞開 PPO（RLHF 主流的強化學習演算法）那套基礎設施。
  anchor_type: 設計參數
  qualifiers:
  - text: 這是不完整的挪用：Decision Transformer 真正的威力在於處理多步驟、有前後因果關係的序列決策，而 Persona-Aware-D2S 的場景是單次生成，沒有多步驟決策結構
    source_quote: 但這是個**不完整的挪用**。Decision Transformer 真正的威力在於處理多步驟、有前後因果關係的序列決策
  importance: 6
  status: normal
- id: c7
  role: context
  text: 監督微調（SFT）用 cross-entropy loss，最小化生成標題與 ground-truth 標題之間的差距；SFT-F 是純監督微調，P-F 是再加上偏好微調的版本
  source_quotes:
  - 做法本身很標準：用 cross-entropy loss，最小化生成標題與 ground-truth 標題之間的差距。
  - SFT-F 是純監督微調，P-F 是再加上偏好微調的版本
  anchor_type: 設計參數
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: Stage 1 的目標是給定論文內容加上 persona 條件，生成投影片的標題序列，也就是大綱；做法分兩步：先做監督微調，再做偏好微調
  source_quotes:
  - 這一階段的目標是給定論文內容加上 persona 條件，生成投影片的標題序列
  - 投影片標題序列，也就是大綱
  - 它分成兩步走：先做監督微調，再做偏好微調。
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 8
  status: normal
- id: c9
  role: mechanism
  text: Stage 2 為每個標題找出對應的句子和圖表 caption，分兩步：先用便宜的方式把候選範圍縮小，再用訓練過的模型從候選裡挑內容
  source_quotes:
  - 有了大綱之後，要為每個標題找出對應的句子和圖表 caption
  - 這階段分成兩步：先用便宜的方式把候選範圍縮小，再用訓練過的模型從候選裡挑內容。
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: Stage 3 負責把前兩階段抽出的零散句子片段整理成連貫的最終輸出：用兩步驟 prompting，先把抽出的內容摘要成 bullet points，再把這些 bullet points 丟回 LLM，要求它在同一標題內部、或跨標題之間重新排列，讓順序更符合聽眾的理解節奏
  source_quotes:
  - 前兩階段抽出來的是零散的句子片段，直接貼上投影片會很難讀。Stage 3 負責把它整理成連貫的最終輸出
  - 機制是兩步驟 prompting：先把 … 的內容摘要成 bullet points，再把這些 bullet points 丟回 LLM，要求它在同一標題內部、或跨標題之間重新排列，讓順序更符合聽眾的理解節奏。
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 10
  status: normal
- id: c11
  role: mechanism
  text: blog 把論文在 §1 和相關研究裡談的問題攤開來看，是五個彼此有依賴關係的挑戰：單一輸出無法因應不同受眾、無法因應時長限制、訓練目標跟人類的多元偏好不對齊、抽取式方法內容不連貫、缺乏可訓練與評測的資料集
  source_quotes:
  - 把論文在 §1 和相關研究裡談的問題攤開來看，其實是五個彼此有依賴關係的挑戰
  - 單一輸出，無法因應不同受眾
  - 無法因應時長限制
  - 訓練目標跟人類的多元偏好不對齊
  - 抽取式方法內容不連貫
  - 缺乏可訓練與評測的資料集
  anchor_type: 部落格考證
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 11
  status: normal
- id: c12
  role: mechanism
  text: 這五個挑戰不是平行並列的：缺資料集（挑戰 5）是前提，沒有資料就談不上條件式生成；有了資料才能把挑戰 1、2 的條件變成模型輸入；一旦要訓練條件式模型，就必須面對挑戰 3（單一 reference 撐不起多元偏好）；挑戰 4 是獨立的內容品質問題，跟 persona 無關但同樣得解
  source_quotes:
  - 這五點不是平行並列的。挑戰 5 是前提：沒有資料就談不上條件式生成；有了資料才能把挑戰 1、2 的條件變成模型輸入；而一旦要訓練這種條件式模型，就必須面對挑戰 3（單一 reference 撐不起多元偏好）。挑戰 4 則是獨立的內容品質問題，跟 persona 無關但同樣得解。
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 12
  status: normal
- id: c13
  role: mechanism
  text: 文件中的圖表在形式化裡寫成「圖片加 caption」，但模型實際上只吃 caption 這段文字，圖片本身從頭到尾沒有被理解過
  source_quotes:
  - 雖然寫成「圖片 + caption」，但模型實際上只吃 caption 這段文字，圖片本身從頭到尾沒有被理解過。
  anchor_type: 部落格考證
  importance: 13
  status: normal
- id: c14
  role: evaluation
  text: 論文自己承認的限制包括：大部分技術術語需要額外解釋才能讓非專家理解，但模型在這方面能力有限；完全依賴人類撰寫的圖表 caption，不會生成原創圖表，也不理解圖片本身的內容；只能產生 bullet-point 格式的文字摘要，不涉及任何排版設計
  source_quotes:
  - 論文的 Limitations 章節列了五點
  - 大部分技術術語需要額外解釋才能讓非專家理解，但模型在這方面能力有限。
  - 完全依賴人類撰寫的圖表 caption，不會生成原創圖表，也不理解圖片本身的內容。
  - 只能產生 bullet-point 格式的文字摘要，不涉及任何排版設計。
  anchor_type: 原作者解讀
  importance: 14
  status: normal
- id: c15
  role: evaluation
  text: 論文自承限制的第 3 點（完全依賴人類撰寫的圖表 caption、不會生成原創圖表、不理解圖片本身的內容）和第 4 點（只能產生 bullet-point 文字摘要、不涉及排版設計）加起來，決定了這個系統的輸出離「可以直接開場報告的投影片」還有很長一段距離；輸出是結構化文字大綱，不是能直接用的簡報
  source_quotes:
  - 第 3 點和第 4 點加起來，其實就決定了這個系統的輸出離「可以直接開場報告的投影片」還有很長一段距離。
  - 完全依賴人類撰寫的圖表 caption，不會生成原創圖表，也不理解圖片本身的內容。
  - 只能產生 bullet-point 格式的文字摘要，不涉及任何排版設計。
  - 完全不含排版、顏色、字體，本質上輸出的是結構化文字大綱，不是能直接用的簡報
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 15
  status: normal
- id: c16
  role: evaluation
  text: 方法論本身沒有原創性：SFT 加上 RLHF-lite 的組合，是把 Christiano et al. (2017) 的 reward modeling 和 Chen et al. (2021) 的 reward-conditioning 拼裝起來，而且後者還只借了表層技巧
  source_quotes:
  - 但方法論本身沒有原創性——SFT 加上 RLHF-lite 的組合，是把 Christiano et al. (2017) 的 reward modeling 和 Chen et al. (2021) 的 reward-conditioning 拼裝起來，而且後者還只借了表層技巧。
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 日期
  qualifiers:
  - text: 這是不完整的挪用：Decision Transformer 真正的威力在於處理多步驟、有前後因果關係的序列決策，而 Persona-Aware-D2S 的場景是單次生成，沒有多步驟決策結構
    source_quote: 但這是個**不完整的挪用**。Decision Transformer 真正的威力在於處理多步驟、有前後因果關係的序列決策
  importance: 16
  status: normal
- id: c17
  role: evaluation
  text: 這個問題定義本身很有價值，論文能上 EACL 2024 long paper 也主要吃在這裡；整體來說，這篇論文更適合當作「問題定義」的參考，而不是「解決方案」的參考
  source_quotes:
  - 這個問題定義本身很有價值，論文能上 EACL 2024 long paper 也主要吃在這裡。
  - 整體來說，這篇論文更適合當作「問題定義」的參考，而不是「解決方案」的參考
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 17
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

以下是很基本的通用詞，blog 沒有解釋，由撰寫者以一般知識補充；它們不是卡上的主張，不能當作 blog 的說法引用。

- **cross-entropy loss**：分類與語言模型訓練最常用的損失函數，衡量模型預測的機率分布與正確答案之間的差距。
- **ground-truth**：資料集中人工標註的標準答案。
- **PPO**：一種常用的強化學習演算法，RLHF 傳統上用它來更新模型；需要額外的 reward 模型與線上取樣，基礎設施較複雜。
- **RLHF**：用人類偏好訓練出 reward 模型，再用強化學習讓語言模型朝高 reward 的方向調整的對齊做法。
