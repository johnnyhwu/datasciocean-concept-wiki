---
id: cer-critical-token-confidence
title: 算推理路徑的自信度時，整段平均會被高機率的功能性詞彙稀釋；CER 先用 Prompt 規定模型輸出答案標籤，再只算標籤後關鍵字的機率
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: cer
  article_title: "ACL 2025 | 超越 Self-Consistency！CER 論文解析：無需訓練，靠「過程自信度」激發 Llama 3 與 DeepSeek 推理潛能"
  url: https://datasciocean.com/paper-intro/cer/
  sections:
  - 前言
  - Noise in Whole-Sequence Uncertainty
  - 方法介紹
  - Reasoning Path Generation
  - Identifying Critical Tokens
  - Confidence-Weighted Aggregation
  - "單詞層級聚合 (\\(f\\)): 從 Token 到 Word"
  - 結語
  first_appearance: true
parent: null
related:
  - cer-process-confidence-weighted-voting
  - cer-results-how-to-read
  - verifier-expected-value-vs-argmax
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 'CER 認為一句話中大部分的詞都是雜訊（填充詞），只有推理的結點才是訊號；所以它不算整句的機率，而是用 Regex 抓出 Prompt 定義好的標籤（如 Answer: 或 Response:）後面的內容當關鍵字，讓自信度分數純粹反映模型對「推理結果」的把握'
  source_quotes:
  - "傳統方法會計算整句生成的 Log-Likelihood，但 CER 認為: **一句話中大部分的詞都是雜訊 (填充詞) ，只有推理的結點 (Node) 才是訊號。**"
  - "我們利用 Regex 抓取 Prompt 中定義好的標籤 (如 `Answer:` 或 `Response:`) ，並鎖定其後的內容作為「關鍵字」。"
  - "確保我們的自信度分數純粹反映了模型對「推理結果」的把握。"
  anchor_type: 設計參數
  importance: 1
  status: normal
- id: c2
  role: context
  text: CER（Confidence Enhanced Reasoning）是一個不需要訓練的框架，不修改模型權重、不需要外部的 Reward Model，純粹利用 LLM 推理時輸出的 Logits（機率分佈）做後處理，用每條推理路徑的自信度來加權多條路徑的投票
  source_quotes:
  - "這是一個完全 **無需訓練 (Training-free)** 的框架，不需要修改模型的權重，也不需要外部的 Reward Model。它純粹利用現有 LLM 在推理時輸出的 Logits (機率分佈) 來進行精細的後處理。"
  - "**CER (Our Method)**: 計算支持該答案的所有路徑的**自信度總和**。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: mechanism
  text: 直接計算整條推理路徑的自信度會有很大的雜訊：思維鏈裡有大量功能性詞彙（如 "First, we need to calculate..."、"Therefore, the answer is..."），模型生成它們的機率通常非常高，算整段的平均機率時，這些高分 Token 會稀釋掉真正關鍵的資訊（例如某個關鍵的運算數字或實體名稱）
  source_quotes:
  - "直接計算整條推理路徑 (Whole-sequence) 的自信度會有很大的雜訊。"
  - "一個典型的思維鏈 (Chain-of-Thought, CoT) 包含了大量的**功能性詞彙** (Functional Words)"
  - "*\"First, we need to calculate...\"*"
  - "*\"Therefore, the answer is...\"*"
  - "這些詞彙對於文法通順很重要，模型生成它們的機率通常非常高 (自信度高) 。如果我們計算整段文字的平均機率，這些無關緊要的高分 Token 會**稀釋**掉真正關鍵的資訊 (例如某個關鍵的運算數字或實體名稱) 。"
  anchor_type: 部落格推論
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 結果是很難區分一條「邏輯正確的路徑」和一條「廢話連篇但文法通順的路徑」
  source_quotes:
  - "這導致我們很難區分一條「邏輯正確的路徑」和一條「廢話連篇但文法通順的路徑」。"
  anchor_type: 部落格推論
  importance: 6
  status: normal
- id: c5
  role: mechanism
  text: blog 把這個問題比喻成訊噪比：推理過程中數值和專有名詞是真正的「訊號」，連接詞和填充詞是背景「雜訊」；混在一起算平均，強大的背景雜訊會掩蓋微弱但關鍵的訊號波動
  source_quotes:
  - "我們可以把這個問題想像成「訊噪比 (Signal-to-Noise Ratio) 」的問題。在推理過程中，**數值**和**專有名詞**是真正的「訊號」，而連接詞和填充詞則是背景「雜訊」。如果我們把整段話混在一起算平均，強大的背景雜訊會掩蓋掉微弱但關鍵的訊號波動。"
  anchor_type: 部落格舉例
  importance: 7
  status: normal
- id: c6
  role: mechanism
  text: '為了讓程式能自動抓重點，CER 用 Prompt 要求模型在每一個推理步驟結束時依特定格式輸出中間答案：數學任務要求輸出「Answer: [數值]」，問答任務要求輸出「Response: [實體/短語]」'
  source_quotes:
  - "為了後續能讓程式自動抓取重點，我們必須跟模型「約法三章」。"
  - "我們要求模型在每一個推理步驟結束時，必須依照特定的格式輸出中間答案。"
  - "**數學任務**: 要求輸出 `Answer: [數值]`。"
  - "**問答任務**: 要求輸出 `Response: [實體/短語]`。"
  anchor_type: 設計參數
  importance: 4
  status: normal
  figures:
  - file: figures/cer/figure4.png
    article: cer
    src: figure4.png
    caption: 'CER 用於數學推理的 Prompt 範例。注意它要求模型使用 ''Answer: [answer]'' 格式輸出。'
    sha256: 77b12fdb4bf388f21e65ba39c0aff51362e9dd8ac8af3708a2c11cd8e423a6ce
- id: c7
  role: mechanism
  text: 這樣做把非結構化的思維鏈轉成「半結構化」的資料，後續可以用正規表達式（Regex）輕鬆提取資訊
  source_quotes:
  - "這樣做的目的是將非結構化的思維鏈 (CoT) 轉化為「半結構化」的數據，讓我們後續可以用正規表達式 (Regex) 輕鬆提取資訊。"
  anchor_type: 設計參數
  importance: 8
  status: normal
- id: c8
  role: mechanism
  text: 關鍵字依任務而定：數學任務關注數值（例如計算過程中出現的 "100"、"5"、"125"），開放域問答關注專有名詞（例如人名、地名或特定實體）
  source_quotes:
  - "**數學任務 (Math Tasks)**: 關注 **數值 (Numerical values)**。例如在計算過程中出現的 \"100\", \"5\", \"125\"。"
  - "**開放域問答 (Open-Domain QA)**: 關注 **專有名詞 (Proper Nouns)**。例如人名、地名或特定實體。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 5
  status: normal
- id: c9
  role: mechanism
  text: 透過這個篩選，排除了 "Therefore"、"We calculate"、"is equal to" 這些高機率但無資訊量的詞彙
  source_quotes:
  - "透過這個篩選機制，我們排除了 \"Therefore\", \"We calculate\", \"is equal to\" 這些高機率但無資訊量的詞彙"
  anchor_type: 設計參數
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: 一個關鍵字可能由多個 Token 組成，CER 用聯合機率（Joint Probability）計算這個單詞的整體自信度，也就是把所有組成 Token 的機率相乘：c_w = ∏ p_t；blog 說這是論文驗證後發現最有效的方法
  source_quotes:
  - "一個關鍵字 (例如 \"125\") 可能由多個 Token 組成 (例如 Token IDs `[1, 2, 5]`) 。我們需要一個函數 \\(f\\) 來計算這個單詞的整體自信度 \\(c_w\\)。"
  - "論文驗證後發現，最有效的方法是計算 **聯合機率 (Joint Probability)**，也就是將所有組成 Token 的機率相乘:"
  - "$$ c_w = f(\\{p_t | t \\in w\\}) = \\prod_{t \\in w} p_t $$"
  anchor_type: 原作者解讀
  importance: 10
  status: normal
- id: c11
  role: evaluation
  text: 'blog 認為 CER 教的第一件工程實戰價值是資料結構化的力量：透過 Prompt 強制模型輸出 Answer: 或 Response: 標籤，把非結構化的自然語言轉成半結構化的資料，這是在不改變模型架構下，提升系統可控性的關鍵技巧'
  source_quotes:
  - "CER 教會了我們兩件在工程實戰中極具價值的事:"
  - "**資料結構化的力量**: 透過 Prompt 強制模型輸出 `Answer:` 或 `Response:` 標籤，我們能將非結構化的自然語言轉化為半結構化的資料。這是在不改變模型架構下，提升系統可控性的關鍵技巧。"
  anchor_type: 部落格判斷
  importance: 11
  status: normal
- id: c12
  role: evaluation
  text: blog 認為第二件事是 Logits 是被低估的金礦：模型的原始輸出（Logits）包含比最終文字豐富得多的資訊，學會去雜存菁、只算關鍵 Token 的機率，是從現有模型中榨出更多效能的有效途徑
  source_quotes:
  - "**Logits 是被低估的金礦**: 模型的原始輸出 (Logits) 包含了比最終文字 (Text) 豐富得多的資訊。學會如何去雜存菁 (只算關鍵 Token 的機率) ，是我們從現有模型中榨出更多效能的有效途徑。"
  anchor_type: 部落格判斷
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: blog 指出 LLM-as-a-Verifier 也是讀取模型輸出的機率分佈，不過它讀的是 LLM 打分數時各個分數的機率，用期望值取代只取機率最高的那個分數，來解決評分老是平手的問題
  source_quotes:
  - "[LLM-as-a-Verifier](../llm-as-a-verifier/) 也是讀取模型輸出的機率分佈，不過它讀的是 LLM 打分數時各個分數的機率，用期望值取代只取機率最高的那個分數，來解決評分老是平手的問題。"
  anchor_type: 外部研究引用
  importance: 13
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

- 聯合機率（joint probability）：幾件事同時發生的機率。
- 獎勵模型（reward model）：另外訓練來替模型輸出打分數的模型。
