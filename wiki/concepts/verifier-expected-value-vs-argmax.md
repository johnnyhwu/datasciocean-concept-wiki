---
id: verifier-expected-value-vs-argmax
title: LLM 打分數時內部的信念是連續的，是 argmax 把它壓扁的；改算分數 token 機率分佈的期望值，平手就拆開了，代價是被迫每次表態
type_hint: 方法
context_type: bound_to_source
sources:
- article: llm-as-a-verifier
  article_title: "LLM 打分數老是平手？LLM-as-a-Verifier 改讀機率分佈"
  url: https://datasciocean.com/paper-intro/llm-as-a-verifier/
  sections:
  - LLM 打分數老是平手，是 argmax 把資訊丟掉了
  - 問題：資訊在 argmax 那一步被壓扁
  - judge 與 verifier，以及 scoring prompt 怎麼寫
  - 核心公式：用期望值取代 argmax
  - 正規化與 Bradley–Terry：把分數差變成勝率
  - 粒度 G：對付解析度不足
  - 一個案例：query-optimize 為什麼 judge 看不出來
  - 可以帶走的東西
  - 結論
  first_appearance: true
parent: null
related:
- verifier-three-knobs-g-k-c
- ppt-pivot-tournament
- verifier-results-how-to-read
- bradley-terry-pairwise-preference
- confidence-three-metrics
- jev-cascade-overview
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: LLM 打分數時內部的信念是連續的，是 argmax 把它壓扁的；把 argmax 換成期望值，平手率從 27% 降到 0%，排序能力就回來了
  source_quotes:
  - "這篇論文的核心洞見很小、也很實在：**LLM 打分數時內部的信念是連續的，是 argmax 把它壓扁的**。把 argmax 換成期望值，平手率從 27% 降到 0%，排序能力就回來了。"
  qualifiers:
  - text: 27% 是論文在 Terminal-Bench 上量到的比較結果平手比例
    source_quote: "在 Terminal-Bench 上，論文量到 27% 的比較結果是平手。"
  - text: verifier 的 0% 平手，是在同一個 query-optimize 任務各評分一百次（平手 0/100），以及不同重複次數下的平手率對照（verifier 平手率 0.0%）中量到的
    source_quote: "表中 \\( s_c \\) 是正確軌跡的分數，\\( s_i \\) 是錯誤軌跡的分數，每種方法各評分一百次。"
  - text: 不同重複次數下，verifier 的平手率都是 0.0%（K=1 時 judge 平手率 26.7%）
    source_quote: "| 1 | 71.8% | 74.7% | 26.7% | 0.0% |"
  - text: 代價是被迫每次表態：在同一個 query-optimize 任務各評分一百次，離散 judge 的排錯次數是 0/100，連續 verifier 消除平手後，其中二三成表錯了
    source_quote: "連續 verifier 消除平手的代價，是被迫每次都表態，其中二三成表錯了。"
  - text: 表錯的實際次數是 verifier（G=5）31/100、verifier（G=20）23/100
    source_quote: "| Verifier（連續，G=5） | 69/100 | 0/100 | 31/100 |"
  anchor_type: 原作者解讀
  comparison_target: 標準做法：取分數 token 機率最高者（argmax）的離散 LLM judge
  importance: 1
  status: normal
- id: c2
  role: context
  text: 用 LLM 幫另一個 LLM 的輸出打分數，現在幾乎是標配：叫模型輸出一個 1 到 5 的整數，然後拿那個整數去排序、篩選、當 reward（訓練時給模型的獎勵訊號）
  source_quotes:
  - "用 LLM 幫另一個 LLM 的輸出打分數，現在幾乎是標配：叫模型輸出一個 1 到 5 的整數，然後拿那個整數去排序、篩選、當 reward（訓練時給模型的獎勵訊號）。"
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 2
  status: normal
- id: c3
  role: context
  text: LLM-as-a-Verifier（arXiv 2607.05391v2，Stanford / UC Berkeley / NVIDIA）把「改算期望值」這個改動加上重複取樣、準則拆解，包成一個框架，再配一個新的排名演算法 PPT（用成對比較，從 N 條候選裡挑出最好的一條），橫跨程式、機器人、醫療三個領域做了實驗
  source_quotes:
  - "（arXiv 2607.05391v2，Stanford / UC Berkeley / NVIDIA）"
  - "作者把這個改動加上重複取樣、準則拆解，包成一個叫 LLM-as-a-Verifier 的框架，再配一個新的排名演算法 PPT（用成對比較，從 N 條候選裡挑出最好的一條），橫跨程式、機器人、醫療三個領域做了實驗。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 模型在輸出分數的那個 token 位置，內部產生的是一個完整的機率分佈（每個分數各有多大機率），但標準做法只取機率最高的那一個（argmax），其餘全丟；資訊不是模型沒產生，是解碼策略把它丟掉的
  source_quotes:
  - "模型在輸出分數的那個 token（模型處理文字的最小單位）位置，內部產生的是一個**完整的機率分佈**，也就是「每個分數各有多大機率」，但標準做法只取機率最高的那一個（這個動作叫 argmax），其餘全丟。資訊不是模型沒產生，是解碼策略把它丟掉的。"
  anchor_type: 原作者解讀
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 改法很單純：不取 argmax，改算期望值（把每個分數乘上它的機率再加總），分數從離散整數變成連續實數
  source_quotes:
  - "改法很單純：不取 argmax，改算**期望值**（把每個分數乘上它的機率再加總），分數從離散整數變成連續實數。"
  anchor_type: 設計參數
  importance: 5
  status: normal
- id: c6
  role: evidence
  text: 粗粒度的量表配上 argmax 解碼，大量候選解會打成平手；在 Terminal-Bench（一個考 agent 做任務的 benchmark）上，論文量到 27% 的比較結果是平手；平手就不能排序，不能排序就沒辦法從 N 條候選裡挑一條
  source_quotes:
  - "在 Terminal-Bench（一個考 agent 做任務的 benchmark，也就是拿來比較模型的標準測試題組）上"
  - "粗粒度的量表配上這種解碼方式，後果很直接：**大量候選解會打成平手**。在 Terminal-Bench 上，論文量到 27% 的比較結果是平手。平手就是不能排序，不能排序就沒辦法從 N 條候選裡挑一條。"
  anchor_type: 實驗結果
  comparison_target: 全部比較結果（27% 是其中平手的比例）
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: 公式的意思：對同一條軌跡（agent 做事的完整紀錄），每個準則各問 K 次，每次把「每個可能的分數乘上它的機率」加起來，最後全部平均；最內層對 G 個分數 token 做機率加權（granularity），中層同一準則重複 K 次（repetition），外層對 C 個準則加總（criteria），最後除以 C×K
  source_quotes:
  - "公式的意思，用一句話說：對同一條軌跡，每個準則各問 \\( K \\) 次，每次把「每個可能的分數乘上它的機率」加起來，最後全部平均。"
  - "\\( \\tau \\)（讀作 tau）是被評分的軌跡（agent 做事的完整紀錄）"
  - "**最內層（對 g 加總）：granularity。** 一次 LLM 呼叫，取得分數 token 位置的機率分佈，把 G 個候選分數做機率加權，得到 1 個期望值。"
  - "**中層（對 k 加總）：repetition。** 同一準則重複 K 次，得到 K 個期望值，加總。"
  - "**外層（對 c 加總）：criteria。** 每個準則各自跑完中層，全部加總。"
  - "**最後**除以 \\( C \\times K \\)。"
  anchor_type: 設計參數
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: 每條軌跡的 LLM 呼叫次數是 C×K，主實驗設定 C=3、K=8，所以每條軌跡 24 次（成對比較時，每一對也是 C×K=24 次）；再乘上 PPT 的比較對數，總量會很可觀，而論文從未討論延遲與成本
  source_quotes:
  - "而是**取得每個 R 所需的 LLM 呼叫成本**，每一對就是 \\( C \\times K \\) = 24 次。"
  - "成本要自己算清楚：每條軌跡的 LLM 呼叫次數 = \\( C \\times K \\)，主實驗設定 C=3, K=8，所以每條軌跡 24 次。再乘上 PPT 的比較對數，總量會很可觀。論文從未討論延遲與成本，這是套用前必須自己算的一筆帳。"
  qualifiers:
  - text: G 要不要重跑 LLM，論文兩處講法打架：如果要重跑，「G 不影響呼叫次數」那句就不成立，整個成本評估要重算
    source_quote: "這件事影響很大：如果要重跑，前面「G 不影響呼叫次數」那句就不成立，整個成本評估要重算。"
  anchor_type: 數學推導
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 8
  status: normal
- id: c9
  role: anchor
  text: 舉例：G=5，某條軌跡給 1 到 5 各級的機率依序是 0.02、0.05、0.13、0.35、0.45，離散 judge 走 argmax 拿到 5，verifier 算期望值拿到 4.16；另一條軌跡若 p(v5)=0.52、p(v4)=0.30，argmax 一樣是 5（平手），但期望值會落在 4.3 附近（不平手）；平手率歸零的機制就是這麼來的
  source_quotes:
  - "實際算一遍最有感。假設 G=5，某條軌跡的分數分佈是："
  - "| \\( v_1 \\) | 1 | 0.02 | 0.02 |"
  - "| \\( v_2 \\) | 2 | 0.05 | 0.10 |"
  - "| \\( v_3 \\) | 3 | 0.13 | 0.39 |"
  - "| \\( v_4 \\) | 4 | 0.35 | 1.40 |"
  - "| \\( v_5 \\) | 5 | 0.45 | 2.25 |"
  - "離散 judge 走 argmax 拿到 **5**；verifier 算期望值拿到 **4.16**。現在關鍵來了：另一條軌跡如果分佈是 \\( p(v_5)=0.52 \\)、\\( p(v_4)=0.30 \\)（其餘機率分給更低的分數），argmax 一樣是 5（**平手**），但期望值會落在 4.3 附近（**不平手**）。平手率歸零的機制就是這麼來的。"
  qualifiers:
  - text: 這組機率是示意值，論文從未公布任何一次評分的實際機率分佈
    source_quote: "上面那組機率是示意值，因為**論文從未公布任何一次評分的實際機率分佈**。"
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: verifier 實際收到的 prompt 一次塞兩個候選解，對照著評；<score_A> / <score_B> 這兩個標籤是整個機制的關鍵：真正要的不是標籤裡輸出的文字，而是該 token 位置上整個 vocabulary 的機率分佈，標籤讓你能精準定位分數在第幾個 token，才有辦法去撈 logprob
  source_quotes:
  - "**一次 prompt 塞兩個候選解，對照著評。** 不是各自單獨評分再比大小。"
  - "**`<score_A>` / `<score_B>` 這兩個標籤是整個機制的關鍵。**"
  - "真正要的不是標籤裡輸出的那串文字，而是該 token 位置上整個 vocabulary 的機率分佈。標籤存在的意義是讓你能精準定位「分數在第幾個 token」，才有辦法去撈 logprob（模型替每個候選 token 算出的對數機率）。"
  qualifiers:
  - text: 為什麼兩條軌跡要放在同一個 prompt，論文沒有解釋原因；數學上不需要，分兩次 prompt 各自評分完全可行
    source_quote: "但論文明講是同一個 prompt 一次拿兩個分數，而且**沒有解釋原因**。"
  anchor_type: 設計參數
  importance: 10
  status: normal
- id: c11
  role: mechanism
  text: prompt 裡沒有 ground truth（標準答案）：verifier 只拿到任務描述和軌跡內容，必須自己從 log、工具呼叫結果、輸出格式這些證據判斷對錯，這是刻意的 reference-free 設計
  source_quotes:
  - "這裡有個容易被忽略的設計：**prompt 裡沒有 ground truth**（標準答案）。verifier 只拿到任務描述和軌跡內容，必須自己從 log、工具呼叫結果、輸出格式這些證據判斷對錯，不是拿去跟標準答案比對。這是刻意的 reference-free 設計"
  qualifiers:
  - text: 把 ground truth 放進 prompt、單條評分判對錯的用法，論文從未驗證過：所有實驗都是「選最好」或「兩兩比較」
    source_quote: "但**論文從未驗證過這個用法**：所有實驗都是「選最好」或「兩兩比較」，沒有任何「單條對照 ground truth 判對錯」的實驗。"
  anchor_type: 設計參數
  importance: 11
  status: normal
- id: c12
  role: mechanism
  text: 分數算完之後會正規化到 [0,1]（最低分是 0、最高分是 1），再用 Bradley–Terry（一個把實力差距轉成勝率的模型）把兩條軌跡的分數差轉成偏好機率：分數差越大，前者贏的機率越接近 1；兩者一樣，就是對半
  source_quotes:
  - "分數算完之後會壓到 [0,1]："
  - "白話說，就是把分數換算成「落在量表的哪個位置」：最低分是 0，最高分是 1。"
  - "接著把分數差轉成偏好機率，用的是 Bradley–Terry（一個把實力差距轉成勝率的模型）。"
  - "白話說：分數差越大，前者贏的機率越接近 1；兩者一樣，就是對半。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 12
  status: normal
- id: c13
  role: mechanism
  text: 論文沒解釋為什麼要正規化；從機制推敲：正規化不改變單次比較的排序，真正影響的是 sigmoid（把任意大小的數字壓到 0 到 1 之間的函數）會不會飽和：1–20 原始量表上兩條差 8 分，σ(差值)=0.9997；正規化後同樣差距是 0.42，σ=0.60；沒有正規化的話，「好一點」和「好很多」都會被壓成 1.0；這在排名演算法 PPT 裡才真正出問題：PPT 把多場比較的機率累加起來當排名依據，一旦飽和，累加值就幾乎只反映「有沒有碰到弱對手」，而不是「到底多強」
  source_quotes:
  - "論文沒解釋為什麼要正規化，但從機制推敲得出來：正規化不改變單次比較的排序（它是線性單調變換），真正影響的是下一步 sigmoid（把任意大小的數字壓到 0 到 1 之間的函數）會不會飽和。"
  - "| 1–20 原始量表，兩條差 8 分 | 8.0 | 0.9997 |"
  - "| 正規化後同樣差距 | 0.42 | 0.60 |"
  - "沒有正規化的話，「好一點」和「好很多」都會被壓成 1.0，等於把剛剛辛苦保留下來的細緻度又丟掉一次。這在後面會細講的排名演算法 PPT 裡才真正出問題，因為 PPT 是把多場比較的機率**累加**起來當排名依據；一旦飽和，累加值就幾乎只反映「你有沒有碰到弱對手」，而不是「你到底多強」。"
  anchor_type: 部落格推論
  comparison_target: 同樣差距在未正規化（1–20 原始量表）與正規化後的 sigmoid 輸出
  importance: 13
  status: normal
- id: c14
  role: evaluation
  text: 這篇的 Bradley–Terry 用法跟經典 BT 是反過來的：經典 BT 已知勝負紀錄、反推潛在實力值；本篇已知分數 R、正推偏好機率，等於直接把 R 當成潛在實力值，跳過了 BT 最麻煩的參數估計
  source_quotes:
  - "而且這篇的用法跟經典 BT 是反過來的："
  - "| 已知 | 勝負紀錄 | 分數 \\( R(x,\\tau) \\) |"
  - "| 方向 | 觀測 → 反推 | 實力 → 正推 |"
  - "論文直接把 R 當成 latent strength（潛在實力值，經典 BT 要從勝負紀錄反推的那個東西），等於跳過了 BT 最麻煩的參數估計。"
  anchor_type: 部落格考證
  importance: 14
  status: normal
- id: c15
  role: context
  text: 一個 Terminal-Bench V2 的案例（query-optimize）：給定一個 SQLite 資料庫和一段沒優化過的 SQL 查詢，寫出效能更好、而且輸出結果完全相同的版本；兩條軌跡都由 Claude Opus 4.5 產生。失敗的那條把資料庫複製到 /tmp、在複製品上加索引，拿兩個不同物理存取路徑上的結果比較，從來沒有真正驗證等價性，但它自己回報「內部 diff 檢查通過」
  source_quotes:
  - "這個案例來自 Terminal-Bench V2。**任務**：給定一個 SQLite 資料庫（一種常見的資料庫）和一段沒優化過的 SQL 查詢（向資料庫要資料的指令），寫出效能更好、而且**輸出結果完全相同**的版本。兩條軌跡都由 Claude Opus 4.5 產生"
  - "把資料庫複製到 /tmp → 在複製品上加索引"
  - "失敗的關鍵在於它是在**兩個不同的物理存取路徑**（資料庫實際取資料的路線，加了索引前後不同）上比較結果。"
  - "所以它從來沒有真正驗證等價性，但它自己回報「內部 diff 檢查通過」。"
  anchor_type: 原作者解讀
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 15
  status: normal
- id: c16
  role: mechanism
  text: 在這個案例裡，verifier（Gemini 2.5 Flash）其實有看出 agent 修改了資料庫來取得參考輸出、並未正確驗證等價性，卻用帶保留、程度性的措辭表達，講得像無關緊要；模型內部有正確判斷，但這個判斷在 argmax 那一步被壓扁了
  source_quotes:
  - "verifier 有看出來嗎？有。論文附錄引用的 Gemini 2.5 Flash 推理過程明確指出：agent 修改了資料庫來取得參考輸出，違反了任務的隱含限制，因此並未正確驗證等價性。"
  - "**verifier 抓到了，卻用帶保留、程度性的措辭表達**（像是「稍微乾淨一些」「略為直接一點」），講得像無關緊要。模型內部有正確判斷，但這個判斷在 argmax 那一步被壓扁了。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 16
  status: normal
- id: c17
  role: evidence
  text: 同一個 query-optimize 任務，每種方法各評分一百次（正確軌跡分數高於錯誤軌跡／平手／低於）：離散 judge（G=5）是 12/88/0；連續 verifier（G=5）是 69/0/31；連續 verifier（G=20）是 77/0/23
  source_quotes:
  - "表中 \\( s_c \\) 是正確軌跡的分數，\\( s_i \\) 是錯誤軌跡的分數，每種方法各評分一百次。"
  - "| Judge（離散，G=5） | 12/100 | **88/100** | 0/100 |"
  - "| Verifier（連續，G=5） | 69/100 | 0/100 | 31/100 |"
  - "| Verifier（連續，G=20） | **77/100** | 0/100 | 23/100 |"
  anchor_type: 實驗結果
  comparison_target: 同一任務、同樣評分一百次的離散 judge（G=5）
  importance: 17
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/table2.png
    article: llm-as-a-verifier
    src: table2.png
    caption: 圖 4 — 同一個任務跑一百次：離散 judge 有 88 次無法區分，連續 verifier 一次都沒有。（來源：原始論文 Table 2。）
    sha256: 806e6f4d25c74c98ba7b96df9085d2c0b61b93cd719ee1c416cf1a275b0bdd9b
- id: c18
  role: evaluation
  text: 這個對照設計很乾淨，因為一次只動一個變因：同一個 1–5 量表只換解碼方式（argmax → 期望值），88 次平手歸零、正確排序從 12 上升到 69；同樣是期望值只換量表（1–5 → 1–20），正確排序從 69 上升到 77
  source_quotes:
  - "這個對照設計很乾淨，因為它一次只動一個變因："
  - "**第 1 列 → 第 2 列**：同一個 1–5 量表，只換解碼方式（argmax → 期望值）。88 次平手歸零，正確排序從 12 上升到 69。"
  - "**第 2 列 → 第 3 列**：同樣是期望值，只換量表（1–5 → 1–20）。正確排序從 69 上升到 77。"
  anchor_type: 部落格判斷
  comparison_target: 同一任務上的離散 judge（G=5）與連續 verifier（G=5）
  importance: 18
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/table2.png
    article: llm-as-a-verifier
    src: table2.png
    caption: 圖 4 — 同一個任務跑一百次：離散 judge 有 88 次無法區分，連續 verifier 一次都沒有。（來源：原始論文 Table 2。）
    sha256: 806e6f4d25c74c98ba7b96df9085d2c0b61b93cd719ee1c416cf1a275b0bdd9b
- id: c19
  role: evaluation
  text: 論文沒討論的 trade-off：離散 judge 的排錯次數是 0/100，它從不把錯的排在對的前面，只是不表態；連續 verifier 消除平手的代價，是被迫每次都表態，其中二三成表錯了
  source_quotes:
  - "不過最右欄有個論文沒討論的 trade-off：**離散 judge 的排錯次數是 0/100**。它從不把錯的排在對的前面，它只是不表態。連續 verifier 消除平手的代價，是被迫每次都表態，其中二三成表錯了。"
  qualifiers:
  - text: 表錯的實際次數是 verifier（G=5）31/100、verifier（G=20）23/100
    source_quote: "| Verifier（連續，G=5） | 69/100 | 0/100 | 31/100 |"
  anchor_type: 部落格判斷
  comparison_target: 同一任務上的離散 judge（G=5）
  importance: 19
  status: normal
- id: c20
  role: evaluation
  text: 用「平手算半分」計分，judge 是 56、verifier（G=5）是 69、verifier（G=20）是 77，verifier 確實還是勝出；但如果下游流程是「平手就交給人審」，judge 的行為反而更安全，論文沒有提這一層
  source_quotes:
  - "用「平手算半分」計分的話，Judge = 12 + 88×0.5 = 56，Verifier G=5 = 69，G=20 = 77，verifier 確實還是勝出，結論站得住腳。但如果你的下游流程是「平手就交給人審」，judge 的行為反而更安全。論文沒有提這一層。"
  anchor_type: 部落格考證
  comparison_target: 同一任務上的離散 judge（G=5），平手算半分
  importance: 20
  status: normal
```
