---
id: persona-d2s-training-design-flaws
title: Persona-Aware-D2S 的訓練設計站不住腳：偏好微調的關鍵細節缺漏、每種條件各訓一個模型無法隨維度擴展、80 筆小樣本，偏好微調也不是無條件的提升
type_hint: 判斷
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
  - 偏好微調（P-F）
  - 效果如何：端到端評測
  - 論文沒提、但我認為存在的問題
  - 工程落地：哪些該抄，哪些別碰
  first_appearance: true
parent: null
related:
  - persona-d2s-task-and-pipeline
  - persona-d2s-what-to-borrow
  - decision-transformer-reward-conditioning
  - bradley-terry-pairwise-preference
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: Persona-Aware-D2S 的訓練設計有站不住腳的地方：訓練資料規模很小、reward model 沒做容量消融、四種 persona 各訓一個模型的架構無法隨 persona 維度擴展；偏好微調的關鍵細節也沒有交代，效果並非無條件的提升
  source_quotes:
  - 站不住腳的地方：訓練資料規模很小（大綱生成只有 80 筆樣本、dev split 僅 5 篇論文）、reward model 只有 66M 參數且沒做容量消融、四種 persona 各訓一個模型的架構無法隨 persona 維度擴展。
  - 這至少說明偏好微調不是無條件的提升
  - 論文在這一步略過了兩個細節
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 1
  status: normal
- id: c2
  role: context
  text: Persona-Aware-D2S 的第一階段要生成投影片大綱：先做監督微調（SFT，用 cross-entropy loss 最小化生成標題與 ground-truth 標題之間的差距），再做偏好微調；SFT-F 是純監督微調，P-F 是再加上偏好微調的版本
  source_quotes:
  - 它分成兩步走：先做監督微調，再做偏好微調。
  - 做法本身很標準：用 cross-entropy loss，最小化生成標題與 ground-truth 標題之間的差距。
  - SFT-F 是純監督微調，P-F 是再加上偏好微調的版本
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 2
  status: normal
- id: c3
  role: context
  text: 論文訓練的是四個獨立模型，分別對應四種 persona 組合（受眾為專家或非專家、長度為長或短），而不是訓練單一模型、把受眾和長度當成 prompt 裡的條件
  source_quotes:
  - 論文訓練的是四個獨立模型，分別對應四種 persona 組合
  - 而不是訓練單一模型、把 … 當成 prompt 裡的條件。
  - 受眾背景：專家 / 非專家
  - 簡報長度：長 / 短
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 3
  status: normal
- id: c4
  role: context
  text: 偏好微調是為了處理單一 gold standard 撐不起多元偏好的問題：以最大化與單一 gold reference 的相似度為目標的最大概似（MLE）訓練，預設「只有一種正確答案」，跟 persona 問題本質上的「一對多」直接衝突
  source_quotes:
  - 這一步是為了處理前面的挑戰 3：單一 gold standard 撐不起多元偏好。
  - 這種最大概似（MLE）訓練預設「只有一種正確答案」，跟 persona 問題本質上的「一對多」直接衝突
  anchor_type: 部落格判斷
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 偏好微調的第一段是收集人類偏好資料：用 SFT 模型生成 5 組候選大綱，3 位專家對專家的兩種配置（長 vs 短）做成對排序，3 位非專家對非專家的兩種配置做同樣的事
  source_quotes:
  - 四個 \( \pi_{SFT} \) 各自用不同的 temperature、top-K、top-p 生成 5 組候選大綱；3 位專家負責對專家的兩種配置（長 vs 短）做成對排序，3 位非專家對非專家的兩種配置做同樣的事。
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 5
  status: normal
- id: c6
  role: mechanism
  text: 評分準則有兩個：對目標受眾的可理解度（comprehensibility），以及長度上的滿意度；只有多數決有共識的樣本會被保留，沒共識的直接丟掉
  source_quotes:
  - 評分準則有兩個：對目標受眾的可理解度（comprehensibility），以及長度上的滿意度。只有多數決有共識的樣本會被保留，沒共識的直接丟掉。
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: 第二段是用 Bradley-Terry loss 訓練 reward model（給候選輸出打分的模型）；因為評分準則有兩個、受眾有兩種，最後會得到四個 reward model：專家的可理解度與長度、非專家的可理解度與長度
  source_quotes:
  - 第二段是訓練 reward model，用的是 Bradley-Terry loss
  - 因為評分準則有兩個、受眾有兩種，最後會得到四個 reward model
  - 用 reward model 給每組打分
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: 第三段是最終的偏好微調，借用 Decision Transformer 的 reward-conditioning：從 train set 抽 prompt，用 SFT 模型生成 5 組大綱，用 reward model 給每組打分，得到「(prompt, reward) → 大綱」的訓練配對，再拿這批配對去微調 LLM；本質上仍然是監督學習，只是輸入裡多塞了一個 reward 當條件，推論時直接把「最大 reward 值」餵進去，讓模型生成對應高分的大綱
  source_quotes:
  - 步驟是：從 train set 抽 prompt，用 … 生成 5 組大綱，用 reward model 給每組打分，得到「(prompt, reward) → 大綱」這樣的訓練配對，再拿這批配對去微調 LLM。本質上仍然是監督學習，只是輸入裡多塞了一個 reward 當條件。推論時就直接把「最大 reward 值」餵進去，讓模型生成對應高分的大綱。
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 8
  status: normal
- id: c9
  role: evaluation
  text: 論文在偏好微調略過了兩個細節：所謂的「maximum reward」具體數值怎麼來（是訓練資料裡的觀察最大值，還是手動設的常數），以及兩個 reward 分數是合併成單一純量、還是兩個都塞進 prompt；缺了這些要複現會很痛苦
  source_quotes:
  - 論文在這一步略過了兩個細節：所謂的「maximum reward」具體數值怎麼來（是訓練資料裡的觀察最大值？還是手動設的常數？），以及兩個 reward 分數是合併成單一純量、還是兩個都塞進 prompt。缺了這些要複現會很痛苦。
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 9
  status: normal
- id: c10
  role: evaluation
  text: reward model 用的是 distilbert-base-cased，一個約 66M 參數的小型 encoder；「這段大綱對非專家好不好懂」是相當吃語意理解的判斷，這種 capacity 夠不夠，論文沒有做任何消融驗證
  source_quotes:
  - reward model 用的是 distilbert-base-cased，一個約 66M 參數的小型 encoder。「這段大綱對非專家好不好懂」是相當吃語意理解的判斷，這種 capacity 夠不夠，論文沒有做任何消融驗證。
  anchor_type: 部落格判斷
  comparison_target: 沒有與其他容量的 reward model 比較（論文沒有做容量消融驗證）
  importance: 10
  status: normal
- id: c11
  role: anchor
  text: 大綱生成的訓練資料規模很袖珍：train split 只有 20 篇論文，乘上 4 種配置等於 80 筆訓練樣本，拿去微調 GPT-3.5-turbo；dev split 僅 5 篇論文
  source_quotes:
  - 訓練規模則相當袖珍：train split 只有 20 篇論文，乘上 4 種配置等於 **80 筆訓練樣本**，拿去微調 GPT-3.5-turbo
  - 大綱生成只有 80 筆樣本、dev split 僅 5 篇論文
  anchor_type: 部落格考證
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 11
  status: normal
- id: c12
  role: evaluation
  text: 小樣本微調很容易 overfit 到這批論文的寫作風格，換 domain 的泛化能力存疑
  source_quotes:
  - 小樣本微調很容易 overfit 到這批論文的寫作風格，換 domain 的泛化能力存疑
  anchor_type: 部落格判斷
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: 四個獨立模型這個選擇在效果上也許更乾淨，但代價很大；四種 persona 配置要訓練 4 個獨立 SFT 模型加 4 組 reward model，如果要再加一個 persona 維度（例如角色：PM／工程師／主管），模型數量是乘法成長，完全不 scalable
  source_quotes:
  - 這個選擇在效果上也許更乾淨，但代價很大
  - 四種 persona 配置要訓練 4 個獨立 SFT 模型加 4 組 reward model。如果要再加一個 persona 維度（例如角色：PM／工程師／主管），模型數量是乘法成長，完全不 scalable
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 13
  status: normal
- id: c14
  role: evaluation
  text: 在端到端評測裡，SFT-F 與 P-F 全面壓過 zero-shot 和 few-shot baseline；P-F 在多數配置勝出，但 Expert-Short 這個配置例外，反而是純監督微調較好（R-1：SFT-F 0.17 對 P-F 0.13）
  source_quotes:
  - SFT-F 與 P-F 全面壓過 zero-shot 和 few-shot baseline，差距不小。
  - P-F 在多數配置勝出，但 **Expert-Short** 這個配置例外，反而是純監督微調更好（R-1：SFT-F 0.17 vs P-F 0.13）。論文的解讀是純監督微調在「為專家做精簡摘要」這件事上表現更好。不管解讀對不對，這至少說明偏好微調不是無條件的提升。
  anchor_type: 實驗結果
  comparison_target: Expert-Short 配置下，純監督微調（SFT-F）對加上偏好微調的版本（P-F）
  qualifiers:
  - text: 論文把這個差異解讀為純監督微調在「為專家做精簡摘要」這件事上表現更好；blog 說不管解讀對不對，這至少說明偏好微調不是無條件的提升
    source_quote: 論文的解讀是純監督微調在「為專家做精簡摘要」這件事上表現更好。不管解讀對不對，這至少說明偏好微調不是無條件的提升。
  importance: 14
  status: normal
- id: c15
  role: evaluation
  text: 論文的實驗涵蓋面相當完整（模組級評測、端到端評測、消融實驗、質化分析都有），問題是規模不足而不是沒有做：質化分析 10 篇、認知負荷研究 3 位專家、消融實驗 10 篇，每一項的樣本數都撐不起太強的統計結論
  source_quotes:
  - 質化分析 10 篇、認知負荷研究 3 位專家、消融實驗 10 篇，統計效力偏低
  - 這是「規模不足」而不是「沒有做」。論文的實驗涵蓋面其實相當完整，模組級評測、端到端評測、消融實驗、質化分析都有，只是每一項的樣本數都撐不起太強的統計結論。
  anchor_type: 部落格判斷
  comparison_target: blog 只判斷這些樣本數撐不起太強的統計結論，沒有給具體的對照數字
  importance: 15
  status: pending_author_confirmation
- id: c16
  role: evaluation
  text: 「每種條件訓練一個獨立模型」的 Stage 1 與 Stage 2 第二步架構落地可行性低，訓練與維運成本隨 persona 維度乘法成長，不建議直接複現；小樣本 SFT 本身風險也偏高，除非任務是「教模型輸出格式或風格」而不是「教模型新知識」，前者小樣本有機會，後者基本無望
  source_quotes:
  - 訓練與維運成本隨 persona 維度乘法成長，不建議直接複現
  - 不建議複現：Stage 1 與 Stage 2 第二步的「每種條件訓練一個獨立模型」架構。小樣本 SFT 本身風險也偏高，除非你的任務也是「教模型輸出格式或風格」而不是「教模型新知識」——前者小樣本有機會，後者基本無望。
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 16
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

以下是很基本的通用詞，blog 沒有解釋，由撰寫者以一般知識補充；它們不是卡上的主張，不能當作 blog 的說法引用。

- **temperature、top-K、top-p**：控制語言模型生成時隨機程度的取樣參數。temperature 越高，輸出越多樣；top-K 只從機率最高的 K 個候選 token 中取樣；top-p 只從累積機率達到 p 的最小候選集合中取樣。大綱調整這三個參數，是為了讓同一個模型產生內容不同的候選大綱。
- **ROUGE**：比對生成結果與參考答案字詞重疊程度的指標；ROUGE-1（R-1）看單字層級的重疊。
- **encoder**：把輸入文字轉成向量表示的 Transformer 模型；distilbert 是 BERT 的縮小版。
- **zero-shot / few-shot baseline**：不微調，只靠 prompt（不給範例或只給少數範例）讓模型完成任務的對照組。
- **PPO、RLHF、cross-entropy loss**：見 persona-d2s-task-and-pipeline 卡的名詞補充。
