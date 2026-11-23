---
id: subagent-boundary-lossy-handoff
title: "多 subagent 架構的毛病很多，但最根本的是每次交接都經過一份別人寫的摘要，被省略的細節就此消失"
type_hint: 判斷
context_type: evidence_from_single_source
sources:
  - article: subagent-fold
    article_title: "該不該拆 Subagent？Anthropic 談把多 Agent 折回單一 Agent Loop"
    url: https://datasciocean.com/ai-concept/subagent-fold/
    sections:
      - 一個沒說錯、卻漏掉發票的 subagent
      - 五種失敗模式
      - 最根本的問題：每次交接都是一次有損摘要
      - 放到 agent 上為什麼特別傷
      - 這些主張有多扎實
      - 結論
    first_appearance: true
parent: null
related:
  - single-loop-progressive-disclosure
  - judgment-skill-hard-rules-tool-code
  - subagent-fold-eval-gated-migration
  - conway-law-agent-org-chart
  - claude-code-extension-and-context
  - discard-history-relevance-at-the-time
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: '多 subagent 架構的毛病很多，但最根本的是每次交接都經過一份別人寫的摘要，被省略的細節就此消失'
    source_quotes:
      - '小結：多 subagent 架構的毛病很多，但最根本的是每次交接都經過一份別人寫的摘要，被省略的細節就此消失。'
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
    role: mechanism
    text: '文章的核心理由是：每一條 subagent 邊界都是一次有損的 context（模型當下看得到的全部資訊）交接，而這些邊界常常只是組織圖的投影，不是技術上非切不可'
    source_quotes:
      - '核心理由是：每一條 subagent 邊界都是一次有損的 context（模型當下看得到的全部資訊）交接，而這些邊界常常只是組織圖的投影，不是技術上非切不可。'
    anchor_type: 原作者解讀
    importance: 4
    status: normal
  - id: c5
    role: mechanism
    text: 'Subagent 做完事，回傳給主 agent 的是它自己寫的摘要，不是原始資料；摘要省略了什麼，主 agent 完全看不到'
    source_quotes:
      - 'Subagent 做完事，回傳給主 agent 的是它自己寫的摘要，不是原始資料；摘要省略了什麼，主 agent 完全看不到。'
    anchor_type: 原作者解讀
    importance: 5
    status: normal
  - id: c6
    role: anchor
    text: '客人問客服 agent：「這筆訂單能不能退？發票怎麼處理？」系統把問題轉給專管退貨的小 agent，它讀完訂單原文，回報一句「可退貨」，這句話完全正確'
    source_quotes:
      - '客人問客服 agent：「這筆訂單能不能退？發票怎麼處理？」系統把問題轉給專管退貨的小 agent。它讀完訂單原文，回報一句「可退貨」，這句話完全正確。'
    anchor_type: 部落格舉例
    qualifiers:
      - text: '這是 blog 為了說明而設計的情境'
        source_quote: '這是為了說明而設計的情境，後面會一直用到它。'
    importance: 6
    status: normal
  - id: c7
    role: anchor
    text: '可是這張訂單的發票已經開立、要先作廢；發票不在退貨 agent 的任務範圍，所以沒寫進回報，負責回答客人的那個 agent 永遠不會知道。沒有人做錯事，資訊卻在交接時掉了'
    source_quotes:
      - '可是這張訂單的發票已經開立、要先作廢；發票不在它的任務範圍，所以沒寫進回報，負責回答客人的那個 agent 永遠不會知道。沒有人做錯事，資訊卻在交接時掉了。'
    anchor_type: 部落格舉例
    qualifiers:
      - text: '這是 blog 為了說明而設計的情境'
        source_quote: '這是為了說明而設計的情境，後面會一直用到它。'
    importance: 7
    status: normal
  - id: c8
    role: anchor
    text: '同一個問題換成單一 loop：主 agent 自己讀訂單原文，看得見發票狀態，回答時一併處理作廢；拆成 subagent 時，主 agent 只拿到「可退貨」這份摘要，不知道發票已開立、需先作廢'
    source_quotes:
      - '誰讀訂單原文 | 退貨 agent 讀完訂單原文 | 主 agent 自己讀訂單原文'
      - '主 agent 拿到什麼 | 只有摘要：可退貨 | 原文，看得見發票狀態'
      - '結果 | 主 agent 不知道發票已開立、需先作廢 | 回答時一併處理作廢'
    anchor_type: 部落格舉例
    qualifiers:
      - text: '這是 blog 自編的例子'
        source_quote: '回到開頭的例子（自編）。'
    importance: 8
    status: normal
  - id: c9
    role: mechanism
    text: '文章列了多 subagent 架構的五種失敗模式，其中「Context 管理」是：要決定 agent 之間交換哪些資訊，來回傳遞時細節會掉；blog 說五項裡最根本的是這一項'
    source_quotes:
      - '文章列了五種失敗模式'
      - 'Context 管理 | 要決定 agent 之間交換哪些資訊，來回傳遞時細節會掉'
      - '五項裡最根本的是第一項。'
    anchor_type: 部落格判斷
    importance: 9
    status: normal
  - id: c10
    role: mechanism
    text: '失敗模式「Subagent 氾濫」：每個團隊各出一個，最後有大量功能重疊、沒有標準、沒有負責人的 subagent'
    source_quotes:
      - 'Subagent 氾濫 | 每個團隊各出一個，最後有大量功能重疊、沒有標準、沒有負責人的 subagent'
    anchor_type: 原作者解讀
    importance: 10
    status: normal
  - id: c11
    role: mechanism
    text: '失敗模式「Frankenprompt」：每個團隊往 system prompt 加一句，規則互相衝突，語氣也不一致'
    source_quotes:
      - 'Frankenprompt | 每個團隊往 system prompt 加一句，規則互相衝突，語氣也不一致'
    anchor_type: 原作者解讀
    importance: 11
    status: normal
  - id: c12
    role: mechanism
    text: '失敗模式「Eval 過度局部」（eval 是一組固定的測試題，用來替 agent 打分）：各團隊只為自己的子任務調分數，沒人維護整體，決策依據是被稀釋過的分數'
    source_quotes:
      - '表中的 eval 是一組固定的測試題，用來替 agent 打分'
      - 'Eval 過度局部 | 各團隊只為自己的子任務調分數，沒人維護整體，決策依據是被稀釋過的分數'
    anchor_type: 原作者解讀
    importance: 12
    status: normal
  - id: c13
    role: evidence
    text: '失敗模式「延遲」：多層架構本身就拉長時間；有個客戶把多 agent harness（包在模型外面、負責執行工具與設上限的程式）換成單一 loop，執行時間約快 2 倍'
    source_quotes:
      - '延遲 | 多層架構本身就拉長時間。有個客戶把多 agent harness（包在模型外面、負責執行工具與設上限的程式）換成單一 loop，執行時間約快 2 倍'
    anchor_type: 官方宣稱
    comparison_target: '該客戶原本的多 agent harness'
    qualifiers:
      - text: '這是單一案例，比較條件沒說明'
        source_quote: '單一 loop 執行時間約快 2 倍 | 一個客戶的案例 | 單一案例，比較條件沒說明'
      - text: 'blog 提醒，拿「快 2 倍」去說服別人之前，記得它是單一案例'
        source_quote: '**存疑**：拿「快 2 倍」「縮減超過 80%」去說服別人之前，記得它們是單一案例和自家經驗。'
    importance: 13
    status: normal
  - id: c14
    role: mechanism
    text: '一般軟體的團隊邊界會變成 API 邊界，資料還能完整傳過去；Agent 的邊界卻是 context 的邊界，每一條團隊邊界都變成一次有損的摘要交接'
    source_quotes:
      - '一般軟體的團隊邊界會變成 API 邊界，資料還能完整傳過去。Agent 的邊界卻是 context 的邊界，每一條團隊邊界都變成一次有損的摘要交接'
      - '文中標（推論）的是筆者在文章之外的推斷，標（自編）的是為了說明而設計的情境，標（一般知識）的是業界通用的背景知識；沒有標的都是文章內容。'
    anchor_type: 原作者解讀
    importance: 14
    status: normal
  - id: c15
    role: anchor
    text: '文章的例子：一家公司的客服 agent 底下有十幾個 specialist subagent，品牌語氣難以保持一致，延遲也傷害了使用者體驗'
    source_quotes:
      - '文章的例子：一家公司的客服 agent 底下有十幾個 specialist subagent，品牌語氣難以保持一致，延遲也傷害了使用者體驗。'
    anchor_type: 官方宣稱
    importance: 15
    status: normal
```
