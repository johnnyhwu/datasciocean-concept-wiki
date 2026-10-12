---
id: claude-code-permission-blast-radius
title: "無人看管的自主 Agent，安全不能靠模型每次猜對：使用者選權限模式、確認提示隨動作可逆程度調整、沙盒另外限制最壞情況，目標是讓犯錯便宜且可逆"
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
  - article: claude-code
    article_title: "拆解 Claude Code：Agentic Loop、工具系統、Skills 與權限機制"
    url: https://datasciocean.com/ai-concept/claude-code/
    sections:
      - 前言
      - Agentic Loop
      - 權限機制與影響範圍(Blast Radius)
      - 結語
    first_appearance: true
parent: null
related:
  - claude-code-agentic-loop-and-tools
  - claude-code-extension-and-context
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: '一個能無人看管地執行任意 shell 指令、修改檔案的 Agent，需要一層不能單純仰賴模型「每次都猜對」的安全機制；目標不是讓 Agent 完全不可能犯錯，而是讓犯錯的代價變得低廉且可逆，使迴圈得以持續運作，而不需要人類在每一次失誤時都出手介入'
    source_quotes:
      - '一個能無人看管地執行任意 shell 指令、修改檔案的 Agent，需要一層不能單純仰賴模型「每次都猜對」的安全機制。'
      - '目標不是讓 Agent 完全不可能犯錯，而是讓犯錯的代價變得低廉且可逆，使迴圈得以持續運作，而不需要人類在每一次失誤時都出手介入。'
    anchor_type: 部落格判斷
    importance: 1
    status: normal
  - id: c2
    role: context
    text: 'Claude Code 是 Anthropic 推出的 agentic 編碼 CLI：被交付一個目標後就自行主導全局——讀檔、下指令、改程式碼、驗證自己的成果，全部在一個迴圈中自主完成'
    source_quotes:
      - 'Claude Code 是 Anthropic 推出的 agentic 編碼 CLI：與其在人類主導下預測下一行程式碼，它更像是被交付一個目標後就自行主導全局——讀檔、下指令、改程式碼、驗證自己的成果，全部在一個迴圈中自主完成。'
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
    text: '因為模型必須明確發出一個工具呼叫，而不是用自由文字說「我現在要去改檔案了」，harness 獲得一個乾淨的攔截點，可以在任何動作真正發生前，執行權限檢查、記錄 log、或觸發 Hooks'
    source_quotes:
      - '因為模型必須明確發出一個工具呼叫，而不是用自由文字說「我現在要去改檔案了」，harness 因此獲得一個乾淨的攔截點——可以在任何動作真正發生前，執行權限檢查、記錄 log、或觸發 Hooks。'
    anchor_type: 設計參數
    importance: 5
    status: normal
  - id: c6
    role: mechanism
    text: '被拒絕的權限請求不會讓迴圈中止，而是變成下一輪的輸入，模型會據此重新規劃'
    source_quotes:
      - '測試失敗、語法錯誤、被拒絕的權限請求——這些都不會讓迴圈中止，而是變成下一輪的輸入，模型會據此重新規劃。'
    anchor_type: 設計參數
    importance: 6
    status: normal
  - id: c7
    role: anchor
    text: 'blog 給的 agent_loop 範例裡，需要確認的工具呼叫會先問使用者，使用者不核准就把拒絕的回饋附進 transcript 並繼續下一輪'
    source_quotes:
      - 'if requires_confirmation(response.tool_call): approved = ask_user(response.tool_call) if not approved: transcript.append(denial_feedback(response.tool_call)) continue'
    anchor_type: 部落格舉例
    importance: 7
    status: normal
  - id: c8
    role: mechanism
    text: 'Claude Code 的權限做法是漸進式的，而非二元的'
    source_quotes:
      - 'Claude Code 的做法是漸進式的，而非二元的'
    anchor_type: 設計參數
    importance: 8
    status: normal
  - id: c9
    role: mechanism
    text: '權限模式(Permission Modes)從「每個非瑣碎動作都先詢問」，到「在明確清單內自動核准」(例如唯讀指令，或工作目錄內的編輯)，再到「在隔離環境中完全自主執行」'
    source_quotes:
      - '**權限模式(Permission Modes)** 從「每個非瑣碎動作都先詢問」，到「在明確清單內自動核准」(例如唯讀指令，或工作目錄內的編輯)，再到「在隔離環境中完全自主執行」'
    anchor_type: 設計參數
    importance: 9
    status: pending_author_confirmation
  - id: c10
    role: mechanism
    text: '權限模式由使用者選擇，而非模型自己決定'
    source_quotes:
      - '由使用者選擇模式，而非模型自己決定。'
    anchor_type: 設計參數
    importance: 10
    status: normal
  - id: c11
    role: mechanism
    text: '可逆性決定是否需要確認提示'
    source_quotes:
      - '**可逆性決定是否需要確認提示。**'
    anchor_type: 設計參數
    importance: 11
    status: normal
  - id: c12
    role: mechanism
    text: '讀取檔案或執行測試在幾乎所有模式下都會被自動核准，因為就算判斷錯了，代價也很低'
    source_quotes:
      - '讀取檔案或執行測試在幾乎所有模式下都會被自動核准，因為就算判斷錯了，代價也很低。'
    anchor_type: 設計參數
    importance: 12
    status: pending_author_confirmation
  - id: c13
    role: mechanism
    text: '強制推送(force-push)、刪除分支、rm -rf 這類動作，在任何模式下預設都需要明確確認，因為事後可能根本無法復原'
    source_quotes:
      - '強制推送(force-push)、刪除分支、`rm -rf` 這類動作，在任何模式下預設都需要明確確認，因為事後可能根本無法復原。'
    anchor_type: 設計參數
    importance: 13
    status: pending_author_confirmation
  - id: c14
    role: mechanism
    text: '即使在寬鬆的模式下，在容器或範圍受限的環境中執行，也代表一個錯誤的 shell 指令無法觸及任務工作目錄以外的地方'
    source_quotes:
      - '**沙盒限制了最壞情況的範圍。** 即使在寬鬆的模式下，在容器或範圍受限的環境中執行，也代表一個錯誤的 shell 指令無法觸及任務工作目錄以外的地方'
    anchor_type: 設計參數
    importance: 14
    status: normal
  - id: c15
    role: evaluation
    text: 'blog 認為，權限機制與執行邊界是兩道獨立的防線，而非互相替代'
    source_quotes:
      - '權限機制與執行邊界是兩道獨立的防線，而非互相替代'
    anchor_type: 部落格判斷
    importance: 15
    status: normal
```
