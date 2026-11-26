---
id: skill-pack-vs-ontology-graph
title: 領域知識要用扁平的 skill 包還是圖，看領域之間有沒有衍生或依賴關係：幾乎不互相引用，扁平的 skill 包就夠；有依賴關係，圖只要把關係定義一次，到處都能沿著走。再往下一層，還要選知識是蒸餾成文件再交付，還是讓 agent 直接查活的結構
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: evoontology
  article_title: "EvoOntology 解析：在 data agent 與資料之間，加一層會自己演化的 ontology"
  url: https://datasciocean.com/paper-intro/evoontology/
  sections:
  - data agent 每次都從零摸資料，把說明整包塞進 prompt 還可能更糟
  - 帶得走的收穫：該不該整包塞，看量有多大；自我演化的骨架，閘門先行
  - Skill-per-domain 與 Ontology-graph：怎麼選
  - 跟 WikiSkill 比：知識要先蒸餾再交付，還是讓 agent 直接查活的結構
  first_appearance: true
parent: null
related:
  - evoontology-three-layer-ontology
  - evoontology-evolution-loop-gate-first
  - evoontology-query-over-prompt-stuffing
  - evoontology-limits-backbone-and-cold-start
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 可以遷移的判斷規則是：領域之間幾乎不互相引用，用 skill-per-domain 這種扁平做法就夠，維護也簡單；領域之間有衍生或依賴關係，圖狀結構的優勢就會顯出來，因為關係定義一次，到處都能沿著走，不用在每個用到的地方重複兜同一套推導邏輯
  source_quotes:
  - "可以遷移的判斷規則是："
  - "領域之間幾乎不互相引用（例如「文件解析」skill 與「排程」skill 沒什麼關係），用 skill-per-domain 這種扁平做法就夠，維護也簡單。"
  - "領域之間有衍生或依賴關係（例如某個指標要組合好幾個不同來源的欄位與規則），圖狀結構的優勢就會顯出來，因為關係定義一次，到處都能沿著走，不用在每個用到的地方重複兜同一套推導邏輯。"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: 很多實務上的 agent 系統和 EvoOntology 的 ontology 做法屬於同一個大類別，都是把散落的領域知識結構化，讓 agent 查得到，差別在組織方式；blog 舉的例子是替不同領域各寫一份 skill、每個 skill 綁定該領域的 schema 與知識的做法（skill-per-domain）
  source_quotes:
  - "很多實務上的 agent 系統（例如替不同領域各寫一份 skill，每個 skill 綁定該領域的 schema 與知識）和這篇論文的 ontology 做法，屬於同一個大類別：都是把散落的領域知識結構化，讓 agent 查得到。差別在組織方式。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c3
  role: context
  text: "EvoOntology 出自論文《EvoOntology: A Self-Evolving Ontology Layer for Data Agents》：它在 data agent（根據自然語言指令操作資料庫表格、CSV、文件、log 這類異質資料的 AI agent）與資料之間放一層可查詢、會演化的 ontology，由 Schema、Content、Tool 三層組成；blog 建議先把這一層的核心 ontology 理解成一份結構化的領域知識：有哪些業務概念、每個概念對應到資料庫的哪個欄位、使用這些概念要遵守什麼規則，再用「圖」把概念之間的關係連起來"
  source_quotes:
  - "EvoOntology: A Self-Evolving Ontology Layer for Data Agents"
  - "一種根據自然語言指令，去操作資料庫表格、CSV、文件、log 這類異質資料的 AI agent"
  - "做法是在 agent 與資料之間放一層可查詢、會演化的 ontology，由 Schema、Content、Tool 三層組成。"
  - "這一層的核心是 ontology（本體）。先把它理解成一份結構化的領域知識：有哪些業務概念、每個概念對應到資料庫的哪個欄位、使用這些概念要遵守什麼規則，再用「圖」把概念之間的關係連起來。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c4
  role: mechanism
  text: 兩種組織方式的差別：skill-per-domain 的組織單位是一個領域的完整包（schema 與領域知識綁在一起），依問題標記對應哪個 skill，skill 之間預設互不相干，要跨領域通常得手動兜起來；ontology-graph 的組織單位是一個 Term（概念）節點，概念之間用 typed edge 連起來，agent 主動呼叫 browse、resolve 兩個工具，查詢單位是概念、不是整包 skill，Term 之間可以是 association、hierarchy、composition、derivation 等關係，agent 可以沿著關係走過去
  source_quotes:
  - "組織單位 | 一個 skill 就是一個領域的完整包（schema 與領域知識綁在一起） | 一個 Term（概念）就是一個節點，概念之間用 typed edge 連起來"
  - "取用方式 | 依問題標記對應哪個 skill | agent 主動呼叫 browse、resolve 兩個工具，查詢單位是概念，不是整包 skill"
  - "跨領域關聯 | 弱：skill 之間預設互不相干，要跨領域通常得手動兜起來 | 強：Term 之間可以是 association、hierarchy、composition、derivation 等關係，例如 Profit 直接連到 Revenue 與 Cost，agent 可以沿著關係走過去"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c5
  role: anchor
  text: 有依賴關係的例子：Profit 由 Revenue 與 Cost 推導，在圖裡 Profit 直接連到 Revenue 與 Cost，圖只要把關係定義一次，到處都能沿著走
  source_quotes:
  - "領域之間有衍生或依賴關係時（例如 Profit 由 Revenue 與 Cost 推導），圖只要把關係定義一次，到處都能沿著走"
  - "例如 Profit 直接連到 Revenue 與 Cost，agent 可以沿著關係走過去"
  anchor_type: 部落格舉例
  importance: 3
  status: normal
- id: c6
  role: anchor
  text: 互不引用的例子：「文件解析」skill 與「排程」skill 沒什麼關係，扁平的 skill 包就夠
  source_quotes:
  - "領域之間幾乎不互相引用（例如「文件解析」skill 與「排程」skill 沒什麼關係），用 skill-per-domain 這種扁平做法就夠"
  - "領域之間幾乎不互相引用時，扁平的 skill 包就夠。"
  anchor_type: 部落格舉例
  importance: 4
  status: normal
- id: c7
  role: mechanism
  text: WikiSkill 是另一篇自我演化知識系統論文，架構是 Raw Layer（原始軌跡）、Wiki Layer（整理過的中間知識）、Skill Layer（最終交給 agent 的技能文件）三層：軌跡先進維護用的 Wiki，再蒸餾成 Skill；執行期 agent 只看 Skill，完全不碰 Wiki；這是刻意的設計，不只是訓練期的臨時限制，貫穿訓練與部署兩個階段
  source_quotes:
  - "是我們之前讀過的另一篇自我演化知識系統論文，架構是 Raw Layer（原始軌跡）、Wiki Layer（整理過的中間知識）、Skill Layer（最終交給 agent 的技能文件）三層。"
  - "軌跡先進維護用的 Wiki（優化過程的工作台），再蒸餾成 Skill（最終產物）"
  - "WikiSkill 的設計是刻意的，不只是訓練期的臨時限制：執行期 agent 在 inference 階段確實只讀 Skill，完全不接觸 Wiki，這貫穿訓練與部署兩個階段。"
  anchor_type: 外部研究引用
  importance: 3
  status: normal
- id: c8
  role: mechanism
  text: EvoOntology 則不蒸餾：軌跡直接修補進 ontology 本體（Content、Tool、Schema），執行期 agent 每次都透過 Tool Layer 即時查詢 ontology 本身；它沒有一個獨立的「最終文件」，agent 看到的資料形態，與系統儲存的資料形態是同一個東西
  source_quotes:
  - "軌跡直接修補進 ontology 本體（Content、Tool、Schema）"
  - "每次都透過 Tool Layer 即時查詢 ontology 本身"
  - "EvoOntology 則沒有一個獨立的「最終文件」，agent 看到的資料形態，與系統儲存的資料形態是同一個東西。"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c9
  role: evaluation
  text: blog 把這看成「怎麼選」框架再往下一層的軸線：不只是知識怎麼組織（扁平包或圖），還有知識怎麼交付給執行期的 agent：蒸餾成一份文件、只露出最終產物，或讓 agent 直接查活的結構、完全不封裝
  source_quotes:
  - "這其實是前面「Skill-per-domain 與 Ontology-graph：怎麼選」那個框架再往下一層的軸線：不只是知識怎麼組織（扁平包或圖），還有知識怎麼交付給執行期的 agent（蒸餾成一份文件、只露出最終產物，或讓 agent 直接查活的結構、完全不封裝）。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c10
  role: evidence
  text: 封裝可以避免 agent 在推論時被中間過程的雜訊干擾；WikiSkill 的消融實驗顯示，讓 agent 直接碰 Wiki 反而讓最終品質下降
  source_quotes:
  - "**封裝**可以避免 agent 在推論時被中間過程的雜訊干擾。WikiSkill 的消融實驗顯示，讓 agent 直接碰 Wiki 反而讓最終品質下降。"
  anchor_type: 外部研究引用
  importance: 3
  status: normal
- id: c11
  role: evaluation
  text: 不封裝則保留了「知識還在持續演化、agent 每次都拿到最新版本」的即時性，不需要一個明確的「蒸餾完成」時間點；blog 認為封裝與不封裝兩者各有道理
  source_quotes:
  - "兩者各有道理："
  - "**不封裝**則保留了「知識還在持續演化、agent 每次都拿到最新版本」的即時性，不需要一個明確的「蒸餾完成」時間點。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c12
  role: evaluation
  text: blog 把「規則和事實怎麼分工」（ontology 是規則層、knowledge graph 是事實層）與「要用扁平的 skill 包還是圖」看成知識存好之後的兩個組織問題，兩者是同一條「知識供給設計」思路往下展開的結果，不是互相獨立的知識點
  source_quotes:
  - "知識存好之後，還有兩個組織上的問題，延伸閱讀有細講。第一，規則和事實怎麼分工：ontology 是規則層，knowledge graph 是事實層，規則規範事實。第二，要用扁平的 skill 包還是圖"
  - "這兩個問題是同一條「知識供給設計」思路往下展開的結果，不是互相獨立的知識點。"
  anchor_type: 部落格判斷
  importance: 4
  status: normal
```
