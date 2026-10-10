---
id: skillopt-bounded-edit-budget
title: 合併後的修改不能全套：用遞減的「編輯預算」限流，初期大步探索、後期小步鞏固，修復失敗永遠優先於強化成功
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
  - 分析師的合約
  - 合併，但不失去脈絡
  - 池內的樹狀合併
  - 跨池合併：修復失敗永遠優先
  - 文字版的學習率：編輯預算
  - 餘弦衰減的預算
  - 排序哪些修改能過關
  - 真正做出決定的守門員
  - 評分函式的瓶頸
  - 優化器強度：一定要前沿等級嗎？
  first_appearance: true
parent: null
related:
  - skillopt-overview
  - skillopt-batch-evidence-minibatch
  - skillopt-blind-acceptance-gate
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 合併完成之後，提案的修改數量可能還是遠超過一次套用的安全上限；SkillOpt 用編輯預算 L_t 來限制單一步驟能套用多少修改，這是學習率在文字空間裡的直接對應。一次套用太多修改，就跟梯度下降時踩了太大的步伐一樣，技能文件可能因此陷入不穩定的狀態，並丟失先前辛苦累積下來的教訓
  source_quotes:
  - 合併完成之後，提案的修改數量可能還是遠超過一次套用的安全上限。SkillOpt 用**編輯預算** \( L_t \) 來限制單一步驟能套用多少修改——這是學習率在文字空間裡的直接對應。一次套用太多修改，就跟梯度下降時踩了太大的步伐一樣：技能文件可能因此陷入不穩定的狀態，並丟失先前辛苦累積下來的教訓。
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: SkillOpt 把責任拆分給兩個獨立的模型：凍結的目標模型負責實際執行工作，唯一會改變的是它的技能文件；優化器模型只在離線訓練階段運作，讀取目標模型的執行軌跡與分數，針對技能文件提出具體的修改建議，例如新增啟發式規則、刪掉過時的指令、替換模糊的措辭
  source_quotes:
  - SkillOpt 把責任拆分給兩個獨立的模型，而不是要求同一個模型既要完成任務、又要幫自己的作業打分。
  - 對它來說唯一會隨著每一輪跑分而改變的，是被塞進它工作區、或附加在前面的技能文件
  - 它通常是一個能力更強的「前沿(frontier)」模型，而且只在離線訓練階段運作。它的工作是讀取目標模型的執行軌跡與分數，然後針對技能文件提出具體的修改建議——新增這條啟發式規則、刪掉那句過時的指令、把這段模糊的措辭換掉。
  anchor_type: 背景說明
  qualifiers:
  - text: 優化器也可以降級成跟目標模型一樣的模型，也就是目標模型自己優化自己
    source_quote: 即使把「教練」降級成跟目標模型一樣(規模小得多)的模型——也就是目標模型自己優化自己——有界更新加上驗證守門這套機制，依然足以挽回相較於前沿等級優化器所取得收益的 56% 到 74%。
  importance: 2
  status: normal
- id: c3
  role: context
  text: 多個並行的分析師各自回傳對技能文件的修改建議之後，SkillOpt 必須把可能重疊、有時互相矛盾的多份修改清單收斂成一份，做法是兩階段的階層式合併
  source_quotes:
  - 當並行的分析師們回傳各自的修改建議之後，SkillOpt 必須把可能重疊、有時互相矛盾的多份修改清單，收斂成一份。它透過兩階段的階層式合併來完成這件事。
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 如果任一個池子裡的提案超過 8 份，就會進行樹狀合併（Tree Reduce）：每最多 8 份為一批進行合併，直到每個池子都只剩下一份統一的清單為止
  source_quotes:
  - 如果任一個池子裡的提案超過 8 份，就會進行**樹狀合併(Tree Reduce)**：每最多 8 份為一批，兩兩合併(透過 `merge_failure.md` 或 `merge_success.md`)，直到每個池子都只剩下一份統一的清單為止。
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 4
  status: pending_author_confirmation
- id: c5
  role: mechanism
  text: 在樹狀合併過程中，重複的建議會被收斂成措辭最通用的一版，並附上 support_count，用來追蹤有多少個獨立的分析師提出了等價的建議，這是「這個失敗或好習慣到底有多常出現」的粗略指標
  source_quotes:
  - 在這個合併過程中，重複的建議會被收斂成措辭最通用的一版，並附上 `support_count`，用來追蹤有多少個獨立的分析師提出了等價的建議——這是「這個失敗或好習慣到底有多常出現」的粗略指標。
  anchor_type: 設計參數
  qualifiers:
  - text: 樹狀合併是在任一個池子裡的提案超過 8 份時進行的（原文：如果超過 8 份，就會進行）
    source_quote: 如果任一個池子裡的提案超過 8 份，就會進行樹狀合併
  importance: 5
  status: normal
- id: c6
  role: mechanism
  text: 在池內的樹狀合併這一步，池子裡試圖修改技能文件中完全相同位置、但方式互不相容的提案就會被解決，而不是留到之後才發生衝突
  source_quotes:
  - 試圖修改技能文件中完全相同位置、但方式互不相容的提案，也會在這一步就被解決，而不是留到之後才發生衝突。
  anchor_type: 設計參數
  qualifiers:
  - text: 樹狀合併是在任一個池子裡的提案超過 8 份時進行的（原文：如果超過 8 份，就會進行）
    source_quote: 如果任一個池子裡的提案超過 8 份，就會進行樹狀合併
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: 失敗池與成功池各自統一的兩份清單，會經過最終的跨池合併，規則是「修復失敗永遠優先」：如果一個成功池的修改與一個失敗池的修改鎖定了同一個位置，失敗池的版本會被保留，沒有例外，只有不衝突的成功面修改才能存活到下一個階段
  source_quotes:
  - 兩份此時已經各自統一的清單——一份來自失敗池、一份來自成功池——會經過最終的跨池合併(`merge_final.md`)，而這裡的規則毫不含糊：**修復失敗永遠優先**。如果一個來自成功池的修改與一個來自失敗池的修改，鎖定了同一個位置，失敗池的版本會被保留，沒有例外，只有不衝突的成功面修改才能存活到下一個階段。
  anchor_type: 設計參數
  importance: 7
  status: normal
- id: c8
  role: evaluation
  text: 修復壞掉的東西，被視為嚴格高於強化已經運作良好的東西的優先級
  source_quotes:
  - 修復壞掉的東西，被視為嚴格高於強化已經運作良好的東西的優先級。
  anchor_type: 設計參數
  importance: 8
  status: normal
- id: c9
  role: mechanism
  text: 編輯預算遵循餘弦衰減排程，通常從 L_t = 4 開始，逐漸衰減到 L_t = 2
  source_quotes:
  - 這個預算本身遵循餘弦衰減排程，通常從 \( L_t = 4 \) 開始，逐漸衰減到 \( L_t = 2 \)。
  anchor_type: 設計參數
  comparison_target: 訓練初期的預算（4）與後期的預算（2）互相比較，這是方法提出者選的設定值
  qualifiers:
  - text: 預算是「通常」從 4 衰減到 2，不是固定值
    source_quote: 通常從 \( L_t = 4 \) 開始，逐漸衰減到 \( L_t = 2 \)
  importance: 9
  status: normal
- id: c10
  role: evaluation
  text: blog 說明衰減的理由：訓練初期技能文件大部分還是空的，所以較大幅度的結構性修改是安全且有用的（探索）；到了後期，文件已經累積了實質內容，就只該讓小幅度的用詞微調通過（鞏固），再多推進就有可能拆解掉已經運作良好的部分
  source_quotes:
  - 訓練初期，技能文件大部分還是空的，所以較大幅度的結構性修改是安全且有用的(探索)；到了後期，一旦文件已經累積了實質內容，就只該讓小幅度的用詞微調通過(鞏固)——再多推進就有可能拆解掉已經運作良好的部分。
  anchor_type: 部落格判斷
  importance: 10
  status: normal
- id: c11
  role: mechanism
  text: 決定哪些修改能進入這個預算，由一個專門的排序步驟負責，它嚴格按照優先順序，依四項標準排序所有合併後的候選修改：一、能修復多少條軌跡的問題，與 support_count 直接掛鉤；二、是否真正補上一個缺口，而不是重複陳述文件裡已經有的內容；三、是否讀起來像一條普遍適用的規則，而不是死板地寫死了某個任務的特定細節；四、是否具體、可操作，而不是空泛的建議
  source_quotes:
  - 決定哪些修改能進入這個預算，由一個專門的排序步驟(`ranking.md`)負責，它依照四項標準，嚴格按照優先順序排序所有合併後的候選修改：
  - 能修復多少條軌跡的問題(與 `support_count` 直接掛鉤)。
  - 是否真正補上一個缺口，而不是重複陳述文件裡已經有的內容。
  - 是否讀起來像一條普遍適用的規則，而不是死板地寫死了某個任務的特定細節。
  - 是否具體、可操作，而不是空泛的建議。
  anchor_type: 設計參數
  importance: 11
  status: normal
- id: c12
  role: mechanism
  text: 只有排名前 L_t 名的修改，才能進入候選技能；而候選技能並不會因為看起來合理就被信任，還必須在優化器從未看過的 D_sel 上被盲測打分、嚴格大於目前技能，才會被寫入硬碟
  source_quotes:
  - 只有排名前 \( L_t \) 名的修改，才能進入候選技能。
  - 並不會因為看起來合理就被信任——它必須靠著在 \( D_{sel} \) 上被盲測打分來爭取通過，而 \( D_{sel} \) 正是優化器從未看過的那個切分。只有當 \( \text{score}(\tilde{s}) \) **嚴格大於**目前技能的分數，這個候選才會被寫入硬碟，成為新的目前技能。
  anchor_type: 設計參數
  qualifiers:
  - text: 整套系統完全仰賴驗證守門機制，而驗證守門機制又完全仰賴一個便宜、可靠、自動化的評分方式
    source_quote: 整套系統完全仰賴驗證守門機制，而驗證守門機制又完全仰賴一個**便宜、可靠、自動化的評分方式**
  importance: 12
  status: normal
```
