---
id: prompt-repetition-causal-bottleneck-and-fix
title: Decoder-only 模型的前面 token 是在對後文一無所知時被編碼的；把 Prompt 原封不動貼兩次，第二遍的每個 token 都看得到整個第一遍，等於在不改架構的前提下模擬雙向注意力
type_hint: 方法
context_type: evidence_from_single_source
sources:
- article: prompt-repetition
  article_title: "Google 2025 論文解讀：只要「複製貼上」就能變強？Prompt Repetition 如何成為 LLM 的免費午餐"
  url: https://datasciocean.com/paper-intro/prompt-repetition/
  sections:
  - 前言
  - 問題定義
  - The Causal Attention Bottleneck
  - "實例解析: 歧義性問題"
  - Sensitivity to Input Order
  - The Trade-off
  - 方法介紹
  - 核心操作：Prompt Repetition
  - 為什麼這樣做有效？ (從 Attention 視角解析)
  - Variations & Ablations
  - 對「輸入順序」的強大修復力
  - 「免費午餐」的實證：延遲與長度不變
  first_appearance: true
parent: null
related:
  - prompt-repetition-free-lunch-latency
  - prompt-repetition-results-and-boundary
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 在 Decoder-only 架構中，Token 的表徵品質受限於它出現的時間點；Prompt Repetition 把輸入的 Prompt 複製一遍，第二遍中的每一個位置都能完整地「看見」整個第一遍，創造出一種偽雙向注意力（Pseudo-Bidirectional Attention）的效果，可以被視為在 Decoder-only 架構上模擬雙向注意力的手段
  source_quotes:
  - "這導致了一個根本性的問題: **Token 的 Representation Quality 受限於其出現的時間點。**"
  - "**\\(P_2\\) 中的每一個位置都能完整地「看見」整個 \\(P_1\\)。**"
  - "這創造了一種 **Pseudo-Bidirectional Attention** 的效果"
  - "為什麼 **Prompt Repetition** 可以被視為一種在 Decoder-only 架構上模擬 **Bidirectional Attention** 的巧妙手段"
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
  role: context
  text: 主流大型語言模型（如 GPT-4、Gemini、Llama）大多採用 Transformer Decoder-only 架構，這類模型是 Causal 的：處理序列中第 i 個 Token 時，只能「看見」位置 j ≤ i 的 Token，無法看見未來的 Token
  source_quotes:
  - "目前主流大型語言模型 (LLMs，如 GPT-4, Gemini, Llama) 的基礎架構限制。這些模型大多採用 **Transformer Decoder-only** 架構"
  - "在 Decoder-only 架構中，模型是 **Causal** 的。這代表模型在生成或處理序列中的第 \\(i\\) 個 Token \\(x_i\\) 時，只能「看見 (Attend to) 」位置 \\(j \\le i\\) 的 Token，而無法看見未來的 Token \\(x_{j > i}\\)。"
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 模型處理序列前端的 Token 時，生成的 Key 和 Value 僅包含該時間點之前的資訊，也就是這些早期的 Token 是在「對未來一無所知」的狀態下被編碼的
  source_quotes:
  - "當模型處理序列前端的 Token 時，它所生成的 **Key (\\(K\\))** 和 **Value (\\(V\\))** 僅包含了該時間點之前的資訊。這意味著這些早期的 Token 是在「對未來一無所知」的狀態下被編碼的。"
  anchor_type: 部落格推論
  importance: 4
  status: normal
- id: c5
  role: anchor
  text: 以輸入語句「The bark was rough.」為例：模型讀到 bark 時只看得到「The bark」，無法確定是指「狗叫聲」還是「樹皮」，生成的 Key/Value 向量可能是模糊的混合體；讀到後面的 rough（粗糙的）時，雖然這個 Token 知道整句在講樹皮，但它回頭抓取的 bark 的 Value 向量是早期生成的、品質低落且含糊不清的，這限制了模型最終的理解能力
  source_quotes:
  - "輸入語句: `\"The bark was rough. <Question> ...\"`"
  - "當模型讀到 `\"bark\"` 這個字時，它只看得到 `\"The bark\"`。此時，模型無法確定這裡的 \"bark\" 是指「狗叫聲」還是「樹皮」。因此，它生成的 Key/Value 向量可能是一個模糊的混合體。"
  - "當模型讀到後面的 `\"rough\"` (粗糙的) 時，雖然最後這個 Token 知道整句話是在講樹皮，但它必須回頭去 Attend 前面 `\"bark\"` 的資訊。"
  - "但它所抓取的原料 (即 `\"bark\"` 的 \\(V\\) 向量) 是早期生成的、品質低落且含糊不清的。這限制了模型最終的理解能力。"
  anchor_type: 部落格舉例
  importance: 5
  status: normal
- id: c6
  role: mechanism
  text: 最後一個 Token 雖然看過所有內容，仍無法解決這個問題，blog 稱之為 Attention 機制的 Path Dependency：最後一個 Token 的 Latent 是由前面所有 Token 的 Value 加權平均而來，如果前面的 Value 本身因為缺乏上下文而品質不佳，就算擁有再好的 Attention Weight，也無法從這些「品質低落的原料」中還原出完美的語義
  source_quotes:
  - "是的，最後一個 Token 確實看過所有內容。但問題在於 Attention 機制的 **Path Dependency**。"
  - "最後一個 Token 的 Latent 是由前面所有 Token 的 Value (\\(V\\)) 加權平均而來。如果前面的 \\(V\\) 本身因為缺乏上下文而品質不佳 (例如沒有凸顯出「樹皮」的語義特徵) ，那麼最後一個 Token 就算擁有再好的 Attention Weight，也無法從這些「品質低落的原料」中還原出完美的語義。"
  anchor_type: 部落格推論
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: 單向注意力的限制也讓模型對 Prompt 的順序極度敏感：Context/Options 擺前面時，模型閱讀 Context 還不知道 Question 是什麼，無法針對性地提取與問題相關的資訊；Question 擺前面時，理論上閱讀 Context 會有更好的聚焦，但隨著 Context 變長，模型可能會遺忘前面的問題，或者注意力被分散
  source_quotes:
  - "由於上述的單向注意力限制，模型對 Prompt 的順序變得極度敏感。"
  - "模型在閱讀 Context 時，還不知道 Question 是什麼。因此，它無法針對性地提取與問題相關的資訊"
  - "模型先看到問題，理論上在閱讀 Context 時會有更好的聚焦。但隨著 Context 變長，模型可能會遺忘前面的問題，或者注意力被分散。"
  anchor_type: 部落格推論
  importance: 7
  status: normal
- id: c8
  role: context
  text: 在 Prompt Repetition 之前的第一種解法是 Chain-of-Thought（CoT）：讓模型 "Think step by step" 或先複述問題，透過生成過程強迫自己重新處理資訊，解決了表徵問題；缺點是昂貴且慢，因為它增加了生成的 Token 數量（Decode 階段），直接導致 Latency 增加和 API 成本上升
  source_quotes:
  - "讓模型 \"Think step by step\" 或先複述問題。"
  - "**優點:** 模型透過生成過程，強迫自己重新處理資訊，解決了上述的表徵問題。"
  - "**缺點:** **昂貴且慢**。這增加了生成的 Token 數量 (Decode 階段) ，直接導致 Latency 增加和 API 成本上升。"
  anchor_type: 背景說明
  importance: 8
  status: normal
- id: c9
  role: context
  text: 第二種解法是像 BERT 或 T5 那樣的 Bidirectional Attention / Prefix LM，允許 Input Token 互相看見，從根本上解決表徵問題；缺點是需要改變模型架構或訓練目標，對只能透過 API 呼叫的現成 Decoder-only 模型（如 GPT-4、Claude 3）是不可能的任務
  source_quotes:
  - "**Bidirectional Attention / Prefix LM:**"
  - "像 BERT 或 T5 那樣，允許 Input Token 互相看見。"
  - "**優點:** 從根本上解決表徵問題。"
  - "**缺點:** 這需要改變模型架構或訓練目標。對於我們只能透過 API 呼叫的現成 Decoder-only 模型 (如 GPT-4, Claude 3) ，這是不可能的任務。"
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 9
  status: normal
- id: c10
  role: context
  text: 論文想處理的挑戰是：如何在不改變模型架構（Black-box compatible）且不增加生成延遲（Zero latency overhead）的前提下，克服因果模型的單向注意力瓶頸，讓模型獲得類似「雙向注意力」的理解能力
  source_quotes:
  - "如何在不改變模型架構 (Black-box compatible) 且不增加生成延遲 (Zero latency overhead) 的前提下，克服因果模型的單向注意力瓶頸，讓模型獲得類似「雙向注意力」的理解能力？"
  qualifiers:
  - text: 延遲方面，blog 提到唯一的例外是 Claude 處理極長文本（Custom Tasks）時延遲有顯著增加；「零延遲增加」的結論是在絕大多數通用場景下成立
    source_quote: "唯一的例外是 Anthropic 的模型 (Claude) 在處理極長文本 (Custom Tasks) 時，延遲有顯著增加。作者推測這可能與 Claude API 內部的 Prefill 處理機制或緩存策略有關。但在絕大多數通用場景下，「零延遲增加」的結論是成立的。"
  anchor_type: 原作者解讀
  importance: 10
  status: normal
- id: c11
  role: mechanism
  text: 把重複後的輸入分成第一遍 P1 與第二遍 P2：處理 P1 時一如平常受因果注意力限制，對後面的資訊一無所知，產生的 Key/Value 表徵可能不完美；處理 P2 時，原本位於開頭的 Token（例如 Context）可以透過 Attention 去查詢 P1 結尾的 Token（例如 Question），所以 P2 生成的 Key/Value 是「已經看過全文」的高品質表徵，模型最終生成答案時會高度依賴這些來自 P2 的資訊
  source_quotes:
  - "當模型處理 \\(P_1\\) 時，它就像平常一樣，受限於因果注意力，對後面的資訊一無所知。這裡產生的 Key/Value 表徵可能是不完美的。"
  - "在 \\(P_2\\) 中，原本位於開頭的 Token (例如 Context) ，現在可以透過 Attention 機制去查詢 \\(P_1\\) 結尾的 Token (例如 Question) 。"
  - "這意味著 \\(P_2\\) 生成的 Key/Value Pairs 是 **「已經看過全文」** 的高品質表徵。"
  - "當模型最終要生成答案時，它會高度依賴這些來自 \\(P_2\\) 的高品質資訊，從而做出準確的預測。"
  anchor_type: 部落格推論
  importance: 11
  status: normal
- id: c12
  role: evaluation
  text: blog 認為這也解決了輸入順序問題：無論原始 Prompt 是 <Context><Question> 還是 <Question><Context>，重複之後 P2 的部分都能「互相關照」，開發者不再需要煩惱 Prompt 該怎麼擺放
  source_quotes:
  - "無論原始 Prompt 是 `<Context><Question>` 還是 `<Question><Context>`，在重複之後，\\(P_2\\) 的部分都能確保「互相關照」。開發者不再需要煩惱 Prompt 該怎麼擺放"
  qualifiers:
  - text: 實驗發現，在 Baseline 中 Options-first（選項在前、問題在後）的表現通常較差
    source_quote: "實驗發現，在 Baseline 中，`Options-first` 的表現通常較差 (因為讀選項時不知道問題) 。然而，一旦使用了 **Prompt Repetition**："
  - text: Options-first 使用 Prompt Repetition 後的表現是「追平或超越」Question-first
    source_quote: "其表現甚至追平或超越了原本較優的 `Question-first`。"
  anchor_type: 部落格判斷
  importance: 12
  status: normal
- id: c13
  role: evidence
  text: 作者設計了變體來測試。Prompt Repetition - Verbose 在兩遍之間加上「Let me repeat that:」，用來測試模型是否需要像人類一樣的自然語言轉折；結論是效果與標準重複差不多，但多了一些 token，性價比略低
  source_quotes:
  - "為了證明這個效果不是巧合，作者設計了幾種變體來進行測試。"
  - "格式：`\\( <QUERY> \\text{Let me repeat that:} <QUERY> \\)`"
  - "邏輯：測試模型是否需要像人類一樣的自然語言轉折。"
  - "結論：效果與標準重複差不多，但多了一些 token，性價比略低。"
  comparison_target: 標準的 Prompt Repetition（<QUERY><QUERY>）
  anchor_type: 實驗結果
  importance: 13
  status: normal
- id: c14
  role: evidence
  text: 另一個變體 Padding 在 <QUERY> 前面填入點號，用來驗證性能提升是因為「重複了有意義的資訊」，還是僅僅因為「輸入變長了，讓模型有更多運算空間」；結論是 Padding 完全無效
  source_quotes:
  - "格式：`\\( ...(\\text{dots})... <QUERY> \\)`"
  - "邏輯：我們需要驗證：性能提升是因為「重複了有意義的資訊」，還是僅僅因為「輸入變長了，讓模型有更多運算空間」？"
  - "結論：**Padding 完全無效**。"
  anchor_type: 實驗結果
  importance: 14
  status: normal
- id: c15
  role: evaluation
  text: blog 認為 Padding 無效反證了提升的來源確實來自它推導的「雙向注意力模擬」，而非單純的深度增加
  source_quotes:
  - "這反證了提升的來源確實是來自於我們推導的「雙向注意力模擬」，而非單純的深度增加。"
  anchor_type: 部落格推論
  importance: 15
  status: normal
```
