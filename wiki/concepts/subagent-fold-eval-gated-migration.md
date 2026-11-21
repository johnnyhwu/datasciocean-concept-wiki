---
id: subagent-fold-eval-gated-migration
title: "把 subagent 折回單一 loop，原則是一次只改一件事、每一步都用 eval 確認沒有退步；要不要折由分數決定，而且要逐題看翻轉、每題多跑幾次，不能只看總分"
type_hint: 方法
context_type: evidence_from_single_source
sources:
  - article: subagent-fold
    article_title: "該不該拆 Subagent？Anthropic 談把多 Agent 折回單一 Agent Loop"
    url: https://datasciocean.com/ai-concept/subagent-fold/
    sections:
      - 一個沒說錯、卻漏掉發票的 subagent
      - 五種失敗模式
      - 怎麼折：用 eval 把關的分階段遷移
      - 先建 eval
      - Loop 怎麼運作：寫計畫的就是執行的
      - 三種做法，依序進行
      - 總分一樣，也可能藏著退步
      - 多切一個 agent 之前先問一句
      - 這些主張有多扎實
      - 量什麼
      - 題目要涵蓋什麼
      - 怎麼比
      - 怎麼判斷要留 subagent
      - 誰維護 eval
    first_appearance: true
parent: null
related:
  - subagent-boundary-lossy-handoff
  - single-loop-progressive-disclosure
  - judgment-skill-hard-rules-tool-code
  - conway-law-agent-org-chart
  - skillopt-blind-acceptance-gate
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: '遷移的原則是一次只改一件事，每一步都用 eval 確認沒有退步；要不要折，由分數決定，不由直覺決定'
    source_quotes:
      - '遷移的原則是一次只改一件事，每一步都用 eval 確認沒有退步。要不要折，由分數決定，不由直覺決定。'
    anchor_type: 原作者解讀
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
    text: 'Anthropic 最近一篇文章主張，這種架構很多時候可以折回單一 agent loop；eval 是一組固定的測試題，用來替 agent 打分'
    source_quotes:
      - 'Anthropic 最近一篇文章主張，這種架構很多時候可以折回單一 agent loop。'
      - '表中的 eval 是一組固定的測試題，用來替 agent 打分'
    anchor_type: 原作者解讀
    qualifiers:
      - text: '不是全部都要折：文章列了三種仍該保留 subagent 的情況'
        source_quote: '當然也不是全部都要折。文章列了三種仍該保留 subagent 的情況'
    importance: 3
    status: normal
  - id: c4
    role: mechanism
    text: 'Eval 分兩層：中央團隊維護一套端到端 eval，各團隊上線 skill 時，附上只測該 skill 的小 eval；起步用 10 個 golden examples（人工確認過正確答案的範例）就夠了'
    source_quotes:
      - 'Eval 分兩層：中央團隊維護一套端到端 eval，各團隊上線 skill 時，附上只測該 skill 的小 eval。起步用 10 個 golden examples（人工確認過正確答案的範例）就夠了。'
    anchor_type: 設計參數
    numeric_kind: non_comparative
    numeric_reason: 計數
    importance: 4
    status: normal
  - id: c5
    role: mechanism
    text: '做法 A，把 subagent 當 tool 呼叫：主 agent 把 subagent 當成一個工具呼叫，自己持續握著和使用者的對話；好處是不必改寫 subagent，就能先拿到 baseline，也可以統一各 subagent 的回應格式，讓主 agent 拿真實資料去核對 subagent 的結論。只有在 subagent 必須親自和使用者對話時，才讓它直接接手整段對話（full handoff）'
    source_quotes:
      - '**A. 把 subagent 當 tool 呼叫。** 主 agent 把 subagent 當成一個工具呼叫，自己持續握著和使用者的對話。好處是不必改寫 subagent，就能先拿到 baseline（之後每一步拿來比較的基準分數）；同時可以統一各 subagent 的回應格式，讓主 agent 拿真實資料去核對 subagent 的結論。只有在 subagent 必須親自和使用者對話時，才讓它直接接手整段對話（full handoff）。'
    anchor_type: 設計參數
    importance: 5
    status: normal
  - id: c6
    role: evaluation
    text: '做法 A 還沒解決的事：每個 specialist 仍有自己的 prompt、owner 與 eval；回傳的仍然是有損摘要；每次呼叫都是多一層巢狀 loop，延遲還在'
    source_quotes:
      - '每個 specialist 仍有自己的 prompt、owner 與 eval；回傳的仍然是有損摘要；每次呼叫都是多一層巢狀 loop，延遲還在。'
    anchor_type: 原作者解讀
    importance: 6
    status: normal
  - id: c7
    role: mechanism
    text: '做法 B，合併 domain agents：從使用量最大的開始，把會串接彼此輸出、碰同一份資料、常被一起呼叫的 specialist（負責單一領域的 subagent）合併；看生產流量，如果很大一部分流量是「specialist 1 做完，接著叫 specialist 2」，這兩個就是緊密耦合的一對'
    source_quotes:
      - '**B. 合併 domain agents。** 從使用量最大的開始，把會串接彼此輸出、碰同一份資料、常被一起呼叫的 specialist 合併。怎麼找出這種組合？看生產流量：如果很大一部分流量是「specialist 1 做完，接著叫 specialist 2」，這兩個就是緊密耦合的一對。'
      - 'specialist（負責單一領域的 subagent）'
    anchor_type: 設計參數
    numeric_kind: non_comparative
    numeric_reason: 名稱
    importance: 7
    status: normal
  - id: c8
    role: mechanism
    text: '做法 C，折成 skills 加 tools：一次一個，subagent 的 prompt 改寫成 skill，它呼叫的 API 改成 MCP tool（MCP 是 Model Context Protocol，讓 agent 透過統一介面呼叫外部工具的協定）；有和沒有這個 subagent 分別跑一輪 eval，再決定去留'
    source_quotes:
      - '**C. 折成 skills 加 tools。** 一次一個：subagent 的 prompt 改寫成 skill，它呼叫的 API 改成 MCP tool（MCP 是 Model Context Protocol，讓 agent 透過統一介面呼叫外部工具的協定；一般知識）。有和沒有這個 subagent 分別跑一輪 eval，再決定去留。'
    anchor_type: 設計參數
    importance: 8
    status: normal
  - id: c9
    role: evaluation
    text: 'blog 把 A、B、C 三種做法讀成依序進行的階段，這是推論：文章原話是可以「合併、當 tool 呼叫，或用 skills 和 tools 取代」，沒有明說是三選一還是依序；依據是文章稱 A 為好的第一步，而且那一節講的就是分階段遷移'
    source_quotes:
      - '這裡把它們讀成依序進行的階段（推論；文章沒有明說，依據見本節最後的摺疊區）'
      - '文章原話是可以「合併、當 tool 呼叫，或用 skills 和 tools 取代」，沒有明說三者是三選一的選項，還是依序進行的階段。採分階段讀法的依據是：文章稱 A 為好的第一步，而且那一節講的就是分階段遷移。'
    anchor_type: 部落格推論
    importance: 9
    status: normal
  - id: c10
    role: mechanism
    text: '判斷要不要留 subagent 的主規則：折疊版分數比較差，才保留 subagent'
    source_quotes:
      - '**主規則**：折疊版分數比較差，才保留 subagent。'
    anchor_type: 設計參數
    qualifiers:
      - text: 'blog 推論，三種保留情況裡的「需要平行且乾淨的 context」是架構需求，不是 eval 分數能反映的，要另外判斷'
        source_quote: '**另外判斷的一項**：需要平行且乾淨的 context 是架構需求，不是 eval 分數能反映的，要另外判斷（推論；文章只是把它和另外兩個條件並列）。'
    importance: 10
    status: normal
  - id: c11
    role: mechanism
    text: '文章列了三種仍該保留 subagent 的情況：context 膨脹造成可量測的退化；需要平行執行、而且各自乾淨的 context；agent 選不對工具，或指令互相衝突'
    source_quotes:
      - '文章列了三種仍該保留 subagent 的情況'
      - '**context 膨脹，造成可量測的退化**。'
      - '**需要平行執行、而且各自乾淨的 context**。'
      - '**agent 選不對工具，或指令互相衝突**。'
    anchor_type: 原作者解讀
    importance: 11
    status: normal
  - id: c12
    role: evaluation
    text: 'blog 推論：context 膨脹、選不對工具、指令互相衝突都能從 eval 指標看出來，但需要平行且乾淨的 context 是架構需求，不是 eval 分數能反映的，要另外判斷'
    source_quotes:
      - '**輔助訊號**：context 膨脹造成可量測的退化、選不對工具、prompt 指令互相衝突，這三者都能從〈量什麼〉的指標看出來。'
      - '**另外判斷的一項**：需要平行且乾淨的 context 是架構需求，不是 eval 分數能反映的，要另外判斷（推論；文章只是把它和另外兩個條件並列）。'
    anchor_type: 部落格推論
    importance: 12
    status: normal
  - id: c13
    role: mechanism
    text: '折疊後不能只看總分，要逐題比對：哪些任務從通過變失敗，哪些從失敗變通過'
    source_quotes:
      - '折疊後不能只看總分，要逐題比對，哪些任務從通過變失敗，哪些從失敗變通過。'
    anchor_type: 原作者解讀
    importance: 13
    status: normal
  - id: c14
    role: anchor
    text: '假設 eval 共 20 題，折疊前後的通過題數一樣是 15 題，但題號 3、7 從通過變失敗，題號 11、18 從失敗變通過；如果題號 3、7 是絕對不能錯的流程，總分就把退步藏起來了'
    source_quotes:
      - '假設 eval 共 20 題（自編）'
      - '通過題數（共 20 題） | 15 | 15'
      - '題號 3、7 | 通過 | 失敗'
      - '題號 11、18 | 失敗 | 通過'
      - '總分一樣是 15 題，但如果題號 3、7 這兩題是絕對不能錯的流程，總分就把退步藏起來了。'
    anchor_type: 部落格舉例
    numeric_kind: non_comparative
    numeric_reason: 假設題設
    qualifiers:
      - text: '這是 blog 自編的假設'
        source_quote: '假設 eval 共 20 題（自編）'
    importance: 14
    status: normal
  - id: c15
    role: anchor
    text: '文章給了一個實例：一個示範用的客服 agent，把一個 subagent 折進另一個之後，延遲下降了，但一個原本通過的流程壞掉：主 agent 手上已經有查訂單的 tool，就自己回答了，沒有去問物流 specialist 實際的送達日期'
    source_quotes:
      - '文章給了一個實例。一個示範用的客服 agent，把一個 subagent 折進另一個之後，延遲下降了，但一個原本通過的流程壞掉：主 agent 手上已經有查訂單的 tool，就自己回答了，沒有去問物流 specialist 實際的送達日期。'
    anchor_type: 官方宣稱
    importance: 15
    status: normal
  - id: c16
    role: anchor
    text: '這個失誤在兩次執行中只出現一次，只跑一次很可能根本抓不到'
    source_quotes:
      - '而且這個失誤在兩次執行中只出現一次，只跑一次很可能根本抓不到。'
    anchor_type: 官方宣稱
    qualifiers:
      - text: '這是一個示範用的客服 agent 的實例'
        source_quote: '一個示範用的客服 agent，把一個 subagent 折進另一個之後'
    importance: 16
    status: normal
  - id: c17
    role: mechanism
    text: '教訓：模型手上的資訊「看起來夠用」時，會跳過原本設計好的步驟；所以每題要多跑幾次，而且每一條會一起執行的串接都要有題目'
    source_quotes:
      - '模型手上的資訊「看起來夠用」時，會跳過原本設計好的步驟。所以每題要多跑幾次，而且每一條會一起執行的串接都要有題目'
    anchor_type: 原作者解讀
    qualifiers:
      - text: '每題要跑幾次才夠，文章沒說'
        source_quote: '**每題要跑幾次才夠**，文章沒說。'
    importance: 17
    status: normal
  - id: c18
    role: mechanism
    text: '題目除了涵蓋生產環境中每一條會一起執行的 agent 串接，agent 絕對不能違反的每一條規則，也都要有對應的題目'
    source_quotes:
      - '生產環境中每一條會一起執行的 agent 串接都要有題目。'
      - 'Agent 絕對不能違反的每一條規則，都要有對應的題目。'
    anchor_type: 設計參數
    importance: 18
    status: normal
  - id: c19
    role: mechanism
    text: '要量的指標：結果面看 rubric 評分（依評分標準給最終回覆打分）與 task-completion（任務完成率，比較架構時最重要）；過程面折疊前看 routing accuracy（路由準確率），折疊後看有沒有載入對的 skill、呼叫對的 tool 的選擇正確率，以及用串接題目看該走的步驟有沒有走完；效率面看每任務延遲、每任務成本'
    source_quotes:
      - '結果 | 最後的回覆好不好 | Rubric 評分：依評分標準給最終回覆打分 | 全程'
      - '結果 | 事情有沒有真的辦成 | Task-completion（任務完成率） | 比較架構時最重要'
      - '過程 | 有沒有分派給對的 subagent | Routing accuracy（路由準確率） | 折疊前'
      - '過程 | 有沒有載入對的 skill、呼叫對的 tool | 選擇正確率 | 折疊後'
      - '過程 | 該走的步驟有沒有走完 | 串接題目（見下一小節） | 折疊後'
      - '效率 | 有沒有變快、變便宜 | 每任務延遲、每任務成本 | 全程'
    anchor_type: 設計參數
    qualifiers:
      - text: 'Rubric 和 task-completion 的差別文章沒有明確定義'
        source_quote: 'Rubric 和 task-completion 的差別文章沒有明確定義。'
    importance: 19
    status: normal
  - id: c20
    role: mechanism
    text: '內部系統難以重播、使用者互動難以模擬時，可以在重要事件上記錄時間戳，之後拿來重播成針對性的 eval'
    source_quotes:
      - '內部系統難以重播、使用者互動難以模擬時，可以在重要事件上記錄時間戳，之後拿來重播成針對性的 eval。'
    anchor_type: 設計參數
    qualifiers:
      - text: '文章沒說明怎麼用時間戳重播成 eval'
        source_quote: '**怎麼用時間戳重播成 eval**：文章建議內部系統難以重播時，在重要事件上記錄時間戳，之後重播成 eval（文末〈誰維護 eval〉），但沒說明怎麼做'
    importance: 20
    status: normal
```
