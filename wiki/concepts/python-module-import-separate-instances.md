---
id: python-module-import-separate-instances
title: 兩個 Python 檔案各自 import 同一個類別再各自初始化，得到的是兩個完全獨立的實例，因為 sys.modules 只快取模組、不會讓實例共用；但類別屬性仍被所有實例共享，會造成跨端點的 Race Condition；更好的做法是集中建立唯一的共享實例
type_hint: 方法
context_type: standalone_classic
sources:
- article: fastapi-race-condition
  article_title: "FastAPI 的並行陷阱：從 Race Condition 到 Deadlock，徹底搞懂全域變數的正確用法"
  url: https://datasciocean.com/other/fastapi-race-condition/
  sections:
  - 同一個類別被載入到不同的文件中並初始化為相同的全域變數
  - Python 的模組匯入與快取機制
  - "危險情況: 類別中定義了類別屬性 (Class Attributes)"
  - 最佳實作方式
  - 集中化依賴管理
  - Request 之間的共享物件一定會發生 Race Condition 嗎?
  first_appearance: true
parent: null
related:
  - shared-object-race-condition-mutable-state
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 多個 Python 檔案共用一個類別、各自初始化出同名的全域變數（例如 endpoint_a.py 與 endpoint_b.py 各自 retriever = Retriever()），兩個 retriever 物件實際上完全獨立，對 A 的請求和對 B 的請求使用不同的物件，實例屬性（self.xxx）完全隔離
  source_quotes:
  - "現在，讓我們來思考以下情境: 多個 Python 文件共用一個類別並初始化出相同的全域變數"
  - 完全不會! 兩個 retriever Object 實際上是完全獨立的。一個在 endpoint_a 模組的全域範圍中，另一個在 endpoint_b 模組的全域範圍中。因此，對 A 的請求和對 B 的請求會使用不同的物件，它們之間的實例屬性 (self.xxx) 是完全隔離的。
  qualifiers:
  - text: 例外是類別屬性：類別中定義的類別屬性會被兩個實例共享
    source_quote: 如果在 Retriever 類別中定義了類別屬性，那麼這個屬性將會被 instance_A 和 instance_B 共享！
  - text: 隔離的是 A 與 B 之間；Race Condition 問題依然存在，只是被侷限在各自的 Endpoint 內
    source_quote: 我們之前討論的 Race Condition 問題依然存在，只是被侷限在了各自的 Endpoint 內
  anchor_type: 背景說明
  importance: 1
  status: normal
- id: c2
  role: context
  text: 情境是 FastAPI Server 的多個 Endpoint 檔案：先前討論的是多個 Request 共用一個全域變數，這裡問的是兩個 Request 同時分別執行 Endpoint A 與 B（不管透過 Multi-Threading 或 Async）會發生什麼
  source_quotes:
  - 在前面的例子中, 我們聚焦在多個 Request 共用一個全域變數的情況
  - 當 FastAPI Server 啟動時 (e.g. uvicorn main:app)，它會開始匯入程式碼。
  - 當兩個 Request 同時分別的執行 (不管透過 Multi-Threading 或 Async) Endpoint A 與 B 此時會發生什麼事情嗎?
  anchor_type: 部落格舉例
  importance: 2
  status: normal
- id: c3
  role: mechanism
  text: 理解這個行為的關鍵不在 FastAPI，而在 Python 本身 import 的運作原理：Python 維護一個名為 sys.modules 的 Global Dictionary 當作模組的快取
  source_quotes:
  - 要理解這個行為，關鍵其實不在 FastAPI，而在於 Python 本身的 import 的運作原理。
  - Python 會維護著一個名為 sys.modules 的 Global Dictionary，它扮演著模組的快取角色。
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 第一次遇到 import src 或 from src import Retriever 時，Python 檢查 sys.modules 中有沒有 'src'，沒有就找到 src.py、執行裡面的所有程式碼，再把模組物件存入 sys.modules['src']；之後在另一個檔案再次遇到時，直接從快取取出該模組物件，不會再次執行 src.py
  source_quotes:
  - 當第一次遇到 import src 或 from src import Retriever 時，Python 會：
  - a. 檢查 sys.modules 中是否已經有 'src'
  - b. 如果沒有，它會找到 src.py 檔案，執行裡面的所有程式碼，然後將建立的模組物件存入 sys.modules['src']
  - 當之後在另一個檔案中再次遇到 import src 或 from src import Retriever 時，Python 會發現 'src' 已經在 sys.modules 中了，於是它會直接從快取中取出該模組物件，而不會再次執行 src.py 檔案
  anchor_type: 背景說明
  importance: 4
  status: normal
- id: c5
  role: anchor
  text: 啟動流程：主應用程式 import endpoint_a 時，第一次遇到 from src import Retriever，Python 執行 src.py 並快取 src 模組；接著 retriever = Retriever() 這行被執行，建立一個 Retriever 實例（instance_A），賦值給 endpoint_a 模組內的全域變數 retriever
  source_quotes:
  - 主應用程式 import endpoint_a
  - 遇到 from src import Retriever。因為是第一次，Python 執行 src.py 並快取 src 模組。Retriever 類別被載入記憶體
  - 遇到 retriever = Retriever()。這行程式碼被執行，一個 Retriever 的實例被建立（我們稱之為 instance_A），並賦值給 endpoint_a 模組內的全域變數 retriever。
  anchor_type: 部落格舉例
  importance: 5
  status: normal
- id: c6
  role: anchor
  text: 接著主應用程式 import endpoint_b：這次 Python 在 sys.modules 找到 src 模組，直接從快取取出 Retriever 類別，src.py 不會再次執行；但 retriever = Retriever() 這行也被執行，呼叫同一個 Retriever 類別的建構函式，建立一個全新的、獨立的實例（instance_B），賦值給 endpoint_b 模組內的全域變數 retriever
  source_quotes:
  - 主應用程式接著 import endpoint_b。
  - 遇到 from src import Retriever。這次 Python 在 sys.modules 中找到了 src 模組，直接從快取中取出 Retriever 類別。src.py 不會再次執行。
  - 遇到 retriever = Retriever()。這行程式碼也被執行，它呼叫了同一個 Retriever 類別的建構函式，建立了一個全新的、獨立的 Retriever 實例（我們稱之為 instance_B），並賦值給 endpoint_b 模組內的全域變數 retriever。
  anchor_type: 部落格舉例
  importance: 6
  status: normal
- id: c7
  role: anchor
  text: 因為是兩個不同的物件實例，如果 instance_A 內部有一個計數器 self.count，它的改變完全不會影響到 instance_B 的 self.count
  source_quotes:
  - 因為它們是兩個不同的物件實例，所以它們各自的實例屬性 (self.xxx) 是完全隔離的。如果 instance_A 內部有一個計數器 self.count，它的改變完全不會影響到 instance_B 的 self.count。
  anchor_type: 部落格舉例
  importance: 7
  status: normal
- id: c8
  role: qualifier
  text: 先前討論的 Race Condition 問題依然存在，只是被侷限在各自的 Endpoint 內：多個同時對 A 的 Request 共享 instance_A，可能在 instance_A 內部產生 Race Condition，對 B 亦然；但 A 的 Request 和 B 的 Request 之間不會因為 retriever 物件而互相干擾
  source_quotes:
  - 我們之前討論的 Race Condition 問題依然存在，只是被侷限在了各自的 Endpoint 內
  - 多個同時對 A 的 Request，將會共享 instance_A，可能在 instance_A 內部產生 Race Condition
  - 多個同時對 B 的 Request，將會共享 instance_B，可能在 instance_B 內部產生 Race Condition
  - 但是，A 的 Request 和 B 的 Request 之間不會因為 retriever 物件而互相干擾
  anchor_type: 背景說明
  importance: 8
  status: normal
- id: c9
  role: anchor
  text: 危險情況：兩個實例雖然分開，但由同一個類別建立；如果 Retriever 類別定義了類別屬性 total_requests_processed，並在方法裡執行 Retriever.total_requests_processed += 1，那麼不管是對 A 還是對 B 的 Request 都會修改同一個變數，導致跨端點的 Race Condition
  source_quotes:
  - 雖然兩個實例是分開的，但它們是由同一個類別建立的。如果在 Retriever 類別中定義了類別屬性，那麼這個屬性將會被 instance_A 和 instance_B 共享！
  - "Retriever.total_requests_processed += 1 # 修改共享的類別屬性！"
  - 在這個例子中，不管是對 A 還是對 B 的 Request，都會修改同一個 Retriever.total_requests_processed 變數，這將會導致跨端點的 Race Condition。
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 9
  status: normal
- id: c10
  role: evaluation
  text: 在每個 Endpoint 檔案中都自行初始化相同類別的架構，雖然在技術上可行，但通常被認為是不良實踐：違反 DRY（在多個地方重複物件的建立邏輯）
  source_quotes:
  - 上述的架構模式（在每個 Endpoint 檔案中都自行初始化相同類別）雖然在技術上可行，但通常被認為是不良實踐，原因如下：
  - 違反 DRY (Don't Repeat Yourself)：在多個地方重複了物件的建立邏輯
  anchor_type: 部落格判斷
  importance: 10
  status: normal
- id: c11
  role: evaluation
  text: 這種架構的另外兩個問題：如果 Retriever() 的初始化是昂貴的操作（例如載入大模型），等於載入兩次，佔用雙倍的記憶體和啟動時間；而且可能期望 retriever 是全域單例（Singleton），實際上卻建立了多個實例，可能導致非預期的行為
  source_quotes:
  - 資源浪費：如果 Retriever() 的初始化是一個昂貴的操作（例如載入大模型），您現在等於是載入了兩次，佔用了雙倍的記憶體和啟動時間
  - 狀態不一致：可能期望 retriever 是一個全域單例 (Singleton)，但實際上卻建立了多個實例，這可能導致非預期的行為
  anchor_type: 部落格判斷
  comparison_target: 只載入一次（各檔各自初始化「等於是載入了兩次」）
  importance: 11
  status: normal
- id: c12
  role: mechanism
  text: 更清晰、更健壯的做法是集中化依賴管理：在一個檔案（例如 src/dependencies.py）建立唯一的、共享的實例，讓各個 Endpoint 檔案直接匯入這個實例；這樣所有 Request，無論到 A 還是 B，都共享這個唯一實例，既節省資源，也讓狀態管理清晰可控
  source_quotes:
  - 更清晰、更健壯的做法是只建立一個共享的實例，然後讓所有需要它的地方都使用這一個實例。
  - "# 在這裡建立唯一的、共享的實例"
  - "from src.dependencies import retriever # 匯入同一個實例！"
  - 這樣一來，所有 Request，無論是到 A 還是 B，都會共享 dependencies.py 中建立的唯一實例。這不僅節省了資源，也讓狀態管理變得清晰可控。
  qualifiers:
  - text: 集中化之後所有 Request 共享同一個實例；共享物件會不會發生 Race Condition，關鍵仍在 Class 內部是否有 Shared Mutable State
    source_quote: "會不會發生 Race Condition 的關鍵在於: Retriever Class 內部是否有 Shared Mutable State?"
  anchor_type: 部落格判斷
  importance: 12
  status: normal
```
