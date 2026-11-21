---
id: success-gated-efficiency-advantage
title: 想同時優化「答對」和「便宜」時，次要目標只能在達標的集合內比較：CLM 的 RL 只在答對的軌跡之間依成本加減分，否則最便宜的做法就是直接放棄
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: context-language-models
  article_title: "Context Language Models 解析：讓 agent 用 Bash 改自己的 context"
  url: https://datasciocean.com/paper-intro/context-language-models/
  sections:
  - context 爆了，誰來決定留什麼？CLM 讓模型自己改
  - 改權重：用 RL 學會怎麼編輯 context
  - GRPO 沒變，變的是兩處
  - 效率獎勵只在答對的軌跡之間比
  - 實驗結果：準確率打平，成本低約四成
  - 整體評價：概念值得試，證據只夠說明有潛力
  - 結論：值得帶走的東西
  - 次要目標只能在達標的集合內比較
  - credit assignment：總分怎麼分給每個 step
  - 零樣本、skill 演化、RL：三組互不重疊的證據
  - 編輯 context 的成本：位置決定要重算多少
  - 要注意：「何時編輯」其實有 harness 在幫忙
  - 其餘實驗：補充證據與 CLM 的依賴
  first_appearance: true
parent: null
related:
  - clm-context-as-editable-file
  - clm-results-tight-budget-not-across-the-board
  - context-edit-cost-by-position
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 想同時優化「答對」和「便宜」時，如果對所有軌跡都獎勵便宜，最便宜的做法是什麼都不做、直接放棄；做法是先分對錯，再只在答對的軌跡之間比成本。CLM 的 RL 就只在「已經答對」的軌跡之間，依成本（prefix-reuse FLOPs）排序加減分，這種設計叫 success-gated
  source_quotes:
  - "想同時優化「答對」和「便宜」時，如果對所有軌跡都獎勵便宜，最便宜的做法是什麼都不做、直接放棄，這就是 reward hacking。做法是先分對錯，再只在答對的軌跡之間比成本。"
  - "所以論文只在「已經答對」的軌跡之間，依成本（prefix-reuse FLOPs）排序加減分，這種設計叫 success-gated：只有答對的軌跡才參與效率比較。"
  anchor_type: 設計參數
  importance: 1
  status: normal
- id: c2
  role: context
  text: 這是 Context Language Models 論文的 RL 訓練設計。論文提出的 CLM 把模型當前的 context 鏡像成一個檔案，模型用 Bash 想改哪裡就改哪裡；RL 改模型權重，讓模型從「最後有沒有答對」學會怎麼編輯 context
  source_quotes:
  - "Context Language Models 這篇論文提出的做法叫 CLM：把模型當前的 context 鏡像成一個檔案，模型用 Bash 想改哪裡就改哪裡"
  - "前一章改的是 context 裡的文字，這一章改模型權重，讓模型從「最後有沒有答對」學會怎麼編輯 context。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: 成本用的是論文自訂的 prefix-reuse FLOPs，算「伺服器實際要做的計算量」：沒對上快取的那段要重新 prefill 的計算量，加上模型生成新 token 的 decode 計算量；它是公式算出來的理論值，不是實測延遲或帳單
  source_quotes:
  - "論文自訂了 prefix-reuse FLOPs，算「伺服器實際要做的計算量」"
  - "論文的公式只算兩件事：沒對上快取的那段（從第一個不同 token 起到結尾）要重新 prefill 的計算量，加上模型生成新 token 的 decode 計算量。"
  - "論文通篇的「少 X% FLOPs」都是這個公式算出來的理論值，不是實測延遲或帳單。"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c4
  role: context
  text: 訓練用的 GRPO（Group Relative Policy Optimization，來自 DeepSeekMath）是一種 RL 演算法：同一題先抽一組完整軌跡，每條軌跡的 advantage（優勢）等於它的得分相對於組內平均的好壞。CLM 的訓練沿用這套，改動只有兩處
  source_quotes:
  - "GRPO（Group Relative Policy Optimization） 是一種 RL 演算法（來自 DeepSeekMath，Shao et al., 2024）。同一題先抽一組（group）完整軌跡，每條軌跡的 advantage（優勢）等於它的得分相對於組內平均的好壞"
  - "CLM 的訓練沿用這套，改動只有兩處："
  anchor_type: 背景說明
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 第一處是輸入的準備：CLM 會編輯 context，最終的 context 已經不是早期某一步當時看到的內容，所以每次模型呼叫連同它當時真正看到的 context 各自算一次（stepwise GRPO），整條軌跡的 advantage 原封不動分給底下每一次呼叫。這不是論文新發明，延續 ReSum 與 Sculptor；第二處的效率獎勵才是論文自己的新設計
  source_quotes:
  - "輸入的準備：CLM 會編輯 context，所以最終的 context 已經不是早期某一步當時看到的內容。論文的做法是每次模型呼叫連同它當時真正看到的 context，各自算一次（stepwise GRPO），整條軌跡的 advantage 原封不動分給底下每一次呼叫。這個做法不是論文新發明，附錄 A 說明延續 ReSum 與 Sculptor。"
  - "advantage 多了一項效率獎勵（下一小節），這才是論文自己的新設計。"
  anchor_type: 設計參數
  importance: 5
  status: normal
- id: c6
  role: mechanism
  text: 為什麼要 success-gated：結果獎勵只分對錯，對「編輯得好不好」是弱監督，答對的軌跡裡可能有很笨的編輯；直接獎勵「編輯次數」或「刪掉的 token 量」又會被鑽漏洞，模型可能做一堆沒必要的編輯、把重要資訊也刪掉，或破壞 prefix 重用，這叫 reward hacking
  source_quotes:
  - "結果獎勵只分對錯，對「編輯得好不好」是弱監督：答對的軌跡裡可能有很笨的編輯，答錯的裡也可能有好的編輯。直接獎勵「編輯次數」或「刪掉的 token 量」又會被鑽漏洞，模型可能做一堆沒必要的編輯、把重要資訊也刪掉，或破壞 prefix 重用，這叫 reward hacking。"
  anchor_type: 部落格推論
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: 效率 advantage 的算法（論文 Eq. 6）：答對的軌跡裡，比平均便宜的加分、比平均貴的扣分，結果限制在 −1 到 +1；答錯的完全不參與。最後的 advantage 是標準 GRPO 的結果 advantage 加上權重乘以效率 advantage，權重論文 Appendix E 給 0.25。答對的軌跡少於 2 條時，整組的效率 advantage 都設為 0
  source_quotes:
  - "白話：答對的軌跡裡，比平均便宜的加分、比平均貴的扣分；答錯的完全不參與。寫成式子是論文 Eq. 6："
  - "\\( \\mathrm{clip}(\\cdot, -1, 1) \\)：把結果限制在 −1 到 +1。"
  - "A_i = A_i^{\\mathrm{out}} + w_{\\mathrm{eff}}\\, A_i^{\\mathrm{eff}}"
  - "\\( A_i^{\\mathrm{out}} \\)：標準 GRPO 的結果 advantage。\\( w_{\\mathrm{eff}} \\)：權重，論文 Appendix E 給 0.25。"
  - "答對的軌跡少於 2 條時，整組的 \\( A^{\\mathrm{eff}} \\) 都設為 0。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 7
  status: normal
- id: c8
  role: anchor
  text: 自編例子：同一題抽 4 條軌跡，成本分別是 2.0（對）、1.0（對）、0.5（錯）、3.0（對）。答對的成本平均 2.0，成本 1.0 的那條效率 advantage 是 +0.5，成本 3.0 的是 −0.5；成本 0.5 的那條成本最低卻答錯，拿不到效率加分。效率項只是排序用的小項，0.25 ×（±0.5）= ±0.125，遠小於對錯造成的差距
  source_quotes:
  - "用四條軌跡舉例（自編例子），成本分別是 2.0（對）、1.0（對）、0.5（錯）、3.0（對）："
  - "算法：答對的成本平均 \\( \\bar{c} = (2+1+3)/3 = 2.0 \\)，\\( \\tau_2 \\) 是 \\( (2-1)/2 = +0.5 \\)，\\( \\tau_4 \\) 是 \\( (2-3)/2 = -0.5 \\)。"
  - "\\( \\tau_3 \\) 成本最低卻答錯，所以拿不到效率加分，這就是 success-gated 的作用；效率項只是排序用的小項，\\( 0.25 \\times (\\pm 0.5) = \\pm 0.125 \\)，遠小於對錯造成的差距。"
  anchor_type: 部落格舉例
  comparison_target: 同組答對軌跡的平均成本（2.0）；±0.125 對比對錯造成的 advantage 差距
  importance: 8
  status: normal
- id: c9
  role: anchor
  text: 同一組例子若對全部軌跡比成本（平均成本 1.625），答錯的那條拿到約 +0.69，失敗反而被獎勵；只在答對的軌跡內比，它拿 0，不參與
  source_quotes:
  - "對全部比成本，平均成本 1.625 | \\( (1.625 - 0.5) / 1.625 \\approx +0.69 \\)，失敗反而被獎勵"
  - "只在答對的軌跡內比 | 0，不參與"
  anchor_type: 部落格舉例
  comparison_target: 對全部軌跡比成本對只在答對軌跡內比
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: blog 由此推出的可遷移規則：任何「主目標加次要目標」的優化，次要目標都要設門檻或排序，不能直接加總，例如準確率加延遲、品質加成本
  source_quotes:
  - "可遷移的規則（一般知識加我的推論）："
  - "任何「主目標加次要目標」的優化，次要目標都要設門檻或排序，不能直接加總。例如準確率加延遲、品質加成本。"
  anchor_type: 部落格推論
  importance: 10
  status: normal
- id: c11
  role: evaluation
  text: blog 推論的副作用：答對的軌跡少於 2 條時，這項整個歸零；題目很難、成功率低時，效率訊號幾乎不存在
  source_quotes:
  - "副作用（推論）：答對的軌跡少於 2 條時，這項整個歸零。題目很難、成功率低時，效率訊號幾乎不存在。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 11
  status: normal
- id: c12
  role: evaluation
  text: 效率分數怎麼落到每個 step 上（credit assignment，功勞分配），論文沒講清楚：論文明講把結果 advantage 分給軌跡底下每一次模型呼叫，Appendix E 又說效率 advantage 套用在「context 管理相關的 token」上。blog 推論，若合計值直接分給整條軌跡的所有 token，模型分不出便宜是因為編輯得好還是少搜了幾輪，可能靠「少做事、早收工」降成本，而不是學會更好的 context 管理
  source_quotes:
  - "先說答案：論文明講的部分，是把結果 advantage 直接分給軌跡底下每一次模型呼叫；效率那一項到底有沒有一起分、怎麼分，論文沒講清楚。"
  - "論文 Appendix E 又說效率 advantage 是套用在「context 管理相關的 token」上。"
  - "整條軌跡的所有 token | 只有編輯 token"
  - "不能：模型分不出便宜是因為編輯得好，還是少搜了幾輪 | 比較能"
  - "模型可能靠「少做事、早收工」降成本，而不是學會更好的 context 管理"
  anchor_type: 部落格推論
  qualifiers:
  - text: 兩種讀法各自在訓練什麼是 blog 的推論；論文文字無法判定是哪一種
    source_quote: "論文文字無法判定是哪一種"
  importance: 12
  status: normal
- id: c13
  role: anchor
  text: RL 實驗設定：Qwen3.5-9B，用 OpenResearcher 資料集的 3,040 題訓練 70 步，在 BrowseComp-Plus（在固定語料上搜尋並回答難題的深度研究基準）全部 830 題評估。CLM 的 context 預算 28K，另加效率 advantage（權重 0.25）以及工具呼叫失敗與格式錯誤的懲罰；對照組 Summary 累積到 28,672 tokens 時把整段歷史換成一則摘要，Appendix E 寫它只用任務獎勵訓練
  source_quotes:
  - "模型與資料：Qwen3.5-9B，用 OpenResearcher 資料集的 3,040 題訓練 70 步，在 BrowseComp-Plus 全部 830 題評估。"
  - "BrowseComp-Plus（一個在固定語料上搜尋並回答難題的深度研究基準，簡稱 BCP）"
  - "CLM：context 預算 28K（保留 2,048 tokens），最多 80 輪，編輯回合不計入；另加效率 advantage（權重 0.25，論文 Appendix E 說套用在 context 管理相關的 token 上）以及工具呼叫失敗與格式錯誤的懲罰。"
  - "對照組 Summary：agent 照常累積 context，累積到 28,672 tokens 時，除了 system prompt 和任務訊息之外，整段歷史被換成一則摘要（摘要用 Codex 的摘要 prompt），最多跑 100 輪。"
  - "Appendix E 寫它只用任務獎勵訓練。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 13
  status: normal
- id: c14
  role: evidence
  text: 訓練後準確率實質上打平：Summary 從 34.7% 到 42.1%，CLM 從 28.8% 到 42.5%；CLM 每題成本從 1.52 到 1.34 PFLOPs，Summary 從 4.01 到 2.19，訓練後 CLM 每題成本低約 38.8%
  source_quotes:
  - "Summary（對照組） | 34.7 到 42.1（+7.4） | 4.01 到 2.19"
  - "CLM | 28.8 到 42.5（+13.7） | 1.52 到 1.34"
  - "訓練後，準確率實質上打平（42.5 對 42.1），CLM 每題成本低約 38.8%（\\( (2.19 - 1.34) / 2.19 \\)，與論文引言一致）。"
  anchor_type: 實驗結果
  comparison_target: 同一套 RL 訓練前後的 Summary 對照組（訓練後 42.5 對 42.1；每題成本 1.34 對 2.19）
  qualifiers:
  - text: CLM 另加效率獎勵與格式懲罰、Summary 只用任務獎勵；表上沒標每列是否含效率獎勵，所以 1.34 對 2.19 可能不是同條件比較
    source_quote: "論文引言說 Summary 用「同樣的訓練配方」，但 Appendix E 寫 CLM 另加效率獎勵與格式懲罰、Summary 只用任務獎勵；上面的表沒標每列是否含效率獎勵，所以 1.34 對 2.19 可能不是同條件比較。"
  - text: 成本是 prefix-reuse FLOPs 的理論值，不是實測延遲或帳單
    source_quote: "論文通篇的「少 X% FLOPs」都是這個公式算出來的理論值，不是實測延遲或帳單。"
  - text: RL checkpoint 由保留的驗證集挑選
    source_quote: "表 2 — Qwen3.5-9B 在 BrowseComp-Plus 上的 RL 前後結果，RL checkpoint 由保留的驗證集挑選。（來源：原始論文 Table 2。）"
    source: figure_caption
  figures:
  - file: figures/context-language-models/table2.png
    article: context-language-models
    src: table2.png
    caption: 表 2 — Qwen3.5-9B 在 BrowseComp-Plus 上的 RL 前後結果，RL checkpoint 由保留的驗證集挑選。（來源：原始論文 Table 2。）
    sha256: c5b4057ed36c76a6ca94b8d214b0dd7f505c816bc6d26bb28287b77df82cd18b
  importance: 14
  status: normal
- id: c15
  role: evidence
  text: 訓練前，CLM 比 Summary 低約 6 點；論文歸因於小模型的 context 管理能力不足，Appendix F 也說 Qwen3.5-9B 很少編輯 context（在 TerminalBench 2.1 這組終端機任務上平均 1.4 次，一半的任務完全不編輯）
  source_quotes:
  - "訓練前，CLM 比 Summary 低約 6 點。論文歸因於小模型的 context 管理能力不足；論文 Appendix F 也說 Qwen3.5-9B 很少編輯 context"
  - "（在 TerminalBench 2.1 這組終端機任務上平均 1.4 次，一半的任務完全不編輯）"
  anchor_type: 原作者解讀
  comparison_target: 訓練前的 Summary 對照組（28.8 對 34.7）
  qualifiers:
  - text: 這是 RL 評估的設定（28K、最多 80 輪）；論文 Appendix F 的零樣本實驗（32K、100 輪）裡，9B 在 BCP 上 CLM 是 39.9%，高於 Summary 的 37.7%，兩者設定不同是 blog 的推論
    source_quote: "論文 Appendix F 說 9B 在 BCP 上零樣本 CLM 是 39.9%，高於 Summary 的 37.7%；但 RL 章的表 2 說 9B 訓練前 CLM 是 28.8%，低於 Summary 的 34.7%。兩者設定不同（零樣本實驗：32K、100 輪；RL 評估：28K、最多 80 輪）。這是我的推論，論文沒點明這個差別。"
  importance: 15
  status: normal
- id: c16
  role: evaluation
  text: 論文摘要的「提升 47.6%」是相對值（42.5 除以 28.8），起點很低；絕對提升是 13.7 點，和訓練後的 Summary 比只贏 0.4 點，真正的差別在成本
  source_quotes:
  - "論文摘要的「提升 47.6%」是相對值（42.5 除以 28.8），起點很低；絕對提升是 13.7 點。和訓練後的 Summary 比只贏 0.4 點，真正的差別在成本。"
  anchor_type: 部落格考證
  comparison_target: CLM 自己訓練前的 28.8%（47.6% 與 13.7 點）；訓練後的 Summary 42.1%（0.4 點）
  qualifiers:
  - text: CLM 另加效率獎勵與格式懲罰、Summary 只用任務獎勵，成本差距可能不是同條件比較
    source_quote: "論文引言說 Summary 用「同樣的訓練配方」，但 Appendix E 寫 CLM 另加效率獎勵與格式懲罰、Summary 只用任務獎勵；上面的表沒標每列是否含效率獎勵，所以 1.34 對 2.19 可能不是同條件比較。"
  - text: 成本是論文公式算出來的理論 FLOPs，不是實測延遲或帳單
    source_quote: "論文通篇的「少 X% FLOPs」都是這個公式算出來的理論值，不是實測延遲或帳單。"
  importance: 16
  status: normal
- id: c17
  role: evaluation
  text: Summary 對照組也同樣被訓練變強（34.7% 到 42.1%），所以 RL 證明的是「CLM 可以被訓練」，不是「CLM 比對手更吃訓練的紅利」；「訓練或演化後的 CLM，在 EdgeBench 這類任務上更強」，論文沒有這組實驗
  source_quotes:
  - "RL：9B 從 28.8% 升到 42.5%，但 Summary 對照組也同樣被訓練變強（34.7% 到 42.1%）。所以證明的是「CLM 可以被訓練」，不是「CLM 比對手更吃訓練的紅利」"
  - "兩者都沒有在長時間任務上驗證：「訓練或演化後的 CLM，在 EdgeBench 這類任務上更強」，論文沒有這組實驗。"
  anchor_type: 部落格判斷
  comparison_target: Summary 對照組同樣的訓練前後變化
  qualifiers:
  - text: 訓練後只是追平，差別在成本，而且兩邊的獎勵設計不同
    source_quote: "訓練後只是追平，差別在成本，而且兩邊的獎勵設計不同。"
  importance: 17
  status: normal
- id: c18
  role: evaluation
  text: blog 認為 success-gated 效率 advantage 是論文唯一真正算新的部分，但只能算「小」貢獻：權重只有 0.25；對應的做法在別的領域早有類似設計（附錄 A 提到只在答對的回答上罰長度的 Arora & Zanette，以及 DDCA），差別只是這篇用 FLOPs 當成本；而且這一項怎麼分給 token，論文沒講清楚
  source_quotes:
  - "真正算新的只有 success-gated 效率 advantage"
  - "它只能算「小」貢獻，理由有三個：權重只有 0.25；對應的做法在別的領域早有類似設計（附錄 A 提到只在答對的回答上罰長度的 Arora & Zanette，以及 DDCA），差別只是這篇用 FLOPs 當成本；而且這一項怎麼分給 token，論文沒講清楚。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 18
  status: normal
```
