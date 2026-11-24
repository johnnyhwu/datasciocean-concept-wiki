---
id: taste-privileged-teacher-distillation
title: 同一個模型當老師與學生，老師多看到答案；學生先用 forward KL 學老師的推理，再在自己的推理後面校準最後的選擇，在沒見過的任務上準確率從 30.0% 升到 47.9%，但目前只能當方向性的訊號
type_hint: 方法
context_type: bound_to_source
sources:
- article: tasteful-agent
  article_title: "The Tasteful Agent 解析：用 agent 跑過的軌跡，量測並訓練 AI 的決策品味"
  url: https://datasciocean.com/paper-intro/tasteful-agent/
  sections:
  - agent 的中途決策沒人量過，這篇論文用跑過的軌跡免費出題
  - 同任務、同前綴，結果的差異才能歸給判斷
  - 從 4,657 個候選篩到 502 題
  - 品味能訓練嗎：讓偷看答案的老師教學生
  - 設定：同一個模型，老師多看一段答案
  - 為什麼學推理、用什麼損失：forward KL
  - 第二階段：讓學生在自己的推理後面也選對
  - 洩漏控制，以及它擋不到的轉述
  - 蒸餾結果：沒見過的任務上，30.0% 升到 47.9%
  - 值得肯定的，以及研究與工程上的價值
  - KL 要在誰寫的文字上算
  - parallel 與 detour 也決定了標籤怎麼來
  first_appearance: true
parent: null
related:
  - taste-fork-outcome-labels
  - taste-advice-deployment-gap
  - forward-kl-truncation-teacher-topk
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 同一個模型當老師與學生，老師多看到答案；學生先用 forward KL 學老師的推理，再在自己的推理後面校準最後的選擇。學生在沒見過的任務上，準確率從 30.0% 升到 47.9%，但這個數字目前只能當方向性的訊號
  source_quotes:
  - "整理一下：同一個模型當老師與學生，老師多看到答案；學生先用 forward KL 學老師的推理，再在自己的推理後面校準最後的選擇。"
  - "學生在沒見過的任務上，準確率從 30.0% 升到 47.9%"
  - "後面兩個訓練實驗的數字，目前只能當方向性的訊號"
  anchor_type: 部落格判斷
  comparison_target: 沒有微調的基礎模型 Qwen3.6-27B
  qualifiers:
  - text: 校準這一步直接用了標準答案，正文沒提、只在附錄寫到；論文也沒有報告校準前後的準確率差異
    source_quote: "校準直接用了標準答案，正文沒提它，只在附錄寫到；論文也沒有報告校準前後的準確率差異。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: The Tasteful Agent 這篇論文把「做出好的長程決策的能力」稱為 taste（品味），並從 agent 軌跡中的決策岔路口造出評測集 Taste-Bench：同一個任務的多次嘗試在中途走向不同方向，把分歧點之後的內容藏起來，只問模型「該選哪個方向」，答案是事後結果比較好的那一邊。Taste-Bench 量出來的是「現有模型品味有限」，下一個問題是這種品味能不能訓練
  source_quotes:
  - "The Tasteful Agent 這篇論文"
  - "把「做出好的長程決策的能力」稱為 taste（品味）。"
  - "同一個任務常被 agent 嘗試好幾次，這些嘗試會在中途走向不同方向，最後結果一好一壞。把分歧點之後的內容藏起來，只問模型「該選哪個方向」，答案就是紀錄下來的結果，不需要人工標註。"
  - "用這個方法，論文造出一個 502 題的評測集 Taste-Bench。"
  - "Taste-Bench 量出來的是「現有模型品味有限」。下一個問題是：這種品味能不能訓練？"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 這個「多次嘗試、分歧前相同」的對照只適用 parallel：detour 是同一次嘗試裡 agent 走錯後自己改正，沒有另一條平行的分支可以對照
    source_quote: "沒有另一條平行的分支可以對照"
  - text: Taste-Bench 裡 parallel 有 172 題，detour 有 330 題
    source_quote: "在 Taste-Bench 裡，parallel 有 172 題，detour 有 330 題"
  importance: 2
  status: normal
- id: c3
  role: mechanism
  text: 做法是讓一個「偷看過答案」的老師（privileged teacher，輸入裡多了學生拿不到的正確答案）寫出解題推理，再訓練一個「沒看過答案」的學生，在自己的輸入下寫出同樣的推理與選擇。老師和學生是同一個基礎模型 Qwen3.6-27B（凍結，用 LoRA 訓練額外加上的小型低秩矩陣），差別只在輸入：老師的輸入是題目加 demonstration（寫明這個岔路口正確的做法是哪個候選、要避開另一個），學生的輸入是題目本身，跟評測時受測模型看到的一模一樣
  source_quotes:
  - "做法是讓一個「偷看過答案」的老師寫出解題推理，再訓練一個「沒看過答案」的學生，在自己的輸入下寫出同樣的推理與選擇。老師和學生是同一個模型，差別只在輸入內容。"
  - "privileged teacher（有特權資訊的老師）： 老師的輸入裡多了學生拿不到的資訊，這裡就是正確答案。"
  - "demonstration： 放進老師輸入的一小段文字，寫明「這個岔路口正確的做法是這個候選，要避開另一個」。"
  - "LoRA： 不改動原模型的權重，只訓練額外加上的小型低秩矩陣"
  - "基礎模型是 Qwen3.6-27B（凍結），老師與學生都是它。"
  - "老師的輸入是題目加 demonstration；學生的輸入是題目本身（任務、前綴、兩個打亂順序的候選），跟評測時受測模型看到的一模一樣。"
  anchor_type: 設計參數
  figures:
  - file: figures/tasteful-agent/figure6.png
    article: tasteful-agent
    src: figure6.png
    caption: 圖 6 — 蒸餾與建議注入的總覽。左半是把看過正確候選的老師的推理，蒸餾給只看到題目的學生；右半是評測時把學生在每個岔路口的判斷寫成建議，交給固定的 agent 獨立完成任務。（來源：原始論文 Figure 6。）
    sha256: ded8df1c3ebb036c045a51f7854a054332d3461e46c4b4c25c6161940783696a
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 2
  status: normal
- id: c4
  role: mechanism
  text: 訓練資料是 Taste-Bench 502 題中的 390 道工程題，依任務切成兩份（各 195 題），學生在一份上訓練、在另一份上測試，所以測試題的任務學生訓練時沒見過（held-out）；兩份的結果合併成 390 題的成績
  source_quotes:
  - "訓練資料是 390 道工程題，依任務切成兩份（論文稱為 fold，各 195 題，每個 repository 兩份都有）。學生在一份上訓練、在另一份上測試，所以測試題的任務學生訓練時沒見過，這種留作測試的資料稱為 held-out。"
  - "兩份的結果合併成 390 題的成績。"
  - "最後通過 undecidable 過濾的剩 502 題，分成四格："
  - "| 工程 | 124 | 266 | 390 |"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 3
  status: normal
- id: c5
  role: mechanism
  text: 學推理而不是直接學標籤：每一題只有一個二選一的標籤，沒有中間推理；論文的理由是，只用標籤微調，模型會背答案而沒有學到判斷
  source_quotes:
  - "為什麼要學推理，而不是直接學標籤？每一題只有一個二選一的標籤，沒有中間推理。論文的理由是：只用標籤微調，模型會背答案而沒有學到判斷。"
  anchor_type: 原作者解讀
  qualifiers:
  - text: 論文沒有附「只學標籤」的對照實驗，這是論文給的理由
    source_quote: "要注意，論文沒有附「只學標籤」的對照實驗，這是論文給的理由。"
  importance: 3
  status: normal
- id: c6
  role: mechanism
  text: 損失函數用 forward KL：KL 散度衡量兩個機率分布差多少，完全一樣時為 0。在老師寫出的推理的每一個位置，老師與學生讀同一段前文、各自預測下一個 token，兩邊的猜法差越多損失越大，訓練就把學生的猜法拉向老師
  source_quotes:
  - "損失函數用的是 forward KL。"
  - "衡量兩個機率分布差多少：兩個分布完全一樣時為 0，差越多越大。在老師寫出的推理的每一個位置 \\( t \\)，兩邊讀同一段前文，各自預測下一個 token；兩邊的猜法差越多，損失越大，訓練就把學生的猜法拉向老師。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 2
  status: normal
- id: c7
  role: mechanism
  text: 「學生要模仿誰」和「在誰寫的那段文字上比較」是兩件不同的事：學生模仿的對象永遠是老師，論文選擇用老師寫的文字當比較的現場。論文的理由是，兩邊的輸入只差在 demonstration，真正預測不同的 token 只出現在老師的輸出裡；學生自己的樣本很少產生這些 token，在學生的文字上算 KL，就抓不到老師的偏好
  source_quotes:
  - "「學生要模仿誰」和「在誰寫的那段文字上比較」是兩件不同的事。學生模仿的對象永遠是老師；論文選擇用老師寫的文字當比較的現場。"
  - "論文的理由，翻成白話：兩邊的輸入只差在 demonstration，真正預測不同的 token，只出現在老師的輸出裡。學生自己的樣本很少產生這些 token，在學生的文字上算 KL，就抓不到老師的偏好。"
  anchor_type: 原作者解讀
  qualifiers:
  - text: 在學生自己的取樣上算 KL 是 on-policy distillation 的標準做法；論文刻意不照那樣做，沒有提供改用學生文字的對照實驗
    source_quote: "在學生自己的取樣上算 KL，是 on-policy distillation（在學生自己的輸出上蒸餾）的標準做法。論文刻意不照那樣做，並且把理由寫在附錄；論文沒有提供改用學生文字的對照實驗。"
  importance: 3
  status: normal
- id: c8
  role: evaluation
  text: 一般化來看，蒸餾時如果老師與學生的差異來自「老師多看到的資訊」，就要在老師的軌跡上比較：只有在老師的軌跡上，那些資訊的影響才會顯現；學生想不到的洞見，不會出現在它自己的文字裡，也就沒有東西可以教它
  source_quotes:
  - "蒸餾時如果老師與學生的差異來自「老師多看到的資訊」，就要在老師的軌跡上比較，因為只有在老師的軌跡上，那些資訊的影響才會顯現；在學生自己的軌跡上，學生永遠走不到那裡。"
  - "學生想不到的洞見，不會出現在它自己的文字裡，也就沒有東西可以教它。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c9
  role: mechanism
  text: 蒸餾之後還有第二階段「校準」：蒸餾時學生的最終選擇是接在老師寫的推理後面學的，實際考試時接的卻是自己寫的推理。校準讓學生對每道訓練題自己寫出推理，只在最後選擇的位置，用 cross-entropy（衡量模型給正確答案多少機率的損失）對標準答案訓練，推理部分不動；學習率是蒸餾的十分之一、1 個 epoch
  source_quotes:
  - "蒸餾時，學生的最終選擇是接在「老師寫的推理」後面學的；但實際考試時，學生接的是「自己寫的推理」。校準就是讓學生在自己的推理後面也能選對："
  - "學生對每道訓練題（A、B 兩種順序各一次）自己寫出推理。"
  - "只在最後選擇的位置，用 cross-entropy（衡量模型給正確答案多少機率的損失）對標準答案訓練，推理部分不動。"
  - "設定：學習率 \\( 10^{-5} \\)（蒸餾的十分之一）、1 個 epoch"
  anchor_type: 設計參數
  comparison_target: 蒸餾階段的學習率
  qualifiers:
  - text: 為什麼需要校準論文沒有解釋，「訓練與考試接的推理不同」是 blog 的推論；校準直接用了標準答案，正文沒提、只在附錄寫到；論文也沒有報告校準前後的準確率差異
    source_quote: "為什麼需要校準，論文沒有解釋，上面「訓練與考試接的推理不同」是我的推論。校準直接用了標準答案，正文沒提它，只在附錄寫到；論文也沒有報告校準前後的準確率差異。"
  importance: 3
  status: normal
- id: c10
  role: mechanism
  text: 洩漏控制：老師的輸出是看過 demonstration 才寫出來的，若混了「只有看過答案才寫得出來」的內容，學生就會學成「假裝有依據，然後猜」。論文的結構性控制是把選擇限定成 A 或 B、老師的輸出到最終答案就結束，所以輸出裡沒有任何一段是照抄 demonstration 的文字
  source_quotes:
  - "還有一個要防的事：老師的輸出是看過 demonstration 才寫出來的，如果輸出裡混了「只有看過答案才寫得出來」的內容，學生被訓練去寫這些內容，就會學成「假裝有依據，然後猜」。論文的做法稱為結構性控制：選擇限定成 A 或 B，老師的輸出到最終答案就結束，所以輸出裡沒有任何一段是照抄 demonstration 的文字。"
  anchor_type: 設計參數
  qualifiers:
  - text: 結構性控制只擋了答案欄位；推理那段仍是自由生成的文字，老師可以用自己的話轉述 demonstration 的內容，這種轉述控制擋不到，論文也沒有報告這方面的檢查數據
    source_quote: "結構性控制只擋了答案欄位。推理那段仍是自由生成的文字，老師可以用自己的話轉述 demonstration 的內容，例如 Ansible 例子裡的「既有測試會直接呼叫這個 helper」，這種轉述不算照抄，控制擋不到；論文也沒有報告這方面的檢查數據。"
  importance: 3
  status: normal
- id: c11
  role: anchor
  text: 在學生沒見過的那份工程題上（兩份合併共 390 題），嚴格準確率（A、B 兩種順序都答對才算對）從基礎模型的 30.0% 升到學生的 47.9%；平均準確率（兩順序各算一次）從 42.7% 升到 62.4%
  source_quotes:
  - "比較對象是沒有微調的基礎模型 Qwen3.6-27B。"
  - "| 嚴格準確率（兩順序都對） | 未報告 | 基礎模型 30.0% → 學生 47.9% |"
  - "| 平均準確率（兩順序各算一次） | 未報告 | 42.7% → 62.4% |"
  - "390 題工程題依任務切成兩份，學生在一份上訓練、在另一份上測試，兩份的結果合併成 390 題的成績。"
  anchor_type: 實驗結果
  comparison_target: 沒有微調的基礎模型 Qwen3.6-27B
  qualifiers:
  - text: 校準這一步直接用了標準答案，正文沒提、只在附錄寫到；論文也沒有報告校準前後的準確率差異
    source_quote: "校準直接用了標準答案，正文沒提它，只在附錄寫到；論文也沒有報告校準前後的準確率差異。"
  - text: 後面兩個訓練實驗的數字，目前只能當方向性的訊號
    source_quote: "後面兩個訓練實驗的數字，目前只能當方向性的訊號"
  - text: 推理裡的轉述擋不到，學生學到的有多少是真判斷，要看沒見過的那份題目上的結果
    source_quote: "學生學到的有多少是真判斷，要看沒見過的那份題目上的結果，也就是下一節。"
  figures:
  - file: figures/tasteful-agent/figure7.png
    article: tasteful-agent
    src: figure7.png
    caption: 圖 7 — 蒸餾結果。左圖：在 390 題 held-out 工程題上，蒸餾後的學生準確率高於基礎模型，虛線是 GPT-5.6 Sol 的 56.9%；右圖：在 held-out 的 SWE-bench Pro 任務上，使用學生建議的執行 agent 成功率達到上限（虛線長條，也就是每個岔路口建議都正確）的大部分。（來源：原始論文 Figure 7。）
    sha256: 324b8fe7f82379294788fb8b7160405f547bdc5c96fb5094d3acb97aea723678
  importance: 2
  status: normal
- id: c12
  role: evidence
  text: 用論文附錄的數字驗算：學生兩順序都對有 187 題，基礎模型有 117 題；學生對、基礎模型錯的有 104 題，反過來有 34 題，淨增 70 題，70/390 = 17.9 個百分點
  source_quotes:
  - "用論文附錄的數字驗算：學生兩順序都對有 187 題，基礎模型有 117 題。學生對、基礎模型錯的有 104 題，反過來有 34 題，淨增 70 題，\\( 70 / 390 = 17.9 \\) 個百分點。"
  anchor_type: 部落格考證
  comparison_target: 沒有微調的基礎模型在同一批 390 題上的答對題數
  importance: 4
  status: normal
- id: c13
  role: qualifier
  text: 在學生訓練過的那份題目上，單一順序答對的比例是 48.6% → 92.9%；但訓練那份只代表模型背得下訓練題，沒見過的那份才是證據
  source_quotes:
  - "| 單一順序答對的比例 | 48.6% → 92.9% | 未報告 |"
  - "訓練那份只代表模型背得下訓練題，沒見過的那份才是證據。"
  anchor_type: 部落格判斷
  comparison_target: 同一列箭頭前的 48.6%（訓練那份上的單一順序答對比例）
  importance: 4
  status: normal
- id: c14
  role: evidence
  text: 學生的 47.9% 放在工程題排名上：低於 GPT-5.6 Sol 的 56.9% 與 GPT-5.6 Terra 的 50.0%，和 GLM-5.2 的 47.9% 相當，高於 Claude Opus 5 的 46.7%；基礎模型的 30.0% 則略低於 GPT-5.4 Nano 的 32.1%
  source_quotes:
  - "| GPT-5.6 Sol | 56.9% | 學生較低 |"
  - "| GPT-5.6 Terra | 50.0% | 學生較低 |"
  - "| GLM-5.2 | 47.9% | 相當 |"
  - "| Claude Opus 5 | 46.7% | 學生較高 |"
  - "基礎模型（30.0%）則略低於 GPT-5.4 Nano（32.1%）。"
  - "| 對象 | 工程題準確率 | 與學生（47.9%）的關係 |"
  anchor_type: 部落格考證
  comparison_target: 各前沿模型在 Taste-Bench 工程題上的準確率
  qualifiers:
  - text: 後面兩個訓練實驗的數字，目前只能當方向性的訊號
    source_quote: "後面兩個訓練實驗的數字，目前只能當方向性的訊號"
  importance: 4
  status: normal
- id: c15
  role: evaluation
  text: blog 的評價：蒸餾部分是 context distillation（把放在輸入裡的資訊的效果，透過訓練內化進模型權重）的變體；蒸餾與建議注入這一塊，顯示「把看過結果的判斷內化」是可行的方向，但還沒有證明能部署在新任務上
  source_quotes:
  - "蒸餾部分是 context distillation 的變體。"
  - "context distillation（上下文蒸餾）： 把「放在輸入裡的資訊」的效果，透過訓練內化進模型權重。"
  - "蒸餾與建議注入這一塊，顯示「把看過結果的判斷內化」是可行的方向，但還沒有證明能部署在新任務上。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
```
