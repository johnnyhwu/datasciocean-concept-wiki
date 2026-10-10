---
id: skillopt-overview
title: 把凍結模型的技能文件當成可訓練的權重，用深度學習優化器的紀律來更新：學習只發生在一份文字檔，部署成本幾乎為零
type_hint: 方法概覽
context_type: bound_to_source
sources:
- article: skillopt
  article_title: "SkillOpt：把 AI Agent 的技能文件當成可訓練的權重來優化，不用碰模型本身"
  url: https://datasciocean.com/paper-intro/skillopt/
  sections:
  - 兩個模型，各司其職
  - 目標模型（M）
  - 優化器模型（O）
  - 技能檔案本身
  - 整套系統的深度學習類比
  - 餘弦衰減的預算
  - 排序哪些修改能過關
  - 每個 Epoch 結束時的宏觀調控
  - 真正做出決定的守門員
  - 這一切真的有效嗎？
  - 52 個組合的主要結果
  - 最終產物有多便宜？
  - 真的能泛化嗎？遷移實驗
  - 優化器強度：一定要前沿等級嗎？
  - 評分函式的瓶頸
  - Token 的經濟帳
  - 單一檔案終究撐不住規模
  - 總結
  first_appearance: true
parent: null
related:
  - skillopt-batch-evidence-minibatch
  - skillopt-bounded-edit-budget
  - skillopt-blind-acceptance-gate
  - skillopt-epoch-level-control
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: blog 總結 SkillOpt 真正主張的，是一種思維上的轉變：提示詞/技能的迭代，不該是黑盒子式的試錯，而應該是一套真正的優化管線，擁有深度學習領域早已視為理所當然的紀律——用成批的證據取代單一的軼事、用有界的步伐取代不受約束的重寫、用真正盲測的驗證切分取代憑感覺判斷，再加上一個較長時程的機制，防止短期的補丁侵蝕掉先前學到的教訓
  source_quotes:
  - SkillOpt 真正在主張的，是一種思維上的轉變：提示詞/技能的迭代，不該是一個黑盒子式的試錯過程，而應該是一套真正的優化管線，擁有深度學習領域早已視為理所當然的那些紀律——用成批的證據取代單一的軼事、用有界的步伐取代不受約束的重寫、用真正盲測的驗證切分取代憑感覺判斷「這個修改看起來有幫助」，再加上一個較長時程的機制，防止短期的補丁侵蝕掉先前學到的教訓
  anchor_type: 部落格判斷
  qualifiers:
  - text: 整套系統完全仰賴驗證守門機制，而驗證守門機制又完全仰賴一個便宜、可靠、自動化的評分方式
    source_quote: 整套系統完全仰賴驗證守門機制，而驗證守門機制又完全仰賴一個**便宜、可靠、自動化的評分方式**
  - text: 對於開放式、主觀性高的任務，要打造一個好到足以做為守門依據的評分器，可能需要引入 LLM-as-judge 這類機制，而這又把管線原本想避開的成本與雜訊帶了回來
    source_quote: 但對於開放式、主觀性高的任務(創意寫作、開放式的客服對話)，要打造一個好到足以做為守門依據的評分器，老實說可能需要引入 LLM-as-judge 這類機制，而這又把這整套管線原本想避開的成本與雜訊給帶了回來。
  importance: 1
  status: normal
- id: c2
  role: context
  text: SkillOpt 把責任拆分給兩個獨立的模型。目標模型是實際執行工作的那一方（回答問題、呼叫工具、寫程式碼）；它的權重與原生的 system prompt 在整個訓練過程中都保持凍結，唯一會隨著每一輪跑分而改變的，是被塞進它工作區、或附加在前面的技能文件
  source_quotes:
  - SkillOpt 把責任拆分給兩個獨立的模型，而不是要求同一個模型既要完成任務、又要幫自己的作業打分。
  - 目標模型是實際執行工作的那一方——回答問題、呼叫工具、寫程式碼
  - 它的權重與原生的 system prompt 在整個訓練過程中都保持凍結。對它來說唯一會隨著每一輪跑分而改變的，是被塞進它工作區、或附加在前面的技能文件
  anchor_type: 背景說明
  qualifiers:
  - text: 優化器也可以降級成跟目標模型一樣的模型，也就是目標模型自己優化自己
    source_quote: 即使把「教練」降級成跟目標模型一樣(規模小得多)的模型——也就是目標模型自己優化自己——有界更新加上驗證守門這套機制，依然足以挽回相較於前沿等級優化器所取得收益的 56% 到 74%。
  importance: 2
  status: normal
- id: c3
  role: mechanism
  text: 優化器模型完全不碰任務本身。它通常是一個能力更強的「前沿(frontier)」模型，而且只在離線訓練階段運作；它的工作是讀取目標模型的執行軌跡與分數，然後針對技能文件提出具體的修改建議
  source_quotes:
  - 優化器模型完全不碰任務本身。它通常是一個能力更強的「前沿(frontier)」模型，而且只在離線訓練階段運作。它的工作是讀取目標模型的執行軌跡與分數，然後針對技能文件提出具體的修改建議
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 把目標模型與優化器模型徹底分開，是這整套設計在部署階段成本幾乎為零的原因：訓練結束後，優化器那一側的 API 花費就消失了，實際送進正式環境的只有凍結的目標模型加一份小小的文字檔
  source_quotes:
  - 把這兩個角色徹底分開，正是這整套設計在部署階段成本幾乎為零的原因：一旦訓練結束，優化器那一側的 API 花費就完全消失了，實際送進正式環境的，只有那個凍結的目標模型，加上一份小小的文字檔。
  anchor_type: 部落格判斷
  qualifiers:
  - text: 即使只訓練一份技能，也需要花上數千萬到上億個訓練 token
    source_quote: 即使只訓練一份技能，也需要花上數千萬到上億個訓練 token
  importance: 4
  status: normal
- id: c5
  role: context
  text: 被優化的技能文件是一份叫 best_skill.md 的文字檔，長度通常落在 300 到 2,000 個 token 之間；單純問答任務時直接附加到 system prompt 前面，操作工具的 Agent（如 Codex、Claude Code）則寫進工作區，作為存在硬碟上的持久筆記
  source_quotes:
  - 長度通常落在 300 到 2,000 個 token 之間。依照執行環境的不同，它有時會直接被附加到 system prompt 前面(適用於單純的問答任務)，有時則會被寫進目標模型的工作區，作為一份持久化、存在硬碟上的筆記(適用於像 Codex 或 Claude Code 這種操作工具的 Agent)
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 5
  status: normal
- id: c6
  role: mechanism
  text: blog 說貫穿全文的心智模型，是直接對照經典深度學習優化器的類比：技能文件對應參數，基於 Minibatch 產生的修改建議對應梯度，編輯預算對應學習率，盲測守門機制與嚴格淘汰制對應驗證集 Checkpoint，逐 Epoch 的「慢速更新」對應動量／EMA
  source_quotes:
  - 貫穿全文的心智模型——也是讓後面所有設計都能說得通的關鍵——是直接對照經典深度學習優化器的類比
  - 參數…技能文件
  - 梯度 | 基於 Minibatch 產生的修改建議
  - 學習率 | 編輯預算
  - 驗證集 Checkpoint…盲測守門機制與嚴格淘汰制
  - 動量／EMA | 逐 Epoch 的「慢速更新」
  anchor_type: 部落格判斷
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: 只有排名前 L_t 名（L_t 是編輯預算）的修改，才能進入候選技能；候選技能要在優化器從未看過的切分上被盲測打分，嚴格大於目前技能的分數才會被寫入硬碟，成為新的目前技能；平手或分數下降，整個步驟都會被丟棄，先前的技能維持不變
  source_quotes:
  - SkillOpt 用**編輯預算** \( L_t \) 來限制單一步驟能套用多少修改
  - 只有排名前 \( L_t \) 名的修改，才能進入候選技能。
  - 必須靠著在 \( D_{sel} \) 上被盲測打分來爭取通過，而 \( D_{sel} \) 正是優化器從未看過的那個切分。只有當 \( \text{score}(\tilde{s}) \) **嚴格大於**目前技能的分數，這個候選才會被寫入硬碟，成為新的目前技能。平手或分數下降，則整個步驟都會被丟棄，先前的技能維持不變。
  anchor_type: 設計參數
  qualifiers:
  - text: 整套系統完全仰賴驗證守門機制，而驗證守門機制又完全仰賴一個便宜、可靠、自動化的評分方式
    source_quote: 整套系統完全仰賴驗證守門機制，而驗證守門機制又完全仰賴一個**便宜、可靠、自動化的評分方式**
  - text: 對於開放式、主觀性高的任務，要打造一個好到足以做為守門依據的評分器，可能需要引入 LLM-as-judge 這類機制，而這又把管線原本想避開的成本與雜訊帶了回來
    source_quote: 但對於開放式、主觀性高的任務(創意寫作、開放式的客服對話)，要打造一個好到足以做為守門依據的評分器，老實說可能需要引入 LLM-as-judge 這類機制，而這又把這整套管線原本想避開的成本與雜訊給帶了回來。
  importance: 7
  status: normal
- id: c8
  role: anchor
  text: 論文的主要結果是在六個基準測試、多種目標模型規模（從 GPT-5.5 到小得多的 Qwen3.5-4B）與三種執行環境（直接對話、Codex、Claude Code）下，共 52 個（模型、基準測試、執行環境）組合；SkillOpt 在這 52 個欄位裡每一個都拿到最佳或並列最佳（blog 同時稱它勝過 TextGrad、GEPA、EvoSkill 這類基準方法）
  source_quotes:
  - 論文的主要結果，是在六個基準測試、多種目標模型規模(從 GPT-5.5 一路到小得多的 Qwen3.5-4B)，以及三種執行環境(直接對話、Codex、Claude Code)下進行的主要比較——總共 52 個(模型、基準測試、執行環境)組合。
  - SkillOpt 在這 52 個欄位裡，每一個都拿到最佳或並列最佳的成績，全面勝過像 TextGrad、GEPA、EvoSkill 這類基準方法
  anchor_type: 實驗結果
  comparison_target: TextGrad、GEPA、EvoSkill 這類基準方法（blog 內文提到的對照）
  importance: 8
  status: normal
- id: c9
  role: anchor
  text: 提升幅度相當取決於執行環境：在單純的直接對話情境下平均提升約 +23.5 分，在 Codex 環境提升 +24.8 分，在 Claude Code 環境提升 +19.1 分
  source_quotes:
  - 提升幅度的大小則相當取決於執行環境：在單純的直接對話情境下，平均提升約 +23.5 分；在操作工具的 Codex 環境中，提升幅度同樣可觀，達到 +24.8 分；而在 Claude Code 環境中，則有相當可觀的 +19.1 分
  anchor_type: 實驗結果
  comparison_target: blog 內文沒寫這些「提升」是相對於誰（無技能基準，或其他基準方法）；需作者確認
  importance: 9
  status: pending_author_confirmation
- id: c11
  role: anchor
  text: 在全部六個基準測試中，最終的技能檔案都只需要一到四次被接受的修改；blog 說驗證守門把絕大多數提出的修改都擋了下來
  source_quotes:
  - 在全部六個基準測試中，最終的技能檔案都只需要**一到四次被接受的修改**——驗證守門把絕大多數提出的修改都擋了下來
  anchor_type: 實驗結果
  comparison_target: 被提出但被驗證守門擋下的修改（blog 只說「絕大多數」，沒給總數）
  importance: 10
  status: normal
- id: c12
  role: anchor
  text: 一份在 Codex 環境裡針對試算表任務訓練出來的技能，沒有進一步優化，直接丟進 Claude Code 環境，把那個環境的分數從 22.1 拉到 81.8（+59.7 分），甚至超過直接在 Claude Code 環境裡訓練出來的技能（80.4）
  source_quotes:
  - 一份在 Codex 環境裡針對試算表任務訓練出來的技能，在完全沒有進一步優化的情況下，直接丟進 Claude Code 環境，把那個環境的分數從 22.1 拉到 81.8——足足提升了 +59.7 分，而且這個成績甚至**超過**了直接在 Claude Code 環境裡訓練出來的技能(80.4)
  anchor_type: 實驗結果
  comparison_target: Claude Code 環境原本的分數 22.1，以及直接在 Claude Code 環境裡訓練出來的技能（80.4）
  qualifiers:
  - text: 這描述的是一份技能（Codex 環境針對試算表任務訓練）搬到 Claude Code 的一次遷移
    source_quote: 一份在 Codex 環境裡針對試算表任務訓練出來的技能
  importance: 11
  status: normal
- id: c14
  role: anchor
  text: 即使把優化器降級成跟目標模型一樣（規模小得多）的模型，也就是目標模型自己優化自己，有界更新加上驗證守門，依然足以挽回相較於前沿等級優化器所取得收益的 56% 到 74%
  source_quotes:
  - 即使把「教練」降級成跟目標模型一樣(規模小得多)的模型——也就是目標模型自己優化自己——有界更新加上驗證守門這套機制，依然足以挽回相較於前沿等級優化器所取得收益的 56% 到 74%。
  anchor_type: 實驗結果
  comparison_target: 前沿等級優化器所取得的收益
  qualifiers:
  - text: 自我教練的效果打了折扣，但遠遠稱不上沒用
    source_quote: 自我教練的效果雖然打了折扣，但遠遠稱不上沒用
  importance: 14
  status: normal
- id: c15
  role: anchor
  text: 每提升一分所需的訓練 token 數依任務型態差異極大：短、以工具呼叫為主的任務（SpreadsheetBench、OfficeQA）約 0.6M 到 1.1M，長上下文任務（SearchQA、DocVQA）約 38M 到 46M
  source_quotes:
  - 然而每提升一分所需的 token 成本，則依任務型態而有極大差異
  - 短、以工具呼叫為主(SpreadsheetBench、OfficeQA) | 0.6M – 1.1M
  - 長上下文(SearchQA、DocVQA) | 38M – 46M
  anchor_type: 實驗結果
  comparison_target: 短、以工具呼叫為主的任務與長上下文任務互相比較（每提升一分所需的訓練 token 數）
  importance: 15
  status: normal
- id: c16
  role: evaluation
  text: blog 指出部署階段沒有額外的推論、沒有額外的延遲，就只是一份靜態文字檔，但訓練要花數千萬到上億個 token，這個取捨明顯比較適合高頻率、結構穩定、犯錯代價高的正式生產 Agent，不太適合一次性或低頻的任務，後者的 token 投資大概永遠回不了本
  source_quotes:
  - 部署成本確實是零——沒有額外的推論、沒有額外的延遲，就只是一份靜態的文字檔——但如上面表 6 所示，即使只訓練一份技能，也需要花上數千萬到上億個訓練 token。這樣的取捨，明顯比較適合**高頻率、結構穩定、犯錯代價高**的正式生產 Agent(例如財務報表自動化、維運腳本執行)，而不太適合一次性或低頻的任務，對後者來說，這筆 token 投資大概永遠回不了本。
  anchor_type: 部落格判斷
  importance: 16
  status: normal
- id: c17
  role: evaluation
  text: blog 認為把一切塞進單一一份 best_skill.md 雖然簡潔，但在涵蓋數百種不同業務情境的大型、異質化部署裡會變成瓶頸：單一 Markdown 檔案很快就會撞上 context 上限，針對不同情境設計的規則也可能開始互相牴觸
  source_quotes:
  - 在結構上，這套設計刻意把一切都塞進單一一份
  - 檔案，以維持簡潔——但這正是在一個涵蓋數百種不同業務情境的大型、異質化部署裡，最終會變成瓶頸的地方。單一一份 Markdown 檔案很快就會撞上 context 上限，而針對不同情境設計的規則，也可能開始在同一份文件裡互相牴觸。
  anchor_type: 部落格判斷
  importance: 17
  status: normal
- id: c18
  role: evaluation
  text: blog 認為單一檔案撐不住規模時，如果真的需要擴展到那種規模，自然的下一步看起來會是把 SkillOpt 跟某種技能庫路由機制結合起來：多份針對不同領域、各自獨立優化的技能檔案，在執行時由一個調度器來選擇，而不是全部擠進同一份檔案裡
  source_quotes:
  - 如果真的需要擴展到那種規模，自然的下一步，看起來會是把 SkillOpt 跟某種技能庫路由機制結合起來——多份針對不同領域、各自獨立優化的技能檔案，在執行時由一個調度器來選擇，而不是全部擠進同一份檔案裡。
  anchor_type: 部落格推論
  importance: 18
  status: normal
- id: c19
  role: evaluation
  text: blog 認為遷移的結果強烈暗示，優化器萃取出來的東西，更接近「該怎麼用 Pandas 思考如何處理試算表資料」，而不是「該怎麼針對這個特定執行環境的語法來措辭指令」
  source_quotes:
  - 這強烈暗示，優化器萃取出來的東西，更接近「該怎麼用 Pandas 思考如何處理試算表資料」，而不是「該怎麼針對這個特定執行環境的語法來措辭指令」。
  anchor_type: 部落格推論
  importance: 19
  status: normal
- id: c20
  role: mechanism
  text: SkillOpt 用編輯預算 L_t 來限制單一步驟能套用多少修改，這是學習率在文字空間裡的直接對應；一次套用太多修改，就跟梯度下降時踩了太大的步伐一樣，技能文件可能因此陷入不穩定的狀態，並丟失先前辛苦累積下來的教訓
  source_quotes:
  - SkillOpt 用**編輯預算** \( L_t \) 來限制單一步驟能套用多少修改——這是學習率在文字空間裡的直接對應。一次套用太多修改，就跟梯度下降時踩了太大的步伐一樣：技能文件可能因此陷入不穩定的狀態，並丟失先前辛苦累積下來的教訓。
  anchor_type: 部落格判斷
  importance: 7
  status: normal
- id: c21
  role: mechanism
  text: 逐步的修改在設計上本來就是短視的，每一步都只針對最近這一批任務做出反應；為了抓住更長時程的退步，SkillOpt 加入第二層、比較慢的控制迴圈，每個 Epoch 才跑一次，而不是每個 Step 都跑
  source_quotes:
  - 逐步的修改在設計上本來就是短視的——每一步都只針對最近這一批 40 個任務做出反應。為了抓住更長時程的退步，SkillOpt 加入了第二層、比較慢的控制迴圈，每個 Epoch 才跑一次，而不是每個 Step 都跑。
  anchor_type: 部落格判斷
  importance: 8
  status: normal
```
