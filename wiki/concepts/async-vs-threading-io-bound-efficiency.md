---
id: async-vs-threading-io-bound-efficiency
title: 在 I/O 密集型應用中，Async 能以更低的成本實現更高的資源利用率：上下文切換便宜得多、每個 Coroutine 的記憶體遠小於一個 Thread Stack，而 Python 的 GIL 本來就限制了多執行緒的 CPU 並行
type_hint: 判斷
context_type: standalone_classic
sources:
- article: fastapi-race-condition
  article_title: "FastAPI 的並行陷阱：從 Race Condition 到 Deadlock，徹底搞懂全域變數的正確用法"
  url: https://datasciocean.com/other/fastapi-race-condition/
  sections:
  - FastAPI 如何處理同步 (def) 與非同步 (async def) Endpoint?
  - 什麼情況下 Async 比 Multi-Threading 更有效率?
  - 上下文切換 (Context Switch) 的成本天差地遠
  - 記憶體開銷 (Memory Overhead)
  - Python 的全域直譯器鎖 (Global Interpreter Lock, GIL)
  - Multi-Threading 與 Async 比較
  - Thread-Safe 與 Async-Safe 的敵人是誰?
  first_appearance: true
parent: null
related:
  - shared-object-race-condition-mutable-state
  - local-variables-isolated-stack-and-coroutine
  - thread-safe-not-async-safe-deadlock
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: Async 比 Multi-threading 更有效率，是在特定且非常常見的場景下，也就是 I/O 密集型（I/O-Bound）的應用中，Async 的運作模式能以更低的成本實現更高的資源利用率
  source_quotes:
  - 您經常聽到 Async 比 Multi-threading 更有效率，是因為在特定且非常常見的場景下——也就是 I/O 密集型 (I/O-Bound) 的應用中——Async 的運作模式能以更低的成本實現更高的資源利用率。
  qualifiers:
  - text: Async 世界只有一個 Thread；任何一段程式碼佔用 CPU 不放或做 Blocking I/O，整個 Event Loop 就會被卡住，所有其他並行任務都停滯
    source_quote: 原因：在 Async 世界裡，只有一個 Thread。如果任何一段程式碼佔用 CPU 不放，或者進行了 Blocking I/O 操作，整個 Event Loop 就會被卡住，所有其他的並行任務都將停滯
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: 在 FastAPI 中，def 定義的 Endpoint 走 Multi-Threading：直接在主事件迴圈執行可能阻塞整個服務，所以 FastAPI 把它委派給一個獨立的 Thread Pool；async def 定義的 Endpoint 走 Async：在主事件迴圈中，多個請求在同一個執行緒中交錯執行
  source_quotes:
  - 當 FastAPI 直接在主事件迴圈中執行它，將可能會阻塞整個服務 (e.g. 當這個 Endpoint 會進行 I/O Blocking 或是 CPU Intensive 的運算)，使其無法回應其他請求。為了避免這種情況，FastAPI 會將這些同步函式的執行，委派給一個獨立的 Thread Pool。
  - FastAPI 會在主事件迴圈 (Main Event Loop) 中直接執行它。這意味著多個請求會以 Cooperative Multitasking 的方式，在同一個執行緒中交錯執行
  - 特性 | Multi-Threading (def 端點) | Async (async def 端點)
  qualifiers:
  - text: def Endpoint 直接在主事件迴圈執行時是「可能」阻塞整個服務，例子是 Endpoint 會做 I/O Blocking 或 CPU Intensive 的運算
    source_quote: 將可能會阻塞整個服務 (e.g. 當這個 Endpoint 會進行 I/O Blocking 或是 CPU Intensive 的運算)
  anchor_type: 背景說明
  importance: 2
  status: normal
- id: c3
  role: context
  text: 效率的提升主要來自幾個關鍵因素，其中上下文切換（Context Switch）的成本是最核心、最重要的原因；Python 的全域直譯器鎖（GIL）這一點在 Python 的世界中尤其重要
  source_quotes:
  - 效率的提升主要來自以下幾個關鍵因素：
  - 這是最核心、最重要的原因。
  - 這一點在 Python 的世界中尤其重要。
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: Multi-threading 的上下文切換由作業系統核心強制執行，是重量級操作：要儲存當前 Thread 所有的 CPU 狀態（CPU Register、Program Counter、Stack Pointer 等）再載入下一個 Thread 的完整狀態，牽涉 Kernel Mode 與 User Mode 的切換；而且是搶佔式（Preemptive），可能發生在任何時間點
  source_quotes:
  - 由作業系統 (OS) 核心強制執行：當作業系統決定要暫停一個 Thread，改為執行另一個 Thread 時，它需要介入
  - 重量級操作：這個過程需要儲存當前 Thread 所有的 CPU 狀態，包括 CPU Register、Program Counter、Stask Pointer 等。然後，載入下一個 Thread 的完整狀態。這是一個牽涉到作業系統 Kernel Mode 與 User Mode 的切換
  - 搶佔式 (Preemptive)：作業系統會強制剝奪 Thread 的執行權，不管它自己願不願意，這可能發生在任何時間點
  anchor_type: 背景說明
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: Async 的上下文切換由應用程式的 Event Loop 執行，完全發生在 User Space，作業系統不知道這些 Coroutine 的存在；切換只在 await 處發生，Event Loop 只是保存當前 Coroutine 的狀態（幾個變數和一個指標），再從 Queue 取出下一個就緒的 Coroutine；是協作式（Cooperative），由 Coroutine 主動讓出執行權
  source_quotes:
  - 由應用程式的 Event Loop 執行：切換完全發生在應用程式的 User Space，作業系統根本不知道也不關心這些 Coroutine 的存在
  - 輕量級操作：切換只在 await 關鍵字處發生。Event Loop 所做的僅僅是：保存當前 Coroutine 的狀態 (幾個變數和一個指標)，然後從 Queue 中取出下一個就緒的 Coroutine 來執行。
  - 協作式 (Cooperative)：切換只發生在程式設計師明確寫下 await 的地方，是 Coroutine「主動讓出」執行權
  anchor_type: 背景說明
  importance: 5
  status: normal
- id: c6
  role: anchor
  text: 切換成本的量級：Thread 的上下文切換通常是微秒級，但累積起來非常可觀；Async 的切換幾乎和一次函式呼叫一樣快，是奈秒級
  source_quotes:
  - 以電腦的尺度來看，是非常耗時的操作 (通常是微秒級，但累積起來非常可觀)
  - 這幾乎和一次函式呼叫一樣快 (奈秒級)
  anchor_type: 背景說明
  importance: 6
  status: normal
- id: c7
  role: evaluation
  text: 處理 10,000 個並行請求，Multi-threading 可能需要作業系統進行數萬次昂貴的上下文切換；Async 只需要 Event Loop 進行數萬次極其廉價的內部狀態切換
  source_quotes:
  - 結論：處理 10,000 個並行請求，Multi-threading 可能需要作業系統進行數萬次昂貴的上下文切換；而 Async 只需要 Event Loop 進行數萬次極其廉價的內部狀態切換。
  anchor_type: 部落格判斷
  comparison_target: Async 的 Event Loop 進行數萬次廉價的內部狀態切換
  importance: 7
  status: normal
- id: c8
  role: anchor
  text: 記憶體開銷：每建立一個 Thread，作業系統都要分配一塊完整的 Thread Stack，預設大小通常不小（例如在 Linux 上可能是 8MB）；建立 1,000 個執行緒處理 1,000 個並行請求，光是堆疊就佔用 1000 * 8MB = 8GB，使系統無法擴展到非常高的並行數量
  source_quotes:
  - Multi-threading：每建立一個 Thread，作業系統都需要為其分配一塊完整的 Thread Stack。這個 Stack 的預設大小通常不小 (例如在 Linux 上可能是 8MB)。如果你要建立 1,000 個執行緒來處理 1,000 個並行請求，光是堆疊就會佔用 1000 * 8MB = 8GB 的記憶體！這使得系統無法擴展到非常高的並行數量
  qualifiers:
  - text: 8MB 是「例如在 Linux 上可能是」的預設 Stack 大小，不是固定值
    source_quote: 這個 Stack 的預設大小通常不小 (例如在 Linux 上可能是 8MB)
  anchor_type: 數學推導
  comparison_target: Async 只有一個 Thread、一個 Stack，每個 Coroutine Object 通常只有幾 KB
  importance: 8
  status: normal
- id: c9
  role: anchor
  text: Async 只有一個 Thread、一個 Stack；Coroutine Object 雖然也佔 Heap 記憶體，但每個通常只有幾 KB，遠小於一個完整的 Thread Stack，所以用幾個 GB 的記憶體就能維持數萬甚至數十萬個處於「等待 I/O」狀態的 Coroutine
  source_quotes:
  - Async：只有一個 Thread，所以只有一個 Stack。所有的 Coroutine Object 雖然也佔用記憶體 (在 Heap 中)，但每個 Coroutine Object 的大小遠遠小於一個完整的 Thread Stack (通常只有幾 KB)。因此，用幾個 GB 的記憶體，你可以輕鬆地維持數萬甚至數十萬個處於「等待 I/O」狀態的 Coroutine。
  anchor_type: 背景說明
  importance: 9
  status: normal
- id: c10
  role: evaluation
  text: 記憶體開銷的差異是 Async 能夠輕鬆解決 C10k 問題（單機同時處理一萬個連線）的關鍵
  source_quotes:
  - 這個差異是 Async 能夠輕鬆解決著名的 C10k 問題 (單機同時處理一萬個連線) 的關鍵。
  anchor_type: 部落格判斷
  importance: 10
  status: normal
- id: c11
  role: mechanism
  text: CPython 直譯器中的 GIL 確保任何時刻只有一個 Thread 能執行 Python 的位元組碼（Bytecode）；所以即使在 8 核心的 CPU 上，一個 Python 程式的多個 Thread 也無法真正地並行執行 CPU 密集型的計算，實際上是在同一個 CPU 核心上快速輪流執行，看起來像並行，但總的計算量沒有增加
  source_quotes:
  - CPython 直譯器中的 GIL 是一把大鎖，它確保了在任何時刻，只有一個 Thread 能執行 Python 的位元組碼 (Bytecode)
  - 這意味著，即使在一個 8 核心的 CPU 上，一個 Python 程式的多個 Thread 也無法真正地並行 (Parallel) 執行 CPU 密集型的計算。它們實際上是在同一個 CPU 核心上快速輪流執行，看起來像並行，但總的計算量沒有增加
  qualifiers:
  - text: Thread 在等待 I/O 時會釋放 GIL，所以 Multi-threading 在 Python 中對 I/O-Bound 任務仍然有效
    source_quote: 但是，當一個 Thread 在等待 I/O (如網路、磁碟讀寫) 時，它會釋放 GIL。這就是為什麼 Multi-threading 在 Python 中對 I/O-Bound 任務仍然有效的原因。
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 假設題設
  importance: 11
  status: normal
- id: c12
  role: qualifier
  text: 但 Thread 在等待 I/O（如網路、磁碟讀寫）時會釋放 GIL，這就是 Multi-threading 在 Python 中對 I/O-Bound 任務仍然有效的原因
  source_quotes:
  - 但是，當一個 Thread 在等待 I/O (如網路、磁碟讀寫) 時，它會釋放 GIL。這就是為什麼 Multi-threading 在 Python 中對 I/O-Bound 任務仍然有效的原因。
  anchor_type: 背景說明
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: 既然 GIL 限制了真正的 CPU 並行，而 Async 又能在單一 Thread 上用更低的成本處理 I/O-Bound 任務，在大多數 Web 服務場景下，Async 的模型就顯得更具吸引力
  source_quotes:
  - 然而，既然 GIL 限制了真正的 CPU 並行，而 Async 又能在單一 Thread 上用更低的成本處理 I/O-Bound 任務，那麼在大多數 Web 服務場景下，Async 的模型就顯得更具吸引力。
  qualifiers:
  - text: Async 世界只有一個 Thread；任何一段程式碼佔用 CPU 不放或做 Blocking I/O，整個 Event Loop 就會被卡住，所有其他並行任務都停滯
    source_quote: 原因：在 Async 世界裡，只有一個 Thread。如果任何一段程式碼佔用 CPU 不放，或者進行了 Blocking I/O 操作，整個 Event Loop 就會被卡住，所有其他的並行任務都將停滯
  anchor_type: 部落格判斷
  importance: 13
  status: normal
- id: c14
  role: evidence
  text: 兩者比較：Multi-Threading 的執行單位是 Thread、排程者是作業系統、搶佔式切換、每個執行緒有各自獨立的 OS Stack、狀態永遠存在各自的 Stack 中；Async 的執行單位是 Coroutine、排程者是應用程式層級的 Event Loop、協作式切換、所有協程共享同一個 Thread 的 Stack、暫停時狀態打包存回 Heap 上的協程物件；記憶體開銷與上下文切換成本都是 Multi-Threading 大、Async 小
  source_quotes:
  - 執行單位 | Thread (執行緒) | Coroutine (協程/任務)
  - 排程者 | 作業系統 (OS) | Event Loop (應用程式層級)
  - 切換方式 | Preemptive (搶佔式，OS 強制切換) | Cooperative (協作式，await 主動讓出)
  - Stack 管理 | 每個執行緒有各自獨立的 OS Stack。 | 所有協程共享同一個 Thread 的 Stack。
  - 狀態儲存 | 狀態永遠存在於各自的 Stack 中。 | 當協程暫停 (await)時，其狀態 (包含區域變數) 會被打包儲存回Heap 上的協程物件中。
  - 記憶體開銷 | 大 | 小
  - 上下為切換成本 | 大 | 小
  anchor_type: 背景說明
  importance: 14
  status: normal
```
