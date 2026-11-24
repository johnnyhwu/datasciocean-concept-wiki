---
id: taste-fork-outcome-labels
title: 同一個任務的多次嘗試，在中途分歧之前完全相同，最後的結果就是岔路口那個決策的標籤：軌跡的後半段，就是前半段決策的答案卷
type_hint: 方法
context_type: evidence_from_single_source
sources:
- article: tasteful-agent
  article_title: "The Tasteful Agent 解析：用 agent 跑過的軌跡，量測並訓練 AI 的決策品味"
  url: https://datasciocean.com/paper-intro/tasteful-agent/
  sections:
  - agent 的中途決策沒人量過，這篇論文用跑過的軌跡免費出題
  - 為什麼 agent 的品味這麼難量
  - 同任務、同前綴，結果的差異才能歸給判斷
  - 一道題長什麼樣子：標籤與答對率
  - 兩種挖岔路口的方法：parallel 與 detour
  - generator 的防呆規則：不要事後諸葛、不要稻草人
  - 從 4,657 個候選篩到 502 題
  - 人工審查：標籤和紀錄對得上，但不等於因果
  - 值得肯定的，以及研究與工程上的價值
  - 帶走一（論文本身的貢獻）：造題配方
  - 一句話總結
  - parallel 與 detour 也決定了標籤怎麼來
  - 怎麼讀人工審查的一致率
  first_appearance: true
parent: null
related:
  - taste-bench-frontier-results
  - pairwise-eval-swap-order-twice
  - taste-privileged-teacher-distillation
  - taste-advice-deployment-gap
  - forward-kl-truncation-teacher-topk
  - llm-patch-validation-format-not-semantics
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 同一個任務的多次嘗試，在中途分歧之前完全相同，最後的結果就是岔路口那個決策的標籤：軌跡的後半段，就是前半段決策的答案卷
  source_quotes:
  - "這篇論文的核心想法很簡單：同一個任務的多次嘗試，在中途分歧之前完全相同，最後的結果就是岔路口那個決策的標籤。"
  - "軌跡的後半段，就是前半段決策的答案卷。"
  anchor_type: 原作者解讀
  qualifiers:
  - text: parallel 的實際造法是把同一任務一成一敗的兩次嘗試配成一對，generator 讀完兩份完整軌跡各自找出岔路口，以成功那次在岔路口之前的部分當作前綴
    source_quote: "在同一個任務裡，挑一次成功、一次失敗的嘗試配成一對"
  - text: generator 讀完兩份完整軌跡，各自找出岔路口；成功那次在岔路口之前的部分當作前綴
    source_quote: "generator 讀完兩份完整軌跡，各自找出岔路口。"
  - text: 成功那次在岔路口之前的部分當作前綴
    source_quote: "成功那次在岔路口之前的部分當作前綴；兩個方向各寫成一段簡短、中性的描述，當作兩個候選。"
  - text: 這個「多次嘗試、分歧前相同」的對照只適用 parallel：detour 是同一次嘗試裡 agent 走錯後自己改正，沒有另一條平行的分支可以對照
    source_quote: "沒有另一條平行的分支可以對照"
  - text: Taste-Bench 裡 parallel 有 172 題，detour 有 330 題
    source_quote: "在 Taste-Bench 裡，parallel 有 172 題，detour 有 330 題"
  - text: 分支分開之後，執行品質仍然會影響結果；論文用後續的過濾步驟來處理
    source_quote: "分支分開之後，執行品質仍然會影響結果。論文用後續的過濾步驟來處理"
  - text: 一次的結果含有運氣成分，所以標籤嚴格說是「這一次誰贏」，不等於「期望上誰比較好」；論文靠後面的過濾來降低這個問題
    source_quote: "一次的結果含有運氣成分，所以標籤嚴格說是「這一次誰贏」，不等於「期望上誰比較好」。論文靠後面的過濾來降低這個問題。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: The Tasteful Agent 這篇論文把「做出好的長程決策的能力」稱為 taste（品味）。LLM agent 做長任務時，中途的決策（先測哪個假設、沿用哪個實作）常常決定整體成敗；但現有的 agent 評測（例如讓 agent 修真實 GitHub 問題的 SWE-bench）屬於 end-to-end benchmark（端到端評測），只報告 agent 最後有沒有完成任務，不報告中途每個決策的品質
  source_quotes:
  - "LLM agent 做長任務時，這種中途的決策（先測哪個假設、沿用哪個實作）常常決定整體成敗。"
  - "The Tasteful Agent 這篇論文"
  - "把「做出好的長程決策的能力」稱為 taste（品味）。問題是，現有的評測只看 agent 最後有沒有做完，沒有人直接量測決策本身的品質。"
  - "現有的 agent 評測，例如讓 agent 修真實 GitHub 問題的 SWE-bench，屬於 end-to-end benchmark（端到端評測）：只報告 agent 最後有沒有完成任務，完全不報告中途每個決策的品質。"
  anchor_type: 原作者解讀
  importance: 2
  status: normal
- id: c3
  role: mechanism
  text: 實務上，agent 系統常常對同一個任務跑好幾次，這些嘗試會在中途走向不同方向；論文把這個分歧點稱為 decision fork（決策岔路口）。出題方式是把軌跡凍結在岔路口，藏起後面所有的過程，只問模型「這兩個方向，你選哪個？」；題目是任務、前綴、兩個候選
  source_quotes:
  - "實務上，agent 系統常常對同一個任務跑好幾次，這些嘗試會在中途走向不同方向。"
  - "論文把這個分歧點稱為 decision fork（決策岔路口）。出題方式是：把軌跡凍結在岔路口，藏起後面所有的過程，只問模型「這兩個方向，你選哪個？」"
  - "也就是任務、前綴、兩個候選，岔路口之後的所有內容都藏起來。"
  anchor_type: 設計參數
  figures:
  - file: figures/tasteful-agent/figure1.png
    article: tasteful-agent
    src: figure1.png
    caption: 圖 1 — 機器學習軌跡中的決策岔路口。受測模型必須在後面的 loss 揭曉候選 A 較好之前做出選擇。（來源：原始論文 Figure 1。）
    sha256: e5b0bbaa41be553ab8e193defb088010d53d58358adcece15086cbc6b8601d59
  importance: 2
  status: normal
- id: c4
  role: mechanism
  text: 一定要用同一個任務的兩次嘗試，是因為單一軌跡的結果混雜了判斷的好壞、執行的品質、環境因素三件事，看不出結果是不是判斷造成的；如果兩次嘗試在岔路口之前完全相同（同一個任務、同一段前文，這段前文稱為前綴），兩條分支的結果差異就主要來自岔路口的那個判斷
  source_quotes:
  - "為什麼一定要用同一個任務的兩次嘗試？因為單一軌跡的結果混雜了三件事：判斷的好壞、執行的品質、環境因素，看不出結果是不是判斷造成的。如果兩次嘗試在岔路口之前完全相同，也就是同一個任務、同一段前文（這段前文稱為前綴），兩條分支的結果差異就主要來自岔路口的那個判斷。"
  anchor_type: 原作者解讀
  qualifiers:
  - text: parallel 的實際造法是把同一任務一成一敗的兩次嘗試配成一對，generator 讀完兩份完整軌跡各自找出岔路口，以成功那次在岔路口之前的部分當作前綴
    source_quote: "在同一個任務裡，挑一次成功、一次失敗的嘗試配成一對"
  - text: generator 讀完兩份完整軌跡，各自找出岔路口；成功那次在岔路口之前的部分當作前綴
    source_quote: "generator 讀完兩份完整軌跡，各自找出岔路口。"
  - text: 成功那次在岔路口之前的部分當作前綴
    source_quote: "成功那次在岔路口之前的部分當作前綴；兩個方向各寫成一段簡短、中性的描述，當作兩個候選。"
  - text: 這個假設不是百分之百成立：分支分開之後，執行品質仍然會影響結果；論文用後續的過濾步驟來處理
    source_quote: "分支分開之後，執行品質仍然會影響結果。論文用後續的過濾步驟來處理"
  importance: 2
  status: normal
- id: c5
  role: mechanism
  text: 標籤就是兩條分支中最終結果比較好的那一條：每條分支各自跑到結束留下證據（例如測試結果、研究分數），用一個函數把證據換成分數，誰的最終分數高，誰就是對的；答案就是紀錄下來的結果，不需要人工標註
  source_quotes:
  - "一道題對應一個岔路口，標籤就是兩條分支中最終結果比較好的那一條。"
  - "每條分支各自跑到結束，留下證據 \\( E_i \\)（例如測試結果、研究分數）。再用一個函數 \\( U \\) 把證據換成一個數字，數字越大代表結果越好。白話來說：誰的最終分數高，誰就是對的。"
  - "答案就是紀錄下來的結果，不需要人工標註。"
  anchor_type: 設計參數
  qualifiers:
  - text: 一次的結果含有運氣成分，所以標籤嚴格說是「這一次誰贏」，不等於「期望上誰比較好」；論文靠後面的過濾來降低這個問題
    source_quote: "一次的結果含有運氣成分，所以標籤嚴格說是「這一次誰贏」，不等於「期望上誰比較好」。論文靠後面的過濾來降低這個問題。"
  importance: 2
  status: normal
- id: c6
  role: anchor
  text: 論文的例子：任務是訓練一個 masked language model（遮罩語言模型），候選 A 是縮小模型、多訓練幾步，候選 B 是維持模型大小、少訓練幾步；很多步之後，A 的最終 loss 是 6.56，B 是 7.66（B 的訓練跑到逾時）。loss 越低越好，所以答案是 A
  source_quotes:
  - "任務是訓練一個 masked language model（遮罩語言模型）。候選 A 是縮小模型、多訓練幾步，候選 B 是維持模型大小、少訓練幾步。很多步之後，A 的最終 loss 是 6.56，B 是 7.66（B 的訓練跑到逾時）。loss 越低越好"
  - "\\( U(E_1) \\) 較大，所以 \\( y = 1 \\)，答案是 A"
  anchor_type: 實驗結果
  comparison_target: 同一個岔路口的另一個候選（B 的最終 loss 7.66）
  figures:
  - file: figures/tasteful-agent/figure1.png
    article: tasteful-agent
    src: figure1.png
    caption: 圖 1 — 機器學習軌跡中的決策岔路口。受測模型必須在後面的 loss 揭曉候選 A 較好之前做出選擇。（來源：原始論文 Figure 1。）
    sha256: e5b0bbaa41be553ab8e193defb088010d53d58358adcece15086cbc6b8601d59
  importance: 4
  status: normal
- id: c7
  role: mechanism
  text: 岔路口有兩個來源。parallel（平行軌跡）是兩次獨立嘗試走向不同方向：在同一個任務裡挑一次成功、一次失敗的嘗試配成一對，出題模型（generator，這裡是 GPT-5.6 Sol）讀完兩份完整軌跡找出岔路口，成功那次在岔路口之前的部分當作前綴，兩個方向各寫成一段簡短、中性的描述當作兩個候選，成功的那條分支就是答案；它抓的是 agent 一路都沒發現的錯誤
  source_quotes:
  - "岔路口有兩個來源：兩次獨立嘗試走向不同方向，稱為 parallel（平行軌跡）"
  - "兩種都由同一個 generator（出題模型，這裡是 GPT-5.6 Sol，high reasoning effort）讀軌跡之後，找出岔路口並寫成題目。"
  - "Parallel 抓的是 agent 一路都沒發現的錯誤。"
  - "在同一個任務裡，挑一次成功、一次失敗的嘗試配成一對"
  - "generator 讀完兩份完整軌跡，各自找出岔路口。"
  - "成功那次在岔路口之前的部分當作前綴；兩個方向各寫成一段簡短、中性的描述，當作兩個候選。"
  - "成功的那條分支就是答案。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  figures:
  - file: figures/tasteful-agent/figure2.png
    article: tasteful-agent
    src: figure2.png
    caption: 圖 2 — Taste-Bench 的建構與過濾。parallel 比較同一任務的不同分支，detour 比較被放棄的方向與後來的改正，之後再經過過濾。（來源：原始論文 Figure 2。）
    sha256: dbba11e94d86eead13bb4af212bf79fd8329d2dbec666221afdef6197bf13d25
  importance: 3
  status: normal
- id: c8
  role: mechanism
  text: detour（繞路軌跡）是同一次嘗試裡 agent 走錯後自己改正：generator 讀一份完整軌跡和它的結果，依序找出「agent 選了某個方向、觀察到的失敗讓這個方向結束、agent 改走另一個方向並完成任務」；岔路口放在 agent 開始走被放棄方向的前一步，兩個候選是被放棄的方向和後來的改正，改正的方向是答案。這個構造測的是受測模型能不能比當時行動的 agent 更早看出失敗
  source_quotes:
  - "或是同一次嘗試裡 agent 走錯後自己改正，稱為 detour（繞路軌跡）。"
  - "generator 讀一份完整軌跡和它的結果，依序找出三件事：agent 選了某個方向、觀察到的失敗讓這個方向結束、agent 改走另一個方向並完成任務。"
  - "岔路口放在「agent 開始走被放棄方向」的前一步，前面的部分當前綴。"
  - "兩個候選是「被放棄的方向」和「後來的改正」，用平行的措辭寫成。"
  - "改正的方向是答案，因為被放棄的方向產生了可觀察的失敗，改正則完成了任務。"
  - "這個構造測的是：受測模型能不能比當時行動的 agent 更早看出失敗。"
  anchor_type: 設計參數
  qualifiers:
  - text: blog 的推論（不是論文原文）：detour 標籤的可信度，比 parallel 更依賴 generator 的規則與後面的過濾
    source_quote: "這裡是我的推論，不是論文原文：detour 標籤的可信度，比 parallel 更依賴 generator 的規則與後面的過濾"
  figures:
  - file: figures/tasteful-agent/figure2.png
    article: tasteful-agent
    src: figure2.png
    caption: 圖 2 — Taste-Bench 的建構與過濾。parallel 比較同一任務的不同分支，detour 比較被放棄的方向與後來的改正，之後再經過過濾。（來源：原始論文 Figure 2。）
    sha256: dbba11e94d86eead13bb4af212bf79fd8329d2dbec666221afdef6197bf13d25
  importance: 3
  status: normal
- id: c9
  role: evaluation
  text: parallel 與 detour 不只是「樣本從哪裡來」，它們同時決定了「這題的答案是怎麼得到的」：parallel 的兩條分支在岔路口之前完全相同，是真正的對照；detour 沒有另一條平行的分支可以對照。任何從日誌挖評測題的做法都會碰到這個選擇：用「兩次不同的執行」構成反事實對照，標籤更可靠；用「一次執行裡的自我修正」，資料量更大，但也比較容易碰上「事後諸葛」的風險
  source_quotes:
  - "parallel 與 detour 不只是「樣本從哪裡來」，它們同時決定了「這題的答案是怎麼得到的」。"
  - "有：兩條分支在岔路口之前完全相同，是真正的對照"
  - "沒有另一條平行的分支可以對照"
  - "任何從日誌挖評測題的做法，都會碰到同一個選擇。用「兩次不同的執行」構成反事實對照，還是用「一次執行裡的自我修正」？前者標籤更可靠；後者資料量更大，但也比較容易碰上「事後諸葛」的風險。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: parallel 的實際造法是把同一任務一成一敗的兩次嘗試配成一對，generator 讀完兩份完整軌跡各自找出岔路口，以成功那次在岔路口之前的部分當作前綴
    source_quote: "在同一個任務裡，挑一次成功、一次失敗的嘗試配成一對"
  - text: generator 讀完兩份完整軌跡，各自找出岔路口；成功那次在岔路口之前的部分當作前綴
    source_quote: "generator 讀完兩份完整軌跡，各自找出岔路口。"
  - text: 成功那次在岔路口之前的部分當作前綴
    source_quote: "成功那次在岔路口之前的部分當作前綴；兩個方向各寫成一段簡短、中性的描述，當作兩個候選。"
  importance: 3
  status: normal
- id: c10
  role: mechanism
  text: generator 被一組防呆規則綁著：不要事後諸葛（「較好的方向」只有看到失敗之後才說得出來，就拒絕這條軌跡，因為這樣的題目不需要判斷力）；不要稻草人（兩個候選必須都是當下合理的選擇，措辭平行、長度與語氣相近，不能出現「正確地」「較好」這類洩漏答案的詞）；差異要來自方向（parallel 要拒絕結果差異主要來自打錯字、當機、運氣、缺套件等跟方向無關的情況）
  source_quotes:
  - "generator 不是自由發揮，它被一組防呆規則綁著。"
  - "不要事後諸葛。 如果「較好的方向」只有看到失敗之後才說得出來，就拒絕這條軌跡，因為這樣的題目不需要判斷力。"
  - "不要稻草人。 兩個候選必須都是當下合理的選擇，措辭也要平行、長度與語氣相近，不能出現「正確地」「較好」這類洩漏答案的詞。"
  - "差異要來自方向。 parallel 要拒絕「結果差異主要來自打錯字、當機、運氣、缺套件」等跟方向無關的情況。"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c11
  role: mechanism
  text: detour 還多一道機械檢查：generator 必須依序引用四段軌跡原文（選擇被放棄方向的那一步、使它結束的失敗、選擇改正的那一步、改正成功的證據），程式檢查原文真的出現在被引用的那一步、四步的順序正確、失敗那段確實有失敗訊號（例如非零的結束碼或錯誤訊息），任何一項不過就丟掉
  source_quotes:
  - "detour 還多一道機械檢查：generator 必須引用四段軌跡原文，依序是選擇被放棄方向的那一步、使它結束的失敗、選擇改正的那一步、改正成功的證據。程式會檢查三件事：原文真的出現在被引用的那一步、四步的順序正確、失敗那段確實有失敗訊號（例如非零的結束碼或錯誤訊息）。任何一項不過就丟掉。"
  anchor_type: 設計參數
  importance: 4
  status: normal
- id: c12
  role: mechanism
  text: 論文再用四個裁判模型（都不是 generator）過濾兩次：trivial（太簡單）過濾只給裁判兩個候選的文字、沒有任務和軌跡，四個裁判全部答對就剔除，擋的是光看措辭就能猜到答案的題；undecidable（無法判定）過濾給裁判完整紀錄，只要有一個裁判不同意標籤就剔除，擋的是標籤和完整紀錄對不上的題。所以釋出的每一題，把軌跡藏起來時至少有一個裁判答錯，把完整紀錄攤開時四個裁判都認同標籤
  source_quotes:
  - "都不是 generator）過濾兩次："
  - "| 裁判看到什麼 | 只有兩個候選的文字，沒有任務和軌跡 | 完整紀錄：任務、前綴、兩條分支的完整後續、最終結果 |"
  - "| 剔除條件 | 四個裁判全部答對 | 只要有一個裁判不同意標籤 |"
  - "| 在擋什麼 | 光看措辭就能猜到答案的題 | 標籤和完整紀錄對不上的題 |"
  - "所以釋出的每一題都同時滿足兩件事：把軌跡藏起來時，至少有一個裁判答錯；把完整紀錄攤開時，四個裁判都認同標籤。"
  anchor_type: 設計參數
  figures:
  - file: figures/tasteful-agent/figure2.png
    article: tasteful-agent
    src: figure2.png
    caption: 圖 2 — Taste-Bench 的建構與過濾。parallel 比較同一任務的不同分支，detour 比較被放棄的方向與後來的改正，之後再經過過濾。（來源：原始論文 Figure 2。）
    sha256: dbba11e94d86eead13bb4af212bf79fd8329d2dbec666221afdef6197bf13d25
  importance: 3
  status: normal
- id: c13
  role: anchor
  text: 用這個方法造出的評測集 Taste-Bench：generator 提出的 4,657 個候選岔路口中，1,809 個通過 generator 自己依 rubric（評分準則）的檢查，729 個通過 trivial 過濾，最後通過 undecidable 過濾的剩 502 題，只有 10.8%
  source_quotes:
  - "generator 提出的 4,657 個候選岔路口，最後只有 10.8%、也就是 502 題通過全部過濾。"
  - "4,657 個候選中，有 1,809 個通過 generator 自己依 rubric（評分準則）的檢查"
  - "1,809 個通過 rubric 的候選中，729 個通過 trivial 過濾，最後通過 undecidable 過濾的剩 502 題"
  anchor_type: 實驗結果
  comparison_target: generator 提出的 4,657 個候選岔路口
  qualifiers:
  - text: 工程類原料是論文作者自己讓 GPT-5.4 與 GPT-5.5 的 agent 在 517 個 SWE-bench Pro 任務上跑出的 2,677 條有評分的軌跡
    source_quote: "工程類： 論文作者自己讓 GPT-5.4 與 GPT-5.5 的 agent 在 517 個 SWE-bench Pro 任務上跑出 2,677 條有評分的軌跡。"
  - text: 研究類原料是 47 個 AI R&D 任務的 1,132 次 agent 執行，軌跡取自 METR 公開釋出的 MALT 資料集
    source_quote: "研究類： 1,132 次 agent 執行，來自 47 個 AI R&D 任務（RE-Bench 與 HCAST 的研究子集），軌跡取自 METR 公開釋出的 MALT 資料集。"
  figures:
  - file: figures/tasteful-agent/figure8.png
    article: tasteful-agent
    src: figure8.png
    caption: 圖 3 — 每一格題型的篩選產出。帶子寬度正比於各階段剩下的候選數量：4,657 個候選中，1,809 個通過 generator 的 rubric，729 個通過 trivial 過濾，最終釋出 502 題。（來源：原始論文 Figure 8。）
    sha256: 465d93cd2fd1620e689ceaca319a06c7392db6932c8a9191ee0992f51cf66dbf
  importance: 2
  status: normal
- id: c14
  role: evaluation
  text: 實務上要預期的產出率：論文從 4,657 個候選只留下 502 題（10.8%），所以要準備大約十倍的候選量；裁判不能包含 generator 本身
  source_quotes:
  - "實務上要預期的產出率：論文從 4,657 個候選只留下 502 題（10.8%），所以要準備大約十倍的候選量。裁判不能包含 generator 本身。"
  anchor_type: 部落格判斷
  comparison_target: 論文的候選數 4,657 與釋出題數 502
  importance: 4
  status: normal
- id: c15
  role: evidence
  text: 人工審查：論文作者抽 100 題（70 題正式題、15 題被 trivial 過濾剔除、15 題被 undecidable 過濾剔除），兩位審查員先選自己會選哪個方向，再看後續過程與結果的摘要，判斷哪個決策比較好。有明確 A/B 判斷的 172 次判斷中，170 次與自動標籤一致（98.8%）；兩位審查員互相比較，兩人都有明確選擇的 74 題中 73 題選的一樣（一致率 98.6%），Cohen's kappa（扣掉碰巧選一樣之後的一致程度，1 代表完全一致）是 0.973
  source_quotes:
  - "論文作者抽 100 題（70 題是正式題，15 題被 trivial 過濾剔除，15 題被 undecidable 過濾剔除），請兩位審查員先選自己會選哪個方向，再看後續過程與結果的摘要，判斷哪個決策比較好。"
  - "結果是：在有明確 A/B 判斷的 172 次判斷中，170 次與自動標籤一致（98.8%）；兩位審查員互相比較（兩人都有明確選擇的 74 題中，73 題選的一樣），一致率 98.6%，Cohen's kappa（扣掉碰巧選一樣之後的一致程度，1 代表完全一致）是 \\( \\kappa = 0.973 \\)。"
  anchor_type: 實驗結果
  comparison_target: 98.8% 是審查員對自動標籤；98.6% 與 kappa 是兩位審查員彼此比較
  qualifiers:
  - text: 審查員是看過結果才判斷的，所以這驗證的是「標籤和紀錄對得上」，不是「這個決策真的造成了結果差異」
    source_quote: "審查員是看過結果才判斷的，所以這驗證的是「標籤和紀錄對得上」，不是「這個決策真的造成了結果差異」。"
  figures:
  - file: figures/tasteful-agent/table9.png
    article: tasteful-agent
    src: table9.png
    caption: 表 2 — 看過結果後的人工審查。每位審查員的保留判斷數與標籤一致率。（來源：原始論文 Table 9。）
    sha256: b09c0c07d8dac8dd58b219c42db7f5cd3d94c204d7ed857f569df6f37149eb6b
  importance: 3
  status: normal
- id: c16
  role: evaluation
  text: 人對標籤的 98.8% 驗證的是「自動標籤和記錄下來的結果對得上」，等於一致性檢查；它沒有驗證「這個決策真的是造成結果差異的原因」，也沒有驗證「這一題在決策當下真的答得出來」。審查員第一階段（看到結果之前）的選擇，等於人類在這個任務上的準確率，論文正文沒有報告這個數字
  source_quotes:
  - "比較 1：人對標籤。"
  - "所以 98.8% 驗證的是「自動標籤和記錄下來的結果對得上」，等於一致性檢查。它沒有驗證「這個決策真的是造成結果差異的原因」，也沒有驗證「這一題在決策當下真的答得出來」。另外，審查員第一階段（看到結果之前）的選擇，等於人類在這個任務上的準確率，可以拿來跟模型比較；論文正文沒有報告這個數字。"
  anchor_type: 部落格判斷
  comparison_target: 審查員的判斷對自動標籤（人對標籤）
  importance: 3
  status: normal
- id: c17
  role: evaluation
  text: 用 LLM 自動產生標籤的資料集，品質檢查要把「人對標籤」和「人對人」兩件事分開報告：前者回答標籤是否可信，後者回答這個任務本身有沒有清楚的答案
  source_quotes:
  - "用 LLM 自動產生標籤的資料集，品質檢查要把「人對標籤」和「人對人」兩件事分開報告：前者回答標籤是否可信，後者回答這個任務本身有沒有清楚的答案。"
  anchor_type: 部落格判斷
  importance: 4
  status: normal
- id: c18
  role: evaluation
  text: blog 認為研究上這篇的新意不高：用結果標註中途決策，是 process reward（用後續把任務跑完的結果來評每一步）這條線的延伸；蒸餾部分是 context distillation 的變體；新的是把這些東西套到 agent 長任務的岔路口，並給出一套可複製的造題流程。工程上，價值集中在造題那一塊，論文本身只有一項值得帶走：造題配方
  source_quotes:
  - "研究上，這篇的新意不高：用結果標註中途決策，是 process reward（用後續把任務跑完的結果，也就是 rollout，來評每一步）這條線的延伸；蒸餾部分是 context distillation 的變體。"
  - "新的是把這些東西套到 agent 長任務的岔路口，並且給出一套可複製的造題流程。"
  - "工程上，價值集中在造題那一塊。"
  - "論文本身只有一項值得帶走：造題配方"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c19
  role: evaluation
  text: blog 認為「同一個任務的兩次嘗試如果在中途分歧之前完全相同，結果的差異就主要來自分歧點的那個決定，所以誰的結果好可以當成這個決定好不好的標籤」這個推論不依賴特定模型，也不依賴特定領域，所以耐久；要用這套配方，需要的原料有三樣：同一個任務的多次執行紀錄、每次執行一個可信的結果訊號（測試通過與否、評分）、一個能讀完整軌跡的 generator 模型
  source_quotes:
  - "但同一個任務的兩次嘗試，如果在中途分歧之前完全相同，結果的差異就主要來自分歧點的那個決定，所以「誰的結果好」可以當成「這個決定好不好」的標籤。這個推論不依賴特定模型，也不依賴特定領域，所以耐久。需要的原料有三樣："
  - "同一個任務的多次執行紀錄。"
  - "每次執行一個可信的結果訊號（測試通過與否、評分）。"
  - "一個能讀完整軌跡的 generator 模型。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
```
