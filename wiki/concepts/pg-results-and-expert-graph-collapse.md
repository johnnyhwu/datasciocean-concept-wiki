---
id: pg-results-and-expert-graph-collapse
title: PG 對比無記憶 ReAct 在 24 格中贏了 23 格，但看成績要打三個折扣；而實驗三最穩的訊號是手寫專家圖在 MultiChallenge 上會讓成績崩盤，有驗證閘門的分批演化救得回來
type_hint: 發現
context_type: bound_to_source
sources:
  - article: procedural-graphs
    article_title: "把流程畫成圖，AI Agent 就不會迷路？Procedural Graphs 解析"
    url: https://datasciocean.com/paper-intro/procedural-graphs/
    sections:
      - agent 做長任務，為什麼會迷路？
      - 實驗一：23 / 24 有進步，但要打折來看
      - 實驗三：手寫專家圖可能崩盤，演化救得回來
      - 七個 baseline：各自存什麼
    first_appearance: true
parent: null
related:
  - pg-structure-and-inference
  - pg-local-subgraph-vs-full-graph
  - propose-validate-reject-evolution-loop
  - ragu-results-peeling-confounds
  - baseline-who-built-it
  - clm-results-tight-budget-not-across-the-board
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: 同一個模型、同一個 solver 對比沒有記憶的 ReAct，Procedural Graph（PG）在 24 個「模型 × benchmark」格子中有 23 格為正，但要打三個折扣（HotpotQA 幾乎沒增益、對每格最強 baseline 的部分勝利是對手退步造成的、blog 推測存在論文未承認的驗證集潛在混淆）；實驗三最站得住的訊號則是手寫專家圖在 MultiChallenge 上可能讓成績崩掉，有驗證閘門的分批演化可以救回來
    source_quotes:
      - "同一個模型、同一個 solver（負責選動作的那個 LLM），拿來對比沒有記憶的 ReAct（先想一步、呼叫一個工具、看結果、再想的 agent 迴圈，下一節細講）："
      - "多數有進步：24 個「模型 × benchmark（標準測試任務）」格子中，有 23 格為正；但 HotpotQA（需要跨多篇資料推理的問答）幾乎沒有增益（最大 +1.7）。"
      - "整體有用，但要打三個折扣：HotpotQA 幾乎沒進步；有些勝利是對手退步造成的；比較是否公平，還有一個我懷疑的潛在混淆（這是我的推測，論文沒有承認）。"
      - "所以對每格最強 baseline 的 19 勝，有一部分是對手退步"
      - "PG 的驗證閘門額外用了驗證集（HotpotQA 1,000 題、MultiChallenge 100 題，Appendix B.1），論文沒說 baseline 能不能用驗證集。"
      - "這個實驗最站得住的一句話，是手寫的專家圖在 MultiChallenge 上可能讓成績崩掉，有驗證閘門的分批演化可以救回來（這份資料只看得到結果，看不出原因）。"
    anchor_type: 部落格判斷
    comparison_target: 同模型、同 solver 的無記憶 ReAct（實驗一）；無圖基準與未演化專家圖（實驗三）
    qualifiers:
      - text: 實驗一評測範圍是 4 個 LLM、6 個 benchmark、7 個 baseline
        source_quote: "4 個 LLM（Claude Sonnet 4.6、Gemini 3.1 Pro、Gemini 3.5 Flash、Grok 4.1 Fast），6 個 benchmark，7 個對照做法（baseline）。"
      - text: 實驗三只用 Gemini 3.5 Flash，在 HotpotQA（1,000 題）與 MultiChallenge（56 題）上測
        source_quote: "同一個模型（Gemini 3.5 Flash，Appendix D.3）…HotpotQA 測試 1,000 題，1 題等於 0.1 分；MultiChallenge 在這張表只用其中 56 題"
      - text: 在 HotpotQA 上，專家圖起點時演化沒有額外加分；MultiChallenge 的資料也分不出空圖起步能不能追平專家圖
        source_quote: "在 HotpotQA 上，專家圖起點時演化沒有額外加分。…至於空圖起步能不能追平專家圖，MultiChallenge 的資料分不出來。"
    importance: 1
    status: normal

  - id: c2
    role: context
    text: "Procedural Graph（PG）出自 Google 論文《Procedural Graphs: Self-Evolving Execution Structures for LLM Agents》，把 agent 的做事流程存成可編輯的有向圖；推論時只取目前位置附近一小段由另一個 LLM 翻成提示，離線時由 LLM 修改這張圖並交給獨立驗證集把關"
    source_quotes:
      - "這篇整理 Google 的論文 *Procedural Graphs: Self-Evolving Execution Structures for LLM Agents*（arXiv 2609.09153v1，2026 年九月）。它的做法分兩半："
      - "推論時（agent 實際在做事）：把 agent 的「做事流程」存成一張可編輯的有向圖（節點是步驟，箭頭指向下一步）。每一步只取 agent 目前所在位置附近的一小段，由另一個 LLM 翻成提示。"
      - "離線時（事先準備、改進這張圖）：讓一個 LLM 負責修改這張圖；改得有沒有用，交給獨立的驗證集（一組沒拿去訓練的題目）決定。"
    anchor_type: 設計參數
    qualifiers:
      - text: 每一步多一次 LLM 呼叫，token 大約是不用圖的 1.33 到 1.85 倍
        source_quote: "每一步多一次 LLM 呼叫，token（模型處理文字的計量單位）大約是不用圖的 1.33 到 1.85 倍。"
    importance: 2
    status: normal

  - id: c3
    role: context
    text: 實驗一涵蓋 4 個 LLM（Claude Sonnet 4.6、Gemini 3.1 Pro、Gemini 3.5 Flash、Grok 4.1 Fast）、6 個 benchmark（HotpotQA 1,000 題、MultiChallenge 166 題、GDPval 44 題、ALFWorld 134 題、τ-bench 115 題、BFCL v3 100 題）與 7 個 baseline，所有方法共用同一個 ReAct solver、全部用 greedy decoding
    source_quotes:
      - "設定（Section 4）：4 個 LLM（Claude Sonnet 4.6、Gemini 3.1 Pro、Gemini 3.5 Flash、Grok 4.1 Fast），6 個 benchmark，7 個對照做法（baseline）。所有方法共用同一個 ReAct solver，只差經驗怎麼存、怎麼用。guidance model 與 refiner 和 solver 用同一個 LLM，全部用 greedy decoding。"
      - "HotpotQA Acc. | 多跳問答的答案是否正確（LLM 評審判斷與標準答案等價） | 1,000"
      - "MultiChallenge Acc. | 多輪對話中，是否記得並遵守先前的指令（LLM 評審的整體成功率） | 166"
      - "GDPval Rubric Score | 專業交付物按每題評分表打分的平均 | 44"
      - "ALFWorld Success | 虛擬家庭任務的成功率，動作順序要求嚴格 | 134"
      - "\\( \\tau \\)-bench Pass@1 | 客服情境，最後資料庫狀態是否等於標準答案的比例 | 115"
      - "BFCL v3 Acc. | 多輪函式呼叫的準確率 | 100"
    anchor_type: 設計參數
    numeric_kind: non_comparative
    numeric_reason: 計數
    qualifiers:
      - text: GDPval 只有 44 題，一題約 2.3 分，小差距很容易只是雜訊
        source_quote: "GDPval 只有 44 題，一題約 2.3 分，小差距很容易只是雜訊。"
    importance: 3
    status: normal

  - id: c4
    role: context
    text: 實驗一的七個 baseline 中，Vanilla ReAct 什麼都不存，其餘 6 個是學習型做法（MemoryBank、RAP、ExpeL、AWM 存文字記憶或工作流；AutoGuide 存條件式指引；KnowAgent 存動作轉移文字規則）；與 PG 最近的是 AutoGuide（指引彼此獨立、未連成圖）與 KnowAgent（靜態文字、不依位置只取一段）
    source_quotes:
      - "七個對照做法裡，1 個是不用任何記憶的 ReAct，其餘 6 個是學習型做法。"
      - "七個對照做法大致可以這樣分：Vanilla ReAct 什麼都不存；MemoryBank、RAP、ExpeL、AWM 存的是經驗摘要、歷史軌跡、歸納出的心得或工作流這類文字；AutoGuide 存「在狀態 X 做 Y」的條件式指引；KnowAgent 存「哪個動作後可接哪個」的規則。"
      - "AutoGuide：論文自己說最接近（Appendix A.4）。同樣是「情境對應動作」，也是每步檢索。差別是 AutoGuide 的指引彼此獨立，PG 把它們連成圖。"
      - "KnowAgent：它存的「動作轉移規則」，概念上就是 PG 的邊，但它是一份靜態文字，沒有圖結構，也不會依當前位置只取一段。"
    anchor_type: 背景說明
    numeric_kind: non_comparative
    numeric_reason: 計數
    importance: 4
    status: normal

  - id: c5
    role: anchor
    text: 實驗一用 PG 減去無記憶 ReAct（同模型、同 solver），24 格中 23 格為正，唯一為負的是 Claude Sonnet 4.6 的 HotpotQA（-0.10 分）；HotpotQA 幾乎沒有增益（最大只有 +1.70，小於該列的信賴區間寬度），其餘五個 benchmark 介於 +3.48 到 +22.39 分
    source_quotes:
      - "乾淨對照：用 PG 減去無記憶 ReAct，同一個模型、同一個 solver，單位是分。"
      - "24 格中 23 格為正，唯一為負的是 Claude 的 HotpotQA（-0.10）。"
      - "Claude Sonnet 4.6 | -0.10 | +6.03 | +5.26 | +6.71 | +7.82 | +6.00"
      - "HotpotQA 幾乎沒有增益，最大只有 +1.7，小於該列的信賴區間寬度。其餘五個 benchmark 是 +3.48 到 +22.39。"
      - "Grok 4.1 Fast | +1.70 | +18.68 | +13.96 | +13.43 | +3.48 | +8.00"
    anchor_type: 部落格考證
    comparison_target: 同模型、同 solver 的無記憶 ReAct（Vanilla ReAct）
    qualifiers:
      - text: 實驗一在 4 個 LLM 與 6 個 benchmark 上評測；其中 GDPval 只有 44 題，1 題約 2.3 分
        source_quote: "GDPval 只有 44 題，一題約 2.3 分，小差距很容易只是雜訊。"
    figures:
      - file: figures/procedural-graphs/table1.png
        article: procedural-graphs
        src: table1.png
        caption: 表 3 — 各 LLM 與 benchmark 的主結果，括號內為 95% 信賴區間。（來源：原始論文 Table 1。）
        sha256: 28050c33c59bb811aaf0c2e81fec1cc451ff02af2e63cb106e2d234f2b4d1533
    importance: 5
    status: normal

  - id: c6
    role: anchor
    text: 論文自己宣稱對每格最強的 baseline，PG 在 24 格中有 21 格排第一或並列第一（19 勝、2 平、3 敗）；3 敗是 Claude 的 HotpotQA、Grok 的 ALFWorld 與 τ-bench，2 平是 Claude 與 Gemini 3.5 Flash 的 MultiChallenge
    source_quotes:
      - "和每格最強的對照做法比，是論文自己的宣稱：PG 在 24 個「模型 × benchmark」格子中，有 21 格排第一或並列第一"
      - "論文的宣稱（Section 5.1）：對每格最強的 baseline，PG 是 19 勝、2 平、3 敗。3 敗是 Claude 的 HotpotQA、Grok 的 ALFWorld 與 \\( \\tau \\)-bench；2 平是 Claude 與 Gemini 3.5 Flash 的 MultiChallenge。"
    anchor_type: 實驗結果
    comparison_target: 24 格中每格最強的 baseline
    qualifiers:
      - text: 不少 baseline 本身比無記憶 ReAct 還差，對最強 baseline 的 19 勝有一部分是對手退步造成的
        source_quote: "「贏 baseline」要打折，因為不少 baseline 本身比無記憶還差。…所以對每格最強 baseline 的 19 勝，有一部分是對手退步，和無記憶對照才看得出 PG 本身的貢獻。"
      - text: blog 推測存在潛在混淆：PG 額外用了驗證集，但論文沒說學習型 baseline 能不能用驗證集
        source_quote: "論文說所有學習型 baseline 吃同樣的訓練軌跡，但 PG 的驗證閘門額外用了驗證集（HotpotQA 1,000 題、MultiChallenge 100 題，Appendix B.1），論文沒說 baseline 能不能用驗證集。"
    figures:
      - file: figures/procedural-graphs/table1.png
        article: procedural-graphs
        src: table1.png
        caption: 表 3 — 各 LLM 與 benchmark 的主結果，括號內為 95% 信賴區間。（來源：原始論文 Table 1。）
        sha256: 28050c33c59bb811aaf0c2e81fec1cc451ff02af2e63cb106e2d234f2b4d1533
    importance: 6
    status: normal

  - id: c7
    role: evaluation
    text: 「贏 baseline」要打折，因為不少 baseline 本身比無記憶還差（例如 Gemini 3.1 Pro 的 ALFWorld，無記憶是 94.78，MemoryBank 是 85.07，RAP 是 80.60），和無記憶對照才看得出 PG 本身的貢獻
    source_quotes:
      - "「贏 baseline」要打折，因為不少 baseline 本身比無記憶還差。例如 Gemini 3.1 Pro 的 ALFWorld，無記憶是 94.78，MemoryBank 是 85.07，RAP 是 80.60。所以對每格最強 baseline 的 19 勝，有一部分是對手退步，和無記憶對照才看得出 PG 本身的貢獻。"
    anchor_type: 部落格考證
    comparison_target: 同模型同任務的無記憶 ReAct（94.78）
    figures:
      - file: figures/procedural-graphs/table1.png
        article: procedural-graphs
        src: table1.png
        caption: 表 3 — 各 LLM 與 benchmark 的主結果，括號內為 95% 信賴區間。（來源：原始論文 Table 1。）
        sha256: 28050c33c59bb811aaf0c2e81fec1cc451ff02af2e63cb106e2d234f2b4d1533
    importance: 7
    status: normal

  - id: c8
    role: evaluation
    text: blog 提出一個論文沒有承認的潛在混淆：論文說所有學習型 baseline 吃同樣的訓練軌跡，但 PG 的驗證閘門額外用了驗證集（HotpotQA 1,000 題、MultiChallenge 100 題），論文沒說 baseline 能不能用驗證集
    source_quotes:
      - "論文說所有學習型 baseline 吃同樣的訓練軌跡，但 PG 的驗證閘門額外用了驗證集（HotpotQA 1,000 題、MultiChallenge 100 題，Appendix B.1），論文沒說 baseline 能不能用驗證集。"
      - "比較是否公平，還有一個我懷疑的潛在混淆（這是我的推測，論文沒有承認）。"
    anchor_type: 部落格推論
    numeric_kind: non_comparative
    numeric_reason: 計數
    importance: 8
    status: normal

  - id: c9
    role: context
    text: 實驗三使用 Gemini 3.5 Flash，在 HotpotQA（1,000 題，看答案字串與標準答案完全相同的 Exact Match，1 題等於 0.1 分）與 MultiChallenge（只用 56 題，看整段對話指令都遵守的 Overall，1 題等於 1.79 分）比較五種建構模式：手寫專家圖（不更新、一次大改、分批演化）與空圖 Start → End（一次大改、分批演化），其中只有分批演化有驗證閘門
    source_quotes:
      - "設定：同一個模型（Gemini 3.5 Flash，Appendix D.3），改變「圖從哪來、怎麼更新」，比較五種組合（Appendix D.2）："
      - "1 | 手寫專家圖 | 不更新 | 無"
      - "2 | 手寫專家圖 | 跑完整個訓練集後一次大改 | 無"
      - "3 | 手寫專家圖 | 分批演化 | 有"
      - "4 | 空圖（Start → End） | 一次大改 | 無"
      - "5 | 空圖 | 分批演化 | 有"
      - "HotpotQA 看答案是否和標準答案完全相同（EM），MultiChallenge 看整段對話的指令是否都遵守（Overall）。HotpotQA 測試 1,000 題，1 題等於 0.1 分；MultiChallenge 在這張表只用其中 56 題（實驗一用 166 題，論文沒說為什麼這裡只用 56 題），1 題等於 1.79 分，所以 MultiChallenge 上每一題的差距都不小。"
    anchor_type: 設計參數
    comparison_target: 各自測試集總題數（HotpotQA 1,000 題、MultiChallenge 56 題）下每題佔分
    qualifiers:
      - text: 實驗三與實驗二的 MultiChallenge 題目子集不同，無圖基準分別是 87.50 與 80.27，數字不能跨實驗比較
        source_quote: "同樣用 Gemini 3.5 Flash、同樣不用圖，MultiChallenge 的基準在實驗二是 80.27、在這裡是 87.50，原因是兩個實驗用的題目子集不同（表 4 的 caption 寫明是 fixed subsets），數字不能跨實驗比較。"
    importance: 9
    status: normal

  - id: c10
    role: anchor
    text: 在 MultiChallenge（56 題）上，手寫專家圖會讓成績崩掉：無圖是 87.50（49/56），模式 1（手寫專家圖不更新）掉到 58.93（33/56，比無圖少 16 題），模式 2（專家圖＋一次大改）掉到 53.57（30/56，少 19 題）；模式 3（專家圖＋分批演化）回到 92.86（52/56，比無圖多 3 題、比模式 1 高 +33.93 分）
    source_quotes:
      - "無圖 | 58.8 | - | 87.50（49/56） | -"
      - "1 手寫專家圖 | 62.8 | +4.0 | 58.93（33/56） | -16 題"
      - "2 專家圖＋一次大改 | 63.8 | +5.0 | 53.57（30/56） | -19 題"
      - "3 專家圖＋分批演化 | 63.1 | +4.3 | 92.86（52/56） | +3 題"
      - "模式 1、2 比無圖少 16、19 題，模式 3 從模式 1 的 33 題回到 52 題，差距為 92.86 − 58.93 = +33.93，和論文報的數字一致。"
    anchor_type: 實驗結果
    comparison_target: 無圖基準（87.50，49/56）與模式 1 手寫專家圖（58.93，33/56）
    qualifiers:
      - text: 使用 Gemini 3.5 Flash，MultiChallenge 在表 5 只測 56 題，且這份資料只看得到結果、看不出崩盤與救回的原因
        source_quote: "這個實驗最站得住的一句話，是手寫的專家圖在 MultiChallenge 上可能讓成績崩掉，有驗證閘門的分批演化可以救回來（這份資料只看得到結果，看不出原因）。"
    figures:
      - file: figures/procedural-graphs/table2.png
        article: procedural-graphs
        src: table2.png
        caption: 表 5 — 五種建構模式在 HotpotQA 與 MultiChallenge 上的表現。（來源：原始論文 Table 2。）
        sha256: 84fe01d2d2278c9678c48073235151aa5a27cbf8556821f85f50276a22042c24
    importance: 10
    status: normal

  - id: c11
    role: evaluation
    text: 在 MultiChallenge（56 題）上，模式 3（52/56）、模式 4（空圖＋一次大改，50/56，89.29）、模式 5（空圖＋分批演化，51/56，91.07）和無圖（49/56）只差 1 到 3 題，blog 認為不能據此說誰比誰好，也不能說「空圖起步追平專家圖」
    source_quotes:
      - "無圖 | 58.8 | - | 87.50（49/56） | -"
      - "3 專家圖＋分批演化 | 63.1 | +4.3 | 92.86（52/56） | +3 題"
      - "4 空圖＋一次大改 | 55.4 | -3.4 | 89.29（50/56） | +1 題"
      - "5 空圖＋分批演化 | 66.3 | +7.5 | 91.07（51/56） | +2 題"
      - "但模式 3、4、5 彼此只差 1 題、和無圖只差 1 到 3 題，不能據此說誰比誰好，也不能說「空圖起步追平專家圖」。"
    anchor_type: 部落格判斷
    comparison_target: 無圖基準（49/56）與模式 3、4、5 彼此之間
    qualifiers:
      - text: 使用 Gemini 3.5 Flash，MultiChallenge 只測 56 題，1 題等於 1.79 分
        source_quote: "MultiChallenge 在這張表只用其中 56 題（實驗一用 166 題，論文沒說為什麼這裡只用 56 題），1 題等於 1.79 分"
    figures:
      - file: figures/procedural-graphs/table2.png
        article: procedural-graphs
        src: table2.png
        caption: 表 5 — 五種建構模式在 HotpotQA 與 MultiChallenge 上的表現。（來源：原始論文 Table 2。）
        sha256: 84fe01d2d2278c9678c48073235151aa5a27cbf8556821f85f50276a22042c24
    importance: 11
    status: normal

  - id: c12
    role: anchor
    text: 在 HotpotQA（1,000 題 EM）上，只有模式 5（空圖＋分批演化，66.3）明顯最好，比無圖（58.8）多 7.5 分（多答對 75 題）、比同為空圖起點的模式 4（一次大改，55.4，比無圖少 34 題）高 10.9 分
    source_quotes:
      - "HotpotQA 測試 1,000 題，1 題等於 0.1 分"
      - "無圖 | 58.8 | - | 87.50（49/56） | -"
      - "4 空圖＋一次大改 | 55.4 | -3.4 | 89.29（50/56） | +1 題"
      - "5 空圖＋分批演化 | 66.3 | +7.5 | 91.07（51/56） | +2 題"
      - "HotpotQA 只有模式 5（空圖＋分批演化）明顯最好。它比無圖多答對 75 題。模式 4 和 5 都從空圖出發，EM 差 10.9；比無圖還差的模式 4（空圖＋一次大改），則少答對 34 題。"
    anchor_type: 實驗結果
    comparison_target: 無圖基準（58.8）與模式 4 空圖＋一次大改（55.4）
    qualifiers:
      - text: 使用 Gemini 3.5 Flash，HotpotQA 測試 1,000 題，指標為 Exact Match
        source_quote: "同一個模型（Gemini 3.5 Flash，Appendix D.3）"
    figures:
      - file: figures/procedural-graphs/table2.png
        article: procedural-graphs
        src: table2.png
        caption: 表 5 — 五種建構模式在 HotpotQA 與 MultiChallenge 上的表現。（來源：原始論文 Table 2。）
        sha256: 84fe01d2d2278c9678c48073235151aa5a27cbf8556821f85f50276a22042c24
    importance: 12
    status: normal

  - id: c13
    role: evidence
    text: 在 HotpotQA 上，專家圖起點時分批演化沒有額外加分：模式 3（專家圖＋分批演化，63.1）只比不更新的模式 1（62.8）高 0.3 分，還低於模式 2（專家圖＋一次大改，63.8）；三個專家圖模式都落在 62.8 到 63.8 之間
    source_quotes:
      - "在 HotpotQA 上，專家圖起點時演化沒有額外加分。模式 3（專家圖＋分批演化，63.1）只比不更新的模式 1（62.8）高 0.3，還低於模式 2（專家圖＋一次大改，63.8）。三個專家圖模式都落在 62.8 到 63.8 之間，空圖起步的模式 5 則是 66.3。"
    anchor_type: 實驗結果
    comparison_target: 模式 1 手寫專家圖不更新（62.8）與模式 2 專家圖＋一次大改（63.8）
    qualifiers:
      - text: 使用 Gemini 3.5 Flash，HotpotQA 測試 1,000 題，指標為 Exact Match
        source_quote: "同一個模型（Gemini 3.5 Flash，Appendix D.3）"
    figures:
      - file: figures/procedural-graphs/table2.png
        article: procedural-graphs
        src: table2.png
        caption: 表 5 — 五種建構模式在 HotpotQA 與 MultiChallenge 上的表現。（來源：原始論文 Table 2。）
        sha256: 84fe01d2d2278c9678c48073235151aa5a27cbf8556821f85f50276a22042c24
    importance: 13
    status: normal
```
