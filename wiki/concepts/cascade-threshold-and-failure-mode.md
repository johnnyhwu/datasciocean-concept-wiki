---
id: cascade-threshold-and-failure-mode
title: 串接門檻 τ 要隨第一階段判官、強判官、任務重選；門檻選對時，串接失敗是花更多錢，而不是掉分
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: jev-as-a-judge
  article_title: 便宜判官先判、沒把握才找 GPT-6：JEV 串接真的省錢嗎？
  url: https://datasciocean.com/paper-intro/jev-as-a-judge/
  sections:
  - 評測設計
  - 串接分流與門檻怎麼選
  - 門檻 τ 怎麼選：基本規則
  - 門檻 τ 怎麼選：保守規則
  - 換強判官時，同一套規則不一定通用
  - 前瞻性即時測試
  - 結論
  - 資料切分：pilot 剩下的部分做什麼用
  - 串接的成本與準確度怎麼取捨
  - 方法
  - 設計串接要看「失敗時的樣子」，好的設計失敗時是花更多錢，而不是掉分
  - 先弄清楚什麼是 LLM 判官
  - 信心 q：定義與驗證
  - 信心很高，不代表可靠，尤其在判官手上沒有東西可核對的時候
  - 整體評價
  first_appearance: true
parent: null
related:
- jev-cascade-overview
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 串接的門檻 τ 是第一階段判官、強判官、任務三者的函數，換任何一個都要用自己的標註資料重選；門檻選對時，好的串接設計失敗時是把成本推高，而不是把錯誤放行
  source_quotes:
  - \( \tau \) 是第一階段判官、強判官、任務三者的函數，換任何一個都要用自己的標註資料重選
  - \( \tau \) 不是 JEV 的屬性，而是「第一階段判官、強判官、任務」三者一起決定的，換任何一個都要重新選。
  - 第一階段變弱時，系統是把成本推高，而不是把錯誤放行。
  - 好的串接設計，應該讓門檻設保守時，壞掉的永遠是成本這一邊。
  anchor_type: 部落格判斷
  importance: 1
  status: normal
  qualifiers:
  - text: 這個保證只在門檻選對時成立；論文的反例是 GPT-5.6 Sol 的門檻選到 0.70，在 JudgeBench 掉了 4.81 分
    source_quote: 只在門檻選對時成立。論文的反例：GPT-5.6 Sol 的 \( \tau \) 選到 0.70，在 JudgeBench 掉了 4.81 分。
  - text: 沒有證據可對照的任務，強判官自己也近乎亂猜，轉出去不會變好，所以「失敗時變貴」的保證在這裡也不成立
    source_quote: 沒有證據可對照的任務，強判官自己也近乎亂猜，轉出去不會變好，所以「失敗時變貴」的保證在這裡也不成立。
  - text: 只有 200 題；論文自己說只能證明結果跟任務有關，不能斷言差別純粹來自有沒有證據
    source_quote: 限制：只有 200 題，論文自己說只能證明結果跟任務有關，不能斷言差別純粹來自有沒有證據。
- id: c2
  role: context
  text: 串接是便宜判官先判全部題目，沒把握的才交給強判官；τ 是門檻（放行線），q 達到 τ 就採用第一階段判官的判決，低於 τ 就轉給強判官
  source_quotes:
  - 便宜判官先判全部題目，沒把握的才交給強判官
  - \( \tau \) 是「門檻」（放行線）
  - \( q \ge \tau \)：JEV 的判決就是最終答案
  anchor_type: 背景說明
  importance: 2
  status: normal
- id: c3
  role: context
  text: JEV 是 TypeSafe AI 的託管模型，屬決策型判官：只輸出判決與每個標籤的機率，不產生任何文字，便宜、快；論文測的是 1.13 版
  source_quotes:
  - 決策型判官（decision-only judge） | 只輸出判決與每個標籤的機率，不產生任何文字 | 便宜、快。**[JEV](../../ai-concept/jev-overview/)**（TypeSafe AI 的託管模型，論文測的是 1.13 版）就是這類
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 信心 q 是 JEV 所有標籤機率中最大的那一個，也就是它對自己所選判決的把握
  source_quotes:
  - \( q \) 是 JEV 所有標籤機率中最大的那一個，也就是它對自己所選判決的把握
  anchor_type: 設計參數
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 選 τ 的基本規則：拿一批有標準答案的題目把串接模擬一遍，挑「最省錢、而且準確度掉不超過 2 個百分點」的 τ
  source_quotes:
  - 拿一批有標準答案的題目把串接模擬一遍，挑「最省錢、而且準確度掉不超過 2 個百分點」的 \( \tau \)。
  anchor_type: 設計參數
  comparison_target: 強判官單獨作答的準確度（掉分容忍度 2 個百分點）
  qualifiers:
  - text: 容忍度（掉幾分）是使用者自己訂的，不是模型替你算出來的
    source_quote: 容忍度（掉幾分）是使用者自己訂的，不是模型替你算出來的。
  importance: 5
  status: normal
- id: c6
  role: anchor
  text: 論文的實際做法：候選值是 0.5、0.6、…、0.99 共 7 個；在 96 題 pilot 選擇題（64 題 RewardBench、32 題 JudgeBench）上，挑在強判官的選擇集準確度 2 點之內、接受 JEV 判決最多的 τ，之後完全不重新擬合；對 GPT-6 選出的是 τ = 0.9
  source_quotes:
  - 論文的實際做法：候選值是 0.5、0.6、…、0.99 共 7 個；在 96 題 pilot 選擇題（64 題 RewardBench、32 題 JudgeBench）上，挑「在強判官的選擇集準確度 2 點之內、接受 JEV 判決最多（coverage 最大）」的 \( \tau \)，之後完全不重新擬合。對 GPT-6 選出的是 \( \tau = 0.9 \)。
  anchor_type: 設計參數
  comparison_target: 強判官在選擇集上的準確度（容忍 2 點之內）
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: 用來選參數的資料，不能同時拿來證明參數選得好：select（選擇集）決定參數，held-out（驗收集）只在最後驗收一次，必須完全沒參與選擇，數字才可信
  source_quotes:
  - 用來選參數的資料，不能同時拿來證明參數選得好。
  - select（選擇集） | 決定參數，例如門檻 \( \tau \)、溫度 \( T \) | 這份資料已經被「看過」，用來選參數
  - held-out（驗收集） | 只在最後驗收一次 | 必須完全沒參與選擇，數字才可信
  anchor_type: 背景說明
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: 保守規則（lower-bound rule）：練習題很少時，量到「只差 2 分」可能是運氣，所以改問「最壞情況可能差多少」，把量到的差往壞的方向扣一個懲罰，題目越少扣得越多，扣完還要在 2 分以內才通過
  source_quotes:
  - 練習題很少時，量到「只差 2 分」可能是運氣，所以保守規則改問「最壞情況可能差多少」，而不是「量到差多少」。
  - 保守規則（論文稱 lower-bound rule）把量到的差再往壞的方向扣一個懲罰，懲罰的大小代表這個數字有多不穩，題目越少扣得越多，扣完還要在 2 分以內才通過。
  - 再跟強判官單獨作答的總分比
  anchor_type: 設計參數
  comparison_target: 強判官單獨作答的準確度（掉分容忍度 2 分）
  importance: 8
  status: normal
  qualifiers:
  - text: 這個規則不是新方法，容忍度是人訂的，也沒有統計保證
    source_quote: 這個規則不是新方法，容忍度是人訂的，也沒有統計保證
- id: c9
  role: mechanism
  text: 串接的安全性來自一個結構：q 低就轉給強判官，所以第一階段越不確定，轉出越多，最終答案越接近強判官單獨的結果
  source_quotes:
  - 串接的安全性來自一個結構：\( q \) 低就轉給強判官，所以第一階段越不確定，轉出越多，最終答案越接近強判官單獨的結果。
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  qualifiers:
  - text: 這個保證只在門檻選對時成立；論文的反例是 GPT-5.6 Sol 的門檻選到 0.70，在 JudgeBench 掉了 4.81 分
    source_quote: 只在門檻選對時成立。論文的反例：GPT-5.6 Sol 的 \( \tau \) 選到 0.70，在 JudgeBench 掉了 4.81 分。
  - text: 沒有證據可對照的任務，強判官自己也近乎亂猜，轉出去不會變好，所以「失敗時變貴」的保證在這裡也不成立
    source_quote: 沒有證據可對照的任務，強判官自己也近乎亂猜，轉出去不會變好，所以「失敗時變貴」的保證在這裡也不成立。
  - text: 只有 200 題；論文自己說只能證明結果跟任務有關，不能斷言差別純粹來自有沒有證據
    source_quote: 限制：只有 200 題，論文自己說只能證明結果跟任務有關，不能斷言差別純粹來自有沒有證據。
  importance: 9
  status: normal
- id: c10
  role: anchor
  text: 前瞻實驗的兩個新任務上 JEV 本來就弱，串接的準確度仍與 GPT-6 完全一致，代價是費用接近 GPT-6 單獨的水準：PPE 轉出 68%、費用 0.69；JudgeBench Claude 轉出 89%、費用 0.91
  source_quotes:
  - 在兩個新任務上，用保守規則選門檻，串接的準確度跟 GPT-6 一模一樣
  - 兩個任務 JEV 本來就弱，準確度仍與 GPT-6 完全一致，代價是費用接近 GPT-6 單獨的水準（PPE 轉出 68%、費用 0.69；JudgeBench Claude 轉出 89%、費用 0.91）。
  anchor_type: 實驗結果
  comparison_target: GPT-6 單獨（費用以 GPT-6 單獨 = 1 為基準）
  qualifiers:
  - text: 這個保證只在門檻選對時成立；論文的反例是 GPT-5.6 Sol 的門檻選到 0.70，在 JudgeBench 掉了 4.81 分
    source_quote: 只在門檻選對時成立。論文的反例：GPT-5.6 Sol 的 \( \tau \) 選到 0.70，在 JudgeBench 掉了 4.81 分。
  - text: 這兩個任務是在先凍結流程、每個任務抽 100 題當選擇集、用保守規則選門檻後，即時串接剩下的題
    source_quote: 設計是先凍結流程，每個任務抽 100 題當選擇集、用保守規則選 \( \tau \)，再在剩下的題上即時串接。
  - text: 對照組是低推理強度的 GPT-6，不是它的最強設定
    source_quote: 對照組是低推理強度的 GPT-6，不是它的最強設定
  importance: 10
  status: normal
- id: c11
  role: anchor
  text: 前瞻實驗中選擇集上 JEV 比 GPT-6 差 12.5 分（PPE）和 17 分（JudgeBench），所以規則選了很嚴的門檻：PPE 是 0.95，JudgeBench 是 0.99
  source_quotes:
  - 選擇集上 JEV 比 GPT-6 差 12.5 分（PPE）和 17 分（JudgeBench），所以規則選了很嚴的 \( \tau \)：PPE 是 0.95，JudgeBench 是 0.99。
  anchor_type: 實驗結果
  comparison_target: GPT-6 單獨在同一選擇集上的準確度
  importance: 11
  status: normal
- id: c12
  role: anchor
  text: 三個強判官用同樣的規則、同樣的 96 題選擇集：GPT-5.4 選出 τ = 0.90，RewardBench 串接比強判官 +0.37（區間含 0）、JudgeBench 0.00（區間含 0）；GPT-6 選出 τ = 0.90，RewardBench +1.27（區間不含 0）、JudgeBench −0.74（區間含 0）
  source_quotes:
  - 三個強判官，用同樣的規則、同樣的 96 題選擇集
  - GPT-5.4 | 0.90 | +0.37（區間含 0） | 0.00（區間含 0）
  - GPT-6 | 0.90 | +1.27（區間不含 0） | −0.74（區間含 0）
  anchor_type: 實驗結果
  comparison_target: 各自的強判官單獨（串接準確度減強判官單獨準確度）
  importance: 12
  status: normal
- id: c13
  role: anchor
  text: 同樣的規則換成 GPT-5.6 Sol，選出較鬆的 τ = 0.70；RewardBench 串接比強判官 +0.82（區間含 0），但 JudgeBench 掉了 4.81 分（區間 [−8.52, −1.48]，完全在負的那一側），超過 2 分的容忍度，這不是運氣；JudgeBench 只轉出 28.5% 的題，漏掉太多 JEV 會錯的題
  source_quotes:
  - GPT-5.6 Sol | 0.70 | +0.82（區間含 0） | **−4.81 [−8.52, −1.48]（區間不含 0）**
  - GPT-5.6 Sol 在 JudgeBench 掉了 4.81 分，超過 2 分的容忍度，而且區間完全在負的那一側，這不是運氣。
  - 所以在 JudgeBench 只轉出 28.5% 的題，漏掉太多 JEV 會錯的題。
  anchor_type: 實驗結果
  comparison_target: GPT-5.6 Sol 單獨（串接準確度減強判官單獨準確度；容忍度 2 分）
  importance: 13
  status: normal
- id: c14
  role: evaluation
  text: 論文的解釋：96 題選擇集裡 JudgeBench 只有 32 題，其餘是 RewardBench；RewardBench 上放寬門檻很安全，規則被這一大塊拉著選出偏鬆的 τ，結果在難任務上失靈
  source_quotes:
  - 論文的解釋：96 題選擇集裡 JudgeBench 只有 32 題，其餘是 RewardBench。RewardBench 上放寬門檻很安全，規則被這一大塊拉著選出偏鬆的 \( \tau \)，結果在難任務上失靈。
  anchor_type: 原作者解讀
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 14
  status: normal
- id: c15
  role: anchor
  text: 換任務也要重選 τ：前瞻實驗若沿用通用的 τ = 0.9，費用降到 0.62，但準確度掉 0.53 分（區間 [−1.58, 0.35]，含 0），在 JudgeBench Claude 分組上掉 1.18 分
  source_quotes:
  - 反事實對照：如果當初沿用前面的通用 \( \tau = 0.9 \)（原表另有一列算這個假設），費用降到 0.62，但準確度掉 0.53 分（區間 [−1.58, 0.35]，含 0），在 JudgeBench Claude 分組上掉 1.18 分。所以「換任務要重選 \( \tau \)」再次被驗證。
  anchor_type: 實驗結果
  comparison_target: GPT-6 單獨（準確度差距以 GPT-6 單獨為基準，費用以 GPT-6 單獨 = 1）
  qualifiers:
  - text: 這是原表另有一列算的假設情境（反事實對照），不是實際跑的設定
    source_quote: （原表另有一列算這個假設）
  - text: 對照組是低推理強度的 GPT-6，不是它的最強設定
    source_quote: 對照組是低推理強度的 GPT-6，不是它的最強設定
  importance: 15
  status: pending_author_confirmation
- id: c16
  role: evaluation
  text: 前瞻實驗證明的是「規則在弱任務上會夠嚴、不掉分」，不是「串接在弱任務上很划算」
  source_quotes:
  - 這個實驗證明的是「規則在弱任務上會夠嚴、不掉分」，不是「串接在弱任務上很划算」。
  anchor_type: 部落格判斷
  importance: 16
  status: normal
- id: c17
  role: evaluation
  text: 設計任何分流或升級機制，都要問兩件事：第一階段失靈時，錯誤是被放行，還是被推高成本？門檻設錯時，壞掉的是哪一邊？
  source_quotes:
  - 設計任何分流或升級機制，都要問兩件事。第一階段失靈時，錯誤是被放行，還是被推高成本？門檻設錯時，壞掉的是哪一邊？
  anchor_type: 部落格判斷
  importance: 17
  status: normal
- id: c18
  role: qualifier
  text: 論文提到，如果知道答錯一題的成本，門檻應該由「錯誤成本與轉出成本的比值」推出，但沒有實測這個做法
  source_quotes:
  - 論文提到，如果知道答錯一題的成本，門檻應該由「錯誤成本與轉出成本的比值」推出，但沒有實測這個做法。
  anchor_type: 原作者解讀
  importance: 18
  status: normal
```
