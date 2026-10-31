---
id: verifier-results-how-to-read
title: LLM-as-a-Verifier 的實驗數字只有「只改一個變因」的對照能歸功給方法：主表扣掉 harness 差異只剩幾個百分點，最乾淨的證據在機器人，進度預警的說法則被自己的統計否定
type_hint: 判斷
context_type: bound_to_source
sources:
- article: llm-as-a-verifier
  article_title: "LLM 打分數老是平手？LLM-as-a-Verifier 改讀機率分佈"
  url: https://datasciocean.com/paper-intro/llm-as-a-verifier/
  sections:
  - LLM 打分數老是平手，是 argmax 把資訊丟掉了
  - 值得解決嗎？看 oracle 的落差
  - 核心公式：用期望值取代 argmax
  - 實驗結果：怎麼讀比讀到什麼更重要
  - 主結果表要分兩半讀
  - 最強的結果不在主表，在機器人上
  - 進度追蹤：論文講過頭的地方
  - 準則拆解 C：對付評分標準本身不合理
  - 結論
  first_appearance: true
parent: null
related:
- verifier-expected-value-vs-argmax
- verifier-three-knobs-g-k-c
- ppt-pivot-tournament
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 主表只有「同一候選池」那一半能歸功給 verifier，而機器人這一列是同一個模型只改解碼方式，是最乾淨的因果證據；論文說這個分數可以兼作進度預警，但它自己的統計（成功與失敗軌跡只差 0.079）並不支持
  source_quotes:
  - "小結：主表只有「同一候選池」那一半能歸功給 verifier，而機器人這一列是同一個模型只改解碼方式，是最乾淨的因果證據。"
  - "另外，論文說這個分數可以兼作進度預警，但它自己的統計（成功與失敗軌跡只差 0.079）並不支持，用的時候要打折扣。"
  qualifiers:
  - text: 機器人那一列的保留：論文完全沒有解釋專門訓練的機器人 reward model 為什麼會在自己的領域輸掉
    source_quote: "論文完全沒有解釋，為什麼專門訓練的機器人 reward model 會在自己的領域輸掉。相關那節只列數字，沒有任何分析。"
  - text: 機器人那一列的保留：RoboRewardBench 是共同作者也掛名的 RoboReward 論文提出的，被比較的 RoboReward-8B 正是那篇的模型，論文沒揭露這層利益關係
    source_quote: "另外有一層利益關係論文自己沒揭露：RoboRewardBench 是共同作者也掛名的 RoboReward 論文提出的，被比較的 RoboReward-8B 正是那篇的模型。"
  anchor_type: 部落格判斷
  comparison_target: 成功軌跡與失敗軌跡的 VOC（verifier 分數與步驟順序的等級相關）
  importance: 1
  status: normal
- id: c2
  role: context
  text: LLM-as-a-Verifier（arXiv 2607.05391v2，Stanford / UC Berkeley / NVIDIA）讓 LLM 替另一個 LLM 的輸出打分數時，不取分數 token 機率最高的那一個（argmax），改算期望值（把每個分數乘上它的機率再加總），分數從離散整數變成連續實數；再配一個排名演算法 PPT（用成對比較，從 N 條候選裡挑出最好的一條），橫跨程式、機器人、醫療三個領域做了實驗
  source_quotes:
  - "（arXiv 2607.05391v2，Stanford / UC Berkeley / NVIDIA）"
  - "但標準做法只取機率最高的那一個（這個動作叫 argmax），其餘全丟。"
  - "改法很單純：不取 argmax，改算**期望值**（把每個分數乘上它的機率再加總），分數從離散整數變成連續實數。作者把這個改動加上重複取樣、準則拆解，包成一個叫 LLM-as-a-Verifier 的框架，再配一個新的排名演算法 PPT（用成對比較，從 N 條候選裡挑出最好的一條），橫跨程式、機器人、醫療三個領域做了實驗。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 2
  status: normal
- id: c3
  role: context
  text: 四個 benchmark 用完全相同的流程：生成策略對每題產生 N 條候選，verifier 用 PPT 兩兩評分，選出正規化分數最高者提交；超參數全程固定在 G=20（分數 token 數）、K=8（重複次數）、C=3（準則數），沒有針對個別 benchmark 調過；完全 training-free，沒有任何領域 fine-tuning
  source_quotes:
  - "四個 benchmark 用完全相同的流程：生成策略對每題產生 N 條候選 → verifier 用 PPT 兩兩評分 → 選出正規化分數最高者提交。"
  - "**超參數全程固定**在 G=20、K=8、C=3，沒有針對個別 benchmark 調過。"
  - "**完全 training-free**，四個 benchmark 共用同一個框架，沒有任何領域 fine-tuning（針對特定領域再訓練）。"
  - "準則總數（主實驗 C=3）"
  - "重複次數（主實驗 K=8）"
  - "取用的分數 token 數（下面的例子用 5，主實驗 G=20）"
  qualifiers:
  - text: C=3 的三個準則明說是為 code-agent 軌跡設計的，機器人和醫療的實驗也宣稱用同一組，但換到別的領域怎麼套用，論文沒有回答
    source_quote: "**換到別的領域怎麼套用，也沒回答。** 這三個準則明說是為 code-agent 軌跡設計的，但機器人和醫療的實驗也宣稱用同一組。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 3
  status: normal
- id: c4
  role: context
  text: oracle 是理想的挑選者，每次都能從候選裡挑中對的那條；Pass@1 是每題只交一次答案的成功率。Terminal-Bench V2 上 98.9% 是放任 K 一路增大時的 oracle 覆蓋率上限（理論天花板），主實驗表格裡的 92.1% 則是實際候選池只有 N=5 時的 oracle，後者才是這套系統真正在爭取的空間
  source_quotes:
  - "oracle（理想的挑選者）每次都能從候選裡挑中對的那條，對照組是 Pass@1（每題只交一次答案的成功率）。"
  - "這裡的 98.9% 是**放任 K 一路增大**時的 oracle 覆蓋率上限，後面主實驗表格裡那個 92.1% 則是**實際候選池只有 N=5** 時的 oracle Pass@N。兩個數字量的不是同一件事：前者是理論天花板，後者才是這套系統真正在爭取的空間。"
  - "Terminal-Bench V2 的解出率可以到 **98.9%**"
  qualifiers:
  - text: 98.9% 這個上限的設定，是光靠重複抽樣得到的 oracle 解出率
    source_quote: "光靠重複抽樣就能把 Terminal-Bench V2 解到 98.9%"
    source: figure_caption
  anchor_type: 部落格考證
  comparison_target: K 一路增大時的 oracle 上限（98.9%）與 N=5 候選池的 oracle（92.1%）
  importance: 4
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/figure5.png
    article: llm-as-a-verifier
    src: figure5.png
    caption: 圖 1 — 如果有一個完美的 verifier，光靠重複抽樣就能把 Terminal-Bench V2 解到 98.9%。（來源：原始論文 Figure 5。）
    sha256: 232e4eb335b569377f0a388da6c0a7a374425d34663c5f11434401d3b8851f29
- id: c5
  role: evaluation
  text: 主結果表要分兩半讀：左半是其他模型的成績，用的是不同的 harness、不同的抽樣設定，是蘋果比橘子；右半是同一個候選池上的 Pass@1 → Oracle → Ours，同一批候選、同一個生成器，唯一變因是「怎麼挑」，這才是 verifier 的功勞
  source_quotes:
  - "這張表要分兩半讀。左半是其他模型的成績，用的是不同的 harness、不同的抽樣設定，是蘋果比橘子；右半是同一個候選池上的 Pass@1 → Oracle → Ours，是完全可控的對照，這才是 verifier 的功勞。"
  - "右半才是誠實的證據，因為同一批候選、同一個生成器，唯一變因是「怎麼挑」："
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 5
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/table3.png
    article: llm-as-a-verifier
    src: table3.png
    caption: 圖 8 — 主結果表。左半和右半是完全不同性質的比較，混著讀會得到錯誤結論。（來源：原始論文 Table 3。）
    sha256: 004aba73c2f9c91766c7afa15f146d9adaadbc7f29ff6fb88f8efea4890ff5e0
- id: c6
  role: evidence
  text: 同一候選池上 Pass@1 → Ours：Terminal-Bench V2 是 83.1% → 86.5%（+3.4pp），SWE-Bench Verified 是 76.1% → 78.2%（+2.1pp），MedAgentBench 是 70.2% → 73.3%（+3.1pp）；這是扣掉 harness 差異之後 verifier 真正的貢獻
  source_quotes:
  - "| Terminal-Bench V2 | 83.1% → 86.5% | **+3.4pp** | 9.0pp | 38% |"
  - "| SWE-Bench Verified | 76.1% → 78.2% | **+2.1pp** | 8.3pp | 25% |"
  - "| MedAgentBench | 70.2% → 73.3% | **+3.1pp** | 4.8pp | 65% |"
  - "右半才是誠實的證據，因為同一批候選、同一個生成器，唯一變因是「怎麼挑」："
  qualifiers:
  - text: SWE-Bench 的候選池是異質的：N=3 是從三個不同模型各抽一條，Pass@1 是三模型平均，跟其他列不可直接比較
    source_quote: "**SWE-Bench 的候選池是異質的。** N=3 是從三個不同模型各抽一條，Pass@1 是三模型平均，verifier 的任務其實變成「跨模型家族挑最好」。這是更有價值的應用場景（模型路由），但也讓它跟其他列不可直接比較。"
  anchor_type: 部落格考證
  comparison_target: 同一候選池、同一生成器的 Pass@1
  importance: 6
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/table3.png
    article: llm-as-a-verifier
    src: table3.png
    caption: 圖 8 — 主結果表。左半和右半是完全不同性質的比較，混著讀會得到錯誤結論。（來源：原始論文 Table 3。）
    sha256: 004aba73c2f9c91766c7afa15f146d9adaadbc7f29ff6fb88f8efea4890ff5e0
- id: c7
  role: evaluation
  text: 實際候選池上可搶的 oracle 空間（oracle 減 Pass@1）不大（Terminal-Bench V2 9.0pp、SWE-Bench Verified 8.3pp、MedAgentBench 4.8pp），verifier 兌現了四分之一到三分之二（38%、25%、65%），跟「把 oracle 的巨大潛力兌現」的敘事還有距離
  source_quotes:
  - "| Terminal-Bench V2 | 83.1% → 86.5% | **+3.4pp** | 9.0pp | 38% |"
  - "| SWE-Bench Verified | 76.1% → 78.2% | **+2.1pp** | 8.3pp | 25% |"
  - "| MedAgentBench | 70.2% → 73.3% | **+3.1pp** | 4.8pp | 65% |"
  - "這個幅度不難看，但實際候選池上可搶的 oracle 空間也就 5 到 9pp，兌現了四分之一到三分之二，跟「把 oracle 的巨大潛力兌現」的敘事還有距離。"
  qualifiers:
  - text: SWE-Bench 的候選池是異質的（N=3，三個不同模型各抽一條），跟其他列不可直接比較
    source_quote: "但也讓它跟其他列不可直接比較。"
  anchor_type: 部落格考證
  comparison_target: 同一候選池的 oracle 與 Pass@1 之間的落差
  importance: 7
  status: normal
- id: c8
  role: evaluation
  text: 「SOTA」宣稱混雜了 harness 差異：Terminal-Bench V2 的 86.5% 是 GPT-5.5 加上 Capy harness 加上 N=5 抽樣加上 verifier，而對照的 84.7% 是 GPT-5.5 加上另一個 harness；三個變因不同，把差距全歸給 verifier 不成立，乾淨的比較是 83.1% → 86.5%
  source_quotes:
  - "**「SOTA」宣稱混雜了 harness 差異。** 86.5% 是 GPT-5.5 加上 Capy harness 加上 N=5 抽樣加上 verifier，而 84.7% 是 GPT-5.5 加上另一個 harness。三個變因不同，把差距全歸給 verifier 不成立，乾淨的比較是 83.1% → 86.5%。"
  - "| Terminal-Bench V2 | GPT-5.5 (84.7%) |"
  anchor_type: 部落格判斷
  comparison_target: 主表左半 Terminal-Bench V2 的 GPT-5.5（另一個 harness，84.7%）；乾淨的對照是同一候選池的 Pass@1（83.1%）
  importance: 8
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/table3.png
    article: llm-as-a-verifier
    src: table3.png
    caption: 圖 8 — 主結果表。左半和右半是完全不同性質的比較，混著讀會得到錯誤結論。（來源：原始論文 Table 3。）
    sha256: 004aba73c2f9c91766c7afa15f146d9adaadbc7f29ff6fb88f8efea4890ff5e0
- id: c9
  role: context
  text: 機器人的 benchmark RoboRewardBench 量的是 preference accuracy（偏好準確率）；比較的對象包括能看影像的語言模型（VLM）與專門訓練的機器人 reward model
  source_quotes:
  - "在機器人的 benchmark RoboRewardBench 上，量的是 preference accuracy（偏好準確率）。下表的 VLM 指能看影像的語言模型。"
  - "| LLM-as-a-Judge（同一個 VLM，離散） | 70.8% |"
  - "一個零訓練的框架打贏兩個專門訓練的機器人 reward model。"
  anchor_type: 背景說明
  importance: 9
  status: normal
- id: c10
  role: evidence
  text: RoboRewardBench 上，LLM-as-a-Verifier 是 87.4%，RoboReward-8B（訓練過，約 4.5 萬 episode）是 81.4%，Robometer-4B（訓練過，約 100 萬筆比較）是 78.8%，TOPReward 是 74.7%，同一個 VLM 的離散 LLM-as-a-Judge 是 70.8%
  source_quotes:
  - "| **LLM-as-a-Verifier（本方法）** | **87.4%** |"
  - "| RoboReward-8B（訓練過，約 4.5 萬 episode） | 81.4% |"
  - "| Robometer-4B（訓練過，約 100 萬筆比較） | 78.8% |"
  - "| TOPReward | 74.7% |"
  - "| LLM-as-a-Judge（同一個 VLM，離散） | 70.8% |"
  qualifiers:
  - text: RoboRewardBench 是共同作者也掛名的 RoboReward 論文提出的，被比較的 RoboReward-8B 正是那篇的模型，論文沒揭露這層利益關係
    source_quote: "另外有一層利益關係論文自己沒揭露：RoboRewardBench 是共同作者也掛名的 RoboReward 論文提出的，被比較的 RoboReward-8B 正是那篇的模型。"
  anchor_type: 實驗結果
  comparison_target: 兩個專門訓練的機器人 reward model、TOPReward，以及同一個 VLM 的離散 judge
  importance: 10
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/table4.png
    article: llm-as-a-verifier
    src: table4.png
    caption: 圖 9 — 同一個模型，只改解碼方式，準確率從 70.8% 跳到 87.4%，還贏過兩個專門訓練的機器人 reward model。（來源：原始論文 Table 4。）
    sha256: d194fa96490f88da81a1200347e2116e5d2141b1a6c442963df6f062b3d28c5c
- id: c11
  role: evaluation
  text: 87.4% 和 70.8% 是同一個 Qwen 3.6 35B，唯一差別是離散 argmax 對上連續期望值；這 16.6pp 是全篇最大、也最能歸因給方法本身的數字，完全沒有 harness 混雜
  source_quotes:
  - "**同一個模型的乾淨對照。** 87.4% 和 70.8% 是同一個 Qwen 3.6 35B，唯一差別是離散 argmax 對上連續期望值。這 16.6pp 是全篇最大、也最能歸因給方法本身的數字，完全沒有 harness 混雜。"
  anchor_type: 部落格判斷
  comparison_target: 同一個 Qwen 3.6 35B 的離散 argmax judge（70.8%）
  importance: 11
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/table4.png
    article: llm-as-a-verifier
    src: table4.png
    caption: 圖 9 — 同一個模型，只改解碼方式，準確率從 70.8% 跳到 87.4%，還贏過兩個專門訓練的機器人 reward model。（來源：原始論文 Table 4。）
    sha256: d194fa96490f88da81a1200347e2116e5d2141b1a6c442963df6f062b3d28c5c
- id: c12
  role: evaluation
  text: 一個零訓練的框架打贏兩個專門訓練的機器人 reward model；而且輸入從文字換成多幀影片，方法完全不用改；把 RoboReward-8B 改用連續公式解碼的附帶結果也說明，這套解碼方式可以直接加在既有的 reward model 上，不是非得從頭換掉
  source_quotes:
  - "一個零訓練的框架打贏兩個專門訓練的機器人 reward model。"
  - "**跨模態。** 輸入從文字換成多幀影片，方法完全不用改。"
  - "也就是說，這套解碼方式可以直接加在既有的 reward model 上，不是非得從頭換掉。"
  qualifiers:
  - text: 論文完全沒有解釋，為什麼專門訓練的機器人 reward model 會在自己的領域輸掉，相關那節只列數字
    source_quote: "論文完全沒有解釋，為什麼專門訓練的機器人 reward model 會在自己的領域輸掉。相關那節只列數字，沒有任何分析。"
  - text: RoboRewardBench 是共同作者也掛名的 RoboReward 論文提出的，被比較的 RoboReward-8B 正是那篇的模型，論文沒揭露這層利益關係
    source_quote: "另外有一層利益關係論文自己沒揭露：RoboRewardBench 是共同作者也掛名的 RoboReward 論文提出的，被比較的 RoboReward-8B 正是那篇的模型。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 12
  status: normal
- id: c13
  role: evidence
  text: 把 RoboReward-8B 的輸出改用連續公式解碼，與人類標註的 MAE（平均絕對誤差，越小越接近人類）從 1.11 降到 0.72
  source_quotes:
  - "還有一個附帶結果同樣值得記住：把 RoboReward-8B 的輸出改用連續公式解碼，與人類標註的 MAE（平均絕對誤差，越小越接近人類）從 **1.11 降到 0.72**。也就是說，這套解碼方式可以直接加在既有的 reward model 上，不是非得從頭換掉。"
  anchor_type: 實驗結果
  comparison_target: RoboReward-8B 原本的解碼方式
  importance: 13
  status: normal
- id: c14
  role: context
  text: 論文定義了 Value-Order Correlation（VOC），把「步驟的時間順序」跟「verifier 對該步驟前綴的分數」算 Spearman 等級相關（衡量兩組排序有多一致，1 代表完全同向）；分數完美隨步驟遞增，VOC 就趨近 1
  source_quotes:
  - "論文定義了 Value-Order Correlation（VOC），把「步驟的時間順序」跟「verifier 對該步驟**前綴**的分數」算 Spearman 等級相關（衡量兩組排序有多一致，1 代表完全同向）。分數完美隨步驟遞增，VOC 就趨近 1。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 14
  status: normal
- id: c15
  role: evidence
  text: 論文主張 verifier 在停滯或走向失敗的軌跡上分數大致持平，因此同一個分數可以兼作進度量測與早期預警
  source_quotes:
  - "論文主張 verifier 在停滯或走向失敗的軌跡上分數**大致持平**，因此同一個分數可以兼作進度量測與早期預警。"
  qualifiers:
  - text: 論文自己的統計數字不支持這個說法：500 條 Terminal-Bench V2 軌跡上，成功軌跡的 VOC 是 0.848，失敗軌跡是 0.769，失敗軌跡的分數也在隨時間穩定上升
    source_quote: "但它自己的統計數字不支持這個說法。"
  - text: 0.769 是相當高的正相關，失敗軌跡的分數也在隨時間穩定上升，離「持平」差得很遠
    source_quote: "0.769 是相當高的正相關，代表**失敗軌跡的分數也在隨時間穩定上升**，離「持平」（VOC ≈ 0）差得很遠。"
  anchor_type: 原作者解讀
  importance: 15
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/figure8.png
    article: llm-as-a-verifier
    src: figure8.png
    caption: 圖 10 — 單一任務上的對照：成功軌跡分數穩定爬升，失敗軌跡在裝錯套件、磁碟爆掉之後一路低迷。（來源：原始論文 Figure 8。）
    sha256: 3623722caa1c30ebdf1188b4e33ef3fab90b000a6fecdbb8bab5b963bf467a55
- id: c16
  role: evidence
  text: 在 500 條 Terminal-Bench V2 軌跡上，成功軌跡的 VOC 是 0.848 ± 0.012，失敗軌跡是 0.769 ± 0.016，落差只有 0.079
  source_quotes:
  - "但它自己的統計數字不支持這個說法。在 500 條 Terminal-Bench V2 軌跡上："
  - "| 成功 | 上升 ↗ | 0.848 ± 0.012 |"
  - "| 失敗 | 持平 → | 0.769 ± 0.016（幾乎一樣在升） |"
  - "| **落差** |  | **+0.079** |"
  anchor_type: 實驗結果
  comparison_target: 成功軌跡與失敗軌跡的 VOC
  importance: 16
  status: normal
- id: c17
  role: evaluation
  text: 0.769 是相當高的正相關，代表失敗軌跡的分數也在隨時間穩定上升，離「持平」（VOC ≈ 0）差得很遠；用 0.079 的落差做執行中的即時預警，鑑別力其實很弱
  source_quotes:
  - "0.769 是相當高的正相關，代表**失敗軌跡的分數也在隨時間穩定上升**，離「持平」（VOC ≈ 0）差得很遠。"
  - "用 0.079 的落差做執行中的即時預警，鑑別力其實很弱。"
  anchor_type: 部落格判斷
  comparison_target: 「持平」對應的 VOC ≈ 0；成功軌跡的 VOC
  importance: 17
  status: normal
- id: c18
  role: evaluation
  text: 論文拿來當敘事主軸的是單一任務的單一案例（成功軌跡分數持續上升到約 1.0，失敗軌跡在不必要地裝 torchvision、磁碟空間耗盡之後一路偏低），而不是 500 條軌跡的統計，也沒討論後者為什麼落差這麼小
  source_quotes:
  - "| 成功 | Read model.py → Install g++ → Install CPU-only torch → Update hidden_dim → DONE | 持續上升 → ~1.0 |"
  - "| 失敗 | 不必要地裝 torchvision → 磁碟空間耗盡 → 編譯錯誤 | 一路偏低 |"
  - "上表是 500 條軌跡的統計，論文選擇用前者當敘事主軸，卻沒討論後者為什麼落差這麼小。"
  - "圖 10 是單一任務的單一案例"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 18
  status: normal
  figures:
  - file: figures/llm-as-a-verifier/figure8.png
    article: llm-as-a-verifier
    src: figure8.png
    caption: 圖 10 — 單一任務上的對照：成功軌跡分數穩定爬升，失敗軌跡在裝錯套件、磁碟爆掉之後一路低迷。（來源：原始論文 Figure 8。）
    sha256: 3623722caa1c30ebdf1188b4e33ef3fab90b000a6fecdbb8bab5b963bf467a55
```
