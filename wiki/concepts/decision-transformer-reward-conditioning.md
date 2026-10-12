---
id: decision-transformer-reward-conditioning
title: Decision Transformer 把強化學習改寫成序列預測：訓練時學「怎麼走與最後拿多少分」的關聯，使用時先設定想要的分數；它的威力在多步決策，單次生成只借得到表層技巧
type_hint: 方法
context_type: standalone_classic
sources:
- article: persona-aware-d2s
  article_title: "拆解 Persona-Aware-D2S：同一份文件，怎麼依受眾和長度長出不同簡報"
  url: https://datasciocean.com/paper-intro/persona-aware-d2s/
  sections:
  - Decision Transformer：把強化學習包裝成序列預測
  first_appearance: true
parent: null
related:
  - persona-d2s-training-design-flaws
  - bradley-terry-pairwise-preference
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: Decision Transformer 的提案是把強化學習（RL）問題重新包裝成序列預測問題，用 GPT 式的監督學習訓練，完全不估計價值函數、不做 bootstrapping；訓練時是「觀察別人怎麼走、最後拿多少分，學會兩者的關聯」，使用時是「你先設定想要的分數，模型回推該怎麼走」
  source_quotes:
  - Decision Transformer 的提案是一個典範轉移——把 RL 問題重新包裝成序列預測問題，用 GPT 式的監督學習訓練，完全不估計價值函數、不做 bootstrapping。
  - 一句話總結：訓練時是「觀察別人怎麼走、最後拿多少分，學會兩者的關聯」；使用時是「你先設定想要的分數，模型回推該怎麼走」。
  anchor_type: 背景說明
  importance: 1
  status: normal
- id: c2
  role: context
  text: Decision Transformer（Chen et al., 2021）在 2021 年 6 月掛上 arXiv，同年在 NeurIPS 發表；時間點卡在 GPT-3 之後、ChatGPT 之前，屬於「Transformer 能不能用來解序列決策問題」那波研究風潮的代表作
  source_quotes:
  - Decision Transformer（Chen et al., 2021）2021 年 6 月掛上 arXiv，同年在 NeurIPS 發表。時間點卡在 GPT-3 之後、ChatGPT 之前，屬於「Transformer 能不能用來解序列決策問題」那波研究風潮的代表作。
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 日期
  importance: 2
  status: normal
- id: c3
  role: context
  text: Decision Transformer 想解決傳統 RL 的老毛病：Q-learning、policy gradient 這類方法訓練不穩定、需要精細調參，而且常常得跟環境 online 互動
  source_quotes:
  - 它想解決的是傳統 RL 的老毛病：Q-learning、policy gradient 這類方法訓練不穩定、需要精細調參、而且常常得跟環境 online 互動。
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 一條軌跡（trajectory）由一連串的 (state, action, reward) 組成
  source_quotes:
  - 一條軌跡（trajectory）由一連串的 (state, action, reward) 組成。
  anchor_type: 背景說明
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 訓練前先把 reward 轉成 return-to-go：從現在這一步到終點，總共還會拿到多少分
  source_quotes:
  - 訓練前先把 reward 轉成 return-to-go：從現在這一步到終點，總共還會拿到多少分。
  anchor_type: 背景說明
  importance: 5
  status: normal
- id: c6
  role: mechanism
  text: 模型的輸入是交錯排列的三元組序列，依序是 return-to-go、state、action，重複排下去
  source_quotes:
  - 模型的輸入是交錯排列的三元組序列：
  - return-to-go, state, action, return-to-go, state, action
  anchor_type: 背景說明
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: 訓練時蓋住 action，讓模型根據前面的 (return-to-go, state) 預測該輸出什麼 action；學到的映射大致是「我還想拿到多少分，而我現在在位置 A → 往右走」
  source_quotes:
  - 訓練時蓋住 action，讓模型根據前面的 (return-to-go, state) 預測該輸出什麼 action。學到的映射大致是「我還想拿到 10 分，而我現在在位置 A → 往右走」。
  anchor_type: 部落格舉例
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: 推論時使用者先許願，設定一個目標 return，模型根據這個目標加上目前 state 吐出動作；每走一步，剩餘的 return-to-go 就按實際拿到的分數遞減，重複到走完
  source_quotes:
  - 推論時使用者先許願：設定一個目標 return（例如「我想拿 10 分」），模型根據這個目標加上目前 state 吐出動作；每走一步，剩餘的 return-to-go 就按實際拿到的分數遞減，重複到走完。
  anchor_type: 部落格舉例
  importance: 8
  status: normal
- id: c9
  role: evaluation
  text: Decision Transformer 在研究圈內確實有影響力：同期有 Trajectory Transformer 提出類似想法，後續有 Online Decision Transformer，也被延伸到推薦系統、機器人、embodied AI、網頁導航 agent 等領域
  source_quotes:
  - 在研究圈內確實有影響力：同期有 Trajectory Transformer（Janner et al., 2021）提出類似想法，後續有 Online Decision Transformer，也被延伸到推薦系統、機器人、embodied AI、網頁導航 agent 等領域。
  anchor_type: 背景說明
  importance: 9
  status: normal
- id: c10
  role: evaluation
  text: Decision Transformer 沒有成為 LLM alignment 的主流路線：今天 RLHF 生態的主流仍然是 PPO（InstructGPT 那條線）或後來的 DPO；它比較像是在 offline RL 與機器人控制這個子領域持續發揮影響力，不是一個家喻戶曉的產品級技術
  source_quotes:
  - 沒有成為 LLM alignment 的主流路線——今天的 … 生態主流仍然是 PPO（InstructGPT 那條線）或後來的 …。
  - Decision Transformer 比較像是在 offline RL 與機器人控制這個子領域持續發揮影響力，不是一個家喻戶曉的產品級技術。
  anchor_type: 部落格判斷
  importance: 10
  status: normal
- id: c11
  role: evaluation
  text: Decision Transformer 真正的威力在於處理多步驟、有前後因果關係的序列決策：這一步怎麼選，會影響下一步能拿到多少分
  source_quotes:
  - Decision Transformer 真正的威力在於處理多步驟、有前後因果關係的序列決策：這一步怎麼選，會影響下一步能拿到多少分。
  anchor_type: 部落格判斷
  importance: 11
  status: normal
- id: c12
  role: anchor
  text: Persona-Aware-D2S 只借用了「reward-conditioned generation」這個訓練技巧——把 reward 當條件塞進輸入，用監督學習訓練，藉此繞開 PPO 的基礎設施複雜度；但這是個不完整的挪用，因為它的場景是單次生成，prompt 丟進去、完整大綱吐出來，沒有多步驟決策結構，也沒有軌跡的概念
  source_quotes:
  - 它只借用了「reward-conditioned generation」這個訓練技巧——把 reward 當條件塞進輸入，用監督學習訓練，藉此繞開 PPO 的基礎設施複雜度。但這是個不完整的挪用。
  - 而 Persona-Aware-D2S 的場景是單次生成，prompt 丟進去、完整大綱吐出來，沒有多步驟決策結構，也沒有軌跡的概念。
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 12
  status: normal
- id: c13
  role: anchor
  text: Decision Transformer 概念與 Persona-Aware-D2S 的對應：return-to-go（還想拿多少分）對應 reward model 打出的分數；state（目前在哪）對應 prompt（論文內容加上 persona 條件）；action（要往哪走）對應要生成的大綱；一整條軌跡在 Persona-Aware-D2S 裡不存在，只有單步生成
  source_quotes:
  - return-to-go（還想拿多少分） | reward model 打出的分數
  - state（目前在哪） | prompt（論文內容加上 persona 條件）
  - action（要往哪走） | 要生成的大綱
  - 一整條軌跡 | 不存在，只有單步生成
  anchor_type: 部落格考證
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 13
  status: normal
- id: c14
  role: evaluation
  text: 對照表最後一列才是重點：Persona-Aware-D2S 借了表層技巧，但沒有用到 Decision Transformer 真正被設計來解決的核心問題
  source_quotes:
  - 表格最後一列才是重點：借了表層技巧，但沒有用到它真正被設計來解決的核心問題。
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 14
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

以下是很基本的通用詞，blog 沒有解釋，由撰寫者以一般知識補充；它們不是卡上的主張，不能當作 blog 的說法引用。

- **價值函數（value function）**：估計「在某個狀態下，未來預期能拿到多少總報酬」的函數；Q-learning 等傳統 RL 方法要先估計它。
- **bootstrapping**：用自己目前的估計值去更新自己的估計，是傳統 RL 訓練不穩定的來源之一。
- **Q-learning、policy gradient**：兩大類傳統 RL 方法，前者學習每個動作的價值，後者直接優化選動作的策略。
- **online / offline RL**：online 指訓練時需要不斷與環境互動取得新資料；offline 只用事先收集好的固定資料。
- **PPO、RLHF**：見 persona-d2s-task-and-pipeline 卡的名詞補充。
- **DPO**：一種不需要另外訓練 reward model、也不用強化學習，直接用偏好資料微調語言模型的對齊方法。
- **reward model**：給候選輸出打分的模型，分數代表人類偏好的程度。
