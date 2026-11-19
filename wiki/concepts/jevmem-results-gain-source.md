---
id: jevmem-results-gain-source
title: 和架構相同的 MAGMA 比，Jev-Mem 建構快約 8.9 倍、查詢延遲少 37%，總分 +0.077；但準確度的提升大半來自對抗題，時間題其實略輸，而且評估只有一個測驗集、沒有消融
type_hint: 發現
context_type: bound_to_source
sources:
- article: jev-mem
  article_title: "Jev-Mem：讓小模型打分數管 AI agent 記憶，建構速度進步 8.9 倍"
  url: https://datasciocean.com/paper-intro/jev-mem/
  sections:
  - agent 的記憶裡，藏著一大串小判斷
  - System One 判斷、System Two 作答
  - Jev 不寫字，只回答一批是非題
  - 讀取之一：出發前先訂搜尋計畫
  - 預算：每種邊能看幾個鄰居
  - 寫入：每句話的 Jev 成本固定
  - Jev 判斷要不要建邊
  - 每隔一段時間做一次整理
  - 實驗：比 MAGMA 快很多，準確度提升主要在對抗題
  - 先看懂指標
  - 最乾淨的對照：MAGMA 與 Jev-Mem
  - 拿來用之前要知道的限制
  - 總結：三件值得記住的事
  - Jev 的輸入長什麼樣子
  first_appearance: true
parent: null
related:
  - jevmem-small-scorer-controls-memory
  - jevmem-write-fixed-cost-coarse-filter
  - jevmem-read-plan-expand-stop
  - decisionrag-results-gain-source
  - jevact-results-gain-source
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 和架構相同的 MAGMA 相比，Jev-Mem 建構快約 8.9 倍、查詢延遲少 37%，總分 +0.077；準確度的提升大半來自對抗題
  source_quotes:
  - "和架構相同的 MAGMA 相比，Jev-Mem 建構快約 8.9 倍、查詢延遲少 37%，總分 +0.077；準確度的提升大半來自對抗題。"
  anchor_type: 部落格考證
  comparison_target: MAGMA（同一組作者先前、架構相同的記憶系統）
  qualifiers:
  - text: 論文只有兩張表，沒有消融實驗，只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini
    source_quote: "論文只有兩張表，沒有消融實驗（一次拿掉一個元件，看分數掉多少），只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini。"
  - text: 以表格為準，時間題 Jev-Mem 是輸的（0.637，低於 MAGMA 的 0.650）
    source_quote: "正文說「時間題與最佳並列 0.650」，但表 1 裡 Jev-Mem 是 0.637，低於 MAGMA 的 0.650。以表格為準，時間題是輸的。"
  - text: 論文摘要寫的「6.6 倍」是跟建構最快的其他系統 Nemori 比，不是跟 MAGMA 比
    source_quote: "論文摘要寫的「6.6 倍」，是跟建構最快的其他系統 Nemori（1044 秒）比，不是跟架構相同的 MAGMA 比。"
  figures:
  - file: figures/jev-mem/table1.png
    article: jev-mem
    src: table1.png
    caption: 表 1 — 各方法在 LoCoMo 上的準確度（LLM-as-a-Judge，回答模型 gpt-4o-mini）（來源：原始論文 Table 1。）
    sha256: c22c97433cf375e64612c525107bad62c3849b0fe566c964d191d4646abc21e5
  - file: figures/jev-mem/table2.png
    article: jev-mem
    src: table2.png
    caption: 表 2 — 各方法的記憶建構時間與查詢延遲（來源：原始論文 Table 2。）
    sha256: 424639e151477b7fb8372c22ffe963e751b9e6caa2c1d072fc3c4e5cab51a587
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
  importance: 2
  status: normal
- id: c3
  role: context
  text: LoCoMo 是超長、多場次的對話記憶測驗集，題目分五類（多跳、時間、開放領域、單跳、對抗）；其中對抗題問的是對話裡沒說過的事，正確做法是回答不知道
  source_quotes:
  - "LoCoMo：超長、多場次的對話記憶測驗集，題目分五類（多跳、時間、開放領域、單跳、對抗）。其中對抗題問的是對話裡沒說過的事，正確做法是回答不知道。"
  anchor_type: 背景說明
  qualifiers:
  - text: 題型說明是一般知識，論文沒有解釋
    source_quote: "（一般知識，題型說明論文沒有解釋）"
  importance: 2
  status: normal
- id: c4
  role: context
  text: 準確度用 LLM-as-a-Judge 評，讓另一個 LLM 判斷答案是否與標準答案一致，測的是最終答案，不單獨評檢索。建構時間是把整段對話存成記憶的總秒數；查詢延遲是每題從檢索到回答的平均秒數
  source_quotes:
  - "LLM-as-a-Judge：讓另一個 LLM 判斷答案是否與標準答案一致。它測的是最終答案，不單獨評檢索。"
  - "建構時間：把整段對話存成記憶的總秒數。"
  - "查詢延遲：每題從檢索到回答的平均秒數。"
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c5
  role: context
  text: 評估的範圍：論文只有兩張表，沒有消融實驗（一次拿掉一個元件，看分數掉多少），只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini
  source_quotes:
  - "也要先知道評估的範圍：論文只有兩張表，沒有消融實驗（一次拿掉一個元件，看分數掉多少），只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini。"
  anchor_type: 部落格考證
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 2
  status: normal
- id: c6
  role: context
  text: MAGMA 是同一組作者先前的系統，也是最強的對手；依程式碼，Jev-Mem 建在 MAGMA 之上，把控制層換成 Jev，所以這組差距最接近方法本身的貢獻
  source_quotes:
  - "MAGMA 是同一組作者先前的系統，也是最強的對手。（依程式碼）Jev-Mem 建在 MAGMA 之上，把控制層換成 Jev。所以這組差距最接近方法本身的貢獻。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c7
  role: evidence
  text: 建構時間 MAGMA 1404 秒、Jev-Mem 158 秒，約快 8.9 倍；存一整段對話從 1404 秒降到 158 秒
  source_quotes:
  - "| 項目 | MAGMA | Jev-Mem | 差距 |"
  - "| 建構時間（秒） | 1404 | 158 | 約快 8.9 倍 |"
  - "最醒目的是速度：存一整段對話從 1404 秒降到 158 秒。"
  anchor_type: 實驗結果
  comparison_target: MAGMA
  qualifiers:
  - text: 論文只有兩張表，沒有消融實驗，只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini
    source_quote: "論文只有兩張表，沒有消融實驗（一次拿掉一個元件，看分數掉多少），只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini。"
  figures:
  - file: figures/jev-mem/table2.png
    article: jev-mem
    src: table2.png
    caption: 表 2 — 各方法的記憶建構時間與查詢延遲（來源：原始論文 Table 2。）
    sha256: 424639e151477b7fb8372c22ffe963e751b9e6caa2c1d072fc3c4e5cab51a587
  importance: 2
  status: normal
- id: c8
  role: evidence
  text: 查詢延遲 MAGMA 1.47 秒、Jev-Mem 0.93 秒，少 36.7%
  source_quotes:
  - "| 項目 | MAGMA | Jev-Mem | 差距 |"
  - "| 查詢延遲（秒） | 1.47 | 0.93 | −36.7% |"
  anchor_type: 實驗結果
  comparison_target: MAGMA
  qualifiers:
  - text: 論文只有兩張表，沒有消融實驗，只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini
    source_quote: "論文只有兩張表，沒有消融實驗（一次拿掉一個元件，看分數掉多少），只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini。"
  figures:
  - file: figures/jev-mem/table2.png
    article: jev-mem
    src: table2.png
    caption: 表 2 — 各方法的記憶建構時間與查詢延遲（來源：原始論文 Table 2。）
    sha256: 424639e151477b7fb8372c22ffe963e751b9e6caa2c1d072fc3c4e5cab51a587
  importance: 3
  status: normal
- id: c9
  role: evidence
  text: 總分 MAGMA 0.700、Jev-Mem 0.777，差距 +0.077
  source_quotes:
  - "| 項目 | MAGMA | Jev-Mem | 差距 |"
  - "| 總分 | 0.700 | 0.777 | +0.077 |"
  anchor_type: 實驗結果
  comparison_target: MAGMA
  qualifiers:
  - text: 提升大半來自其中一類「對抗題」
    source_quote: "不過提升大半來自其中一類「對抗題」"
  - text: 論文只有兩張表，沒有消融實驗，只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini
    source_quote: "論文只有兩張表，沒有消融實驗（一次拿掉一個元件，看分數掉多少），只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini。"
  figures:
  - file: figures/jev-mem/table1.png
    article: jev-mem
    src: table1.png
    caption: 表 1 — 各方法在 LoCoMo 上的準確度（LLM-as-a-Judge，回答模型 gpt-4o-mini）（來源：原始論文 Table 1。）
    sha256: c22c97433cf375e64612c525107bad62c3849b0fe566c964d191d4646abc21e5
  importance: 2
  status: normal
- id: c10
  role: evidence
  text: 對抗題 MAGMA 0.742、Jev-Mem 0.962，一項就升了 0.220，比其他四類都多
  source_quotes:
  - "| 項目 | MAGMA | Jev-Mem | 差距 |"
  - "| 對抗題 | 0.742 | 0.962 | +0.220 |"
  - "準確度上，對抗題一項就升了 0.220，比其他四類都多"
  anchor_type: 實驗結果
  comparison_target: MAGMA
  qualifiers:
  - text: 論文只有兩張表，沒有消融實驗，只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini
    source_quote: "論文只有兩張表，沒有消融實驗（一次拿掉一個元件，看分數掉多少），只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini。"
  figures:
  - file: figures/jev-mem/table1.png
    article: jev-mem
    src: table1.png
    caption: 表 1 — 各方法在 LoCoMo 上的準確度（LLM-as-a-Judge，回答模型 gpt-4o-mini）（來源：原始論文 Table 1。）
    sha256: c22c97433cf375e64612c525107bad62c3849b0fe566c964d191d4646abc21e5
  importance: 2
  status: normal
- id: c11
  role: evidence
  text: 其他三類的進步較小：開放領域 0.517 → 0.618（+0.101）、多跳 0.528 → 0.623（+0.095）、單跳 0.776 → 0.802（+0.026）
  source_quotes:
  - "| 項目 | MAGMA | Jev-Mem | 差距 |"
  - "| 開放領域 | 0.517 | 0.618 | +0.101 |"
  - "| 多跳 | 0.528 | 0.623 | +0.095 |"
  - "| 單跳 | 0.776 | 0.802 | +0.026 |"
  anchor_type: 實驗結果
  comparison_target: MAGMA
  qualifiers:
  - text: 論文只有兩張表，沒有消融實驗，只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini
    source_quote: "論文只有兩張表，沒有消融實驗（一次拿掉一個元件，看分數掉多少），只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini。"
  figures:
  - file: figures/jev-mem/table1.png
    article: jev-mem
    src: table1.png
    caption: 表 1 — 各方法在 LoCoMo 上的準確度（LLM-as-a-Judge，回答模型 gpt-4o-mini）（來源：原始論文 Table 1。）
    sha256: c22c97433cf375e64612c525107bad62c3849b0fe566c964d191d4646abc21e5
  importance: 3
  status: normal
- id: c12
  role: evidence
  text: 時間題 MAGMA 0.650、Jev-Mem 0.637（−0.013）。論文正文說「時間題與最佳並列 0.650」，但表格裡 Jev-Mem 是 0.637，低於 MAGMA 的 0.650；以表格為準，時間題是輸的
  source_quotes:
  - "| 項目 | MAGMA | Jev-Mem | 差距 |"
  - "| 時間 | 0.650 | 0.637 | −0.013 |"
  - "正文說「時間題與最佳並列 0.650」，但表 1 裡 Jev-Mem 是 0.637，低於 MAGMA 的 0.650。以表格為準，時間題是輸的。"
  anchor_type: 實驗結果
  comparison_target: MAGMA
  qualifiers:
  - text: 論文只有兩張表，沒有消融實驗，只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini
    source_quote: "論文只有兩張表，沒有消融實驗（一次拿掉一個元件，看分數掉多少），只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini。"
  figures:
  - file: figures/jev-mem/table1.png
    article: jev-mem
    src: table1.png
    caption: 表 1 — 各方法在 LoCoMo 上的準確度（LLM-as-a-Judge，回答模型 gpt-4o-mini）（來源：原始論文 Table 1。）
    sha256: c22c97433cf375e64612c525107bad62c3849b0fe566c964d191d4646abc21e5
  importance: 2
  status: normal
- id: c13
  role: qualifier
  text: 論文摘要寫的「6.6 倍」，是跟建構最快的其他系統 Nemori（1044 秒）比，不是跟架構相同的 MAGMA 比
  source_quotes:
  - "論文摘要寫的「6.6 倍」，是跟建構最快的其他系統 Nemori（1044 秒）比，不是跟架構相同的 MAGMA 比。"
  anchor_type: 部落格考證
  comparison_target: Nemori（建構最快的其他系統）
  qualifiers:
  - text: 論文只有兩張表，沒有消融實驗，只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini
    source_quote: "論文只有兩張表，沒有消融實驗（一次拿掉一個元件，看分數掉多少），只報告 LoCoMo 一個測驗集，負責寫答案的模型是 gpt-4o-mini。"
  figures:
  - file: figures/jev-mem/table2.png
    article: jev-mem
    src: table2.png
    caption: 表 2 — 各方法的記憶建構時間與查詢延遲（來源：原始論文 Table 2。）
    sha256: 424639e151477b7fb8372c22ffe963e751b9e6caa2c1d072fc3c4e5cab51a587
  importance: 2
  status: normal
- id: c14
  role: evaluation
  text: blog 推論，對抗題大幅提升，可能來自停止規則要求證據「足夠、不缺、不矛盾」才停，比較不會拿不相關的記憶硬答；不過記憶裡根本沒有答案時，「值得再找」的分數可能一直偏高，只能靠硬上限停下
  source_quotes:
  - "（推論）對抗題大幅提升，可能來自停止規則要求證據「足夠、不缺、不矛盾」才停，比較不會拿不相關的記憶硬答。不過記憶裡根本沒有答案時，「值得再找」的分數可能一直偏高，只能靠硬上限停下"
  anchor_type: 部落格推論
  qualifiers:
  - text: 論文沒報告兩條停止規則各被觸發幾次
    source_quote: "論文也沒報告兩條停止規則各被觸發幾次"
  importance: 3
  status: normal
- id: c15
  role: evaluation
  text: 評估很薄：只有 LoCoMo 一個測驗集、兩張表，沒有消融實驗，看不出哪個元件貢獻了多少
  source_quotes:
  - "評估很薄。只有 LoCoMo 一個測驗集、兩張表，沒有消融實驗，看不出哪個元件貢獻了多少。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c16
  role: evaluation
  text: 超參數沒交代：讀取時「每種邊能看幾個鄰居」的總預算 80 怎麼選、跑兩張主結果表用 repo 裡哪份設定檔（依程式碼，repo 有兩份），論文都沒說
  source_quotes:
  - "往外找之前，Jev 只看問題，一次決定三件事：開哪幾種邊（路由）、每種邊能看幾個鄰居（預算）"
  - '總共 \( B = 80 \) 張，每種開啟的邊先保底 1 張'
  - "超參數沒交代。預算 80 怎麼選、跑表 1、表 2 用 repo 裡哪份設定檔（依程式碼，repo 有兩份），論文都沒說"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 3
  status: normal
- id: c17
  role: evaluation
  text: 寫入時每 20 次寫入做一次整理（檢查重複、矛盾、過時等），但沒有關掉整理的對照，定期整理對結果的貢獻未知
  source_quotes:
  - "每 20 次寫入做一次整理"
  - "它們之間是否重複、矛盾、過時，或值得補一條連結？"
  - "定期整理的貢獻未知。沒有關掉整理的對照"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 3
  status: normal
- id: c18
  role: evaluation
  text: 在更多測驗集與消融實驗出來之前，blog 建議把 Jev-Mem 當成一個值得嘗試的方向，而不是定論
  source_quotes:
  - "至於 Jev-Mem 本身，在更多測驗集與消融實驗出來之前，把它當成一個值得嘗試的方向，而不是定論。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
```
