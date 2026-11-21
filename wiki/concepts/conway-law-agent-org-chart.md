---
id: conway-law-agent-org-chart
title: "多切一個 agent 之前先問：「如果整個系統只由一個團隊負責，這條邊界還會存在嗎？」不會存在，這條邊界只是組織圖的投影（Conway's law），應該改掉；而要改的往往是組織，不只是架構"
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
  - article: subagent-fold
    article_title: "該不該拆 Subagent？Anthropic 談把多 Agent 折回單一 Agent Loop"
    url: https://datasciocean.com/ai-concept/subagent-fold/
    sections:
      - 一個沒說錯、卻漏掉發票的 subagent
      - 五種失敗模式
      - 目標架構：單一 loop 加上漸進式揭露
      - 沒有各自的 agent 之後，團隊要負責什麼
      - Skills 怎麼維護、不氾濫
      - 值得帶走的觀念：Conway's law
      - 這個定律從哪來、為什麼成立
      - 放到 agent 上為什麼特別傷
      - 多切一個 agent 之前先問一句
      - 要改的往往是組織，不只是架構
    first_appearance: true
parent: null
related:
  - subagent-boundary-lossy-handoff
  - single-loop-progressive-disclosure
  - judgment-skill-hard-rules-tool-code
  - subagent-fold-eval-gated-migration
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: '多切一個 agent 之前，先問：「如果整個系統只由一個團隊負責，這條邊界還會存在嗎？」會存在，代表有技術理由，這種邊界可以留；不會存在，這條邊界只是組織圖的投影，應該改掉'
    source_quotes:
      - '「如果整個系統只由一個團隊負責，這條邊界還會存在嗎？」'
      - '**會存在**：代表有技術理由，例如可量測的 context 膨脹、需要平行且乾淨的 context、工具太多選不準。這種邊界可以留。'
      - '**不會存在**：這條邊界只是組織圖的投影，應該改掉。'
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
    text: 'Anthropic 最近一篇文章主張，這種架構很多時候可以折回單一 agent loop；核心理由是每一條 subagent 邊界都是一次有損的 context（模型當下看得到的全部資訊）交接，而這些邊界常常只是組織圖的投影，不是技術上非切不可'
    source_quotes:
      - 'Anthropic 最近一篇文章主張，這種架構很多時候可以折回單一 agent loop。'
      - '核心理由是：每一條 subagent 邊界都是一次有損的 context（模型當下看得到的全部資訊）交接，而這些邊界常常只是組織圖的投影，不是技術上非切不可。'
    anchor_type: 原作者解讀
    qualifiers:
      - text: '不是全部都要折：文章列了三種仍該保留 subagent 的情況'
        source_quote: '當然也不是全部都要折。文章列了三種仍該保留 subagent 的情況'
    importance: 3
    status: normal
  - id: c4
    role: context
    text: "Conway's law 說：設計系統的組織，做出來的系統結構會複製組織自己的溝通結構"
    source_quotes:
      - "Conway's law 說：設計系統的組織，做出來的系統結構會複製組織自己的溝通結構。"
    anchor_type: 背景說明
    importance: 4
    status: normal
  - id: c5
    role: context
    text: "Conway's law 由 Melvin Conway 在 1968 年提出，屬於軟體工程與組織設計領域，在討論微服務該怎麼切分時很常見，在 AI agent 領域則還少見"
    source_quotes:
      - "Conway's law 由 Melvin Conway 在 1968 年提出，屬於軟體工程與組織設計領域，在討論微服務該怎麼切分時很常見，在 AI agent 領域則還少見（一般知識）。"
    anchor_type: 背景說明
    numeric_kind: non_comparative
    numeric_reason: 日期
    importance: 5
    status: normal
  - id: c6
    role: mechanism
    text: "Agent 架構變成組織圖的複製品，就是 Conway's law 在 agent 上的表現；blog 認為文章是把它當成真正的診斷工具在用，不是借個名詞來裝飾"
    source_quotes:
      - 'Agent 架構變成組織圖的複製品，就是這個定律在 agent 上的表現。'
      - '文章是把它當成真正的診斷工具在用，不是借個名詞來裝飾。'
    anchor_type: 部落格判斷
    importance: 6
    status: normal
  - id: c7
    role: mechanism
    text: 'blog 把這個定律為什麼成立拆成三步：每個團隊只能輕鬆修改自己擁有的部分；跨團隊的介面要協調，成本很高，所以系統邊界自然落在團隊邊界上；每個團隊只為自己那一塊負責，也就只為那一塊優化，例如寫只測自己子任務的 eval'
    source_quotes:
      - '它為什麼成立，可以拆成三步（一般知識加推論）：'
      - '每個團隊只能輕鬆修改自己擁有的部分。'
      - '跨團隊的介面要協調，成本很高，所以系統邊界自然落在團隊邊界上。'
      - '每個團隊只為自己那一塊負責，也就只為那一塊優化，例如寫只測自己子任務的 eval（也就是前面五種失敗模式裡的「Eval 過度局部」）。'
    anchor_type: 部落格推論
    qualifiers:
      - text: '這三步是一般知識加 blog 的推論；blog 的小結稱之為「一個合理的解釋」'
        source_quote: '小結：一個合理的解釋是，團隊只改得動、也只優化自己那一塊，agent 就跟著長成組織圖'
    importance: 7
    status: normal
  - id: c8
    role: mechanism
    text: '結果是：系統邊界依「誰負責什麼」劃分，而不是依技術需求劃分'
    source_quotes:
      - '結果是：系統邊界依「誰負責什麼」劃分，而不是依技術需求劃分。'
    anchor_type: 部落格推論
    qualifiers:
      - text: '這是 blog 以一般知識加推論拆出的三步得出的結果'
        source_quote: '它為什麼成立，可以拆成三步（一般知識加推論）：'
    importance: 8
    status: normal
  - id: c9
    role: mechanism
    text: '放到 agent 上特別傷：一般軟體的團隊邊界會變成 API 邊界，資料還能完整傳過去；Agent 的邊界卻是 context 的邊界，每一條團隊邊界都變成一次有損的摘要交接'
    source_quotes:
      - '一般軟體的團隊邊界會變成 API 邊界，資料還能完整傳過去。Agent 的邊界卻是 context 的邊界，每一條團隊邊界都變成一次有損的摘要交接'
      - '文中標（推論）的是筆者在文章之外的推斷，標（自編）的是為了說明而設計的情境，標（一般知識）的是業界通用的背景知識；沒有標的都是文章內容。'
    anchor_type: 原作者解讀
    importance: 9
    status: normal
  - id: c10
    role: anchor
    text: '文章的例子：一家公司的客服 agent 底下有十幾個 specialist subagent，品牌語氣難以保持一致，延遲也傷害了使用者體驗'
    source_quotes:
      - '文章的例子：一家公司的客服 agent 底下有十幾個 specialist subagent，品牌語氣難以保持一致，延遲也傷害了使用者體驗。'
    anchor_type: 官方宣稱
    importance: 10
    status: normal
  - id: c11
    role: mechanism
    text: '文章列了三種仍該保留 subagent 的情況：context 膨脹，造成可量測的退化；需要平行執行、而且各自乾淨的 context；agent 選不對工具，或指令互相衝突'
    source_quotes:
      - '開頭提過，文章列了三種仍該保留 subagent 的情況。'
      - '**context 膨脹，造成可量測的退化**。'
      - '**需要平行執行、而且各自乾淨的 context**。'
      - '**agent 選不對工具，或指令互相衝突**。'
    anchor_type: 原作者解讀
    importance: 11
    status: normal
  - id: c12
    role: anchor
    text: '需要平行且乾淨 context 的例子：同時調查幾個互不相關的方向，每個方向都要讀大量文件；混在同一個 context 裡會互相干擾，分給幾個 subagent 各自讀、各自回報比較合適'
    source_quotes:
      - '同時調查幾個互不相關的方向，每個方向都要讀大量文件；混在同一個 context 裡會互相干擾，分給幾個 subagent 各自讀、各自回報比較合適。'
    anchor_type: 部落格舉例
    qualifiers:
      - text: '這是 blog 自編的例子'
        source_quote: '用例子說明（例子皆為自編）'
    importance: 12
    status: normal
  - id: c13
    role: mechanism
    text: '折成一個之後，各團隊不再擁有一個 agent，而是貢獻 skills（寫給 agent 看的做事說明）、tools（agent 可以呼叫的功能）或知識庫'
    source_quotes:
      - '各團隊不再擁有一個 agent，而是貢獻 skills、tools 或知識庫。'
      - '領域知識寫成 skills（寫給 agent 看的做事說明），能力做成 tools（agent 可以呼叫的功能，例如查訂單）'
    anchor_type: 原作者解讀
    importance: 13
    status: normal
  - id: c14
    role: mechanism
    text: '一個小型中央團隊擁有 system prompt 與端到端品質，每個新的 skill、tool、eval 上線前都要經過它審核；中央團隊要刻意保持小，迭代才快，協調成本才低'
    source_quotes:
      - '一個小型中央團隊擁有 system prompt 與端到端品質，每個新的 skill、tool、eval 上線前都要經過它審核。中央團隊要刻意保持小，迭代才快，協調成本才低。'
    anchor_type: 原作者解讀
    importance: 14
    status: normal
  - id: c15
    role: mechanism
    text: '文章不是叫團隊消失，而是改變團隊擁有的單位；組織邊界換了，系統邊界才不會被慢慢拉回原狀'
    source_quotes:
      - '文章不是叫團隊消失，而是改變團隊擁有的單位'
      - '它在這裡多補了一層理由：組織邊界換了，系統邊界才不會被慢慢拉回原狀。'
    anchor_type: 原作者解讀
    importance: 15
    status: normal
  - id: c16
    role: evaluation
    text: 'Subagent 拆掉之後，「氾濫」這個問題很可能換成 skill 的形式重演'
    source_quotes:
      - 'Subagent 拆掉之後，「氾濫」這個問題很可能換成 skill 的形式重演。'
    anchor_type: 部落格判斷
    importance: 16
    status: normal
  - id: c17
    role: mechanism
    text: '文章防止 skill 氾濫的做法：每個團隊指定一位 DRI（Directly Responsible Individual，直接負責人）負責自己的 skill，確保寫得好、不和其他 skill 重疊，並附上 eval；維護責任交還給寫 skill 的人，粗重的工作則交給 Claude，用專門的 skill 去建立、測試、刪減其他 skill；依使用量與成本資料決定去留，沒人用的 skill 就刪掉'
    source_quotes:
      - 'Subagent 拆掉之後，「氾濫」這個問題很可能換成 skill 的形式重演。文章的做法：'
      - '每個團隊指定一位 DRI（Directly Responsible Individual，直接負責人，來自管理領域的用語）負責自己的 skill，確保寫得好、不和其他 skill 重疊，並附上 eval。'
      - '維護責任交還給寫 skill 的人，粗重的工作則交給 Claude：用專門的 skill 去建立、測試、刪減其他 skill。'
      - '依使用量與成本資料決定去留，沒人用的 skill 就刪掉。'
    anchor_type: 設計參數
    importance: 17
    status: normal
```
