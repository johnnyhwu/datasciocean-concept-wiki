---
id: discard-history-relevance-at-the-time
title: 要不要丟掉歷史，關鍵問題不是模型夠不夠強，而是相關性能不能在資訊出現的當下就被正確判斷；拿掉「回頭核對原始資料」這條路，就等於把賭注全押在當下的判斷上
type_hint: 判斷
context_type: evidence_from_single_source
sources:
- article: skill-state
  article_title: "SKILL.state 論文：Agent 不留對話歷史只留狀態，200 步任務省 41 倍 token"
  url: https://datasciocean.com/paper-intro/skill-state/
  sections:
  - Agent 跑越久越貴：把對話歷史換成一份狀態
  - 對話式執行的兩個問題：越疊越長，舊資訊賴著不走
  - 倉儲環境：任務夠長才拉開差距，最大的差距在 token
  - 它會在哪裡失敗：小模型的錯誤與三種失效情境
  - 實務上該選 ReAct 還是 SKILL.state
  - 結論：省成本可以期待，全面變準還不行
  - 看數字前的保留：長任務只在自建環境測過
  - 三樣輸入、三樣輸出，狀態用合併來更新
  - 走一遍倉儲出貨的一步
  - 軟體版本庫：中途一度輸給 Stateful
  first_appearance: true
parent: null
related:
  - skillstate-state-replaces-history
  - llm-patch-validation-format-not-semantics
  - skillstate-results-cost-vs-accuracy
  - stateful-and-budget-matched-controls
  - subagent-boundary-lossy-handoff
  - context-chunk-keep-offload-compress-delete
  - tree-routing-bounded-by-node-descriptions
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 要不要丟掉歷史，關鍵問題不是模型夠不夠強，而是相關性能不能在資訊出現的當下就被正確判斷；架構如果拿掉了「回頭核對原始資料」這條路，就等於把賭注全押在當下的判斷上
  source_quotes:
  - "要不要丟掉歷史，關鍵問題不是模型夠不夠強，而是相關性能不能在資訊出現的當下就被正確判斷。架構如果拿掉了「回頭核對原始資料」這條路，就等於把賭注全押在當下的判斷上。"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: "SKILL.state 是 Google 與 Purdue 的論文《SKILL.state: Scalable Long-Horizon Agent Skills》提出的做法：模型每一步只看三樣東西：任務指令、一份描述「世界現在長什麼樣」的結構化狀態、這一步的最新觀察；模型的思考過程用完就丟，只把「狀態該怎麼改」的結論留下來"
  source_quotes:
  - "這是 Google 與 Purdue 的論文《SKILL.state: Scalable Long-Horizon Agent Skills》提出的做法。模型每一步只看三樣東西：任務指令、一份描述「世界現在長什麼樣」的結構化狀態、這一步的最新觀察。模型的思考過程用完就丟，只把「狀態該怎麼改」的結論留下來。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: 對照的另一端是 ReAct（保留歷史）：模型每一步先寫一段推理、選一個動作，環境回傳觀察，這三樣都接到 prompt 後面，下一步再整段讀一次
  source_quotes:
  - "今天常見的 agent 做法叫 ReAct：模型每一步先寫一段推理、選一個動作，環境回傳觀察，這三樣都接到 prompt 後面，下一步再整段讀一次。"
  - "傾向 ReAct（保留歷史） | 傾向 SKILL.state（丟棄歷史）"
  anchor_type: 背景說明
  importance: 2
  status: normal
- id: c4
  role: mechanism
  text: 整套設計依賴一個前提：執行狀態可以成為未來執行的充分統計量，意思是過去發生的一切，只要當下就被正確寫進狀態，就不需要保留原始文字
  source_quotes:
  - "整套設計依賴一個前提：執行狀態可以成為未來執行的充分統計量。意思是過去發生的一切，只要當下就被正確寫進狀態，就不需要保留原始文字。"
  anchor_type: 原作者解讀
  importance: 2
  status: normal
- id: c5
  role: qualifier
  text: 論文自己承認，這個前提在三種情境下會失效：schema 沒辦法事先固定，必須邊執行邊發現該追蹤哪些欄位；某個早期觀察，當下沒被判斷為重要，後來才發現有關，因為沒寫進狀態，事後也找不回來；任務的目標就是歷史軌跡本身，例如稽核、debug 溯源、解釋過去做了什麼決策，丟掉歷史直接跟任務目標衝突
  source_quotes:
  - "論文自己承認，這個前提在三種情境下會失效："
  - "Schema 沒辦法事先固定：必須邊執行邊發現該追蹤哪些欄位。"
  - "某個早期觀察，當下沒被判斷為重要，後來才發現有關：因為沒寫進狀態，事後也找不回來。"
  - "任務的目標就是歷史軌跡本身：例如稽核、debug 溯源、解釋過去做了什麼決策。這種任務下，丟掉歷史直接跟任務目標衝突。"
  anchor_type: 原作者解讀
  importance: 2
  status: normal
- id: c6
  role: evaluation
  text: 第二種失效（早期觀察後來才發現有關）是三者中最現實、最容易在正式環境踩到的一項；整個架構最根本的賭注，是賭模型在當下就能做出正確的取捨，一旦賭錯，沒有回頭路
  source_quotes:
  - "這是三者中最現實、最容易在正式環境踩到的一項。整個架構最根本的賭注，是賭模型在當下就能做出正確的取捨，一旦賭錯，沒有回頭路。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c7
  role: evaluation
  text: 任何為了效率丟掉原始資料、只留摘要或萃取結果的系統，都在做同一種賭注；這個問題不限於 agent 設計，值得在任何「要不要丟棄原始資料」的系統設計裡重新問一次
  source_quotes:
  - "任何為了效率丟掉原始資料、只留摘要或萃取結果的系統，都在做同一種賭注，所以比論文結論本身更值得留下的，就是這個問題：它不限於 agent 設計，值得在任何「要不要丟棄原始資料」的系統設計裡重新問一次。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c8
  role: mechanism
  text: 「保留過去的動作紀錄比較有容錯空間」的「容錯」有兩種意義要拆開看：第一種是事後可以追溯、可以除錯，這方面保留歷史確實佔優勢，SKILL.state 一旦把資訊丟掉，就真的回不去了；第二種是長任務的準確率會不會因為保留歷史而更穩
  source_quotes:
  - "一個常見的直覺是：保留過去的動作紀錄比較有容錯空間，對強模型來說應該利大於弊。這個「容錯」其實有兩種意義，要拆開看。"
  - "第一種是事後可以追溯、可以除錯。這方面保留歷史確實佔優勢，出錯後還能回頭檢查原始資料；SKILL.state 一旦把資訊丟掉，就真的回不去了"
  - "第二種是長任務的準確率會不會因為保留歷史而更穩。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c9
  role: evidence
  text: 第二種容錯被倉儲環境的實測反駁：即使用論文測過最強的模型 Gemini-3-Flash，保留完整歷史的 Prompt(ReAct) 準確率還是從任務長度 T=10 的 0.90 一路跌到 T=200 的 0.74，標準差還放大了 7 倍
  source_quotes:
  - "前面 Table 1 的數字反駁了這個直覺：即使用論文測過最強的模型 Gemini-3-Flash，保留完整歷史的 Prompt(ReAct) 準確率還是從 0.90 一路跌到 0.74，標準差還放大了 7 倍。"
  - "Table 1 是倉儲環境的主表"
  - "Prompt 從 \\( T=10 \\) 的 \\( 0.90\\pm0.02 \\) 跌到 \\( T=200 \\) 的 \\( 0.74\\pm0.14 \\)"
  anchor_type: 實驗結果
  comparison_target: 同一做法（Prompt(ReAct)）在 T=10 時的準確率與標準差
  qualifiers:
  - text: 最有說服力的長任務數字，全部來自論文自己設計、自己控制的合成環境
    source_quote: "最有說服力的長任務數字，全部來自自己設計、自己控制的合成環境。"
  - text: 在軟體版本庫環境，T=25 時保留完整歷史的 Stateful 對照組反而贏過只留狀態的 SKILL.state（0.94 對 0.88）
    source_quote: "而它在軟體版本庫 \\( T=25 \\) 時甚至贏過 SKILL.state，就是前面那個 Stateful 0.94、SKILL.state 0.88 的反例。"
  importance: 2
  status: normal
- id: c10
  role: evaluation
  text: 論文引用 lost-in-the-middle 現象（Liu et al., 2024）來解釋長 context 的準確率退化：模型技術上看得到長 context 裡的資訊，不代表能可靠地用到。blog 推論這不是推理能力不夠，所以換成更強的前沿模型，這個弱點也不會消失，只是程度可能緩和；「強模型加保留歷史，利大於弊」在短中距離的任務成立，在長任務上則被實測數據推翻
  source_quotes:
  - "論文引用 lost-in-the-middle 現象（Liu et al., 2024）來解釋長 context 的準確率退化：模型技術上看得到長 context 裡的資訊，不代表能可靠地用到。我的推論是，這不是推理能力不夠，所以換成更強的前沿模型，這個弱點也不會消失，只是程度可能緩和。「強模型加保留歷史，利大於弊」在短中距離的任務成立，在長任務上則被實測數據推翻。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 日期
  qualifiers:
  - text: 倉儲環境短任務（T=10）打平的是 Memory、Stateful 與 SKILL.state（都是 1.00）
    source_quote: "短任務（\\( T=10 \\)）沒有準確率優勢：主要對照組 Memory、Stateful 和 SKILL.state 都是 1.00，打平。"
  - text: Prompt(ReAct) 在 T=10 時是 0.90±0.02
    source_quote: "Prompt 從 \\( T=10 \\) 的 \\( 0.90\\pm0.02 \\)"
  - text: 最有說服力的長任務數字，全部來自論文自己設計、自己控制的合成環境
    source_quote: "最有說服力的長任務數字，全部來自自己設計、自己控制的合成環境。"
  importance: 3
  status: normal
- id: c11
  role: mechanism
  text: 決策表的前三條軸線：相關性事後才發現有用（debug、探索式研究）傾向 ReAct，當下就能判斷這筆該不該記（倉儲、資料庫狀態這類）傾向 SKILL.state；軌跡本身是產出物（稽核、合規、解釋過程）傾向 ReAct，只要最終狀態或結果對傾向 SKILL.state；狀態密集互相依賴（Git 圖、連鎖財務計算）傾向 ReAct，稀疏獨立（像 500 個互不相關的貨架）傾向 SKILL.state
  source_quotes:
  - "相關性何時能判斷 | 事後才發現某個觀察有用（debug、探索式研究） | 當下就能判斷這筆該不該記（倉儲、資料庫狀態這類）"
  - "軌跡本身是不是產出物 | 是（稽核、合規、解釋過程） | 否（只要最終狀態或結果對）"
  - "狀態的關聯密度 | 密集互相依賴（Git 圖、連鎖財務計算） | 稀疏獨立（像 500 個互不相關的貨架）"
  - "傾向 ReAct（保留歷史） | 傾向 SKILL.state（丟棄歷史）"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 2
  status: normal
- id: c12
  role: mechanism
  text: 關聯密集時，patch（模型輸出的狀態差異，描述這一步要對狀態做哪些修改）一旦出錯，後果會無聲擴散，而且無法回頭比對原文；關聯稀疏時，錯誤的影響範圍被限制住
  source_quotes:
  - "關聯密集時，patch 一旦出錯，後果會無聲擴散，而且無法回頭比對原文；關聯稀疏時，錯誤的影響範圍被限制住。"
  - '\( \Delta\Sigma_t \) 是狀態的「差異」，一個 JSON 字典，描述這一步要對狀態做哪些修改。'
  - '`state_patch` 就是 \( \Delta\Sigma_t \)'
  anchor_type: 部落格推論
  importance: 3
  status: normal
- id: c13
  role: mechanism
  text: 決策表的後三條軸線：預期執行長度短到中（關聯稀疏時約 25 步以內）時兩者準確率打平、ReAct 比較簡單，長（100 步以上）時保留歷史的做法準確率退化、變異放大，狀態型維持穩定；弱模型時合法但語意錯誤的 patch 被無感套用是重大風險，強模型能降低這個風險；對成本或延遲不敏感（呼叫次數少、預算充足）傾向 ReAct，敏感（高頻呼叫、要上正式環境）傾向 SKILL.state
  source_quotes:
  - "預期執行長度 | 短到中（關聯稀疏時約 25 步以內）：兩者準確率打平，ReAct 比較簡單 | 長（100 步以上）：保留歷史的做法準確率退化、變異放大，狀態型維持穩定"
  - "模型能力 | 弱模型：合法但語意錯誤的 patch 被無感套用是重大風險 | 強模型能降低這個風險"
  - "對成本／延遲的敏感度 | 不敏感（呼叫次數少、預算充足） | 敏感（高頻呼叫、要上正式環境）"
  - "傾向 ReAct（保留歷史） | 傾向 SKILL.state（丟棄歷史）"
  anchor_type: 部落格判斷
  comparison_target: 決策表中傾向 ReAct（保留歷史）的一側對比傾向 SKILL.state（丟棄歷史）的一側，在不同預期執行長度下的準確率
  qualifiers:
  - text: 換到軟體版本庫就有 T=25 這個反例；SKILL.state 在這張表的標準差也偏大（±0.08），結果不算穩定
    source_quote: "換到軟體版本庫就有 \\( T=25 \\) 這個反例，論文正文完全沒有提到。SKILL.state 在這張表的標準差也偏大（\\( \\pm0.08 \\)），結果不算穩定。"
  - text: 倉儲環境短任務（T=10）打平的是 Memory、Stateful 與 SKILL.state（都是 1.00）
    source_quote: "短任務（\\( T=10 \\)）沒有準確率優勢：主要對照組 Memory、Stateful 和 SKILL.state 都是 1.00，打平。"
  - text: Prompt(ReAct) 在 T=10 時是 0.90±0.02
    source_quote: "Prompt 從 \\( T=10 \\) 的 \\( 0.90\\pm0.02 \\)"
  - text: 這組倉儲結果用的是論文測過最強的模型 Gemini-3-Flash
    source_quote: "即使用論文測過最強的模型 Gemini-3-Flash"
  - text: 換成公開權重的 Gemma-4-31B，SKILL.state 在 T=100 的倉儲任務上準確率只剩 0.42
    source_quote: "換成公開權重的 Gemma-4-31B，SKILL.state 在 \\( T=100 \\) 的倉儲任務上準確率只剩 0.42。"
  - text: 最有說服力的長任務數字，全部來自論文自己設計、自己控制的合成環境
    source_quote: "最有說服力的長任務數字，全部來自自己設計、自己控制的合成環境。"
  - text: 「25 步以內打平」只適用於關聯稀疏的環境，關聯密集時這條線會更早出現，例如軟體版本庫在 T=25 就已經反過來輸
    source_quote: "「25 步以內打平」也只適用於關聯稀疏的環境，關聯密集時這條線會更早出現，例如軟體版本庫在 \\( T=25 \\) 就已經反過來輸。"
  - text: 前沿模型只是沒測過，沒有證據顯示完全免疫
    source_quote: "但前沿模型只是沒測過，沒有證據顯示完全免疫"
  importance: 3
  status: normal
- id: c14
  role: evaluation
  text: 先問這一句：這個 domain 的狀態，能不能在事情發生的當下就決定該不該記？如果能（結構清楚、關聯稀疏、任務夠長），選 SKILL.state；如果不能，或需要稽核軌跡，或狀態關聯密集，優先考慮 ReAct，或「狀態加有限歷史」的混合做法
  source_quotes:
  - "這個 domain 的狀態，我能不能在事情發生的當下就決定該不該記？如果能（結構清楚、關聯稀疏、任務夠長），選 SKILL.state；如果不能，或需要稽核軌跡，或狀態關聯密集，優先考慮 ReAct，或「狀態加有限歷史」的混合做法。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c15
  role: evaluation
  text: blog 推論，如果不確定「當下就能正確判斷什麼該記」這個假設成不成立，「狀態加一小段近期歷史」的混合做法，可能比論文給的兩個極端都務實：有把握的部分交給結構化狀態，同時留一小段滾動歷史當安全網，萬一 schema 漏掉了什麼，近期歷史還能補救；成本介於兩者之間
  source_quotes:
  - "我的推論是，如果不確定「當下就能正確判斷什麼該記」這個假設成不成立，「狀態加一小段近期歷史」的混合做法，可能比論文給的兩個極端都務實：有把握的部分交給結構化狀態，同時留一小段滾動歷史當安全網，萬一 schema 漏掉了什麼，近期歷史還能補救。成本介於兩者之間"
  anchor_type: 部落格推論
  importance: 3
  status: normal
- id: c16
  role: evaluation
  text: 如果你正在做會跑很久的 agent，可以先替自己的 domain 列一份狀態欄位，再找出哪些資訊沒辦法在出現的當下決定該不該記：那些地方，就是還需要保留歷史的地方
  source_quotes:
  - "如果你正在做會跑很久的 agent，可以先替自己的 domain 列一份狀態欄位，再找出哪些資訊沒辦法在出現的當下決定該不該記：那些地方，就是你還需要保留歷史的地方。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
```
