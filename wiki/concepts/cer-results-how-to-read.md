---
id: cer-results-how-to-read
title: CER 增強的是推理能力，不是知識庫存：看整個過程勝過只看最後一步，在數學上的表現通常比知識問答更穩定
type_hint: 發現
context_type: bound_to_source
sources:
- article: cer
  article_title: "ACL 2025 | 超越 Self-Consistency！CER 論文解析：無需訓練，靠「過程自信度」激發 Llama 3 與 DeepSeek 推理潛能"
  url: https://datasciocean.com/paper-intro/cer/
  sections:
  - 方法介紹
  - Confidence-Weighted Aggregation
  - "路徑層級聚合 (\\(g\\)): 從 Word 到 Path"
  - 實驗結果
  - "整體效能: CER 全面優於 Baseline"
  - 「弱模型」與「難任務」獲益更多
  - "核心假設驗證: 「過程」真的比「結果」重要"
  - "數學 vs. 知識問答: 推理與記憶的差異"
  - 適用於最新的推理模型 (DeepSeek-R1)
  - 結語
  first_appearance: true
parent: null
related:
  - cer-process-confidence-weighted-voting
  - cer-critical-token-confidence
  - judge-readable-vs-derive
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: CER 是用來增強「推理能力」的，而不是用來彌補「知識庫存」的：自信度可以過濾「邏輯謬誤」，但無法憑空創造「缺失的知識」
  source_quotes:
  - "這告訴我們: CER 是用來增強「推理能力」的，而不是用來彌補「知識庫存」的。"
  - "這提醒我們，**自信度可以過濾「邏輯謬誤」，但無法憑空創造「缺失的知識」。**"
  qualifiers:
  - text: CER 在數學推理上表現亮眼，但實驗也顯示了它在純知識檢索任務上的局限性
    source_quote: "最後，雖然 CER 在數學推理上表現亮眼，但實驗也顯示了它在純知識檢索任務上的局限性。"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: CER（Confidence Enhanced Reasoning）是一個不需要訓練的框架：它不像 Self-Consistency 那樣只計算每個答案出現了幾次，而是把支持該答案的所有路徑的自信度加總，而每條路徑的自信度是由推理過程中各步驟關鍵答案的自信度綜合而成
  source_quotes:
  - "這是一個完全 **無需訓練 (Training-free)** 的框架"
  - "**Self-Consistency (Baseline)**: 單純計算每個答案出現了幾次 (Count Voting) 。"
  - "**CER (Our Method)**: 計算支持該答案的所有路徑的**自信度總和**。"
  - "其中 \\(j\\) 是步驟的序號 (Step 1, Step 2...) ，\\(c_{a_j}\\) 是第 \\(j\\) 步關鍵答案的自信度。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: 論文的實驗涵蓋了 3B 到 8B 的模型規模，在三個數學資料集（GSM8K、MATH、MathQA）和兩個問答資料集（TriviaQA、HotPotQA）上測試，比較的基準包含貪婪解碼（Greedy）、Self-Consistency 以及其他基於機率的統計方法
  source_quotes:
  - "涵蓋了不同的模型規模 (從 3B 到 8B) 以及不同性質的任務 (數學推理與開放域問答) 。"
  - "作者在三個數學資料集 (GSM8K, MATH, MathQA) 和兩個問答資料集 (TriviaQA, HotPotQA) 上進行了測試。比較的基準 (Baseline) 包含貪婪解碼 (Greedy) 、Self-Consistency (SC) 以及其他基於機率的統計方法。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 3
  status: normal
- id: c4
  role: evidence
  text: 論文設了對照組 CER-LAST，忽略中間過程、只計算「最後一個答案」的自信度；blog 說，就它附上的這組 CER 與 CER-LAST 比較結果而言，考慮所有步驟的 CER 在所有情況下都顯著優於 CER-LAST
  source_quotes:
  - "作者設計了一個對照組 **CER-LAST**，即忽略中間過程，只計算「最後一個答案」的自信度。"
  - "結果如上圖所示，**CER (Blue Bar) 在所有情況下都顯著優於 CER-LAST (Red Bar)**。"
  comparison_target: CER-LAST（只計算最後一個答案的自信度）
  anchor_type: 實驗結果
  importance: 4
  status: normal
  figures:
  - file: figures/cer/figure3.png
    article: cer
    src: figure3.png
    caption: 'Figure 3: CER (藍色，考慮所有步驟) 與 CER-LAST (紅色，只看最後一步) 的效能比較。'
    sha256: 8ff5177e6134ec0464ae979432daadaa78f368416a762752bd7286cd28b498d8
- id: c5
  role: evaluation
  text: blog 認為 CER-LAST 的結果證明了作者的核心論點：模型可能在最後給出一個很有自信的錯誤答案，但在中間推理過程中其實已經顯露出猶豫；只看最後一步就會被模型騙過，只有全程監控才能抓出這些隱藏的錯誤
  source_quotes:
  - "這直接證明了作者的核心論點: 模型可能在最後給出一個很有自信的錯誤答案 (Overconfidence) ，但在中間推理過程中其實已經顯露出了猶豫。如果我們只看最後一步，就會被模型騙過；只有全程監控，才能抓出這些隱藏的錯誤。"
  anchor_type: 部落格推論
  importance: 5
  status: normal
- id: c6
  role: evidence
  text: 比較數學任務與開放域問答的結果，CER 在數學上的表現通常比問答更穩定
  source_quotes:
  - "比較數學任務與開放域問答 (QA) 的結果，我們發現 CER 在數學上的表現通常比 QA 更穩定。"
  comparison_target: 開放域問答（TriviaQA、HotPotQA）上的表現
  anchor_type: 部落格判斷
  importance: 6
  status: normal
  figures:
  - file: figures/cer/table1.png
    article: cer
    src: table1.png
    caption: 'Table 1: 在數學任務上的準確率比較。綠色數字代表相較於最佳 Baseline 的提升幅度。'
    sha256: b73cfdea9603a77e75f65d7762123b263ef4205ebf2044defe6bd64090f42d0c
  - file: figures/cer/table2.png
    article: cer
    src: table2.png
    caption: 'Table 2: 在開放域問答任務（TriviaQA, HotPotQA）上的準確率比較。可以看到部分模型（如 Llama-3.2-3B）在知識密集型任務上的提升幅度不如數學任務顯著。'
    sha256: 69fbe9af49ada3f3b0f527cdc4addc81201b8f33753937714246228ff807df83
- id: c7
  role: evaluation
  text: blog 對數學與問答差異的解釋是：數學是邏輯推理，CER 可以透過自信度判斷邏輯是否連貫；問答是知識檢索，如果模型參數裡根本沒有這個知識，不管怎麼推理、自信度怎麼算，模型都不可能答對（這被稱為「因無知而產生的幻覺」）
  source_quotes:
  - "**數學是邏輯推理**: CER 可以透過自信度判斷邏輯是否連貫。"
  - "**QA 是知識檢索**: 如果模型參數裡根本**沒有這個知識** (Knowledge Gap) ，不管怎麼推理、自信度怎麼算，模型都不可能答對 (這被稱為「因無知而產生的幻覺」) 。"
  anchor_type: 部落格推論
  importance: 7
  status: normal
- id: c8
  role: anchor
  text: Llama 3.2 3B 在數學上提升了 4.1%，但在問答上幾乎沒有幫助
  source_quotes:
  - "特別是 **Llama 3.2 3B** 這個模型，在數學上提升了 4.1%，但在 QA 上幾乎沒有幫助。"
  anchor_type: 實驗結果
  importance: 8
  status: pending_author_confirmation
  figures:
  - file: figures/cer/table1.png
    article: cer
    src: table1.png
    caption: 'Table 1: 在數學任務上的準確率比較。綠色數字代表相較於最佳 Baseline 的提升幅度。'
    sha256: b73cfdea9603a77e75f65d7762123b263ef4205ebf2044defe6bd64090f42d0c
  - file: figures/cer/table2.png
    article: cer
    src: table2.png
    caption: 'Table 2: 在開放域問答任務（TriviaQA, HotPotQA）上的準確率比較。可以看到部分模型（如 Llama-3.2-3B）在知識密集型任務上的提升幅度不如數學任務顯著。'
    sha256: 69fbe9af49ada3f3b0f527cdc4addc81201b8f33753937714246228ff807df83
- id: c9
  role: evidence
  text: blog 說 CER 在所有資料集和模型上都取得了比 Baseline 更好的成績
  source_quotes:
  - "**一致性提升**: CER 在所有資料集和模型上都取得了比 Baseline 更好的成績。"
  comparison_target: Baseline（貪婪解碼、Self-Consistency 以及其他基於機率的統計方法）
  anchor_type: 實驗結果
  importance: 9
  status: pending_author_confirmation
  figures:
  - file: figures/cer/table1.png
    article: cer
    src: table1.png
    caption: 'Table 1: 在數學任務上的準確率比較。綠色數字代表相較於最佳 Baseline 的提升幅度。'
    sha256: b73cfdea9603a77e75f65d7762123b263ef4205ebf2044defe6bd64090f42d0c
  - file: figures/cer/table2.png
    article: cer
    src: table2.png
    caption: 'Table 2: 在開放域問答任務（TriviaQA, HotPotQA）上的準確率比較。可以看到部分模型（如 Llama-3.2-3B）在知識密集型任務上的提升幅度不如數學任務顯著。'
    sha256: 69fbe9af49ada3f3b0f527cdc4addc81201b8f33753937714246228ff807df83
- id: c10
  role: anchor
  text: 在 MathQA 這種難度較高的資料集上，CER 的提升幅度達到 7.4%（OLMo-2-7B）
  source_quotes:
  - "**顯著差異**: 在 MathQA 這種難度較高的資料集上，提升幅度甚至達到了 **7.4%** (OLMo-2-7B) 。"
  - "比較的基準 (Baseline) 包含貪婪解碼 (Greedy) 、Self-Consistency (SC) 以及其他基於機率的統計方法。"
  comparison_target: Baseline（blog 正文列出貪婪解碼、Self-Consistency 以及其他基於機率的統計方法，沒指明是其中哪一個）
  anchor_type: 實驗結果
  importance: 10
  status: normal
  figures:
  - file: figures/cer/table1.png
    article: cer
    src: table1.png
    caption: 'Table 1: 在數學任務上的準確率比較。綠色數字代表相較於最佳 Baseline 的提升幅度。'
    sha256: b73cfdea9603a77e75f65d7762123b263ef4205ebf2044defe6bd64090f42d0c
- id: c11
  role: evidence
  text: CER 的提升幅度並不是均勻的；像 Llama 3.1 8B 這樣強大的模型，在相對簡單的 GSM8K 上提升幅度較小
  source_quotes:
  - "如果我們仔細觀察數據，會發現提升的幅度並不是均勻的。"
  - "**強模型 (Strong Models)**: 對於像 **Llama 3.1 8B** 這樣強大的模型，在相對簡單的 GSM8K 任務上，提升幅度較小"
  anchor_type: 實驗結果
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 11
  status: normal
  figures:
  - file: figures/cer/table1.png
    article: cer
    src: table1.png
    caption: 'Table 1: 在數學任務上的準確率比較。綠色數字代表相較於最佳 Baseline 的提升幅度。'
    sha256: b73cfdea9603a77e75f65d7762123b263ef4205ebf2044defe6bd64090f42d0c
- id: c12
  role: anchor
  text: Llama 3.1 8B 在 GSM8K 上的提升幅度約 0.4%
  source_quotes:
  - "對於像 **Llama 3.1 8B** 這樣強大的模型，在相對簡單的 GSM8K 任務上，提升幅度較小 (約 0.4%) 。"
  - "比較的基準 (Baseline) 包含貪婪解碼 (Greedy) 、Self-Consistency (SC) 以及其他基於機率的統計方法。"
  comparison_target: Baseline（blog 正文列出貪婪解碼、Self-Consistency 以及其他基於機率的統計方法，沒指明是其中哪一個）
  anchor_type: 實驗結果
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: blog 對強模型提升小的解釋是：強模型原本就很有信心，且錯誤率極低，改進空間有限
  source_quotes:
  - "這是因為強模型原本就很有信心，且錯誤率極低，改進空間有限。"
  anchor_type: 部落格推論
  importance: 13
  status: normal
- id: c14
  role: evidence
  text: 對於參數較少或推理能力較弱的模型（如 OLMo 2 7B 或 Mistral 7B），CER 帶來的提升非常巨大；blog 的解釋是弱模型面對難題時往往生成許多「似是而非」的推理路徑，CER 像一個過濾器，透過檢查中間步驟的自信度，篩掉那些模型自己都「心虛」的錯誤路徑
  source_quotes:
  - "**弱模型 (Weak Models)**: 對於參數較少或推理能力較弱的模型 (如 **OLMo 2 7B** 或 **Mistral 7B**) ，CER 帶來的提升非常巨大。"
  - "弱模型在面對難題時，往往會生成許多「似是而非」的推理路徑 (雜訊) 。CER 就像一個過濾器，透過檢查中間步驟的自信度，成功幫弱模型篩掉了那些它自己都「心虛」的錯誤路徑"
  anchor_type: 部落格推論
  importance: 14
  status: pending_author_confirmation
  figures:
  - file: figures/cer/table1.png
    article: cer
    src: table1.png
    caption: 'Table 1: 在數學任務上的準確率比較。綠色數字代表相較於最佳 Baseline 的提升幅度。'
    sha256: b73cfdea9603a77e75f65d7762123b263ef4205ebf2044defe6bd64090f42d0c
- id: c15
  role: anchor
  text: 即使是經過強化學習優化、已經專門針對思維鏈微調過的 DeepSeek-R1 變體，CER 依然能將 GSM8K 的準確率從 87.2% 提升到 90.2%
  source_quotes:
  - "作者還測試了近期非常熱門的 **DeepSeek-R1** 變體 (經過強化學習優化的推理模型) 。結果顯示，即使是這種已經專門針對 CoT 微調過的模型，CER 依然能將 GSM8K 的準確率從 87.2% 提升到 **90.2%**。"
  qualifiers:
  - text: 測試的模型是 DeepSeek-R1-Distill-Qwen-7B
    source_quote: "CER 應用於 DeepSeek-R1-Distill-Qwen-7B 模型上的表現"
    source: figure_caption
  anchor_type: 實驗結果
  importance: 15
  status: pending_author_confirmation
  figures:
  - file: figures/cer/table3.png
    article: cer
    src: table3.png
    caption: 'Table 3: CER 應用於 DeepSeek-R1-Distill-Qwen-7B 模型上的表現。即使在經過強化學習優化（RL）的強推理模型上，CER 依然能將 GSM8K 的準確率進一步推升。'
    sha256: 36ceb944ae23bd1dfef311c58fa0e6c2afb7713cc243712328361f874d97ca65
- id: c16
  role: evaluation
  text: blog 由 DeepSeek-R1 變體的結果推論，CER 捕捉到的「自信度訊號」是模型內部普遍存在的特徵，即便是經過 RLHF 訓練後的模型也依然保有這些資訊可供利用
  source_quotes:
  - "為了驗證方法的通用性，作者還測試了近期非常熱門的 **DeepSeek-R1** 變體 (經過強化學習優化的推理模型) 。"
  - "這意味著 CER 所捕捉到的「自信度訊號」，是模型內部普遍存在的特徵，即便是經過 RLHF 訓練後的模型也依然保有這些資訊可供利用。"
  qualifiers:
  - text: blog 在同一節把這個 DeepSeek-R1 變體描述為經過強化學習優化的推理模型
    source_quote: "**DeepSeek-R1** 變體 (經過強化學習優化的推理模型)"
  - text: 這個推論的依據是一個 DeepSeek-R1 變體（DeepSeek-R1-Distill-Qwen-7B）上的測試
    source_quote: "CER 應用於 DeepSeek-R1-Distill-Qwen-7B 模型上的表現"
    source: figure_caption
  anchor_type: 部落格推論
  importance: 16
  status: normal
  figures:
  - file: figures/cer/table3.png
    article: cer
    src: table3.png
    caption: 'Table 3: CER 應用於 DeepSeek-R1-Distill-Qwen-7B 模型上的表現。即使在經過強化學習優化（RL）的強推理模型上，CER 依然能將 GSM8K 的準確率進一步推升。'
    sha256: 36ceb944ae23bd1dfef311c58fa0e6c2afb7713cc243712328361f874d97ca65
```

## 名詞補充（通用知識，非 blog 內容）

- 貪婪解碼（greedy decoding）：每一步都直接選機率最高的 token，只生成一條答案。
- RLHF（reinforcement learning from human feedback）：用人類偏好訓練出的獎勵訊號，以強化學習微調語言模型的做法。
