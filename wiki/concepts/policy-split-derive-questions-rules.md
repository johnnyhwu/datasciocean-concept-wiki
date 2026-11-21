---
id: policy-split-derive-questions-rules
title: 把「能不能做」拆成程式算得出的事實、模型讀得出的意圖、規則組得起來的邏輯，各交給擅長的一方；JevAct 離線把政策拆給計算機、Kev 的是非題與審核表，再用不需要正確答案的兩道品管修程式、刪爛題
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
  - 計算機寧可漏報也不誤報
  - Kev 只在 95% 有把握時才說「不」
  - 兩道品管：不用正確答案也能修程式、刪爛題
  - 放棄前清單：轉接真人之前，該做的步驟做了沒
  - 用成功場次刪掉會亂擋的步驟
  - hand-off check 怎麼判
  - 結論：回顧全文與值得帶走的重點
  - 審核表：文字說明與範例對不上
  first_appearance: true
parent: null
related:
  - jevact-pre-execution-gate
  - handoff-checklist-not-discussed-not-ruled-out
  - jevact-results-gain-source
  - policy-checks-blind-to-user-request
  - judge-readable-vs-derive
  - judgment-skill-hard-rules-tool-code
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 把「能不能做」拆成程式算得出的事實、模型讀得出的意圖、規則組得起來的邏輯，各交給擅長的一方
  source_quotes:
  - "第一，把「能不能做」拆成程式算得出的事實、模型讀得出的意圖、規則組得起來的邏輯，各交給擅長的一方"
  anchor_type: 部落格判斷
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
  role: mechanism
  text: 編譯器是 Claude Opus 4.6，離線執行，每個領域只跑一次；它讀政策與工具 schema，為每個寫入工具產出三樣東西。題目清單，全部交給 Kev 回答；審核表，一條只合併 Kev 答案的 Python 布林運算式；derive 函式（計算機），讀這次呼叫的參數與先前所有工具結果，計算事實並自行列出違規，不經過審核表
  source_quotes:
  - "編譯器是 Claude Opus 4.6，離線執行，每個領域只跑一次。它讀政策與工具 schema（工具的參數格式說明），為每個寫入工具產出三樣東西"
  - "全部交給 Kev 回答。計算機不出題。"
  - "審核表：一條 Python 布林運算式，只合併 Kev 的答案。"
  - "derive 函式（計算機）：讀這次呼叫的參數與先前所有工具結果，計算事實並自行列出違規，不經過審核表。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 2
  status: normal
- id: c4
  role: mechanism
  text: 這樣拆的理由是：Kev 只會讀、不會算，日期與金額的比較交給程式；程式讀不懂「使用者是否真的同意」，交給 Kev；「任一條件成立即可」這種組合邏輯，則由規則來表達
  source_quotes:
  - "為什麼這樣拆：Kev 只會讀、不會算，日期與金額的比較交給程式；程式讀不懂「使用者是否真的同意」，交給 Kev；「任一條件成立即可」這種組合邏輯，則由規則來表達。"
  anchor_type: 原作者解讀
  qualifiers:
  - text: 論文附上的 cancel_reservation 實際規則裡沒有用 or 組合，而是交給 Kev 一題總結題來回答
    source_quote: "但它附上的 `cancel_reservation` 實際規則裡沒有 or，而是交給 Kev 一題總結題來回答。"
  importance: 2
  status: normal
- id: c5
  role: anchor
  text: blog 用一句取消政策示範怎麼拆：政策是 24 小時內、商務艙、有保險、航空公司取消任一成立才可取消，取消前使用者須明確同意；計算機算訂票過了幾小時（312 小時 > 24，違規）；Kev 的是非題問「使用者有明確確認嗎？」；審核表用 and／or 合併 Kev 的答案
  source_quotes:
  - "下表用一句取消政策示範怎麼拆。"
  - "| 政策（輸入） | 24 小時內／商務艙／有保險／航空公司取消，任一成立才可取消；取消前使用者須明確同意 | 交給編譯器（離線）拆解 |"
  - "| 計算機＝derive 函式 | 算數字 | 算訂票過了幾小時：312 小時 > 24 → 違規 |"
  - "| 閱讀員＝Kev 的 yes/no 題 | 讀對話 | 問：使用者有明確確認嗎？ |"
  - "| 審核表＝布林規則 | 組合答案 | 用 and／or 合併 Kev 的答案 |"
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 示範題
  qualifiers:
  - text: 論文附上的 cancel_reservation 實際規則裡沒有用 or 組合，而是交給 Kev 一題總結題來回答
    source_quote: "但它附上的 `cancel_reservation` 實際規則裡沒有 or，而是交給 Kev 一題總結題來回答。"
  importance: 3
  status: normal
- id: c6
  role: anchor
  text: 題目清單每個工具 12–20 題，Airline（航空客服）的 6 個寫入工具共 86 題，Telecom（電信客服）共 75 題
  source_quotes:
  - "題目清單：每個工具 12–20 題，Airline 的 6 個寫入工具共 86 題，Telecom 共 75 題"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 5
  status: normal
- id: c7
  role: mechanism
  text: 題目分四個面向：政策條件（動作符不符合政策）、參數來源（參數來自紀錄，還是 agent 自己編的）、使用者意圖（使用者真的要做這件事嗎）、前置步驟（該確認的都確認了嗎）；例如 cancel_reservation（取消訂位）的實際題目有「使用者真的要求取消，而不只是詢問？」。每題附一個 bad_if 欄位標記「答什麼代表違規」，題目中的參數寫成占位符，執行時先填入這次呼叫的實際值，再交給 Kev
  source_quotes:
  - "下表的例題是論文中 `cancel_reservation`（取消訂位）的實際題目（中譯）："
  - "| 政策條件 | 動作符不符合政策 | 根據工具結果，這張訂位還沒有任何航段已經飛了嗎？ |"
  - "| 參數來源 | 參數來自紀錄，還是 agent 自己編的 | 這個訂位編號，工具結果確認屬於這位使用者嗎？ |"
  - "| 使用者意圖 | 使用者真的要做這件事嗎 | 使用者真的要求取消，而不只是詢問？ |"
  - "| 前置步驟 | 該確認的都確認了嗎 | agent 列出取消細節後，使用者是否明確說了「是」？ |"
  - "每題附一個 `bad_if` 欄位，標記「答什麼代表違規」"
  - "題目中的參數寫成占位符，例如 `{reservation_id}`，執行時先填入這次呼叫的實際值，再交給 Kev。"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c8
  role: mechanism
  text: 判決規則是審核表不成立，或計算機回報違規，任一發生就擋下；兩者可能重疊，例如「是否在 24 小時內」既是 Kev 的一題，計算機也會檢查
  source_quotes:
  - "判決規則：審核表不成立，或計算機回報違規，任一發生就擋下。兩者可能重疊，例如「是否在 24 小時內」既是 Kev 的一題，計算機也會檢查"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 示範題
  qualifiers:
  - text: 實際的取消規則怎麼處理這一題，blog 在文末另有交代
    source_quote: "實際的取消規則怎麼處理這題，見文末〈審核表：文字說明與範例對不上〉"
  - text: 實際規則保留了總結題，拿掉了四個單一條件題
    source_quote: "實際規則保留了總結題，拿掉了四個單一條件題"
  importance: 3
  status: normal
- id: c9
  role: mechanism
  text: Kev 不必自己算時間，因為輸入給它之前，系統已在每個日期旁標註「距今多久」，並把清單類結果預先排序（例如價格由低到高）
  source_quotes:
  - "Kev 不必自己算時間，因為輸入給它之前，系統已在每個日期旁標註「距今多久」。"
  - "輸入前先做兩項預處理：在日期旁標註「距今多久」，並把清單類結果預先排序（例如價格由低到高）。"
  anchor_type: 設計參數
  qualifiers:
  - text: blog 推論，即使有「距今多久」的標註，「24 小時內」這類時間判斷仍不是 Kev 的強項
    source_quote: "（我的推論）「24 小時內」牽涉時間判斷，即使有「距今多久」的標註，這仍不是 Kev 的強項"
  importance: 4
  status: normal
- id: c10
  role: mechanism
  text: 計算機只在紀錄「確定」違規時回報；缺紀錄，或規則牽涉使用者說了什麼，一律不報，留給 Kev；程式拋出例外也當作沒有違規；程式只能用標準函式庫，並以白名單方式執行
  source_quotes:
  - "計算機只在紀錄「確定」違規時回報。缺紀錄，或規則牽涉使用者說了什麼，一律不報，留給 Kev；程式拋出例外也當作沒有違規。程式只能用標準函式庫，並以白名單方式執行。"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c11
  role: evaluation
  text: blog 推論計算機寧可漏報的理由是：計算機一回報就直接擋下動作，誤報的代價高
  source_quotes:
  - "（我的推論）計算機一回報就直接擋下動作，誤報的代價高，所以寧可漏報。"
  anchor_type: 部落格推論
  importance: 4
  status: normal
- id: c12
  role: evaluation
  text: 審核表的實際寫法和論文的文字說明並不一致：文字說「任一條件成立即可」這類多選一邏輯在審核表裡用 or 組合，但附上的 cancel_reservation 實際規則裡沒有 or，而是交給 Kev 一題總結題（「至少符合一項條件？」）來回答；兩種寫法結論相同，差別在「四選一」由誰判斷
  source_quotes:
  - "審核表的實際寫法和論文的文字說明並不一致"
  - "論文文字說，「任一條件成立即可」這類多選一邏輯，在審核表裡用 or 組合；但它附上的 `cancel_reservation` 實際規則裡沒有 or，而是交給 Kev 一題總結題來回答。"
  - "| Kev 回答 | 四題：24 小時內？是；商務艙？否；有保險？否；航空公司取消？否 | 一題：至少符合一項條件？是 |"
  - "兩邊結論相同，差別在「四選一」由誰判斷。"
  anchor_type: 部落格考證
  numeric_kind: non_comparative
  numeric_reason: 示範題
  qualifiers:
  - text: 論文沒說明範例為什麼這樣寫；可以確定的只有編規則的 prompt 允許拿掉「判斷時用不到」的題目
    source_quote: "論文未說明範例為什麼選 B；可以確定的只有：編規則的 prompt 允許拿掉「判斷時用不到」的題目。"
  - text: blog 推論，計算機也會獨立檢查取消資格，所以就算 Kev 判斷錯了，還有計算機兜底
    source_quote: "但計算機也會獨立檢查取消資格，所以就算 Kev 判斷錯了，還有計算機兜底。"
  importance: 4
  status: normal
- id: c13
  role: mechanism
  text: 編譯器產出的材料難免有錯，所以用開發階段的 agent 紀錄做兩道品管，兩道都不需要正確答案的標註。品管一是修正計算機：用訓練集紀錄裡的寫入呼叫跑一遍計算機，挑出它回報違規的案例（最多 16 筆，每個工具的每種違規各一筆），交給寫程式碼的同一個模型（Claude Opus 4.6）逐筆對照政策與紀錄，違規屬實就保留那段檢查，不屬實就找出 bug 修掉；只修一輪，也不提供正確答案
  source_quotes:
  - "編譯器一次產出的材料難免有錯，所以再用開發階段的 agent 紀錄做兩道品管。兩道都不需要正確答案的標註。"
  - "品管一：修正計算機（Step 4）。修程式碼的仍是寫程式碼的同一個模型（Claude Opus 4.6），只是另外發一次 prompt：自己寫、自己修。"
  - "用訓練集紀錄裡的寫入呼叫跑一遍計算機，挑出它回報違規的案例：最多 16 筆，每個工具的每種違規各一筆。"
  - "模型逐筆對照政策與紀錄，判斷違規是否屬實：屬實就保留那段檢查，不屬實就找出 bug 修掉，最後交回修好的完整程式碼。只修一輪，也不提供正確答案。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 2
  status: normal
- id: c14
  role: evidence
  text: '品管一修掉的 bug 例如把「Error: User not found」這段錯誤訊息當成使用者資料來讀、用了一筆已經被後續查詢取代的舊訂位；在 Airline 保留的測試任務上，計算機對「原本正確的寫入呼叫」的誤報率從 11.3% 降到 1.4%'
  source_quotes:
  - "論文舉了兩個被修掉的 bug：一是把「Error: User not found」這段錯誤訊息當成使用者資料來讀；二是用了一筆已經被後續查詢取代的舊訂位。"
  - "在 Airline 保留的測試任務上，計算機對「原本正確的寫入呼叫」的誤報率，從 11.3% 降到 1.4%。"
  anchor_type: 實驗結果
  comparison_target: 品管一修正之前的計算機（11.3%）
  importance: 2
  status: normal
- id: c15
  role: mechanism
  text: 品管二是淘汰爛題目：Kev-27B 對開發紀錄裡的每一次寫入呼叫回答所有題目，某一題「有把握地判定違規」的次數如果超過該工具呼叫次數的 10%，整題刪除；被刪的題目上線後不再回報，在審核表裡一律當作「是」
  source_quotes:
  - "品管二：淘汰爛題目（Step 5）。Kev-27B 對開發紀錄裡的每一次寫入呼叫回答所有題目。某一題「有把握地判定違規」的次數，如果超過該工具呼叫次數的 10%，整題刪除。被刪的題目上線後不再回報，在審核表裡一律當作「是」。"
  anchor_type: 設計參數
  comparison_target: 該工具在開發紀錄裡的呼叫次數
  qualifiers:
  - text: 10% 的淘汰線（以及判違規的門檻）只在 Airline 設定一次，直接沿用到 Telecom
    source_quote: "判違規的門檻 \\( P(\\text{是}) \\le 0.05 \\) 與 10% 的淘汰線，都只在 Airline 設定一次，直接沿用到 Telecom。"
  importance: 3
  status: normal
- id: c16
  role: mechanism
  text: 品管二背後的假設是：真正的違規很少見，所以太常判違規的題目，多半是 Kev 從對話裡讀不出這件事，或政策根本沒這樣要求
  source_quotes:
  - "背後的假設是：真正的違規很少見，所以太常判違規的題目，多半是 Kev 從對話裡讀不出這件事，或政策根本沒這樣要求。"
  anchor_type: 原作者解讀
  importance: 3
  status: normal
- id: c17
  role: evidence
  text: 品管二的結果是 Airline 的 86 題刪了 17 題；Telecom 的 75 題刪了 5 題（依據 175 筆開發寫入呼叫）
  source_quotes:
  - "結果：Airline 的 86 題刪了 17 題；Telecom 的 75 題刪了 5 題（依據 175 筆開發寫入呼叫）。"
  anchor_type: 實驗結果
  numeric_kind: non_comparative
  numeric_reason: 計數
  qualifiers:
  - text: 判違規的門檻 P(是) ≤ 0.05 與 10% 的淘汰線，都只在 Airline 設定一次，直接沿用到 Telecom
    source_quote: "判違規的門檻 \\( P(\\text{是}) \\le 0.05 \\) 與 10% 的淘汰線，都只在 Airline 設定一次，直接沿用到 Telecom。"
  importance: 4
  status: normal
- id: c18
  role: qualifier
  text: 這兩道品管都不需要正確答案的標註；相對地，JevAct 過濾放棄前清單的那道步驟需要結果標註，因為要知道哪一場成功
  source_quotes:
  - "兩道都不需要正確答案的標註。"
  - "這道過濾和品管二有一個關鍵差異：它需要結果標註，因為要知道哪一場成功。"
  - "放棄前清單是離線 Step 6 的產物"
  - "清單寫好之後還要過濾。最後仍成功解決的對話，裡面的轉接視為正確"
  anchor_type: 設計參數
  importance: 4
  status: normal
```
