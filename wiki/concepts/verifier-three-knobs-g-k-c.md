---
id: verifier-three-knobs-g-k-c
title: 讓連續分數更準的三個旋鈕各對付一個問題、各有限制：粒度 G 對付解析度不足，重複 K 只降變異數不降偏誤，準則拆解 C 只證明了三個比一個好
type_hint: 方法
context_type: bound_to_source
sources:
- article: llm-as-a-verifier
  article_title: "LLM 打分數老是平手？LLM-as-a-Verifier 改讀機率分佈"
  url: https://datasciocean.com/paper-intro/llm-as-a-verifier/
  sections:
  - LLM 打分數老是平手，是 argmax 把資訊丟掉了
  - 問題：資訊在 argmax 那一步被壓扁
  - 核心公式：用期望值取代 argmax
  - 三個旋鈕：粒度、重複、準則拆解
  - 粒度 G：對付解析度不足
  - 重複 K：對付單次評估的隨機偏差
  - 準則拆解 C：對付評分標準本身不合理
  - 一個案例：query-optimize 為什麼 judge 看不出來
  - 可以帶走的東西
  first_appearance: true
parent: null
related:
- verifier-expected-value-vs-argmax
- verifier-results-how-to-read
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 三個旋鈕各對付一個問題，也各有限制：G 對付解析度不足，效果明確，但成本論述自相矛盾；K 對付單次評估的隨機偏差，只降變異數、不降偏誤；C 對付評分標準本身不合理，只證明了三個比一個好
  source_quotes:
  - "三個旋鈕各對付一個問題，也各有限制："
  - "**G**：解析度不足；效果明確，但成本論述自相矛盾。"
  - "**K**：單次評估的隨機偏差；只降變異數，不降偏誤。"
  - "**C**：評分標準本身不合理；只證明了三個比一個好。"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: LLM-as-a-Verifier（arXiv 2607.05391v2，Stanford / UC Berkeley / NVIDIA）讓 LLM 替另一個 LLM 的輸出打分數時，不取分數 token 機率最高的那一個（argmax），改算期望值（把每個分數乘上它的機率再加總），分數從離散整數變成連續實數；作者再加上重複取樣、準則拆解，包成一個框架
  source_quotes:
  - "（arXiv 2607.05391v2，Stanford / UC Berkeley / NVIDIA）"
  - "用 LLM 幫另一個 LLM 的輸出打分數，現在幾乎是標配"
  - "但標準做法只取機率最高的那一個（這個動作叫 argmax），其餘全丟。"
  - "改法很單純：不取 argmax，改算**期望值**（把每個分數乘上它的機率再加總），分數從離散整數變成連續實數。作者把這個改動加上重複取樣、準則拆解，包成一個叫 LLM-as-a-Verifier 的框架"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 2
  status: normal
- id: c3
  role: context
  text: 三個旋鈕對應評分公式的三層：最內層對 G 個分數 token 做機率加權（granularity，一次 LLM 呼叫得到 1 個期望值），中層同一準則重複 K 次（repetition），外層對 C 個準則加總（criteria），最後除以 C×K；主實驗的設定是 C=3、K=8、G=20
  source_quotes:
  - "**最內層（對 g 加總）：granularity。** 一次 LLM 呼叫，取得分數 token 位置的機率分佈，把 G 個候選分數做機率加權，得到 1 個期望值。"
  - "**中層（對 k 加總）：repetition。** 同一準則重複 K 次，得到 K 個期望值，加總。"
  - "**外層（對 c 加總）：criteria。** 每個準則各自跑完中層，全部加總。"
  - "**最後**除以 \\( C \\times K \\)。"
  - "準則總數（主實驗 C=3）"
  - "重複次數（主實驗 K=8）"
  - "主實驗 G=20"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 3
  status: normal
- id: c4
  role: context
  text: 這一節的準確率指配對驗證準確率（pairwise accuracy）：把兩條軌跡（agent 做事的完整紀錄）配成一對，verifier 判對的比例
  source_quotes:
  - "下面的準確率指配對驗證準確率（pairwise accuracy），也就是把兩條軌跡配成一對，verifier 判對的比例。"
  - "\\( \\tau \\)（讀作 tau）是被評分的軌跡（agent 做事的完整紀錄）"
  anchor_type: 背景說明
  importance: 4
  status: normal
- id: c5
  role: evidence
  text: 把分數 token 的粒度 G 拉大，準確率一路上升：G=1 是 73.1%、G=4 是 75.1%、G=16 是 77.2%、G=20 是 77.5%
  source_quotes:
  - "第一個旋鈕是 **Score Token Granularity（G，分數 token 的粒度）**，對付的是「解析度不足」。把 G 拉大，準確率一路上升："
  - "| G | 1 | 2 | 4 | 8 | 16 | 20 |"
  - "| 準確率 | 73.1% | 73.3% | 75.1% | 75.9% | 77.2% | 77.5% |"
  anchor_type: 實驗結果
  comparison_target: G=1 的準確率
  importance: 5
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/figure4.png
    article: llm-as-a-verifier
    src: figure4.png
    caption: 圖 3 — 驗證準確率沿著三個維度都會上升：分數粒度、重複次數、準則拆解。（來源：原始論文 Figure 4。）
    sha256: 636df20c8eee234a4d07db737031f0a575159a73d7fc0395fe9b214d789531b7
- id: c6
  role: mechanism
  text: 擴大量表並沒有給 verifier 任何新資訊；論文的說法是，它給了 decoder 一個更細的空間，去投射模型內部本來就有的信念：原本會被四捨五入到同一格的相近信念，現在落到不同的連續值上
  source_quotes:
  - "反直覺的地方在於：擴大量表**並沒有給 verifier 任何新資訊**。論文的說法是，它給了 decoder（把機率轉成輸出的那一步）一個更細的空間，去投射模型內部本來就有的信念：原本會被四捨五入到同一格的相近信念，現在落到不同的連續值上。"
  anchor_type: 原作者解讀
  importance: 6
  status: normal
- id: c7
  role: evaluation
  text: 實務上很要緊、但論文自相矛盾的點：G 到底要不要重跑 LLM？若不用重跑，G 只是事後從 API 回傳的候選清單多取幾個，免費；若要重跑（1–5 和 1–20 是兩個不同的 prompt），換 G 就要換 prompt 重跑，不免費，「G 不影響呼叫次數」那句就不成立，整個成本評估要重算
  source_quotes:
  - "這裡有個實務上很要緊、但論文自相矛盾的點：**G 到底要不要重跑 LLM？** 論文沒有澄清，兩處講法直接打架。這件事影響很大：如果要重跑，前面「G 不影響呼叫次數」那句就不成立，整個成本評估要重算。"
  - "G 只是事後從 API 回傳的候選清單多取幾個，**免費**"
  - "而 1–5 和 1–20 是兩個不同的 prompt | 換 G 就要換 prompt 重跑，**不免費**"
  - "論文兩種講法都有，所以第一件事是在自己的環境確認是哪一種。"
  anchor_type: 部落格考證
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 7
  status: normal
- id: c8
  role: evidence
  text: 第二個旋鈕是重複評估 K：同一個問題問 K 次再取平均，數學上就是個 Monte Carlo estimator；K=1 時準確率 74.7%，K=4 是 77.1%，K=16 是 77.5%
  source_quotes:
  - "第二個旋鈕是 **Repeated Evaluation（K，重複評估）**，對付的是單次評估的隨機偏差。做法就是同一個問題問 K 次再取平均，數學上就是個 Monte Carlo estimator（用多次隨機取樣的平均去逼近真值的估計方法）："
  - "| K | 1 | 2 | 4 | 8 | 16 |"
  - "| 準確率 | 74.7% | 76.1% | 77.1% | 77.3% | 77.5% |"
  anchor_type: 實驗結果
  comparison_target: K=1 的準確率
  importance: 8
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/figure4.png
    article: llm-as-a-verifier
    src: figure4.png
    caption: 圖 3 — 驗證準確率沿著三個維度都會上升：分數粒度、重複次數、準則拆解。（來源：原始論文 Figure 4。）
    sha256: 636df20c8eee234a4d07db737031f0a575159a73d7fc0395fe9b214d789531b7
- id: c9
  role: mechanism
  text: 平均只降變異數，不降偏誤（模型系統性地往同一個方向誤判）：變異數以 O(1/K) 縮小，偏誤完全不變；如果 verifier 對某類軌跡每次都往同一個方向錯，跑一百次還是錯，就像秤本身永遠多 2 公斤，量再多次也修不掉
  source_quotes:
  - "這裡的眉角是：**平均只降變異數，不降偏誤**（偏誤是指模型系統性地往同一個方向誤判）。變異數以 O(1/K) 縮小，偏誤完全不變。如果 verifier 對某類軌跡有系統性誤判、每次都往同一個方向錯，跑一百次還是錯。"
  - "拿量測來類比就很清楚：增加樣本數可以縮小標準誤，但如果秤本身永遠多 2 公斤，量再多次也修不掉那 2 公斤。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 9
  status: normal
- id: c10
  role: qualifier
  text: 論文自己也承認 K 變大時報酬遞減，因為困難樣本上的偏誤是相關的
  source_quotes:
  - "論文自己也承認 K 變大時報酬遞減，因為困難樣本上的偏誤是相關的。"
  anchor_type: 原作者解讀
  importance: 10
  status: normal
- id: c11
  role: evidence
  text: 拿離散 judge 和 verifier 在不同重複次數下對照：K=1 時 judge 準確率 71.8%、平手率 26.7%，verifier 準確率 74.7%、平手率 0.0%；K=16 時 judge 準確率 74.7%、平手率 5.5%，verifier 準確率 77.5%、平手率 0.0%
  source_quotes:
  - "| K | Judge 準確率 | Verifier 準確率 | Judge 平手率 | Verifier 平手率 |"
  - "| 1 | 71.8% | 74.7% | 26.7% | 0.0% |"
  - "| 16 | 74.7% | 77.5% | 5.5% | 0.0% |"
  anchor_type: 實驗結果
  comparison_target: 同一個 K 下的離散 judge（取 argmax）
  importance: 11
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/figure7.png
    article: llm-as-a-verifier
    src: figure7.png
    caption: 圖 5 — 拉高重複次數，judge 的平手率從 26.7% 掉到 5.5%，但準確率幾乎沒動；verifier 從頭到尾零平手。（來源：原始論文 Figure 7。）
    sha256: 47db62fc4b7b968b2e4b21ed7abfa1dc22475a1855bf13ec9a3fd157afc6f5f4
- id: c12
  role: evidence
  text: 論文想讓人看的是對角線：verifier 只跑 1 次（74.7%）就等於 judge 跑 16 次（74.7%）
  source_quotes:
  - "論文想讓你看的是對角線：**verifier 只跑 1 次（74.7%）就等於 judge 跑 16 次（74.7%）**。"
  qualifiers:
  - text: 「16 倍運算」這個對比有點誇大：judge 和 verifier 在每個 K 下的差距都落在 2.7 到 2.9pp 之間，那個對比只在剛好只在乎「追平 74.7%」這個門檻時才成立
    source_quote: "「16 倍運算」這個對比其實有點誇大：judge 和 verifier 在每個 K 下的差距都落在 2.7 到 2.9pp 之間，那個對比只在你剛好只在乎「追平 74.7%」這個門檻時才成立。"
  anchor_type: 原作者解讀
  comparison_target: 離散 judge 重複評估 16 次（K=16）
  importance: 12
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/figure7.png
    article: llm-as-a-verifier
    src: figure7.png
    caption: 圖 5 — 拉高重複次數，judge 的平手率從 26.7% 掉到 5.5%，但準確率幾乎沒動；verifier 從頭到尾零平手。（來源：原始論文 Figure 7。）
    sha256: 47db62fc4b7b968b2e4b21ed7abfa1dc22475a1855bf13ec9a3fd157afc6f5f4
- id: c13
  role: mechanism
  text: judge 靠重複評估得到的改善，主要機制是用平均打破平手（平手率 26.7% → 5.5%），而不是真的變會判斷；就像用重複測量去彌補一把刻度太粗的尺，而 verifier 是直接換一把刻度細的
  source_quotes:
  - "judge 靠重複評估得到的改善，主要機制是用平均打破平手（26.7% → 5.5%），而不是真的變會判斷。就像用重複測量去彌補一把刻度太粗的尺，而 verifier 是直接換一把刻度細的。"
  anchor_type: 部落格推論
  comparison_target: judge 在 K=1 與 K=16 的平手率
  importance: 13
  status: normal
- id: c14
  role: evaluation
  text: 更實質的差別是天花板不同：judge 在 K=16 已經飽和（74.4% → 74.7%），verifier 還停在 77.5%
  source_quotes:
  - "更實質的差別是天花板不同：judge 在 K=16 已經飽和（74.4 → 74.7），verifier 還停在 77.5%。"
  anchor_type: 部落格判斷
  comparison_target: 同在 K=16 的 verifier；judge 自己 K=4 與 K=16 的準確率
  importance: 14
  status: normal
- id: c15
  role: mechanism
  text: 第三個旋鈕是準則拆解 C，對付的是評分標準本身不合理：在長時序的 agent 任務裡，「這條軌跡正確嗎？」把好幾個邏輯上獨立的因素混在一起，verifier 往往只抓住 prompt 裡最顯眼的那一個；論文對 code agent 拆出三個子準則：Specification（有沒有滿足任務的所有要求）、Output（最終輸出格式是否符合預期）、Errors（log／工具輸出有無失敗訊號）
  source_quotes:
  - "第三個旋鈕是 **Criteria Decomposition（C，準則拆解）**，對付的是評分標準本身不合理。"
  - "但在長時序的 agent 任務裡，「這條軌跡正確嗎？」這個問題把好幾個邏輯上獨立的因素混在一起，verifier 往往只抓住 prompt 裡最顯眼的那一個。"
  - "論文對 code agent 拆出三個子準則："
  - "| Specification | 有沒有滿足任務的所有要求？ | 完整性 |"
  - "| Output | 最終輸出格式是否符合預期？ | 結果 |"
  - "| Errors | log／工具輸出有無失敗訊號？ | 證據 |"
  anchor_type: 設計參數
  importance: 15
  status: normal
- id: c16
  role: evidence
  text: 單一準則的準確率是 Specification 75.2%、Errors 76.0%、Output 76.4%，三者 ensemble 是 78.3%
  source_quotes:
  - "| Specification 單獨 | 75.2% |"
  - "| Errors 單獨 | 76.0% |"
  - "| Output 單獨 | 76.4% |"
  - "| **三者 ensemble** | **78.3%** |"
  qualifiers:
  - text: 圖裡誤差棒重疊得很明顯，1.9pp 的改善沒做顯著性檢定，也沒說明誤差棒代表什麼
    source_quote: "圖裡誤差棒重疊得很明顯，1.9pp 的改善沒做顯著性檢定，也沒說明誤差棒代表什麼。"
  anchor_type: 實驗結果
  comparison_target: 各子準則單獨使用的準確率
  importance: 16
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/figure4.png
    article: llm-as-a-verifier
    src: figure4.png
    caption: 圖 3 — 驗證準確率沿著三個維度都會上升：分數粒度、重複次數、準則拆解。（來源：原始論文 Figure 4。）
    sha256: 636df20c8eee234a4d07db737031f0a575159a73d7fc0395fe9b214d789531b7
- id: c17
  role: mechanism
  text: 準則拆解說白了就是 ML 的 ensemble：多個各有不同偏誤的弱分類器，只要錯誤不完全相關，平均起來就會優於單一最強者
  source_quotes:
  - "說白了這就是 ML 的 ensemble：多個各有不同偏誤的弱分類器，只要錯誤不完全相關，平均起來就會優於單一最強者。"
  anchor_type: 部落格推論
  importance: 17
  status: normal
- id: c18
  role: evaluation
  text: C 的證據比前兩個旋鈕薄：三個準則怎麼來的論文沒說，也沒有「試過 4 個、5 個」的 ablation；C 根本沒有 scaling 曲線，只有四根柱子，嚴格講只證明了「3 個比 1 個好」，沒證明 C 是一個可 scaling 的軸，但摘要就把它跟另外兩個並列
  source_quotes:
  - "這一個旋鈕的證據比前兩個薄，有四個缺口："
  - "**三個準則怎麼來的，論文沒說**，沒有交代選擇過程，也沒有「試過 4 個、5 個」的 ablation"
  - "**C 根本沒有 scaling 曲線。** G 和 K 都有完整曲線，C 只有四根柱子，沒有 C=2 的資料，也不知道 C=5、C=10 會怎樣。嚴格講，論文只證明了「3 個比 1 個好」，沒證明 C 是一個可 scaling 的軸，但摘要就把它跟另外兩個並列。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 18
  status: normal
- id: c19
  role: evaluation
  text: 換到別的領域怎麼套用也沒回答：這三個準則明說是為 code-agent 軌跡設計的，但機器人和醫療的實驗也宣稱用同一組；子準則要自己設計，論文提供不了設計方法論
  source_quotes:
  - "**換到別的領域怎麼套用，也沒回答。** 這三個準則明說是為 code-agent 軌跡設計的，但機器人和醫療的實驗也宣稱用同一組。"
  - "但子準則要自己設計：論文那組 Specification / Output / Errors 是為 reference-free 的 terminal 任務設計的，不見得適用其他情境，而論文也提供不了設計方法論。"
  anchor_type: 部落格判斷
  importance: 19
  status: normal
```
