---
id: judgment-skill-hard-rules-tool-code
title: "需要判斷的交給模型或 skill，絕對不能違反的寫進 tool 程式碼，固定的機械式步驟留給一般程式碼"
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
  - article: subagent-fold
    article_title: "該不該拆 Subagent？Anthropic 談把多 Agent 折回單一 Agent Loop"
    url: https://datasciocean.com/ai-concept/subagent-fold/
    sections:
      - 一個沒說錯、卻漏掉發票的 subagent
      - 目標架構：單一 loop 加上漸進式揭露
      - 原本的元件搬去哪
      - 三種做法，依序進行
      - 沒有各自的 agent 之後，團隊要負責什麼
      - Tool、skill、知識庫怎麼選
      - Tool 的設計：依意圖分組，規則寫在程式碼裡
      - 這些主張有多扎實
      - 結論
    first_appearance: true
parent: null
related:
  - subagent-boundary-lossy-handoff
  - single-loop-progressive-disclosure
  - subagent-fold-eval-gated-migration
  - conway-law-agent-org-chart
  - policy-split-derive-questions-rules
  - claude-code-permission-blast-radius
  - jevact-pre-execution-gate
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: '需要判斷的交給模型或 skill，絕對不能違反的寫進 tool 程式碼，固定的機械式步驟留給一般程式碼'
    source_quotes:
      - '需要判斷的交給模型或 skill，絕對不能違反的寫進 tool 程式碼，固定的機械式步驟留給一般程式碼。'
    anchor_type: 部落格判斷
    importance: 1
    status: normal
  - id: c2
    role: context
    text: '企業裡的 agent 很常長成這樣：每個團隊各做一個 subagent（被上層叫去處理某一件子任務的 agent），平台團隊再疊一個 orchestrator（負責把問題分派給各個 subagent 的上層 agent）'
    source_quotes:
      - '企業裡的 agent 很常長成這樣：每個團隊各做一個 subagent（被上層叫去處理某一件子任務的 agent），平台團隊再疊一個 orchestrator（負責把問題分派給各個 subagent 的上層 agent）。'
    anchor_type: 背景說明
    importance: 2
    status: normal
  - id: c3
    role: context
    text: 'Anthropic 最近一篇文章主張，這種架構很多時候可以折回單一 agent loop'
    source_quotes:
      - 'Anthropic 最近一篇文章主張，這種架構很多時候可以折回單一 agent loop。'
    anchor_type: 原作者解讀
    qualifiers:
      - text: '不是全部都要折：文章列了三種仍該保留 subagent 的情況'
        source_quote: '當然也不是全部都要折。文章列了三種仍該保留 subagent 的情況'
    importance: 3
    status: normal
  - id: c4
    role: context
    text: '折回的單一 loop 裡，領域知識寫成 skills（寫給 agent 看的做事說明），能力做成 tools（agent 可以呼叫的功能，例如查訂單）；折成單一 loop 之後，多 agent 架構裡的各種元件不會憑空消失，而是各自找到新的家'
    source_quotes:
      - '領域知識寫成 skills（寫給 agent 看的做事說明），能力做成 tools（agent 可以呼叫的功能，例如查訂單）'
      - '折成單一 loop 之後，多 agent 架構裡的各種元件不會憑空消失，而是各自找到新的家。'
    anchor_type: 設計參數
    importance: 4
    status: normal
  - id: c5
    role: mechanism
    text: 'router 與意圖分類器（先判斷「這個問題該交給哪個 subagent」的元件）搬去模型：模型讀目錄，自己挑 skill 和 tool'
    source_quotes:
      - '表中第一列的 router 與意圖分類器，指的是先判斷「這個問題該交給哪個 subagent」的元件'
      - 'router、意圖分類器 | 模型讀目錄，自己挑 skill 和 tool'
    anchor_type: 設計參數
    qualifiers:
      - text: '「選擇本身就是模型擅長的判斷」這個理由是 blog 的推論；文章只說 router 被折進主 loop'
        source_quote: '選擇本身就是模型擅長的判斷（推論；文章只說 router 被折進主 loop）'
    importance: 5
    status: normal
  - id: c6
    role: mechanism
    text: '依規則改寫計畫的程式碼不需要了，理由是模型每一步自己決定；步驟順序、領域流程搬進 skills，理由是這是「團隊怎麼做事」的知識'
    source_quotes:
      - '依規則改寫計畫的程式碼 | 不需要了 | 模型每一步自己決定'
      - '步驟順序、領域流程 | skills | 這是「團隊怎麼做事」的知識'
    anchor_type: 設計參數
    importance: 6
    status: normal
  - id: c7
    role: mechanism
    text: '硬限制（驗證、核准閘門）放進 tools 內部，理由是它們必須百分之百遵守，不能靠模型記得'
    source_quotes:
      - '硬限制（驗證、核准閘門） | tools 內部 | 必須百分之百遵守，不能靠模型記得'
    anchor_type: 設計參數
    importance: 7
    status: normal
  - id: c8
    role: mechanism
    text: '規則寫在 prompt 裡，只是「請」模型遵守；寫在 tool 的程式碼裡，則是條件不符時直接擋下，並回傳模型看得懂的訊息'
    source_quotes:
      - '規則寫在 prompt 裡，只是「請」模型遵守；寫在 tool 的程式碼裡，則是條件不符時直接擋下，並回傳模型看得懂的訊息。'
      - '文中標（推論）的是筆者在文章之外的推斷，標（自編）的是為了說明而設計的情境，標（一般知識）的是業界通用的背景知識；沒有標的都是文章內容。'
    anchor_type: 原作者解讀
    importance: 8
    status: normal
  - id: c9
    role: mechanism
    text: '對話中途才需要的事（例如查記憶）做成 tools，需要時才呼叫；便宜、幾乎每次都用到的東西（例如 entity resolution，把口語說法對應到具體訂單）由程式碼預先載入，不值得讓模型每次都決定一遍'
    source_quotes:
      - '對話中途才需要的事（例如查記憶） | tools | 需要時才呼叫'
      - '便宜、幾乎每次都用到的東西（例如 entity resolution，把口語說法對應到具體訂單） | 程式碼預先載入 | 不值得讓模型每次都決定一遍'
    anchor_type: 設計參數
    importance: 9
    status: normal
  - id: c10
    role: mechanism
    text: '機械式處理（組 API 請求、解析串流、問完使用者後接回流程）是固定步驟，寫成程式碼，包在 tool 裡'
    source_quotes:
      - '機械式處理（組 API 請求、解析串流、問完使用者後接回流程） | 程式碼，包在 tool 裡 | 固定步驟'
    anchor_type: 設計參數
    qualifiers:
      - text: '「問完使用者後接回流程」原文是 resuming a clarification，文章沒有解釋，這個理解是 blog 的推論'
        source_quote: '「問完使用者後接回流程」原文是 resuming a clarification，文章沒有解釋，這裡的理解是推論。'
    importance: 10
    status: normal
  - id: c11
    role: mechanism
    text: 'tool 要依使用者意圖分組，不要一支 API 一個 tool；不常用的 tool，再用 tool search 延遲載入'
    source_quotes:
      - '**依使用者意圖分組，不要一支 API 一個 tool。**'
      - '不常用的 tool，再用 tool search 延遲載入。'
    anchor_type: 設計參數
    importance: 11
    status: normal
  - id: c12
    role: evidence
    text: 'System prompt 裡的 tool 定義超過 30 到 50 個，工具選擇的準確度通常會下降'
    source_quotes:
      - 'System prompt 裡的 tool 定義超過 30 到 50 個，工具選擇的準確度通常會下降'
    anchor_type: 官方宣稱
    numeric_kind: non_comparative
    numeric_reason: 計數
    qualifiers:
      - text: '文章沒說這是哪個模型、哪類任務的觀察'
        source_quote: '（文章沒說是哪個模型、哪類任務的觀察）'
    importance: 12
    status: normal
  - id: c13
    role: anchor
    text: '一支 API 一個 tool 時（get_order、get_shipment、get_carrier_status），模型要自己判斷串哪幾個、按什麼順序；依意圖分組成 track_order、內部依序呼叫三支 API，模型只要判斷使用者想追包裹'
    source_quotes:
      - '一支 API 一個 tool | `get_order`、`get_shipment`、`get_carrier_status` | 自己判斷要串哪幾個、按什麼順序'
      - '依意圖分組 | `track_order`，內部依序呼叫三支 API | 只要判斷使用者想追包裹'
    anchor_type: 部落格舉例
    qualifiers:
      - text: 'tool 的寫法是 blog 自編的例子'
        source_quote: 'tool 長什麼樣（自編）'
    importance: 13
    status: normal
  - id: c14
    role: mechanism
    text: '前置條件寫進 tool：如果 Y 需要 X 的輸出，就由 Y 的 tool 自己檢查，缺少時回傳一段模型能照著做的指示；硬性前置條件要盡量少，只保留真正必要的'
    source_quotes:
      - '**前置條件寫進 tool。** 如果 Y 需要 X 的輸出，就由 Y 的 tool 自己檢查，缺少時回傳一段模型能照著做的指示。硬性前置條件要盡量少，只保留真正必要的。'
    anchor_type: 設計參數
    importance: 14
    status: normal
  - id: c15
    role: anchor
    text: '退款例子：模型呼叫 refund（訂單 A），refund tool 回覆「尚未驗證身分，請先呼叫 verify_identity」；模型呼叫 verify_identity 後再呼叫 refund，tool 回覆退款已送出；規則不靠模型記得，而是由 tool 的程式碼擋下並指路'
    source_quotes:
      - 'r1["模型呼叫 refund（訂單 A）"]'
      - 'x["refund tool 回覆：尚未驗證身分，請先呼叫 verify_identity"]'
      - 'v["模型呼叫 verify_identity"]'
      - 'r2["模型再呼叫 refund（訂單 A）"]'
      - 'ok["refund tool 回覆：退款已送出"]'
      - '前置條件寫在 tool 裡：規則不靠模型記得，而是由 tool 的程式碼擋下並指路。（自編例子）'
    anchor_type: 部落格舉例
    qualifiers:
      - text: '這是 blog 自編的例子'
        source_quote: '以退款為例（自編）'
    importance: 15
    status: normal
  - id: c16
    role: mechanism
    text: '權限檢查寫進 tool：每個 tool 自己檢查呼叫者能看什麼、能做什麼，不行就回傳一句白話的拒絕；這樣同一個 loop 就能服務不同權限的使用者，不必每個權限等級各做一個 agent'
    source_quotes:
      - '**權限檢查寫進 tool。** 每個 tool 自己檢查呼叫者能看什麼、能做什麼，不行就回傳一句白話的拒絕。這樣同一個 loop 就能服務不同權限的使用者，不必每個權限等級各做一個 agent。'
    anchor_type: 設計參數
    importance: 16
    status: normal
  - id: c17
    role: mechanism
    text: '團隊貢獻的東西有三種載體：MCP tool（MCP 是 Model Context Protocol，讓 agent 透過統一介面呼叫外部工具的協定）適合要執行動作、讀即時資料，或要回傳固定格式的結果；skill 適合團隊「怎麼做事」：步驟、規則、判斷方式；知識庫適合偶爾才需要的參考資料：政策、指標定義、產品規格'
    source_quotes:
      - '團隊貢獻的東西有三種載體'
      - 'MCP 是 Model Context Protocol，讓 agent 透過統一介面呼叫外部工具的協定；一般知識'
      - 'MCP tool | 要執行動作、讀即時資料，或要回傳固定格式的結果'
      - 'Skill | 團隊「怎麼做事」：步驟、規則、判斷方式'
      - '知識庫 | 偶爾才需要的參考資料：政策、指標定義、產品規格'
    anchor_type: 設計參數
    importance: 17
    status: normal
  - id: c18
    role: mechanism
    text: '知識庫有兩種放法：放在搜尋或查詢 tool 後面，讓模型自己呼叫；或者當成參考檔案放進 skill。文章要求避免的是「由程式碼先檢索，再直接貼進 prompt」'
    source_quotes:
      - '知識庫有兩種放法：放在搜尋或查詢 tool 後面，讓模型自己呼叫；或者當成參考檔案放進 skill。文章要求避免的是「由程式碼先檢索，再直接貼進 prompt」。'
    anchor_type: 設計參數
    qualifiers:
      - text: '理由文章在這裡沒說；blog 推論是讀不讀、讀哪一段，應該交給模型按需決定'
        source_quote: '理由文章在這裡沒說，合理的解讀是：讀不讀、讀哪一段，應該交給模型按需決定（推論）。'
    importance: 18
    status: normal
```
