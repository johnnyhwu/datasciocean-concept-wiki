---
id: evoontology-evolution-loop-gate-first
title: 自我演化系統的四步循環是診斷、歸因、局部修補、閘門；其中閘門最不能省，先確保有一個嚴謹的驗收閘門，再談怎麼把診斷與歸因做細
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: evoontology
  article_title: "EvoOntology 解析：在 data agent 與資料之間，加一層會自己演化的 ontology"
  url: https://datasciocean.com/paper-intro/evoontology/
  sections:
  - data agent 每次都從零摸資料，把說明整包塞進 prompt 還可能更糟
  - 自我演化迴圈：診斷、歸因、局部修補、閘門
  - Diagnose 與 Attribute：先判斷問題出在 Content、Tool 還是 Schema
  - Patch：一次候選修補只能動一層
  - Gate：候選要在同條件下贏過父版本至少 τ 分才轉正
  - 候選逐一處理，被拒絕的也會留下紀錄
  - workload 怎麼分給不同用途，以及 split-and-swap 評估法
  - 實驗結果：主動查詢勝過整包塞 prompt，閘門最不能省
  - Ablation：Gate、Mappings、Tool 層各自貢獻多少
  - 演化到底跑了幾輪：因 backbone 與 benchmark 而異
  - 評價：貢獻中等偏架構層面，細節缺口不小
  - 跨 backbone 遷移：換底層模型，ontology 幾乎要重新演化
  - 把兩輪演化串成一條時間線
  - 冷啟動：不靠人工、不看標準答案，生出第一版 ontology
  - 主結果：六個 backbone 全贏，整包塞 prompt 反而掉分
  - Schema Layer：像 class 定義的規則書，改它不動既有知識
  - 帶得走的收穫：該不該整包塞，看量有多大；自我演化的骨架，閘門先行
  first_appearance: true
parent: null
related:
  - evoontology-three-layer-ontology
  - evoontology-query-over-prompt-stuffing
  - evoontology-limits-backbone-and-cold-start
  - skill-pack-vs-ontology-graph
  - skillopt-blind-acceptance-gate
  - subagent-fold-eval-gated-migration
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 自我演化系統的四步循環是 diagnose（找反覆失敗模式）、attribute（先分類問題屬於哪個子系統）、patch（局部修補、一次只動一層）、gate（配對驗證，候選與父版本同條件比較）；其中 gate 是整個骨架裡最不能省的一步，對任何想做「agent 自我優化知識庫或 skill 庫」的系統，可以直接借用的優先順序是先確保有一個嚴謹的驗收閘門，再談怎麼把 diagnose 與 attribute 做細
  source_quotes:
  - "自我演化系統的四步循環。** 也就是 diagnose（找反覆失敗模式）、attribute（先分類問題屬於哪個子系統）、patch（局部修補、一次只動一層）、gate（配對驗證，候選與父版本同條件比較）。"
  - "其中 **gate 是整個骨架裡最不能省的一步**"
  - "對任何想做「agent 自我優化知識庫或 skill 庫」的系統，這是可以直接借用的優先順序：先確保有一個嚴謹的驗收閘門，再談怎麼把 diagnose 與 attribute 做細。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 「Gate 的貢獻最大」來自 DDR-Bench 上的消融
    source_quote: "演化迴圈裡 Gate 的貢獻最大（DDR-Bench 消融）"
  - text: 這個骨架的價值不在於是這篇論文原創，而在於每一步都有明確的設計理由，且 ablation 量化了每一步的貢獻
    source_quote: "這個骨架的價值不在於是這篇論文原創，而在於每一步都有明確的設計理由，且 ablation 量化了每一步的貢獻。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: "blog 在論文《EvoOntology: A Self-Evolving Ontology Layer for Data Agents》的解析裡談這個骨架，說論文給出的具體答案落在這個更通用的骨架上：data agent（根據自然語言指令操作資料庫表格、CSV、文件、log 這類異質資料的 AI agent）事前不認識資料、每次都要重新摸索，EvoOntology 在 agent 與資料之間放一層可查詢、會演化的 ontology（blog 建議先把它理解成一份結構化的領域知識），由 Schema、Content、Tool 三層組成"
  source_quotes:
  - "EvoOntology: A Self-Evolving Ontology Layer for Data Agents"
  - "**論文對這個問題給出的具體答案，落在一個更通用的骨架上："
  - "一種根據自然語言指令，去操作資料庫表格、CSV、文件、log 這類異質資料的 AI agent"
  - "EvoOntology 想解決的是 data agent 事前不認識資料、每次都要重新摸索的問題，做法是在 agent 與資料之間放一層可查詢、會演化的 ontology，由 Schema、Content、Tool 三層組成。"
  - "先把它理解成一份結構化的領域知識"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: 冷啟動建好的初始 ontology 是靠 workload（訓練用的查詢集合）猜出來的，agent 真的拿去用之後，一定會暴露出「哪裡漏了」「哪裡誤導了」；自我演化迴圈要做的，就是持續把這些問題變成對 ontology 的具體修補
  source_quotes:
  - "冷啟動建好的初始 ontology 是靠 workload 猜出來的，agent 真的拿去用之後，一定會暴露出「哪裡漏了」「哪裡誤導了」。自我演化迴圈要做的，就是持續把這些問題變成對 ontology 的具體修補。"
  - "訓練用的查詢集合（workload）"
  anchor_type: 部落格推論
  importance: 2
  status: normal
- id: c4
  role: mechanism
  text: Diagnose 與 Attribute：evolution agent 從歷史執行軌跡與目前的 ontology 抽出反覆出現的訊號，再把每個訊號判給 Content、Tool 或 Schema 其中一層。用財務案例走一次：「依通路拆分成本」的問題，ontology 找不到對應的 Term 或 Mapping，判給 Content（缺的是概念本身）；「固定匯率下的成本」的問題，agent 沒有工具可以做幣別轉換，判給 Tool（缺的是執行能力）
  source_quotes:
  - "*\"Given historical trajectories \\( T_t \\) and the current state \\( L_t \\), the evolution agent extracts recurrent signatures \\( \\Sigma_t = \\text{analyze}(T_t, L_t) \\). The agent assigns the signature to Content, Tool, or Schema through \\( \\alpha : \\Sigma_t \\to \\{C, T, S\\} \\).\"*"
  - "帶入圖 2 的案例走一次。"
  - "σ1 = 問題牽涉「依通路（channel）拆分成本」，"
  - "但 ontology 找不到對應的 Term 或 Mapping"
  - "σ2 = 問題牽涉「固定匯率下的成本」，"
  - "但 agent 沒有工具可以做幣別轉換"
  - "α(σ1) = Content   （缺的是概念本身，內容層的缺口）"
  - "α(σ2) = Tool      （缺的不是概念，是執行能力，工具層的缺口）"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c5
  role: mechanism
  text: 先分類「屬於哪一層」，才不會拿錯的層級去修問題，例如把明明是工具不夠的問題，誤判成「加個新概念就好」
  source_quotes:
  - "先分類「屬於哪一層」的重要性在於，才不會拿錯的層級去修問題，例如把明明是工具不夠的問題，誤判成「加個新概念就好」。"
  anchor_type: 部落格推論
  importance: 3
  status: normal
- id: c6
  role: mechanism
  text: Patch：針對歸因完成的訊號生出一個候選新狀態，規則是一次候選修補只能動一層。一個假設需要好幾個互相依賴的 Content 物件才能完整實現時，可以一起更新，因為它們都屬於 Content 這同一層；財務案例裡「新增 Term:Channel 加它的 Mapping」（動 Content）與「新增 FX Convert 工具」（動 Tool）是兩個各自獨立的候選，不會合併成同時動兩層的修補
  source_quotes:
  - "針對歸因完成的訊號，真的動手生出一個修補方案，規則是**一次候選修補只能動一層**。"
  - "*\"For an attributed signature \\( \\sigma \\), the agent proposes \\( L'_t = \\text{patch}(L_t, \\sigma, \\alpha(\\sigma)) \\). Each candidate modifies one level only.\"*"
  - "如果一個假設需要好幾個**互相依賴**的 Content 物件才能完整實現，這些物件可以一起更新，這不違反「一次只動一層」，因為它們都屬於 Content 這同一層。"
  - "α 判定 Content → patch：新增 Term:Channel + Mapping"
  - "α 判定 Tool    → patch：新增 Tool 3: FX Convert"
  - "這是兩個**各自獨立**的候選修補，一個動 Content、一個動 Tool，不會合併成同時動兩層的修補。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c7
  role: mechanism
  text: Gate：候選和目前正式生效的父版本，拿同一份驗證題目 V、同樣的取樣設定與互動輪數上限各跑一次；打分函式要標記 backbone（驅動 agent 的底層 LLM），因為同一個候選換一個 LLM 來用，表現可能不一樣；候選的分數要比父版本高出至少門檻 τ，才會取代它，否則維持原狀。V 是從訓練 workload 切出來、專門保留給驗證用的那份。把其他變因全部鎖死，讓分數差異只可能來自 ontology 改了什麼
  source_quotes:
  - "**backbone（骨幹模型）** 指驅動這個 agent 的底層 LLM 本身"
  - "公式裡之所以要特別標記 backbone，是因為同一個 ontology 候選，換一個 LLM 來用，表現可能不一樣。"
  - "候選和目前正式生效的版本，拿同一份驗證題目、同樣的設定各跑一次；候選的分數要比現在的版本高出至少"
  - "才會取代它，否則維持原狀。"
  - "驗證用的題目集合，從訓練 workload 切出來、專門保留給驗證用的那份"
  - "「paired（配對）」的重點是：候選與父版本用完全相同的"
  - "完全相同的取樣設定、完全相同的互動輪數上限去跑。把其他變因全部鎖死，讓分數差異只可能來自 ontology 改了什麼。"
  anchor_type: 設計參數
  qualifiers:
  - text: 論文未公開實際的門檻 τ（blog 範例用的 τ = 5 是假設值）
    source_quote: "（\\( \\tau = 5 \\) 是假設值，論文未公開實際門檻）"
  importance: 2
  status: normal
- id: c8
  role: mechanism
  text: 照論文的公式，候選是逐一處理的：patch 吃一個訊號、吐出一個候選，gate 比的也是這一個候選與它的父版本；論文明講每一輪對應恰好一個通過的候選。第二輪拿來比較的父版本，是已經吸收了第一輪修補結果的版本
  source_quotes:
  - "照論文的公式，候選是逐一處理的，每一輪只對應一個訊號、一個候選。"
  - "patch 吃進去的是一個 \\( \\sigma \\)，吐出一個候選，gate 比的也是這一個候選與它的父版本，從頭到尾都是一對一。"
  - "明講每一輪對應恰好一個通過的候選。"
  - "第二輪拿來比較的父版本，是已經吸收了第一輪修補結果的版本，不是最原始的版本。"
  anchor_type: 部落格推論
  qualifiers:
  - text: 如果 analyze 在同一輪一次抓出好幾個訊號，論文完全沒說系統怎麼決定先處理哪一個、用什麼順序（blog 讀論文後的疑問）
    source_quote: "如果 analyze 在同一輪一次抓出好幾個訊號，論文完全沒說系統怎麼決定先處理哪一個、用什麼順序。"
  - text: blog 對「輪」的用法前後不一：符號表說 ontology 每被修補接受一次，輪數 t 才加 1
    source_quote: "第幾輪演化；ontology 每被修補接受一次，\\( t \\) 就加 1"
  - text: 但 blog 的示意時間線把被拒絕的候選也算成一輪（第 2 輪的候選只贏 3 分，被拒絕，正式版本維持不變）
    source_quote: "第 2 輪的 \\( \\sigma_2 \\)（缺幣別轉換能力）只贏 3 分，被拒絕，正式版本維持不變。"
  importance: 3
  status: normal
- id: c9
  role: mechanism
  text: 被拒絕的候選不會部署，它的訊號、介入內容與評估結果會被記錄下來，目的是避免重複無效的更新
  source_quotes:
  - "*\"Rejected candidates are not deployed, and their signatures, interventions, and evaluation outcomes are logged to avoid repeated ineffective updates.\"*"
  anchor_type: 設計參數
  qualifiers:
  - text: 這份日誌具體怎麼被下一輪的 patch 讀取、怎麼影響新候選的生成，論文沒有說
    source_quote: "這份日誌具體怎麼被下一輪的 patch 讀取、怎麼影響新候選的生成，論文沒有說。"
  importance: 4
  status: normal
- id: c10
  role: evidence
  text: 論文 Table 5（DDR-Bench，Traj-Wise）逐一拿掉演化迴圈的步驟：拿掉 Gate 掉 11.2 分（掉最多），拿掉 Attribution 掉 6.3，拿掉 Diagnose 掉 4.8，把 Patch stage 換成自由發揮式重寫掉 1.7
  source_quotes:
  - "**演化迴圈四步驟，拿掉各自掉多少分**（DDR-Bench，Traj-Wise，論文 Table 5）："
  - "Gate（驗證閘門） | −11.2（掉最多"
  - "Attribution（歸因判斷哪一層） | −6.3"
  - "Diagnose（找反覆失敗模式） | −4.8"
  - "Patch stage（換成自由發揮式重寫） | −1.7"
  anchor_type: 實驗結果
  comparison_target: 沒拿掉該步驟的完整演化迴圈（「拿掉各自掉多少分」）
  qualifiers:
  - text: 實驗部分 blog 只保留關鍵數字，沒有逐表細讀
    source_quote: "這部分我們沒有逐表細讀，判斷是架構層面的思路已經理解清楚，數字本身的增量價值有限。"
  importance: 2
  status: normal
- id: c11
  role: evaluation
  text: 為什麼 gate 最不能省：沒有閘門，壞的修補進得來、出不去；沒有它，任何局部修補機制都可能把壞的改動放進系統，而系統本身沒有機制把它撤銷
  source_quotes:
  - "沒有閘門，壞的修補進得來、出不去"
  - "沒有它，任何局部修補機制都可能把壞的改動放進系統，而系統本身沒有機制把它撤銷。"
  anchor_type: 部落格推論
  importance: 2
  status: normal
- id: c12
  role: evidence
  text: 論文 Table 6 把三個可編輯層級限制成只准動一層：只准 Tool 層增益 +13.2、只准 Content 層 +8.7、只准 Schema 層 +3.6，三層都開放的完整版 +20.0；blog 的結論是三層互補，不能互相取代
  source_quotes:
  - "**三個可編輯層級，限制成只准動一層**（論文 Table 6）："
  - "只准 Tool 層 | +13.2"
  - "只准 Content 層 | +8.7"
  - "只准 Schema 層 | +3.6"
  - "三層都開放（完整版） | **+20.0**"
  - "三層互補，不能互相取代。"
  anchor_type: 實驗結果
  comparison_target: 同一張表內各組互比：只准動單一層的三組，對比三層都開放的完整版
  qualifiers:
  - text: +20.0 只取四個 backbone 的平均，和主結果表涵蓋六個 backbone 的範圍不同
    source_quote: "主結果表（表 1）涵蓋六個 backbone；後面消融實驗的 +20.0，則是只取四個 backbone 的平均。"
  importance: 3
  status: normal
- id: c13
  role: evidence
  text: 四個 backbone 加總，被接受的修補 Tool 層 6 次、Content 層 11 次、Schema 層 3 次，共 20 輪，正好等於被接受的總輪數，也支持「每一輪對應一個通過的候選」的讀法
  source_quotes:
  - "四個 backbone 加總，Tool 層被接受 6 次、Content 層 11 次、Schema 層 3 次，共 20 輪。"
  - "Tool 6 輪加 Content 11 輪加 Schema 3 輪，共 20 輪，正好等於被接受的總輪數，也支持這個讀法。"
  anchor_type: 實驗結果
  numeric_kind: non_comparative
  numeric_reason: 計數
  qualifiers:
  - text: 這是 DDR-Bench 上、四個 backbone 加總的分布
    source_quote: "（DDR-Bench，四個 backbone 加總）"
    source: figure_caption
  figures:
  - file: figures/evoontology/figure7.png
    article: evoontology
    src: figure7.png
    caption: 圖 5 — 被接受的演化增益在 Content、Tool、Schema 三種修補之間的分布（DDR-Bench，四個 backbone 加總）。（來源：原始論文 Figure 7。）
    sha256: b429456b39ceae7a1d8564e7936f9aa6c51c6308dffe710bdce43e62237885a3
  importance: 4
  status: pending_author_confirmation
- id: c13b
  role: evaluation
  text: blog 對 Schema 層級修補次數最少的解釋是：大多數時候問題出在知識內容不夠，而不是規則本身表達力不夠
  source_quotes:
  - "這也解釋了後面實驗裡 Schema 層級的修補次數最少：大多數時候問題出在知識內容不夠，而不是規則本身表達力不夠。"
  anchor_type: 部落格推論
  importance: 5
  status: normal
- id: c14
  role: mechanism
  text: 論文的評估用 Reciprocal Two-Fold Evaluation（split-and-swap）：把查詢切成兩份互斥資料，一份用來建置與演化（再切出 gate 用的驗證集），另一份在 ontology 凍結後才拿來算最終分數，再反過來跑一次，取兩個方向的平均分數，避免「用來建置系統的資料同時拿來評估系統」造成的樂觀偏誤
  source_quotes:
  - "這叫 **Reciprocal Two-Fold Evaluation**（split-and-swap）：兩份互斥資料互為訓練與測試，取平均分數，避免「用來建置系統的資料同時拿來評估系統」造成的樂觀偏誤。"
  - "gate 用的驗證集 V"
  - "Fold B（約 50 筆）→ 完全不碰，ontology 凍結後才拿來算最終分數"
  - "反過來再跑一次 B→A，最後 Score = (Score_{A→B} + Score_{B→A}) / 2"
  anchor_type: 設計參數
  qualifiers:
  - text: 論文原文只講了兩層切分，沒有把冷啟動、演化、驗證切成三塊分開；blog 給的切法比例是依論文敘述的推測
    source_quote: "論文原文只講了兩層切分，而且沒有把冷啟動、演化、驗證切成三塊分開：冷啟動用的資料與演化迴圈用的軌跡（agent 執行任務時留下的完整過程）來源，論文是混在一起講的。因此下面的比例，是我們依論文敘述的推測。"
  - text: 冷啟動用的查詢和演化迴圈用的軌跡是不是同一批，論文完全沒說
    source_quote: "這兩者是同一批約 35 筆查詢（依我們推測的切法）重複被使用，還是有先後次序或再切分，論文完全沒說。"
  importance: 3
  status: normal
- id: c15
  role: evaluation
  text: blog 認為 split-and-swap 是任何「系統會自動修改自己」的場景都該採用的驗證框架，可以遷移，不限於這篇論文的場景
  source_quotes:
  - "Reciprocal Two-Fold（split-and-swap）評估法，是任何「系統會自動修改自己」的場景都該採用的驗證框架"
  - "這是可以遷移的評估方法論，不限於這篇論文的場景。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c16
  role: evaluation
  text: blog 評價這個骨架（結構化知識層、從失敗軌跡歸因、驗證閘門）與同類「agent 自我演化知識庫或技能庫」論文在架構精神上同構，不是原創突破；blog 列出三個比較站得住腳的貢獻，其中一個是驗收閘門的具體設計：用「候選對父版本，同條件跑同一份驗證集」決定要不要接受修補，相對嚴謹
  source_quotes:
  - "核心骨架（結構化知識層、從失敗軌跡歸因、驗證閘門）與同類的「agent 自我演化知識庫或技能庫」論文"
  - "在架構精神上同構，不是原創突破。"
  - "比較站得住腳的貢獻有三個："
  - "backbone-conditional paired validation 這個驗收閘門的具體設計：用「候選對父版本，同條件跑同一份驗證集」決定要不要接受修補，相對嚴謹。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
```
