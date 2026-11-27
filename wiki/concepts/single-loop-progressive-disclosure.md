---
id: single-loop-progressive-disclosure
title: "當初拆 subagent 的主要理由是「所有專業知識塞進一個 prompt 會太長」；知識改成按需載入（漸進式揭露）之後，這個理由就不成立了，而單一 loop 裡寫計畫的模型就是執行計畫的模型"
type_hint: 方法
context_type: evidence_from_single_source
sources:
  - article: subagent-fold
    article_title: "該不該拆 Subagent？Anthropic 談把多 Agent 折回單一 Agent Loop"
    url: https://datasciocean.com/ai-concept/subagent-fold/
    sections:
      - 一個沒說錯、卻漏掉發票的 subagent
      - 五種失敗模式
      - 目標架構：單一 loop 加上漸進式揭露
      - 漸進式揭露：平常只放目錄，需要才載入
      - 為什麼比拆 subagent 好
      - Loop 怎麼運作：寫計畫的就是執行的
      - 多切一個 agent 之前先問一句
      - 這些主張有多扎實
      - 結論
    first_appearance: true
parent: null
related:
  - subagent-boundary-lossy-handoff
  - judgment-skill-hard-rules-tool-code
  - subagent-fold-eval-gated-migration
  - conway-law-agent-org-chart
  - claude-code-agentic-loop-and-tools
  - claude-code-extension-and-context
  - tree-routing-bounded-by-node-descriptions
  - evoontology-query-over-prompt-stuffing
  - pg-local-subgraph-vs-full-graph
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: '當初拆 subagent 的主要理由，是「所有專業知識塞進一個 prompt 會太長」；知識改成按需載入之後，這個理由就不成立了'
    source_quotes:
      - '當初拆 subagent 的主要理由，是「所有專業知識塞進一個 prompt 會太長」。知識改成按需載入之後，這個理由就不成立了。'
    anchor_type: 原作者解讀
    qualifiers:
      - text: 'blog 列的仍該保留 subagent 的情況之一，是 context 膨脹，造成可量測的退化'
        source_quote: '**context 膨脹，造成可量測的退化**。'
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
    text: '文章想要的單一 loop 是一個模型、一個 context window（模型一次能看到的全部內容，包含指令、對話紀錄與工具回傳的結果）；領域知識寫成 skills（寫給 agent 看的做事說明），能力做成 tools（agent 可以呼叫的功能，例如查訂單），兩者平常都只放一份目錄'
    source_quotes:
      - '再看文章想要的樣子：在 loop 裡反覆「呼叫工具、看結果、決定下一步」，知識和工具平常只放目錄，需要時才載入。'
      - '具體來說是一個模型、一個 [context window](../context-engineering/)（模型一次能看到的全部內容，包含指令、對話紀錄與工具回傳的結果）。領域知識寫成 skills（寫給 agent 看的做事說明），能力做成 tools（agent 可以呼叫的功能，例如查訂單），兩者平常都只放一份目錄。'
    anchor_type: 設計參數
    importance: 4
    status: normal
  - id: c5
    role: mechanism
    text: '漸進式揭露（progressive disclosure）的意思是：agent 一開始只看到每個 skill 和 tool 的名稱加一行描述，真正需要時才把全文或完整定義載入 context'
    source_quotes:
      - '漸進式揭露（progressive disclosure）的意思是：agent 一開始只看到每個 skill 和 tool 的名稱加一行描述，真正需要時才把全文或完整定義載入 context。'
    anchor_type: 設計參數
    importance: 5
    status: normal
  - id: c6
    role: mechanism
    text: '這個概念套在兩種東西上：skill 是寫給 agent 看的做事說明，包含步驟、規則與判斷方式，原本寫在各個 subagent prompt 裡的專業知識就搬到這裡；tool search 是同一個想法套用在工具上，工具定義延遲到需要時才搜尋並載入'
    source_quotes:
      - '這個概念套在兩種東西上：'
      - '**Skill**：寫給 agent 看的做事說明，包含步驟、規則與判斷方式。原本寫在各個 subagent prompt 裡的專業知識，就搬到這裡。'
      - '**Tool search**：同一個想法套用在工具上，工具定義延遲到需要時才搜尋並載入。'
    anchor_type: 設計參數
    importance: 6
    status: normal
  - id: c7
    role: anchor
    text: '客服例子：使用者問「我的訂單到哪了？」，一開始就在 context 的是 skill 目錄、tool 目錄與精簡的 system prompt；模型判斷後載入物流 skill 全文，需要時呼叫查訂單 tool，退貨 skill、發票 skill 這次沒用到，不占 context'
    source_quotes:
      - '用同一個客服例子（自編），這次使用者問「我的訂單到哪了？」：'
      - 'ctx["一開始就在 context（很短）：skill 目錄、tool 目錄、精簡的 system prompt"]'
      - 'ctx -->|模型判斷後載入| l1'
      - 'l1 -->|需要時呼叫| l2'
      - 'n1["退貨 skill、發票 skill：這次沒用到，不占 context"]'
      - 'l1["物流 skill 全文"]'
    anchor_type: 部落格舉例
    qualifiers:
      - text: '這是 blog 自編的例子'
        source_quote: '用同一個客服例子（自編）'
    importance: 7
    status: normal
  - id: c8
    role: mechanism
    text: '文章給的第一個理由是共享 context：前面每一步的原始結果都在同一個視窗裡，agent 能自己把它們串起來'
    source_quotes:
      - '文章給了三個理由：'
      - '共享 context | 前面每一步的原始結果都在同一個視窗裡，agent 能自己把它們串起來'
    anchor_type: 原作者解讀
    importance: 8
    status: normal
  - id: c9
    role: evidence
    text: '共享 context 這個理由配的證據是：多個企業部署的比較中，單一 agent 加 skills 在品質上「經常」勝過單一大 prompt 與 subagent 設計，成本與延遲也「常常」比較低'
    source_quotes:
      - '**共享 context**：多個企業部署的比較中，單一 agent 加 skills 在品質上「經常」勝過單一大 prompt 與 subagent 設計，成本與延遲也「常常」比較低。'
    anchor_type: 官方宣稱
    qualifiers:
      - text: '這份證據沒有數字、任務或模型資訊'
        source_quote: '單一 agent 加 skills 品質「經常」較好、成本延遲「常常」較低 | 多個企業部署的比較 | 沒有數字、任務或模型資訊'
    importance: 9
    status: normal
  - id: c10
    role: mechanism
    text: '第二個理由是防止 context 膨脹：知識放在按需載入的 skill，不必一次塞進 prompt'
    source_quotes:
      - '防止 context 膨脹 | 知識放在按需載入的 skill，不必一次塞進 prompt'
    anchor_type: 原作者解讀
    qualifiers:
      - text: 'blog 列的仍該保留 subagent 的情況之一，是 context 膨脹，造成可量測的退化'
        source_quote: '**context 膨脹，造成可量測的退化**。'
    importance: 10
    status: normal
  - id: c11
    role: evidence
    text: '防止 context 膨脹這個理由配的證據是：Claude Code 針對較強的模型，把 system prompt 縮減了超過 80%'
    source_quotes:
      - '**防止 context 膨脹**：[Claude Code](../claude-code/) 針對較強的模型，把 system prompt 縮減了超過 80%。'
    anchor_type: 官方宣稱
    comparison_target: 'Claude Code 縮減前的 system prompt'
    qualifiers:
      - text: '這個縮減「包含」漸進式揭露的效果，但不全是它的功勞，文章沒說其餘來自哪裡'
        source_quote: '這個縮減「包含」漸進式揭露的效果，但不全是它的功勞（文章沒說其餘來自哪裡）。'
      - text: '這是 Claude Code 自己的經驗'
        source_quote: 'Claude Code 的 system prompt 縮減超過 80% | Claude Code 自己的經驗 | 縮減「包含」漸進式揭露，不全是它的功勞'
    importance: 11
    status: normal
  - id: c12
    role: mechanism
    text: '第三個理由是模型變強了：一個 loop 能管的事變多，不需要 harness 替模型拆步驟。文章的說法是，從 Opus 4.5 起，模型能在單一 loop 裡處理的事比多數團隊預期得多'
    source_quotes:
      - '模型變強了 | 一個 loop 能管的事變多，不需要 harness 替模型拆步驟'
      - '第三個理由，文章的說法是：從 Opus 4.5 起，模型能在單一 loop 裡處理的事比多數團隊預期得多。'
    anchor_type: 原作者解讀
    numeric_kind: non_comparative
    numeric_reason: 名稱
    qualifiers:
      - text: '「模型夠強就能折」只是從 Opus 4.5 起的觀察，沒有跨模型比較，也沒有「多強才夠」的門檻'
        source_quote: '模型夠強就能折 | 從 Opus 4.5 起的觀察 | 沒有跨模型比較，也沒有「多強才夠」的門檻'
    importance: 12
    status: normal
  - id: c13
    role: mechanism
    text: '近期的模型會邊做邊交代進度、檢查自己的結果，讓部分 harness 設計變得多餘；過於死板的多 agent 結構，反而常常是新模型發揮不出來的原因'
    source_quotes:
      - '近期的模型會邊做邊交代進度、檢查自己的結果，讓部分 harness 設計變得多餘。每出一代新模型，就能把更多決策從 harness 移到模型身上；過於死板的多 agent 結構，反而常常是新模型發揮不出來的原因。'
    anchor_type: 原作者解讀
    qualifiers:
      - text: '這個「模型夠強就能折」的說法沒有跨模型比較，也沒有「多強才夠」的門檻'
        source_quote: '模型夠強就能折 | 從 Opus 4.5 起的觀察 | 沒有跨模型比較，也沒有「多強才夠」的門檻'
    importance: 13
    status: normal
  - id: c14
    role: mechanism
    text: '模型要多強才能折，文章沒有給門檻，而是用症狀和 eval（一組固定的測試題，用來替 agent 打分）取代門檻：折疊後分數比較差才保留 subagent，再搭配三個保留條件判斷：context 膨脹、需要平行乾淨的 context、選錯工具或指令衝突'
    source_quotes:
      - '那模型要多強才能折？文章沒有給門檻，而是用症狀和 eval 取代門檻：折疊後分數比較差才保留 subagent，再搭配開頭提到的三個保留條件判斷（context 膨脹、需要平行乾淨的 context、選錯工具或指令衝突'
      - '表中的 eval 是一組固定的測試題，用來替 agent 打分'
    anchor_type: 設計參數
    importance: 14
    status: normal
  - id: c15
    role: evaluation
    text: 'blog 推論，較弱的模型會更早出現這些症狀，流程依然適用，只是能折進去的 subagent 比較少'
    source_quotes:
      - '較弱的模型會更早出現這些症狀，流程依然適用，只是能折進去的 subagent 比較少（推論）。'
    anchor_type: 部落格推論
    importance: 15
    status: normal
  - id: c16
    role: mechanism
    text: '單一 loop 裡，決策都由模型做，harness（包在模型外面的程式）只負責執行工具與設上限：模型寫計畫、輸出一批 tool calls，harness 平行執行、原始結果直接回傳，上限包括回合預算、成本預算、寫入閘門'
    source_quotes:
      - '這裡的 [harness](../harness-engineering/) 指包在模型外面的程式；決策都由模型做，harness 只負責執行工具與設上限：'
      - 't["模型輸出一批 tool calls"]'
      - 'h["harness 平行執行，原始結果直接回傳"]'
      - 'b["harness 上限：回合預算、成本預算、寫入閘門；超出預算也會停"]'
      - 'p["模型寫計畫（寫在 context，可隨時改）"]'
    anchor_type: 設計參數
    qualifiers:
      - text: '寫入閘門（write gate）文章沒有定義，blog 推論可以理解成修改資料前的檢查或核准'
        source_quote: '圖中的寫入閘門（write gate）文章沒有定義，可以理解成修改資料前的檢查或核准（推論）。'
    importance: 16
    status: normal
  - id: c17
    role: mechanism
    text: '和 orchestrator 架構最大的差別是：寫計畫的模型，就是執行計畫的模型。orchestrator 架構裡，planner 寫好計畫交給 specialist（負責單一領域的 subagent）執行，中途發現不對很難改；單一 loop 裡，模型每看到一批新結果，就能當場修改計畫'
    source_quotes:
      - '和 orchestrator 架構最大的差別是：寫計畫的模型，就是執行計畫的模型。在 orchestrator 架構裡，planner 寫好計畫交給 specialist（負責單一領域的 subagent）執行，中途發現不對很難改；在單一 loop 裡，模型每看到一批新結果，就能當場修改計畫。'
    anchor_type: 原作者解讀
    importance: 17
    status: normal
```
