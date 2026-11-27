---
id: evoontology-three-layer-ontology
title: EvoOntology 在 data agent 與資料之間放一層可查詢、會演化的 ontology，由 Schema、Content、Tool 三層組成：Schema 是規則書，Content 是照規則長出來的知識圖，Tool 是 agent 唯一碰得到的查詢窗口
type_hint: 方法
context_type: bound_to_source
sources:
- article: evoontology
  article_title: "EvoOntology 解析：在 data agent 與資料之間，加一層會自己演化的 ontology"
  url: https://datasciocean.com/paper-intro/evoontology/
  sections:
  - data agent 每次都從零摸資料，把說明整包塞進 prompt 還可能更糟
  - 問題：agent 不認識資料，既有的兩派做法各有短板
  - 做法：在 agent 與資料之間放一層三層 ontology
  - Content Layer：用四種節點和兩種邊把領域知識連成圖
  - Evidence 和 Constraint 差在哪：用卡牌合法性案例走一次
  - Schema Layer：像 class 定義的規則書，改它不動既有知識
  - Tool Layer：agent 唯一碰得到的窗口，manifest 加 browse 與 resolve
  - 走一遍：「上個月成本為什麼上漲」是怎麼被查出來的
  - Ablation：Gate、Mappings、Tool 層各自貢獻多少
  - 實驗結果：主動查詢勝過整包塞 prompt，閘門最不能省
  - 評價：貢獻中等偏架構層面，細節缺口不小
  - 帶得走的收穫：該不該整包塞，看量有多大；自我演化的骨架，閘門先行
  - Ontology 與 Knowledge Graph 到底差在哪
  first_appearance: true
parent: null
related:
  - evoontology-evolution-loop-gate-first
  - evoontology-query-over-prompt-stuffing
  - evoontology-limits-backbone-and-cold-start
  - skill-pack-vs-ontology-graph
  - pg-structure-and-inference
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: EvoOntology 想解決的是 data agent 事前不認識資料、每次都要重新摸索的問題，做法是在 agent 與資料之間放一層可查詢、會演化的 ontology，由 Schema、Content、Tool 三層組成
  source_quotes:
  - "EvoOntology 想解決的是 data agent 事前不認識資料、每次都要重新摸索的問題，做法是在 agent 與資料之間放一層可查詢、會演化的 ontology，由 Schema、Content、Tool 三層組成。"
  anchor_type: 設計參數
  importance: 1
  status: normal
- id: c2
  role: context
  text: "EvoOntology 出自 Renmin University of China 團隊 2026 年 9 月的論文《EvoOntology: A Self-Evolving Ontology Layer for Data Agents》，做法是在 agent 與資料之間插入一層可以被查詢、而且會根據使用經驗自我修補的知識層。data agent 指的是根據自然語言指令，去操作資料庫表格、CSV、文件、log 這類異質資料的 AI agent"
  source_quotes:
  - "EvoOntology: A Self-Evolving Ontology Layer for Data Agents"
  - "Renmin University of China 的團隊，2026 年 9 月）的做法，是在 agent 與資料之間插入一層可以被查詢、而且會根據使用經驗自我修補的知識層。"
  - "一種根據自然語言指令，去操作資料庫表格、CSV、文件、log 這類異質資料的 AI agent"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 日期
  importance: 2
  status: normal
- id: c3
  role: context
  text: 這一層的核心是 ontology（本體），可以先理解成一份結構化的領域知識：有哪些業務概念、每個概念對應到資料庫的哪個欄位、使用這些概念要遵守什麼規則，再用「圖」把概念之間的關係連起來
  source_quotes:
  - "這一層的核心是 ontology（本體）。先把它理解成一份結構化的領域知識：有哪些業務概念、每個概念對應到資料庫的哪個欄位、使用這些概念要遵守什麼規則，再用「圖」把概念之間的關係連起來。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c4
  role: context
  text: 要解決的落差：agent 只能透過 SQL 介面、file reader 這類通用工具接觸資料，但資料的欄位怎麼命名、彼此怎麼 join、內容長什麼樣子，它事前一無所知，於是每次任務都要重新盲目探索。論文把「agent 知道的」與「資料實際的樣子」之間的落差，稱為 agent-data gap
  source_quotes:
  - "核心麻煩是：agent 只能透過 SQL 介面（用結構化查詢語言向資料庫發問的方式）、file reader 這類通用工具接觸資料，但資料的欄位怎麼命名、彼此怎麼 join、內容長什麼樣子，它事前一無所知。於是每次任務都要重新盲目探索"
  - "論文把「agent 知道的」與「資料實際的樣子」之間的落差，稱為 **agent-data gap**。"
  anchor_type: 原作者解讀
  figures:
  - file: figures/evoontology/figure1.png
    article: evoontology
    src: figure1.png
    caption: 圖 1 — 自我演化的 ontology 層如何幫助 data agent 理解異質資料。（來源：原始論文 Figure 1。）
    sha256: 058f72711cd46c9b8a86cf78f44b6efc54c94df579b9b900259e569361c0b471
  importance: 3
  status: normal
- id: c5
  role: context
  text: 既有做法大致分兩派。Raw querying（DIN-SQL、MAC-SQL、CHESS 這類 text-to-SQL agent）讓 agent 直接摸 schema、發 exploratory query，資料一大一異質就陷入重複無效的探索，學到的東西不會被留下來。Semantic layer（dbt 的 semantic layer、OWL ontology）由人工預先定義好業務概念對應到哪些欄位、哪些指標，整包塞進 prompt，資料源一大就超過 context 長度限制，而且文件要人工維護
  source_quotes:
  - "Raw querying | DIN-SQL、MAC-SQL、CHESS 這類 text-to-SQL agent | 讓 agent 直接摸 schema（資料表與欄位的結構）、發 exploratory query | 資料一大一異質，就陷入重複無效的探索；這次好不容易摸清楚的欄位對應，下次任務又要重摸，學到的東西不會被留下來"
  - "Semantic layer | dbt 的 semantic layer、OWL ontology | 人工預先定義好業務概念對應到哪些欄位、哪些指標，整包塞進 prompt | 資料源一大就超過 context 長度限制；而且文件要人工維護，新資料、新任務一來就得跟著改"
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c6
  role: mechanism
  text: 這層 ontology 由三層組成：存知識的 Content Layer、管規則的 Schema Layer、讓 agent 來查的 Tool Layer；這一層被包成 MCP server，agent 用工具呼叫去問它，而不是把整包知識硬塞進 context
  source_quotes:
  - "它由三層組成，存知識的 Content Layer、管規則的 Schema Layer、讓 agent 來查的 Tool Layer。"
  - "這一層被包成 MCP（Model Context Protocol，一種讓 agent 用統一格式呼叫外部工具的協定）server，agent 用工具呼叫去問它，而不是把整包知識硬塞進 [context](../../ai-concept/context-engineering/)。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c7
  role: mechanism
  text: Content Layer 是一個有型別的語意圖（typed semantic graph），有四種節點家族：Term（抽象的領域概念本身）、Mapping（把 Term 落地到具體欄位與串接路徑）、Constraint（規範概念合法使用方式的業務規則）、Evidence（支撐語意聲明的實際觀測證據）；兩種邊家族：Semantic Relations 連 Term 與 Term（association、hierarchy、composition、equivalence、derivation 共五種），Structural References 把 Term 連到 Mapping、把 Constraint 與 Evidence 掛到它們支持的對象上
  source_quotes:
  - "Content Layer 是一個 typed semantic graph（有型別的語意圖），裡面有四種節點家族、兩種邊家族。"
  - "Term（概念） | 抽象的領域概念本身，不是實際資料"
  - "Mapping（對應） | 把 Term 落地到具體欄位與串接路徑"
  - "Constraint（規則） | 規範這些概念合法使用方式的業務規則"
  - "Evidence（佐證） | 支撐前面語意聲明的實際觀測證據"
  - "Semantic Relations | Term 與 Term 之間 | association（關聯）、hierarchy（上下位）、composition（部分與整體）、equivalence（等價）、derivation（推導），共五種"
  - "Structural References | Term 連到 Mapping，以及把 Constraint、Evidence 掛到它們所支持的對象上"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c8
  role: anchor
  text: 論文的財務分析案例：Profit 以 derivation 邊連到 Revenue 與 Cost，Cost 掛著一個指向 fact_cost.total_cost 的 Mapping，Profit 受「Profit = Revenue - Cost」這條 Constraint 規範，Mapping 再掛著 cost catalog 觀測樣本這個 Evidence。derivation 邊把「Profit 是從 Revenue 減 Cost 算出來的」變成圖結構本身的一部分，agent 查到 Profit 可以沿著邊找到 Revenue 與 Cost，再找到實際欄位與佐證資料
  source_quotes:
  - "圖 2 是整篇會反覆用到的財務分析案例"
  - "Profit 以 derivation 連到 Revenue 與 Cost（Profit 是由 Revenue 減 Cost 算出來的）。"
  - "Cost 掛著一個 Mapping，指向 `fact_cost.total_cost`。"
  - "Profit 受一條 Constraint 規範：Profit = Revenue - Cost。"
  - "那個 Mapping 再掛著 Evidence：cost catalog 的觀測樣本。"
  - "最關鍵的是 derivation 這條邊。它把「Profit 不是憑空存在，而是從 Revenue 減 Cost 算出來的」這件事，變成圖結構本身的一部分，而不是塞在某個字串定義裡。agent 查到 Profit 這個 Term，可以沿著 derivation 邊直接找到 Revenue 與 Cost，再沿著它們各自的 structural reference 找到實際欄位與佐證資料。"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c9
  role: mechanism
  text: Constraint 與 Evidence 回答不同的問題：Constraint 回答這個概念應該怎麼用（業務規則文字），Evidence 回答這個概念的聲明是不是真的（builder agent 對資料源實際發 query 拿到的原始結果）。論文的卡牌合法性案例：被接受的修補新增「Legality Status Code」這個 Term，同時加上指向 legalities.status 的 Mapping、實際觀測到的值分佈（Banned、Legal、Restricted 等）這個 Evidence，以及「status 為 Banned 且 format 等於目標賽制才算被禁用」這條 Constraint
  source_quotes:
  - "回答的問題 | 這個概念**應該怎麼用** | 這個概念的聲明**是不是真的**"
  - "內容形式 | 業務規則文字，例如 Profit = Revenue - Cost | 實際抓回來的資料片段，例如某欄位實際出現過哪些值"
  - "builder agent 對資料源實際發 query 拿到的原始結果"
  - "圖 3 是卡牌合法性任務裡一次被接受的修補"
  - "系統要新增「Legality Status Code」這個概念，代表 `legalities.status` 這個欄位，三個東西一起加進去："
  - "**Evidence**：實際觀測到的值分佈（Banned、Legal、Restricted 等）。"
  - "**Constraint**：`legalities.status` 為 `Banned` 且 `legalities.format` 等於目標賽制，才算被禁用。"
  anchor_type: 設計參數
  qualifiers:
  - text: Evidence 存的不只是數值，也可以是 schema 結構、樣本資料、目錄清單
    source_quote: "要注意 Evidence 存的不只是數值，也可以是 schema 結構、樣本資料、目錄清單"
  figures:
  - file: figures/evoontology/figure8.png
    article: evoontology
    src: figure8.png
    caption: 圖 3 — 卡牌合法性任務中的 ontology 演化：被接受的修補新增 Term、Mapping、Evidence 與 Constraint。（來源：原始論文 Figure 8。）
    sha256: a17744b3f57b29164411ee083705596411d34353a574da590cce169c97433233
  importance: 3
  status: normal
- id: c10
  role: mechanism
  text: Schema Layer 像 class 的定義，Content Layer 才是實際 new 出來的物件。它定義四種節點家族各自的欄位、合法的 Semantic Relation 類型、合法的 reference pattern；好處是改 Schema 不會動到既有的知識內容，例如想支援新的關係類型 temporal_dependency，只要改 Schema，既有的 Profit、Revenue、Cost 完全不用動
  source_quotes:
  - "**Schema Layer 像 class 的定義，Content Layer 才是實際 new 出來的物件**。"
  - "**四種節點家族各自的欄位**"
  - "**合法的 Semantic Relation 類型**"
  - "**合法的 reference pattern**"
  - "這層設計的關鍵好處是：改 Schema 不會動到既有的知識內容。比如想讓系統支援一種新的關係類型 temporal_dependency（時間先後依賴），只要改"
  - "加了這條規則後，既有的 Profit、Revenue、Cost 完全不用動"
  anchor_type: 設計參數
  qualifiers:
  - text: 論文沒有把每個節點型別的完整欄位列出來，只在敘述裡零星提到
    source_quote: "論文沒有把每個型別的完整欄位列出來，只在敘述裡零星提到"
  importance: 3
  status: normal
- id: c11
  role: mechanism
  text: Tool Layer 是三層裡唯一真正與 agent 互動的介面，由一份 manifest 加 browse、resolve 兩個工具組成。manifest 是唯一會直接塞進 prompt 的東西，內容很精簡：資料源有哪些、工具怎麼用；browse(q, k, n) 依查詢 q、在節點家族 k 裡做模糊比對與檢索，回傳語意上最相近的 n 個候選；resolve(I, c) 拿某個已知物件的完整內容，輸出物件本身加上它連到的所有東西（Mapping、Relations、Constraints、Evidence）。agent 先用 browse 找到 Term，再用 resolve 一次拿到它連著的 Mapping、Constraint 與 Evidence，才開始寫查詢
  source_quotes:
  - "也是三層裡唯一真正與 agent 互動的介面。這個窗口由三樣東西組成：一份 manifest，加上"
  - "唯一會直接塞進 prompt 的東西，內容很精簡：資料源有哪些、這個工具怎麼用。"
  - "找相關概念的模糊比對與檢索。"
  - "agent 想查的東西，可以是自然語言或關鍵字"
  - "限定只在哪個節點家族裡找"
  - "要回傳前幾名"
  - "輸出是一份排序過的候選清單，也就是語意上與"
  - "最相近的"
  - "拿某個已知物件的完整內容。"
  - "輸出是這個物件本身，加上它連到的所有東西（Mapping、Relations、Constraints、Evidence）。"
  - "manifest 讓 agent 知道有哪些窗口可以用，browse 找到 Term，resolve 一次拿到它連著的 Mapping、Constraint 與 Evidence，agent 才開始寫查詢。"
  anchor_type: 設計參數
  qualifiers:
  - text: resolve 的參數 c 論文沒有說明；blog 推測它可能類似 browse 的 k，用來限定只展開哪一類關聯物件，但這只是推論
    source_quote: "我們推測 \\( c \\) 可能類似 browse 的 \\( k \\)，用來限定只展開哪一類關聯物件，但這只是推論。"
  importance: 2
  status: normal
- id: c12
  role: evidence
  text: 論文 Table 7 逐一拿掉 Content Layer 的物件家族：拿掉 Mappings 掉 13.4 分（掉最多）、Evidence 掉 8.7、Constraints 掉 3.5、Relations 掉 2.1
  source_quotes:
  - "**Content Layer 的物件家族，拿掉各自掉多少分**（論文 Table 7；Term 無法單獨遮蔽，所以不在表中）："
  - "Mappings（概念接到實際欄位） | −13.4（掉最多）"
  - "Evidence（觀測佐證） | −8.7"
  - "Constraints（業務規則） | −3.5"
  - "Relations（語意關係邊） | −2.1"
  anchor_type: 實驗結果
  comparison_target: 沒拿掉該物件家族的 EvoOntology（「拿掉各自掉多少分」）
  qualifiers:
  - text: Term 無法單獨遮蔽，所以不在這張消融表中
    source_quote: "Term 無法單獨遮蔽，所以不在表中"
  - text: 實驗部分 blog 只保留關鍵數字，沒有逐表細讀
    source_quote: "這部分我們沒有逐表細讀，判斷是架構層面的思路已經理解清楚，數字本身的增量價值有限。"
  importance: 3
  status: normal
- id: c13
  role: evaluation
  text: 從這組消融，blog 的結論是 Mappings 與 Evidence 才是 Content Layer 真正的骨幹：沒有 Mapping，概念接不到實際資料；沒有 Evidence，agent 就沒辦法驗證候選的 SQL 片段對不對
  source_quotes:
  - "結論是 **Mappings 與 Evidence 才是 Content Layer 真正的骨幹**。沒有 Mapping，概念接不到實際資料；沒有 Evidence，agent 就沒辦法驗證候選的 SQL 片段對不對。"
  anchor_type: 部落格推論
  importance: 4
  status: normal
- id: c14
  role: mechanism
  text: 傳統知識表示領域的分法：Ontology 是規則層，定義有哪些類別、類別之間怎麼關聯才合法，程式類比是 class diagram 或 database schema，通常有邏輯推理（像 OWL）；Knowledge Graph 是事實層，是實際存在的具體資料點，程式類比是資料庫裡實際的 row，通常沒有邏輯推理。Knowledge Graph 通常是依照某個 Ontology 的規則，把實際資料填進去的結果
  source_quotes:
  - "講的是什麼層次 | **規則層**：定義有哪些類別、類別之間怎麼關聯才合法 | **事實層**：實際存在的具體資料點"
  - "程式類比 | class diagram 或 database schema | 資料庫裡實際的 row"
  - "有沒有邏輯推理 | 通常有（像 OWL） | 通常沒有，就是存好的事實圖"
  - "Knowledge Graph 通常是「依照某個 Ontology 的規則，把實際資料填進去」的結果。"
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c15
  role: evaluation
  text: EvoOntology 的架構剛好同時包含這兩層：Schema Layer 是 Ontology 那一半，定義有哪些節點類型、哪些關係類型合法；Content Layer 是 Knowledge Graph 那一半；前者規範後者。所以 blog 認為論文標題叫 ontology 並不是亂用
  source_quotes:
  - "而 EvoOntology 自己的架構，剛好同時包含這兩層："
  - "**Schema Layer 是 Ontology 那一半**：定義有哪些節點類型、哪些關係類型合法。"
  - "**Content Layer 是 Knowledge Graph 那一半**"
  - "前者規範後者。"
  - "所以論文標題叫 ontology 並不是亂用"
  anchor_type: 部落格判斷
  qualifiers:
  - text: blog 在評價段也說，EvoOntology 沒有 OWL 那種形式邏輯推理，它的 Content Layer 比較接近可以查詢的 typed knowledge graph，是檢索導向，「ontology」這個詞在這裡用得有點鬆散
    source_quote: "它的 Content Layer 比較接近一個可以查詢的 typed knowledge graph，是檢索導向，不是推理導向。老實說，「ontology」這個詞在這裡用得有點鬆散。"
  importance: 4
  status: normal
- id: c16
  role: mechanism
  text: blog 一開始把差別說成「semantic layer 是扁平字典、ontology 是圖」，後來修正：dbt 支援 derived metric，本身就會形成有依賴關係的圖，兩者都可能是圖，差別在圖的表達力與涵蓋範圍。dbt 的圖只有「算式依賴」一種語意，EvoOntology 的邊有五種語意；dbt 的節點限定在指標與維度，EvoOntology 的節點可以是任何領域概念，還把 Constraint 與 Evidence 做成一等公民
  source_quotes:
  - "最初的說法是「semantic layer 是扁平字典、ontology 是圖」，但這個切法後來被指出不準確：dbt 支援 derived metric（例如把 Profit 定義成 revenue − cost），本身就會形成有依賴關係的圖。"
  - "修正後的框架是：兩者都可能是圖，差別在圖的**表達力**與**涵蓋範圍**。"
  - "**邊的種類**：dbt 的圖只有一種語意，「算式依賴」。EvoOntology 的邊有五種語意（derivation、association、hierarchy、composition、equivalence）"
  - "**節點的範圍**：dbt 的節點限定在指標（metric）與維度（dimension），天生綁死在結構化表格上。EvoOntology 的節點可以是任何領域概念，還把 Constraint 與 Evidence 都做成一等公民"
  anchor_type: 部落格判斷
  importance: 4
  status: normal
```
