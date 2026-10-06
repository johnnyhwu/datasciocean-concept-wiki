---
id: cascade-complementary-errors
title: 串接的價值來自「兩個判官錯在不同的題」；兩邊都錯的題，怎麼轉都修不回來
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: jev-as-a-judge
  article_title: 便宜判官先判、沒把握才找 GPT-6：JEV 串接真的省錢嗎？
  url: https://datasciocean.com/paper-intro/jev-as-a-judge/
  sections:
  - 評測設計
  - 串接分流與門檻怎麼選
  - 凍結政策在沒看過的題上的結果
  - 串接的價值，來自「兩個判官錯在不同的題」
  - 先弄清楚什麼是 LLM 判官
  - 信心 q：定義與驗證
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
  text: 這個串接設計能成立的前提，是兩個判官錯在不同的題：如果第一階段錯的題，強判官大多答對，轉出去就能補回來；但兩邊都錯的題，怎麼轉都修不回來
  source_quotes:
  - '**這個設計能成立的前提，是兩個判官錯在不同的題。**'
  - 如果第一階段錯的題，強判官大多答對，轉出去就能補回來。但兩邊都錯的題，怎麼轉都修不回來。
  anchor_type: 部落格判斷
  importance: 1
  status: normal
  qualifiers:
  - text: 這個串接設計只是眾多設計中的一種，論文只實測了這一種
    source_quote: 這只是眾多設計中的一種，而且論文只實測了這一種
- id: c2
  role: context
  text: 串接是便宜判官先判全部題目，沒把握的才交給強判官；被接受的題用第一階段的答案，被轉出的題用強判官的答案
  source_quotes:
  - 便宜判官先判全部題目，沒把握的才交給強判官
  - 串接的結果是，被接受的題用第一階段的答案，被轉出的題用強判官的答案。
  anchor_type: 背景說明
  importance: 2
  status: normal
- id: c3
  role: context
  text: 串接中強判官不看第一階段判官的答案、獨立重判，它的判決整個取代第一階段的判決
  source_quotes:
  - 交給強判官。強判官不看 JEV 的答案、獨立重判，它的判決整個取代 JEV
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c4
  role: context
  text: JEV 是 TypeSafe AI 的託管模型，屬決策型判官：只輸出判決與每個標籤的機率，不產生任何文字，便宜、快；論文測的是 1.13 版
  source_quotes:
  - 決策型判官（decision-only judge） | 只輸出判決與每個標籤的機率，不產生任何文字 | 便宜、快。**[JEV](../../ai-concept/jev-overview/)**（TypeSafe AI 的託管模型，論文測的是 1.13 版）就是這類
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 信心 q 是 JEV 所有標籤機率中最大的那一個，也就是它對自己所選判決的把握
  source_quotes:
  - \( q \) 是 JEV 所有標籤機率中最大的那一個，也就是它對自己所選判決的把握
  anchor_type: 設計參數
  importance: 5
  status: normal
- id: c6
  role: anchor
  text: JudgeBench 全部 350 題的原順序判斷：JEV 錯 75 題，GPT-6 在其中答對 60 題；GPT-6 錯 24 題，JEV 在其中答對 9 題；兩邊共同錯的有 15 題
  source_quotes:
  - 以 JudgeBench 全部 350 題的原順序判斷來看，JEV 錯 75 題，GPT-6 在其中答對 60 題；GPT-6 錯 24 題，JEV 在其中答對 9 題；兩邊共同錯的有 15 題。
  anchor_type: 實驗結果
  comparison_target: JEV 與 GPT-6 的錯題互相對照（同一批 JudgeBench 350 題）
  qualifiers:
  - text: 這是 JudgeBench 全部 350 題的原順序判斷；另一章表中 JudgeBench 的 270 題只是其中 held-out 的部分，所以準確度數字不同
    source_quote: （下一章表中 JudgeBench 的 270 題只是其中 held-out 的部分，所以準確度數字不同。）
  importance: 6
  status: normal
- id: c7
  role: anchor
  text: 如果有一個完美的挑題員，每題都挑到比較對的那一個，準確度可達 95.7%，高於 GPT-6 單獨的約 93%
  source_quotes:
  - 如果有一個完美的挑題員，每題都挑到比較對的那一個，準確度可達 95.7%。
  - 完美挑題員可達 95.7%，高於 GPT-6 單獨的約 93%。
  anchor_type: 數學推導
  comparison_target: GPT-6 單獨的準確度（約 93%）
  qualifiers:
  - text: 這是假設有完美挑題員的上限，不是實際分流的結果
    source_quote: 如果有一個完美的挑題員，每題都挑到比較對的那一個，準確度可達 95.7%。
  - text: 這個 95.7% 是以 JudgeBench 全部 350 題的原順序判斷來看
    source_quote: 以 JudgeBench 全部 350 題的原順序判斷來看
  importance: 7
  status: normal
- id: c8
  role: anchor
  text: 自編例子：100 題，強判官錯 10 題，JEV 錯 15 題，其中 3 題兩邊都錯；完美挑題員只轉 JEV 會錯的題，剩下的錯題只有那 3 題，串接準確度 97%，比強判官單獨的 90% 還高；如果兩邊的錯一模一樣，串接最好也只能做到強判官的水準
  source_quotes:
  - 自編例子：100 題，強判官錯 10 題，JEV 錯 15 題，其中 3 題兩邊都錯。如果有一個完美的挑題員，只轉 JEV 會錯的題，剩下的錯題只有那 3 題，串接準確度 97%，比強判官單獨的 90% 還高。如果兩邊的錯一模一樣（15 題全重疊），串接最好也只能做到強判官的水準。
  anchor_type: 部落格舉例
  comparison_target: 強判官單獨的準確度（90%，blog 自編例子，不是論文數字）
  importance: 8
  status: pending_author_confirmation
- id: c9
  role: evaluation
  text: 串接的天花板是兩者的共同錯，不是強判官自己的準確度
  source_quotes:
  - 串接的天花板是兩者的共同錯，不是強判官自己的準確度
  anchor_type: 部落格判斷
  importance: 9
  status: normal
  qualifiers:
  - text: 這個串接設計只是眾多設計中的一種，論文只實測了這一種
    source_quote: 這只是眾多設計中的一種，而且論文只實測了這一種
- id: c10
  role: evaluation
  text: 選第一階段，除了看便宜，還要看它的錯是否跟強判官不同，也要看它的 q 能讓你放行多少題；便宜但幾乎放行不了，就省不了錢
  source_quotes:
  - 選第一階段，除了看便宜，還要看它的錯是否跟強判官不同，也要看它的 \( q \) 能讓你放行多少題（便宜但幾乎放行不了，就省不了錢）
  anchor_type: 部落格判斷
  importance: 10
  status: normal
- id: c11
  role: evaluation
  text: 兩個判官越像（同家族、同訓練資料），串接越沒用
  source_quotes:
  - 兩個判官越像（同家族、同訓練資料），串接越沒用（推論，論文沒有直接測）
  anchor_type: 部落格推論
  qualifiers:
  - text: 這是 blog 的推論，論文沒有直接測
    source_quote: （推論，論文沒有直接測）
  importance: 11
  status: normal
- id: c12
  role: anchor
  text: RewardBench（held-out 1,340 題）上，串接只轉 25% 的題、費用只要 27%，準確度略勝 GPT-6（+1.27 個百分點，區間不含 0）
  source_quotes:
  - RewardBench（1,340 題） | 92.8 | 93.7 | 92.4 | +1.27 [0.45, 2.03] | 25% | 0.27
  - 只轉 25% 的題，費用只要 27%，準確度還略勝 GPT-6，區間不含 0，所以略勝是真的。
  anchor_type: 實驗結果
  comparison_target: GPT-6 單獨（準確度差距以 GPT-6 單獨為基準，費用以 GPT-6 單獨 = 1）
  qualifiers:
  - text: JEV 有沒有看過這些基準的訓練資料，論文並不知道，所以「JEV 在 RewardBench 追平 GPT-6」這類結果無法排除訓練重疊
    source_quote: 所以「JEV 在 RewardBench 追平 GPT-6」這類結果，無法排除訓練重疊。
  - text: 對照組是低推理強度的 GPT-6，不是它的最強設定
    source_quote: 對照組是低推理強度的 GPT-6，不是它的最強設定
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: RewardBench 上串接略勝 GPT-6，原因是兩個判官錯在不同題，串接等於挑了各自擅長的部分
  source_quotes:
  - 原因是兩個判官錯在不同題，串接等於挑了各自擅長的部分。
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 13
  status: normal
- id: c14
  role: anchor
  text: JudgeBench（270 題）上，串接要轉 65% 的題、費用 0.67，準確度與 GPT-6 看不出差別（區間含 0），但那是靠 GPT-6 補回來的
  source_quotes:
  - JudgeBench（270 題） | 81.3 | 92.2 | 93.0 | −0.74 [−2.22, 0.74] | 65% | 0.67
  - 要轉 65%，費用 67%，只省了三分之一。準確度與 GPT-6 看不出差別（區間含 0），但那是靠 GPT-6 補回來的。
  anchor_type: 實驗結果
  comparison_target: GPT-6 單獨（準確度差距以 GPT-6 單獨為基準，費用以 GPT-6 單獨 = 1）
  importance: 14
  status: normal
  qualifiers:
  - text: 對照組是低推理強度的 GPT-6，不是它的最強設定
    source_quote: 對照組是低推理強度的 GPT-6，不是它的最強設定
```
