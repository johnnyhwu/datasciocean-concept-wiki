---
id: stateful-and-budget-matched-controls
title: 要驗證「丟掉歷史」與「結構化」的價值，得看只差那一件事的對照組：Stateful 只差有沒有保留完整歷史，預算對齊控制組排除「贏只是因為 prompt 比較短」，證明贏的是「結構化」而不只是「變短」
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: skill-state
  article_title: "SKILL.state 論文：Agent 不留對話歷史只留狀態，200 步任務省 41 倍 token"
  url: https://datasciocean.com/paper-intro/skill-state/
  sections:
  - Agent 跑越久越貴：把對話歷史換成一份狀態
  - 對照組：關鍵是 Stateful 與預算對齊組
  - 倉儲環境：任務夠長才拉開差距，最大的差距在 token
  - 軟體版本庫：中途一度輸給 Stateful
  - 預算對齊：贏在結構化，不只是 prompt 變短
  - 實務上該選 ReAct 還是 SKILL.state
  - 結論：省成本可以期待，全面變準還不行
  - 看數字前的保留：長任務只在自建環境測過
  first_appearance: true
parent: null
related:
  - skillstate-state-replaces-history
  - llm-patch-validation-format-not-semantics
  - skillstate-results-cost-vs-accuracy
  - discard-history-relevance-at-the-time
  - baseline-who-built-it
  - ragu-results-peeling-confounds
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: Stateful 是最關鍵的對照組，只有這一組比較，才真正驗證了「丟掉歷史」這個決定有沒有價值；預算對齊控制組則專門排除「贏只是因為 prompt 比較短」，證明贏的是「結構化」，而不只是「變短」，這個方法論比論文的核心主張更值得留在腦子裡
  source_quotes:
  - "Stateful 是最關鍵的對照組。"
  - "只有這一組比較，才真正驗證了「丟掉歷史」這個決定有沒有價值"
  - "論文另外設了一組預算對齊控制組，專門排除「贏只是因為 prompt 比較短」這個可能。"
  - "預算對齊控制組這個實驗設計也值得記住：它證明贏的是「結構化」，而不只是「變短」，這個方法論比論文的核心主張更值得留在腦子裡。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 預算對齊實驗是在倉儲環境做的
    source_quote: "表 5 — 倉儲環境的預算對齊控制組：同樣的 token 預算下比準確率（來源：原始論文 Table 5。）"
    source: figure_caption
  figures:
  - file: figures/skill-state/table5.png
    article: skill-state
    src: table5.png
    caption: 表 5 — 倉儲環境的預算對齊控制組：同樣的 token 預算下比準確率（來源：原始論文 Table 5。）
    sha256: cfec06ca704f69d0ca08a217e25bc2dd0344f0e20baf6496afe0960b88d928c3
  importance: 1
  status: normal
- id: c2
  role: context
  text: "SKILL.state 是 Google 與 Purdue 的論文《SKILL.state: Scalable Long-Horizon Agent Skills》提出的做法：模型每一步只看三樣東西：任務指令、一份描述「世界現在長什麼樣」的結構化狀態、這一步的最新觀察；模型的思考過程用完就丟，只把「狀態該怎麼改」的結論留下來"
  source_quotes:
  - "這是 Google 與 Purdue 的論文《SKILL.state: Scalable Long-Horizon Agent Skills》提出的做法。模型每一步只看三樣東西：任務指令、一份描述「世界現在長什麼樣」的結構化狀態、這一步的最新觀察。模型的思考過程用完就丟，只把「狀態該怎麼改」的結論留下來。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: Stateful(LangGraph) 對照組仿照 LangGraph（一個 agent 開發框架，可以在對話之外維護一份結構化狀態）的做法，有結構化的狀態區塊，但同時保留完整的滾動對話紀錄；它跟 SKILL.state 一樣有結構化狀態，唯一的差別是「狀態加完整歷史並存」還是「只有狀態，歷史全丟」
  source_quotes:
  - "Stateful(LangGraph) 仿照 LangGraph（一個 agent 開發框架，可以在對話之外維護一份結構化狀態）的做法，有結構化的狀態區塊，但同時保留完整的滾動對話紀錄。"
  - "它跟 SKILL.state 一樣有結構化狀態，唯一的差別是「狀態加完整歷史並存」還是「只有狀態，歷史全丟」。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c4
  role: context
  text: 另外兩個架構對照組：Prompt(ReAct) 是最原始的做法，每一步的觀察、推理、動作全部往後疊加；Memory(Summary) 保留最近三輪的原文，再加上一份定期更新的自然語言摘要。這些對照組頂多證明「結構化狀態比純文字歷史好」
  source_quotes:
  - "Prompt(ReAct) 是最原始的做法，每一步的觀察、推理、動作全部往後疊加。Memory(Summary) 保留最近三輪的原文，再加上一份定期更新的自然語言摘要。"
  - "其他對照組頂多證明「結構化狀態比純文字歷史好」。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 3
  status: normal
- id: c5
  role: anchor
  text: 拿 Stateful 對照組來比：倉儲環境 T=200 時 Stateful 用掉 5,041,164 個 token，SKILL.state 只用 122,384 個，差了 41 倍；但在狀態彼此高度關聯的軟體版本庫環境，T=25 時 Stateful（0.94）反而贏過 SKILL.state（0.88）
  source_quotes:
  - "Table 1 是倉儲環境的主表"
  - "真正壓倒性的是 token：\\( T=200 \\) 時 Stateful 用掉 5,041,164 個，SKILL.state 只用 122,384 個，差了 41 倍。"
  - "軟體版本庫是 SkillExecBench 的第二個子環境，狀態彼此高度關聯。"
  - "而它在軟體版本庫 \\( T=25 \\) 時甚至贏過 SKILL.state，就是前面那個 Stateful 0.94、SKILL.state 0.88 的反例。"
  anchor_type: 實驗結果
  comparison_target: SKILL.state 對比同一環境、同一任務長度的 Stateful 對照組
  qualifiers:
  - text: 同一張表裡，軟體版本庫 T=50 時 SKILL.state 贏回來（0.86 對 0.74），T=100 領先擴大到 15 個百分點（0.78 對 0.63）
    source_quote: "\\( T=50 \\) 才贏回來（0.86 對 0.74），\\( T=100 \\) 領先擴大到 15 個百分點（0.78 對 0.63）。"
  - text: 最有說服力的長任務數字，全部來自論文自己設計、自己控制的合成環境
    source_quote: "最有說服力的長任務數字，全部來自自己設計、自己控制的合成環境。"
  importance: 2
  status: normal
- id: c6
  role: context
  text: 預算對齊控制組的三種做法都把 prompt 硬壓到跟 SKILL.state 差不多短：Truncated(Sliding Window) 只留最近幾輪，硬卡 token 上限；Summary-capped 用自然語言摘要，但嚴格限制摘要本身的長度；ReAct+LLMLingua 用 LLMLingua 壓縮，這個工具讓一個小模型依困惑度（小模型覺得一段文字有多難預測）刪掉它認為不重要的字，硬壓到目標 token 數
  source_quotes:
  - "三種做法都把 prompt 硬壓到跟 SKILL.state 差不多短：Truncated(Sliding Window) 只留最近幾輪，硬卡 token 上限；Summary-capped 用自然語言摘要，但嚴格限制摘要本身的長度；ReAct+LLMLingua 用 LLMLingua 壓縮，這個工具讓一個小模型依困惑度（小模型覺得一段文字有多難預測）刪掉它認為不重要的字，硬壓到目標 token 數。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c7
  role: anchor
  text: 三種預算對齊做法都把 prompt 硬壓到跟 SKILL.state 差不多短，預算一對齊，壓縮型的做法全部崩掉：Truncated(Sliding Window) 只剩 0.18，ReAct+LLMLingua 只剩 0.22，Summary-capped 有 0.52，SKILL.state 維持 0.94
  source_quotes:
  - "三種做法都把 prompt 硬壓到跟 SKILL.state 差不多短"
  - "預算一對齊，壓縮型的做法全部崩掉：Truncated(Sliding Window) 只剩 0.18，ReAct+LLMLingua 只剩 0.22，Summary-capped 有 0.52，SKILL.state 維持 0.94。"
  anchor_type: 實驗結果
  comparison_target: SKILL.state 對比 prompt 被硬壓到跟它差不多短的三種壓縮型做法
  qualifiers:
  - text: 這是倉儲環境的預算對齊實驗
    source_quote: "表 5 — 倉儲環境的預算對齊控制組：同樣的 token 預算下比準確率（來源：原始論文 Table 5。）"
    source: figure_caption
  figures:
  - file: figures/skill-state/table5.png
    article: skill-state
    src: table5.png
    caption: 表 5 — 倉儲環境的預算對齊控制組：同樣的 token 預算下比準確率（來源：原始論文 Table 5。）
    sha256: cfec06ca704f69d0ca08a217e25bc2dd0344f0e20baf6496afe0960b88d928c3
  importance: 2
  status: normal
- id: c8
  role: evaluation
  text: 預算對齊是全篇最紮實的實驗，因為它排除了「贏只是因為 prompt 比較短」這個混淆因素
  source_quotes:
  - "這是全篇最紮實的實驗，因為它排除了「贏只是因為 prompt 比較短」這個混淆因素。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 這是倉儲環境的預算對齊實驗
    source_quote: "表 5 — 倉儲環境的預算對齊控制組：同樣的 token 預算下比準確率（來源：原始論文 Table 5。）"
    source: figure_caption
  figures:
  - file: figures/skill-state/table5.png
    article: skill-state
    src: table5.png
    caption: 表 5 — 倉儲環境的預算對齊控制組：同樣的 token 預算下比準確率（來源：原始論文 Table 5。）
    sha256: cfec06ca704f69d0ca08a217e25bc2dd0344f0e20baf6496afe0960b88d928c3
  importance: 2
  status: normal
- id: c9
  role: mechanism
  text: blog 對結果的解釋：同樣的 token 預算下，統計式壓縮（LLMLingua）和簡單截斷會把語意上關鍵的資訊一起壓爛，SKILL.state 的結構化狀態則完整保留了關鍵的關聯資訊
  source_quotes:
  - "同樣的 token 預算下，統計式壓縮（LLMLingua）和簡單截斷會把語意上關鍵的資訊一起壓爛，SKILL.state 的結構化狀態則完整保留了關鍵的關聯資訊。"
  anchor_type: 部落格推論
  qualifiers:
  - text: 這是倉儲環境的預算對齊實驗
    source_quote: "表 5 — 倉儲環境的預算對齊控制組：同樣的 token 預算下比準確率（來源：原始論文 Table 5。）"
    source: figure_caption
  figures:
  - file: figures/skill-state/table5.png
    article: skill-state
    src: table5.png
    caption: 表 5 — 倉儲環境的預算對齊控制組：同樣的 token 預算下比準確率（來源：原始論文 Table 5。）
    sha256: cfec06ca704f69d0ca08a217e25bc2dd0344f0e20baf6496afe0960b88d928c3
  importance: 3
  status: normal
- id: c10
  role: evaluation
  text: 歷史要不要跟狀態並存：Dialogue State Tracking 是狀態加完整對話歷史並存，這篇是只留狀態；設計任何結構化狀態的系統時，先問這個子問題，而不是只把「有沒有結構化狀態」當成唯一的分類
  source_quotes:
  - "歷史要不要跟狀態並存：Dialogue State Tracking 是狀態加完整對話歷史並存，這篇是只留狀態。設計任何結構化狀態的系統時，先問這個子問題，而不是只把「有沒有結構化狀態」當成唯一的分類。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c11
  role: evaluation
  text: Stateful 對照組，也就是 LangGraph 風格的「結構化狀態加完整對話歷史」，介於純 ReAct 與只留狀態的 SKILL.state 之間
  source_quotes:
  - "介於兩者之間的，是 Table 1 和 Table 6 裡的 Stateful 對照組，LangGraph 風格的「結構化狀態加完整對話歷史」。它不是純 ReAct，也不是 SKILL.state 那種只留狀態"
  anchor_type: 部落格判斷
  importance: 4
  status: normal
```
