---
id: shared-object-race-condition-mutable-state
title: 多個 Request 共用同一個全域物件不一定會有 Race Condition，關鍵在物件內部有沒有 Shared Mutable State；最推薦的做法是讓物件 Stateless，Lock 與每個請求新建物件都有代價
type_hint: 可遷移原則
context_type: standalone_classic
sources:
- article: fastapi-race-condition
  article_title: "FastAPI 的並行陷阱：從 Race Condition 到 Deadlock，徹底搞懂全域變數的正確用法"
  url: https://datasciocean.com/other/fastapi-race-condition/
  sections:
  - 前言
  - FastAPI 如何處理同步 (def) 與非同步 (async def) Endpoint?
  - Request 之間的共享物件一定會發生 Race Condition 嗎?
  - "安全情況: Stateless 或是只有 Read-only State 的 Retriever"
  - "危險情況: 有 Shared Mutable State 的 Retriever"
  - 實作 Stateless Object
  - 使用 Threading Lock
  - 為每個 Request 初始化新的 Object
  - 讓一個 Function/Method 是 Thread-Safe 且 Async-Safe 的黃金守則?
  - 追求純函式與無狀態 (Statelessness) - 黃金法則
  - 使用不可變狀態 (Immutability)
  - 將狀態管理外部化 (Externalize State Management)
  - 最佳實踐
  - "危險情況: 類別中定義了類別屬性 (Class Attributes)"
  first_appearance: true
parent: null
related:
  - local-variables-isolated-stack-and-coroutine
  - async-vs-threading-io-bound-efficiency
  - thread-safe-not-async-safe-deadlock
  - python-module-import-separate-instances
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 不同的 Request 共用同一個全域變數（例如一個 retriever 物件）時，會不會發生 Race Condition 的關鍵在於這個物件的 Class 內部是否有 Shared Mutable State
  source_quotes:
  - 在 retriever 變數被所有 Request 共享的情況下，就一定會發生 Race Condition 嗎?
  - "會不會發生 Race Condition 的關鍵在於: Retriever Class 內部是否有 Shared Mutable State?"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: 情境是用 FastAPI 建 AI 服務的 PoC Server：有些時候 AI 服務的初始化需要時間，沒辦法每個 Request 都重新初始化，這時可能會事先把它初始化成一個全域變數，讓所有 Request 透過 Endpoint 存取同一個全域變數
  source_quotes:
  - 在做 AI 服務的 PoC 開發時，我們經常會透過 FastAPI 來建立一個 Server
  - 有些時候，由於 AI 服務的初始化 (將抽象的 AI 服務初始化程式中的實體物件) 需要時間，我們沒有辦法針對每個 Request 都重新初始化一個全新的 AI 服務 (物件)。在這樣的情況下，我們可能會事先將 AI 服務初始化為一個全域變數，讓所有的 Request 都可以透過 Endpoint 來存取同一個全域變數
  anchor_type: 部落格舉例
  importance: 2
  status: normal
- id: c3
  role: context
  text: FastAPI 對 async def 定義的 Endpoint，會在主事件迴圈（Main Event Loop）中直接執行，多個請求以 Cooperative Multitasking 的方式在同一個執行緒中交錯執行；對 def 定義的 Endpoint，為了避免它阻塞整個服務，會把執行委派給一個獨立的 Thread Pool
  source_quotes:
  - 如果將 Endpoint 定義為 async def，那麼這個 Endpoint 就是一個 Asynchronous Endpoint，FastAPI 會在主事件迴圈 (Main Event Loop) 中直接執行它。這意味著多個請求會以 Cooperative Multitasking 的方式，在同一個執行緒中交錯執行
  - 當 FastAPI 直接在主事件迴圈中執行它，將可能會阻塞整個服務 (e.g. 當這個 Endpoint 會進行 I/O Blocking 或是 CPU Intensive 的運算)，使其無法回應其他請求。為了避免這種情況，FastAPI 會將這些同步函式的執行，委派給一個獨立的 Thread Pool。
  qualifiers:
  - text: def Endpoint 直接在主事件迴圈執行時是「可能」阻塞整個服務，例子是 Endpoint 會做 I/O Blocking 或 CPU Intensive 的運算
    source_quote: 將可能會阻塞整個服務 (e.g. 當這個 Endpoint 會進行 I/O Blocking 或是 CPU Intensive 的運算)
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: context
  text: 無論 Endpoint 是 Synchronous 還是 Asynchronous，不同的 Request 都會存取到相同的全域變數
  source_quotes:
  - 可以發現到，無論是 Synchonous 還是 Asynchronous，不同的 Request 都會存取到相同的全域變數 retriever。
  anchor_type: 背景說明
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 安全情況：如果方法執行的所有操作，要嘛基於傳入的參數，要嘛基於初始化後就不再改變的實例變數，沒有修改任何 self.xxx 的屬性，那麼就算 100 個執行緒同時呼叫它，也只是在讀取共享資料，不會互相干擾，是執行緒安全的（Thread-Safe），不會有 Race Condition
  source_quotes:
  - 在這個例子中，__call__ 方法執行的所有操作，要嘛是基於傳入的參數 (query)，要嘛是基於初始化後就不再改變的實例變數 (self._model)。它沒有修改任何 self.xxx 的屬性。因此，就算 100 個執行緒同時呼叫它，它們也只是在讀取共享資料，而不會互相干擾。這種情況是執行緒安全的 (Thread-Safe)，不會有 Race Condition。
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 假設題設
  importance: 5
  status: normal
- id: c6
  role: anchor
  text: 危險情況一：self.request_count += 1 是典型的 Read-Modify-Write 操作，不是原子操作（Atomic Operation）；兩個執行緒可能同時讀到值是 5，各自加 1 後都寫回 6，計數器就少算了一次
  source_quotes:
  - "self.request_count += 1: 這是一個典型的 Read-Modify-Write 操作，它不是一個原子操作 (Atomic Operation)。兩個執行緒可能同時讀取到 self.request_count 的值是 5，然後各自加 1，最後都寫回 6。結果計數器就少算了一次。"
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 6
  status: normal
- id: c7
  role: anchor
  text: 危險情況二：在共享的 self.cache 上，兩個執行緒可能同時判斷 query 不在快取中，然後都去執行耗時的查詢，最後都嘗試寫入快取，造成資源浪費
  source_quotes:
  - "self.cache: 兩個執行緒可能同時判斷 query 不在快取中，然後都去執行耗時的查詢，最後都嘗試寫入快取。這不僅會造成資源浪費，在更複雜的邏輯下還可能導致資料不一致。"
  qualifiers:
  - text: 資料不一致是「在更複雜的邏輯下還可能」發生，不是這個例子必然的結果
    source_quote: 在更複雜的邏輯下還可能導致資料不一致
  anchor_type: 部落格舉例
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: 避免 Race Condition 最乾淨、最推薦的架構是讓 Class 本身變得 Stateless：把快取移到 Redis 這類外部服務、把計數或監控交給 Prometheus 這類監控系統、資料庫連線不在類別中長期持有而是透過 FastAPI 的依賴注入在每次請求時獲取
  source_quotes:
  - 這是最乾淨、最推薦的架構。盡量讓 Class 本身 (e.g. Retriever) 變得 Stateless。
  - 移除快取：將快取邏輯移到專門的外部服務，如 Redis。Redis 本身是原子操作的，可以安全地處理並行存取。
  - 移除計數器：將計數或監控邏輯交給專門的監控系統 (如 Prometheus)。
  - 依賴注入：如果需要連線物件 (如資料庫連線)，不要在類別中長期持有，而是透過 FastAPI 的依賴注入系統，在每次請求時獲取一個連線。
  anchor_type: 部落格判斷
  importance: 8
  status: normal
- id: c9
  role: mechanism
  text: 如果必須在物件內部維護可變的狀態，最直接的方法是用 Lock 建立 Critical Section，把存取共享物件的程式碼包在裡面；示範的寫法把耗時操作移出鎖的範圍，避免阻塞其他執行緒太久，寫入快取前再次檢查
  source_quotes:
  - 如果必須在物件內部維護一個可變的狀態，那麼最直接的方法就是使用 Lock 來建立 Critical Section，來把對共享物件的存取的程式碼包在 Critical Section 當中
  - "# 將耗時操作移出鎖的範圍，避免阻塞其他執行緒太久"
  - "# 再次檢查，可能在我們查詢的期間，已有其他執行緒放入結果"
  qualifiers:
  - text: 這裡示範的 Lock 是 threading.Lock；blog 後文說 threading 模組的同步原語是為 Multi-Thread 環境設計的，asyncio 的同步原語是為 Single-Thread 的協程環境設計的，絕對不要混用
    source_quote: 隔離原則：threading 模組中的同步原語（Lock, Event, Semaphore 等）是為 Multi-Thread 環境設計的；asyncio 模組中的同步原語是為 Single-Thread 的協程環境設計的。絕對不要混用它們。
  anchor_type: 背景說明
  importance: 9
  status: normal
- id: c10
  role: evaluation
  text: Lock 直接解決了 Race Condition，但會降低並行效能（一次只有一個執行緒能進入臨界區）；鎖的範圍太大（例如鎖住整個 I/O 操作）會使多執行緒失去意義；還可能引入死鎖（Deadlock）的風險
  source_quotes:
  - "優點: 直接解決了 Race Condition"
  - 會降低並行效能，因為一次只有一個執行緒能進入臨界區
  - 如果鎖的範圍太大（例如鎖住了整個 I/O 操作），會使多執行緒失去意義
  - 可能會引入死鎖 (Deadlock) 的風險
  qualifiers:
  - text: 這裡示範的 Lock 是 threading.Lock；blog 後文說 threading 模組的同步原語是為 Multi-Thread 環境設計的，asyncio 的同步原語是為 Single-Thread 的協程環境設計的，絕對不要混用
    source_quote: 隔離原則：threading 模組中的同步原語（Lock, Event, Semaphore 等）是為 Multi-Thread 環境設計的；asyncio 模組中的同步原語是為 Single-Thread 的協程環境設計的。絕對不要混用它們。
  anchor_type: 部落格判斷
  importance: 10
  status: normal
- id: c11
  role: evaluation
  text: 用 FastAPI 的依賴注入為每個請求建立全新的物件，完全隔離、不會有 Race Condition；但如果初始化非常耗時（例如要載入幾 GB 的大模型），每個請求都重建會是巨大的效能災難，只適用於物件建立成本極低的情況
  source_quotes:
  - 也可以利用 FastAPI 的依賴注入系統 (Dependency Injection) 來為每一個請求建立一個全新的 Retriever 物件
  - "優點: 完全隔離，絕對不會有 Race Condition，因為每個請求都有自己的 retriever 物件。"
  - 如果 Retriever() 的初始化過程非常耗時（例如需要載入一個幾 GB 的大模型），那麼為每個請求都重新建立一次物件將會是巨大的效能災難。這種方法只適用於物件建立成本極低的情況。
  qualifiers:
  - text: 隔離的是實例屬性；blog 另一處說同一個類別建立的實例仍共享類別屬性，修改這個共享的類別屬性會導致 Race Condition
    source_quote: 如果在 Retriever 類別中定義了類別屬性，那麼這個屬性將會被 instance_A 和 instance_B 共享！…都會修改同一個 Retriever.total_requests_processed 變數，這將會導致跨端點的 Race Condition。
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 假設題設
  importance: 11
  status: normal
- id: c12
  role: evaluation
  text: 要寫出同時 Thread-Safe 和 Async-Safe 的程式碼，心態應該從「我該用哪個鎖?」轉變為「我如何才能完全避免用鎖?」，答案幾乎總是消除 Shared Mutable State；遵循這個核心原則，程式碼會變得更簡單、更能適應各種並行模型
  source_quotes:
  - 要寫出同時 Thread-Safe 和 Async-Safe 的程式碼，你的心態應該從「我該用哪個鎖?」轉變為「我如何才能完全避免用鎖?」。答案幾乎總是：消除 Shared Mutable State。遵循這個核心原則，程式碼將會變得更簡單、更能適應各種並行模型
  anchor_type: 部落格判斷
  importance: 12
  status: normal
- id: c13
  role: mechanism
  text: 黃金法則是追求純函式與無狀態：如果函式的輸出完全由輸入決定，就沒有任何需要保護的東西；做法是不讀寫全域變數或實例屬性（self.xxx）、所有資料透過參數明確傳入、不修改傳入的物件而是返回新物件；blog 的範例函式 process_data 只依賴傳入的參數、返回全新的物件，blog 說它無論被 100 個 Thread 還是 100 個 Coroutine 同時呼叫，永遠都是安全的
  source_quotes:
  - 這是最重要、最有效的一條。如果一個函式或方法沒有狀態，或者說它的輸出完全由其輸入決定，那麼它就沒有任何需要保護的東西。
  - 函式不應讀取或寫入任何全域變數或其類別的實例屬性 (self.xxx)
  - 所有需要的資料都應該透過函式參數明確傳入
  - 函式不應有 Side Effects，例如修改傳入的物件（除非是返回一個新的物件）
  - "def process_data(data: dict, config: dict) -> dict:"
  - "# 只依賴傳入的參數"
  - "# 返回一個全新的物件，而不是修改原始的 data"
  - 這個函式無論被 100 個 Thread 還是 100 個 Coroutine 同時呼叫，永遠都是安全的。
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 假設題設
  importance: 13
  status: normal
- id: c14
  role: mechanism
  text: 如果必須要有狀態，就讓它不可變：用 tuple 取代 list、frozenset 取代 set、dataclasses 設定 frozen=True，需要「修改」時建立新物件而不是原地修改
  source_quotes:
  - 如果必須要有狀態，那就讓它成為不可變的。一旦建立，就不能修改。
  - 使用元組 (tuple) 而不是列表 (list)
  - 使用 frozenset 而不是 set
  - 使用 dataclasses 並設定 frozen=True
  - 如果需要「修改」，那就建立一個新的物件而不是在原地修改。
  qualifiers:
  - text: 示範中 self._config 這個參考本身仍可被指向另一個物件，安全的是 AppConfig 這個不可變物件本身
    source_quote: "# 雖然可以讓 self._config 指向另一個物件，但 AppConfig 本身是安全的"
  anchor_type: 部落格判斷
  importance: 14
  status: normal
- id: c15
  role: mechanism
  text: 將狀態管理外部化：不在應用程式記憶體中自己管理複雜的共享狀態，而是交給專門為並行設計的外部服務，例如快取改用 Redis（blog 說它的 SET、GET 是原子性的）、任務佇列改用 RabbitMQ 或 Celery、資料儲存依賴資料庫的交易與行級鎖
  source_quotes:
  - 不要在你的應用程式記憶體中自己管理複雜的共享狀態，而是將這個責任交給專門為並行而設計的外部服務。
  - 快取 (Caching)：不要用 self.cache = {}，改用 Redis。Redis 的操作（如 SET, GET）是原子性的，天生就是為高並行場景設計的。
  - 任務佇列 (Task Queues)：不要用 self.tasks = []，改用 RabbitMQ 或 Celery。
  - 資料儲存 (Data Storage)：使用資料庫，並依賴其提供的交易 (Transactions) 和行級鎖 (Row-level Locking) 來保證資料一致性。
  anchor_type: 部落格判斷
  importance: 15
  status: normal
```
