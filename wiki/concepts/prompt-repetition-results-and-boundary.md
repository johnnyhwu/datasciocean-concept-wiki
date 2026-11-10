---
id: prompt-repetition-results-and-boundary
title: Prompt Repetition 在 70 個模型－任務組合中 47 勝 0 敗，但強制開啟 CoT 後效果變成中性；它最適合需要精準理解、但不需要複雜多步推理的任務
type_hint: 發現
context_type: bound_to_source
sources:
- article: prompt-repetition
  article_title: "Google 2025 論文解讀：只要「複製貼上」就能變強？Prompt Repetition 如何成為 LLM 的免費午餐"
  url: https://datasciocean.com/paper-intro/prompt-repetition/
  sections:
  - 前言
  - 方法介紹
  - 核心操作：Prompt Repetition
  - 驚人的「零敗績」紀錄
  - 對「輸入順序」的強大修復力
  - 推理任務 vs. 非推理任務
  - 自定義任務的「顯微鏡效應」
  - 我們學到了什麼？
  first_appearance: true
parent: null
related:
  - prompt-repetition-causal-bottleneck-and-fix
  - prompt-repetition-free-lunch-latency
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: Prompt Repetition 在總共 70 個「模型－任務」組合中取得 47 勝 0 敗；但強制模型開啟 "Think step by step"（CoT）後，效果變成「中性至微幅正面」（5 勝 1 敗 22 平）；blog 據此認為 Prompt Repetition 最適合那些「需要精準理解，但不需要複雜多步推理」的任務
  source_quotes:
  - "在總共 70 個「模型-任務」的組合測試中，Prompt Repetition 取得了 **47 勝 0 敗** 的壓倒性成績"
  - "強制模型開啟 **\"Think step by step\" (CoT)**。"
  - "當開啟 CoT 後，Prompt Repetition 的效果變成了 **「中性至微幅正面」** (5 勝 1 敗 22 平) 。"
  - "這告訴我們：**Prompt Repetition 最適合那些「需要精準理解，但不需要複雜多步推理」的任務**"
  comparison_target: Baseline（不重複 Prompt）；CoT 設定下比的是 Baseline + CoT
  anchor_type: 部落格判斷
  importance: 1
  status: normal
  figures:
  - file: figures/prompt-repetition/figure1.png
    article: prompt-repetition
    src: figure1.png
    caption: 'Figure 1: Prompt Repetition 與 Baseline 在各種模型及 Benchmark 上的準確率比較。'
    sha256: dfc0be7ddacaca3ce5f4b8e11573850289d43b5878ddc46315f479b01f46b0a8
  - file: figures/prompt-repetition/figure4.png
    article: prompt-repetition
    src: figure4.png
    caption: 'Figure 4: 當開啟推理模式 (step by step) 後，Prompt Repetition 與 Baseline 的準確率差距縮小，效果變得中性。'
    sha256: 86135ff0b3f97b8453273a028559f3e0d1dd5b128247cdf929e362c7b82b2229
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
  role: anchor
  text: 作者使用 McNemar 檢定評估統計顯著性（設定 p < 0.1）；在總共 70 個「模型－任務」組合中，Prompt Repetition 取得 47 勝 0 敗，其餘為平手或無顯著差異
  source_quotes:
  - "作者使用了 **McNemar 檢定** 來評估統計顯著性 (設定 \\(p < 0.1\\)) 。"
  - "在總共 70 個「模型-任務」的組合測試中，Prompt Repetition 取得了 **47 勝 0 敗** 的壓倒性成績 (其餘為平手/無顯著差異) 。"
  comparison_target: Baseline（不重複 Prompt）
  qualifiers:
  - text: 另一組強制開啟 CoT 的對照實驗中，Prompt Repetition 的效果變成「中性至微幅正面」（5 勝 1 敗 22 平）
    source_quote: "當開啟 CoT 後，Prompt Repetition 的效果變成了 **「中性至微幅正面」** (5 勝 1 敗 22 平) 。"
  anchor_type: 實驗結果
  importance: 3
  status: normal
  figures:
  - file: figures/prompt-repetition/figure1.png
    article: prompt-repetition
    src: figure1.png
    caption: 'Figure 1: Prompt Repetition 與 Baseline 在各種模型及 Benchmark 上的準確率比較。'
    sha256: dfc0be7ddacaca3ce5f4b8e11573850289d43b5878ddc46315f479b01f46b0a8
- id: c4
  role: evaluation
  text: blog 認為這在機器學習領域極為罕見：通常某個 Trick 可能對 GPT 有效、對 Claude 卻無效，但 Prompt Repetition 跨越了不同的模型架構與參數量級
  source_quotes:
  - "這在機器學習領域極為罕見。通常某個 Trick 可能對 GPT 有效，對 Claude 卻無效。但 Prompt Repetition 跨越了不同的模型架構與參數量級。"
  qualifiers:
  - text: 強制開啟 CoT 後，Prompt Repetition 的效果變成「中性至微幅正面」（5 勝 1 敗 22 平）
    source_quote: "當開啟 CoT 後，Prompt Repetition 的效果變成了 **「中性至微幅正面」** (5 勝 1 敗 22 平) 。"
  anchor_type: 部落格判斷
  importance: 4
  status: normal
- id: c5
  role: evidence
  text: 論文比較了 Options-first（<選項> <問題>）與 Question-first（<問題> <選項>）兩種格式：在 Baseline 中 Options-first 的表現通常較差；一旦使用 Prompt Repetition，Options-first 的性能獲得了巨大的提升，表現甚至追平或超越了原本較優的 Question-first
  source_quotes:
  - "論文比較了兩種格式："
  - "**Options-first:** `<選項> <問題>`"
  - "**Question-first:** `<問題> <選項>`"
  - "實驗發現，在 Baseline 中，`Options-first` 的表現通常較差 (因為讀選項時不知道問題) 。然而，一旦使用了 **Prompt Repetition**："
  - "`Options-first` 的性能獲得了巨大的提升。"
  - "其表現甚至追平或超越了原本較優的 `Question-first`。"
  comparison_target: Baseline 的 Options-first；以及原本較優的 Question-first
  qualifiers:
  - text: blog 要讀者特別注意的 Options-first 結果在 OpenBookQA 和 MMLU-Pro 這兩個 Benchmark
    source_quote: "Figure 1: (同上圖) 請特別注意 OpenBookQA 和 MMLU-Pro 中的 \"options-first\" 欄位。"
    source: figure_caption
  anchor_type: 實驗結果
  importance: 5
  status: normal
  figures:
  - file: figures/prompt-repetition/figure1.png
    article: prompt-repetition
    src: figure1.png
    caption: 'Figure 1: (同上圖) 請特別注意 OpenBookQA 和 MMLU-Pro 中的 "options-first" 欄位。'
    sha256: dfc0be7ddacaca3ce5f4b8e11573850289d43b5878ddc46315f479b01f46b0a8
- id: c6
  role: evaluation
  text: blog 認為這證實了它的理論：重複輸入讓模型在閱讀第二次的選項時，已經知道了問題是什麼
  source_quotes:
  - "這證實了我們的理論：**重複輸入讓模型在閱讀第二次的選項時，已經知道了問題是什麼**。"
  qualifiers:
  - text: blog 要讀者特別注意的 Options-first 結果在 OpenBookQA 和 MMLU-Pro 這兩個 Benchmark
    source_quote: "Figure 1: (同上圖) 請特別注意 OpenBookQA 和 MMLU-Pro 中的 \"options-first\" 欄位。"
    source: figure_caption
  anchor_type: 部落格推論
  importance: 6
  status: normal
  figures:
  - file: figures/prompt-repetition/figure1.png
    article: prompt-repetition
    src: figure1.png
    caption: 'Figure 1: (同上圖) 請特別注意 OpenBookQA 和 MMLU-Pro 中的 "options-first" 欄位。'
    sha256: dfc0be7ddacaca3ce5f4b8e11573850289d43b5878ddc46315f479b01f46b0a8
- id: c7
  role: evidence
  text: 為了探討邊界，作者做了對照實驗，強制模型開啟 "Think step by step"（CoT）；結果 Prompt Repetition 的效果變成「中性至微幅正面」（5 勝 1 敗 22 平）
  source_quotes:
  - "為了探討邊界，作者做了一個有趣的對照實驗：強制模型開啟 **\"Think step by step\" (CoT)**。"
  - "當開啟 CoT 後，Prompt Repetition 的效果變成了 **「中性至微幅正面」** (5 勝 1 敗 22 平) 。"
  comparison_target: Baseline + CoT（不重複 Prompt、同樣開啟 CoT）
  anchor_type: 實驗結果
  importance: 7
  status: normal
  figures:
  - file: figures/prompt-repetition/figure4.png
    article: prompt-repetition
    src: figure4.png
    caption: 'Figure 4: 當開啟推理模式 (step by step) 後，Prompt Repetition 與 Baseline 的準確率差距縮小，效果變得中性。'
    sha256: 86135ff0b3f97b8453273a028559f3e0d1dd5b128247cdf929e362c7b82b2229
- id: c8
  role: evaluation
  text: blog 對 CoT 結果的解讀：Baseline + CoT 時，模型自己在 Output 階段做了重複／思考，修復了表徵問題；所以 Repetition + CoT 時，在 Input 端幫它重複一次的邊際效益就遞減了
  source_quotes:
  - "**Baseline + CoT:** 模型自己在 Output 階段做了重複/思考，修復了表徵問題。"
  - "**Repetition + CoT:** 雖然沒壞處，但因為模型已經會自己修復了，我們在 Input 端幫它重複一次的邊際效益就遞減了 (Diminishing Returns)。"
  anchor_type: 部落格推論
  importance: 8
  status: normal
- id: c9
  role: evaluation
  text: blog 舉的適用任務例子是資訊提取、閱讀測驗這類「需要精準理解，但不需要複雜多步推理」的任務
  source_quotes:
  - "**Prompt Repetition 最適合那些「需要精準理解，但不需要複雜多步推理」的任務** (如資訊提取、閱讀測驗) 。"
  anchor_type: 部落格判斷
  importance: 9
  status: normal
- id: c10
  role: context
  text: 作者設計了兩個極端的「查找任務」（Appendix A.3），其中最經典的是 NameIndex：給一串 50 個名字，問「第 25 個名字是誰？」
  source_quotes:
  - "作者設計了兩個極端的「查找任務」 (Appendix A.3) ，其中最經典的是 **NameIndex** 任務。"
  - "**任務：** 給一串 50 個名字，問：「第 25 個名字是誰？」"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 10
  status: normal
- id: c11
  role: anchor
  text: 在 NameIndex 上，Gemini 2.0 Flash-Lite 的 Baseline 只有 21.33%，使用 Prompt Repetition 後達到 97.33%
  source_quotes:
  - "**Gemini 2.0 Flash-Lite 的表現：**"
  - "**Baseline:** **21.33%** (幾乎是瞎猜)。"
  - "**Prompt Repetition:** **97.33%** (接近完美)。"
  comparison_target: 同一模型（Gemini 2.0 Flash-Lite）在 NameIndex 上的 Baseline（21.33%）
  qualifiers:
  - text: NameIndex 是作者設計的極端查找任務
    source_quote: "作者設計了兩個極端的「查找任務」 (Appendix A.3)"
  anchor_type: 實驗結果
  importance: 11
  status: normal
  figures:
  - file: figures/prompt-repetition/figure1.png
    article: prompt-repetition
    src: figure1.png
    caption: 'Figure 1: Prompt Repetition 與 Baseline 在各種模型及 Benchmark 上的準確率比較。'
    sha256: dfc0be7ddacaca3ce5f4b8e11573850289d43b5878ddc46315f479b01f46b0a8
- id: c12
  role: evaluation
  text: blog 對差距的解釋：Baseline 中，模型讀到那個名字時還不知道問題是要找哪一個，所以沒有特別記住；等讀完問題已經來不及回頭（因果限制）。Prompt Repetition 讓模型在讀第二遍時，帶著「要找哪一個」的意圖去掃描列表
  source_quotes:
  - "因為在 Baseline 中，模型讀到第 25 個名字時，還不知道問題是「找第 25 個」，所以它沒有特別記住那個名字。等到讀完問題，已經來不及回頭了 (因果限制) 。而 Prompt Repetition 讓模型在讀 **第二遍** 時，帶著「我要找第 25 個」的強烈意圖去掃描列表，自然一抓一個準。"
  anchor_type: 部落格推論
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: blog 認為這個極端的例子是本篇論文最有力的證據，證明了 Prompt Repetition 賦予了模型類似 Random Access Memory 的能力
  source_quotes:
  - "這個極端的例子，是本篇論文最有力的證據，證明了 Prompt Repetition 賦予了模型類似 **Random Access Memory** 的能力。"
  qualifiers:
  - text: 這個例子的數字只列出單一模型 Gemini 2.0 Flash-Lite 的表現
    source_quote: "**Gemini 2.0 Flash-Lite 的表現：**"
  - text: NameIndex 是作者設計的極端查找任務
    source_quote: "作者設計了兩個極端的「查找任務」 (Appendix A.3)"
  anchor_type: 部落格判斷
  importance: 13
  status: normal
- id: c14
  role: evaluation
  text: 經過強化學習（RL）訓練的 Reasoning Models（如 o1）往往會在推理過程中自發性地學會「把問題重說一遍」；blog 認為這暗示 Prompt Repetition 也許是模型為了克服注意力瓶頸而演化出的一種隱式策略（Implicit Strategy），而這篇論文的貢獻就是把這個策略「顯式化」並應用在非推理模型上
  source_quotes:
  - "經過強化學習 (RL) 訓練的 Reasoning Models (如 o1)，往往會在推理過程自發性地學會「把問題重說一遍」。這暗示了 Prompt Repetition 也許是模型為了克服注意力瓶頸而演化出的一種 Implicit Strategy。這篇論文的貢獻，就是將這個策略「顯式化 (Explicit) 」並應用在非推理模型上。"
  anchor_type: 部落格推論
  importance: 14
  status: normal
```
