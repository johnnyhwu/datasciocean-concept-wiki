---
id: context-edit-cost-by-position
title: 改 context 的成本由位置決定：伺服器只能沿用開頭完全相同的那段快取，成本幾乎就是「要重算的 token 數加生成的 token 數」，編輯越靠前，要重算的越多
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: context-language-models
  article_title: "Context Language Models 解析：讓 agent 用 Bash 改自己的 context"
  url: https://datasciocean.com/paper-intro/context-language-models/
  sections:
  - context 爆了，誰來決定留什麼？CLM 讓模型自己改
  - 編輯 context 的成本：位置決定要重算多少
  - 編輯成本由位置決定
  - 結論：值得帶走的東西
  - 其餘實驗：補充證據與 CLM 的依賴
  first_appearance: true
parent: null
related:
  - clm-context-as-editable-file
  - success-gated-efficiency-advantage
  - prompt-repetition-free-lunch-latency
  - intermediate-results-out-of-context
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 改 context 的成本由位置決定：成本幾乎就是「要重算的 token 數加生成的 token 數」，編輯越靠前，要重算的越多
  source_quotes:
  - "記住這個結論就夠：成本幾乎就是「要重算的 token 數加生成的 token 數」，編輯越靠前，要重算的越多。"
  anchor_type: 部落格推論
  qualifiers:
  - text: 這是標準服務（prefix cache 重用）下的情況；論文另在服務端提出 SCR（Suffix Cache Reuse），改動中間內容之後仍然重用所有留下來的 token 的快取，減少重新 prefill
    source_quote: "順帶一提，圖 4 右半的 SCR（Suffix Cache Reuse）是論文在服務端提出的做法：改動中間內容之後，仍然重用所有留下來的 token 的快取，減少重新 prefill。"
  - text: 「幾乎」成立的原因是在論文附錄 C 的那個例子裡，每個 token 的固定處理成本佔了約 86% 的總計算量
    source_quote: "原因是在這個例子裡，每個 token 的固定處理成本（MLP 與各種投影，也就是模型每層裡和 context 長度無關的運算，約 \\( 48.70\\times10^{9} \\) FLOPs/token）佔了約 86% 的總計算量"
  - text: 論文註明附錄 C 那個例子的長度是為說明而選，不是實測
    source_quote: "論文註明這些長度是為說明而選，不是實測："
  - text: 這裡的成本是論文公式算出來的理論計算量，不是實測延遲或帳單
    source_quote: "論文通篇的「少 X% FLOPs」都是這個公式算出來的理論值，不是實測延遲或帳單。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: 這個問題出自 Context Language Models 這篇論文提出的 CLM：把模型當前的 context 鏡像成一個檔案，模型用 Bash 想改哪裡就改哪裡，改完立刻同步回下一輪真正餵給模型的 context。CLM 會改 context 中間的內容，這會讓推論伺服器的快取失效，所以光比 token 數不公平
  source_quotes:
  - "Context Language Models 這篇論文提出的做法叫 CLM：把模型當前的 context 鏡像成一個檔案，模型用 Bash 想改哪裡就改哪裡，改完立刻同步回它的 live context（下一輪真正餵給模型的那份 context）。"
  - "CLM 會改 context 中間的內容，這會讓推論伺服器的快取失效，所以光比 token 數不公平。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: mechanism
  text: 要看懂成本，先認識伺服器怎麼處理一份 prompt：prefill 是模型一次讀完輸入的 prompt，算出每個 token 的中間狀態（KV cache，鍵值快取）；decode 是模型一個一個生成新 token。prefix cache 重用是伺服器記住上一輪算過的 KV cache，新 prompt 若開頭一段完全相同，這段就直接沿用；從第一個不同的 token 開始，後面全部都要重算（re-prefill）
  source_quotes:
  - "prefill：模型一次讀完輸入的 prompt，算出每個 token 的中間狀態（KV cache，鍵值快取）。"
  - "要看懂它，先認識伺服器怎麼處理一份 prompt："
  - "decode：模型一個一個生成新 token。"
  - "prefix cache 重用：伺服器記住上一輪算過的 KV cache。新 prompt 若開頭一段完全相同，這段就直接沿用；從第一個不同的 token 開始，後面全部都要重算（re-prefill）。"
  anchor_type: 背景說明
  figures:
  - file: figures/context-language-models/figure4.png
    article: context-language-models
    src: figure4.png
    caption: 圖 4 — 標準服務與 Suffix Cache Reuse（SCR）的比較。左半示範為什麼改動中間內容會讓後面的快取失效。（來源：原始論文 Figure 4。）
    sha256: 51919ce81852e6d65b25d5d5e8aae7c269f0939fb5f199f567303b67daee40cc
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: blog 解釋這背後的原理（一般知識）：每個 token 的 KV 快取取決於它前面所有 token，所以伺服器只能沿用「開頭完全相同」的那一段，第一個不同的 token 之後全部重算
  source_quotes:
  - "原理（一般知識）：每個 token 的 KV 快取取決於它前面所有 token，所以伺服器只能沿用「開頭完全相同」的那一段，第一個不同的 token 之後全部重算。"
  anchor_type: 背景說明
  qualifiers:
  - text: 這是標準服務（prefix cache 重用）下的情況；論文另在服務端提出 SCR（Suffix Cache Reuse），改動中間內容之後仍然重用所有留下來的 token 的快取，減少重新 prefill
    source_quote: "順帶一提，圖 4 右半的 SCR（Suffix Cache Reuse）是論文在服務端提出的做法：改動中間內容之後，仍然重用所有留下來的 token 的快取，減少重新 prefill。"
  importance: 4
  status: normal
- id: c5
  role: anchor
  text: 自編例子：context 是 [A B C]。只在後面追加，A、B、C 全部沿用，只算新增的部分；把 B 改成 B'，只有 A 能沿用，B' 和 C 都要重算，即使 C 一個字都沒變
  source_quotes:
  - "自編例子（概念見下圖左半）：context 是 [A B C]。只在後面追加，A、B、C 全部沿用，只算新增的部分。把 B 改成 B'，只有 A 能沿用，B' 和 C 都要重算，即使 C 一個字都沒變。"
  anchor_type: 部落格舉例
  figures:
  - file: figures/context-language-models/figure4.png
    article: context-language-models
    src: figure4.png
    caption: 圖 4 — 標準服務與 Suffix Cache Reuse（SCR）的比較。左半示範為什麼改動中間內容會讓後面的快取失效。（來源：原始論文 Figure 4。）
    sha256: 51919ce81852e6d65b25d5d5e8aae7c269f0939fb5f199f567303b67daee40cc
  importance: 5
  status: normal
- id: c6
  role: mechanism
  text: 論文自訂了 prefix-reuse FLOPs，算「伺服器實際要做的計算量」（FLOPs 是浮點運算次數）。公式只算兩件事：沒對上快取的那段（從第一個不同 token 起到結尾）要重新 prefill 的計算量，加上模型生成新 token 的 decode 計算量
  source_quotes:
  - "論文自訂了 prefix-reuse FLOPs，算「伺服器實際要做的計算量」（FLOPs 是浮點運算次數，衡量計算量）。"
  - "論文的公式只算兩件事：沒對上快取的那段（從第一個不同 token 起到結尾）要重新 prefill 的計算量，加上模型生成新 token 的 decode 計算量。"
  - '\mathrm{FLOPs}_{\text{prefix-reuse}} = \mathrm{FLOPs}_{\text{prefill}}(\text{unmatched suffix}) + \mathrm{FLOPs}_{\text{decode}}(\text{generated tokens})'
  anchor_type: 設計參數
  importance: 6
  status: normal
- id: c7
  role: anchor
  text: 論文附錄 C 用 Qwen3.6-27B 做的數字例子：只追加時可沿用 18,000 tokens 的前綴，該輪計算量 1.41×10^14 FLOPs；改中間時可沿用 10,000 tokens，5.74×10^14 FLOPs；改開頭（等於沒有快取）可沿用 0，10.81×10^14 FLOPs，是只追加的 7.7 倍
  source_quotes:
  - "論文附錄 C 用 Qwen3.6-27B 做了一個數字例子（下圖）。"
  - "只追加 | 18,000 tokens | \\( 1.41\\times10^{14} \\) FLOPs"
  - "改中間 | 10,000 tokens | \\( 5.74\\times10^{14} \\) FLOPs"
  - "改開頭（等於沒有快取） | 0 | \\( 10.81\\times10^{14} \\) FLOPs（追加的 7.7 倍）"
  anchor_type: 數學推導
  comparison_target: 同一輪只追加、改中間、改開頭三種情況互相比較；7.7 倍是改開頭對只追加
  qualifiers:
  - text: 論文註明這些長度是為說明而選，不是實測
    source_quote: "論文註明這些長度是為說明而選，不是實測："
  - text: 這些是論文公式算出來的理論計算量，不是實測延遲或帳單
    source_quote: "論文通篇的「少 X% FLOPs」都是這個公式算出來的理論值，不是實測延遲或帳單。"
  figures:
  - file: figures/context-language-models/figure14.png
    article: context-language-models
    src: figure14.png
    caption: 圖 5 — 在假設的長度（輸入 20,000、生成 500 tokens）下，三種可重用前綴長度對應的單輪計算量。（來源：原始論文 Figure 14。）
    sha256: 603b0f8813509117a5075149634889355c8a43ce5f8a227a8a9db9d27efb30c9
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: 成本幾乎只看 token 數的原因：在這個例子裡，每個 token 的固定處理成本（MLP 與各種投影，也就是模型每層裡和 context 長度無關的運算，約 48.70×10^9 FLOPs/token）佔了約 86% 的總計算量，attention 這種隨 context 長度增長的成本只佔約 14%；86% 是 blog 由論文給的數字驗算
  source_quotes:
  - "原因是在這個例子裡，每個 token 的固定處理成本（MLP 與各種投影，也就是模型每層裡和 context 長度無關的運算，約 \\( 48.70\\times10^{9} \\) FLOPs/token）佔了約 86% 的總計算量（我由論文給的數字驗算），attention 這種隨 context 長度增長的成本只佔約 14%。"
  anchor_type: 部落格考證
  comparison_target: 同一個例子的總計算量（固定處理成本約 86% 對 attention 約 14%）
  qualifiers:
  - text: 這是附錄 C 那個為說明而選、不是實測的例子
    source_quote: "論文註明這些長度是為說明而選，不是實測："
  importance: 8
  status: normal
- id: c9
  role: anchor
  text: 直覺例子（自編例子，假設成本與重算 token 數成正比）：同樣是改 20,000 tokens 的 context 裡的一處，改在 18,000 個 token 的位置附近，只需重算約 2,000 個；改在 2,000 個 token 的位置附近，要重算約 18,000 個，差 9 倍
  source_quotes:
  - "直覺例子（自編例子，假設成本與重算 token 數成正比）：同樣是改 20,000 tokens 的 context 裡的一處。改在 18,000 個 token 的位置附近，只需重算約 2,000 個；改在 2,000 個 token 的位置附近，要重算約 18,000 個，差 9 倍。"
  anchor_type: 部落格舉例
  comparison_target: 改在 18,000 個 token 附近對改在 2,000 個 token 附近
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: blog 由上面的算式推出可遷移的設計規則：context 由前到後，依變動頻率排列，穩定的放前面（system prompt、長期有效的筆記），較少變動的居中（已定案的摘要），常變動的放最後（最近幾輪）。blog 認為這個規則對任何會改歷史的 harness 都成立，不限於 CLM
  source_quotes:
  - "可遷移的設計規則（推論，由上面的算式推出）：context 由前到後，依變動頻率排列，穩定的放前面（system prompt、長期有效的筆記），較少變動的居中（已定案的摘要），常變動的放最後（最近幾輪）。"
  - "這個規則對任何會改歷史的 harness 都成立，不限於 CLM"
  anchor_type: 部落格推論
  qualifiers:
  - text: 這是標準服務（prefix cache 重用）下的情況；論文另在服務端提出 SCR（Suffix Cache Reuse），改動中間內容之後仍然重用所有留下來的 token 的快取，減少重新 prefill
    source_quote: "順帶一提，圖 4 右半的 SCR（Suffix Cache Reuse）是論文在服務端提出的做法：改動中間內容之後，仍然重用所有留下來的 token 的快取，減少重新 prefill。"
  - text: 這裡的成本是理論 FLOPs，有前述的限制
    source_quote: "成本是理論 FLOPs，限制見前面「編輯 context 的成本」一章。"
  importance: 10
  status: normal
- id: c11
  role: mechanism
  text: blog 在排列規則之後列出兩點：要壓縮就集中做一次，別在中間反覆小改；同樣是刪 8,000 tokens，刪在尾端和刪在開頭，成本差好幾倍
  source_quotes:
  - "要壓縮就集中做一次，別在中間反覆小改。"
  - "同樣是刪 8,000 tokens，刪在尾端和刪在開頭，成本差好幾倍。"
  anchor_type: 部落格推論
  comparison_target: 同樣刪 8,000 tokens，刪在尾端對刪在開頭
  qualifiers:
  - text: 這是標準服務（prefix cache 重用）下的情況；論文另在服務端提出 SCR（Suffix Cache Reuse），改動中間內容之後仍然重用所有留下來的 token 的快取，減少重新 prefill
    source_quote: "順帶一提，圖 4 右半的 SCR（Suffix Cache Reuse）是論文在服務端提出的做法：改動中間內容之後，仍然重用所有留下來的 token 的快取，減少重新 prefill。"
  - text: 這裡的成本是理論 FLOPs，有前述的限制
    source_quote: "成本是理論 FLOPs，限制見前面「編輯 context 的成本」一章。"
  importance: 11
  status: normal
- id: c12
  role: evaluation
  text: 這個公式把 CLM 編輯造成的重算也算進去，對 CLM 並不偏袒；但它把一個 prefill token 和一個 decode token 當成成本相同，實務上 decode 是逐字生成，通常慢得多（一般知識，不是論文內容），所以對延遲的預測會有偏差
  source_quotes:
  - "它把 CLM 編輯造成的重算也算進去，對 CLM 並不偏袒；但它把一個 prefill token 和一個 decode token 當成成本相同，實務上 decode 是逐字生成，通常慢得多（一般知識，不是論文內容），所以對延遲的預測會有偏差。"
  anchor_type: 部落格判斷
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: blog 給自己做 agent 的建議：改 context 盡量改在後面
  source_quotes:
  - "自己做 agent 時：改 context 盡量改在後面（論文附錄的例子裡，改開頭的成本是只追加的 7.7 倍）"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 這是標準服務（prefix cache 重用）下的情況；論文另在服務端提出 SCR（Suffix Cache Reuse），改動中間內容之後仍然重用所有留下來的 token 的快取，減少重新 prefill
    source_quote: "順帶一提，圖 4 右半的 SCR（Suffix Cache Reuse）是論文在服務端提出的做法：改動中間內容之後，仍然重用所有留下來的 token 的快取，減少重新 prefill。"
  - text: 依據是論文附錄的例子（改開頭的成本是只追加的 7.7 倍），那個例子的長度是為說明而選，不是實測
    source_quote: "論文註明這些長度是為說明而選，不是實測："
  importance: 13
  status: normal
```
