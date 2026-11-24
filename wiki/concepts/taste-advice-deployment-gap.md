---
id: taste-advice-deployment-gap
title: 學生的建議讓 executor 成功率從 14.6% 升到 33.7%，但岔路口與候選是事先從同一任務的舊執行挖出來的：33.7% 能證明的是「建議品質夠好時，executor 會受益」，不是「這套方法能在新任務上直接提升成功率」
type_hint: 判斷
context_type: bound_to_source
sources:
- article: tasteful-agent
  article_title: "The Tasteful Agent 解析：用 agent 跑過的軌跡，量測並訓練 AI 的決策品味"
  url: https://datasciocean.com/paper-intro/tasteful-agent/
  sections:
  - agent 的中途決策沒人量過，這篇論文用跑過的軌跡免費出題
  - 同任務、同前綴，結果的差異才能歸給判斷
  - 設定：同一個模型，老師多看一段答案
  - 把學生的選擇寫成建議：executor 成功率 14.6% 升到 33.7%
  - 流程：學生只做二選一，建議交給另一個 agent
  - 結果：拿到上限的約 78%
  - 兩個實驗差在哪：有沒有 executor
  - 端到端的成功率還不能直接搬到新任務：部署缺口
  - 一句話總結
  - 蒸餾結果：沒見過的任務上，30.0% 升到 47.9%
  - parallel 與 detour 也決定了標籤怎麼來
  first_appearance: true
parent: null
related:
  - taste-fork-outcome-labels
  - taste-privileged-teacher-distillation
  - taste-bench-frontier-results
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 端到端實驗用的岔路口與候選，是事先從同一任務的舊執行挖出來的；所以 33.7% 能證明的是「建議品質夠好時，executor 會受益」，不是「這套方法能在新任務上直接提升成功率」
  source_quotes:
  - "端到端實驗用的岔路口與候選，是事先從同一任務的舊執行挖出來的"
  - "33.7% 能證明的是「建議品質夠好時，executor 會受益」，不是「這套方法能在新任務上直接提升成功率」。"
  anchor_type: 部落格判斷
  comparison_target: 沒有建議時的成功率 14.6%
  qualifiers:
  - text: 蒸餾與端到端的結果是正面的方向性訊號，但端到端用的是事先挖好的岔路口，還不能當作可以直接用在新任務上的證據
    source_quote: "蒸餾與端到端的結果（30.0% 到 47.9%、14.6% 到 33.7%）是正面的方向性訊號，但端到端用的是事先挖好的岔路口，所以還不能當作可以直接用在新任務上的證據。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: The Tasteful Agent 這篇論文把「做出好的長程決策的能力」稱為 taste（品味），從 agent 軌跡中的決策岔路口（同一個任務的多次嘗試在中途走向不同方向的分歧點）出題，只問模型「這兩個方向，你選哪個？」；並以 Qwen3.6-27B 為基礎模型訓練學生（題目依任務切成兩份，兩份各訓練一個學生），在每個岔路口從兩個候選中選一個。端到端實驗看學生的選擇能不能讓另一個 agent 把任務做得更好：學生不親自寫程式，只在每個岔路口給一則建議，另一個固定的 agent（executor，執行者）讀完建議再去做任務
  source_quotes:
  - "The Tasteful Agent 這篇論文"
  - "把「做出好的長程決策的能力」稱為 taste（品味）。"
  - "實務上，agent 系統常常對同一個任務跑好幾次，這些嘗試會在中途走向不同方向。"
  - "論文把這個分歧點稱為 decision fork（決策岔路口）。出題方式是：把軌跡凍結在岔路口，藏起後面所有的過程，只問模型「這兩個方向，你選哪個？」"
  - "建議由「沒有訓練過這個任務的那個學生」產生（兩份各訓練一個學生）。"
  - "基礎模型是 Qwen3.6-27B（凍結），老師與學生都是它。"
  - "學生會選了，但選對有沒有用？這一節看學生的選擇能不能讓另一個 agent 把任務做得更好。"
  - "學生不親自寫程式，只在每個岔路口給一則建議；另一個固定的 agent，稱為 executor（執行者），讀完建議再去做任務，看成功率有沒有提高。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  qualifiers:
  - text: 這個「多次嘗試、分歧前相同」的對照只適用 parallel：detour 是同一次嘗試裡 agent 走錯後自己改正，沒有另一條平行的分支可以對照
    source_quote: "沒有另一條平行的分支可以對照"
  - text: Taste-Bench 裡 parallel 有 172 題，detour 有 330 題
    source_quote: "在 Taste-Bench 裡，parallel 有 172 題，detour 有 330 題"
  importance: 2
  status: normal
- id: c3
  role: mechanism
  text: 流程：41 個 held-out 任務事先已有 98 個岔路口，岔路口與兩個候選的文字是造題流程從這些任務的舊執行挖出來的；學生對每個岔路口選一個候選（建議由沒有訓練過這個任務的那個學生產生），每個岔路口寫成一則建議筆記（情境、要避開的候選、要採用的候選），所有筆記放在 executor 的第一則訊息裡、問題描述之前；executor 獨立完成整個任務，用官方 SWE-bench Pro 的測試判定 patch 是否被接受
  source_quotes:
  - "每個 held-out 任務事先已有幾個岔路口（41 個任務共 98 個），岔路口與兩個候選的文字，是前面造題的流程從這些任務的舊執行挖出來的。"
  - "學生對每個岔路口選一個候選。建議由「沒有訓練過這個任務的那個學生」產生（兩份各訓練一個學生）。"
  - "每個岔路口寫成一則建議筆記：情境、要避開的候選、要採用的候選。"
  - "所有筆記放在 executor 的第一則訊息裡、問題描述之前。"
  - "executor 獨立完成整個任務。"
  - "用官方 SWE-bench Pro 的測試判定 patch 是否被接受，這就是成功。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 計數
  figures:
  - file: figures/tasteful-agent/figure6.png
    article: tasteful-agent
    src: figure6.png
    caption: 圖 6 — 蒸餾與建議注入的總覽。左半是把看過正確候選的老師的推理，蒸餾給只看到題目的學生；右半是評測時把學生在每個岔路口的判斷寫成建議，交給固定的 agent 獨立完成任務。（來源：原始論文 Figure 6。）
    sha256: ded8df1c3ebb036c045a51f7854a054332d3461e46c4b4c25c6161940783696a
  importance: 2
  status: normal
- id: c4
  role: mechanism
  text: 學生真正決定的只有一件事：建議的文字（情境、候選描述）是照模板組出來的，來自造題時寫好的內容；學生只決定哪個候選標成要避開、哪個標成要採用，也就是每個岔路口一個二選一。選擇的規則是把學生對兩種順序下 A、B 兩個答案 token 的 log-odds（兩個答案的機率比取對數）加總，取總和偏向的那個候選
  source_quotes:
  - "學生真正決定的只有一件事。 建議的文字（情境、候選描述）是照模板組出來的，來自 generator 在造題時寫好的內容；學生只決定「哪個候選標成要避開、哪個標成要採用」，也就是每個岔路口一個二選一。"
  - "選擇的規則：把學生對兩種順序下 A、B 兩個答案 token 的 log-odds（兩個答案的機率比取對數，越正越偏向 A）加總，取總和偏向的那個候選。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c5
  role: context
  text: executor 是 SWE-agent 1.1.0，模型是沒有蒸餾過的 Qwen3.6-27B（關閉 thinking，temperature 0.7），每次執行最多 75 次模型呼叫、每個指令 600 秒、總共 4,800 秒；41 個任務涵蓋 11 個 repository
  source_quotes:
  - "executor 是 SWE-agent 1.1.0，模型是 Qwen3.6-27B（沒有蒸餾過，關閉 thinking，temperature 0.7），每次執行最多 75 次模型呼叫、每個指令 600 秒、總共 4,800 秒，在該任務的官方 SWE-bench Pro 容器中執行。41 個任務涵蓋 11 個 repository。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 4
  status: normal
- id: c6
  role: anchor
  text: 41 個沒見過的 SWE-bench Pro 任務、同一個固定的 executor：沒有建議的成功率 14.6%，每個岔路口都給正確候選的成功率 39.0%，給學生選的候選的成功率 33.7%
  source_quotes:
  - "41 個沒見過的 SWE-bench Pro 任務、三種設定，由同一個固定的 executor（Qwen3.6-27B 加 SWE-agent）執行，成功與否由官方測試判定："
  - "| no advice | 沒有建議 | 14.6% |"
  - "| correct advice | 每個岔路口都給正確的候選 | 39.0% |"
  - "| student advice | 給學生選的候選 | 33.7% |"
  anchor_type: 實驗結果
  comparison_target: 沒有建議（no advice）的成功率 14.6%
  qualifiers:
  - text: 岔路口與候選是事先從同一任務的舊執行挖出來的，這個實驗測的是「有了現成的候選對，建議有沒有用」，不是「agent 遇到新任務時，自己判斷」
    source_quote: "所以這個實驗測的是「有了現成的候選對，建議有沒有用」，不是「agent 遇到新任務時，自己判斷」。"
  - text: 這 41 個任務都是「至少挖出一個岔路口」的任務，等於只挑了確實有決策分歧的任務
    source_quote: "另外，這 41 個任務都是「至少挖出一個岔路口」的任務，等於只挑了確實有決策分歧的任務。"
  - text: 後面兩個訓練實驗的數字，目前只能當方向性的訊號
    source_quote: "後面兩個訓練實驗的數字，目前只能當方向性的訊號"
  figures:
  - file: figures/tasteful-agent/figure7.png
    article: tasteful-agent
    src: figure7.png
    caption: 圖 7 — 蒸餾結果。左圖：在 390 題 held-out 工程題上，蒸餾後的學生準確率高於基礎模型，虛線是 GPT-5.6 Sol 的 56.9%；右圖：在 held-out 的 SWE-bench Pro 任務上，使用學生建議的執行 agent 成功率達到上限（虛線長條，也就是每個岔路口建議都正確）的大部分。（來源：原始論文 Figure 7。）
    sha256: 324b8fe7f82379294788fb8b7160405f547bdc5c96fb5094d3acb97aea723678
  importance: 2
  status: normal
- id: c7
  role: evidence
  text: 正確建議對沒建議的差距是 24.4 個百分點，論文把它當作這種建議的上限；學生建議的差距是 19.1 個百分點，約達上限的 78%（19.1 / 24.4）。學生在這 98 個岔路口中選對 77 個（78.6%）
  source_quotes:
  - "正確建議對沒建議的差距是 24.4 個百分點，論文把它當作這種建議的上限。學生建議的差距是 19.1 個百分點，約達上限的 78%（\\( 19.1 / 24.4 \\)）。學生在這 98 個岔路口中選對 77 個（78.6%）。"
  anchor_type: 部落格考證
  comparison_target: 正確建議相對於沒建議的差距 24.4 個百分點（論文當作上限）；78.6% 的分母是 98 個岔路口
  qualifiers:
  - text: 岔路口與候選是事先從同一任務的舊執行挖出來的，這個實驗測的是「有了現成的候選對，建議有沒有用」，不是「agent 遇到新任務時，自己判斷」
    source_quote: "所以這個實驗測的是「有了現成的候選對，建議有沒有用」，不是「agent 遇到新任務時，自己判斷」。"
  importance: 3
  status: normal
- id: c8
  role: evaluation
  text: 論文原文也說，建議在新的一次執行開始前就已準備好；所以這個實驗測的是「有了現成的候選對，建議有沒有用」，不是「agent 遇到新任務時，自己判斷」
  source_quotes:
  - "論文原文也說，建議在新的一次執行開始前就已準備好。所以這個實驗測的是「有了現成的候選對，建議有沒有用」，不是「agent 遇到新任務時，自己判斷」。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c9
  role: evaluation
  text: 把整條流程拆開：學生對一道已經寫好的 A/B 題做選擇，論文有測（沒見過的任務上 47.9%）；把選擇寫成建議交給 executor，有測；偵測「現在是不是岔路口」、自己列出兩個措辭平行的候選，這兩步沒測。新任務沒有舊執行，這兩步在實際使用時要由 agent 自己完成，而論文都沒驗證
  source_quotes:
  - "| 學生對一道已經寫好的 A/B 題做選擇 | 有（沒見過的任務上 47.9%） |"
  - "| 偵測「現在是不是岔路口」 | 沒測 |"
  - "| 自己列出兩個措辭平行的候選 | 沒測 |"
  - "| 把選擇寫成建議交給 executor | 有 |"
  - "新任務沒有舊執行，所以「找岔路口、寫候選」這兩步在實際使用時要由 agent 自己完成，而這兩步論文都沒驗證。"
  - "比較對象是沒有微調的基礎模型 Qwen3.6-27B。"
  anchor_type: 部落格判斷
  comparison_target: 47.9% 是學生在沒見過的任務上的準確率，比較對象是沒有微調的基礎模型 Qwen3.6-27B
  qualifiers:
  - text: 後面兩個訓練實驗的數字，目前只能當方向性的訊號
    source_quote: "後面兩個訓練實驗的數字，目前只能當方向性的訊號"
  importance: 2
  status: normal
- id: c10
  role: evaluation
  text: blog 推論，真實的候選不會像 Taste-Bench 那樣被整理成乾淨的平行措辭，找岔路口與寫候選這兩步各自也會出錯
  source_quotes:
  - "我的推論是，真實的候選不會像 Taste-Bench 那樣被整理成乾淨的平行措辭，這兩步各自也會出錯。"
  anchor_type: 部落格推論
  importance: 3
  status: normal
- id: c11
  role: qualifier
  text: 這 41 個任務都是「至少挖出一個岔路口」的任務，等於只挑了確實有決策分歧的任務
  source_quotes:
  - "另外，這 41 個任務都是「至少挖出一個岔路口」的任務，等於只挑了確實有決策分歧的任務。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 3
  status: normal
- id: c12
  role: evaluation
  text: 蒸餾遷移與端到端用的是同一批學生，問的是不同的問題：蒸餾遷移問「學生會不會選」，衡量選對岔路口的比例（30.0% → 47.9%）；端到端問「學生選完，有沒有讓別人做得更好」，衡量任務成功率（14.6% → 33.7%）。端到端每個任務的建議都是由沒有訓練過該任務的學生寫的，兩個實驗在「學生沒見過這個任務」這點上是一致的
  source_quotes:
  - "兩個實驗用的是同一批學生，但問的是不同的問題："
  - "| 衡量什麼 | 選對岔路口的比例（30.0% → 47.9%） | 任務成功率（14.6% → 33.7%） |"
  - "簡單說，蒸餾遷移問「學生會不會選」，端到端問「學生選完，有沒有讓別人做得更好」。端到端每個任務的建議，都是由沒有訓練過該任務的那一個學生寫的，所以兩個實驗在「學生沒見過這個任務」這點上是一致的。"
  - "比較對象是沒有微調的基礎模型 Qwen3.6-27B。"
  - "| no advice | 沒有建議 | 14.6% |"
  anchor_type: 部落格判斷
  comparison_target: 30.0% 是沒有微調的基礎模型；14.6% 是沒有建議的 executor
  qualifiers:
  - text: 後面兩個訓練實驗的數字，目前只能當方向性的訊號
    source_quote: "後面兩個訓練實驗的數字，目前只能當方向性的訊號"
  - text: 端到端用的是事先挖好的岔路口，還不能當作可以直接用在新任務上的證據
    source_quote: "蒸餾與端到端的結果（30.0% 到 47.9%、14.6% 到 33.7%）是正面的方向性訊號，但端到端用的是事先挖好的岔路口，所以還不能當作可以直接用在新任務上的證據。"
  importance: 3
  status: normal
- id: c13
  role: evaluation
  text: 下次看到「學生建議讓成功率大增」這類結果，先問一句：岔路口是誰找出來的？
  source_quotes:
  - "下次看到「學生建議讓成功率大增」這類結果，先問一句：岔路口是誰找出來的？"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
```
