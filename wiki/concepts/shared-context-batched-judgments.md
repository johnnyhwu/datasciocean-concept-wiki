---
id: shared-context-batched-judgments
title: 把 N 個獨立的是非判斷放進同一個 context 一起答：分數因為「看過全部對手」而可以互相比較；位置編號重疊加 attention 遮罩讓題目互不干擾、不因排第幾被偏好
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: decision-rag
  article_title: "DecisionRAG：讓決策模型沿著語料樹找資料，準確度追平 GPT-5 重排、快一個數量級"
  url: https://datasciocean.com/paper-intro/decision-rag/
  sections:
  - RAG 裡最跟不上的一環，是檢索器
  - 是非題：讀一次 context，同時回答每個候選
  - 同一張桌子：分數為什麼能互相比較
  - 讀表前要知道的資料集與指標
  - 多題共用一個 context：位置編號重疊加遮罩
  - 重點回顧：DecisionRAG 換掉了什麼、證明了什麼
  - 同一個 context 放越多候選，判斷會變差嗎？
  first_appearance: true
parent: null
related:
  - decisionrag-tree-navigation-decision-model
  - decisionrag-speedup-deployment-fairness
  - verifier-expected-value-vs-argmax
  - confidence-three-metrics
  - jevmem-small-scorer-controls-memory
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 多題共用一個 context 時，題目之間彼此看不到，但所有候選都寫在同一個 context 裡，每一題都是在「看過全部對手」的條件下作答，有更好的候選在場時，原本看起來還不錯的候選分數就會被壓低；再用「位置編號重疊 + 遮罩」消除題目順序偏差
  source_quotes:
  - "題目之間彼此看不到，但所有候選都寫在同一個 context 裡，就像所有應徵者圍著同一張桌子一起面試，每一題都是在「看過全部對手」的條件下作答。有更好的候選在場時，原本看起來還不錯的候選分數就會被壓低。"
  - "多題共用一個 context 時，用「位置編號重疊 + 遮罩」消除題目順序偏差"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 位置編號重疊加遮罩是論文自訓的開源審查員的做法；論文用的 Jev 內部是不是這樣做，論文未說明
    source_quote: "Jev 內部是不是這樣做，論文未說明"
  - text: 「消除題目排第幾的偏差」是 blog 的推論，論文未說明這個設計的動機
    source_quote: "（推論，論文未說明動機）"
  - text: 這不是數學保證：分數仍然是各自的二選一，「壓低對手」的效果要靠模型自己學會
    source_quote: "分數仍然是各自的二選一，「壓低對手」的效果要靠模型自己學會。"
  - text: 消除的是「題目排第幾」的偏差；候選內容在 context 裡的先後順序造成的偏差沒有被消除
    source_quote: "候選 1 的描述在 context 開頭、候選 200 在結尾，兩者和題目的距離不同，這部分的偏差沒有被消除"
  importance: 1
  status: normal
- id: c2
  role: context
  text: 這個做法出自 DecisionRAG：它把語料整理成一棵樹，由決策模型（不逐字寫出答案，而是直接對每個選項給出機率）每一層對所有候選各出一題 yes／no 的是非題，所有題目共用同一個 context（使用者問題加上所有候選的描述），在一次 forward pass（不逐字生成）裡全部答完
  source_quotes:
  - "把語料整理成一棵樹，從上往下每一層都由一個模型判斷哪些分支值得往下翻"
  - "這個模型論文稱為決策模型：它不逐字寫出答案，而是直接對每個選項給出機率。"
  - "每個候選各自一題 yes／no，所有題目共用同一個 context（模型這一次讀進去的全部輸入，在這裡是使用者問題加上所有候選的描述），並在一次 forward pass（模型把輸入從頭算到尾、直接得出輸出，不逐字生成）裡全部答完。"
  anchor_type: 設計參數
  qualifiers:
  - text: 論文用的決策模型 Jev 1.13 是供應商的線上服務，只能透過 API 使用，模型大小未公開
    source_quote: "論文用的 [Jev 1.13](../../ai-concept/jev-overview/) 是供應商的線上服務，只能透過 API 使用，模型大小未公開。"
  importance: 2
  status: normal
- id: c3
  role: context
  text: 適用情境：一段很長的共同前綴，後面接 N 個彼此獨立的判斷；DecisionRAG 的是非題就是這樣（問題加所有候選描述是前綴，每個候選一題接在後面），其他例子還有同一段文字的 N 個分類題、同一個 prompt 配 N 個回覆交給 reward model 打分
  source_quotes:
  - "適用情境：一段很長的共同前綴，後面接 N 個彼此獨立的判斷。DecisionRAG 的是非題就是這樣：問題加所有候選描述是前綴，每個候選一題接在後面。其他例子還有同一段文字的 N 個分類題、同一個 prompt 配 N 個回覆交給 reward model 打分。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c4
  role: qualifier
  text: 「同一張桌子」讓分數可比的效果，論文 6.2 節叫 calibration（校準），但用法比統計上的原意寬鬆，實際指的是「分數彼此可比」
  source_quotes:
  - "論文 6.2 節把這個效果叫 calibration（校準），但用法比統計上的原意寬鬆，實際指的是「分數彼此可比」。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 3
  status: normal
- id: c5
  role: anchor
  text: blog 自編的示意例子：A（真答案）與 B（相關但沒有答案）兩段，分開判斷（每個請求只放一段）時 A 0.85、B 0.88，排第一的是 B（錯）；一起判斷（同一個 context）時 A 0.93、B 0.30，排第一的是 A（對）；分開判斷時，兩個分數不是同一把尺量出來的，放在一起排序就會出錯
  source_quotes:
  - "舉個例子（自編，下表數字僅為示意）："
  - "|  | 分開判斷：每個請求只放一段 | 一起判斷：同一個 context |"
  - "| A：主角是 Leonard Shelby（真答案） | 0.85 | 0.93 |"
  - "| B：Nolan 的電影生涯（相關但沒有答案） | 0.88 | 0.30 |"
  - "| 排第一 | B（錯） | A（對） |"
  - "分開判斷時，兩個分數不是同一把尺量出來的，放在一起排序就會出錯。"
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 3
  status: normal
- id: c6
  role: evidence
  text: 固定難度、只改請求大小（論文 6.2 節，Natural Questions 289 題）：每題固定 200 個候選，拆成每個請求 m 個再合併排序，Hit@1（第一名剛好是正確段落之一的題目比例）從每請求 1 個的 47.8% 升到 50 個的 54.3%，到 100、200 個都持平
  source_quotes:
  - "固定難度，只改請求大小（論文 6.2 節，NQ 289 題）：每題固定 200 個候選，拆成每個請求 \\( m \\) 個，再合併排序。Hit@1 從每請求 1 個的 47.8% 升到 50 個的 54.3%，到 100、200 個都持平"
  - "Hit@1：第一名剛好是正確段落之一的題目比例"
  - "Natural Questions（NQ）"
  anchor_type: 實驗結果
  comparison_target: 同樣 200 個候選、每個請求只放 1 個（分開判斷）
  qualifiers:
  - text: 一個請求放越多候選不會變差，是在論文測過的範圍內
    source_quote: "在論文測過的範圍內不會，從 1 個加到大約 50 個反而變好，之後持平。"
  - text: 排序只測到 200 個候選
    source_quote: "排序只測到 200 個候選"
  importance: 2
  status: normal
  figures:
  - file: figures/decision-rag/figure6.png
    article: decision-rag
    src: figure6.png
    caption: 圖 4 — 固定 200 個候選、拆成每個請求 m 個時，Natural Questions 的 Hit@1（289 題，色帶為 95% 區間）（來源：原始論文 Figure 6。）
    sha256: 6a1e424030042d182ab11e27e934f9e1803a0a7009b52c92388f5bfeee172132
- id: c7
  role: mechanism
  text: 論文說明的是它自訓的開源審查員（Appendix G）：以 Qwen3-Base 為底，把輸出頭換成直接算出 yes 機率的評分頭；輸入排法是每個候選一題，題目後面接「no」「yes」兩個選項，全部接在共享 context 之後
  source_quotes:
  - "論文說明的是它自訓的開源審查員（Appendix G）：以 Qwen3-Base 為底，把輸出頭（模型最後負責吐出下一個字的那一層）換成評分頭（直接算出 yes 機率的一層，算法見本節最後的摺疊）。它的輸入排法是每個候選一題，題目後面接「no」「yes」兩個選項，全部接在共享 context 之後。"
  anchor_type: 設計參數
  qualifiers:
  - text: 論文用的 Jev 內部是不是這樣做，論文未說明
    source_quote: "Jev 內部是不是這樣做，論文未說明"
  importance: 4
  status: normal
- id: c8
  role: mechanism
  text: 要讓這些題目互不干擾，靠兩件事一起做：位置編號（模型被告知每個 token 在序列裡排第幾格）讓每一題都從 context 結束處起算；attention 遮罩（規定每個 token 能看見哪些 token）讓題目之間彼此不能互看
  source_quotes:
  - "要讓這些題目互不干擾，靠的是兩件事一起做：位置編號（模型被告知每個 token 在序列裡排第幾格）讓每一題都從 context 結束處起算，attention 遮罩（規定每個 token 能看見哪些 token）讓題目之間彼此不能互看（論文 Appendix G）。"
  anchor_type: 設計參數
  qualifiers:
  - text: 這是論文自訓的開源審查員的做法；Jev 內部是不是這樣做，論文未說明
    source_quote: "Jev 內部是不是這樣做，論文未說明"
  importance: 2
  status: normal
- id: c9
  role: anchor
  text: blog 自編的長度例子：context 佔序列格子 0–999、位置編號 0–999；題目 1 佔格子 1000–1019、位置編號 1000–1019；題目 2 實際排在題目 1 後面（格子 1020–1044），但給模型的位置編號是 1000–1024，與題目 1 重疊
  source_quotes:
  - "用（自編）的長度舉例："
  - "| context | 0–999 | 0–999 |"
  - "| 題目 1 | 1000–1019 | 1000–1019 |"
  - "| 題目 2 | 1020–1044（排在題目 1 後面） | 1000–1024（與題目 1 重疊） |"
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 4
  status: normal
- id: c10
  role: mechanism
  text: 位置編號重疊讓每一題感受到的「自己和 context 的距離」，都和「只有這一題」時一樣；attention 遮罩讓題目 2 看不到題目 1，少了它，題目 2 會讀到題目 1 的內容，就不再是獨立判斷
  source_quotes:
  - "位置編號重疊：每一題感受到的「自己和 context 的距離」，都和「只有這一題」時一樣。"
  - "attention 遮罩：題目 2 看不到題目 1。少了它，題目 2 會讀到題目 1 的內容，就不再是獨立判斷。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 3
  status: normal
- id: c11
  role: mechanism
  text: blog 推論為什麼要這樣設計：如果位置照實際順序往後排，越後面的題目離 context 越遠，模型可能偏好或壓低後面的候選；全部從同一個位置起算，題目在位置上就對稱了，「題目排第幾」的偏差就此消除
  source_quotes:
  - "為什麼要這樣設計？（推論，論文未說明動機）如果位置照實際順序往後排，越後面的題目離 context 越遠，模型可能偏好或壓低後面的候選。全部從同一個位置起算，題目在位置上就對稱了，「題目排第幾」的偏差就此消除。"
  anchor_type: 部落格推論
  qualifiers:
  - text: 論文沒有說明這個設計的動機，這是 blog 的推論
    source_quote: "（推論，論文未說明動機）"
  importance: 3
  status: normal
- id: c12
  role: qualifier
  text: 候選內容的先後順序造成的偏差還在：候選 1 的描述在 context 開頭、候選 200 在結尾，兩者和題目的距離不同，這部分的偏差沒有被消除，論文也沒測過打亂候選順序會怎樣；選項「no」「yes」的位置編號怎麼排，論文也沒交代
  source_quotes:
  - "候選 1 的描述在 context 開頭、候選 200 在結尾，兩者和題目的距離不同，這部分的偏差沒有被消除，論文也沒測過打亂候選順序會怎樣。另外，選項「no」「yes」的位置編號怎麼排，論文也沒交代。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 3
  status: normal
- id: c13
  role: mechanism
  text: blog 把它變成通用做法，三步要一起做、位置編號和遮罩缺一不可：把前綴和 N 個分支串成一條序列；每個分支的位置編號都從前綴結束處重新起算；加 attention 遮罩，每個分支只看得到前綴和自己。算出來的結果等同於把「前綴 + 第 i 個分支」分開跑 N 次，但前綴只算一次；好處是前綴的計算共用，而且每個分支與前綴的相對距離相同
  source_quotes:
  - "把它變成一個通用做法，下面三步要一起做，位置編號和遮罩缺一不可："
  - "把前綴和 N 個分支串成一條序列。"
  - "每個分支的位置編號，都從前綴結束處重新起算。"
  - "加 attention 遮罩：每個分支只看得到前綴和自己，看不到其他分支。"
  - "算出來的結果等同於把「前綴 + 第 \\( i \\) 個分支」分開跑 N 次，但前綴只算一次。"
  - "但前綴只算一次。好處是前綴的計算共用，而且每個分支與前綴的相對距離相同，不會因為排第幾而被偏好或壓低。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c14
  role: qualifier
  text: 這個通用做法有三個限制：前綴內部的順序偏差還在；需要能自己控制位置編號和遮罩，也就是要有開源權重，API 模型做不到；前綴很長時，attention 計算量隨長度平方成長，省下來的部分可能被抵消
  source_quotes:
  - "前綴內部的順序偏差還在（就是上面那個候選先後的問題）。"
  - "需要能自己控制位置編號和遮罩，也就是要有開源權重；API 模型做不到。"
  - "前綴很長時，attention 計算量隨長度平方成長，省下來的部分可能被抵消。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c15
  role: evidence
  text: 非常長的 context（論文 Appendix F，MTRAG 188 輪）：篩 8,578 個頁面標題時，「每請求最多 150k tokens」和「最多 10k tokens」兩種拆法的 R@5 與 nDCG@5（會考慮名次的排序品質指標）只差 −0.7 和 −0.2 點，信賴區間都包含 0
  source_quotes:
  - "非常長的 context（論文 Appendix F，MTRAG 188 輪）：篩 8,578 個頁面標題時，比較「每請求最多 150k tokens」和「最多 10k tokens」兩種拆法，R@5 與 nDCG@5（會考慮名次的排序品質指標）只差 −0.7 和 −0.2 點，信賴區間都包含 0。"
  anchor_type: 實驗結果
  comparison_target: 同一批頁面標題、每請求最多 10k tokens 的拆法
  qualifiers:
  - text: 長 context 只測了「篩頁面標題」這一種任務
    source_quote: "長 context 也只測了「篩頁面標題」這一種任務。"
  importance: 3
  status: normal
- id: c16
  role: evidence
  text: 候選池從 5 長到 1,000 時，Hit@1 整體變低（1,000 個時 47.6%），但池子變大時會混進更多 hard negative（看起來很像答案、其實不是的段落），題目本身變難了，不能拿來當「context 變長會傷品質」的證據；該看的是同樣的池子大小下，一起判斷一直勝過分開判斷
  source_quotes:
  - "候選池從 5 長到 1,000 時，Hit@1 一路下降（1,000 個時 47.6%）。但池子變大時會混進更多 hard negative（看起來很像答案、其實不是的段落），題目本身變難了，不能拿來當「context 變長會傷品質」的證據。這張圖該看的是：同樣的池子大小下，一起判斷一直勝過分開判斷。"
  anchor_type: 部落格判斷
  comparison_target: 同樣池子大小下的分開判斷；1,000 個時的 47.6% 是對池子較小時的分數而言
  qualifiers:
  - text: 這組結果是在 Natural Questions 上、150 題
    source_quote: "候選池變大、所有候選在同一個請求裡一起打分時，Natural Questions 的 Hit@1（150 題）"
    source: figure_caption
  importance: 3
  status: normal
  figures:
  - file: figures/decision-rag/figure5.png
    article: decision-rag
    src: figure5.png
    caption: 圖 5 — 候選池變大、所有候選在同一個請求裡一起打分時，Natural Questions 的 Hit@1（150 題）（來源：原始論文 Figure 5。）
    sha256: c530c3d6d6b4091f19e0309517a627783a22b9b0eaa263ef1d92586f29e47fba
- id: c17
  role: qualifier
  text: 每題 yes／no 的絕對正確率論文沒測，只測了排序；blog 推論 P(Yes) 的絕對值可能會隨 context 長度漂移、卻不影響排序，所以如果要拿 P(Yes) 去對門檻值，這件事沒有被驗證過
  source_quotes:
  - "每題 yes／no 的絕對正確率論文沒測，只測了排序。（推論）\\( P(\\text{Yes}) \\) 的絕對值可能會隨 context 長度漂移，卻不影響排序，所以如果要拿 \\( P(\\text{Yes}) \\) 去對門檻值，這件事沒有被驗證過。"
  anchor_type: 部落格推論
  importance: 4
  status: normal
```


## 名詞補充（通用知識，非 blog 內容）

以下是很基本的通用詞，blog 沒有解釋，由撰寫者以一般知識補充；它們不是卡上的主張，不能當作 blog 的說法引用。
- **R@5（Recall@5）**：正確答案中有幾成出現在排序的前 5 名。
- **reward model**：替模型輸出打分數的模型，常用來判斷哪個回覆比較好。
