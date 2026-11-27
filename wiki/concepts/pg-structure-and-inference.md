---
id: pg-structure-and-inference
title: Procedural Graph 把 agent 的做事流程存成有向圖，推論時只依上一步動作取往後 2 跳的子圖、由另一個 LLM 翻成提醒交給 solver；這像導航只報下一兩個路口，但提醒只是偏向而非強制
type_hint: 方法
context_type: bound_to_source
sources:
  - article: procedural-graphs
    article_title: "把流程畫成圖，AI Agent 就不會迷路？Procedural Graphs 解析"
    url: https://datasciocean.com/paper-intro/procedural-graphs/
    sections:
      - agent 做長任務，為什麼會迷路？
      - ReAct 的痛點：每一步都在自己摸索
      - 圖由什麼組成
      - 實際用的圖很小
      - 推論時：每一步只看腳邊兩跳
      - 定位：agent 現在在圖上的哪裡
      - 生成提示並選動作
      - 四個要記得的性質
      - 定位與子圖：上一步動作怎麼對到節點
      - Ψ 與 solver：各看到什麼、輸出什麼
      - 一個 benchmark 一張圖
    first_appearance: true
parent: null
related:
  - pg-local-subgraph-vs-full-graph
  - pg-results-and-expert-graph-collapse
  - propose-validate-reject-evolution-loop
  - evoontology-three-layer-ontology
  - jevmem-read-plan-expand-stop
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: Procedural Graph（以下簡稱 PG）把 agent 的做事流程存成可編輯的有向圖，推論時每一步只取 agent 目前所在位置往後 2 跳的子圖，由另一個 LLM 翻成提示附加到 solver 的 prompt；這像導航只報下一兩個路口，但提示只是偏向 solver 的下一步動作，不會強制
    source_quotes:
      - "把 agent 的「做事流程」存成一張可編輯的有向圖（節點是步驟，箭頭指向下一步）。每一步只取 agent 目前所在位置附近的一小段，由另一個 LLM 翻成提示。"
      - "推論時的做法是：每一步決策前，先判斷 agent 剛做完圖上的哪個節點，只取那個節點往後 2 跳（沿著箭頭走兩步）的小圖，由另一個 LLM 轉成一小段「現在該做什麼、要避開什麼」的文字，附加到 solver 的 prompt。"
      - "這像是導航：它只報下一兩個路口該怎麼走，不會把整張地圖唸給你聽。"
      - "論文摘要說提示會 bias solver 的下一步動作，但不會 dictate 它。論文沒有任何機制檢查 solver 的動作是不是真的走在圖上。"
    anchor_type: 原作者解讀
    numeric_kind: non_comparative
    numeric_reason: 定義
    qualifiers:
      - text: 推論時圖是凍結的，不會更新
        source_quote: "推論時圖是凍結的，不會更新（Section 3.2）。"
      - text: 每一步多一次 LLM 呼叫（guidance model 本身），成本一定比不用圖高
        source_quote: "每一步多一次 LLM 呼叫（\\( \\Psi \\) 本身），成本一定比不用圖高。"
    figures:
      - file: figures/procedural-graphs/figure2.png
        article: procedural-graphs
        src: figure2.png
        caption: 圖 2 — Procedural Graph 框架總覽。中間是線上推論，右邊是離線演化。（來源：原始論文 Figure 2。）
        sha256: 06bb1d71f39eef889f54cb194497fc5879cf49d9dd599d73d3b902c56b868bfa
    importance: 1
    status: normal

  - id: c2
    role: context
    text: "Procedural Graph 出自 Google 論文《Procedural Graphs: Self-Evolving Execution Structures for LLM Agents》（2026 年九月），用來解決 ReAct（先想一步、呼叫一個工具、看結果、再想的 agent 迴圈）在長任務中每一步都得從越來越長的「動作＋觀察」流水帳裡自己推出下一步，而容易忘記目標、亂序呼叫工具、重複無效動作的問題"
    source_quotes:
      - "這篇整理 Google 的論文 *Procedural Graphs: Self-Evolving Execution Structures for LLM Agents*（arXiv 2609.09153v1，2026 年九月）。"
      - "ReAct（先想一步、呼叫一個工具、看結果、再想的 agent 迴圈，下一節細講）"
      - "問題是每一步都得從一份越來越長的「動作＋觀察」流水帳裡，自己推出下一步。長任務裡就容易忘記目標、亂序呼叫工具、重複無效的動作。"
    anchor_type: 背景說明
    numeric_kind: non_comparative
    numeric_reason: 日期
    importance: 2
    status: normal

  - id: c3
    role: mechanism
    text: PG 的出發點是與知識圖譜的類比：知識圖譜把事實組織成三元組回答「這是什麼」，Procedural Graph 把任務流程組織成三元組回答「接下來做什麼」
    source_quotes:
      - "論文的出發點是一個類比，它靠的是三元組：「起點、關係、終點」三個一組的記法。"
      - "知識圖譜把事實組織成三元組，回答「這是什麼」；Procedural Graph 把任務流程組織成三元組，回答「接下來做什麼」。"
    anchor_type: 原作者解讀
    figures:
      - file: figures/procedural-graphs/figure1.png
        article: procedural-graphs
        src: figure1.png
        caption: 圖 1 — 從知識到流程：知識圖譜回答「是什麼」，Procedural Graph 回答「要做什麼」。（來源：原始論文 Figure 1。）
        sha256: 44fadb9589b417a8539400b8cdcf0d9796618d1398fb3592132f244df1bf66d2
    importance: 3
    status: normal

  - id: c4
    role: mechanism
    text: 一張 PG 由節點集合 V、關係種類 R、邊集合 E，以及邊上的文字屬性 Φ 組成；每個節點代表工具函式、技能、內部推理步驟或任務狀態，每條邊 (u, r, v) 附三段文字：condition（什麼時候該走這條邊）、guidance（怎麼做）、pitfalls（要避開什麼）
    source_quotes:
      - "一張 PG 由四樣東西組成，也就是節點、關係種類、邊，以及每條邊上的文字。邊是「起點、關係、終點」三個一組。"
      - "G = (V,\\, R,\\, E,\\, \\Phi), \\qquad E \\subseteq V \\times R \\times V"
      - "每個節點代表一個工具函式、一個技能、一個內部推理步驟，或一個任務狀態。"
      - "論文用三個：condition（什麼時候該走這條邊）、guidance（怎麼做）、pitfalls（要避開什麼）。"
    anchor_type: 設計參數
    qualifiers:
      - text: 關係種類 R 實際只有四種標籤（LEADS_TO、TRIGGERS、PROVIDES_INPUT_FOR、CONVERGES_TO），且 Appendix B.5 說 serializer 不會把關係標籤印給 guidance model，在這個序列化下推論時不起作用
        source_quote: "關係種類的詞彙表。實際只有四種：LEADS_TO、TRIGGERS、PROVIDES_INPUT_FOR、CONVERGES_TO（Appendix B.4）。"
      - text: 至少在 Appendix B.5 的序列化下，guidance model 只看到節點、箭頭方向和三段文字
        source_quote: "Appendix B.5 說 serializer 不會把關係標籤印給 \\( \\Psi \\)，所以至少在這個序列化下，\\( \\Psi \\) 只看到節點、箭頭方向和三段文字。"
    importance: 4
    status: normal

  - id: c5
    role: anchor
    text: 實際用的 PG 很小：在六個 benchmark 與 EnterpriseArena 共七個環境中，除了 BFCL v3 因為要對應龐大的函式目錄而有 131 個節點、265 條邊，其餘每張圖都只有 7 到 17 個節點、7 到 27 條邊
    source_quotes:
      - "實際用的圖很小。除了 BFCL v3 因為要對應龐大的函式目錄，有 131 個節點、265 條邊，其餘每張圖都只有 7 到 17 個節點、7 到 27 條邊，數字見表 1。表 1 的七欄是六個 benchmark 加上 EnterpriseArena"
    anchor_type: 設計參數
    numeric_kind: non_comparative
    numeric_reason: 計數
    figures:
      - file: figures/procedural-graphs/table7.png
        article: procedural-graphs
        src: table7.png
        caption: 表 1 — 主實驗中各 benchmark 的 Procedural Graph 規模。（來源：原始論文 Table 7。）
        sha256: 512c09b362aa96af7ee1dd7166ec5ca69eb3d9f69fe8d4497ba57c4f795ec011
    importance: 5
    status: normal

  - id: c6
    role: mechanism
    text: 推論時有兩個角色：solver 是實際選下一步動作的 LLM（ReAct 迴圈裡的 agent 本人）；guidance model（Ψ）是另一個負責把子圖翻成提示的 LLM，和 solver 用同一個底層模型
    source_quotes:
      - "solver：實際選下一步動作的 LLM，也就是 ReAct 迴圈裡的 agent 本人。"
      - "guidance model（\\( \\Psi \\)）：另一個 LLM，負責把子圖翻成提示。論文說它和 solver 用同一個底層模型（Section 4）。"
    anchor_type: 設計參數
    importance: 6
    status: normal

  - id: c7
    role: mechanism
    text: 推論的定位步驟把上一步動作 a_{t-1}（solver 上一步輸出的 Action，起點約定 a_0 = Start）與圖上節點做 exact match 得到目前節點 u_t，從 u_t 沿往外的出邊最多展開 h = 2 步取得子圖；遇到分岔時同一層的所有出邊一起收，比對不到時退回整張圖
    source_quotes:
      - "u_t = \\mathrm{Match}(a_{t-1},\\, V), \\qquad G_t = \\begin{cases} N_h(u_t), & u_t \\neq \\emptyset \\\\ G, & \\text{otherwise} \\end{cases}"
      - "起點約定 \\( a_0 = \\text{Start} \\)，所以第一步一定定位在 Start 節點。"
      - "從 \\( u_t \\) 出發，沿著往外的邊最多展開 \\( h \\) 步所得的子圖。實驗用 \\( h = 2 \\)。"
      - "比對失敗時，退回整張圖 \\( G \\)。"
      - "只沿出邊走，也就是順著箭頭方向。走過來的節點不在子圖裡，那段歷史由最近 \\( w = 3 \\) 步的軌跡視窗補上。"
      - "遇到分岔，同一層的所有出邊一起收。"
    anchor_type: 設計參數
    numeric_kind: non_comparative
    numeric_reason: 定義
    qualifiers:
      - text: 論文只寫 exactly match，沒有交代比整行（含參數）還是只比工具名、非工具節點怎麼比對，也沒給比對失敗的頻率
        source_quote: "論文只寫 exactly match，細節沒有交代：比整行（含參數），還是只比工具名？沒說。節點也可以是推理步驟或任務狀態（Section 3.1）…它們不對應任何工具呼叫，怎麼比對？沒說。"
      - text: 比對失敗退回整張圖的頻率論文沒有揭露，不知道這條路徑實際被走到多少次
        source_quote: "但論文沒給比對失敗的頻率，所以不知道這條路徑實際被走到多少次。"
    importance: 7
    status: normal

  - id: c8
    role: mechanism
    text: 定位比對只看字串吻合，不用 embedding、不算相似度，結果是確定的；論文 Section 3.2 認為沿結構取出鄰域可以同時帶出動作和它的程序前提，而獨立做 top-k 相似度檢索可能漏掉步驟之間的連接（例如檢索到 submit 指引卻漏掉前面 check_answer 的轉移）
    source_quotes:
      - "比對只看字串吻合，不用 embedding（把文字轉成一串數字，好用來算相似度）、不算相似度，所以結果是確定的。"
      - "這是 Section 3.2 的論點：獨立做 top-k 相似度檢索（挑出最相似的前 k 筆），可能漏掉步驟之間的連接。例如檢索到 submit 的指引，卻沒有前面 check_answer 的轉移，就可能漏掉讓提交變得合理的驗證步驟。沿結構取出鄰域，可以同時帶出動作和它的程序前提。"
    anchor_type: 原作者解讀
    numeric_kind: non_comparative
    numeric_reason: 名稱
    importance: 8
    status: normal

  - id: c9
    role: mechanism
    text: 取得子圖後，guidance model（Ψ）看著子圖、問題 q 和最近 w = 3 步的軌跡（到目前為止的動作與觀察記錄），寫出自由文字提示 g_t；solver 看不到圖本身，只讀問題、完整軌跡和 g_t，輸出 Thought 與 Action（實驗全部用 greedy decoding，每次取機率最高者）
    source_quotes:
      - "軌跡，就是到目前為止的動作與觀察記錄"
      - "guidance model 看著子圖、問題和最近 3 步的軌跡，寫出一段提示；solver 再看著問題、完整軌跡和這段提示，選出下一個動作。"
      - "g_t = \\Psi\\big(G_t,\\, q,\\, T_{t-w:t}\\big), \\qquad a_t \\sim P_{\\text{solver}}\\big(\\cdot \\mid q,\\, T_t,\\, g_t\\big)"
      - "實驗全部用 greedy decoding（每次取機率最高者），所以實際上是確定的。"
      - "solver 完全看不到圖本身。圖的資訊只透過 \\( \\Psi \\) 的文字進來，所以 \\( \\Psi \\) 寫得好不好，直接決定圖有沒有用。"
      - "\\( g_t \\)：自由文字，論文沒規定格式"
    anchor_type: 設計參數
    numeric_kind: non_comparative
    numeric_reason: 定義
    qualifiers:
      - text: Ψ 的 query 欄有兩種讀法（Appendix B.5 prompt 描述成 current active query / observation，公式寫成使用者問題 q），論文沒有釐清，也沒完整展示 Ψ 的實際輸出全文
        source_quote: "\\( \\Psi \\) 的 query 欄有兩種讀法，論文沒有釐清。Appendix B.5 的 prompt 把它描述成 current active query / observation，論文的公式卻寫成使用者問題 \\( q \\)。"
    importance: 9
    status: normal

  - id: c10
    role: evaluation
    text: 每個 benchmark 只有一張圖，refiner 的輸入只有目前那張圖、輸出只有四種零件修改（add_nodes、delete_nodes、add_edges、delete_edges），沒有「選哪一張圖」或「要不要新增一張圖」的決策
    source_quotes:
      - "每個 benchmark 只有一張圖，演化就是把這一張圖從 \\( G_0 \\) 改到 \\( G_K \\)；refiner 的輸入只有一張圖、輸出只有四種零件修改，所以沒有「選哪一張圖」或「要不要新增一張圖」的決策。"
      - "輸出格式只有 add_nodes、delete_nodes、add_edges、delete_edges，全是改這一張圖的零件，沒有建立新圖的操作。"
    anchor_type: 設計參數
    importance: 10
    status: normal

  - id: c11
    role: evaluation
    text: 論文沒有討論依任務類型切換不同的圖，也沒有驗證過多張圖或異質任務的情況；它靠「上一步動作對應節點」的定位加上 Ψ 過濾，沒有任務類型路由
    source_quotes:
      - "論文沒有討論依任務類型切換不同的圖，也沒有驗證過多張圖或異質任務的情況。"
      - "它靠「上一步動作 → 節點」的定位，加上 \\( \\Psi \\) 這個 LLM 過濾，沒有任務類型路由。"
    anchor_type: 部落格考證
    qualifiers:
      - text: 例如 GDPval 涵蓋不同職業的任務，也只有一張 15 個節點的圖，靠定位機制讓每一步只取圖上的一小段
        source_quote: "例如 GDPval 涵蓋不同職業的任務，也只有一張 15 個節點的圖，再靠定位機制讓每一步只取圖上的一小段。"
    importance: 11
    status: normal

  - id: c12
    role: evaluation
    text: blog 推論，PG 的定位只看上一步動作對應哪個節點、沒有路徑記憶，同一個節點不管任務是哪一類都吐出同一個鄰域；它推測 PG 在流程相近的任務上最說得通（例如 EnterpriseArena 每個月跑同一條主線），異質任務混在一張圖上是否有效沒有被驗證
    source_quotes:
      - "定位只看上一步動作對到哪個節點 | 圖沒有路徑記憶：同一個節點，不管任務是哪一類，都吐出同一個鄰域"
      - "推測：它在流程相近的任務上最說得通，例如 EnterpriseArena 每個月跑同一條主線；異質任務混在一張圖上是否有效，沒有被驗證。"
    anchor_type: 部落格推論
    importance: 12
    status: normal
```
