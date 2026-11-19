---
id: jevmem-small-scorer-controls-memory
title: agent 記憶裡的一大串小判斷，答案都只是「是／否」或一個分數；Jev-Mem 把它們全部交給只輸出 0 到 1 分數的小模型 Jev，大 LLM 只在最後寫答案
type_hint: 方法
context_type: bound_to_source
sources:
- article: jev-mem
  article_title: "Jev-Mem：讓小模型打分數管 AI agent 記憶，建構速度進步 8.9 倍"
  url: https://datasciocean.com/paper-intro/jev-mem/
  sections:
  - agent 的記憶裡，藏著一大串小判斷
  - 這些判斷的答案，都只是「是／否」或一個分數
  - System One 判斷、System Two 作答
  - Jev 不寫字，只回答一批是非題
  - 記憶長什麼樣：一句話一個節點，加上四種邊
  - 四種邊各自怎麼建
  - 寫入：每句話的 Jev 成本固定
  - Jev 判斷要不要建邊
  - 實驗：比 MAGMA 快很多，準確度提升主要在對抗題
  - 拿來用之前要知道的限制
  - 總結：三件值得記住的事
  - 每隔一段時間做一次整理
  - 實體抽取與時間邊
  - Jev 的輸入長什麼樣子
  - 用符號寫下一筆觀察與整份記憶
  - 最乾淨的對照：MAGMA 與 Jev-Mem
  first_appearance: true
parent: null
related:
  - jevmem-write-fixed-cost-coarse-filter
  - jevmem-read-plan-expand-stop
  - jevmem-results-gain-source
  - shared-context-batched-judgments
  - decisionrag-tree-navigation-decision-model
  - confidence-three-metrics
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: agent 記憶裡的這些判斷，答案都是「是／否」或一個分數，不是一段文字；判斷很多、又卡在使用者要等的路上，blog 認為這正好是一個只會打分數的小模型能接手的工作。Jev-Mem 的主張是把這些判斷全部交給一個只輸出 0 到 1 之間的分數的小模型 Jev，大 LLM 只在最後負責寫答案
  source_quotes:
  - "它們有個共同點：答案都是「是／否」或一個分數，不是一段文字。"
  - "小結：判斷很多、又卡在使用者要等的路上，而答案都只是一個分數。這正好是一個只會打分數的小模型能接手的工作。"
  - "主張很單純：這些判斷全部交給一個只輸出 0 到 1 分數的小模型 Jev，大 LLM 只在最後負責寫答案。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 定義
  qualifiers:
  - text: 寫入時的候選舊記憶由規則挑出，最多 10 個
    source_quote: "全部收下 → 打類型分數 → 規則挑最多 10 個候選 → 判斷並建邊"
  - text: 實體名稱相同、時間相鄰這兩種邊由規則直接建
    source_quote: "實體名稱相同、時間相鄰這兩種則由規則直接建。"
  - text: 分數不保證經過校準，門檻都是工程設定，不能讀成「有 60% 把握」
    source_quote: "附錄 B.1 明說它們不保證經過校準。所以後文出現的 0.60、0.95 這些門檻都是工程設定，不能讀成「有 60% 把握」。"
  - text: blog 推論「走多深」實際上由規則（層數上限與節點上限）控制，不是 Jev
    source_quote: "（推論）「走多深」實際上是由規則控制（層數上限與節點上限），不是 Jev。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: Jev-Mem 是 UT Dallas 的 Jiang、Li、Li 提出的方法，處理有長期記憶的 agent 每存一句話、每回答一題背後的一連串小判斷。它分三層：只輸出 0 到 1 之間的分數的小模型 Jev 做所有判斷，稱為 System One；中間是共用的記憶；大 LLM 只寫最後的答案，稱為 System Two
  source_quotes:
  - "一個有長期記憶的 agent，每存一句話、每回答一題，背後都要做一連串小判斷"
  - "UT Dallas 的 Jiang、Li、Li 提出的 Jev-Mem，主張很單純：這些判斷全部交給一個只輸出 0 到 1 分數的小模型 Jev，大 LLM 只在最後負責寫答案。"
  - "Jev-Mem 分三層：Jev 做所有判斷，稱為 System One；中間是共用的記憶；大 LLM 只寫最後的答案，稱為 System Two。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  qualifiers:
  - text: 寫入時的候選舊記憶由規則挑出，最多 10 個
    source_quote: "全部收下 → 打類型分數 → 規則挑最多 10 個候選 → 判斷並建邊"
  - text: 實體名稱相同、時間相鄰這兩種邊由規則直接建
    source_quote: "實體名稱相同、時間相鄰這兩種則由規則直接建。"
  - text: 分數不保證經過校準，門檻都是工程設定，不能讀成「有 60% 把握」
    source_quote: "附錄 B.1 明說它們不保證經過校準。所以後文出現的 0.60、0.95 這些門檻都是工程設定，不能讀成「有 60% 把握」。"
  - text: blog 推論「走多深」實際上由規則（層數上限與節點上限）控制，不是 Jev
    source_quote: "（推論）「走多深」實際上是由規則控制（層數上限與節點上限），不是 Jev。"
  figures:
  - file: figures/jev-mem/figure2.png
    article: jev-mem
    src: figure2.png
    caption: 圖 1 — Jev-Mem 架構總覽：上方寫入、中間共用記憶、下方讀取（來源：原始論文 Figure 2。）
    sha256: c615102804836286411dc85602cc5a7ec303fd67c6fd966fc1c64d441595b180
  importance: 2
  status: normal
- id: c3
  role: context
  text: 這些小判斷包括：這句跟哪些舊記憶有關？該往哪裡找？找到的夠不夠？完整一點還包括「這句是哪種記憶」和「找到的哪個最有用」
  source_quotes:
  - "這句跟哪些舊記憶有關？該往哪裡找？找到的夠不夠？"
  - "前面那串判斷，完整一點還包括「這句是哪種記憶」和「找到的哪個最有用」。"
  anchor_type: 背景說明
  importance: 2
  status: normal
- id: c4
  role: context
  text: 現有系統處理這些判斷大致走兩條路：寫死的規則，快但死板；讓大 LLM 逐字生成再解析，懂語意但慢、貴
  source_quotes:
  - "現有系統處理這些判斷，大致走兩條路："
  - "| 寫死的規則 | 快 | 死板 |"
  - "| 讓大 LLM 逐字生成再解析 | 懂語意 | 慢、貴 |"
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c5
  role: mechanism
  text: 這些判斷就卡在使用者要等的那條路上：每多一次大 LLM 呼叫，使用者就多等一次
  source_quotes:
  - "更麻煩的是，這些判斷就卡在使用者要等的那條路上：每多一次大 LLM 呼叫，使用者就多等一次。"
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c6
  role: mechanism
  text: Jev 不生成文字。每次呼叫給它一份「狀態」（例如問題和手上的證據）和一批題目；每道是非題（論文稱為 Noul）由一句指令、true 條件、false 條件組成，Jev 回傳一個 0 到 1 的分數；只能選一個的情況改用選擇題（Choice），回傳選中的選項和分布。同一份狀態的多道題一次問完，因為不生成文字，也就不需要解析輸出
  source_quotes:
  - "Jev 不生成文字。每次呼叫，給它一份「狀態」（例如問題和手上的證據）和一批題目。"
  - '每道是非題，論文稱為 Noul，由一句指令、true 條件、false 條件組成，Jev 回傳一個 \( [0, 1] \) 的分數。'
  - "只能選一個的情況改用選擇題（Choice），回傳選中的選項和分布。同一份狀態的多道題一次問完；因為不生成文字，也就不需要解析輸出。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 2
  status: normal
- id: c7
  role: mechanism
  text: 打個比方：大 LLM 像是要你寫一篇作文再從中找答案，Jev 則是一張只有是非題的答案卡，每題直接塗一個分數
  source_quotes:
  - "打個比方：大 LLM 像是要你寫一篇作文再從中找答案，Jev 則是一張只有是非題的答案卡，每題直接塗一個分數。"
  anchor_type: 部落格舉例
  importance: 4
  status: normal
- id: c8
  role: qualifier
  text: 論文正文把 Jev 的分數叫「機率」，但附錄 B.1 明說它們不保證經過校準，所以 Jev-Mem 的各個門檻都是工程設定，不能讀成把握程度；這些分數是拿來比門檻的工程數字
  source_quotes:
  - "論文正文把這些分數叫「機率」，但附錄 B.1 明說它們不保證經過校準。所以後文出現的 0.60、0.95 這些門檻都是工程設定，不能讀成「有 60% 把握」。"
  - "這些分數是拿來比門檻的工程數字，不是把握程度。"
  anchor_type: 部落格考證
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 2
  status: normal
- id: c9
  role: mechanism
  text: 整條流程可以看成左右兩欄，中間由記憶相連：左欄寫入，每寫入一句最多呼叫 Jev 2 次，流程形狀是一條直線；右欄讀取，每一輪最多呼叫 Jev 2 次（停止判斷、打分），打分完繞回「證據夠了嗎？」形成迴圈，夠了才交給 System Two
  source_quotes:
  - "整條流程可以看成左右兩欄，中間由記憶相連："
  - "| Jev 呼叫次數 | 每寫入一句最多 2 次 | 每一輪最多 2 次（停止判斷、打分） |"
  - "| 流程形狀 | 一條直線 | 打分完繞回「證據夠了嗎？」形成迴圈，夠了才交給 System Two |"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  qualifiers:
  - text: 每 20 次寫入另做一次整理，由 Jev 判斷
    source_quote: "每 20 次寫入做一次整理，只針對第 20 句和它的候選，原句一律保留。Jev 要判斷這兩組問題："
  importance: 3
  status: normal
- id: c10
  role: context
  text: 記憶是一張圖：一句話一個節點，只存一份；節點之間有四種邊（語意、時間、因果、實體），同一對節點可以同時有好幾種。邊的用途是找到一條記憶之後，沿著邊把相關的記憶一起帶出來
  source_quotes:
  - "記憶是一張圖：一句話一個節點，只存一份；節點之間有四種邊，同一對節點可以同時有好幾種。"
  - "邊的用途是：找到一條記憶之後，沿著邊把相關的記憶一起帶出來。"
  - '\mathcal{G}=\{\text{semantic},\ \text{temporal},\ \text{causal},\ \text{entity}\}'
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c11
  role: mechanism
  text: 四種邊裡，語意邊、因果邊靠 Jev 判斷，時間邊和同名實體的實體邊靠規則
  source_quotes:
  - "語意、因果靠 Jev 判斷，時間和同名實體靠規則。"
  anchor_type: 設計參數
  qualifiers:
  - text: 依程式碼，實體邊大致等於「同一個說話者」，時間邊等於「時間相鄰」
    source_quote: "實體與時間邊都是便宜的固定規則，而且連得很寬：實體邊大致等於「同一個說話者」，時間邊等於「時間相鄰」。論文兩者都沒寫清楚，以下依程式碼。"
  importance: 3
  status: normal
- id: c12
  role: evidence
  text: 和同一組作者先前做的記憶系統 MAGMA（也是實驗裡最強的對手）比，在 LoCoMo（一份超長、多場次的對話記憶測驗集）上，Jev-Mem 建構記憶快約 8.9 倍、回答一題的延遲少 37%，總分從 0.700 升到 0.777；不過提升大半來自其中一類「對抗題」，也就是問對話裡從沒說過的事，正確做法是回答不知道
  source_quotes:
  - "比較的對象是同一組作者先前做的記憶系統 MAGMA，也是實驗裡最強的對手。在 LoCoMo（一份超長、多場次的對話記憶測驗集）上，Jev-Mem 建構記憶快約 8.9 倍、回答一題的延遲少 37%，總分從 0.700 升到 0.777。不過提升大半來自其中一類「對抗題」：問對話裡從沒說過的事，正確做法是回答不知道。"
  anchor_type: 部落格考證
  comparison_target: MAGMA（同一組作者先前的記憶系統）
  qualifiers:
  - text: 論文只有兩張表，沒有消融實驗，只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini
    source_quote: "論文只有兩張表，沒有消融實驗（一次拿掉一個元件，看分數掉多少），只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini。"
  - text: 時間題 Jev-Mem 其實略輸 MAGMA
    source_quote: "準確度上，對抗題一項就升了 0.220，比其他四類都多；時間題反而小輸。"
  importance: 2
  status: normal
- id: c13
  role: evaluation
  text: 對論文的三個問題，blog 的回答是：小模型靠「狀態加一批是非題」同時管寫入與讀取；在 LoCoMo 上，弱模型控制記憶沒有拖累總分，只有時間題略輸；適合這種控制的，是一張節點加四種邊的記憶圖，搭配「訂計畫、逐輪展開、判斷停止」的讀取流程
  source_quotes:
  - "小模型靠「狀態加一批是非題」同時管寫入與讀取；在 LoCoMo 上，弱模型控制記憶沒有拖累總分，只有時間題略輸；適合這種控制的，是一張節點加四種邊的記憶圖，搭配「訂計畫、逐輪展開、判斷停止」的讀取流程。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 論文只有兩張表，沒有消融實驗，只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini
    source_quote: "論文只有兩張表，沒有消融實驗（一次拿掉一個元件，看分數掉多少），只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini。"
  importance: 3
  status: normal
- id: c14
  role: evaluation
  text: 可以怎麼用：如果你在做 agent 記憶或 RAG，先檢查流程裡有多少步其實只需要一個「是／否」或分數，那些步驟就是換成小模型打分的候選
  source_quotes:
  - "可以怎麼用：如果你在做 agent 記憶或 RAG，先檢查流程裡有多少步其實只需要一個「是／否」或分數，那些步驟就是換成小模型打分的候選"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c15
  role: evaluation
  text: 至於 Jev-Mem 本身，在更多測驗集與消融實驗出來之前，blog 建議把它當成一個值得嘗試的方向，而不是定論
  source_quotes:
  - "至於 Jev-Mem 本身，在更多測驗集與消融實驗出來之前，把它當成一個值得嘗試的方向，而不是定論。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
```
