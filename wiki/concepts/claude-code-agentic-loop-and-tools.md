---
id: claude-code-agentic-loop-and-tools
title: "Claude Code 的核心只有一個迴圈：一個能呼叫工具、觀察結果、自己決定下一步的 LLM，搭配一組刻意精簡的通用工具，不另掛規劃模組"
type_hint: 方法
context_type: bound_to_source
sources:
  - article: claude-code
    article_title: "拆解 Claude Code：Agentic Loop、工具系統、Skills 與權限機制"
    url: https://datasciocean.com/ai-concept/claude-code/
    sections:
      - 前言
      - Claude Code 到底是什麼
      - Agentic Loop
      - 工具系統
      - Claude Code 在 Agent Harness 版圖中的定位
      - 結語
    first_appearance: true
parent: null
related:
  - claude-code-extension-and-context
  - claude-code-permission-blast-radius
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: 'Claude Code 以 CLI(以及 SDK)行程的形式運作，其核心其實只有一個原語：一個能呼叫工具、觀察結果、並決定下一步該做什麼的 LLM——如此反覆，直到它自己判斷任務已經完成'
    source_quotes:
      - 'Claude Code 以 CLI(以及 SDK)行程的形式運作，其核心其實只有一個原語：一個能呼叫工具、觀察結果、並決定下一步該做什麼的 LLM——如此反覆，直到它自己判斷任務已經完成。'
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
    text: 'blog 說，「凍結模型、執行腳手架、動態組裝的 Context」這個三層架構並非只是理論，Claude Code 的工具系統、Hooks 與 CLAUDE.md 記憶，正是這套架構的實際落地'
    source_quotes:
      - '一文提出的「凍結模型、執行腳手架、動態組裝的 Context」三層架構並非只是理論——Claude Code 的工具系統、Hooks 與 `CLAUDE.md` 記憶，正是這套架構的實際落地。'
    anchor_type: 部落格判斷
    importance: 4
    status: normal
  - id: c5
    role: mechanism
    text: 'Claude Code 沒有另外掛一個「規劃模組」或「執行模組」，規劃與執行都發生在同一個迴圈裡，由模型自己對剛才觀察到的結果進行推理來驅動'
    source_quotes:
      - '這裡沒有另外掛一個「規劃模組」或「執行模組」——規劃與執行都發生在同一個迴圈裡，由模型自己對剛才觀察到的結果進行推理來驅動。'
    anchor_type: 設計參數
    importance: 5
    status: normal
  - id: c6
    role: mechanism
    text: 'Claude Code 的關鍵特徵是觀察與行動使用同一套介質：一次失敗測試的 stderr 會直接成為下一輪 prompt 的輸入，不需要人類居中轉達'
    source_quotes:
      - 'Claude Code 的關鍵特徵是：**觀察與行動使用同一套介質**——一次失敗測試的 stderr 會直接成為下一輪 prompt 的輸入，不需要人類居中轉達。'
    anchor_type: 設計參數
    importance: 6
    status: normal
  - id: c7
    role: evaluation
    text: 'blog 說，這讓 Claude Code 與 IDE 的自動補全(預測 token，而非行動)以及早期「跟你的程式碼聊天」型助理(只能讀，無法動手)區隔開來'
    source_quotes:
      - '這讓它與 IDE 的自動補全(預測 token，而非行動)以及早期「跟你的程式碼聊天」型助理(只能讀，無法動手)區隔開來。'
    anchor_type: 部落格判斷
    importance: 7
    status: normal
  - id: c8
    role: mechanism
    text: '因為模型必須明確發出一個工具呼叫，而不是用自由文字說「我現在要去改檔案了」，harness 獲得一個乾淨的攔截點，可以在任何動作真正發生前，執行權限檢查、記錄 log、或觸發 Hooks，所以每一輪都可被檢視'
    source_quotes:
      - '**每一輪都可被檢視。** 因為模型必須明確發出一個工具呼叫，而不是用自由文字說「我現在要去改檔案了」，harness 因此獲得一個乾淨的攔截點——可以在任何動作真正發生前，執行權限檢查、記錄 log、或觸發 Hooks。'
    anchor_type: 設計參數
    importance: 8
    status: normal
  - id: c9
    role: mechanism
    text: '失敗只是另一種觀察結果：測試失敗、語法錯誤、被拒絕的權限請求都不會讓迴圈中止，而是變成下一輪的輸入，模型會據此重新規劃'
    source_quotes:
      - '**失敗只是另一種觀察結果。** 測試失敗、語法錯誤、被拒絕的權限請求——這些都不會讓迴圈中止，而是變成下一輪的輸入，模型會據此重新規劃。'
    anchor_type: 設計參數
    importance: 9
    status: normal
  - id: c10
    role: evaluation
    text: 'blog 認為，一個能從錯誤中恢復的單體迴圈，遠比一個沒有預期到錯誤會發生的脆弱多階段管線更穩健'
    source_quotes:
      - '一個能從錯誤中恢復的單體迴圈，遠比一個沒有預期到錯誤會發生的脆弱多階段管線更穩健。'
    anchor_type: 部落格判斷
    importance: 10
    status: normal
  - id: c11
    role: anchor
    text: 'blog 給的 agent_loop 範例裡，模型的回應若是最終答案就結束；否則需要確認的工具呼叫先問使用者，使用者不核准就把拒絕的回饋附進 transcript 並繼續下一輪；核准後執行工具，把觀察結果附進 transcript'
    source_quotes:
      - 'if response.is_final_answer: done = True'
      - 'if requires_confirmation(response.tool_call): approved = ask_user(response.tool_call) if not approved: transcript.append(denial_feedback(response.tool_call)) continue'
      - 'result = execute(response.tool_call, cwd) transcript.append(observation(response.tool_call, result))'
    anchor_type: 部落格舉例
    importance: 11
    status: normal
  - id: c12
    role: mechanism
    text: 'Claude Code 的行動空間是一組精簡的通用工具，而非上百個針對特定任務打造的工具——這是刻意的設計，讓模型能夠自由組合工具，而不是四處尋找「剛好對的」那一個窄用途工具'
    source_quotes:
      - 'Claude Code 的行動空間是一組精簡的通用工具，而非上百個針對特定任務打造的工具——這是刻意的設計，讓模型能夠自由組合工具，而不是四處尋找「剛好對的」那一個窄用途工具'
    anchor_type: 設計參數
    importance: 12
    status: pending_author_confirmation
  - id: c13
    role: anchor
    text: 'blog 的工具表中，Read／Glob／Grep 用來理解程式碼庫而不需要把整個專案塞進 context；Edit／Write 用來進行有針對性的修改(Edit 是精確字串替換，Write 用於新檔案或整檔重寫)；Bash 執行任意 shell 指令，是專用工具涵蓋不到時的通用逃生門'
    source_quotes:
      - '`Read` / `Glob` / `Grep` | 理解程式碼庫——讀取已知檔案、依 pattern 找檔案、用正規表示式搜尋內容——不需要把整個專案塞進 context。'
      - '`Edit` / `Write` | 進行有針對性的修改(`Edit` 是精確字串替換；`Write` 用於新檔案或整檔重寫)。'
      - '`Bash` | 執行任意 shell 指令——build、test、lint、安裝套件、git——是專用工具涵蓋不到時的通用逃生門。'
    anchor_type: 設計參數
    importance: 13
    status: normal
  - id: c14
    role: anchor
    text: 'blog 的工具表中，Task(Subagent) 把獨立、自包含的一段工作委派給另一個擁有自己 context window 的 Agent 實例，只回傳摘要結果；WebFetch／WebSearch 在本地程式碼庫本身無法回答問題時，拉取檔案系統之外的資訊'
    source_quotes:
      - '`Task`(Subagent) | 把獨立、自包含的一段工作委派給另一個擁有自己 context window 的 Agent 實例，只回傳摘要結果。'
      - '`WebFetch` / `WebSearch` | 當本地程式碼庫本身無法回答問題時，拉取檔案系統之外的資訊。'
    anchor_type: 設計參數
    importance: 14
    status: normal
  - id: c15
    role: mechanism
    text: 'blog 認為真正重要的設計選擇並非某一個特定工具，而是：凡是有專用、窄用途工具(Read、Edit、Grep)可用的地方，一律優先於通用的 Bash 逃生門'
    source_quotes:
      - '真正重要的設計選擇並非某一個特定工具，而是：凡是有專用、窄用途工具(`Read`、`Edit`、`Grep`)可用的地方，一律優先於通用的 `Bash` 逃生門。'
    anchor_type: 部落格判斷
    importance: 15
    status: pending_author_confirmation
  - id: c16
    role: evaluation
    text: 'blog 說，窄用途工具的失敗面遠比 shell out 到 sed／cat 小，其結構化輸出也更容易讓模型與 harness 雙方推理'
    source_quotes:
      - '窄用途工具的失敗面遠比 shell out 到 `sed`/`cat` 小，其結構化輸出也更容易讓模型與 harness 雙方推理。'
    anchor_type: 部落格判斷
    importance: 16
    status: pending_author_confirmation
  - id: c17
    role: evaluation
    text: '相較於 OpenClaw 強調長時間運行的自主性與自製工具能力，Claude Code 的定位刻意較為聚焦：它主要針對軟體工程的迴圈本身做優化——讀程式碼、改程式碼、驗證變更'
    source_quotes:
      - '相較於 [OpenClaw](../openclaw-intro/) 強調長時間運行的自主性與自製工具能力，Claude Code 的定位刻意較為聚焦：它主要針對軟體工程的迴圈本身做優化——讀程式碼、改程式碼、驗證變更'
    anchor_type: 部落格判斷
    importance: 17
    status: normal
  - id: c18
    role: evaluation
    text: '這是刻意的取捨：一個範圍較窄、觀測性良好的行動空間，比起完全通用的行動空間，更容易同時做到「有能力」與「安全」'
    source_quotes:
      - '這是刻意的取捨：一個範圍較窄、觀測性良好的行動空間，比起完全通用的行動空間，更容易同時做到「有能力」與「安全」。'
    anchor_type: 部落格判斷
    importance: 18
    status: normal
```
