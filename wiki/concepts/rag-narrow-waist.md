---
id: rag-narrow-waist
title: 窄腰設計：異質資料收斂成極簡介面，寫入端與讀取端就能各自獨立演化
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
  - article: cerebras-rag
    article_title: "拆解 Cerebras 企業知識庫 RAG：窄腰設計、檢索推理解耦與 Pipeline 的邊界"
    url: https://datasciocean.com/paper-intro/cerebras-rag/
    sections:
      - 前言
      - 一個貫穿全文的心智模型：窄腰設計
      - 統一資料抽象層：連 Connector 都要收窄
      - 知識庫變大之後：Projects 與 Scoping
      - 結論
    first_appearance: true
parent: null
related:
  - rrf-rank-fusion
  - rag-planner-single-round-vs-agentic
  - retrieval-reasoning-decoupling
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: "窄腰的價值不在於「統一」這件事本身好看，而在於腰以上和腰以下可以各自獨立演化，互不干擾"
    source_quotes:
      - "窄腰的價值不在於「統一」這件事本身好看，而在於**腰以上和腰以下可以各自獨立演化，互不干擾**。"
    anchor_type: 部落格判斷
    importance: 1
    status: normal
  - id: c2
    role: context
    text: "窄腰設計像一個沙漏：上半部是各種異質的資料寫入來源，中間收窄成一個很單純的介面，下半部又重新展開成各種檢索與編排策略"
    source_quotes:
      - "想像一個沙漏：上半部是各種異質的資料寫入來源——Slack 討論串、Wiki 頁面、程式碼、Jira 票、甚至自訂資料庫；中間收窄成一個很單純的介面；下半部又重新展開成各種檢索與編排策略。"
    anchor_type: 部落格判斷
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
    role: anchor
    text: "在 Cerebras 的系統裡，這個「窄腰」就是一張 embeddings table，只有五個欄位：document（要被搜尋的文字）、embedding（向量）、metadata（一個不透明的 JSON）、source（哪裡來的）、timestamp"
    source_quotes:
      - "這個「窄腰」在 Cerebras 的系統裡就是一張 embeddings table，只有五個欄位：`document`（要被搜尋的文字）、`embedding`（向量）、`metadata`（一個不透明的 JSON）、`source`（哪裡來的）、`timestamp`。"
    anchor_type: 設計參數
    importance: 4
    status: normal
  - id: c5
    role: mechanism
    text: "想新增一個資料源，只要寫一個 connector 把資料塞進這五個欄位，讀取端完全不用改一行；想換一種檢索策略，也只要在讀取端動手，寫入端毫無感覺"
    source_quotes:
      - "想新增一個資料源，只要寫一個 connector 把資料塞進這五個欄位，讀取端完全不用改一行；想換一種檢索策略，也只要在讀取端動手，寫入端毫無感覺。"
    anchor_type: 部落格判斷
    importance: 5
    status: normal
  - id: c6
    role: anchor
    text: "Cerebras 的做法是徹底收到底：下游邏輯永遠不需要知道一行資料是從哪來的才能處理它，source 欄位只在最後呈現結果給使用者時才派上用場"
    source_quotes:
      - "Cerebras 的做法是徹底收到底：下游邏輯永遠不需要知道一行資料是從哪來的才能處理它，`source` 欄位只在最後呈現結果給使用者時才派上用場。"
    qualifiers:
      - text: Projects 是查詢時的邏輯過濾條件，例如對 metadata 裡的 source 欄位做範圍限制
        source_quote: "這代表 project 本質上是查詢時的邏輯過濾條件（例如對 metadata 裡的 `source` 欄位做範圍限制）"
    anchor_type: 設計參數
    importance: 6
    status: normal
  - id: c7
    role: evaluation
    text: "有個陷阱是「形式統一但語意分裂」：如果 embeddings table 為了遷就每個來源，額外加上 slack_channel、code_repo、jira_ticket_id 這種專屬欄位，下游的檢索邏輯還是得針對來源類型寫一堆 if-else，那其實不算真正收窄"
    source_quotes:
      - "有個陷阱是「形式統一但語意分裂」：如果 embeddings table 為了遷就每個來源，額外加上 `slack_channel`、`code_repo`、`jira_ticket_id` 這種專屬欄位，下游的檢索邏輯還是得針對來源類型寫一堆 if-else，那其實不算真正收窄。"
    anchor_type: 部落格判斷
    importance: 7
    status: normal
  - id: c8
    role: evaluation
    text: "判斷窄腰有沒有收乾淨，有個簡單的檢查點：如果下游的檢索或排序邏輯裡出現「if source == 'X' then...」這種分支，就代表窄腰還沒收乾淨"
    source_quotes:
      - "判斷窄腰有沒有收乾淨，有個簡單的檢查點：如果下游的檢索或排序邏輯裡出現「if source == 'X' then...」這種分支，就代表窄腰還沒收乾淨。"
    anchor_type: 部落格判斷
    importance: 8
    status: normal
  - id: c9
    role: anchor
    text: "每個 connector 只需要回答三個問題，而且只有這三個：資料怎麼變成 document 加 metadata（一個轉換函式）、怎麼從來源系統把資料拉過來（一個抓取函式）、多久同步一次；這三件事裡完全沒有「怎麼檢索」"
    source_quotes:
      - "每個 connector 只需要回答三個問題，而且**只有這三個**：資料怎麼變成 document 加 metadata（一個轉換函式）、怎麼從來源系統把資料拉過來（一個抓取函式）、多久同步一次（甚至可以像 Slack 一樣，每個頻道各自設定自己的頻率）。"
      - "這三件事裡完全沒有「怎麼檢索」"
    anchor_type: 設計參數
    importance: 9
    status: normal
  - id: c10
    role: anchor
    text: "契約夠窄帶來一個組織層面的紅利：新增資料源這件事可以完全下放給不熟悉核心系統的團隊自己做，開一個 PR、附上一個小型 Python module，只要輸出符合共享 schema 的一行資料，其餘全部自動接上"
    source_quotes:
      - "契約夠窄帶來一個組織層面的紅利：新增資料源這件事可以完全下放給不熟悉核心系統的團隊自己做。開一個 PR、附上一個小型 Python module，只要輸出符合共享 schema 的一行資料，其餘全部自動接上，不需要核心團隊介入。"
    anchor_type: 設計參數
    importance: 10
    status: normal
  - id: c11
    role: evaluation
    text: "如果新增一個資料源需要核心團隊介入才能完成，通常代表抽象層本身漏水了"
    source_quotes:
      - "這其實是個蠻好的判準：如果新增一個資料源需要核心團隊介入才能完成，通常代表抽象層本身漏水了。"
    anchor_type: 部落格判斷
    importance: 11
    status: normal
  - id: c12
    role: mechanism
    text: "metadata 欄位不只是拿來展示的附加資訊，它同時也是檢索排序訊號的載體，所以 metadata 的設計必須在寫 connector 的當下就想清楚未來可能需要哪些排序訊號，不然事後想加，代價是要把整個 corpus 重新處理一次"
    source_quotes:
      - "`metadata` 欄位不只是拿來展示的附加資訊，它同時也是檢索排序訊號的載體——例如後面會提到的 age decay（隨時間衰減的排序機制）就是直接讀 metadata 裡的 timestamp。這代表 metadata 的設計必須在寫 connector 的當下就想清楚未來可能需要哪些排序訊號（時間戳、來源類型、作者或團隊資訊），不然事後想加，代價是要把整個 corpus 重新處理一次。"
    anchor_type: 部落格判斷
    importance: 12
    status: normal
  - id: c13
    role: anchor
    text: "窄腰的形狀在文章裡至少重複出現三次：資料寫入層收斂成同一張 embeddings table、讀取融合層由 RRF 融合成單一排序、多工具輸出層由 executor 正規化成共同的 evidence schema"
    source_quotes:
      - "值得特別注意的是，這個「窄腰」的形狀在文章裡至少重複出現三次，不是只在資料寫入層出現一次而已"
      - "資料寫入層 | Slack、Wiki、程式碼、Jira 等異質來源 | 同一張 embeddings table"
      - "讀取融合層 | 多個檢索器各自的排名 | RRF 融合成單一排序"
      - "多工具輸出層 | 不同工具吐出格式各異的結果 | executor 正規化成共同的 evidence schema"
    anchor_type: 部落格判斷
    importance: 13
    status: normal
  - id: c14
    role: evaluation
    text: "「全域搜尋」這個假設，規模一大就會系統性地惡化：corpus 越大，噪音對排序品質的侵蝕越嚴重，原本不相關的文件，只要跟查詢沾到一點語意邊或字面邊，就有機會擠進候選集合前段，把真正該出現的答案往下推"
    source_quotes:
      - "「全域搜尋」這個假設，規模一大就會系統性地惡化。corpus 越大，噪音對排序品質的侵蝕越嚴重——原本不相關的文件，只要跟查詢沾到一點語意邊或字面邊，就有機會擠進候選集合前段，把真正該出現的答案往下推。"
    anchor_type: 部落格判斷
    importance: 14
    status: normal
  - id: c15
    role: anchor
    text: "Cerebras 的解法是 Projects：一個 project 就是一組具名的資料源 bundle，關鍵字是「引用」而不是「複製」，同一個資料源可以被多個 project 引用，不需要真的複製一份資料出來"
    source_quotes:
      - "Cerebras 的解法是 Projects：一個 project 就是一組具名的資料源 bundle。關鍵字是「引用」而不是「複製」——同一個資料源可以被多個 project 引用，不需要真的複製一份資料出來。"
    anchor_type: 設計參數
    importance: 15
    status: normal
  - id: c16
    role: evaluation
    text: "project 本質上是查詢時的邏輯過濾條件，而不是一個新的資料容器；這個設計避開了資料更新一致性的風險，也避開了儲存成本隨 project 數量線性成長的問題，新增一個 project 完全不需要碰任何資料寫入邏輯"
    source_quotes:
      - "這代表 project 本質上是查詢時的邏輯過濾條件（例如對 metadata 裡的 `source` 欄位做範圍限制），而不是一個新的資料容器。這個設計避開了資料更新一致性的風險，也避開了儲存成本隨 project 數量線性成長的問題，同樣體現了「寫入端與讀取端獨立演化」的原則——新增一個 project，完全不需要碰任何資料寫入邏輯。"
    anchor_type: 部落格判斷
    importance: 16
    status: normal
  - id: c17
    role: evaluation
    text: "scope 過濾應該在 RRF 融合之前就先執行，不是等融合、rerank 都做完才篩選，不然會浪費排序運算在 scope 外的資料上，還可能讓 top-K 名額被 scope 外的文件佔掉"
    source_quotes:
      - "scope 過濾應該在 RRF 融合之前就先執行，不是等融合、rerank 都做完才篩選，不然會浪費排序運算在 scope 外的資料上，還可能讓 top-K 名額被 scope 外的文件佔掉。"
    anchor_type: 部落格判斷
    importance: 17
    status: normal
  - id: c18
    role: anchor
    text: "Cerebras 的做法是把預設 project 直接綁在使用者的 profile 上；如果要求使用者自行選擇 scope，等於把「系統該懂的組織知識」轉嫁給使用者，這其實是本末倒置"
    source_quotes:
      - "至於新使用者要怎麼知道該選哪個 scope，Cerebras 的做法是把預設 project 直接綁在使用者的 profile 上。如果要求使用者自行選擇 scope，等於把「系統該懂的組織知識」轉嫁給使用者，這其實是本末倒置"
    anchor_type: 部落格判斷
    importance: 18
    status: normal
  - id: c19
    role: evaluation
    text: "窄腰原則從資料抽象層、讀取融合層、多工具編排層，到組織 scoping 層反覆出現了四次，是最值得內化的單一心智模型"
    source_quotes:
      - "這個原則從資料抽象層、讀取融合層、多工具編排層，到組織 scoping 層反覆出現了四次，是最值得內化的單一心智模型。"
    anchor_type: 部落格判斷
    importance: 19
    status: normal
```

## 名詞補充（通用知識，非 blog 內容）

- corpus：被檢索的整批文件集合（語料庫）。
- top-K：排序後取前 K 筆結果。
- rerank：檢索出候選之後，再用另一個模型重新排序。
