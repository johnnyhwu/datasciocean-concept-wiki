---
id: cer-process-confidence-weighted-voting
title: CER 不讓每條推理路徑都算一票，而是用路徑中間步驟的自信度加權投票，而且不需要任何訓練
type_hint: 方法
context_type: bound_to_source
sources:
- article: cer
  article_title: "ACL 2025 | 超越 Self-Consistency！CER 論文解析：無需訓練，靠「過程自信度」激發 Llama 3 與 DeepSeek 推理潛能"
  url: https://datasciocean.com/paper-intro/cer/
  sections:
  - 前言
  - Limitations of Self-Consistency
  - Neglect of Intermediate Reasoning Steps
  - 方法介紹
  - Reasoning Path Generation
  - "路徑層級聚合 (\\(g\\)): 從 Word 到 Path"
  - Confidence-Weighted Aggregation
  - "核心假設驗證: 「過程」真的比「結果」重要"
  - 結語
  first_appearance: true
parent: null
related:
  - cer-critical-token-confidence
  - cer-results-how-to-read
  - confidence-three-metrics
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: CER 的核心理念是「不要只數人頭，要看信心」：Self-Consistency 假設每一條推理路徑的權重都是平等的，CER 則計算支持某個答案的所有路徑的自信度總和；論文的核心貢獻在於證明了推理過程中的自信度比單純看最終答案的自信度更具參考價值，而且整個框架完全不需要訓練
  source_quotes:
  - "CER (Confidence Enhanced Reasoning) 的核心理念在於:"
  - "不要看整句話，只看重點；不要只數人頭，要看信心。"
  - "它假設每一條推理路徑的權重都是平等的，忽略了模型在生成過程中的「猶豫」或「自信」。"
  - "**CER (Our Method)**: 計算支持該答案的所有路徑的**自信度總和**。"
  - "其核心貢獻在於證明了 **「推理過程中的自信度 (Process Confidence) 」比單純看「最終答案的自信度」更具參考價值**。"
  - "這是一個完全 **無需訓練 (Training-free)** 的框架"
  qualifiers:
  - text: 實驗也顯示 CER 在純知識檢索任務上有局限性
    source_quote: "雖然 CER 在數學推理上表現亮眼，但實驗也顯示了它在純知識檢索任務上的局限性。"
  anchor_type: 原作者解讀
  importance: 1
  status: normal
- id: c2
  role: context
  text: CER（Confidence Enhanced Reasoning）是被 ACL 2025 Main Conference 接收的論文，它不需要訓練額外的獎勵模型（Reward Model），也不需要微調 LLM，只靠精心設計的 Prompt 配合模型輸出的 Logits（機率分佈）
  source_quotes:
  - "這篇論文已被 **ACL 2025 Main Conference** 接收"
  - "它不需要訓練額外的獎勵模型 (Reward Model) ，也不需要微調 LLM。它僅僅透過精心設計的 Prompt 配合模型輸出的 Logits (機率分佈)"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 2
  status: normal
- id: c3
  role: context
  text: Self-Consistency（SC）是目前提升推理能力最主流的方法：讓模型對同一個問題生成 K 條不同的推理路徑，再用多數決（Majority Voting）選出現次數最多的答案
  source_quotes:
  - "目前提升推理能力最主流的方法是 **Self-Consistency (SC)**。它的概念很簡單: 讓模型對同一個問題生成 \\(K\\) 條不同的推理路徑 (Reasoning Paths) ，然後統計出現次數最多的答案作為最終結果 (Majority Voting) 。"
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: SC 隱含一個危險的假設：每一條生成的路徑都是「平等」的。模型嚴謹推導、很有信心得出的答案，和推導過程充滿猶豫、最後剛好湊出的答案，在 SC 裡這一票權重一樣
  source_quotes:
  - "這種方法雖然有效，但隱含了一個危險的假設: **每一條生成的路徑都是「平等」的。**"
  - "**情境 A**: 模型經過嚴謹推導，非常有信心地得出答案。"
  - "**情境 B**: 模型在推導過程中充滿猶豫 (低機率) ，最後剛好湊出一個答案。"
  - "在 SC 的機制下，情境 A 和情境 B 的這一票權重是一樣的。"
  anchor_type: 部落格舉例
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 當模型出現「一致性幻覺」，也就是很有信心地、反覆地生成同一個錯誤答案時，SC 會毫不猶豫地選出這個錯誤答案，因為它只看「數量」，不看「品質」
  source_quotes:
  - "更糟糕的是，當模型出現「一致性幻覺 (Consistent Hallucination) 」時——即模型很有信心地、反覆地生成同一個錯誤答案——SC 會毫不猶豫地選出這個錯誤答案，因為它只看「數量」，不看「品質」。"
  anchor_type: 部落格推論
  importance: 9
  status: normal
- id: c6
  role: mechanism
  text: 現有許多方法傾向只評估最終生成答案的自信度，忽略了錯誤往往發生在中間；一個數學題的第二步算錯了，後面推導邏輯再完美、模型再有自信，最終答案也是錯的
  source_quotes:
  - "現有的許多方法傾向於只評估**最終生成答案**的自信度。這忽略了一個核心事實: **錯誤往往發生在中間。**"
  - "一個數學題可能需要五個步驟，如果第二步算錯了，即便後面三步的推導邏輯再完美、模型再有自信，最終答案也是錯的。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 假設題設
  importance: 5
  status: normal
- id: c7
  role: mechanism
  text: 論文認為判斷一條路徑是否可靠必須檢查過程中的每個轉折點：如果模型在中間某一步驟表現出猶豫（高熵值、低機率），這條路徑的權重就應該被大幅降低
  source_quotes:
  - "本篇論文認為，要判斷一條路徑是否可靠，我們不能只看終點，必須檢查過程中的每一個轉折點。如果模型在中間某一步驟表現出猶豫 (高熵值、低機率) ，這就是一個強烈的警訊，暗示這條路徑的權重應該被大幅降低。"
  anchor_type: 原作者解讀
  importance: 6
  status: normal
- id: c8
  role: mechanism
  text: CER 先像 SC 一樣，通常會設定較高的採樣溫度讓模型對同一個問題生成 K 條不同的推理路徑，關鍵改動在 Prompt：要求模型在每一個推理步驟結束時依特定格式輸出中間答案
  source_quotes:
  - "這一步與 Self-Consistency 類似，我們通常會設定較高的採樣溫度 (例如 \\(T=0.7\\) 或 \\(T=1.0\\)) ，讓模型發揮創造力，生成 \\(K\\) 條不同的推理路徑 (Reasoning Paths) 。"
  - "但在這裡，CER 做了一個關鍵的改動: **Prompt 的設計**。"
  - "我們要求模型在每一個推理步驟結束時，必須依照特定的格式輸出中間答案。"
  anchor_type: 設計參數
  importance: 7
  status: normal
  figures:
  - file: figures/cer/figure4.png
    article: cer
    src: figure4.png
    caption: 'CER 用於數學推理的 Prompt 範例。注意它要求模型使用 ''Answer: [answer]'' 格式輸出。'
    sha256: 77b12fdb4bf388f21e65ba39c0aff51362e9dd8ac8af3708a2c11cd8e423a6ce
- id: c9
  role: mechanism
  text: 每條路徑的分數 C_path 用線性加權平均把各步驟中間答案的自信度綜合起來：C_path = Σ j·c_aj / Σ j，其中 j 是步驟序號、c_aj 是第 j 步關鍵答案的自信度，所以越靠近最終答案的步驟，權重越重
  source_quotes:
  - "CER 採用的是 **線性加權平均 (Linearly Weighted Mean)**。"
  - "$$ C_{path} = \\frac{\\sum_{j=1}^{n} j \\cdot c_{a_j}}{\\sum_{j=1}^{n} j} $$"
  - "其中 \\(j\\) 是步驟的序號 (Step 1, Step 2...) ，\\(c_{a_j}\\) 是第 \\(j\\) 步關鍵答案的自信度。"
  - "**越靠近最終答案的步驟，權重越重。**"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c10
  role: mechanism
  text: blog 對加權的解釋是推理是累積的：Step 1 通常只是理解題目、較為簡單，最後的 Step N 往往依賴前面所有步驟的正確性
  source_quotes:
  - "因為推理是累積的。Step 1 通常只是理解題目，較為簡單；而最後的 Step \\(N\\) 往往依賴於前面所有步驟的正確性。"
  anchor_type: 部落格推論
  importance: 10
  status: normal
- id: c11
  role: mechanism
  text: blog 對加權的另一個解釋是：如果模型對最後一步非常有信心，通常暗示前面的基礎也是穩固的
  source_quotes:
  - "如果模型對最後一步非常有信心，通常暗示前面的基礎也是穩固的。"
  qualifiers:
  - text: 同一篇 blog 在 CER-LAST 消融處又說，模型可能在最後給出一個很有自信的錯誤答案，但在中間推理過程中其實已經顯露出了猶豫
    source_quote: "模型可能在最後給出一個很有自信的錯誤答案 (Overconfidence) ，但在中間推理過程中其實已經顯露出了猶豫。"
  anchor_type: 部落格推論
  importance: 14
  status: normal
- id: c12
  role: mechanism
  text: 最後從 K 條路徑選答案：SC 只計算每個答案出現了幾次，CER 則把支持該答案的所有路徑的自信度加總，選總分最高的答案
  source_quotes:
  - "**Self-Consistency (Baseline)**: 單純計算每個答案出現了幾次 (Count Voting) 。"
  - "**CER (Our Method)**: 計算支持該答案的所有路徑的**自信度總和**。"
  - "我們最終選取得分 \\(Score(Answer)\\) 最高的那個答案。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c13
  role: mechanism
  text: 這樣一來，一條路徑若中間過程猶豫不決（自信度低），對總分的貢獻就很小；一條每一步都很有把握的路徑，則會對最終決策產生決定性的影響
  source_quotes:
  - "如果有一條路徑雖然得出了某個答案，但中間過程猶豫不決 (自信度低) ，它對總分的貢獻就會很小；反之，一條邏輯清晰、每一步都很有把握的路徑，將會對最終決策產生決定性的影響。"
  anchor_type: 部落格推論
  importance: 8
  status: normal
- id: c14
  role: evidence
  text: 論文的消融實驗設了對照組 CER-LAST，只計算「最後一個答案」的自信度、忽略中間過程；blog 說，就它附上的這組 CER 與 CER-LAST 比較結果而言，考慮所有步驟的 CER 在所有情況下都顯著優於 CER-LAST
  source_quotes:
  - "作者設計了一個對照組 **CER-LAST**，即忽略中間過程，只計算「最後一個答案」的自信度。"
  - "結果如上圖所示，**CER (Blue Bar) 在所有情況下都顯著優於 CER-LAST (Red Bar)**。"
  comparison_target: CER-LAST（只計算最後一個答案的自信度）
  anchor_type: 實驗結果
  importance: 11
  status: normal
  figures:
  - file: figures/cer/figure3.png
    article: cer
    src: figure3.png
    caption: 'Figure 3: CER (藍色，考慮所有步驟) 與 CER-LAST (紅色，只看最後一步) 的效能比較。'
    sha256: 8ff5177e6134ec0464ae979432daadaa78f368416a762752bd7286cd28b498d8
- id: c15
  role: evaluation
  text: blog 認為這篇論文給的啟示是：在大型語言模型的推理中，「過程」的品質決定了「結果」的可靠性；SC 用多數決解決了隨機性的問題，卻忽略了隱藏在 Logits 中的猶豫與自信
  source_quotes:
  - "這篇論文給了我們一個重要的啟示: **在大型語言模型的推理中，「過程」的品質決定了「結果」的可靠性。**"
  - "過去的 Self-Consistency (SC) 方法雖然透過「多數決」解決了隨機性的問題，但它忽略了模型內部的細微聲音——那些隱藏在 Logits 中的猶豫與自信。"
  anchor_type: 部落格判斷
  importance: 12
  status: normal
- id: c16
  role: evaluation
  text: blog 指出 DeepConf 也處理 Majority Voting 的這個弱點，做法是用從 Token Entropy 算出的信心分數為每一票加權
  source_quotes:
  - "[DeepConf](../deepconf/) 也處理了 Majority Voting 的這個弱點，它透過從 Token Entropy 算出的信心分數來為每一票加權，而不是每條路徑都算一票。"
  anchor_type: 外部研究引用
  importance: 13
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

- 採樣溫度（temperature）：控制模型輸出隨機程度的參數；溫度越高，每次生成的結果差異越大。
- 熵（entropy）：衡量一個機率分佈有多分散；模型對下一個 token 越拿不定主意，熵越高。
- 獎勵模型（reward model）：另外訓練來替模型輸出打分數的模型。
