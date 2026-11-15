---
id: local-variables-isolated-stack-and-coroutine
title: 不論多執行緒還是 async，方法裡的區域變數都不會發生 Race Condition：多執行緒時每個 Thread 有自己的 Stack；async 時只有一個 Stack，但 Coroutine 在 await 時把狀態存回自己在 Heap 上的物件，Stack 上只會有正在執行的那一個
type_hint: 方法
context_type: standalone_classic
sources:
- article: fastapi-race-condition
  article_title: "FastAPI 的並行陷阱：從 Race Condition 到 Deadlock，徹底搞懂全域變數的正確用法"
  url: https://datasciocean.com/other/fastapi-race-condition/
  sections:
  - (Multi-Thread 情況) 不同 Request 同時讀寫共享物件中的區域變數會有 Race Condition?
  - Stack Memory 與 Heap Memory
  - 實際範例
  - (Single Thread 情況) 不同 Request 同時讀寫共享物件中的區域變數會有 Race Condition?
  - Async 的核心：Coroutine 不是函式，而是物件
  - Event Loop 的角色：可以 Concurrently 下很多盤棋的棋藝大師
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
  text: 不同 Request 同時執行共享物件的同一個 Method 時，Method 中的區域變數（Local Variable）本身不會發生 Race Condition；在 def 定義的多執行緒情況下不會，在 async def 定義的單一執行緒情況下依然不會
  source_quotes:
  - 不會，Method 中的 Local Variable (區域變數) 本身絕對不會發生 Race Condition
  - 不會，在 Async 的情況下，不同 Request 的區域變數依然不會發生 Race Condition
  qualifiers:
  - text: 不會衝突的是區域變數本身；它們讀取共享 Heap 上的資料（例如 self._model）時，要那個操作是 Read-Only 的才不會產生衝突
    source_quote: 雖然它們都讀取了位於共享 Heap 上的 self._model，但只要這個操作是 Read-Only 的，就不會產生任何衝突。
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: 情境是 FastAPI Server：Endpoint 用 def 定義時，每個新的 Request 由 Thread Pool 中的一個 Thread 處理；用 async def 定義時，不同的 Request 都由同一個 Thread 處理
  source_quotes:
  - 我們先假設目前的 Endpoint 是一個透過 def 所定義的 Synchronous Function，因此每當 FastAPI Server 接收到新的 Request 時，就會從 Thread Pool 中抓出一個 Thread 來處理這個 Request。
  - 假設目前的 Endpoint 是一個透過 async def 所定義的 Asynchronous Function，因此每當 FastAPI Server 接收到新的 Request 時，都是由同一個 Thread 在處理不同的 Request
  anchor_type: 背景說明
  importance: 2
  status: normal
- id: c3
  role: context
  text: 作業系統把 Program 載入 RAM 成為 Process 時，Process 的記憶體包含 Stack 與 Heap：Stack 是每個 Thread 被建立時分配到的專屬、獨立的記憶體空間；Heap 是 Process 內所有 Thread 共享的記憶體區域，用來存 Class Attributes、Global Variables 這類生命週期更長、需要被共享的資料
  source_quotes:
  - 當作業系統把一個 Program 載入到 RAM 中成為一個 Process 時，這個 Process 的記憶體包含了 Stack 與 Heap 兩種記憶體
  - 特性：每個 Thread 在被作業系統建立時，都會被分配一塊自己專屬、獨立的記憶體空間，這就是該執行緒的 Stack
  - 特性：這是一塊由 Process 內的所有 Thread 共享的記憶體區域
  - 用途：用來儲存生命週期更長、需要被共享的資料。這包括：
  - Class Attributes
  - Global Variables
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 函式或方法被呼叫時，會在該 Thread 的 Stack 上建立一個 Stack Frame，存放 Function Parameters、Function Local Variables 與 Return Address；函式執行完畢時 Stack Frame 自動銷毀，其中的區域變數也隨之消失
  source_quotes:
  - 用途：當一個函式或方法被呼叫時，會在該 Thread 的 Stack 上建立一個 Stack Frame。這個 Stack Frame 用來儲存所有屬於這個函式呼叫的資訊，包括：
  - Function Parameters
  - Function Local Variables
  - Return Address (函式執行完後要跳回哪裡)
  - Life Cycle：當函式執行完畢時，這個 Stack Frame 會被自動銷毀，其中的所有區域變數也隨之消失
  anchor_type: 背景說明
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 多執行緒時，多個 Thread 雖然同時執行同一份程式碼（同一個 Method），但它們的 Local Variable 在記憶體中是隔離的，所以不會發生 Race Condition
  source_quotes:
  - 雖然多個 Thread 同時在執行同一份程式碼 (同一個 Method)，但它們的 Local Varaible 在記憶體中是隔離的，因此才不會發生 Race Condition。
  anchor_type: 背景說明
  importance: 5
  status: normal
- id: c6
  role: anchor
  text: 例子：全域的 retriever 物件與它的 self._model 屬性存在共享的 Heap；Thread A 呼叫 retriever(query="貓")、Thread B 同時呼叫 retriever(query="狗")，各自在自己的 Stack 上建立完全獨立的 Stack Frame，裡面分別是 query = "貓" 與 query = "狗" 等變數；Thread A 完全無法存取 Thread B Stack 上的任何資料，反之亦然
  source_quotes:
  - retriever Object 本身是一個 Global Variable`，因此會被存在 Heap Memory 中。
  - "# `self._model` 這個屬性也跟著物件存在於 Heap 中 (共享)"
  - 'Thread A 呼叫 retriever(query="貓"):'
  - '這個 Frame 裡面有 query = "貓"，process_log = "Processing query: 貓" 等變數。'
  - 'Thread B 同時呼叫 retriever(query="狗"):'
  - 在 Thread B 的 Stack 上建立一個完全獨立的 Stack Frame
  - '這個 Frame 裡面有 query = "狗"，process_log = "Processing query: 狗" 等變數。'
  - 關鍵點：Thread A 完全無法存取 Thread B Stack 上的任何資料，反之亦然。
  qualifiers:
  - text: 兩個 Thread 都讀取共享 Heap 上的 self._model，只要這個操作是 Read-Only 的就不會產生衝突
    source_quote: 雖然它們都讀取了位於共享 Heap 上的 self._model，但只要這個操作是 Read-Only 的，就不會產生任何衝突。
  anchor_type: 部落格舉例
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: 呼叫 def 函式會立即執行並在 Stack 上建立 Stack Frame；呼叫 async def 函式則不會立即執行，而是回傳一個 Coroutine Object
  source_quotes:
  - 當我們呼叫一個 def 函式時，它會立即執行，並在 Stack 上建立一個 Stack Frame。
  - 然而，當我們呼叫一個 async def 函式時，它不會立即執行。相反地，它會回傳一個 Coroutine Object。
  anchor_type: 背景說明
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: Coroutine Object 本質上是一個 Stateful Generator，可以想像成「可暫停的函式」，打包了要執行的程式碼、所有的 Local Variables、以及執行到哪一行的指標（Instruction Pointer）；這些 Coroutine Object 存放在所有 Thread 共享的 Heap 記憶體中
  source_quotes:
  - 這個 Coroutine Object，本質上是一個Stateful Generator。可以把它想像成一個「可暫停的函式」，它打包了執行該函式所需的一切資訊：
  - 要執行的程式碼
  - 它所有的 Local Variables
  - 它執行到哪一行的指標 (Instruction Pointer)
  - 這些 Coroutine Object 本身是存放在 Heap 記憶體中的，也就是所有 Thread 共享的那個區域。
  anchor_type: 背景說明
  importance: 8
  status: normal
- id: c9
  role: anchor
  text: 類比：Event Loop 像一位棋藝大師，每個進來的 Request 產生一個 Coroutine Object，就像一盤新的棋局；大師在多個棋盤之間是 Concurrently 而非 Parallely 地下棋
  source_quotes:
  - 想像一下 Event Loop 是位棋藝大師，而每一個進來的 Request 都會產生一個 Coroutine Object，就像是一盤新的棋局。
  - 這也就說明了棋藝大師是 Concurrently 而非 Parallely 的在多個棋盤之間下棋
  anchor_type: 部落格舉例
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: Event Loop 開始執行 Coroutine_A 時，把它的初始狀態（參數、區域變數）載入到唯一的 Thread 的 Stack 上
  source_quotes:
  - 它將 Coroutine_A 的初始狀態（參數、區域變數）載入到唯一的 Thread 的 Stack 上，開始「下棋」
  anchor_type: 背景說明
  importance: 10
  status: normal
- id: c11
  role: mechanism
  text: await 的語意是「暫停我目前的執行，並將控制權交還給 Event Loop」；暫停前，Coroutine_A 把所有當前狀態（區域變數的值、停在哪一行）完整地儲存回它在 Heap 裡的物件，然後從 Thread Stack 中被移除
  source_quotes:
  - await 的語意是：「暫停我目前的執行，並將控制權交還給 Event Loop」
  - 在暫停前，Coroutine_A 會將它所有的當前狀態（包括它所有區域變數的值、它停在哪一行）完整地儲存回它自己的物件中 (那個在 Heap 裡的 Coroutine_A 物件)
  - 然後，它會從 Thread Stack 中被移除。
  anchor_type: 背景說明
  importance: 11
  status: normal
- id: c12
  role: mechanism
  text: Event Loop 接著把 Coroutine_B 的狀態載入到同一個 Thread Stack 上為 Request B 服務；A 的 I/O 完成後，在下一個適當時機（例如 Coroutine_B 也遇到 await 或執行完畢），Event Loop 從 Coroutine_A 物件把先前儲存的狀態還原到 Thread Stack 上，從 await 的下一行繼續執行
  source_quotes:
  - 它將 Coroutine_B 的狀態載入到同一個 Thread Stack 上，開始為 Request B 服務
  - 在下一個適當的時機 (例如 Coroutine_B 也遇到了 await 或執行完畢)，Event Loop 會再次回到棋盤 A。
  - 它會從 Coroutine_A 物件中，將先前儲存的所有狀態（包括所有區域變數）完美地還原到 Thread Stack 上，然後從 await 的下一行繼續執行。
  anchor_type: 背景說明
  importance: 12
  status: normal
- id: c13
  role: mechanism
  text: 所以 async 時不同 Request 的區域變數雖然共用同一個 Stack，也不會發生 Race Condition：在任何一個時間點，Stack 上只會有當前正在執行的那一個 Coroutine 的資料，不同 Coroutine 的資料透過 Heap 上的物件隔離儲存，永遠不會同時出現在堆疊上
  source_quotes:
  - 這樣不同的 Request 的區域變數都會存在同一個 Stack 中, 而發生 Race Condition 嗎？
  - 不會。因為在任何一個時間點，Stack 上只會有當前正在執行的那一個 Coroutine 的資料。不同 Coroutine 的資料是透過在 Heap 上的物件進行隔離儲存的，它們永遠不會同時出現在堆疊上，因此不可能發生衝突或 Race Condition。
  anchor_type: 部落格推論
  importance: 13
  status: normal
```
