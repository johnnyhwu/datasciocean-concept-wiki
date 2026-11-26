---
id: evoontology-query-over-prompt-stuffing
title: 知識該不該整包塞給 agent，取決於量有多大：量大到可能超出單輪任務需要的領域知識，該做成 agent 可以主動查、按需展開的工具；EvoOntology 的實驗裡，把 semantic layer 整包塞進 prompt 常常沒用甚至倒退
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: evoontology
  article_title: "EvoOntology 解析：在 data agent 與資料之間，加一層會自己演化的 ontology"
  url: https://datasciocean.com/paper-intro/evoontology/
  sections:
  - data agent 每次都從零摸資料，把說明整包塞進 prompt 還可能更糟
  - 問題：agent 不認識資料，既有的兩派做法各有短板
  - 做法：在 agent 與資料之間放一層三層 ontology
  - Tool Layer：agent 唯一碰得到的窗口，manifest 加 browse 與 resolve
  - Gate：候選要在同條件下贏過父版本至少 τ 分才轉正
  - 主結果：六個 backbone 全贏，整包塞 prompt 反而掉分
  - 評價：貢獻中等偏架構層面，細節缺口不小
  - 帶得走的收穫：該不該整包塞，看量有多大；自我演化的骨架，閘門先行
  first_appearance: true
parent: null
related:
  - evoontology-three-layer-ontology
  - evoontology-evolution-loop-gate-first
  - evoontology-limits-backbone-and-cold-start
  - skill-pack-vs-ontology-graph
  - single-loop-progressive-disclosure
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 知識該不該整包塞給 agent，取決於量有多大。可操作的判準是：任何要給 agent 的領域知識，只要量大到可能超出單輪任務需要的範圍，就該做成「agent 可以主動查、按需展開」的工具，而不是無條件塞進系統提示
  source_quotes:
  - "**核心原則：知識該不該整包塞給 agent，取決於量有多大。**"
  - "可以抽象成一句可操作的判準：**任何要給 agent 的領域知識，只要量大到可能超出單輪任務需要的範圍，就該做成「agent 可以主動查、按需展開」的工具，而不是無條件塞進系統提示。**"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: "證據來自論文《EvoOntology: A Self-Evolving Ontology Layer for Data Agents》：data agent（根據自然語言指令操作資料庫表格、CSV、文件、log 這類異質資料的 AI agent）事前不認識資料、每次都要重新摸索，EvoOntology 在 agent 與資料之間放一層可查詢、會演化的 ontology（blog 建議先把它理解成一份結構化的領域知識），由 Schema、Content、Tool 三層組成，並包成 MCP server，agent 用工具呼叫去問它，而不是把整包知識硬塞進 context"
  source_quotes:
  - "EvoOntology: A Self-Evolving Ontology Layer for Data Agents"
  - "一種根據自然語言指令，去操作資料庫表格、CSV、文件、log 這類異質資料的 AI agent"
  - "EvoOntology 想解決的是 data agent 事前不認識資料、每次都要重新摸索的問題，做法是在 agent 與資料之間放一層可查詢、會演化的 ontology，由 Schema、Content、Tool 三層組成。"
  - "先把它理解成一份結構化的領域知識"
  - "這一層被包成 MCP（Model Context Protocol，一種讓 agent 用統一格式呼叫外部工具的協定）server，agent 用工具呼叫去問它，而不是把整包知識硬塞進 [context](../../ai-concept/context-engineering/)。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: 對照的做法是 semantic layer：一本「業務語言與資料庫語言」的翻譯字典，人工預先定義好業務概念對應到哪些欄位、哪些指標，整包塞進 prompt。它的侷限是資料源一大就超過 context 長度限制，而且文件要人工維護，新資料、新任務一來就得跟著改
  source_quotes:
  - "表裡提到的 semantic layer，直覺上是一本「業務語言與資料庫語言」的翻譯字典。"
  - "人工預先定義好業務概念對應到哪些欄位、哪些指標，整包塞進 prompt | 資料源一大就超過 context 長度限制；而且文件要人工維護，新資料、新任務一來就得跟著改"
  anchor_type: 背景說明
  importance: 2
  status: normal
- id: c4
  role: context
  text: 主結果的設定：DDR-Bench 是開放式資料研究的 benchmark，分數是準確率，越高越好；三組對照是 Baseline（無 ontology）、Baseline+SL（把 semantic layer 整包塞進 prompt）、EvoOntology；backbone 指驅動 agent 的底層 LLM，主結果表涵蓋六個 backbone
  source_quotes:
  - "DDR-Bench（一個開放式資料研究的 benchmark，分數是準確率，越高越好）"
  - "三組對照則是：Baseline（無 ontology）、Baseline+SL（把 semantic layer 整包塞進 prompt）、EvoOntology。"
  - "backbone（驅動 agent 的底層 LLM）"
  - "主結果表（表 1）涵蓋六個 backbone"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c5
  role: evidence
  text: EvoOntology 在六個 backbone 上全面贏過沒有 ontology 的 Baseline，DDR-Bench 六個 backbone 的平均增益是 +17.8 分
  source_quotes:
  - "核心結論是 EvoOntology 在六個 backbone 上全面贏過 Baseline，DDR-Bench 六個 backbone 的平均增益是 +17.8 分"
  - "EvoOntology 在六個 backbone（驅動 agent 的底層 LLM）上全面贏過沒有 ontology 的 Baseline，平均增益是 +17.8 分。"
  anchor_type: 實驗結果
  comparison_target: 沒有 ontology 的 Baseline
  qualifiers:
  - text: 主結果表是 DDR-Bench 的 10-K 情境
    source_quote: "表 1 — DDR-Bench 10-K 情境的主結果"
    source: figure_caption
  - text: 消融實驗的 +20.0 是另一個統計範圍（只取四個 backbone 的平均），和這裡六個 backbone 的 +17.8 不能直接比
    source_quote: "後面 ablation 的 +20.0 是另一個統計範圍：只取四個 backbone 的平均，兩個數字不矛盾"
  figures:
  - file: figures/evoontology/table1.png
    article: evoontology
    src: table1.png
    caption: 表 1 — DDR-Bench 10-K 情境的主結果；括號內為相對 Baseline 的增減。（來源：原始論文 Table 1。）
    sha256: 173e6fce85adbeaa04c85474950f26068be67b4709a125fd127ae0eaa8aa90da
  importance: 2
  status: normal
- id: c6
  role: evidence
  text: 把 semantic layer 整包塞進 prompt 的 Baseline+SL 常常沒用，甚至倒退：Claude-Sonnet-5 在 Baseline+SL 上的 Trajectory-Wise 分數（DDR-Bench 的指標之一）反而掉了 15.0 分
  source_quotes:
  - "而 Baseline+SL 常常沒用，甚至倒退：Claude-Sonnet-5 在 Baseline+SL 上的 Trajectory-Wise 反而掉了 15.0 分（表 1）。"
  - "Trajectory-Wise 分數（DDR-Bench 的指標之一）"
  anchor_type: 實驗結果
  comparison_target: 同一個 backbone（Claude-Sonnet-5）沒有 ontology 的 Baseline
  qualifiers:
  - text: 主結果表是 DDR-Bench 的 10-K 情境
    source_quote: "表 1 — DDR-Bench 10-K 情境的主結果"
    source: figure_caption
  figures:
  - file: figures/evoontology/table1.png
    article: evoontology
    src: table1.png
    caption: 表 1 — DDR-Bench 10-K 情境的主結果；括號內為相對 Baseline 的增減。（來源：原始論文 Table 1。）
    sha256: 173e6fce85adbeaa04c85474950f26068be67b4709a125fd127ae0eaa8aa90da
  importance: 2
  status: normal
- id: c7
  role: evaluation
  text: blog 認為這組對照是全篇最有力的證據：整包塞 prompt 這條路是錯的，主動查詢才有效；Baseline+SL 常常反而讓表現變差，是「主動查詢優於整包塞 prompt」最乾淨的證據
  source_quotes:
  - "這組對照是全篇最有力的證據：**整包塞 prompt 這條路是錯的，主動查詢才有效。**"
  - "Baseline+SL 常常反而讓表現變差，就是最乾淨的證據。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: blog 在「帶得走的收穫」寫的核心原則是：知識該不該整包塞給 agent，取決於量有多大
    source_quote: "知識該不該整包塞給 agent，取決於量有多大。"
  - text: 主結果表是 DDR-Bench 的 10-K 情境
    source_quote: "表 1 — DDR-Bench 10-K 情境的主結果"
    source: figure_caption
  figures:
  - file: figures/evoontology/table1.png
    article: evoontology
    src: table1.png
    caption: 表 1 — DDR-Bench 10-K 情境的主結果；括號內為相對 Baseline 的增減。（來源：原始論文 Table 1。）
    sha256: 173e6fce85adbeaa04c85474950f26068be67b4709a125fd127ae0eaa8aa90da
  importance: 3
  status: normal
- id: c8
  role: mechanism
  text: blog 對原因的解釋：靜態塞進 prompt 的知識，會與 agent 其他的指令競爭注意力，而且沒辦法按需裁剪
  source_quotes:
  - "原因不難理解：靜態塞進 prompt 的知識，會與 agent 其他的指令競爭注意力，而且沒辦法按需裁剪。"
  anchor_type: 部落格推論
  importance: 3
  status: normal
- id: c9
  role: anchor
  text: blog 舉的假設情境：一份上百個欄位的完整資料字典，每次任務都整份塞進去，其中絕大部分與這次的問題無關，卻照樣占著 context
  source_quotes:
  - "想像一份上百個欄位的完整資料字典，每次任務都整份塞進去，其中絕大部分與這次的問題無關，卻照樣占著 context（這是我們舉的假設情境，不是論文的數字）。"
  anchor_type: 部落格舉例
  importance: 4
  status: normal
- id: c10
  role: mechanism
  text: EvoOntology 的解法是 Tool Layer：唯一會直接塞進 prompt 的是一份很精簡的 manifest（資料源有哪些、工具怎麼用），實際知識留在 ontology 裡，由 agent 自己決定要不要用 browse（找相關概念）與 resolve（拿某個已知物件的完整內容）兩個工具去查
  source_quotes:
  - "唯一會直接塞進 prompt 的東西，內容很精簡：資料源有哪些、這個工具怎麼用。這正好呼應前面講的問題：semantic layer 的痛點是整包塞進 context，這裡的解法是只把「使用說明書」放進 prompt，實際知識留在 ontology 裡，由 agent 自己決定要不要去查。"
  - "這個窗口由三樣東西組成：一份 manifest，加上"
  - "找相關概念的模糊比對與檢索。"
  - "拿某個已知物件的完整內容。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c11
  role: evaluation
  text: blog 建議的做法：下次替 agent 準備領域知識，先估一下量有多大；量大的，做成它能按需查詢的窗口（manifest 加 browse、resolve），不要整包塞進 prompt
  source_quotes:
  - "**試**：下次替 agent 準備領域知識，先估一下量有多大。量大的，做成它能按需查詢的窗口（manifest 加 browse、resolve），不要整包塞進 prompt。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c12
  role: evaluation
  text: blog 認為 EvoOntology 值得借用的有兩項：驗證閘門的設計，以及「主動查詢優於整包塞 prompt」這個結論。blog 列出的比較站得住腳的貢獻中，第一項是把「三層拆分（Schema、Content、Tool）加上 MCP 包裝」這個具體架構，應用在 agent-data gap（agent 知道的與資料實際的樣子之間的落差）問題上，並證明了「主動查詢優於整包塞 prompt」
  source_quotes:
  - "值得借用的是驗證閘門（候選修改要先通過、才會被採用的一道檢查）的設計，以及「主動查詢優於整包塞 prompt」這個結論。"
  - "比較站得住腳的貢獻有三個："
  - "把「三層拆分（Schema、Content、Tool）加上 MCP 包裝」這個具體架構，應用在 agent-data gap 問題上，並證明了「主動查詢優於整包塞 prompt」。"
  - "論文把「agent 知道的」與「資料實際的樣子」之間的落差，稱為 **agent-data gap**。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: blog 對論文的整體評價是貢獻中等偏低
    source_quote: "不過整體評價是貢獻中等偏低"
  importance: 4
  status: normal
```
