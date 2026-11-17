---
id: handoff-checklist-not-discussed-not-ruled-out
title: 檢查「該做的步驟做了沒」時，「或前提不成立」這種逃生口只能寫成「對話已確認前提不成立」——沒談過，不算已排除；JevAct 用這條規則寫轉接真人前的必做清單，再用成功場次刪掉會亂擋的步驟
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: jevact
  article_title: "JevAct：讓 AI Agent 三思而後行的執行前閘門"
  url: https://datasciocean.com/paper-intro/jevact/
  sections:
  - LLM agent 最怕做錯事：JevAct 在動手前加一道閘門
  - 說錯能更正，做錯難挽回：為什麼要在執行前擋
  - 一張地圖：兩層、兩個 gate
  - 放棄前清單：轉接真人之前，該做的步驟做了沒
  - 清單怎麼產生
  - 最關鍵的規則：沒談過，不算已排除
  - 用成功場次刪掉會亂擋的步驟
  - hand-off check 怎麼判
  - 兩道品管：不用正確答案也能修程式、刪爛題
  - 主結果：Telecom 大進步，但要打折
  first_appearance: true
parent: null
related:
  - jevact-pre-execution-gate
  - policy-split-derive-questions-rules
  - jevact-results-gain-source
  - policy-checks-blind-to-user-request
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 放棄前清單的規則「沒談過，不算已排除」堵住了最容易漏的洞：檢查有前提的步驟時，「或前提不成立」這種逃生口，只能寫成「對話已確認前提不成立」，因為前提可能從頭到尾都沒被確認過
  source_quotes:
  - "「沒談過，不算已排除」堵住了最容易漏的洞"
  - "規則的寫法是：「或前提不成立」這種逃生口，只能寫成「對話已確認前提不成立」。"
  - "這是有前提的步驟。最直覺的檢查題是「做了，或前提不成立」，但前提可能從頭到尾都沒被確認過。"
  anchor_type: 設計參數
  importance: 1
  status: normal
- id: c2
  role: context
  text: JevAct 是 IBM SIL 提出的方法，在 LLM agent「提出動作」和「執行動作」之間加一道閘門，只攔寫入型工具呼叫（write call，會改變資料庫的呼叫）與放棄或轉接真人（hand-off）兩類動作；擔任裁判的是 Kev，一個便宜的外部開源決策模型，只跑一次 forward pass 就直接給出每個固定選項的機率；檢查寫入的關卡叫 write gate，檢查放棄的關卡叫 hand-off check
  source_quotes:
  - "IBM SIL 的 Iftach Shoham、Yuval David 等人提出的 JevAct，在 agent「提出動作」和「執行動作」之間加了一道閘門，只攔兩類難以挽回的動作：寫入型工具呼叫（write call），也就是會改變資料庫的呼叫；以及放棄或轉接真人（hand-off）。"
  - "擔任裁判的不是另一個大型 LLM，而是 Kev：一個便宜的外部開源決策模型。它讀一段 prompt，只跑一次 forward pass（模型把輸入從頭算過一遍；這裡只做讀入輸入的 prefill，不生成任何文字），就直接給出每個固定選項的機率。"
  - "檢查寫入的關卡叫 write gate，檢查放棄的關卡叫 hand-off check。"
  anchor_type: 設計參數
  qualifiers:
  - text: hand-off check 只在 Telecom 啟用，原因是 Airline 誤擋
    source_quote: "hand-off check 只在 Telecom 啟用，原因就是開頭提到的 Airline 誤擋。"
  importance: 2
  status: normal
- id: c3
  role: context
  text: hand-off（放棄或轉接）是轉給真人，或告訴使用者「沒辦法了」，等於結束這次嘗試；Telecom 任務最常見的失敗，就是 agent 太早放棄。放棄前清單是放棄之前必做的步驟，離線產生，上線時只供 hand-off check 使用
  source_quotes:
  - "hand-off（放棄或轉接）：轉給真人，或告訴使用者「沒辦法了」，等於結束這次嘗試。Telecom 任務最常見的失敗，就是 agent 太早放棄。"
  - "放棄前清單，也就是放棄之前必做的步驟。"
  - "放棄前清單是離線 Step 6 的產物，上線時只供 hand-off check 使用。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c4
  role: qualifier
  text: 放棄前清單只在 Telecom 啟用：在 Airline 的離線測試中，原本成功的場次有 26% 的轉接被它擋下，誤擋太多，所以關閉
  source_quotes:
  - "它只在 Telecom 啟用：在 Airline 的離線測試中，原本成功的場次有 26% 的轉接被它擋下，誤擋太多，所以關閉。"
  anchor_type: 實驗結果
  comparison_target: Airline 離線測試中原本成功的場次裡的轉接
  importance: 3
  status: normal
- id: c5
  role: mechanism
  text: 產生清單的兩步只呼叫 Claude Opus 4.6，不需要標註：先抽出「排查問題 B 之前要先修好問題 A」這類前置關係（只有 Telecom），讓 A 的步驟也被標記為 B 的必做步驟；再讀政策、前置關係與 agent 的工具名稱生成清單。清單上的每一步都附一題 settled，交給 Kev 回答「這一步已經處理了嗎？」，試過、確認沒問題，或確定不適用，任一成立就算已處理
  source_quotes:
  - "產生清單的 6a、6b 兩步只呼叫 Claude Opus 4.6，不需要標註。清單上的每一步都附一題 `settled`，交給 Kev 回答「這一步已經處理了嗎？」：試過、確認沒問題，或確定不適用，任一成立就算已處理。"
  - "6a 抽出前置關係（只有 Telecom）：找出「排查問題 B 之前要先修好問題 A」這類規定，讓 A 的步驟也被標記為 B 的必做步驟。"
  - "6b 生成清單：讀政策、前置關係與 agent 的工具名稱，輸出固定格式的 JSON。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 3
  status: normal
- id: c6
  role: mechanism
  text: 生成清單的 prompt 有四條主要規定：照政策的順序列出所有步驟；身分驗證與單純的資訊請求不列；後續步驟依賴的事實，要把「問使用者」列成獨立的一步；settled 題要遵守「沒談過，不算已排除」
  source_quotes:
  - "6b 的 prompt 有四條主要規定："
  - "照政策的順序列出所有步驟。"
  - "身分驗證與單純的資訊請求不列。"
  - "後續步驟依賴的事實，要把「問使用者」列成獨立的一步。"
  - "`settled` 題要遵守「沒談過，不算已排除」。"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c7
  role: anchor
  text: Telecom 的政策寫「若使用者在國外，開啟漫遊」，這是有前提的步驟；blog 自編一段對話（使用者其實在國外，對話裡從沒提到，重開機、檢查數據後還是不行，agent 要轉接真人）比較兩種寫法：沒有這條規則時，已處理題是「漫遊已開，或使用者沒在國外」，沒人提到國外、看起來像沒在國外，於是打勾、放行轉接（錯）；有這條規則時，清單多一步「問是否在國外」，判讀為從沒問過，未完成、擋下，回饋先問是否在國外
  source_quotes:
  - "政策寫「若使用者在國外，開啟漫遊」，這是有前提的步驟。"
  - "下表把同一段對話（自編：使用者其實在國外，對話裡從沒提到）套上兩種寫法："
  - "| 對話 | 無法上網 → 重開機、檢查數據 → 還是不行 → agent：幫你轉接真人 | （同一段對話） |"
  - "| 已處理？題 | 漫遊已開，或使用者沒在國外 | 多一步「問是否在國外」；已處理？對話裡問過了嗎 |"
  - "| Kev 的判讀 | 沒人提到國外，看起來像沒在國外 | 從沒問過 |"
  - "| 結果 | 打勾 → 放行轉接（錯） | 未完成 → 擋下，回饋：先問是否在國外 |"
  anchor_type: 部落格舉例
  qualifiers:
  - text: 論文原文只說沒有這條規則的寫法「看起來已處理，但其實沒人問過」；表中 Kev 的判讀是 blog 依這句話補上的示意
    source_quote: "論文原文只說寫法 A「看起來已處理，但其實沒人問過」；表中 Kev 的判讀是依這句話補上的示意。"
  importance: 2
  status: normal
- id: c8
  role: anchor
  text: blog 的比喻（一般知識，不是論文內容）：開盤尼西林之前的確認單，如果寫「病人不過敏，或病人沒提過自己過敏？」，醫生只要沒問，這格就自動打勾；正確的寫法是「醫生問過病人有沒有過敏嗎？」
  source_quotes:
  - "先看一個比喻（一般知識）：開盤尼西林之前的確認單，如果寫「病人不過敏，或病人沒提過自己過敏？」，醫生只要沒問，這格就自動打勾。正確的寫法是「醫生問過病人有沒有過敏嗎？」。"
  - "（一般知識）是比喻或背景常識，不是論文內容"
  anchor_type: 部落格舉例
  importance: 4
  status: normal
- id: c9
  role: mechanism
  text: 清單寫好之後還要過濾：最後仍成功解決的對話，裡面的轉接視為正確；正確的轉接本來就該通過清單，所以清單在這種轉接上判某步「未完成」，就算一次亂擋；亂擋比例超過 5% 的步驟，整步刪除
  source_quotes:
  - "清單寫好之後還要過濾。最後仍成功解決的對話，裡面的轉接視為正確；正確的轉接本來就該通過清單，所以清單在這種轉接上判某步「未完成」，就算一次亂擋。亂擋比例超過 5% 的步驟，整步刪除。"
  anchor_type: 設計參數
  comparison_target: 成功場次裡的轉接次數（亂擋比例的分母）
  qualifiers:
  - text: 放棄前清單另外在一次結果檢討後修改過，論文沒說檢討了哪些任務
    source_quote: "附錄 A.1 末段另外提到，放棄前清單在一次結果檢討後修改過，但沒說檢討了哪些任務。"
  importance: 3
  status: normal
- id: c10
  role: evidence
  text: 實際數字是用 GPT-4.1 與 Opus 4.6 在 74 個訓練任務上跑 6 次開發實驗，每場只取第一次轉接，共 217 次，其中 36 次發生在成功場次，這 36 次就是分母；36 × 5% = 1.8，所以亂擋 2 次以上就刪；最後共刪 7 步：飛航模式、APN 設定、SIM 狀態、門號停用、欠費、合約到期日、繳費後恢復門號
  source_quotes:
  - "論文的實際數字：用 GPT-4.1 與 Opus 4.6 在 74 個訓練任務上跑 6 次開發實驗，每場只取第一次轉接，共 217 次；其中 36 次發生在成功場次，這 36 次就是計算比例的分母。"
  - "所以亂擋 2 次以上就刪。最後共刪 7 步：飛航模式、APN 設定、SIM 狀態、門號停用、欠費、合約到期日、繳費後恢復門號。"
  - "\\( 36 \\times 5\\% = 1.8 \\)"
  anchor_type: 實驗結果
  comparison_target: 成功場次裡的 36 次轉接（5% 門檻換算成次數）
  importance: 3
  status: normal
- id: c11
  role: qualifier
  text: 這道過濾和 JevAct 淘汰 Kev 爛題目的品管有一個關鍵差異：它需要結果標註，因為要知道哪一場成功；而產生清單本身不需要標註
  source_quotes:
  - "這道過濾和品管二有一個關鍵差異：它需要結果標註，因為要知道哪一場成功。"
  - "品管二：淘汰爛題目（Step 5）。"
  - "產生清單的 6a、6b 兩步只呼叫 Claude Opus 4.6，不需要標註。"
  anchor_type: 設計參數
  importance: 4
  status: normal
- id: c12
  role: mechanism
  text: hand-off check 的觸發條件是轉接工具的呼叫，或經過關鍵字篩選與 Kev 確認的文字放棄；Kev 在一次請求中回答三件事：使用者遇到的是哪種問題（含「其他」）、使用者是否說了問題已解決、清單上每一步是否已處理
  source_quotes:
  - "hand-off check 的觸發條件，是轉接工具的呼叫，或經過關鍵字篩選與 Kev 確認的文字放棄。Kev 在一次請求中回答三件事："
  - "使用者遇到的是哪種問題（含「其他」）。"
  - "使用者是否說了問題已解決。"
  - "清單上每一步是否已處理。"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c13
  role: mechanism
  text: 問題沒解決、而且有任一相關步驟未完成，就擋下，回饋列出未完成的步驟；一步算「未完成」要同時滿足兩件事：這一步跟使用者的問題有關（所有需要這一步的問題機率加總 ≥ 0.5），而且大概還沒做（這一步已處理的機率 ≤ 0.5）
  source_quotes:
  - "如果問題沒解決，而且有任一相關步驟未完成，就擋下，回饋列出未完成的步驟。一步算「未完成」，要同時滿足兩件事：這一步跟使用者的問題有關，而且大概還沒做。"
  - "的問題機率加總，代表這一步和使用者問題的相關程度。"
  - "右式：這一步已處理的機率。"
  - "這裡兩個門檻都是 0.5，和 write gate 的 0.05 不同"
  - 'P(p) \ \ge\ 0.5 \quad \text{且} \quad P(\text{步驟 } k \text{ 已處理}) \ \le\ 0.5'
  anchor_type: 設計參數
  comparison_target: write gate 的 0.05 門檻
  qualifiers:
  - text: 判斷「已解決」用的門檻，論文未說明
    source_quote: "判斷「已解決」用的門檻，論文未說明。"
  - text: hand-off check 的修正預算是 1 次，修正一次之後，下一次放棄就直接執行
    source_quote: "修正一次之後，下一次放棄就直接執行。"
  importance: 2
  status: normal
- id: c14
  role: anchor
  text: blog 自編例子：Kev 給出的問題機率是「無法上網」0.7、「無法傳簡訊」0.2、「其他」0.1，P(已解決) = 0.05，判定未解決；「重開機」相關度 0.9、已處理 0.95，算已處理；「詢問是否在國外」相關度 0.7、已處理 0.10，算未完成；「檢查簡訊設定」相關度 0.2 低於 0.5，不相關跳過；所以擋下，回饋「還沒詢問使用者是否在國外」
  source_quotes:
  - "自編例子：Kev 給出的問題機率是「無法上網」0.7、「無法傳簡訊」0.2、「其他」0.1；"
  - "= 0.05 \\)，判定未解決。"
  - "| 重開機 | 上網、簡訊 | 0.7 + 0.2 = 0.9 | 0.95 | 已處理 |"
  - "| 詢問是否在國外 | 上網 | 0.7 | 0.10 | 未完成 |"
  - "| 檢查簡訊設定 | 簡訊 | 0.2（低於 0.5） | 0.10 | 不相關，跳過 |"
  - "判決：問題未解決，且有一步未完成，所以擋下，回饋「還沒詢問使用者是否在國外」。"
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 4
  status: normal
```
