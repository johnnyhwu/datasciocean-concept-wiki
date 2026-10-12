---
id: claude-code-extension-and-context
title: "Skills、Hooks、MCP 擴充能力又不膨脹基礎 context，CLAUDE.md、compaction、Subagent 管理 context：這些機制單看都不新，價值在能自動彼此組合"
type_hint: 方法
context_type: evidence_from_single_source
sources:
  - article: claude-code
    article_title: "拆解 Claude Code：Agentic Loop、工具系統、Skills 與權限機制"
    url: https://datasciocean.com/ai-concept/claude-code/
    sections:
      - 前言
      - Agentic Loop
      - 擴充 Agent：Skills、Hooks 與 MCP
      - Skills——封裝、可被發現的操作程序
      - Hooks——在生命週期節點上的確定性控制
      - MCP——連接外部世界的標準協定
      - Context 工程的實務應用
      - 結語
    first_appearance: true
parent: null
related:
  - claude-code-agentic-loop-and-tools
  - claude-code-permission-blast-radius
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: 'Claude Code 的摘要、範圍化委派、專案設定檔這三個機制單獨拿出來看都不算新穎，真正讓它們成為「Harness」而非單純「功能」的，是它們能自動彼此組合；結語也說，包含 Skills、Hooks、MCP 在內的這些機制單獨拿出來看都不算特殊技術，真正讓它能運作的，是它們被設計成可以彼此組合'
    source_quotes:
      - '這三個機制單獨拿出來看都不算新穎——摘要、範圍化委派、專案設定檔，在 agentic 編碼工具出現之前就已存在。真正讓它們成為「Harness」而非單純「功能」的，是它們能自動彼此組合'
      - '這些單獨拿出來看都不算是什麼特殊技術——真正讓它能運作的，是這些機制被設計成可以彼此組合'
    anchor_type: 部落格判斷
    importance: 1
    status: normal
  - id: c2
    role: context
    text: 'Claude Code 是 Anthropic 推出的 agentic 編碼 CLI'
    source_quotes:
      - 'Claude Code 是 Anthropic 推出的 agentic 編碼 CLI'
    anchor_type: 背景說明
    importance: 2
    status: normal
  - id: c3
    role: context
    text: 'blog 把 Claude Code 看作圍繞著一個凍結模型所建構的精簡、可組合的 Harness，而不是「一個能存取檔案的聊天機器人」'
    source_quotes:
      - '與其把 Claude Code 理解成「一個能存取檔案的聊天機器人」，不如把它看作圍繞著一個凍結模型所建構的精簡、可組合的 Harness'
    anchor_type: 部落格判斷
    importance: 3
    status: normal
  - id: c4
    role: context
    text: 'blog 把 Claude Code 視為「Model + Harness + Context」框架的具體實作，三層是凍結模型、執行腳手架、動態組裝的 Context；Claude Code 的工具系統、Hooks 與 CLAUDE.md 記憶，正是這套架構的實際落地'
    source_quotes:
      - '「Model + Harness + Context」框架的具體實作。'
      - '一文提出的「凍結模型、執行腳手架、動態組裝的 Context」三層架構並非只是理論——Claude Code 的工具系統、Hooks 與 `CLAUDE.md` 記憶，正是這套架構的實際落地。'
    anchor_type: 部落格判斷
    importance: 4
    status: normal
  - id: c5
    role: mechanism
    text: 'blog 認為，一個凍結的模型加上固定的工具清單，對於編碼 Agent 實際會遇到的任務範圍來說仍然太過僵化；Claude Code 的 harness 層額外提供三個擴充點，各自解決不同的問題'
    source_quotes:
      - '一個凍結的模型加上固定的工具清單，對於編碼 Agent 實際會遇到的任務範圍來說仍然太過僵化。Claude Code 的 harness 層額外提供三個擴充點，各自解決不同的問題'
    anchor_type: 部落格判斷
    importance: 5
    status: normal
  - id: c6
    role: mechanism
    text: 'Skill 是一個資料夾，裡面裝著描述如何完成特定、重複性任務的指示(可選附帶腳本)'
    source_quotes:
      - 'Skill 是一個資料夾，裡面裝著描述如何完成特定、重複性任務的指示(可選附帶腳本)'
    anchor_type: 設計參數
    importance: 6
    status: normal
  - id: c7
    role: mechanism
    text: 'Skills 只會在需要時才載入 context：模型一開始只會看到每個可用 skill 的一行描述，只有真正用到的那一個，才會把完整指示拉進來'
    source_quotes:
      - 'Skills 只會在需要時才載入 context：模型一開始只會看到每個可用 skill 的一行描述，只有真正用到的那一個，才會把完整指示拉進來。'
    anchor_type: 設計參數
    importance: 7
    status: normal
  - id: c8
    role: evaluation
    text: 'blog 把 Skills 的這種載入方式視為「漸進式揭露」原則：不該為當前任務用不到的能力預付 context 成本'
    source_quotes:
      - '這正是 harness-engineering 筆記中 [Just-In-Time 工具注入](../harness-engineering/#just-in-time-jit-tool-injection) 所談的「漸進式揭露」原則——不該為當前任務用不到的能力預付 context 成本。'
    anchor_type: 部落格判斷
    importance: 8
    status: normal
  - id: c9
    role: mechanism
    text: 'Hooks 是 harness 在固定節點執行的 shell 指令——工具執行前、Agent 回覆完成後、Session 開始時'
    source_quotes:
      - 'Hooks 是 harness 在固定節點執行的 shell 指令——工具執行前、Agent 回覆完成後、Session 開始時。'
    anchor_type: 設計參數
    importance: 9
    status: normal
  - id: c10
    role: evaluation
    text: 'blog 認為，因為 Hook 是一般程式碼而非模型呼叫，所以它是實作「模型本身無法被信任會可靠遵守」的保證的正確位置；Hooks 讓「Agent 絕不能做 X」從系統提示裡一句寄望變成真正被強制執行的規則'
    source_quotes:
      - '因為 Hook 是一般程式碼，而非模型呼叫，所以它是實作「模型本身無法被信任會可靠遵守」的保證的正確位置'
      - 'Hooks 讓「Agent 絕不能做 X」從系統提示裡一句寄望變成真正被強制執行的規則。'
    anchor_type: 部落格判斷
    importance: 10
    status: normal
  - id: c11
    role: anchor
    text: 'blog 舉的 Hooks 用法包括：阻擋對受保護路徑的寫入、在每次編輯後自動格式化檔案，或是在 lint 檢查不通過時直接讓該輪失敗'
    source_quotes:
      - '阻擋對受保護路徑的寫入、在每次編輯後自動格式化檔案，或是在 lint 檢查不通過時直接讓該輪失敗'
    anchor_type: 部落格舉例
    importance: 11
    status: normal
  - id: c12
    role: mechanism
    text: 'Model Context Protocol 讓 Claude Code 能透過共通介面與外部服務對話——GitHub、資料庫、內部 API——而不必為每個整合手刻一套客製化工具程式碼'
    source_quotes:
      - 'Model Context Protocol 讓 Claude Code 能透過共通介面與外部服務對話——GitHub、資料庫、內部 API——而不必為每個整合手刻一套客製化工具程式碼。'
    anchor_type: 背景說明
    importance: 12
    status: normal
  - id: c13
    role: mechanism
    text: '一個 MCP server 自己宣告它有哪些工具與資源；harness 再把這些工具以與內建工具相同的方式呈現給模型'
    source_quotes:
      - '一個 MCP server 自己宣告它有哪些工具與資源；harness 再把這些工具以與內建工具相同的方式呈現給模型。'
    anchor_type: 設計參數
    importance: 13
    status: normal
  - id: c14
    role: evaluation
    text: 'blog 認為，這正是讓同一個 Agent 能同時觸及 Slack 工作區、工單系統與私有 repo，而 harness 作者不需要為每一個都自己寫一份 client 的關鍵'
    source_quotes:
      - '這正是讓同一個 Agent 能同時觸及 Slack 工作區、工單系統與私有 repo，而 harness 作者不需要為每一個都自己寫一份 client 的關鍵。'
    anchor_type: 部落格判斷
    importance: 14
    status: normal
  - id: c15
    role: context
    text: 'blog 描述的 harness 會在模型發出工具呼叫時介入(執行權限檢查、記錄 log、觸發 Hooks)、在固定節點執行 Hooks，並把 MCP server 宣告的工具以與內建工具相同的方式呈現給模型'
    source_quotes:
      - 'harness 因此獲得一個乾淨的攔截點——可以在任何動作真正發生前，執行權限檢查、記錄 log、或觸發 Hooks。'
      - 'Hooks 是 harness 在固定節點執行的 shell 指令'
      - '一個 MCP server 自己宣告它有哪些工具與資源；harness 再把這些工具以與內建工具相同的方式呈現給模型。'
    anchor_type: 設計參數
    importance: 15
    status: normal
  - id: c16
    role: mechanism
    text: 'CLAUDE.md 作為專案層級記憶：一份被 checked in 的 CLAUDE.md 會在 session 開始時被讀取並自動摺入 context，持久、共享，且不依附於任何單一對話'
    source_quotes:
      - '一份被 checked in 的 `CLAUDE.md`——就像管轄本 repo 部落格發文慣例的那一份——會在 session 開始時被讀取並自動摺入 context。'
      - '持久、共享，且不依附於任何單一對話'
    anchor_type: 設計參數
    importance: 16
    status: normal
  - id: c17
    role: mechanism
    text: '長時間的 session 終究會逼近 context window 的上限。Claude Code 不會盲目截斷，而是把較早的對話摘要成精簡版本後繼續工作——對話得以延續，使用者不需要重啟或重新解釋先前的決策'
    source_quotes:
      - '長時間的 session 終究會逼近 context window 的上限。Claude Code 不會盲目截斷，而是把較早的對話摘要成精簡版本後繼續工作——對話得以延續，使用者不需要重啟或重新解釋先前的決策。'
    anchor_type: 設計參數
    importance: 17
    status: normal
  - id: c18
    role: mechanism
    text: '透過 Task 工具把一次範圍廣、探索性的搜尋(例如「找出某個設定值在大型程式碼庫裡所有被用到的地方」)派給 Subagent，能讓這次搜尋雜訊多的中間輸出留在主迴圈的 context 之外——只有 Subagent 最終的摘要會回傳'
    source_quotes:
      - '透過 `Task` 工具把一次範圍廣、探索性的搜尋(例如「找出某個設定值在大型程式碼庫裡所有被用到的地方」)派給 Subagent，能讓這次搜尋雜訊多的中間輸出留在主迴圈的 context 之外——只有 Subagent 最終的摘要會回傳。'
    anchor_type: 設計參數
    importance: 18
    status: normal
  - id: c19
    role: evaluation
    text: 'blog 認為 Subagent 委派讓複雜的子任務使 context 長度呈現鋸齒狀變化，而不是對主對話造成永久性、不斷累積的負擔'
    source_quotes:
      - '這正是 Context Engineering 筆記中「Folding」模式的實際應用：複雜的子任務讓 context 長度呈現鋸齒狀變化，而不是對主對話造成永久性、不斷累積的負擔。'
    anchor_type: 部落格判斷
    importance: 19
    status: normal
  - id: c20
    role: anchor
    text: 'blog 舉的機制自動彼此組合的兩個例子：Subagent 的摘要本身也可能在後續的壓縮流程中被再次摺入，而 CLAUDE.md 的慣例無論當前這一輪來自使用者、或來自 Hook 觸發的重試，都會被一致地套用'
    source_quotes:
      - 'Subagent 的摘要本身也可能在後續的壓縮流程中被再次摺入，而 `CLAUDE.md` 的慣例無論當前這一輪來自使用者、或來自 Hook 觸發的重試，都會被一致地套用。'
    anchor_type: 部落格舉例
    importance: 20
    status: normal
```
