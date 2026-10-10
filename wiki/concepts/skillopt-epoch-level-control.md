---
id: skillopt-epoch-level-control
title: 逐步修改天生短視，所以每個 epoch 要另設一層慢速控制：用 A/B 對照抓累積的退步，並讓優化器自己越來越會優化
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: skillopt
  article_title: "SkillOpt：把 AI Agent 的技能文件當成可訓練的權重來優化，不用碰模型本身"
  url: https://datasciocean.com/paper-intro/skillopt/
  sections:
  - 兩個模型，各司其職
  - 目標模型（M）
  - 優化器模型（O）
  - 動手修改之前，先收集證據
  - 真正做出決定的守門員
  - 每個 Epoch 結束時的宏觀調控
  - 慢速更新：受保護的 Epoch 層級記憶
  - 元技能：教優化器學會優化
  - 評分函式的瓶頸
  - 優化器強度：一定要前沿等級嗎？
  first_appearance: true
parent: null
related:
  - skillopt-overview
  - skillopt-blind-acceptance-gate
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 逐步的修改在設計上本來就是短視的，每一步都只針對最近這一批任務做出反應；為了抓住更長時程的退步，SkillOpt 加入第二層、比較慢的控制迴圈，每個 Epoch 才跑一次，而不是每個 Step 都跑
  source_quotes:
  - 逐步的修改在設計上本來就是短視的——每一步都只針對最近這一批 40 個任務做出反應。為了抓住更長時程的退步，SkillOpt 加入了第二層、比較慢的控制迴圈，每個 Epoch 才跑一次，而不是每個 Step 都跑。
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: SkillOpt 把責任拆分給兩個獨立的模型：凍結的目標模型負責實際執行工作，唯一會改變的是它的技能文件；優化器模型只在離線訓練階段運作，讀取目標模型的執行軌跡與分數，針對技能文件提出具體的修改建議
  source_quotes:
  - SkillOpt 把責任拆分給兩個獨立的模型，而不是要求同一個模型既要完成任務、又要幫自己的作業打分。
  - 對它來說唯一會隨著每一輪跑分而改變的，是被塞進它工作區、或附加在前面的技能文件
  - 它通常是一個能力更強的「前沿(frontier)」模型，而且只在離線訓練階段運作。它的工作是讀取目標模型的執行軌跡與分數，然後針對技能文件提出具體的修改建議
  anchor_type: 背景說明
  qualifiers:
  - text: 優化器也可以降級成跟目標模型一樣的模型，也就是目標模型自己優化自己
    source_quote: 即使把「教練」降級成跟目標模型一樣(規模小得多)的模型——也就是目標模型自己優化自己——有界更新加上驗證守門這套機制，依然足以挽回相較於前沿等級優化器所取得收益的 56% 到 74%。
  importance: 2
  status: normal
- id: c3
  role: context
  text: 在 SkillOpt 的每一個訓練步驟，目標模型帶著目前的技能在一批任務上執行；優化器提出修改後，候選技能必須在優化器從未看過的切分上被盲測打分，嚴格大於目前技能的分數才會被寫入硬碟，平手或分數下降則整個步驟被丟棄
  source_quotes:
  - 目標模型帶著目前的技能，在從 \( D_{tr} \) 抽出的一批 40 個任務上執行。
  - 而 \( D_{sel} \) 正是優化器從未看過的那個切分。只有當 \( \text{score}(\tilde{s}) \) **嚴格大於**目前技能的分數，這個候選才會被寫入硬碟，成為新的目前技能。平手或分數下降，則整個步驟都會被丟棄，先前的技能維持不變。
  anchor_type: 背景說明
  qualifiers:
  - text: 整套系統完全仰賴驗證守門機制，而驗證守門機制又完全仰賴一個便宜、可靠、自動化的評分方式
    source_quote: 整套系統完全仰賴驗證守門機制，而驗證守門機制又完全仰賴一個**便宜、可靠、自動化的評分方式**
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 在 Epoch 邊界，系統從訓練集裡隨機抽出 20 個任務，讓上一個 Epoch 的舊技能與這一個 Epoch 的新技能，都在同一份固定的 20 題考卷上重新跑一次，這是一次受控的 A/B 對照，而不只是單純比較原始分數
  source_quotes:
  - 在 Epoch 邊界，系統會從訓練集裡隨機抽出 20 個任務，讓**上一個 Epoch 的舊技能**與**這一個 Epoch 的新技能**，都在同一份固定的 20 題考卷上重新跑一次——這是一次受控的 A/B 對照，而不只是單純比較原始分數。
  anchor_type: 設計參數
  comparison_target: 同一份固定考卷上，上一個 Epoch 的舊技能與這一個 Epoch 的新技能互相比較
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 這 20 題接著會被分到四種狀態之一：進步、退步、持續失敗、穩定成功
  source_quotes:
  - 這 20 題接著會被分到四種狀態之一：進步、退步、持續失敗、穩定成功。
  anchor_type: 設計參數
  comparison_target: 同一份固定考卷上，舊技能與新技能的表現互相比較
  importance: 5
  status: normal
- id: c6
  role: evaluation
  text: 退步這一類是最重要的，因為它是最清楚的訊號，顯示最近的步驟級修改——即使每一項都各自通過了自己的驗證守門——加總起來卻讓某些東西變得更糟
  source_quotes:
  - '**退步**這一類是最重要的，因為它是最清楚的訊號，顯示最近的步驟級修改——即使每一項都各自通過了自己的驗證守門——加總起來卻讓某些東西變得更糟。'
  anchor_type: 部落格判斷
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: 一個專門的「慢速更新」呼叫會讀取這份對照結果，寫出一份宏觀層級的戰略筆記，並插入到 best_skill.md 裡一個特別標記、受保護的區塊；在同一個 Epoch 剩下的時間裡，一般的步驟級修改被禁止碰觸這個區塊，只有 Epoch 邊界的流程能更新它
  source_quotes:
  - 一個專門的「慢速更新」呼叫(`slow_update.md`)會讀取這份對照結果，寫出一份宏觀層級的戰略筆記，並插入到 `best_skill.md` 裡一個特別標記、受保護的區塊
  - 在同一個 Epoch 剩下的時間裡，一般的步驟級修改被禁止碰觸這個區塊——只有 Epoch 邊界的流程能更新它。
  anchor_type: 設計參數
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: 慢速更新也不會被無條件信任：它同樣得通過 D_sel 的驗證守門，如果沒能帶來實質幫助，就會被回滾
  source_quotes:
  - 即使是這項更新，也不會被無條件信任——它同樣得通過 \( D_{sel} \) 的驗證守門，如果沒能帶來實質幫助，就會被回滾。
  anchor_type: 設計參數
  qualifiers:
  - text: 整套系統完全仰賴驗證守門機制，而驗證守門機制又完全仰賴一個便宜、可靠、自動化的評分方式
    source_quote: 整套系統完全仰賴驗證守門機制，而驗證守門機制又完全仰賴一個**便宜、可靠、自動化的評分方式**
  importance: 8
  status: normal
- id: c9
  role: evaluation
  text: blog 說慢速更新正是傳統優化器裡動量或指數移動平均在文字空間的對應版本：它捕捉一個更長時程的趨勢，不該被短期的雜訊給抹掉
  source_quotes:
  - 這正是傳統優化器裡動量或指數移動平均在文字空間的對應版本：它捕捉一個更長時程的趨勢，不該被短期的雜訊給抹掉。
  anchor_type: 部落格判斷
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: 元技能（Meta Skill）是一份獨立的文件，由優化器寫給自己，總結在這個特定領域裡，哪些類型的修改容易通過驗證、哪些容易被拒絕
  source_quotes:
  - 還有第二個比較特別的機制：**元技能(Meta Skill)**。這是一份獨立的文件，由優化器寫給自己，總結在這個特定領域裡，哪些類型的修改容易通過驗證、哪些容易被拒絕。
  anchor_type: 設計參數
  importance: 10
  status: normal
- id: c11
  role: mechanism
  text: 元技能完全不會寫進 best_skill.md，目標模型永遠看不到它；它會被附加到優化器自己下一個 Epoch 的 system prompt 最前面
  source_quotes:
  - 它完全不會寫進 `best_skill.md`，目標模型永遠看不到它——相反地，它會被附加到**優化器自己**下一個 Epoch 的 system prompt 最前面
  anchor_type: 設計參數
  importance: 11
  status: normal
- id: c12
  role: evaluation
  text: blog 認為元技能讓「教練」隨著時間越來越擅長提出修改建議，而部署出去的技能檔案卻不會因此多長一個 token；這是一個小巧但乾淨的元學習（meta-learning）範例：優化器在學習如何在這個環境裡做優化，而這與實際部署的內容完全分開
  source_quotes:
  - 讓「教練」隨著時間越來越擅長提出修改建議，而部署出去的技能檔案卻不會因此多長一個 token。這是一個小巧但乾淨的元學習(meta-learning)範例：優化器在學習如何在這個環境裡做優化，而這與實際部署的內容完全分開。
  anchor_type: 部落格判斷
  importance: 12
  status: normal
```
