---
id: skillstate-state-replaces-history
title: SKILL.state 把「現在的世界狀態」和「歷史文字」分開：每一步只看任務指令、結構化狀態、最新觀察，推理用完就丟，prompt 就不再隨步數變長，總成本從平方量級降到線性量級
type_hint: 方法
context_type: bound_to_source
sources:
- article: skill-state
  article_title: "SKILL.state 論文：Agent 不留對話歷史只留狀態，200 步任務省 41 倍 token"
  url: https://datasciocean.com/paper-intro/skill-state/
  sections:
  - Agent 跑越久越貴：把對話歷史換成一份狀態
  - 對話式執行的兩個問題：越疊越長，舊資訊賴著不走
  - 三樣輸入、三樣輸出，狀態用合併來更新
  - 執行迴圈：推理用完就丟，狀態整份換掉
  - 走一遍倉儲出貨的一步
  - 狀態欄位按 domain 設計一次
  - 驗證擋得住格式錯誤，擋不住語意錯誤
  - 總成本為什麼從平方降到線性
  - 倉儲環境：任務夠長才拉開差距，最大的差距在 token
  - 看數字前的保留：長任務只在自建環境測過
  - 它會在哪裡失敗：小模型的錯誤與三種失效情境
  - 結論：省成本可以期待，全面變準還不行
  first_appearance: true
parent: null
related:
  - llm-patch-validation-format-not-semantics
  - skillstate-results-cost-vs-accuracy
  - stateful-and-budget-matched-controls
  - discard-history-relevance-at-the-time
  - intermediate-results-out-of-context
  - context-chunk-keep-offload-compress-delete
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: SKILL.state 把「現在的世界狀態」和「歷史文字」分開，prompt 就不再隨步數變長：模型每一步只看任務指令、結構化狀態、最新觀察，思考過程用完就丟，整體成本從隨步數平方成長，變成線性成長
  source_quotes:
  - "SKILL.state 用一個簡單的想法解決一個很具體的問題：把「現在的世界狀態」和「歷史文字」分開，prompt 就不再隨步數變長。"
  - "模型的思考過程用完就丟，只把「狀態該怎麼改」的結論留下來。這樣 prompt 大小就跟已經走了幾步無關，整體成本從隨步數平方成長，變成線性成長。"
  anchor_type: 設計參數
  qualifiers:
  - text: 每一步的 prompt 大小是「大致固定」：狀態可能隨任務複雜度緩慢變化，但跟走了幾步無關
    source_quote: "...大小大致固定（Σ 可能隨任務複雜度緩慢變化，但跟走了幾步無關）"
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
  text: 今天常見的 agent 做法叫 ReAct：模型每一步先寫一段推理、選一個動作，環境回傳觀察，這三樣都接到 prompt 後面，下一步再整段讀一次。這種對話式執行有兩個問題：prompt 長度隨執行步數增長，token 成本與延遲跟著漲；舊資訊會「賴著不走」，模型得自己分辨哪些還有效
  source_quotes:
  - "今天常見的 agent 做法叫 ReAct：模型每一步先寫一段推理、選一個動作，環境回傳觀察，這三樣都接到 prompt 後面，下一步再整段讀一次。"
  - "這種對話式執行有兩個具體問題。第一個是 prompt 長度隨執行步數增長，token 成本與延遲跟著漲"
  - "第二個問題是舊資訊會「賴著不走」，模型得自己分辨哪些還有效。"
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 每一步餵給模型的固定是三樣：任務的固定指令 P（整個執行過程不變）、第 t 步當下的結構化執行狀態 Σ_t（一個 JSON 字典，記錄世界現在的樣子）、這一步環境傳來的最新觀察 O_t。模型輸出三樣：推理過程 R_t（用完立刻丟掉，永遠不會出現在下一步的 prompt 裡）、狀態的差異 ΔΣ_t（一個 JSON 字典，描述這一步要對狀態做哪些修改）、要執行的動作 a_t
  source_quotes:
  - "每一步餵給模型的東西固定是三樣。"
  - '\( P \) 是任務的固定指令（procedural specification），例如「你是倉儲管理員，可用動作是 Store/Ship/Move/Wait」，整個執行過程不變。\( \Sigma_t \) 是第 \( t \) 步當下的結構化執行狀態，一個 JSON 字典，記錄世界現在的樣子'
  - '\( O_t \) 是這一步環境傳來的最新觀察'
  - '模型看完這三樣，輸出三樣東西。\( R_t \) 是推理過程，也就是 chain-of-thought（模型一步步寫出來的思考），用完立刻丟掉，永遠不會出現在下一步的 prompt 裡。\( \Delta\Sigma_t \) 是狀態的「差異」，一個 JSON 字典，描述這一步要對狀態做哪些修改。\( a_t \) 是要執行的動作。'
  anchor_type: 設計參數
  figures:
  - file: figures/skill-state/figure1.png
    article: skill-state
    src: figure1.png
    caption: 圖 1 — SKILL.state 架構總覽：左邊的傳統做法 prompt 隨步數變長，右邊的 SKILL.state 維持固定大小（來源：原始論文 Figure 1。）
    sha256: 8d22fcb6c6299ffc6718ba96f8eba19c975c979bf32c027eaa1a7a57f33a8b2a
  importance: 2
  status: normal
- id: c5
  role: mechanism
  text: 狀態用「帶 null 刪除語意的字典合併」更新：ΔΣ_t 裡有的 key，直接覆蓋舊狀態裡同名 key 的值；某個 key 的值被設成 null，代表把它從狀態裡整個刪掉；ΔΣ_t 沒提到的 key 維持原樣。下一步的狀態等於這一步的狀態合併上差異
  source_quotes:
  - '論文定義了一個運算子 \( \oplus \)，叫「帶 null 刪除語意的字典合併」：\( \Delta\Sigma_t \) 裡有的 key，直接覆蓋舊狀態裡同名 key 的值；某個 key 的值被設成 `null`，代表把它從狀態裡整個刪掉；\( \Delta\Sigma_t \) 沒提到的 key 維持原樣。寫成公式就是下一步的狀態等於這一步的狀態合併上差異：'
  - '\Sigma_{t+1} = \Sigma_t \oplus \Delta\Sigma_t'
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c6
  role: mechanism
  text: 執行迴圈裡，Runtime（負責呼叫模型、執行動作的外層程式）先檢查 ΔΣ_t 的格式是否合法，合法才套用更新、執行動作，推理 R_t 永久丟棄；不合法就回滾，要求模型重新輸出。傳統做法每一步都在 prompt 後面加一段新的，SKILL.state 每一步都把狀態整份換掉
  source_quotes:
  - "Runtime（負責呼叫模型、執行動作的外層程式）收到觀察"
  - 'Runtime 檢查 \( \Delta\Sigma_t \) 的格式是否合法。合法就往下走；不合法就回滾，要求模型重新輸出。'
  - '套用更新：\( \Sigma_{t+1} = \Sigma_t \oplus \Delta\Sigma_t \)。'
  - '執行動作 \( a_t \)，\( R_t \) 永久丟棄。'
  - "傳統做法每一步都在 prompt 後面加一段新的，SKILL.state 每一步都把狀態整份換掉。"
  anchor_type: 設計參數
  qualifiers:
  - text: 驗證擋得住「格式不合法」，擋不住「格式合法、但語意錯誤」的輸出，例如會誤刪重要資訊的 patch
    source_quote: "驗證擋得住「格式不合法」，擋不住「格式合法、但語意錯誤」的輸出。比方說模型輸出一個會誤刪重要資訊的 patch，格式完全沒問題，驗證抓不到"
  importance: 3
  status: normal
- id: c7
  role: anchor
  text: 論文附錄的倉儲例子：item_12 放在 shelf_42，觀察是「Customer ordered item_12.」，模型輸出的 state_patch 把 shelf_42 設成 null，動作是「Ship item_12 shelf_42」；套用後 shelf_42 被刪除，沒被提到的 shelf_43 維持 "item_9"。下一輪的 prompt 只有指令、新狀態和新觀察，推理過程和上一步的觀察都沒有出現
  source_quotes:
  - "論文附錄用這個倉儲情境示範一次出貨的完整流程"
  - '開始時，item_12 放在 shelf_42。Runtime 收到觀察 \( O_t \)：「Customer ordered item_12.」'
  - '"state_patch": { "inventory": { "shelf_42": null } },'
  - '"action": "Ship item_12 shelf_42"'
  - 'shelf_42 | "item_12" | null（被刪除／清空）'
  - 'shelf_43 | "item_9" | "item_9"（沒被提到，維持原樣）'
  - '下一輪的 prompt 就是 \( (P, \Sigma_{t+1}, O_{t+1}) \)。推理過程 \( R_t \) 沒有出現，上一步的觀察 \( O_t \) 也沒有出現：模型只看到現在的狀態和最新的觀察，沒有半點歷史文字。'
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 3
  status: normal
- id: c8
  role: mechanism
  text: 總成本的量級：傳統做法第 t 步的 prompt 長度跟 t 成正比，T 步加起來是 O(T²)；SKILL.state 每一步的 prompt 長度是指令、狀態、觀察三者的長度相加，跟 t 無關，T 步加起來是 O(T)。每一步的長度隨 t 線性增加，把這些線性增加的量再加總一次，就變成平方量級
  source_quotes:
  - '傳統做法第 \( t \) 步的 prompt 記作 \( C_t \)，長度 \( |C_t| \) 跟 \( t \) 成正比，是 \( O(t) \)。SKILL.state 第 \( t \) 步的 prompt 記作 \( P_t \)（注意不是前面的任務指令 \( P \)），長度是 \( O(|P|+|\Sigma|+|O|) \)，也就是指令、狀態、觀察三者的長度相加，跟 \( t \) 無關。'
  - '\sum_{t=1}^{T} |C_t| = O(T^2) \qquad \sum_{t=1}^{T} |P_t| = O(T)'
  - "每一步的長度隨 \\( t \\) 線性增加，把這些線性增加的量再加總一次，就變成平方量級。"
  anchor_type: 數學推導
  qualifiers:
  - text: 狀態可能隨任務複雜度慢慢變大，例如關聯密集的環境裡，狀態會隨分支、PR 數量增加而變胖；但它的變化只跟當下世界有多複雜有關，跟已經走了幾步無關，所以是每步 O(1)、總和 O(T)，而不是每步剛好等於某個固定常數
    source_quote: "狀態 \\( \\Sigma \\) 可能隨任務複雜度慢慢變大，例如關聯密集的環境裡，狀態會隨分支、PR 數量增加而變胖。但它的變化只跟「當下世界有多複雜」有關，跟「已經走了幾步」無關，所以說每步 \\( O(1) \\)、總和 \\( O(T) \\)，而不是每步剛好等於某個固定常數。"
  importance: 2
  status: normal
- id: c9
  role: anchor
  text: 用數字驗證：走 10 步、每一步的長度簡化成單位長度，傳統做法是 1, 2, 3, ..., 10，加起來是 55；SKILL.state 是 10 個 1 相加，等於 10
  source_quotes:
  - "假設走 10 步，把每一步的長度簡化成「單位長度」：傳統做法是 1, 2, 3, ..., 10，SKILL.state 是 1, 1, ..., 1。傳統做法加起來是 \\( 1+2+\\cdots+10=(1+10)\\times10/2=55 \\)"
  - "SKILL.state 是 10 個 1 相加，\\( 1\\times10=10 \\)，量級是 \\( T \\)。"
  anchor_type: 數學推導
  comparison_target: 同樣走 10 步，傳統做法（每步長度隨步數加 1）對比 SKILL.state（每步 1 單位）的總長度
  qualifiers:
  - text: 「1 單位」是簡化，SKILL.state 每一步的大小其實是指令、狀態、觀察的長度相加
    source_quote: "「1 單位」是簡化。SKILL.state 每一步的大小其實是 \\( |P|+|\\Sigma|+|O| \\)"
  importance: 3
  status: normal
- id: c10
  role: evidence
  text: 實測對得上理論：倉儲環境的 Table 1 裡，任務長度 T 從 100 加倍到 200 時，Stateful 對照組（同樣有結構化狀態，但還保留完整對話歷史）的總 token 成長了約 4.7 倍，接近理論預期的 4 倍；SKILL.state 只成長約 1.9 倍，接近理論預期的 2 倍
  source_quotes:
  - '後面的 Table 1 裡，\( T \) 從 100 加倍到 200 時，Stateful 對照組（同樣有結構化狀態，但還保留完整對話歷史）的總 token 成長了約 4.7 倍，接近理論預期的 4 倍（\( 2^2 \)）；SKILL.state 只成長約 1.9 倍，接近理論預期的 2 倍（\( 2^1 \)）。'
  - "Table 1 是倉儲環境的主表"
  anchor_type: 實驗結果
  comparison_target: 同一做法在 T=100 時的總 token；並對照理論預期的 4 倍（平方量級）與 2 倍（線性量級）
  qualifiers:
  - text: 最有說服力的長任務數字，全部來自論文自己設計、自己控制的合成環境
    source_quote: "最有說服力的長任務數字，全部來自自己設計、自己控制的合成環境。"
  figures:
  - file: figures/skill-state/table1.png
    article: skill-state
    src: table1.png
    caption: 表 1 — 倉儲環境的長任務 scaling：準確率與 token 消耗隨任務長度的變化（來源：原始論文 Table 1。）
    sha256: 3a1e13c1b1b813134db90665b0a95693a5109cf947fdf86bf1d7599d3753f237
  importance: 2
  status: normal
- id: c11
  role: mechanism
  text: 狀態要記哪些欄位（狀態的 schema）是為整個 domain（同一類任務）設計一次，不是每個任務各設計一套。例如 InterCode CTF 的題目涵蓋逆向工程、鑑識、密碼學、二進位漏洞利用，卻全部共用同一組欄位：已找到的 flag、已試過的假設與指令、目前操作的檔案、目前工作目錄、指令執行摘要；好處是不用每個任務重新設計狀態格式，不同任務還能共用同一套 runtime 程式碼
  source_quotes:
  - "狀態要記哪些欄位，也就是狀態的 schema，是為整個 domain（同一類任務）設計一次，不是每個任務各設計一套。"
  - "InterCode CTF（100 道 Linux 解謎題，agent 要下 bash 指令找出藏起來的 flag 字串）的題目五花八門，涵蓋逆向工程、鑑識、密碼學、二進位漏洞利用，卻全部共用同一組欄位：已找到的 flag、已試過的假設與指令、目前操作的檔案、目前工作目錄、指令執行摘要。好處很直接：不用每個任務重新設計狀態格式，不同任務還能共用同一套 runtime 程式碼。"
  anchor_type: 設計參數
  qualifiers:
  - text: 前提是這個 domain 事先就知道該追蹤哪些欄位；schema 沒辦法事先固定、必須邊執行邊發現該追蹤什麼時，這套做法就不適用（論文在 Limitations 一節自己承認）
    source_quote: "前提是這個 domain 事先就知道該追蹤哪些欄位。如果 schema 沒辦法事先固定、必須邊執行邊發現該追蹤什麼，這套做法就不適用。這是論文在 Limitations 一節自己承認的第一個失效情境。"
  importance: 3
  status: normal
- id: c12
  role: qualifier
  text: 多個 agent 共享同一份狀態時，同時寫入會衝突；論文只說「可以自然擴展」，沒有實作也沒有測試
  source_quotes:
  - "論文另外承認兩個附帶限制。多個 agent 共享同一份狀態時，同時寫入會衝突，論文只說「可以自然擴展」，沒有實作也沒有測試。"
  anchor_type: 原作者解讀
  importance: 4
  status: normal
- id: c13
  role: evaluation
  text: 這篇論文的工程價值很高，尤其在成本上；研究上的新意則中等偏低。核心概念早就存在：MemGPT、LangGraph 的狀態區塊，以及 Dialogue State Tracking 都做過類似的事，論文的貢獻是證明和系統化衡量，不是提出新概念
  source_quotes:
  - "這篇論文的工程價值很高，尤其在成本上；研究上的新意則中等偏低。"
  - "但核心概念早就存在：MemGPT（讓 LLM 自己管理長期記憶的系統）、LangGraph 的狀態區塊，以及 Dialogue State Tracking（對話系統裡追蹤使用者需求的技術）都做過類似的事，論文的貢獻是證明和系統化衡量，不是提出新概念。"
  anchor_type: 部落格判斷
  importance: 4
  status: normal
```
