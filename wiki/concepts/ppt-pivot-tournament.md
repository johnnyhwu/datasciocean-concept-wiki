---
id: ppt-pivot-tournament
title: PPT 用環狀比較便宜地挑出 pivot，再把預算集中在頂端；但它的省錢效果要 N 夠大才明顯，而主實驗的 N 其實很小
type_hint: 方法
context_type: bound_to_source
sources:
- article: llm-as-a-verifier
  article_title: "LLM 打分數老是平手？LLM-as-a-Verifier 改讀機率分佈"
  url: https://datasciocean.com/paper-intro/llm-as-a-verifier/
  sections:
  - LLM 打分數老是平手，是 argmax 把資訊丟掉了
  - judge 與 verifier，以及 scoring prompt 怎麼寫
  - 正規化與 Bradley–Terry：把分數差變成勝率
  - PPT：從 N 條候選裡挑最好的那條
  - Ring pass：一石二鳥
  - Pivot 選擇與最終選出
  - 預算對準確率
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
  text: PPT 用環狀比較便宜地挑出 pivot，再集中預算在頂端；但它的省錢效果要 N 夠大才明顯，主實驗的 N 其實很小
  source_quotes:
  - "小結：PPT 用環狀比較便宜地挑出 pivot，再集中預算在頂端；但它的省錢效果要 N 夠大才明顯，主實驗的 N 其實很小。"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: LLM-as-a-Verifier（arXiv 2607.05391v2，Stanford / UC Berkeley / NVIDIA）讓 LLM 替軌跡打分數時，不取分數 token 機率最高的那一個，改算期望值，得到連續分數；它的 prompt 一次塞兩個候選解對照著評，再用 Bradley–Terry（一個把實力差距轉成勝率的模型）把兩條的分數差轉成「誰贏的機率」。verifier 一次只能比兩條，但實際任務是從 N 條裡選最好的，PPT（Probabilistic Pivot Tournament）就是負責這件事的排名演算法
  source_quotes:
  - "（arXiv 2607.05391v2，Stanford / UC Berkeley / NVIDIA）"
  - "改法很單純：不取 argmax，改算**期望值**（把每個分數乘上它的機率再加總），分數從離散整數變成連續實數。"
  - "**一次 prompt 塞兩個候選解，對照著評。**"
  - "接著把分數差轉成偏好機率，用的是 Bradley–Terry（一個把實力差距轉成勝率的模型）。"
  - "verifier 一次只能比兩條，但實際任務是從 N 條裡選最好的。這一節是 PPT。"
  - "Probabilistic Pivot Tournament（PPT）"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 2
  status: normal
- id: c3
  role: context
  text: 完整循環賽（每條候選都和其他每一條各比一次）的比較次數大約是 N×N 的量級，記作 O(N²)；以 N=20 為例是 190 對，每一對要 C×K=24 次 LLM 呼叫，共 4,560 次
  source_quotes:
  - "完整循環賽（每條候選都和其他每一條各比一次）的比較次數大約是 N×N 的量級，記作 O(N²)。以 N = 20 為例：C(20,2)（20 條裡挑 2 條的配法）= 190 對，190 × 24 = 4,560 次 LLM 呼叫。"
  - "而是**取得每個 R 所需的 LLM 呼叫成本**，每一對就是 \\( C \\times K \\) = 24 次。"
  anchor_type: 數學推導
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: PPT 的核心想法是每條候選只跟一小群 pivot（當作比較基準的候選）比，成本降到 O(Nk)（k 是 pivot 的數量）；但真正的設計重點不是「用 pivot 省錢」，而是怎麼用一個便宜的前置步驟，找出值得當 pivot 的候選
  source_quotes:
  - "核心想法是每條候選只跟一小群 pivot（當作比較基準的候選）比，成本降到 O(Nk)（大約 N×k 次；這裡的 k 是 pivot 的數量，跟前面重複評估的 K 不是同一個東西）。但真正的設計重點不是「用 pivot 省錢」，那很直觀，而是**怎麼用一個便宜的前置步驟，找出值得當 pivot 的候選**。"
  anchor_type: 部落格判斷
  importance: 4
  status: normal
- id: c5
  role: evaluation
  text: PPT 是全篇唯一算得上演算法新貢獻的部分
  source_quotes:
  - "Probabilistic Pivot Tournament（PPT）是全篇唯一算得上演算法新貢獻的部分。"
  anchor_type: 部落格判斷
  importance: 5
  status: normal
- id: c6
  role: mechanism
  text: PPT 分五個階段：N 條候選；隨機環狀比較 N 場（ring pass），得到粗略排名並消除位置偏誤；取前 k 名為 pivot 集合；非 pivot 對 pivot、加上 pivot 彼此互比；累積每條的平均勝分，取最高者
  source_quotes:
  - "**Candidates**：N 條候選。"
  - "**Ring pass**：隨機環狀比較 N 場，得到粗略排名，並消除位置偏誤。"
  - "**Pivot select**：取前 k 名為 pivot 集合 P。"
  - "**Pivot rounds**：非 pivot 對 pivot，加上 pivot 彼此互比。"
  - "**Selection**：累積"
  anchor_type: 設計參數
  importance: 6
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/figure6.png
    article: llm-as-a-verifier
    src: figure6.png
    caption: 圖 6 — PPT 的五個階段，重點在第二階段那圈環狀比較。（來源：原始論文 Figure 6。）
    sha256: 212006321f0e4e6a84786f3ea0061649e54e56bc9f9576fa099104ae47db930e
- id: c7
  role: mechanism
  text: Ring pass 把 N 條候選隨機排成一個環，只比較環上相鄰的 N 對，同時做到兩件事：只花 N 場就能便宜取得粗略排名；每條候選恰好當一次 Trajectory A、當一次 Trajectory B，LLM 對這兩個位置的系統性偏好在期望值上互相抵消（實驗設計裡的平衡設計，counterbalancing）
  source_quotes:
  - "Ring pass 把 N 條候選隨機排成一個環，只比較環上相鄰的 N 對。"
  - "這個結構同時做到兩件事。第一是**便宜取得粗略排名**，只花 N 場就能大致看出誰強誰弱。第二是**消除位置偏誤**：LLM 對 prompt 裡「Trajectory A」和「Trajectory B」這兩個位置常有系統性偏好，這是已知問題。環狀結構讓每條候選恰好當一次 A、當一次 B，偏好在期望值上互相抵消。這其實就是實驗設計裡的平衡設計（counterbalancing）"
  qualifiers:
  - text: 「在期望值上抵消」只在偏誤是加性常數的時候嚴格成立；偏誤跟內容有關時（例如只在兩條差不多時才偏好 A），環狀結構不保證能抵消
    source_quote: "另外，「在期望值上抵消」只在**偏誤是加性常數**的時候嚴格成立。如果偏誤跟內容有關（例如只在兩條差不多時才偏好 A），環狀結構不保證能抵消。"
  anchor_type: 設計參數
  importance: 7
  status: normal
- id: c8
  role: evaluation
  text: 位置偏誤能抵消的前提（偏誤是加性常數），論文沒討論，也沒有做「有 ring pass vs 無 ring pass」的對照實驗
  source_quotes:
  - "論文沒討論這個前提，也沒有做「有 ring pass vs 無 ring pass」的對照實驗。"
  anchor_type: 部落格判斷
  importance: 8
  status: normal
- id: c9
  role: mechanism
  text: 每場比較兩邊都更新：p 是 i 贏 j 的機率，i 的累積勝分加 p、j 的加 (1 − p)，兩邊的場次各加 1；環狀比較跑完後每條都比過 2 場，按「累積勝分除以場次」排序取前 k 名當 pivot，沒有額外規則，純粹 top-k
  source_quotes:
  - "每場比較兩邊都更新（\\( p \\) 是 \\( i \\) 贏 \\( j \\) 的機率）："
  - "`w_i += p`、`c_i += 1`（\\( w_i \\) 是 win mass，累積的勝分；\\( c_i \\) 是第 i 條累計比過的場次"
  - "`w_j += (1 − p)`、`c_j += 1`（兩者相加恰為 1）"
  - "環狀結構讓跑完之後每條的 \\( c_i \\) 都是 2，然後按 \\( w_i/c_i \\) 排序取前 k 名當 pivot，沒有額外規則，純粹 top-k。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: 挑表現好的當 pivot，是因為目標是選出最好的那條，需要細分的是頂端誰最好；pivot 挑到明顯很差的候選，所有比較都只會得到「大家都比它好」這種沒有鑑別力的結果。這跟 quickselect 選 pivot 的思路一樣：資源該集中在可能是答案的那一區
  source_quotes:
  - "為什麼挑表現好的當 pivot？因為目標是選出最好的那條，需要細分的是頂端誰最好，不是墊底誰比較不爛。如果 pivot 挑到明顯很差的候選，所有比較都只會得到「大家都比它好」這種沒有鑑別力的結果。這跟 quickselect 選 pivot 的思路一樣：不需要完全排序，只要找最大者，資源就該集中在可能是答案的那一區。"
  anchor_type: 部落格推論
  importance: 10
  status: normal
- id: c11
  role: evaluation
  text: 論文完全沒分析的疑慮：pivot 是根據 ring pass 裡僅僅兩場比較選出來的，樣本量極小；真正最好的候選若兩場都碰到強對手，可能直接落榜、進不了 pivot 集合，論文沒有分析這個「好候選被誤篩掉」的機率
  source_quotes:
  - "一個論文完全沒分析的疑慮：**pivot 是根據 ring pass 裡僅僅兩場比較選出來的，樣本量極小。** 如果某條真正最好的候選在 ring pass 中運氣不好、兩場都碰到強對手，它的 \\( w_i/c_i \\) 就會偏低，可能直接落榜、進不了 pivot 集合。論文沒有分析這個「好候選被誤篩掉」的機率。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 11
  status: normal
- id: c12
  role: mechanism
  text: 總比較次數是 ring pass 的 N 對、非 pivot 對每個 pivot 的 k(N−k) 對、pivot 彼此互比的 C(k,2) 對三項相加；N=20、k=5 時是 20 + 75 + 10 = 105 對，對照循環賽 190 對，省約 45%
  source_quotes:
  - "接著比兩類配對：非 pivot 對每個 pivot（\\( (N-k)\\times k \\) 對），以及 pivot 彼此互比（\\( C(k,2) \\) 對）。後者是必要的，因為最後還得在 pivot 之間分高下。三項加起來，就是總比較次數："
  - "N=20, k=5 → 20 + 75 + 10 = 105 對，對照循環賽 190 對，省約 45%。"
  qualifiers:
  - text: 主實驗的 N 只有 3 到 5，C(5,2)=10 對，PPT 幾乎省不了什麼
    source_quote: "主實驗的 N 只有 3 到 5，C(5,2)=10 對，PPT 幾乎省不了什麼。"
  anchor_type: 數學推導
  comparison_target: 同樣 N=20 的完整循環賽（190 對）
  importance: 12
  status: normal
- id: c13
  role: mechanism
  text: 最後選「累積勝分除以場次」最高的那條；要除以場次，是因為 pivot 跟所有人比、參與的場次遠多於非 pivot，只看累積勝分的話，pivot 光靠場次多就會累積出比較大的數字
  source_quotes:
  - "最終選出是 \\( i^* = \\arg\\max_i w_i / c_i \\)。為什麼要除以 \\( c_i \\)？因為 pivot 參與的場次遠多於非 pivot（pivot 跟所有人比，非 pivot 只跟 k 個比），只看 \\( w_i \\) 的話，pivot 光靠場次多就會累積出比較大的數字。除以 \\( c_i \\) 換算成「平均每場贏多少」才公平。"
  anchor_type: 設計參數
  importance: 13
  status: normal
- id: c14
  role: context
  text: 預算對準確率的實驗設定是 N=20 候選、89 題、Terminus-2 harness（驅動 agent 的那層腳手架），候選數跟主結果表不同（主實驗的 N 只有 3 到 5），這裡的 pass@1 跟主結果表的 Pass@1 不是同一個設定；表裡的基準線 V1 是論文拿來對照的前一代排名方法，論文全文沒有解釋 V1 怎麼運作
  source_quotes:
  - "設定是 N=20 候選、89 題、Terminus-2 harness，候選數跟主結果表不同（主實驗的 N 只有 3 到 5），所以這裡的 pass@1 跟主結果表的 Pass@1 不是同一個設定，不要直接拿來比。harness 指的是驅動 agent 的那層腳手架"
  - "表裡的 V1 是論文拿來對照的前一代排名方法，`1N` 到 `7N` 指的是它花掉的比較預算倍率。要先說清楚的是，**論文全文沒有解釋 V1 怎麼運作**，只把它當基準線用。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 14
  status: normal
- id: c15
  role: evidence
  text: N=20 候選時，PPT k=1 用 2,570 個查詢配對、準確率 65.83%；k=5 用 6,609 對、66.27%；k=9 用 9,630 對、67.13%；完整循環賽用 13,111 對、67.42%；pass@1 是 52.64%
  source_quotes:
  - "| pass@1 | — | 52.64% |"
  - "| PPT k=1 | 2,570 | 65.83% |"
  - "| PPT k=5 | 6,609 | 66.27% |"
  - "| PPT k=9 | 9,630 | 67.13% |"
  - "| Full Round-Robin | 13,111 | 67.42% |"
  qualifiers:
  - text: 這組結果是 N=20 候選、89 題、Terminus-2 harness 的設定，跟主結果表不同，pass@1 不要直接拿來跟主結果表比
    source_quote: "設定是 N=20 候選、89 題、Terminus-2 harness，候選數跟主結果表不同（主實驗的 N 只有 3 到 5），所以這裡的 pass@1 跟主結果表的 Pass@1 不是同一個設定，不要直接拿來比。"
  anchor_type: 實驗結果
  comparison_target: 同設定下的完整循環賽（Full Round-Robin）與 pass@1
  importance: 15
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/table9.png
    article: llm-as-a-verifier
    src: table9.png
    caption: 圖 7 — PPT 的預算與準確率權衡：k 愈大愈準，但報酬遞減得很快。（來源：原始論文 Table 9。）
    sha256: 9a5eaa260cd8851742fa2a62707165c1db7f9dc745fe2d0fcfdd4620701b6846
- id: c16
  role: evaluation
  text: k 愈大愈準，但報酬遞減得很快：k=1 到 k=9 只漲 1.3pp，預算卻變成將近 4 倍；k=9 已經逼近完整循環賽（67.13% vs 67.42%），預算省 27%
  source_quotes:
  - "k 愈大愈準但報酬遞減得很快（k=1 到 k=9 只漲 1.3pp，預算卻變成將近 4 倍）；k=9 已經逼近完整循環賽（67.13% vs 67.42%），預算省 27%。"
  qualifiers:
  - text: 這組結果是 N=20 候選、89 題、Terminus-2 harness 的設定，跟主結果表不同
    source_quote: "設定是 N=20 候選、89 題、Terminus-2 harness，候選數跟主結果表不同"
  anchor_type: 部落格考證
  comparison_target: PPT k=1；同設定下的完整循環賽
  importance: 16
  status: pending_author_confirmation
  figures:
  - file: figures/llm-as-a-verifier/table9.png
    article: llm-as-a-verifier
    src: table9.png
    caption: 圖 7 — PPT 的預算與準確率權衡：k 愈大愈準，但報酬遞減得很快。（來源：原始論文 Table 9。）
    sha256: 9a5eaa260cd8851742fa2a62707165c1db7f9dc745fe2d0fcfdd4620701b6846
- id: c17
  role: evaluation
  text: 基準線 V1 在 5N 預算之後不升反降（65.85% → 65.53%），PPT 則是單調上升，這點是站得住的
  source_quotes:
  - "| V1 (5N) | 7,000 | 65.85% |"
  - "| V1 (7N) | 9,800 | 65.53% |"
  - "基準線 V1 在 5N 之後不升反降，PPT 則是單調上升，這點是站得住的。"
  qualifiers:
  - text: 論文全文沒有解釋 V1 怎麼運作，只把它當基準線用
    source_quote: "要先說清楚的是，**論文全文沒有解釋 V1 怎麼運作**，只把它當基準線用。"
  - text: 這組結果是 N=20 候選、89 題、Terminus-2 harness 的設定，跟主結果表不同
    source_quote: "設定是 N=20 候選、89 題、Terminus-2 harness，候選數跟主結果表不同"
  anchor_type: 部落格判斷
  comparison_target: 前一代排名方法 V1 在不同預算倍率下的準確率
  importance: 17
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/table9.png
    article: llm-as-a-verifier
    src: table9.png
    caption: 圖 7 — PPT 的預算與準確率權衡：k 愈大愈準，但報酬遞減得很快。（來源：原始論文 Table 9。）
    sha256: 9a5eaa260cd8851742fa2a62707165c1db7f9dc745fe2d0fcfdd4620701b6846
- id: c18
  role: evaluation
  text: 論文沒給選 k 的方法論，只說 k 愈大愈好，但那樣就退化回循環賽了
  source_quotes:
  - "**論文沒給選 k 的方法論**，只說 k 愈大愈好，但那樣就退化回循環賽了。"
  anchor_type: 部落格判斷
  importance: 18
  status: normal
- id: c19
  role: evaluation
  text: O(N²) → O(Nk) 的漸進優勢要 N 夠大才明顯，N=20 還不到那個區間；而這張表的 N=20 是特別策展的設定，主實驗的 N 只有 3 到 5，PPT 幾乎省不了什麼，那些 SOTA 數字裡 PPT 的貢獻其實很有限
  source_quotes:
  - "O(N²) → O(Nk) 的漸進優勢要 N 夠大才明顯，N=20 還不到那個區間。"
  - "**這張表的 N=20 是特別策展的設定**，這點最重要。主實驗的 N 只有 3 到 5，C(5,2)=10 對，PPT 幾乎省不了什麼。換句話說，那些 SOTA 數字裡，PPT 的貢獻其實很有限。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 19
  status: normal
```
