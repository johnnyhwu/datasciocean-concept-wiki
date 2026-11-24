---
id: taste-bench-frontier-results
title: 14 個前沿模型在 Taste-Bench 上最高只有 59.7%（隨機基準 25%），沒有模型接近解完；而且決定性證據出現得越晚，模型越答不準
type_hint: 發現
context_type: bound_to_source
sources:
- article: tasteful-agent
  article_title: "The Tasteful Agent 解析：用 agent 跑過的軌跡，量測並訓練 AI 的決策品味"
  url: https://datasciocean.com/paper-intro/tasteful-agent/
  sections:
  - agent 的中途決策沒人量過，這篇論文用跑過的軌跡免費出題
  - 同任務、同前綴，結果的差異才能歸給判斷
  - 一道題長什麼樣子：標籤與答對率
  - 兩種挖岔路口的方法：parallel 與 detour
  - 從 4,657 個候選篩到 502 題
  - 評分方式：順序對調考兩次，隨機基準是 25%
  - 總成績：最好 59.7%，繞路工程題最難
  - 決定性證據越晚出現，越答不準
  - 值得肯定的，以及研究與工程上的價值
  - 一句話總結
  - parallel 與 detour 也決定了標籤怎麼來
  first_appearance: true
parent: null
related:
  - taste-fork-outcome-labels
  - pairwise-eval-swap-order-twice
  - taste-advice-deployment-gap
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 14 個前沿模型在 Taste-Bench 上最高只有 59.7%（隨機基準 25%），沒有模型接近解完；而且決定性證據出現得越晚，模型越答不準
  source_quotes:
  - "14 個前沿模型最高只有 59.7%，而且決定性證據出現得越晚，模型越答不準。"
  - "隨機基準 25%"
  - "沒有模型接近解完"
  anchor_type: 實驗結果
  comparison_target: 隨機猜的基準 25%
  qualifiers:
  - text: 59.7% 是 Average：工程 56.9%、研究 62.5% 取 1:1 平均；同一模型用 502 題直接合併算的嚴格準確率是 58.2%
    source_quote: "直接合併的嚴格準確率是 \\( 292 / 502 = 58.2\\% \\)。開頭的 59.7% 是 Average：工程 56.9%、研究 62.5%，取 1:1 平均得"
  importance: 1
  status: normal
- id: c2
  role: context
  text: The Tasteful Agent 這篇論文把「做出好的長程決策的能力」稱為 taste（品味），並造出 502 題的評測集 Taste-Bench。每一題對應 agent 軌跡中的一個決策岔路口（論文稱為 decision fork），題目是任務、前綴（岔路口之前的前文）、兩個候選，答案是事後結果比較好的那一邊
  source_quotes:
  - "The Tasteful Agent 這篇論文"
  - "把「做出好的長程決策的能力」稱為 taste（品味）。"
  - "用這個方法，論文造出一個 502 題的評測集 Taste-Bench。"
  - "一道題對應一個岔路口"
  - "論文把這個分歧點稱為 decision fork（決策岔路口）。"
  - "到這裡，一道題的樣子就清楚了：任務、前綴、兩個候選，答案是事後結果比較好的那一邊。"
  - "也就是同一個任務、同一段前文（這段前文稱為前綴）"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 2
  status: normal
- id: c3
  role: context
  text: 岔路口有兩個來源：parallel（平行軌跡）是兩次獨立嘗試走向不同方向；detour（繞路軌跡）是同一次嘗試裡 agent 走錯後自己改正。502 題分成四格：平行工程 124、繞路工程 266、平行研究 48、繞路研究 64
  source_quotes:
  - "岔路口有兩個來源：兩次獨立嘗試走向不同方向，稱為 parallel（平行軌跡）；或是同一次嘗試裡 agent 走錯後自己改正，稱為 detour（繞路軌跡）。"
  - "最後通過 undecidable 過濾的剩 502 題，分成四格："
  - "| 工程 | 124 | 266 | 390 |"
  - "| 研究 | 48 | 64 | 112 |"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 3
  status: normal
- id: c4
  role: context
  text: 計分方式：每一題都考兩次、把 A、B 的順序對調，兩次都答對才算對，無法解析出答案的回應算錯；在這個計分下，每次各 1/2 機率亂猜的隨機基準線是 25%，永遠選同一個位置是 0%
  source_quotes:
  - "每一題都考兩次、把 A、B 的順序對調，兩次都答對才算對。"
  - "兩次都答對，這題才算對。無法解析出答案的回應算錯。"
  - "| 每次各 1/2 的機率亂猜 | \\( \\frac{1}{2} \\times \\frac{1}{2} = 25\\% \\) |"
  - "| 永遠選同一個位置 | 0%（兩次中必有一次錯） |"
  - "所以這個指標的隨機基準線是 25%，不是 50%。"
  - "這個設計讓分數的基準線跟直覺不同："
  anchor_type: 數學推導
  comparison_target: 跟直覺不同：隨機基準線是 25%，不是 50%
  importance: 2
  status: normal
- id: c5
  role: context
  text: 標題的 59.7% 是 Average：研究類與工程類各自算嚴格準確率後取 1:1 平均（研究只有 112 題、工程有 390 題，兩個領域各占一半權重）。以 GPT-5.6 Sol 驗算：502 題直接合併的嚴格準確率是 292/502 = 58.2%；工程 56.9%、研究 62.5%，取 1:1 平均得 59.7%
  source_quotes:
  - "Average： 研究類與工程類各自算嚴格準確率後，取 1:1 平均。研究只有 112 題、工程有 390 題，但兩個領域各占一半權重，所以 Average 和用 502 題直接合併算出的數字不同。"
  - "用 GPT-5.6 Sol 驗算（見表 3）"
  - "直接合併的嚴格準確率是 \\( 292 / 502 = 58.2\\% \\)。開頭的 59.7% 是 Average：工程 56.9%、研究 62.5%，取 1:1 平均得 \\( (56.9 + 62.5) / 2 = 59.7\\% \\)。"
  anchor_type: 部落格考證
  comparison_target: 同一模型 502 題直接合併的嚴格準確率 58.2%
  figures:
  - file: figures/tasteful-agent/table4.png
    article: tasteful-agent
    src: table4.png
    caption: 表 3 — 14 個模型的完整結果。P 與 D 代表平行與繞路，Eng 與 Res 代表工程與研究；Unparsed 是 1,004 次作答中無法解析出答案的次數。（來源：原始論文 Table 4。）
    sha256: 6d4876dedbf2cbbdcdb278efc8e06c54d72f5d2d977e9b64768dc09036e9c829
  importance: 3
  status: normal
- id: c6
  role: anchor
  text: 14 個模型的準確率（Average）：最好的 GPT-5.6 Sol 59.7%，其次 GPT-5.5 59.5%、Claude Opus 5 55.5%；隨機基準 25%，沒有模型接近解完
  source_quotes:
  - "| 14 個模型的準確率（圖 4、表 3） | 現有模型的品味有限 | 最好的 GPT-5.6 Sol 59.7%，其次 GPT-5.5 59.5%、Claude Opus 5 55.5%；隨機基準 25% | 沒有模型接近解完 |"
  anchor_type: 實驗結果
  comparison_target: 隨機基準 25%
  qualifiers:
  - text: 排名後段的 Grok 4.20 Reasoning、GPT-5.4 Mini、GPT-5.4 Nano 分別有 459、112、93 次（共 1,004 次）作答無法解析而被計為答錯，分數混入了格式遵循的因素
    source_quote: "排名後段的 Grok 4.20 Reasoning、GPT-5.4 Mini、GPT-5.4 Nano 分別有 459、112、93 次（共 1,004 次）作答無法解析而被計為答錯，分數混入了格式遵循的因素。"
  - text: 59.7% 是 Average：工程 56.9%、研究 62.5% 取 1:1 平均；同一模型用 502 題直接合併算的嚴格準確率是 58.2%
    source_quote: "直接合併的嚴格準確率是 \\( 292 / 502 = 58.2\\% \\)。開頭的 59.7% 是 Average：工程 56.9%、研究 62.5%，取 1:1 平均得"
  figures:
  - file: figures/tasteful-agent/table4.png
    article: tasteful-agent
    src: table4.png
    caption: 表 3 — 14 個模型的完整結果。P 與 D 代表平行與繞路，Eng 與 Res 代表工程與研究；Unparsed 是 1,004 次作答中無法解析出答案的次數。（來源：原始論文 Table 4。）
    sha256: 6d4876dedbf2cbbdcdb278efc8e06c54d72f5d2d977e9b64768dc09036e9c829
  importance: 2
  status: normal
- id: c7
  role: anchor
  text: 哪一類題最難：14 個模型平均，平行工程 58.1%、平行研究 50.9%、繞路研究 50.8%、繞路工程 35.9%；構造（parallel／detour）的差距大於領域（工程／研究）的差距，繞路工程題最難
  source_quotes:
  - "| 構造與領域的差異 | 哪一類題最難 | 14 個模型平均：平行工程 58.1%、平行研究 50.9%、繞路研究 50.8%、繞路工程 35.9% | 構造（parallel／detour）的差距大於領域（工程／研究）的差距；繞路工程題最難 |"
  anchor_type: 實驗結果
  comparison_target: 其他三格題型的 14 個模型平均準確率
  qualifiers:
  - text: 排名後段的 Grok 4.20 Reasoning、GPT-5.4 Mini、GPT-5.4 Nano 分別有 459、112、93 次（共 1,004 次）作答無法解析而被計為答錯，分數混入了格式遵循的因素
    source_quote: "排名後段的 Grok 4.20 Reasoning、GPT-5.4 Mini、GPT-5.4 Nano 分別有 459、112、93 次（共 1,004 次）作答無法解析而被計為答錯，分數混入了格式遵循的因素。"
  figures:
  - file: figures/tasteful-agent/table4.png
    article: tasteful-agent
    src: table4.png
    caption: 表 3 — 14 個模型的完整結果。P 與 D 代表平行與繞路，Eng 與 Res 代表工程與研究；Unparsed 是 1,004 次作答中無法解析出答案的次數。（來源：原始論文 Table 4。）
    sha256: 6d4876dedbf2cbbdcdb278efc8e06c54d72f5d2d977e9b64768dc09036e9c829
  importance: 2
  status: normal
- id: c8
  role: evaluation
  text: 為什麼難度差這麼多，blog 的推論是：parallel 測的是「兩條分支裡誰的方向比較好」，兩條路都是 agent 真的走完的；detour 測的是「能不能比當時行動的 agent 更早看出這個方向會失敗」，這需要預見後果，而不是比較兩個結果
  source_quotes:
  - "為什麼難度差這麼多？我的推論：parallel 測的是「兩條分支裡誰的方向比較好」，兩條路都是 agent 真的走完的；detour 測的是「能不能比當時行動的 agent 更早看出這個方向會失敗」，這需要預見後果，而不是比較兩個結果。"
  anchor_type: 部落格推論
  importance: 4
  status: normal
- id: c9
  role: evaluation
  text: blog 肯定兩種造題法分開統計：parallel 抓 agent 沒發現的錯，detour 抓 agent 自己改正的錯，讀者看得到兩者的難度差異，不是被混成一個平均數
  source_quotes:
  - "兩種造題法互補，而且分開統計。 parallel 抓 agent 沒發現的錯，detour 抓 agent 自己改正的錯。讀者看得到兩者的難度差異，不是被混成一個平均數。"
  anchor_type: 部落格判斷
  importance: 5
  status: normal
- id: c10
  role: context
  text: 論文替每一題標註時間跨度（要看到多遠的未來，才能確定正確答案），分成四級：in prefix（前綴裡已經有決定性的事實）158 題、inferable（前綴裡的線索合起來就足以判斷）219 題、next step（岔路口之後的第一個觀察結果就能確定）56 題、more work（要做完一次本地檢查，或更長的後續工作才能確定）69 題。標註者是 GPT-5.5，它讀題目、前綴、兩個候選以及正確答案來判斷
  source_quotes:
  - "論文替每一題標註時間跨度：要看到多遠的未來，才能確定正確答案。分成四級，然後看模型在各級的準確率。標註者是 GPT-5.5：它讀題目、前綴、兩個候選，以及正確答案，判斷是哪一種證據支持這個答案。"
  - "| in prefix（前綴內） | 前綴裡已經有決定性的事實，能直接排除一個候選（例如錯誤訊息） | 158 |"
  - "| inferable（可推得） | 沒有單一決定性事實，但前綴裡的線索合起來就足以判斷 | 219 |"
  - "| next step（下一步） | 岔路口之後的第一個觀察結果就能確定 | 56 |"
  - "| more work（更多工作） | 要做完一次本地檢查，或更長的後續工作才能確定 | 69 |"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 計數
  qualifiers:
  - text: more work 是原本最高的兩級合併而成；更長後續工作才確定的最高級只有 13 題，單獨拆出來樣本太少，所以合併
    source_quote: "more work 是原本最高的兩級合併而成：quick local check（做完一次本地檢查才確定）56 題，加上更長後續工作才確定的最高級 13 題，共 69 題。"
  importance: 3
  status: normal
- id: c11
  role: anchor
  text: 14 個模型的平均準確率，隨時間跨度等級升高依序是 62.3%、42.9%、31.5%、21.0%：證據已經在前綴裡的題平均答對 62.3%，要做更多工作才看得出答案的題只剩 21.0%，越晚才看得出答案的題越難
  source_quotes:
  - "結果：14 個模型的平均準確率，隨等級升高依序是 62.3%、42.9%、31.5%、21.0%，越晚才看得出答案的題越難。"
  - "證據已經在前綴裡的題，平均答對 62.3%；要做更多工作才看得出答案的題，只剩 21.0%。"
  anchor_type: 實驗結果
  comparison_target: 各時間跨度等級之間互相比較（in prefix 62.3% 對 more work 21.0%）
  qualifiers:
  - text: 排名後段的 Grok 4.20 Reasoning、GPT-5.4 Mini、GPT-5.4 Nano 分別有 459、112、93 次（共 1,004 次）作答無法解析而被計為答錯，分數混入了格式遵循的因素
    source_quote: "排名後段的 Grok 4.20 Reasoning、GPT-5.4 Mini、GPT-5.4 Nano 分別有 459、112、93 次（共 1,004 次）作答無法解析而被計為答錯，分數混入了格式遵循的因素。"
  - text: 時間跨度的標註者是 GPT-5.5，它讀題目、前綴、兩個候選以及正確答案來判斷
    source_quote: "標註者是 GPT-5.5：它讀題目、前綴、兩個候選，以及正確答案，判斷是哪一種證據支持這個答案。"
  figures:
  - file: figures/tasteful-agent/table6.png
    article: tasteful-agent
    src: table6.png
    caption: 表 5 — 每個模型在各時間跨度等級的準確率。準確率要求兩種呈現順序都答對。（來源：原始論文 Table 6。）
    sha256: f913cbe0449fd92f0153cbebe4b4f890818f9ab5bcf86e4325ab40b9391c8151
  importance: 2
  status: normal
- id: c12
  role: anchor
  text: 推理預算：同一個模型把推理設定從最低開到最高，GPT-5.6 Sol 變化 -0.2 點，GPT-5.6 Luna +2.2 點；多花推理 token 沒有明顯幫助，而且模型在最難的題上想得最久
  source_quotes:
  - "| 推理預算（圖 5 右、表 4） | 多想會不會變準 | 同一個模型把推理設定從最低開到最高：GPT-5.6 Sol 變化 \\( -0.2 \\) 點，GPT-5.6 Luna \\( +2.2 \\) 點 | 多花推理 token 沒有明顯幫助，而且模型在最難的題上想得最久。只測了同一個家族的兩個模型 |"
  anchor_type: 實驗結果
  comparison_target: 同一個模型在最低推理設定下的準確率
  qualifiers:
  - text: 只測了同一個家族的兩個模型
    source_quote: "只測了同一個家族的兩個模型"
  - text: GPT-5.6 Sol 在主實驗是 58.2%（292/502），在表 4 同設定重跑是 55.6%，差 2.6 點，論文沒有說明；blog 推論這個落差和推理預算的差異是同一個量級，解讀推理預算的結論時要記得這個噪音
    source_quote: "第二，GPT-5.6 Sol 在主實驗是 58.2%（292/502），在表 4 同設定重跑是 55.6%，差 2.6 點，論文沒有說明。我的推論：兩者都是 502 題合併的嚴格準確率，所以這個落差和上面推理預算的差異是同一個量級，解讀推理預算的結論時要記得這個噪音。"
  figures:
  - file: figures/tasteful-agent/table7.png
    article: tasteful-agent
    src: table7.png
    caption: 表 4 — 兩個模型在三種推理強度設定下的準確率，同時列出各級「證據多晚出現」的表現（分級見下一小節）。（來源：原始論文 Table 7。）
    sha256: a4cb10148ed51302145593c17acc7d1dd6de1d38aa2deff43903b67f50e44d5a
  importance: 3
  status: normal
```
