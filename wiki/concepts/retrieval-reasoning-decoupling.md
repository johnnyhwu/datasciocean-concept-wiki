---
id: retrieval-reasoning-decoupling
title: 檢索與推理必須解耦：檢索工具只吐原始證據，推理只在管線末端的單次 synthesis 發生
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
  - article: cerebras-rag
    article_title: "拆解 Cerebras 企業知識庫 RAG：窄腰設計、檢索推理解耦與 Pipeline 的邊界"
    url: https://datasciocean.com/paper-intro/cerebras-rag/
    sections:
      - 前言
      - Planner：故意比它服務的工具還便宜
      - 兩種對外介面：MCP 與 Web UI
      - 原本系統的問題：檢索與推理耦合
      - 解耦之後的具體收穫
      - 結論
    first_appearance: true
parent: null
related:
  - rag-planner-single-round-vs-agentic
  - rag-narrow-waist
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: "檢索與推理必須解耦：把推理徹底移出檢索路徑，只在管線末端的單次 synthesis 發生，才能同時解決「跨領域難共用」與「新資料類型要重複開發」這兩個問題"
    source_quotes:
      - "第一，檢索與推理必須解耦：把推理徹底移出檢索路徑，只在管線末端的單次 synthesis 發生，才能同時解決「跨領域難共用」與「新資料類型要重複開發」這兩個問題。"
    qualifiers:
      - text: 不是所有「檢索前的推理」都該被消除；如果某類檢索的本質是計算而非查表（像 SQL 生成需要當場推理才能取得數據），那次推理應該保留，但要藏進檢索工具內部
        source_quote: "當然不是所有「檢索前的推理」都該被消除。前面提過的 lookup vs compute 判準在這裡同樣適用：如果某類檢索的本質是計算而非查表（像 SQL 生成需要當場推理才能取得數據），那次推理應該保留，但要藏進檢索工具內部，只對外暴露「吐出查詢到的證據」，而不是「產生面向使用者問題的部分答案」。"
      - text: 「檢索與推理必須解耦」是作者讀完後自己推導出來的判斷，Cerebras 的文章沒有直接講
        source_quote: "最後會補上兩個文章沒有直接講、但討論過程中自己推導出來的判斷——**檢索與推理必須解耦**"
    anchor_type: 部落格判斷
    importance: 1
    status: normal
  - id: c2
    role: context
    text: "這是作者拿自己手上企業 RAG 系統回頭對照 Cerebras 的文章後，自己推導出來的判斷，不是文章直接寫出來的"
    source_quotes:
      - "最後會補上兩個文章沒有直接講、但討論過程中自己推導出來的判斷——**檢索與推理必須解耦**"
    anchor_type: 部落格推論
    importance: 2
    status: normal
  - id: c3
    role: context
    text: "Cerebras 內部知識庫系統「Cerebras Knowledge」每天處理超過 15,000 次查詢，資料橫跨 Slack、Wiki、程式碼倉庫、Jira，服務對象還包含自動化流程與 AI agent，不只是人類"
    source_quotes:
      - "Cerebras 在 2026 年 7 月發表了一篇部落格文章，介紹他們內部知識庫系統「Cerebras Knowledge」的架構——這系統每天處理超過 15,000 次查詢，資料橫跨 Slack、Wiki、程式碼倉庫、Jira，服務對象還包含自動化流程與 AI agent，不只是人類。"
    anchor_type: 官方宣稱
    numeric_kind: non_comparative
    numeric_reason: 計數
    importance: 3
    status: normal
  - id: c4
    role: context
    text: "作者原本的系統以「領域/客戶」作為分化維度，每個領域綁定固定的幾種檢索方法，例如某個領域固定用三種檢索方法打三種資料庫，再合併結果"
    source_quotes:
      - "我原本的系統以「領域/客戶」作為分化維度，每個領域綁定固定的幾種檢索方法——比如某個領域固定用三種檢索方法打三種資料庫，再合併結果。"
    anchor_type: 部落格舉例
    importance: 4
    status: normal
  - id: c5
    role: evidence
    text: "這種設計規模一大就暴露出兩個問題：第一，不同領域即使有相同類型的資料或問題，也很難共用檢索方法，因為方法是綁死在領域維度上的；第二，同一個領域內只要新增一種資料類型，就得開發一種新的檢索方法，沒辦法對單一查詢的意圖做動態調整"
    source_quotes:
      - "這種設計規模一大就暴露出兩個問題。第一，不同領域即使有相同類型的資料或問題，也很難共用檢索方法，因為方法是綁死在領域維度上的。第二，同一個領域內只要新增一種資料類型，就得開發一種新的檢索方法，分化的粒度綁在領域層級，沒辦法對單一查詢的意圖做動態調整。"
    anchor_type: 部落格判斷
    importance: 5
    status: normal
  - id: c6
    role: mechanism
    text: "兩個問題共同的病灶是「檢索與推理耦合」：原本三種檢索各自呼叫對應的推理方法（比如 SQL 推理、圖文推理），各自產生一份摘要，最後再用一次 LLM 合併三份摘要，等於每一路檢索都內建了完整的推理與摘要流程"
    source_quotes:
      - "往根因追下去，這兩個問題共同的病灶是「檢索與推理耦合」。原本的融合流程是這樣的：三種檢索各自呼叫對應的推理方法（比如 SQL 推理、圖文推理），各自產生一份摘要，最後再用一次 LLM 合併三份摘要。等於每一路檢索都內建了完整的推理與摘要流程，檢索跟推理在架構上根本分不開"
    anchor_type: 部落格判斷
    importance: 6
    status: normal
  - id: c7
    role: mechanism
    text: "耦合導致沒辦法跨領域共用（推理邏輯焊死在檢索上），也沒辦法用動態 planner 取代領域綁定（因為每一路不是純粹的檢索原語，而是一整套完整的問答套件）"
    source_quotes:
      - "這導致沒辦法跨領域共用（推理邏輯焊死在檢索上），也沒辦法用動態 planner 取代領域綁定（因為每一路不是純粹的檢索原語，而是一整套完整的問答套件）。"
    anchor_type: 部落格判斷
    importance: 7
    status: normal
  - id: c8
    role: mechanism
    text: "文章帶來的重構方向是把檢索跟推理解耦：檢索工具只負責吐出原始證據，不做推理、不做摘要，推理只在管線最末端的單次 synthesis 發生"
    source_quotes:
      - "文章帶來的重構方向很清楚：把檢索跟推理解耦，檢索工具只負責吐出原始證據，不做推理、不做摘要，推理只在管線最末端的單次 synthesis 發生。"
    qualifiers:
      - text: 「檢索與推理必須解耦」是作者讀完後自己推導出來的判斷，Cerebras 的文章沒有直接講
        source_quote: "最後會補上兩個文章沒有直接講、但討論過程中自己推導出來的判斷——**檢索與推理必須解耦**"
      - text: 不是所有「檢索前的推理」都該被消除；如果某類檢索的本質是計算而非查表（像 SQL 生成需要當場推理才能取得數據），那次推理應該保留，但要藏進檢索工具內部
        source_quote: "當然不是所有「檢索前的推理」都該被消除。前面提過的 lookup vs compute 判準在這裡同樣適用：如果某類檢索的本質是計算而非查表（像 SQL 生成需要當場推理才能取得數據），那次推理應該保留，但要藏進檢索工具內部，只對外暴露「吐出查詢到的證據」，而不是「產生面向使用者問題的部分答案」。"
    anchor_type: 部落格判斷
    importance: 8
    status: normal
  - id: c9
    role: evidence
    text: "解耦之後，檢索工具變成乾淨、無狀態、不綁推理的原語，天生可以跨領域共用；配合 planner 機制，新增資料類型只需要新增一個檢索工具、更新它的能力描述，planner 自動就會學會在合適的查詢選用它，不需要動既有的推理邏輯"
    source_quotes:
      - "跨領域難共用的問題被解決了，因為解耦之後，檢索工具變成乾淨、無狀態、不綁推理的原語，天生可以跨領域共用。新增資料類型要重新開發檢索方法的問題也解決了，配合 planner 機制，新增資料類型只需要新增一個檢索工具、更新它的能力描述，planner 自動就會學會在合適的查詢選用它，不需要動既有的推理邏輯。"
    anchor_type: 部落格判斷
    importance: 9
    status: normal
  - id: c10
    role: evidence
    text: "解耦修復了跨源推理的能力：原架構「每一路各自完整推理再摘要」，沒有任何一個 LLM 同時看過全部證據，如果正確答案需要跨源交叉推理（比如「A 的一句話加上 B 的一張圖」），原架構結構性地做不到；單次 synthesis 讓所有證據攤在同一個 context 裡一次推理，天生就支援跨源推理"
    source_quotes:
      - "更根本的是修復了跨源推理的能力。原架構裡「每一路各自完整推理再摘要」的做法，會導致沒有任何一個 LLM 同時看過全部證據，如果正確答案需要跨源交叉推理（比如「A 的一句話加上 B 的一張圖」），原架構結構性地做不到。文章架構的單次 synthesis 讓所有證據攤在同一個 context 裡一次推理，天生就支援跨源推理。"
    anchor_type: 部落格判斷
    importance: 10
    status: normal
  - id: c11
    role: evidence
    text: "原架構的「摘要的摘要」（每一路先摘要、最後再合併摘要）是兩層有損壓縮疊加，下游完全無法察覺上游丟失了什麼細節；文章架構只在最末端壓縮一次，證據在此之前保持原始形態，誤差不會累積兩次"
    source_quotes:
      - "另外原架構「摘要的摘要」（每一路先摘要、最後再合併摘要）是兩層有損壓縮疊加，下游完全無法察覺上游丟失了什麼細節；文章架構只在最末端壓縮一次，證據在此之前保持原始形態，誤差不會累積兩次。"
    anchor_type: 部落格判斷
    importance: 11
    status: normal
  - id: c12
    role: mechanism
    text: "區分「查表（lookup）」跟「計算（compute）」：文章列出的工具檢索的對象都是已經被 embed 或索引好、預先算好的靜態資料，檢索動作本質上是唯讀撈取，撈出來就是最終形態的證據；SQL 場景本質不同，「把相關數據取出來」本身需要當場生成 SQL、執行，是一個不可省略的推理步驟，不是唯讀撈取"
    source_quotes:
      - "關鍵在區分「查表（lookup）」跟「計算（compute）」。文章列出的工具——搜尋、搜尋 Slack、搜尋程式碼、查詢誰懂這個領域等等——檢索的對象都是已經被 embed 或索引好、預先算好、躺在那裡等人拿的靜態資料，檢索動作本質上是唯讀撈取，撈出來就是最終形態的證據，可以直接進融合排序，不需要額外推理。SQL 場景本質不同：「把相關數據取出來」這件事本身需要當場生成 SQL、執行，才能得到答案，這是一個不可省略的推理步驟，不是唯讀撈取。"
    anchor_type: 部落格判斷
    importance: 12
    status: normal
  - id: c13
    role: mechanism
    text: "判準是看這次 LLM 呼叫的產出性質：如果產出是「證據」（下游還要再加工），可以保留這一步，但要藏在檢索工具內部；如果產出是「面向使用者問題的部分答案」（比如針對單一資料源提前生成的摘要文字），那一步就該砍掉，延後到管線最末端的單次 synthesis"
    source_quotes:
      - "判準是看這次 LLM 呼叫的產出性質：如果產出是「證據」（下游還要再加工），可以保留這一步，但要**藏在檢索工具內部**——SQL 生成該留在 `search_sql` 這個工具內部，作為取得查詢結果數據的必要步驟，對外只暴露它吐出的數據列。如果產出是「面向使用者問題的部分答案」（比如針對單一資料源提前生成的摘要文字），那一步就該砍掉，延後到管線最末端的單次 synthesis。"
    anchor_type: 部落格判斷
    importance: 13
    status: normal
  - id: c14
    role: anchor
    text: "Cerebras 的系統對外提供兩種介面，共用同一套原語：MCP 介面刻意不包含 planner，只暴露最基本的檢索原語，工具被設計得盡量簡單、盡量不依賴 LLM，由外部 agent（比如 Claude Code）自己決定呼叫順序跟怎麼組合結果"
    source_quotes:
      - "系統對外提供兩種介面，共用同一套原語，但設計目的完全不同。MCP 介面刻意不包含 planner，只暴露最基本的檢索原語，工具被設計得盡量簡單、盡量不依賴 LLM，由外部 agent（比如 Claude Code）自己決定呼叫順序跟怎麼組合結果。"
    anchor_type: 設計參數
    importance: 14
    status: normal
  - id: c15
    role: anchor
    text: "Web UI 介面則相反，把 planner、executor、synthesizer 全部包起來，對使用者呈現一個單純的問答介面"
    source_quotes:
      - "Web UI 介面則相反，把 planner、executor、synthesizer 全部包起來，對使用者呈現一個單純的問答介面。"
    anchor_type: 設計參數
    importance: 15
    status: normal
  - id: c16
    role: evaluation
    text: "MCP 的使用者是另一個具備推理能力的 agent，不該替它預先做決策——如果工具背後偷藏一層 planner，外部 agent 對工具行為的預期就會失控，因為工具行為不再是輸入的確定性函數，而是取決於一個它看不到的隱藏決策層；Web UI 的使用者是人類，人類不會自己組合工具呼叫，系統必須替他把整套流程包好"
    source_quotes:
      - "MCP 的使用者是另一個具備推理能力的 agent，不該替它預先做決策——如果工具背後偷藏一層 planner，外部 agent 對工具行為的預期就會失控，因為工具行為不再是輸入的確定性函數，而是取決於一個它看不到的隱藏決策層。Web UI 的使用者是人類，人類不會自己組合工具呼叫，系統必須替他把整套流程包好。"
    anchor_type: 部落格判斷
    importance: 16
    status: normal
  - id: c17
    role: evaluation
    text: "如果系統未來想被其他 agent 呼叫使用，就必須把「檢索原語」跟「編排決策」拆成兩層、可以獨立暴露的介面——這其實是「檢索與推理解耦」原則在更高一層（編排層）的重演"
    source_quotes:
      - "如果系統未來想被其他 agent 呼叫使用，就必須把「檢索原語」跟「編排決策」拆成兩層、可以獨立暴露的介面——這其實是「檢索與推理解耦」原則在更高一層（編排層）的重演"
    anchor_type: 部落格判斷
    importance: 17
    status: normal
```
