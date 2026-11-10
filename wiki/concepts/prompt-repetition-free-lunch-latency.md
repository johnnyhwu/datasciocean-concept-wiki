---
id: prompt-repetition-free-lunch-latency
title: Prompt 貼兩次、輸入變兩倍長，延遲卻接近不變：多出來的計算落在可平行化的 Prefill，而造成延遲的 Decode 因為輸出長度不變而沒有增加
type_hint: 判斷
context_type: evidence_from_single_source
sources:
- article: prompt-repetition
  article_title: "Google 2025 論文解讀：只要「複製貼上」就能變強？Prompt Repetition 如何成為 LLM 的免費午餐"
  url: https://datasciocean.com/paper-intro/prompt-repetition/
  sections:
  - 前言
  - The Trade-off
  - 方法介紹
  - 核心操作：Prompt Repetition
  - 為什麼這是 "Free Lunch"？
  - Prefill 階段 (處理 Prompt)
  - Decode 階段 (生成答案)
  - 總結比較
  - 「免費午餐」的實證：延遲與長度不變
  - 推理任務 vs. 非推理任務
  - 我們學到了什麼？
  first_appearance: true
parent: null
related:
  - prompt-repetition-causal-bottleneck-and-fix
  - prompt-repetition-results-and-boundary
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 輸入長度變兩倍卻幾乎不變慢，答案在於 LLM 推理過程的 Prefill 與 Decode 兩個階段差異：多出來的輸入落在 GPU 可以高度平行化運算的 Prefill 階段，對使用者幾乎無感；造成延遲的主要元兇是序列化的 Decode 階段，而 Prompt Repetition 沒有改變 Prompt 的語意，模型生成的 Output 長度保持不變
  source_quotes:
  - "你可能會擔心：「輸入長度變兩倍，難道不會變慢嗎？」"
  - "答案在於 LLM 推理過程的兩個階段差異：**Prefill** 與 **Decode**。"
  - "**特性:** GPU 可以 **高度平行化 (Parallel)** 運算。"
  - "雖然我們把輸入加倍了，但這部分的額外時間成本對使用者來說幾乎是無感的。"
  - "**特性:** 這是 **序列化 (Serial)** 的過程，受限於記憶體頻寬 (Memory Bandwidth) ，是造成 LLM 延遲的主要元兇。"
  - "Prompt Repetition 並沒有改變 Prompt 的語意 (例如沒有要求 \"Think step by step\") ，因此**模型生成的 Output 長度保持不變**。"
  comparison_target: 原始（不重複）Prompt 的輸入長度
  qualifiers:
  - text: 例外是 Claude 處理極長文本（Custom Tasks）時延遲有顯著增加；「零延遲增加」的結論是在絕大多數通用場景下成立
    source_quote: "唯一的例外是 Anthropic 的模型 (Claude) 在處理極長文本 (Custom Tasks) 時，延遲有顯著增加。作者推測這可能與 Claude API 內部的 Prefill 處理機制或緩存策略有關。但在絕大多數通用場景下，「零延遲增加」的結論是成立的。"
  anchor_type: 部落格推論
  importance: 1
  status: normal
- id: c2
  role: context
  text: Prompt Repetition 出自 Google Research 團隊於 2025 年 12 月發表的論文〈Prompt Repetition Improves Non-Reasoning LLMs〉，做法是將使用者的輸入 Prompt 原封不動地複製一遍：模型的輸入從 P 變成 [P ; P]，也就是 <QUERY><QUERY> 的形式
  source_quotes:
  - "歡迎來到 **\"Prompt Repetition Improves Non-Reasoning LLMs\"** 的論文筆記。這篇論文由 Google Research 團隊於 2025 年 12 月發表"
  - "**將使用者的輸入 Prompt 原封不動地複製一遍。**"
  - "$$ X_{\\text{method}} = [P ; P] $$"
  - "也就是 `<QUERY><QUERY>` 的形式。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 日期
  importance: 2
  status: normal
- id: c3
  role: mechanism
  text: Prefill 階段是模型閱讀 <QUERY><QUERY> 的階段，GPU 可以高度平行化運算：同時計算 1000 個 Token 的 Attention Matrix 和計算 500 個 Token 的時間差異極小（通常在毫秒等級）
  source_quotes:
  - "這是模型閱讀 `<QUERY><QUERY>` 的階段。"
  - "**特性:** GPU 可以 **高度平行化 (Parallel)** 運算。同時計算 1000 個 Token 的 Attention Matrix 和計算 500 個 Token 的時間差異極小 (通常在毫秒等級) 。"
  comparison_target: 計算 500 個 Token 的 Attention Matrix 所需時間
  qualifiers:
  - text: 例外是 Claude 處理極長文本（Custom Tasks）時延遲有顯著增加，作者推測可能與 Claude API 內部的 Prefill 處理機制或緩存策略有關；「零延遲增加」的結論是在絕大多數通用場景下成立
    source_quote: "唯一的例外是 Anthropic 的模型 (Claude) 在處理極長文本 (Custom Tasks) 時，延遲有顯著增加。作者推測這可能與 Claude API 內部的 Prefill 處理機制或緩存策略有關。但在絕大多數通用場景下，「零延遲增加」的結論是成立的。"
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: Decode 階段是模型一個字一個字吐出 Output 的階段，這是序列化的過程，受限於記憶體頻寬（Memory Bandwidth），是造成 LLM 延遲的主要元兇
  source_quotes:
  - "這是模型一個字一個字吐出 Output 的階段。"
  - "**特性:** 這是 **序列化 (Serial)** 的過程，受限於記憶體頻寬 (Memory Bandwidth) ，是造成 LLM 延遲的主要元兇。"
  anchor_type: 背景說明
  importance: 4
  status: normal
- id: c5
  role: context
  text: 另一種做法 Chain-of-Thought（CoT）讓模型 "Think step by step" 或先複述問題，它的缺點是昂貴且慢：增加了生成的 Token 數量（Decode 階段），直接導致 Latency 增加和 API 成本上升
  source_quotes:
  - "讓模型 \"Think step by step\" 或先複述問題。"
  - "**缺點:** **昂貴且慢**。這增加了生成的 Token 數量 (Decode 階段) ，直接導致 Latency 增加和 API 成本上升。"
  anchor_type: 背景說明
  importance: 5
  status: normal
- id: c6
  role: anchor
  text: blog 的總結比較表：Baseline 輸入短、輸出短，總延遲低；CoT 輸入短、輸出長（變慢的主因），Decode 時間慢，總延遲高；Prompt Repetition 輸入長（由平行化吸收）、輸出短，Prefill 時間快（微幅增加）、Decode 時間快，總延遲低（接近 Baseline）
  source_quotes:
  - "| **Baseline** | 短 | 短 | 快 | 快 | **低** |"
  - "| **CoT (Reasoning)** | 短 | **長 (變慢的主因)** | 快 | **慢** | **高** |"
  - "| **Prompt Repetition** | **長 (由平行化吸收)** | 短 | 快 (微幅增加) | 快 | **低 (接近 Baseline)** |"
  qualifiers:
  - text: 例外是 Claude 處理極長文本（Custom Tasks）時延遲有顯著增加；「零延遲增加」的結論是在絕大多數通用場景下成立
    source_quote: "唯一的例外是 Anthropic 的模型 (Claude) 在處理極長文本 (Custom Tasks) 時，延遲有顯著增加。作者推測這可能與 Claude API 內部的 Prefill 處理機制或緩存策略有關。但在絕大多數通用場景下，「零延遲增加」的結論是成立的。"
  anchor_type: 部落格推論
  importance: 6
  status: normal
- id: c7
  role: evidence
  text: 根據論文的實驗數據，blog 說兩者的生成長度（Output Length）高度一致，證明 Prompt Repetition 不會像 CoT 那樣觸發模型生成長篇大論的解釋
  source_quotes:
  - "請參考論文中 Figure 2 的實驗數據："
  - "**Output Length (生成長度):** 兩者高度一致。這證明 Prompt Repetition 不會像 CoT 那樣觸發模型生成長篇大論的解釋。"
  anchor_type: 實驗結果
  importance: 7
  status: normal
- id: c8
  role: evidence
  text: 延遲（Latency）方面兩者幾乎持平：即使輸入變兩倍長，End-to-End 的延遲幾乎沒有增加；blog 的總結比較表也把 Prompt Repetition 的總延遲列為「低（接近 Baseline）」
  source_quotes:
  - "請參考論文中 Figure 2 的實驗數據："
  - "**Latency (延遲):** 幾乎持平。即使輸入變兩倍長，End-to-End 的延遲幾乎沒有增加。"
  - "| **Prompt Repetition** | **長 (由平行化吸收)** | 短 | 快 (微幅增加) | 快 | **低 (接近 Baseline)** |"
  comparison_target: Baseline（不重複 Prompt）的 End-to-End 延遲
  qualifiers:
  - text: 例外是 Claude 處理極長文本（Custom Tasks）時延遲有顯著增加；「零延遲增加」的結論是在絕大多數通用場景下成立
    source_quote: "唯一的例外是 Anthropic 的模型 (Claude) 在處理極長文本 (Custom Tasks) 時，延遲有顯著增加。作者推測這可能與 Claude API 內部的 Prefill 處理機制或緩存策略有關。但在絕大多數通用場景下，「零延遲增加」的結論是成立的。"
  anchor_type: 實驗結果
  importance: 8
  status: normal
- id: c9
  role: qualifier
  text: 唯一的例外是 Anthropic 的模型（Claude）在處理極長文本（Custom Tasks）時，延遲有顯著增加
  source_quotes:
  - "唯一的例外是 Anthropic 的模型 (Claude) 在處理極長文本 (Custom Tasks) 時，延遲有顯著增加。"
  anchor_type: 實驗結果
  importance: 9
  status: normal
- id: c10
  role: qualifier
  text: 對這個例外，作者推測可能與 Claude API 內部的 Prefill 處理機制或緩存策略有關
  source_quotes:
  - "作者推測這可能與 Claude API 內部的 Prefill 處理機制或緩存策略有關。"
  anchor_type: 原作者解讀
  importance: 10
  status: normal
- id: c11
  role: evaluation
  text: blog 說作者因此大膽聲稱這是一個「Free Lunch」：利用 GPU 在 Prefill 階段過剩的算力，換取模型對內容的精確理解，且沒有犧牲使用者的等待時間
  source_quotes:
  - "這就是為什麼作者敢大膽聲稱這是一個 **\"Free Lunch\"**：我們利用了 GPU 在 Prefill 階段過剩的算力，換取了模型對內容的精確理解，且完全沒有犧牲使用者的等待時間。"
  qualifiers:
  - text: 例外是 Claude 處理極長文本（Custom Tasks）時延遲有顯著增加；「零延遲增加」的結論是在絕大多數通用場景下成立
    source_quote: "唯一的例外是 Anthropic 的模型 (Claude) 在處理極長文本 (Custom Tasks) 時，延遲有顯著增加。作者推測這可能與 Claude API 內部的 Prefill 處理機制或緩存策略有關。但在絕大多數通用場景下，「零延遲增加」的結論是成立的。"
  - text: 強制開啟 CoT 後，Prompt Repetition 的效果變成「中性至微幅正面」（5 勝 1 敗 22 平）
    source_quote: "當開啟 CoT 後，Prompt Repetition 的效果變成了 **「中性至微幅正面」** (5 勝 1 敗 22 平) 。"
  anchor_type: 部落格推論
  importance: 11
  status: normal
- id: c12
  role: evaluation
  text: blog 在結論中把它描述為用 Prefill 階段（廉價、可平行化）的計算量，換取原本只有雙向注意力模型（如 BERT）才能擁有的理解力
  source_quotes:
  - "我們用 **Prefill 階段** (廉價、可平行化) 的計算量，換取了原本只有在 **雙向注意力模型 (如 BERT)** 才能擁有的理解力。"
  qualifiers:
  - text: 強制開啟 CoT 後，Prompt Repetition 的效果變成「中性至微幅正面」（5 勝 1 敗 22 平）
    source_quote: "當開啟 CoT 後，Prompt Repetition 的效果變成了 **「中性至微幅正面」** (5 勝 1 敗 22 平) 。"
  anchor_type: 部落格推論
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: blog 認為因為利用了 GPU 的平行運算能力，幾乎在零延遲負擔（Zero Latency Overhead）的情況下獲得了顯著的準確率提升，這在資源受限的實際應用中極具價值
  source_quotes:
  - "因為利用了 GPU 的平行運算能力，我們幾乎在 **Zero Latency Overhead** 的情況下，獲得了顯著的準確率提升。這在資源受限的實際應用中極具價值。"
  qualifiers:
  - text: 例外是 Claude 處理極長文本（Custom Tasks）時延遲有顯著增加；「零延遲增加」的結論是在絕大多數通用場景下成立
    source_quote: "唯一的例外是 Anthropic 的模型 (Claude) 在處理極長文本 (Custom Tasks) 時，延遲有顯著增加。作者推測這可能與 Claude API 內部的 Prefill 處理機制或緩存策略有關。但在絕大多數通用場景下，「零延遲增加」的結論是成立的。"
  - text: 準確率提升有範圍：強制開啟 CoT 後，Prompt Repetition 的效果變成「中性至微幅正面」（5 勝 1 敗 22 平）
    source_quote: "當開啟 CoT 後，Prompt Repetition 的效果變成了 **「中性至微幅正面」** (5 勝 1 敗 22 平) 。"
  - text: blog 認為 Prompt Repetition 最適合「需要精準理解，但不需要複雜多步推理」的任務
    source_quote: "**Prompt Repetition 最適合那些「需要精準理解，但不需要複雜多步推理」的任務**"
  anchor_type: 部落格判斷
  importance: 13
  status: normal
```
