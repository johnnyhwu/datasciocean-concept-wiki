---
id: llm-patch-validation-format-not-semantics
title: 任何「LLM 產生結構化輸出、程式自動套用」的設計，驗證都只擋得住格式錯誤，擋不住「格式對、內容錯」；SKILL.state 小模型 68% 的失敗正是這一種
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: skill-state
  article_title: "SKILL.state 論文：Agent 不留對話歷史只留狀態，200 步任務省 41 倍 token"
  url: https://datasciocean.com/paper-intro/skill-state/
  sections:
  - Agent 跑越久越貴：把對話歷史換成一份狀態
  - 三樣輸入、三樣輸出，狀態用合併來更新
  - 驗證擋得住格式錯誤，擋不住語意錯誤
  - 軟體版本庫：中途一度輸給 Stateful
  - 走一遍倉儲出貨的一步
  - 測試環境與計分方式
  - 實務上該選 ReAct 還是 SKILL.state
  - 它會在哪裡失敗：小模型的錯誤與三種失效情境
  - 結論：省成本可以期待，全面變準還不行
  first_appearance: true
parent: null
related:
  - skillstate-state-replaces-history
  - skillstate-results-cost-vs-accuracy
  - stateful-and-budget-matched-controls
  - discard-history-relevance-at-the-time
  - jevact-pre-execution-gate
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 驗證只擋得住格式：任何「LLM 產生結構化輸出、程式自動套用」的設計，都要記得驗證擋不住「格式對、內容錯」
  source_quotes:
  - "驗證只擋得住格式：論文自己的實驗（68% 的錯誤來自語意合法但錯誤的 patch）暴露了這一點，論文卻沒有明講它對架構的含義。任何「LLM 產生結構化輸出、程式自動套用」的設計，都要記得驗證擋不住「格式對、內容錯」。"
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
  text: 模型每一步輸出狀態的「差異」ΔΣ_t（一個 JSON 字典，描述這一步要對狀態做哪些修改，文中也稱 patch），狀態用「帶 null 刪除語意的字典合併」更新：ΔΣ_t 裡有的 key 直接覆蓋舊值；某個 key 的值被設成 null，代表把它從狀態裡整個刪掉；沒提到的 key 維持原樣
  source_quotes:
  - '\( \Delta\Sigma_t \) 是狀態的「差異」，一個 JSON 字典，描述這一步要對狀態做哪些修改。'
  - '論文定義了一個運算子 \( \oplus \)，叫「帶 null 刪除語意的字典合併」：\( \Delta\Sigma_t \) 裡有的 key，直接覆蓋舊狀態裡同名 key 的值；某個 key 的值被設成 `null`，代表把它從狀態裡整個刪掉；\( \Delta\Sigma_t \) 沒提到的 key 維持原樣。'
  - '`state_patch` 就是 \( \Delta\Sigma_t \)'
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c4
  role: mechanism
  text: Runtime 在套用狀態差異之前會先做格式驗證：是不是合法的 JSON、key 的結構符不符合預期。驗證失敗就回滾重試，狀態退回上一步，要求模型重新輸出，所以格式錯誤的輸出不會污染狀態
  source_quotes:
  - 'Runtime 在套用 \( \Delta\Sigma_t \) 之前會先做格式驗證：是不是合法的 JSON、key 的結構符不符合預期。驗證失敗就回滾重試，狀態退回上一步，要求模型重新輸出。所以格式錯誤的輸出不會污染狀態。'
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c5
  role: mechanism
  text: 驗證擋不住「格式合法、但語意錯誤」的輸出：模型輸出一個會誤刪重要資訊的 patch，格式完全沒問題，驗證抓不到，錯誤的更新就被「成功」套用了
  source_quotes:
  - "驗證擋得住「格式不合法」，擋不住「格式合法、但語意錯誤」的輸出。比方說模型輸出一個會誤刪重要資訊的 patch，格式完全沒問題，驗證抓不到，錯誤的更新就被「成功」套用了。"
  anchor_type: 部落格推論
  importance: 2
  status: normal
- id: c6
  role: mechanism
  text: 更關鍵的是，舊狀態已經不在 context 裡，一旦錯誤的 patch 被合法套用，就沒有回頭看歷史文字來自我修正的機會；相對於保留完整歷史的做法，這是整個架構在結構上更脆弱的地方
  source_quotes:
  - "更關鍵的是，舊狀態已經不在 context 裡，一旦錯誤的 patch 被合法套用，就沒有回頭看歷史文字來自我修正的機會。相對於保留完整歷史的做法，這是整個架構在結構上更脆弱的地方。"
  anchor_type: 部落格推論
  importance: 2
  status: normal
- id: c7
  role: anchor
  text: 論文把小模型的失敗案例分了類：Premature State Overwrite/Deletion（合併時不小心漏掉既有的 key，等於誤刪）占 68%，Schema Comprehension/Type 錯誤（巢狀的 list 和 dict 搞混）占 20%，JSON 語法／格式錯誤（漏逗號、括號沒對齊）占 12%
  source_quotes:
  - "論文把失敗案例分了類："
  - "Premature State Overwrite/Deletion | 合併時不小心漏掉既有的 key，等於誤刪 | 68%"
  - "Schema Comprehension/Type 錯誤 | 巢狀的 list 和 dict 搞混 | 20%"
  - "JSON 語法／格式錯誤 | 漏逗號、括號沒對齊 | 12%"
  anchor_type: 實驗結果
  comparison_target: 分類後的全部失敗案例（三類合計 100%）
  qualifiers:
  - text: 68% 是小模型失敗中的占比
    source_quote: "論文自己的實驗顯示，小模型 68% 的失敗正是這種「語意上合法但錯誤的更新被無感套用」"
  importance: 2
  status: normal
- id: c8
  role: evidence
  text: 論文的結論是：小模型失敗的根源是結構化輸出的遵從度（能不能照規定的格式和結構正確輸出），不是推理能力不足
  source_quotes:
  - "論文的結論是：小模型失敗的根源是結構化輸出的遵從度（能不能照規定的格式和結構正確輸出），不是推理能力不足。"
  anchor_type: 原作者解讀
  importance: 3
  status: normal
- id: c9
  role: evaluation
  text: blog 的推論是，第一類的 68% 就是驗證盲區的直接證據：語意上合法、但錯誤的 patch 被套用之後，沒辦法回頭校正
  source_quotes:
  - "我的推論是，第一類的 68% 就是前面那個驗證盲區的直接證據：語意上合法、但錯誤的 patch 被套用之後，沒辦法回頭校正。"
  anchor_type: 部落格推論
  comparison_target: 分類後的全部失敗案例（三類合計 100%）
  importance: 3
  status: normal
- id: c10
  role: evidence
  text: blog 推論同一個盲區也出現在軟體版本庫環境（Git 分支、commit、PR、CI 狀態彼此深度關聯）：25 步長的任務上，SKILL.state 輸給保留歷史的對照組 Stateful。單一動作可能連帶影響多個分支；一旦某次 patch 沒有正確捕捉到連帶影響（例如合併了 PR，卻漏了更新相依分支的狀態），錯誤可能一路延續到後面的步驟，因為沒有原始歷史文字可以回頭核對
  source_quotes:
  - "軟體版本庫：Git 分支、commit、PR、CI 狀態彼此深度關聯"
  - "換到關聯密集的軟體版本庫環境，在 25 步長的任務上，只留狀態的做法還輸給保留歷史的對照組。"
  - "我的推論是，這跟軟體版本庫的密集依賴有關。單一動作可能連帶影響多個分支；一旦某次 patch 沒有正確捕捉到連帶影響（例如合併了 PR，卻漏了更新相依分支的狀態），錯誤可能一路延續到後面的步驟，因為沒有原始歷史文字可以回頭核對。這正好是前面說的驗證盲區"
  - "它跟軟體版本庫 \\( T=25 \\) 的反例，本質上是同一個問題的不同表現。"
  anchor_type: 部落格推論
  comparison_target: 保留歷史的對照組 Stateful，同樣 25 步長的任務
  qualifiers:
  - text: 同一張表裡，軟體版本庫 T=50 時 SKILL.state 贏回來（0.86 對 0.74），T=100 領先擴大到 15 個百分點（0.78 對 0.63）
    source_quote: "\\( T=50 \\) 才贏回來（0.86 對 0.74），\\( T=100 \\) 領先擴大到 15 個百分點（0.78 對 0.63）。"
  importance: 3
  status: normal
- id: c11
  role: qualifier
  text: 論文承認，grammar-constrained decoding（生成時直接限制模型只能輸出符合語法的內容）可以消除純語法錯誤，但解決不了誤刪這類語意錯誤
  source_quotes:
  - "論文另外承認兩個附帶限制。"
  - "grammar-constrained decoding（生成時直接限制模型只能輸出符合語法的內容）可以消除上面第三類的純語法錯誤，但解決不了第一類的語意錯誤。"
  anchor_type: 原作者解讀
  importance: 3
  status: normal
- id: c12
  role: evaluation
  text: 論文自己的實驗暴露了驗證只擋得住格式，論文卻沒有明講它對架構的含義
  source_quotes:
  - "驗證只擋得住格式：論文自己的實驗（68% 的錯誤來自語意合法但錯誤的 patch）暴露了這一點，論文卻沒有明講它對架構的含義。"
  anchor_type: 部落格判斷
  importance: 4
  status: normal
- id: c13
  role: evaluation
  text: 關聯密集的任務，加上驗證擋不住的語意錯誤，是 SKILL.state 這個架構真正的軟肋
  source_quotes:
  - "關聯密集的任務，加上驗證擋不住的語意錯誤，是這個架構真正的軟肋。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 在模型能力上，弱模型的「合法但語意錯誤的 patch 被無感套用」是重大風險；強模型能降低這個風險，但前沿模型只是沒測過，沒有證據顯示完全免疫
    source_quote: "弱模型：合法但語意錯誤的 patch 被無感套用是重大風險 | 強模型能降低這個風險，但前沿模型只是沒測過，沒有證據顯示完全免疫"
  importance: 3
  status: normal
```
