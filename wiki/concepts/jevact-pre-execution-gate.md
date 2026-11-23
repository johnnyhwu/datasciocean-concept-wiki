---
id: jevact-pre-execution-gate
title: LLM agent 說錯一句話還能更正，做錯一件事就難了；JevAct 在「提出動作」和「執行動作」之間加一道閘門，只攔寫入型工具呼叫與放棄或轉接真人兩類動作，由便宜的決策模型 Kev 只在很有把握時才擋下
type_hint: 方法
context_type: bound_to_source
sources:
- article: jevact
  article_title: "JevAct：讓 AI Agent 三思而後行的執行前閘門"
  url: https://datasciocean.com/paper-intro/jevact/
  sections:
  - LLM agent 最怕做錯事：JevAct 在動手前加一道閘門
  - 說錯能更正，做錯難挽回：為什麼要在執行前擋
  - 一張地圖：兩層、兩個 gate
  - 決策迴圈：被擋的提案帶著回饋重來
  - 觸發分流：只有寫入與放棄會被檢查
  - Kev 只在 95% 有把握時才說「不」
  - 兩道品管：不用正確答案也能修程式、刪爛題
  - write gate 走一遍：一張還沒確認就要取消的訂位
  - 放棄前清單：轉接真人之前，該做的步驟做了沒
  - hand-off check 怎麼判
  - Jev、Kev、JevLoop、JevAct 四個名字
  first_appearance: true
parent: null
related:
  - policy-split-derive-questions-rules
  - handoff-checklist-not-discussed-not-ruled-out
  - jevact-results-gain-source
  - policy-checks-blind-to-user-request
  - claude-code-permission-blast-radius
  - jev-cascade-overview
  - confidence-three-metrics
  - judgment-skill-hard-rules-tool-code
  - llm-patch-validation-format-not-semantics
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: LLM agent 說錯一句話，下一輪還能更正；做錯一件事就難了。JevAct 在 agent「提出動作」和「執行動作」之間加了一道閘門，只攔兩類難以挽回的動作：寫入型工具呼叫（write call，會改變資料庫的呼叫），以及放棄或轉接真人（hand-off）；上線時 Kev 只有在很有把握時才擋下，並附上回饋，讓 agent 在有限次數內修正
  source_quotes:
  - "LLM agent 說錯一句話，下一輪還能更正；做錯一件事就難了"
  - "在 agent「提出動作」和「執行動作」之間加了一道閘門，只攔兩類難以挽回的動作：寫入型工具呼叫（write call），也就是會改變資料庫的呼叫；以及放棄或轉接真人（hand-off）。"
  - "上線時，Kev 只有在很有把握時才擋下，並附上回饋，讓 agent 在有限次數內修正。"
  anchor_type: 設計參數
  qualifiers:
  - text: 檢查放棄的 hand-off check 只在 Telecom（電信客服）啟用，原因是在 Airline（航空客服）誤擋太多
    source_quote: "hand-off check 只在 Telecom 啟用，原因就是開頭提到的 Airline 誤擋。"
  - text: 「很有把握才擋」指 write gate 的 0.05 門檻；hand-off check 的兩個門檻都是 0.5
    source_quote: "這裡兩個門檻都是 0.5，和 write gate 的 0.05 不同"
  importance: 1
  status: normal
- id: c2
  role: context
  text: 'JevAct 是 IBM SIL 的 Iftach Shoham、Yuval David 等人提出的方法，論文是〈Think Before You Act: Decision Gate for LLM Agents〉（IBM SIL，2026 年 10 月）；擔任裁判的不是另一個大型 LLM，而是 Kev：一個便宜的外部開源決策模型，讀一段 prompt、只跑一次 forward pass（只做讀入輸入的 prefill，不生成任何文字），就直接給出每個固定選項的機率'
  source_quotes:
  - "IBM SIL 的 Iftach Shoham、Yuval David 等人提出的 JevAct"
  - "Think Before You Act: Decision Gate for LLM Agents"
  - "（IBM SIL，2026 年 10 月）"
  - "擔任裁判的不是另一個大型 LLM，而是 Kev：一個便宜的外部開源決策模型。它讀一段 prompt，只跑一次 forward pass（模型把輸入從頭算過一遍；這裡只做讀入輸入的 prefill，不生成任何文字），就直接給出每個固定選項的機率。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 日期
  importance: 2
  status: normal
- id: c3
  role: context
  text: 四個名字裡只有 JevAct 是這篇論文的貢獻：Jev 是 TypeSafe AI 的原版決策模型，只被引用；Kev 是 Jared Palmer 做的開源「Jev 類」決策模型（不是論文作者），實際擔任裁判；JevLoop 是 ZJUNLP 讓決策模型「選動作」的 agent runtime，只用來對比定位。JevLoop 把「選哪個動作」交給決策模型，JevAct 的動作仍由 agent 的 LLM 提出，Kev 只負責審核，也因此 agent 不會審自己的提案
  source_quotes:
  - "四個名字裡，只有 JevAct 是這篇論文的貢獻；Kev 是實際拿來當裁判的外部開源模型，Jev 與 JevLoop 只被引用。"
  - "| Jev | 原版決策模型（System One Model） | TypeSafe AI | 只被引用 |"
  - "| Kev | 開源的「Jev 類」決策模型 | Jared Palmer（GitHub：jaredpalmer/kev），不是論文作者 | 實際擔任裁判 |"
  - "| JevLoop | 讓決策模型「選動作」的 agent runtime | ZJUNLP | 只用來對比定位，沒有做實驗比較 |"
  - "JevLoop 把「選哪個動作」交給決策模型；JevAct 的動作仍由 agent 的 LLM 提出，Kev 只負責審核，也因此 agent 不會審自己的提案。"
  anchor_type: 背景說明
  importance: 4
  status: normal
- id: c4
  role: context
  text: 多數 agent 迴圈在 LLM 提出動作之後就立刻執行，「生成動作」和「確認該不該做」之間沒有任何檢查；既有兩類做法各缺一角：Self-Refine、Reflexion 這類反思方法改善的是「之後的提案」，不會在某個動作執行前逐條對照政策；生成式 LLM-as-judge 輸出自由文字，閘門還得再解讀一次，每一步都叫前沿模型也太貴
  source_quotes:
  - "多數 agent 迴圈在 LLM 提出動作之後就立刻執行，「生成動作」和「確認該不該做」之間沒有任何檢查。"
  - "既有的兩類做法各缺一角。"
  - "| Self-Refine、Reflexion 這類反思方法 | 改善的是「之後的提案」，不會在某個動作執行前逐條對照政策 |"
  - "| 生成式 LLM-as-judge | 輸出自由文字，閘門還得再解讀一次；每一步都叫前沿模型也太貴 |"
  anchor_type: 原作者解讀
  importance: 3
  status: normal
- id: c5
  role: mechanism
  text: JevAct 分成兩層：離線時，LLM 把領域政策編譯成檢查材料；上線時，在 agent 每一步攔下危險動作，程式碼負責算硬事實，Kev 一次 forward pass 給出所有題目的機率。agent 本身的 LLM、基礎 prompt 與工具都不改動
  source_quotes:
  - "JevAct 分成兩層。離線時，LLM 把領域政策編譯成檢查材料，再用開發階段的紀錄做兩道品管。上線時，在 agent 每一步攔下危險動作：程式碼負責算硬事實，Kev 一次 forward pass 給出所有題目的機率"
  - "agent 本身的 LLM、基礎 prompt 與工具都不改動。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c6
  role: mechanism
  text: 每一步都走四個階段：提出、觸發、檢查、放行或重提；只有 write call 與 hand-off 會被檢查，其餘訊息照 ReAct（提出動作就直接執行、中間沒有閘門的標準 agent 迴圈）原樣直接執行。被擋的提案不執行，也不寫進歷史；回饋只在那一次呼叫有效，不寫入對話歷史，所以過去的批評不會在 context 裡越積越多
  source_quotes:
  - "每一步都走四個階段：提出、觸發、檢查、放行或重提。只有 write call 與 hand-off 會被檢查，其餘訊息照 ReAct 原樣直接執行。ReAct 是提出動作就直接執行、中間沒有閘門的標準 agent 迴圈"
  - "被擋的提案不執行，也不寫進歷史。"
  - "回饋只在那一次呼叫有效，不寫入"
  - "所以過去的批評不會在 context 裡越積越多。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c7
  role: mechanism
  text: 每種檢查有修正預算：檢查寫入的 write gate 是 2 次，檢查放棄的 hand-off check 是 1 次；預算用完之後，下一個提案直接執行，不再檢查
  source_quotes:
  - "每種檢查有修正預算 \\( R \\)：write gate 為 \\( R = 2 \\)，hand-off check 為 \\( R = 1 \\)。預算用完之後，下一個提案直接執行，不再檢查。"
  - "檢查寫入的關卡叫 write gate，檢查放棄的關卡叫 hand-off check。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 4
  status: normal
- id: c8
  role: mechanism
  text: 訊息依類型分流，最多進 write gate 與 hand-off check 其中一個；一般回覆與查詢類呼叫兩個都不進。寫入與轉接看工具名稱就能判斷；用文字放棄沒有工具名稱可看，所以先過便宜的關鍵字篩選，再請 Kev 確認
  source_quotes:
  - "訊息依類型分流，最多進其中一個；一般回覆與查詢類呼叫，兩個都不進。寫入與轉接看工具名稱就能判斷；用文字放棄沒有工具名稱可看，所以先過便宜的關鍵字篩選，再請 Kev 確認"
  anchor_type: 設計參數
  qualifiers:
  - text: 論文沒說明寫入工具清單怎麼認定、放棄關鍵字的實際清單，以及一則訊息同時含寫入與放棄時的處理順序
    source_quote: "論文未說明的有三件事：寫入工具清單怎麼認定（我的推論：沿用 benchmark 對工具的分類）、放棄關鍵字的實際清單，以及一則訊息同時含寫入與放棄時的處理順序。"
  importance: 5
  status: normal
- id: c9
  role: mechanism
  text: Kev 對每一題給出答「是」的機率；write gate 只有在 Kev 非常確定答案是「否」時，也就是 P(是) ≤ 0.05、有 95% 以上的把握認為「不是」，才把這題算作「否」並擋下，其他情況一律當作「是」
  source_quotes:
  - "Kev 對每一題給出答「是」的機率。但 write gate 只有在 Kev 非常確定答案是「否」時，才把這題算作「否」並擋下；其他情況一律當作「是」。換句話說，Kev 要有 95% 以上的把握認為「不是」，才算「否」："
  - "| Kev 給的 \\( P(\\text{是}) \\) | Kev 的意思 | 0.05 門檻下的判決 | 若改用 0.5 門檻 |"
  anchor_type: 設計參數
  comparison_target: blog 拿來對照的 0.5 門檻
  qualifiers:
  - text: 0.05 這個門檻只在 Kev-27B 上設定過
    source_quote: "門檻，只在 Kev-27B 上設定過。"
  - text: 0.05 這個判違規門檻只在 Airline 設定一次，直接沿用到 Telecom
    source_quote: "判違規的門檻 \\( P(\\text{是}) \\le 0.05 \\) 與 10% 的淘汰線，都只在 Airline 設定一次，直接沿用到 Telecom。"
  - text: 門檻要有意義，前提是 Kev 的機率校準良好
    source_quote: "門檻要有意義，前提是 Kev 的機率校準良好"
  importance: 2
  status: normal
- id: c10
  role: anchor
  text: blog 自編的三個例子（題目都是「使用者有沒有明確確認要取消？」）：Kev 給 P(是) 0.97，很確定使用者確認過，放行；0.03，很確定沒確認，擋下；0.20，有 80% 機率認為沒確認，在 0.05 門檻下放行，若改用 0.5 門檻則擋下
  source_quotes:
  - "下面三個自編例子，題目都是「使用者有沒有明確確認要取消？」："
  - "| 0.97 | 很確定使用者確認過 | 放行 | 放行 |"
  - "| 0.03 | 很確定使用者沒確認 | 擋下 | 擋下 |"
  - "| 0.20 | 有 80% 機率認為沒確認 | 放行 | 擋下 |"
  - "| Kev 給的 \\( P(\\text{是}) \\) | Kev 的意思 | 0.05 門檻下的判決 | 若改用 0.5 門檻 |"
  anchor_type: 部落格舉例
  comparison_target: 同一個例子在 0.05 門檻與 0.5 門檻下的判決
  importance: 3
  status: normal
- id: c11
  role: evaluation
  text: 論文只說機率讓檢查「只在有把握時出手」，沒有解釋門檻為什麼設得這麼偏；blog 推論是擋錯正確動作的代價被視為比較高，代價是 0.20 這類「大概沒確認」的情況會被放過
  source_quotes:
  - "論文只說機率讓檢查「只在有把握時出手」，沒有解釋門檻為什麼設得這麼偏。（我的推論）擋錯正確動作的代價被視為比較高；代價是 0.20 這類「大概沒確認」的情況會被放過。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 示範題
  qualifiers:
  - text: 門檻要有意義，前提是 Kev 的機率校準良好
    source_quote: "門檻要有意義，前提是 Kev 的機率校準良好"
  importance: 3
  status: normal
- id: c12
  role: mechanism
  text: write gate 擋下時的回饋，先列出已確定的違規與沒過的題目，再給 agent 三條路：修正呼叫、向使用者補問，或說明為什麼無法辦理；agent 如果認為原本的呼叫是對的，可以原封不動再送一次。第二次被擋時，回饋改成要求 agent「回覆使用者，不要再呼叫這個工具」
  source_quotes:
  - "回饋的格式是：先列出已確定的違規與沒過的題目，再給 agent 三條路：修正呼叫、向使用者補問，或說明為什麼無法辦理。agent 如果認為原本的呼叫是對的，可以原封不動再送一次。第二次被擋時，回饋改成要求 agent「回覆使用者，不要再呼叫這個工具」。"
  anchor_type: 設計參數
  importance: 4
  status: normal
- id: c13
  role: anchor
  text: blog 自編的走一遍：使用者要取消 2 小時前剛訂的訂位，agent 沒先確認就呼叫取消；Kev 對「使用者有沒有明確確認？」給 P(是) = 0.02，算「否」，審核規則要求「已確認」不成立，擋下並附回饋；agent 改問使用者是否確定，使用者回「確定」後再次呼叫，Kev 給 0.96，執行取消。被擋不等於失敗
  source_quotes:
  - "逐步演算一次（自編：使用者一開口就要取消，agent 沒先確認就呼叫）："
  - "使用者：幫我取消訂位 ABC（2 小時前剛訂）。"
  - "Kev：「使用者有沒有明確確認？」\\( P(\\text{是}) = 0.02 \\)，算「否」；其他題都高於 0.05。"
  - "判決：審核表要求「已確認」，不成立，擋下並附上回饋。"
  - "agent 重提：不呼叫工具，改問「要取消 ABC、全額退款，確定嗎？」。這是一般訊息，直接送出。"
  - "使用者回「確定」；agent 再次提出 `cancel_reservation(ABC)`，Kev 給 \\( P(\\text{是}) = 0.96 \\)，三步全過，執行取消。"
  - "小結：被擋不等於失敗。agent 改去問使用者，確認之後，同一個呼叫就通過了。"
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 3
  status: normal
- id: c14
  role: qualifier
  text: 檢查放棄前必做步驟的清單只在 Telecom 啟用：在 Airline 的離線測試中，原本成功的場次有 26% 的轉接被它擋下，誤擋太多，所以關閉
  source_quotes:
  - "它只在 Telecom 啟用：在 Airline 的離線測試中，原本成功的場次有 26% 的轉接被它擋下，誤擋太多，所以關閉。"
  anchor_type: 實驗結果
  comparison_target: Airline 離線測試中原本成功的場次裡的轉接
  importance: 4
  status: normal
```
