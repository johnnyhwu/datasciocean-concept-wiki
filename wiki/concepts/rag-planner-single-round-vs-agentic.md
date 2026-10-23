---
id: rag-planner-single-round-vs-agentic
title: Planner 只負責路由、不負責判斷證據夠不夠：用了 LLM 做決策不等於 agentic，這套架構是單輪 pipeline
type_hint: 判斷
context_type: evidence_from_single_source
sources:
  - article: cerebras-rag
    article_title: "拆解 Cerebras 企業知識庫 RAG：窄腰設計、檢索推理解耦與 Pipeline 的邊界"
    url: https://datasciocean.com/paper-intro/cerebras-rag/
    sections:
      - 前言
      - 讓 LLM 做路由，而不是做苦工：Planner 與 Agent 編排
      - Planner：故意比它服務的工具還便宜
      - 兩種對外介面：MCP 與 Web UI
      - 這篇文章沒說的：單輪 pipeline 跟 agentic loop 的邊界
      - 單輪架構的兩個結構性限制
      - 該往哪個方向補強：兩個判斷問題
    first_appearance: true
parent: null
related:
  - retrieval-reasoning-decoupling
  - rrf-rank-fusion
  - rag-narrow-waist
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: "Planner 負責路由，不負責思考夠不夠：LLM 被用來動態決定「這次該用哪些工具」，但整條處理線是決策一次、平行執行一次、synthesis 一次，沒有「證據不夠、回頭再查一輪」的迴圈，本質上是單輪 pipeline，不是 agentic loop"
    source_quotes:
      - "Planner 負責路由，不負責思考夠不夠**：LLM 被用來動態決定「這次該用哪些工具」，但整條處理線是決策一次、平行執行一次、synthesis 一次，沒有「證據不夠、回頭再查一輪」的迴圈——本質上是單輪 pipeline，不是 agentic loop。"
    qualifiers:
      - text: "「這套架構本質上是單輪 pipeline，不是 agentic loop」是作者讀完後自己推導出來的判斷，Cerebras 的文章沒有直接講"
        source_quote: "最後會補上兩個文章沒有直接講、但討論過程中自己推導出來的判斷——**檢索與推理必須解耦**，以及**這套架構本質上是單輪 pipeline，不是 agentic loop**。"
    anchor_type: 部落格判斷
    importance: 1
    status: normal
  - id: c2
    role: context
    text: "Cerebras 內部知識庫系統「Cerebras Knowledge」每天處理超過 15,000 次查詢，資料橫跨 Slack、Wiki、程式碼倉庫、Jira，服務對象還包含自動化流程與 AI agent，不只是人類"
    source_quotes:
      - "Cerebras 在 2026 年 7 月發表了一篇部落格文章，介紹他們內部知識庫系統「Cerebras Knowledge」的架構——這系統每天處理超過 15,000 次查詢，資料橫跨 Slack、Wiki、程式碼倉庫、Jira，服務對象還包含自動化流程與 AI agent，不只是人類。"
    anchor_type: 官方宣稱
    numeric_kind: non_comparative
    numeric_reason: 計數
    importance: 2
    status: normal
  - id: c3
    role: context
    text: "如果每次查詢都無腦呼叫所有工具，不需要的工具也被觸發，會拖慢延遲、浪費成本，不相關工具吐出來的雜訊結果還可能拉低整體排序品質；Planner 存在的第一原理，是把「這次該用哪些工具」從固定規則變成一個動態決策，讓成本跟延遲跟查詢的實際需求成正比"
    source_quotes:
      - "如果每次查詢都無腦呼叫所有工具，會帶來兩個直接的壞處：不需要的工具也被觸發，拖慢延遲、浪費成本；不相關工具吐出來的雜訊結果，還可能拉低整體排序品質。Planner 存在的第一原理，是把「這次該用哪些工具」從固定規則變成一個動態決策，讓成本跟延遲跟查詢的實際需求成正比。"
    anchor_type: 部落格判斷
    importance: 3
    status: normal
  - id: c4
    role: anchor
    text: "Planner 拿到三樣輸入：一份工具目錄（只需要精簡的能力描述）、使用者的查詢本身、以及當前鎖定的查詢範圍（對應 Projects 概念）；輸出是一組工具選擇清單，交給 executor 平行執行"
    source_quotes:
      - "Planner 拿到三樣輸入：一份工具目錄（只需要精簡的能力描述，不需要完整技術文件或內部實作細節）、使用者的查詢本身、以及當前鎖定的查詢範圍（對應後面會講到的 Projects 概念）。輸出則是一組工具選擇清單，交給 executor 平行執行。"
    anchor_type: 設計參數
    importance: 4
    status: normal
  - id: c5
    role: anchor
    text: "Planner 被故意設計得比它服務的工具還便宜：它做的是分類任務（從有限選項裡選一個或幾個），不是生成任務，所以可以用小模型、結構化輸出，推理成本跟延遲都低，是整條處理線裡最便宜的一環"
    source_quotes:
      - "Planner 被故意設計得比它服務的工具還便宜——它做的是分類任務（從有限選項裡選一個或幾個），不是生成任務，所以可以用小模型、結構化輸出，推理成本跟延遲都低，是整條處理線裡最便宜的一環。"
    anchor_type: 設計參數
    importance: 5
    status: normal
  - id: c6
    role: evaluation
    text: "決策層要故意比執行層便宜，不然「用來省錢的決策」本身如果太貴，設計就自相矛盾了"
    source_quotes:
      - "決策層要故意比執行層便宜，不然「用來省錢的決策」本身如果太貴，設計就自相矛盾了。"
    anchor_type: 部落格判斷
    importance: 6
    status: normal
  - id: c7
    role: anchor
    text: "對 Planner 而言，工具永遠是個黑盒子：它只需要知道工具的能力描述，不需要知道工具內部是簡單查表，還是需要額外做一輪推理才能給出結果"
    source_quotes:
      - "對 Planner 而言，工具永遠是個黑盒子——它只需要知道工具的能力描述，不需要知道工具內部是簡單查表，還是需要額外做一輪推理才能給出結果。"
    anchor_type: 設計參數
    importance: 7
    status: normal
  - id: c8
    role: anchor
    text: "Executor 扛兩個職責：平行執行被選中的工具（前提是工具之間沒有依賴關係，本身是無狀態的檢索原語），以及把不同工具吐出的原始格式正規化成一套共同的 evidence schema（包含分數、新鮮度、來源提示等）"
    source_quotes:
      - "Executor 扛兩個職責：平行執行被選中的工具（前提是工具之間沒有依賴關係，本身是無狀態的檢索原語），以及把不同工具吐出的原始格式正規化成一套共同的 evidence schema（包含分數、新鮮度、來源提示等）。"
    anchor_type: 設計參數
    importance: 8
    status: normal
  - id: c9
    role: anchor
    text: "文章描述的完整流程是：查詢進來，planner 決策一次，平行執行一次，synthesis 一次，結束；這個結構性地不支援「發現資訊不夠、需要再查一輪」，因為文章的 executor 是 fan-out 完就結束，沒有「評估夠不夠、不夠再來一輪」的回饋路徑"
    source_quotes:
      - "文章描述的完整流程是：查詢進來，planner 決策一次，平行執行一次，synthesis 一次，結束。這個結構性地不支援兩種很常見的複雜需求。第一種是「發現資訊不夠、需要再查一輪」：synthesis 或某個中間步驟得能判斷「證據不夠」，然後回頭再發一次檢索，但文章的 executor 是 fan-out 完就結束，沒有「評估夠不夠、不夠再來一輪」的回饋路徑。"
    qualifiers:
      - text: "「這套架構本質上是單輪 pipeline，不是 agentic loop」是作者讀完後自己推導出來的判斷，Cerebras 的文章沒有直接講"
        source_quote: "最後會補上兩個文章沒有直接講、但討論過程中自己推導出來的判斷——**檢索與推理必須解耦**，以及**這套架構本質上是單輪 pipeline，不是 agentic loop**。"
    anchor_type: 部落格判斷
    importance: 9
    status: normal
  - id: c10
    role: anchor
    text: "單輪架構也不支援「先查某個、再根據結果查另一個」的序列依賴：文章明確採用平行執行，而平行的前提正是工具彼此獨立、互不依賴，如果工具 B 的輸入依賴工具 A 的輸出，在「平行 fan-out」這個模型下根本沒辦法表達"
    source_quotes:
      - "第二種是「先查某個、再根據結果查另一個」的序列依賴：文章明確採用平行執行，而平行的前提正是工具彼此獨立、互不依賴，如果工具 B 的輸入依賴工具 A 的輸出，在「平行 fan-out」這個模型下根本沒辦法表達。"
    qualifiers:
      - text: "「這套架構本質上是單輪 pipeline，不是 agentic loop」是作者讀完後自己推導出來的判斷，Cerebras 的文章沒有直接講"
        source_quote: "最後會補上兩個文章沒有直接講、但討論過程中自己推導出來的判斷——**檢索與推理必須解耦**，以及**這套架構本質上是單輪 pipeline，不是 agentic loop**。"
    anchor_type: 部落格判斷
    importance: 10
    status: normal
  - id: c11
    role: mechanism
    text: "這兩個問題往根源追其實是同一件事：系統缺少「狀態」和「多步推理」；單輪架構隱含的假設是，這次查詢需要哪些證據，在 planner 決策的那一刻就能被完全決定，但真實情況常常要看過第一輪結果之後才會知道還需要查什麼"
    source_quotes:
      - "這兩個問題表面看是兩件事，往根源追其實是同一件事：**系統缺少「狀態」和「多步推理」**。單輪架構隱含的假設是，這次查詢需要哪些證據，在一開始（planner 決策的那一刻）就能被完全決定；但真實情況常常是，「我還需要查什麼」這件事，往往要看過第一輪結果之後才會知道"
    qualifiers:
      - text: "「這套架構本質上是單輪 pipeline，不是 agentic loop」是作者讀完後自己推導出來的判斷，Cerebras 的文章沒有直接講"
        source_quote: "最後會補上兩個文章沒有直接講、但討論過程中自己推導出來的判斷——**檢索與推理必須解耦**，以及**這套架構本質上是單輪 pipeline，不是 agentic loop**。"
    anchor_type: 部落格判斷
    importance: 11
    status: normal
  - id: c12
    role: anchor
    text: "兩種範式的差異：文章的架構（RAG pipeline）決策一次、工具間獨立可平行、固定流程跑完就停；需要迭代或序列時的架構（agentic loop）多次決策、工具間可能有依賴需要序列、由判斷邏輯動態決定「夠了嗎」"
    source_quotes:
      - "決策次數 | 一次，決定完不再變 | 多次，每輪結果可能觸發下一輪決策"
      - "工具間關係 | 獨立，可平行 | 可能有依賴，需要序列"
      - "何時停止 | 固定流程跑完就停 | 由判斷邏輯動態決定「夠了嗎」"
    qualifiers:
      - text: "「這套架構本質上是單輪 pipeline，不是 agentic loop」是作者讀完後自己推導出來的判斷，Cerebras 的文章沒有直接講"
        source_quote: "最後會補上兩個文章沒有直接講、但討論過程中自己推導出來的判斷——**檢索與推理必須解耦**，以及**這套架構本質上是單輪 pipeline，不是 agentic loop**。"
    anchor_type: 部落格判斷
    importance: 12
    status: normal
  - id: c13
    role: evaluation
    text: "嚴格說，這篇文章做的不是「agentic RAG」，而是「用 LLM 做動態路由的傳統 RAG pipeline」"
    source_quotes:
      - "嚴格說，這篇文章做的不是「agentic RAG」，而是「用 LLM 做動態路由的傳統 RAG pipeline」。"
    qualifiers:
      - text: "「這套架構本質上是單輪 pipeline，不是 agentic loop」是作者讀完後自己推導出來的判斷，Cerebras 的文章沒有直接講"
        source_quote: "最後會補上兩個文章沒有直接講、但討論過程中自己推導出來的判斷——**檢索與推理必須解耦**，以及**這套架構本質上是單輪 pipeline，不是 agentic loop**。"
    anchor_type: 部落格判斷
    importance: 13
    status: normal
  - id: c14
    role: evaluation
    text: "用了 LLM 做決策，不等於 agentic；Agentic 的核心特徵是迴圈跟狀態，而不是決策過程裡有沒有 LLM 參與"
    source_quotes:
      - "用了 LLM 做決策，不等於 agentic**。Agentic 的核心特徵是迴圈跟狀態，而不是決策過程裡有沒有 LLM 參與。"
    anchor_type: 部落格判斷
    importance: 14
    status: normal
  - id: c15
    role: evaluation
    text: "文章給的不是「怎麼做迭代」的答案，而是「迭代迴圈裡每一輪該怎麼做好」的答案；單輪架構的品質決定了迴圈裡每一次迭代的品質，迴圈存在與否決定了系統能不能處理需要多步推理的複雜問題，這兩層彼此正交"
    source_quotes:
      - "文章給的不是「怎麼做迭代」的答案，而是「迭代迴圈裡每一輪該怎麼做好」的答案。"
      - "單輪架構的品質，決定了迴圈裡每一次迭代的品質；迴圈存在與否，決定了系統能不能處理需要多步推理的複雜問題。這兩層彼此正交。"
    qualifiers:
      - text: "「這套架構本質上是單輪 pipeline，不是 agentic loop」是作者讀完後自己推導出來的判斷，Cerebras 的文章沒有直接講"
        source_quote: "最後會補上兩個文章沒有直接講、但討論過程中自己推導出來的判斷——**檢索與推理必須解耦**，以及**這套架構本質上是單輪 pipeline，不是 agentic loop**。"
    anchor_type: 部落格判斷
    importance: 15
    status: normal
  - id: c16
    role: evaluation
    text: "第一個補強問題是「資訊不夠」的判斷發生在哪一層：如果是 synthesis 讀完證據後才發現不夠，需要在 synthesis 之後加一個 self-critique 或 sufficiency check 步驟，輸出「還缺什麼」再回頭餵給 planner 觸發下一輪；如果是使用者追問才觸發，那屬於對話管理的範疇，單輪 pipeline 每次追問重跑一次就夠了"
    source_quotes:
      - "第一個問題是「資訊不夠」的判斷發生在哪一層：如果是 synthesis 讀完證據後才發現不夠，需要在 synthesis 之後加一個 self-critique 或 sufficiency check 步驟，讓它輸出「還缺什麼」，再回頭餵給 planner 觸發下一輪；如果是使用者追問才觸發，那屬於對話管理的範疇，不是需要迴圈的迭代問題，單輪 pipeline 每次追問重跑一次就夠了。"
    anchor_type: 部落格判斷
    importance: 16
    status: normal
  - id: c17
    role: evaluation
    text: "第二個補強問題是序列依賴到底是「有限幾種固定模式」還是「真的需要 agent 臨場規劃」：如果模式有限，可以把序列寫成一個複合工具，內部固定執行順序，對外仍然是 planner 眼中的單一黑盒工具；如果序列依賴是開放式、需要 agent 臨場判斷下一步，那才是真正需要 agentic loop 的情況，此時整套 planner/executor/synthesis 架構最多只能降級成 agent loop 裡「單輪執行」的一個子模組"
    source_quotes:
      - "第二個問題是序列依賴到底是「有限幾種固定模式」還是「真的需要 agent 臨場規劃」：如果模式有限（比如固定「先查人、再查該人的 PR」這種兩步流程），不需要完整的 agentic loop，可以把這個序列寫成一個複合工具，內部固定執行順序，對外仍然是 planner 眼中的單一黑盒工具；如果序列依賴是開放式、沒有固定模式、需要 agent 臨場判斷下一步，那才是真正需要 agentic loop 的情況，此時文章整套 planner/executor/synthesis 架構，最多只能降級成 agent loop 裡「單輪執行」的一個子模組。"
    anchor_type: 部落格判斷
    importance: 17
    status: normal
```
