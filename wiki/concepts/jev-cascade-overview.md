---
id: jev-cascade-overview
title: 便宜判官先判、沒把握才轉給 GPT-6：在答案讀得出的任務上又準又省，難任務上準確度不掉但省得有限
type_hint: 方法概覽
context_type: bound_to_source
sources:
- article: jev-as-a-judge
  article_title: 便宜判官先判、沒把握才找 GPT-6：JEV 串接真的省錢嗎？
  url: https://datasciocean.com/paper-intro/jev-as-a-judge/
  sections:
  - 前言
  - 三十秒版本
  - 先弄清楚什麼是 LLM 判官
  - 論文怎麼問問題
  - 評測設計
  - 信心 q：定義與驗證
  - 串接分流與門檻怎麼選
  - 凍結政策在沒看過的題上的結果
  - 整體評價
  - 第一類：這篇論文本身的貢獻
  - 針對 JEV 1.13 量出來的適用界線
  - 設計串接要看「失敗時的樣子」，好的設計失敗時是花更多錢，而不是掉分
  - 結論
  - 信心很高，不代表可靠，尤其在判官手上沒有東西可核對的時候
  - 前瞻性即時測試
  first_appearance: true
parent: null
related:
- confidence-three-metrics
- cascade-complementary-errors
- judge-readable-vs-derive
- cascade-threshold-and-failure-mode
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 用 JEV 的最大標籤機率 q 當信心，沿著「有把握就採用、沒把握就轉給 GPT-6」分流，在答案能從文字讀出的任務上又準又省，在難任務與新任務上，門檻選對時準確度不掉、但省得有限
  source_quotes:
  - 用 JEV 的最大標籤機率 \( q \) 當信心，沿著「有把握就採用、沒把握就轉給 GPT-6」分流，在答案能從文字讀出的任務上又準又省…在難任務與新任務上，門檻選對時準確度不掉、但省得有限
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 1
  status: normal
  qualifiers:
  - text: 對照組是低推理強度的 GPT-6，不是它的最強設定
    source_quote: 對照組是低推理強度的 GPT-6，不是它的最強設定
- id: c2
  role: context
  text: '這張卡談的是論文 JEV-as-a-Judge: Accept When Confident, Escalate When Unsure（卡內基美隆大學）；它問的是：讓便宜的判官先判，信心夠高就直接採用，信心不夠才轉給強判官，能不能用小得多的成本換到接近強判官的準確度'
  source_quotes:
  - '這篇文章讀的是 *JEV-as-a-Judge: Accept When Confident, Escalate When Unsure*（Li、Miao、Krishnan、Padman，卡內基美隆大學'
  - 讓便宜的判官先判，信心夠高就直接採用，信心不夠才轉給強判官，能不能用小得多的成本換到接近強判官的準確度
  anchor_type: 背景說明
  importance: 2
  status: normal
- id: c3
  role: context
  text: LLM 判官是拿一個 LLM 去評另一個模型的輸出，例如「這兩個回答哪個比較好」，或「這個答案有沒有被給定的證據支持」
  source_quotes:
  - '**[LLM 判官](../chateval/)**是拿一個 LLM 去評另一個模型的輸出，例如「這兩個回答哪個比較好」，或「這個答案有沒有被給定的證據支持」。'
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: context
  text: 推理型判官（如 GPT-6）先在內部想一長串再給結論，難題上比較強，但每次判斷要多花運算，費用高、速度慢
  source_quotes:
  - 推理型判官（reasoning judge） | 先在內部想一長串再給結論，如 GPT-6 | 難題上比較強，但每次判斷要多花運算，費用高、速度慢
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 4
  status: normal
- id: c5
  role: context
  text: JEV 是 TypeSafe AI 的託管模型，屬決策型判官：只輸出判決與每個標籤的機率，不產生任何文字，便宜、快；論文測的是 1.13 版
  source_quotes:
  - 決策型判官（decision-only judge） | 只輸出判決與每個標籤的機率，不產生任何文字 | 便宜、快。**[JEV](../../ai-concept/jev-overview/)**（TypeSafe AI 的託管模型，論文測的是 1.13 版）就是這類
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 5
  status: normal
- role: evaluation
  text: q 的排序可以信，q 的數字不能直接當機率讀
  source_quotes:
  - '**必須知道的結論：\( q \) 的排序可以信，\( q \) 的數字不能直接當機率讀。**'
  anchor_type: 部落格判斷
  status: normal
  id: c6
  importance: 6
  qualifiers:
  - text: 沒有證據可對照的任務，q 的排序能力等於亂猜，不要用
    source_quote: 沒有證據可對照的任務，\( q \) 的排序能力等於亂猜，不要用。
  - text: 只有 200 題；論文自己說只能證明結果跟任務有關，不能斷言差別純粹來自有沒有證據
    source_quote: 限制：只有 200 題，論文自己說只能證明結果跟任務有關，不能斷言差別純粹來自有沒有證據。
  - text: JEV 的 q 排序能力在最難的 JudgeBench 最弱（RewardBench、HaluEval、JudgeBench 的 AUROC 分別是 0.88、0.83、0.73，兩順序平均）
    source_quote: JEV 的 \( q \) 在 RewardBench、HaluEval、JudgeBench 上分別是 0.88、0.83、0.73（兩順序平均），最難的 JudgeBench 最弱。
- id: c7
  role: mechanism
  text: 信心 q 是 JEV 所有標籤機率中最大的那一個，也就是它對自己所選判決的把握
  source_quotes:
  - \( q \) 是 JEV 所有標籤機率中最大的那一個，也就是它對自己所選判決的把握
  anchor_type: 設計參數
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: JEV 先判每一題，q 達到門檻 τ（放行線）就直接把 JEV 的判決當最終答案，沒達到就交給 GPT-6 獨立重判，並以它的判決取代 JEV 的判決
  source_quotes:
  - 核心想法就是下面這張流程圖：JEV 先判每一題，\( q \) 達到門檻 \( \tau \) 就直接把 JEV 的判決當最終答案，沒達到就交給 GPT-6 獨立重判，並以它的判決取代 JEV 的判決。
  - \( \tau \) 是「門檻」（放行線）
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 8
  status: normal
- id: c9
  role: evaluation
  text: 這篇論文是第三方評測，不是提出新方法；串接分流和選門檻都是既有做法，它的價值在於把整套流程事先凍結，再拿沒看過的題目驗收
  source_quotes:
  - 這篇論文是第三方評測，不是提出新方法。串接分流和選門檻都是既有做法，它的價值在於把整套流程事先凍結，再拿沒看過的題目驗收
  anchor_type: 部落格判斷
  qualifiers:
  - text: 論文沒有聲明作者與 TypeSafe（JEV 的提供者）的關係；前言說這是第三方評測，這點是讀的時候要留意的
    source_quote: 論文沒有聲明作者與 TypeSafe（JEV 的提供者）的關係，致謝只提到 NIST、CMU 與 OpenAI 的 API 額度。前言說這是第三方評測，這點是讀的時候要留意的
  importance: 9
  status: normal
- id: c10
  role: anchor
  text: RewardBench 上，串接的準確度略勝 GPT-6（+1.27 個百分點），費用只要 27%
  source_quotes:
  - RewardBench 上，串接的準確度略勝 GPT-6（+1.27 個百分點），費用只要 27%
  - 只轉 25% 的題，費用只要 27%，準確度還略勝 GPT-6，區間不含 0，所以略勝是真的
  - 所以「省錢」是拿「JEV 全部加轉出去的」跟「全部給 GPT-6」比
  anchor_type: 實驗結果
  comparison_target: GPT-6 單獨判全部題目（費用以 GPT-6 單獨為基準，串接的費用含 JEV 本身加轉出去的題）
  qualifiers:
  - text: JEV 有沒有看過這些基準的訓練資料，論文並不知道，所以「JEV 在 RewardBench 追平 GPT-6」這類結果無法排除訓練重疊
    source_quote: 所以「JEV 在 RewardBench 追平 GPT-6」這類結果，無法排除訓練重疊。
  - text: 對照組是低推理強度的 GPT-6，不是它的最強設定
    source_quote: 對照組是低推理強度的 GPT-6，不是它的最強設定
  - text: 推廣範圍有限，只涵蓋幾個公開基準與兩個新任務
    source_quote: 推廣範圍有限，只涵蓋幾個公開基準與兩個新任務
  importance: 10
  status: normal
- id: c11
  role: anchor
  text: JudgeBench（較難）與兩個全新任務上，串接的準確度追平 GPT-6，但轉出比例高（65% 到 89%），只省約 9% 到 33% 的費用
  source_quotes:
  - JudgeBench（較難）與兩個全新任務上，準確度追平 GPT-6，但轉出比例高（65% 到 89%），只省約 9% 到 33% 的費用。
  anchor_type: 實驗結果
  comparison_target: GPT-6 單獨判全部題目
  qualifiers:
  - text: 準確度追平只在門檻選對時成立；論文的反例是 GPT-5.6 Sol 的 τ 選到 0.70，在 JudgeBench 掉了 4.81 分
    source_quote: 只在門檻選對時成立。論文的反例：GPT-5.6 Sol 的 \( \tau \) 選到 0.70，在 JudgeBench 掉了 4.81 分。
  - text: 對照組是低推理強度的 GPT-6，不是它的最強設定
    source_quote: 對照組是低推理強度的 GPT-6，不是它的最強設定
  - text: 推廣範圍有限，只涵蓋幾個公開基準與兩個新任務
    source_quote: 推廣範圍有限，只涵蓋幾個公開基準與兩個新任務
  importance: 11
  status: normal
- id: c12
  role: evaluation
  text: 串接的功勞是把 JEV 的弱點補到 GPT-6 的水準；「超過 GPT-6」只出現在 RewardBench（+1.27），JudgeBench 沒超過，前瞻實驗是剛好打平
  source_quotes:
  - 串接的功勞是把 JEV 的弱點補到 GPT-6 的水準。「超過 GPT-6」只出現在 RewardBench（+1.27），JudgeBench 沒超過，前瞻實驗是剛好打平。
  anchor_type: 部落格判斷
  comparison_target: GPT-6 單獨
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: 論文結論那句「高於 GPT-6 0.9 點、費用 41%」是 1,610 題的合計，其中 83% 是 RewardBench，也就是最好看的那一組
  source_quotes:
  - 論文結論那句「高於 GPT-6 0.9 點、費用 41%」是 1,610 題的合計，其中 83% 是 RewardBench，也就是最好看的那一組。
  anchor_type: 部落格考證
  comparison_target: GPT-6 單獨
  importance: 13
  status: pending_author_confirmation
- id: c14
  role: evaluation
  text: 研究價值低：串接分流與保守選門檻都是既有做法，沒有提出新演算法；能算貢獻的是做法的嚴謹，包括規則先凍結再驗收、把失敗案例攤出來、畫出「讀得出答案／需要推導」的界線
  source_quotes:
  - 串接分流與保守選門檻都是既有做法，論文自己就引用了 FrugalGPT 一類的串接工作，以及 2017 年的選擇性分類文獻，沒有提出新演算法。
  - 能算貢獻的是做法的嚴謹：規則先凍結再驗收、把失敗案例（GPT-5.6 Sol、JudgeBench）攤出來、畫出「讀得出答案／需要推導」的界線。
  anchor_type: 部落格判斷
  importance: 14
  status: normal
- id: c15
  role: evaluation
  text: 工程價值中高但有範圍：在答案能從文字直接讀出的任務上成立；弱任務上串接的準確度仍等於 GPT-6，代價是費用接近 GPT-6 單獨的水準，不是掉分；沒有證據可對照的任務上不成立，不要用
  source_quotes:
  - '**工程價值中高，但有範圍。**'
  - '**成立**：答案能從文字直接讀出的任務。'
  - '**失敗時安全**：弱任務上（PPE、JudgeBench Claude），串接的準確度仍等於 GPT-6，代價是多花錢（費用 0.69 到 0.91），不是掉分。'
  - '**不成立**：沒有證據可對照的任務，\( q \) 的排序能力等於亂猜，不要用。'
  - 代價是費用接近 GPT-6 單獨的水準
  anchor_type: 部落格判斷
  qualifiers:
  - text: 「失敗時安全」只在門檻選對時成立
    source_quote: 只在門檻選對時成立。論文的反例：GPT-5.6 Sol 的 \( \tau \) 選到 0.70，在 JudgeBench 掉了 4.81 分。
  - text: 只有 200 題；論文自己說只能證明結果跟任務有關，不能斷言差別純粹來自有沒有證據
    source_quote: 限制：只有 200 題，論文自己說只能證明結果跟任務有關，不能斷言差別純粹來自有沒有證據。
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 15
  status: normal
- id: c16
  role: anchor
  text: 前瞻實驗的兩個任務合計，串接的中位延遲 1.87 秒、GPT-6 單獨 1.91 秒，p95 延遲串接 4.95 秒、GPT-6 單獨 5.58 秒（p95 是第 95 百分位，也就是最慢那 5% 請求的起點），blog 說延遲幾乎沒有改善；JudgeBench Claude 上串接中位延遲 2.41 秒，比 GPT-6 單獨的 2.35 秒略慢，因為轉出的題要先等 JEV 再等 GPT-6
  source_quotes:
  - 延遲幾乎沒有改善，見下表。
  - JudgeBench Claude 上串接甚至略慢，因為轉出的題要先等 JEV 再等 GPT-6。
  - 兩個任務合計：中位延遲 | 1.87 秒 | 1.91 秒
  - JudgeBench Claude：中位延遲 | 2.41 秒 | 2.35 秒
  - 兩個任務合計：p95 延遲 | 4.95 秒 | 5.58 秒
  - p95 是第 95 百分位，也就是最慢那 5% 請求的起點。
  anchor_type: 實驗結果
  comparison_target: GPT-6 單獨的延遲
  importance: 16
  status: normal
```
