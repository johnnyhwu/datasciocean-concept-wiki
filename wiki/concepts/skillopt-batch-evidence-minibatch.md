---
id: skillopt-batch-evidence-minibatch
title: 不要對單一失敗做反應：先收一大批執行軌跡分成失敗池與成功池，再用 8 個一組的 minibatch 平行診斷，逼模型橫向比較
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
  - 為什麼是 8 個一組的 Minibatch
  - 分析師的合約
  - 優化器強度：一定要前沿等級嗎？
  first_appearance: true
parent: null
related:
  - skillopt-overview
  - skillopt-bounded-edit-budget
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 如果讓優化器只對單一失敗的執行軌跡做出反應，它往往會對造成那次失敗的特定雜訊過度擬合；SkillOpt 刻意用大批次（一批 40 個任務），提供足夠的統計份量去分辨「系統性的弱點」與「單一的偶發狀況」
  source_quotes:
  - 這是刻意設計的大批次。如果讓優化器只對單一失敗的執行軌跡做出反應，它往往會對造成那次失敗的特定雜訊過度擬合——例如一次網路延遲、一個措辭特別奇怪的輸入——而不是找出真正反覆出現的模式。40 個樣本能提供足夠的統計份量，讓系統得以分辨出「系統性的弱點」與「單一的偶發狀況」。
  anchor_type: 部落格判斷
  comparison_target: 只對單一失敗的執行軌跡做出反應
  importance: 1
  status: normal
- id: c2
  role: context
  text: SkillOpt 把責任拆分給兩個獨立的模型：凍結的目標模型負責實際執行工作，其權重與原生的 system prompt 在整個訓練過程中都保持凍結，唯一會改變的是它的技能文件；優化器模型只在離線訓練階段運作，讀取目標模型的執行軌跡與分數，針對技能文件提出具體的修改建議
  source_quotes:
  - SkillOpt 把責任拆分給兩個獨立的模型，而不是要求同一個模型既要完成任務、又要幫自己的作業打分。
  - 它的權重與原生的 system prompt 在整個訓練過程中都保持凍結。對它來說唯一會隨著每一輪跑分而改變的，是被塞進它工作區、或附加在前面的技能文件
  - 它通常是一個能力更強的「前沿(frontier)」模型，而且只在離線訓練階段運作。它的工作是讀取目標模型的執行軌跡與分數，然後針對技能文件提出具體的修改建議
  anchor_type: 背景說明
  qualifiers:
  - text: 優化器也可以降級成跟目標模型一樣的模型，也就是目標模型自己優化自己
    source_quote: 即使把「教練」降級成跟目標模型一樣(規模小得多)的模型——也就是目標模型自己優化自己——有界更新加上驗證守門這套機制，依然足以挽回相較於前沿等級優化器所取得收益的 56% 到 74%。
  importance: 2
  status: normal
- id: c3
  role: mechanism
  text: 每一個訓練步驟都從一次 Rollout（前向執行）開始：目標模型帶著目前的技能，在從訓練集 D_tr 抽出的一批 40 個任務上執行
  source_quotes:
  - 每一個訓練步驟都從一次 **Rollout(前向執行)** 開始：目標模型帶著目前的技能，在從 \( D_{tr} \) 抽出的一批 40 個任務上執行。
  anchor_type: 設計參數
  comparison_target: 只看單一失敗的執行軌跡（見 c1）
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 收集完成的執行軌跡會依照分數被分成失敗池與成功池，因為兩個池子需要不同種類的修改；失敗池的目的是找出可以糾正的修復方式，也就是什麼壞掉了、怎麼補
  source_quotes:
  - 40 條執行軌跡收集完成後，會依照分數被分成**失敗池**與**成功池**。這個分流很重要，因為這兩個池子需要不同種類的修改：失敗池的目的是找出可以糾正的修復方式(什麼壞掉了、怎麼補)
  anchor_type: 設計參數
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 成功池的目的是找出強化（reinforcement）：那些已經在發揮作用、但還沒被寫進技能文件裡的好習慣，如果沒被記錄下來，下一次未必還能單靠運氣重現
  source_quotes:
  - 成功池的目的則是找出強化(reinforcement)——那些已經在發揮作用、但還沒被寫進技能文件裡的好習慣，如果沒被記錄下來，下一次未必還能單靠運氣重現。
  anchor_type: 設計參數
  importance: 5
  status: normal
- id: c6
  role: mechanism
  text: 把一個池子裡所有的失敗案例（大約 20 個左右）一次全部塞進單一次的優化器呼叫，會超出有用的上下文範圍，並且可能招致隨著提示詞越來越長而愈發嚴重的「lost-in-the-middle」現象；所以 SkillOpt 把每個池子切成大小為 8 的 Minibatch，每個 Minibatch 各自發出一次平行 API 呼叫
  source_quotes:
  - 如果把一個池子裡所有的失敗案例(大約 20 個左右)一次全部塞進單一次的優化器呼叫裡，會超出有用的上下文範圍，並且可能招致那種隨著提示詞越來越長而愈發嚴重的「lost-in-the-middle」現象。因此，SkillOpt 改把每個池子切成大小為 8 的 Minibatch，並針對每個 Minibatch 各自發出一次平行 API 呼叫
  anchor_type: 設計參數
  comparison_target: 把一個池子的全部失敗案例（大約 20 個左右）一次塞進單一次優化器呼叫
  qualifiers:
  - text: 池子裡失敗案例的數量是「大約 20 個左右」，不是固定值
    source_quote: 如果把一個池子裡所有的失敗案例(大約 20 個左右)一次全部塞進單一次的優化器呼叫裡
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: 這個形狀恰好對應 MapReduce 的架構：每個 Minibatch 被獨立分析（Map），分析完的建議之後再被彙整起來（Reduce）；系統支援最多同時執行 16 個這樣的呼叫，所以即使某個步驟需要在兩個池子裡診斷多達數十條執行軌跡，也能在一輪平行運算中處理完畢，不必排成一條長長的序列佇列
  source_quotes:
  - 這個形狀恰好對應到 MapReduce 的架構：每個 Minibatch 被獨立分析(Map)，分析完的建議之後再被彙整起來(Reduce)。系統支援最多同時執行 16 個這樣的呼叫，因此即使某個步驟需要在兩個池子裡診斷多達數十條執行軌跡，也能在一輪平行運算中處理完畢，而不必排成一條長長的序列佇列。
  anchor_type: 設計參數
  comparison_target: 排成一條長長的序列佇列
  importance: 7
  status: normal
- id: c8
  role: evaluation
  text: blog 認為 Minibatch 大小訂在 8 是刻意折衷的結果：大小為 1 會重現原本就想避免的單一軌跡過擬合問題；8 則小到足以留在上下文限制之內，又大到足以強迫模型「橫向比較」這幾條軌跡，找出真正在多個任務裡共同出現的失敗模式，而不是只盯著單一案例
  source_quotes:
  - 小批次大小訂在 8，本身也是刻意折衷的結果：大小為 1 會重現原本就想避免的單一軌跡過擬合問題，而 8 則小到足以留在上下文限制之內，又大到足以強迫模型「橫向比較」這幾條軌跡，找出真正在多個任務裡共同出現的失敗模式，而不是只盯著單一案例。
  anchor_type: 部落格判斷
  comparison_target: 大小為 1 的 Minibatch（單一軌跡）
  importance: 8
  status: normal
- id: c9
  role: mechanism
  text: 負責失敗面的分析師會收到一個 Minibatch 的失敗任務執行軌跡，加上目前的技能文件，回傳一個 JSON 物件，列出它找到的共同失敗模式，以及一份 patch——一小串原子級的修改操作（append、insert_after、replace、delete），每一項都精確定位在技能文件中的某個目標字串上
  source_quotes:
  - 負責失敗面的分析師(`analyst_error.md`)會收到 8 個失敗任務的執行軌跡，加上目前的技能文件，回傳一個 JSON 物件，列出它找到的共同失敗模式，以及一份 `patch`——一小串原子級的修改操作(`append`、`insert_after`、`replace`、`delete`)，每一項都精確定位在技能文件中的某個目標字串上。
  anchor_type: 設計參數
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: 負責成功面的分析師做的是對稱版本：找出目標模型已經表現出來、但技能文件裡還沒寫下的好習慣，同時對已經被充分涵蓋的內容保持保守，不重複強化
  source_quotes:
  - 負責成功面的分析師(`analyst_success.md`)做的是對稱版本：找出目標模型已經表現出來、但技能文件裡還沒寫下的好習慣，同時對已經被充分涵蓋的內容保持保守，不重複強化。
  anchor_type: 設計參數
  importance: 10
  status: normal
```
