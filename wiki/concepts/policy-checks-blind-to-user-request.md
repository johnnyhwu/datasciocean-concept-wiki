---
id: policy-checks-blind-to-user-request
title: 從政策出發的檢查，天生看不到使用者當下的具體要求：JevAct 的題目編碼的是政策，Airline 的 101 個錯誤寫入呼叫中有 42 個一題都沒違反，即使 Kev 每題都答對，最多也只抓得到約 58%
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: jevact
  article_title: "JevAct：讓 AI Agent 三思而後行的執行前閘門"
  url: https://datasciocean.com/paper-intro/jevact/
  sections:
  - LLM agent 最怕做錯事：JevAct 在動手前加一道閘門
  - 一張地圖：兩層、兩個 gate
  - 編譯器：把一句政策拆給計算機、閱讀員與審核表
  - 每個寫入工具配到的三樣東西
  - 題目的四個面向
  - hand-off check 怎麼判
  - 盲區：題目只看政策，看不到使用者要什麼
  - 審核表：文字說明與範例對不上
  - 結論：回顧全文與值得帶走的重點
  first_appearance: true
parent: null
related:
  - jevact-pre-execution-gate
  - policy-split-derive-questions-rules
  - handoff-checklist-not-discussed-not-ruled-out
  - jevact-results-gain-source
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 從政策編出的題目，最多只能抓到約 58% 的錯誤呼叫，因為 101 個錯誤中有 42 個一題都沒違反；問題不在 Kev 答錯，而是根本沒有題目在問那件事；論文的解釋是，題目編碼的是政策，不是使用者的要求
  source_quotes:
  - "從政策編出的題目，最多只能抓到約 58% 的錯誤呼叫，因為 101 個錯誤中有 42 個一題都沒違反。問題不在 Kev 答錯，而是根本沒有題目在問那件事。"
  - "論文的解釋是：題目編碼的是政策，不是使用者的要求。"
  anchor_type: 部落格考證
  comparison_target: Airline 開發階段人工標註的 101 個錯誤寫入呼叫
  qualifiers:
  - text: 資料來自 Airline 開發階段 260 個人工標註的寫入呼叫；42 這個數字出自論文的結論節
    source_quote: "資料來自 Airline 開發階段 260 個人工標註的寫入呼叫：159 個正確、101 個錯誤（附錄 A.4，也是後面表 5 的資料；42 這個數字出自論文的結論節）。"
  - text: 58% 是天花板，前提是 Kev 每題都答對
    source_quote: "天花板是：即使 Kev 每題都答對，這套題目最多也只抓得到"
  - text: 論文沒說明計算機能不能抓到這 42 個；blog 推論計算機同樣只檢查政策相關的事實，應該也抓不到
    source_quote: "論文未說明計算機能不能抓到這 42 個。（我的推論）計算機同樣只檢查政策相關的事實，應該也抓不到。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: JevAct 是 IBM SIL 提出的方法，在 LLM agent「提出動作」和「執行動作」之間加一道閘門，只攔寫入型工具呼叫（write call，會改變資料庫的呼叫）與放棄或轉接真人（hand-off）兩類動作；擔任裁判的是 Kev，一個便宜的外部開源決策模型，只跑一次 forward pass 就直接給出每個固定選項的機率。檢查寫入的 write gate 用三種材料：計算機（編譯器寫出的 derive 函式，從工具紀錄計算事實）、閱讀員（給 Kev 回答的單一事實 yes/no 題）、審核表（把 Kev 的答案組合起來的布林規則）；檢查放棄的關卡叫 hand-off check
  source_quotes:
  - "IBM SIL 的 Iftach Shoham、Yuval David 等人提出的 JevAct，在 agent「提出動作」和「執行動作」之間加了一道閘門，只攔兩類難以挽回的動作：寫入型工具呼叫（write call），也就是會改變資料庫的呼叫；以及放棄或轉接真人（hand-off）。"
  - "擔任裁判的不是另一個大型 LLM，而是 Kev：一個便宜的外部開源決策模型。它讀一段 prompt，只跑一次 forward pass（模型把輸入從頭算過一遍；這裡只做讀入輸入的 prefill，不生成任何文字），就直接給出每個固定選項的機率。"
  - "檢查寫入的關卡叫 write gate，檢查放棄的關卡叫 hand-off check。write gate 用三種材料：計算機（編譯器寫出的 derive 函式，從工具紀錄計算事實）、閱讀員（給 Kev 回答的單一事實 yes/no 題）、審核表（把 Kev 的答案組合起來的布林規則）。"
  anchor_type: 設計參數
  qualifiers:
  - text: hand-off check 只在 Telecom 啟用，原因是 Airline 誤擋
    source_quote: "hand-off check 只在 Telecom 啟用，原因就是開頭提到的 Airline 誤擋。"
  - text: 論文實際的 cancel_reservation 規則交給 Kev 的是一題總結題（至少符合一項條件），不是單一條件題
    source_quote: "但它附上的 `cancel_reservation` 實際規則裡沒有 or，而是交給 Kev 一題總結題來回答。"
  importance: 2
  status: normal
- id: c3
  role: context
  text: 題目是離線編出來的：編譯器（Claude Opus 4.6）每個領域只跑一次，讀政策與工具 schema，為每個寫入工具產出一份題目清單（每個工具 12–20 題），全部交給 Kev 回答
  source_quotes:
  - "編譯器是 Claude Opus 4.6，離線執行，每個領域只跑一次。它讀政策與工具 schema（工具的參數格式說明），為每個寫入工具產出三樣東西"
  - "題目清單：每個工具 12–20 題"
  - "全部交給 Kev 回答。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 3
  status: normal
- id: c4
  role: context
  text: 題目分四個面向：政策條件（動作符不符合政策）、參數來源（參數來自紀錄，還是 agent 自己編的）、使用者意圖（使用者真的要做這件事嗎，例如「使用者真的要求取消，而不只是詢問？」）、前置步驟（該確認的都確認了嗎）
  source_quotes:
  - "| 政策條件 | 動作符不符合政策 | 根據工具結果，這張訂位還沒有任何航段已經飛了嗎？ |"
  - "| 參數來源 | 參數來自紀錄，還是 agent 自己編的 | 這個訂位編號，工具結果確認屬於這位使用者嗎？ |"
  - "| 使用者意圖 | 使用者真的要做這件事嗎 | 使用者真的要求取消，而不只是詢問？ |"
  - "| 前置步驟 | 該確認的都確認了嗎 | agent 列出取消細節後，使用者是否明確說了「是」？ |"
  anchor_type: 設計參數
  importance: 4
  status: normal
- id: c5
  role: evidence
  text: 資料是 Airline 開發階段 260 個人工標註的寫入呼叫：159 個正確；錯誤的 101 個裡，違反至少一題的有 59 個，一題都沒違反（盲區）的有 42 個
  source_quotes:
  - "資料來自 Airline 開發階段 260 個人工標註的寫入呼叫：159 個正確、101 個錯誤"
  - "| 正確 | 159 |"
  - "| 錯誤，且違反至少一題 | 59 |"
  - "| 錯誤，但一題都沒違反（盲區） | 42 |"
  anchor_type: 實驗結果
  numeric_kind: non_comparative
  numeric_reason: 計數
  qualifiers:
  - text: 42 這個數字出自論文的結論節
    source_quote: "42 這個數字出自論文的結論節"
  importance: 2
  status: normal
- id: c6
  role: evidence
  text: 天花板是即使 Kev 每題都答對，這套題目最多也只抓得到 59/101 ≈ 58% 的錯誤呼叫
  source_quotes:
  - "天花板是：即使 Kev 每題都答對，這套題目最多也只抓得到 \\( 59/101 \\approx 58\\% \\) 的錯誤呼叫。"
  anchor_type: 數學推導
  comparison_target: 101 個錯誤寫入呼叫
  qualifiers:
  - text: 資料是 Airline 開發階段 260 個人工標註的寫入呼叫（101 個錯誤）
    source_quote: "資料來自 Airline 開發階段 260 個人工標註的寫入呼叫：159 個正確、101 個錯誤"
  importance: 2
  status: normal
- id: c7
  role: mechanism
  text: 題目在離線時從政策編出，每個任務共用一套；使用者當下的具體要求（最便宜、最早、靠窗）各不相同，離線時無從預知，也就沒有題目去檢查它
  source_quotes:
  - "題目在離線時從政策編出，每個任務共用一套；使用者當下的具體要求（最便宜、最早、靠窗）各不相同，離線時無從預知，也就沒有題目去檢查它。"
  anchor_type: 原作者解讀
  importance: 2
  status: normal
- id: c8
  role: anchor
  text: blog 舉的例子：使用者說「回程改成 5/20 最便宜的那班」，agent 挑了第二便宜的班次，使用者回「好」，agent 接著呼叫改票工具；會員等級允許改票、艙等不變、付款有效、訂位編號正確，政策相關的題目全數通過，呼叫卻是錯的，因為政策裡沒有「必須選最便宜」，所以不會有這一題
  source_quotes:
  - "使用者說「回程改成 5/20 最便宜的那班」，agent 挑了第二便宜的班次，使用者回「好」，接著 agent 呼叫 `update_reservation_flights`。會員等級允許改票、艙等不變、付款有效、訂位編號正確，政策相關的題目全數通過，呼叫卻是錯的；政策裡沒有「必須選最便宜」，所以不會有這一題。"
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 2
  status: normal
- id: c9
  role: evaluation
  text: 論文沒說明計算機能不能抓到這 42 個；blog 推論計算機同樣只檢查政策相關的事實，應該也抓不到
  source_quotes:
  - "論文未說明計算機能不能抓到這 42 個。（我的推論）計算機同樣只檢查政策相關的事實，應該也抓不到。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 3
  status: normal
- id: c10
  role: evaluation
  text: 從政策出發的檢查，天生看不到使用者當下說的「最便宜的那班」；自己做 agent 閘門時，可以先從便宜的程式檢查做起，再為使用者的具體要求另找檢查方法
  source_quotes:
  - "第三，從政策出發的檢查，天生看不到使用者當下說的「最便宜的那班」。自己做 agent 閘門時，可以先從便宜的程式檢查做起，再為使用者的具體要求另找檢查方法。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c11
  role: evaluation
  text: blog 把這點列為最值得記住的限制：題目編碼的是政策，不是使用者當下的要求，所以 101 個錯誤呼叫中有 42 個任何題目都抓不到
  source_quotes:
  - "最值得記住的限制：題目編碼的是政策，不是使用者當下的要求，所以 101 個錯誤呼叫中有 42 個任何題目都抓不到。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 計數
  qualifiers:
  - text: 資料是 Airline 開發階段 260 個人工標註的寫入呼叫（101 個錯誤）
    source_quote: "資料來自 Airline 開發階段 260 個人工標註的寫入呼叫：159 個正確、101 個錯誤"
  importance: 3
  status: normal
```
