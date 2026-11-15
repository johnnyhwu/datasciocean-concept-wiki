---
id: thread-safe-not-async-safe-deadlock
title: Thread-Safe 不等於 Async-Safe：兩者要防的敵人不同，把用 threading.Lock 實作的 Thread-Safe 物件直接放進 async 程式碼，持有鎖時一 await 就可能凍結整個 Event Loop 而死鎖；threading 與 asyncio 的同步原語絕對不要混用
type_hint: 可遷移原則
context_type: standalone_classic
sources:
- article: fastapi-race-condition
  article_title: "FastAPI 的並行陷阱：從 Race Condition 到 Deadlock，徹底搞懂全域變數的正確用法"
  url: https://datasciocean.com/other/fastapi-race-condition/
  sections:
  - FastAPI 如何處理同步 (def) 與非同步 (async def) Endpoint?
  - Thread-Safe 與 Async-Safe 是等價的嗎?
  - Thread-Safe 與 Async-Safe 的敵人是誰?
  - "`threading.Lock` vs. `asyncio.Lock` 的運作機制"
  - "Deadlock: 在 Async 程式碼中加入 `threading.Lock`"
  - 最佳實踐
  first_appearance: true
parent: null
related:
  - shared-object-race-condition-mutable-state
  - async-vs-threading-io-bound-efficiency
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: Thread-Safe 和 Async-Safe 絕對不等價；一個典型的 Thread-Safe 實作如果直接用在 Async 的環境中，不僅不是安全的，反而會造成 Deadlock
  source_quotes:
  - 不，Thread-Safe 和 Async-Safe 絕對不等價
  - 更重要的是，一個典型的 Thread-Safe 實作，如果直接用在 Async 的環境中，不僅不是安全的，反而會造成 Deadlock。
  qualifiers:
  - text: blog 推導的死鎖情境是 Coroutine 在持有 threading.Lock 的情況下 await
    source_quote: "await asyncio.sleep(1) # <<--- 在持有 threading.Lock 的情況下 await"
  - text: 而且另一個 Coroutine 接著嘗試獲取同一個 threading.Lock
    source_quote: Coroutine B 執行到 with self._lock:，它嘗試獲取同一個 threading.Lock
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: 在 FastAPI 中，async def 定義的 Endpoint 在主事件迴圈（Main Event Loop）中直接執行，多個請求以 Cooperative Multitasking 的方式在同一個執行緒中交錯執行；def 定義的 Endpoint 則委派給一個獨立的 Thread Pool
  source_quotes:
  - FastAPI 會在主事件迴圈 (Main Event Loop) 中直接執行它。這意味著多個請求會以 Cooperative Multitasking 的方式，在同一個執行緒中交錯執行
  - FastAPI 會將這些同步函式的執行，委派給一個獨立的 Thread Pool。
  anchor_type: 背景說明
  importance: 2
  status: normal
- id: c3
  role: context
  text: 這是許多同時使用同步和非同步程式碼的開發者會遇到的陷阱
  source_quotes:
  - 這是一個極其重要的問題，也是許多同時使用同步和非同步程式碼的開發者會遇到的陷阱
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: Thread-Safe 的敵人是 Parallel Execution／Preemptive Multitasking：作業系統排程多個 Thread 時，一個 Thread 可能在任何時間點、任何指令之間被打斷並切換成另一個 Thread，多個 Thread 就可能同時讀寫同一塊記憶體而發生 Race Condition；武器是 Blocking Locks，例如 threading.Lock
  source_quotes:
  - 敵人：Parallel Execution / Preemptive Multitasking
  - 原因：當多個 Thread 由作業系統進行 Schedule 時，一個 Thread 在 CPU 上執行到一半時，可能在任何時間點、任何指令之間被打斷並切換為另外一個 Thread。此時，就有可能發生多個 Thread 對同一塊記憶體空間同時讀寫而發生 Race Condition
  - 武器：Blocking Locks，例如 threading.Lock
  anchor_type: 背景說明
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: Async-Safe 的敵人是 Blocking the Event Loop：Async 世界只有一個 Thread，任何一段程式碼佔用 CPU 不放或做了 Blocking I/O，整個 Event Loop 就會被卡住，所有其他並行任務都停滯；武器是 Non-blocking Operations 和 Cooperative Yielding，例如 asyncio.Lock 和 await
  source_quotes:
  - 敵人：Blocking the Event Loop
  - 原因：在 Async 世界裡，只有一個 Thread。如果任何一段程式碼佔用 CPU 不放，或者進行了 Blocking I/O 操作，整個 Event Loop 就會被卡住，所有其他的並行任務都將停滯
  - 武器：Non-blocking Operations 和Cooperative Yielding，例如 asyncio.Lock 和 await
  anchor_type: 背景說明
  importance: 5
  status: normal
- id: c6
  role: mechanism
  text: threading.Lock 的 acquire()：Lock 可用就立即獲得；Lock 已被其他 Thread 持有時，會讓當前的 Thread 進入睡眠或阻塞狀態，作業系統把這個 Thread 掛起直到 Lock 被釋放
  source_quotes:
  - 當一個執行緒呼叫 acquire() 時，如果 Lock 是可用的，它會立即獲得 Lock 並繼續執行
  - 如果 Lock 已經被其他 Thread 持有，它會讓當前的 Thread 進入「睡眠」或「阻塞」狀態。作業系統會將這個 Thread 掛起，直到 Lock 被釋放。
  anchor_type: 背景說明
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: await asyncio.Lock.acquire()：Lock 可用就立即獲得；Lock 已被其他 Coroutine 持有時，不會阻塞 Thread，而是把自己註冊為在等待這個 Lock，並主動將控制權交還給 Event Loop，Event Loop 再去執行其他已經就緒的 Coroutine
  source_quotes:
  - 當一個 Coroutine await 一個 acquire() 時，如果 Lock 是可用的，它會立即獲得鎖並繼續執行
  - 如果 Lock 已經被其他 Coroutine 持有，它不會阻塞 Thread。相反地，它會：
  - 將自己註冊為在等待這個 Lock
  - 主動將控制權交還給 Event Loop。
  - Event Loop 在收到控制權後，會去執行其他已經就緒的 Coroutine
  anchor_type: 背景說明
  importance: 7
  status: normal
- id: c8
  role: anchor
  text: 死鎖例子的前半：DangerousRetriever 在 async 方法裡用 threading.Lock 包住整段邏輯，並在持有這把鎖的情況下 await asyncio.sleep(1)（模擬非同步 I/O）；Coroutine A 取得鎖後執行到 await，把控制權交還給 Event Loop，Event Loop 接著執行已就緒的 Coroutine B
  source_quotes:
  - 現在，讓我們把一個用 threading.Lock 實現的 Thread-Safe 物件放到 async def Endpoint 中，看看會發生什麼!
  - "await asyncio.sleep(1) # <<--- 在持有 threading.Lock 的情況下 await"
  - 它成功獲取了 self._lock (一個 threading.Lock)
  - 它執行到 await asyncio.sleep(1)。await 的語意是「暫停我，把控制權交還給 Event Loop」
  - Event Loop收回控制權，發現Coroutine B (process_query_async("B")) 已經就緒，於是開始執行 Coroutine B
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 8
  status: normal
- id: c9
  role: anchor
  text: 死鎖例子的後半：Coroutine B 嘗試獲取同一個 threading.Lock，因為 A 仍持有而阻塞；這是作業系統層級的執行緒阻塞，凍結了 Event Loop 所在的唯一執行緒，整個應用程式被凍結，Event Loop 無法再排程任何任務、無法喚醒 A；A 永遠無法執行到釋放 Lock 的那一行，B 永遠拿不到鎖，形成 Deadlock
  source_quotes:
  - Coroutine B 執行到 with self._lock:，它嘗試獲取同一個 threading.Lock
  - 因為 Coroutine A 仍然持有這個鎖，所以 Coroutine B 的 acquire() 呼叫阻塞了
  - 關鍵點：threading.Lock 的阻塞是作業系統層級的執行緒阻塞。它凍結了 Event Loop 所在的唯一執行緒。
  - 現在，整個應用程式被凍結了。事件迴圈無法再排程任何任務。它無法喚醒 asyncio.sleep(1) 結束後的 Coroutine A。
  - Coroutine A 永遠無法執行到釋放 Lock 的那一行，因為 Event Loop 已經被 Coroutine B 阻塞了。Coroutine B 永遠無法獲得鎖，因為 Coroutine A 永遠無法釋放它。
  - Deadlock
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 9
  status: normal
- id: c10
  role: evaluation
  text: 隔離原則：threading 模組的同步原語（Lock、Event、Semaphore 等）是為 Multi-Thread 環境設計的，asyncio 模組的同步原語是為 Single-Thread 的協程環境設計的，絕對不要混用
  source_quotes:
  - 隔離原則：threading 模組中的同步原語（Lock, Event, Semaphore 等）是為 Multi-Thread 環境設計的；asyncio 模組中的同步原語是為 Single-Thread 的協程環境設計的。絕對不要混用它們。
  anchor_type: 部落格判斷
  importance: 10
  status: normal
- id: c11
  role: evaluation
  text: 為非同步程式碼選擇非同步的工具，為同步程式碼選擇同步的工具，blog 稱這是確保應用程式穩定運行的黃金法則
  source_quotes:
  - 總之，請務必記住：Thread-Safe ≠ Async-Safe。為非同步程式碼選擇非同步的工具，為同步程式碼選擇同步的工具，這是確保應用程式穩定運行的黃金法則。
  anchor_type: 部落格判斷
  importance: 11
  status: normal
```
