---
id: skillstate-results-cost-vs-accuracy
title: SKILL.state 省錢的證據很硬，變準的證據沒那麼穩：跨所有環境都穩定成立的優勢只有 token 節省，「準確率全面提升」會隨環境的關聯密度出現反例
type_hint: 發現
context_type: bound_to_source
sources:
- article: skill-state
  article_title: "SKILL.state 論文：Agent 不留對話歷史只留狀態，200 步任務省 41 倍 token"
  url: https://datasciocean.com/paper-intro/skill-state/
  sections:
  - Agent 跑越久越貴：把對話歷史換成一份狀態
  - 測試環境與計分方式
  - 對照組：關鍵是 Stateful 與預算對齊組
  - 看數字前的保留：長任務只在自建環境測過
  - 倉儲環境：任務夠長才拉開差距，最大的差距在 token
  - 公開 benchmark：三個任務都贏，但零售的對照組不穩
  - 軟體版本庫：中途一度輸給 Stateful
  - 雜訊與狀態恢復：架構本來就保證的結果
  - 結論：省成本可以期待，全面變準還不行
  - 三樣輸入、三樣輸出，狀態用合併來更新
  - 走一遍倉儲出貨的一步
  - 它會在哪裡失敗：小模型的錯誤與三種失效情境
  - 實務上該選 ReAct 還是 SKILL.state
  first_appearance: true
parent: null
related:
  - skillstate-state-replaces-history
  - llm-patch-validation-format-not-semantics
  - stateful-and-budget-matched-controls
  - discard-history-relevance-at-the-time
  - clm-results-tight-budget-not-across-the-board
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: SKILL.state 這篇論文省錢的證據很硬，變準的證據沒那麼穩：「準確率全面提升」會隨環境的關聯密度出現反例，跨所有環境都穩定成立的優勢，只有 token 節省
  source_quotes:
  - "這篇論文省錢的證據很硬，變準的證據沒那麼穩"
  - "「準確率全面提升」會隨環境的關聯密度出現反例；跨所有環境都穩定成立的優勢，只有 token 節省。"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: "SKILL.state 是 Google 與 Purdue 的論文《SKILL.state: Scalable Long-Horizon Agent Skills》提出的做法：模型每一步只看三樣東西：任務指令、一份描述「世界現在長什麼樣」的結構化狀態、這一步的最新觀察；模型的思考過程用完就丟，只把「狀態該怎麼改」的結論留下來"
  source_quotes:
  - "這是 Google 與 Purdue 的論文《SKILL.state: Scalable Long-Horizon Agent Skills》提出的做法。模型每一步只看三樣東西：任務指令、一份描述「世界現在長什麼樣」的結構化狀態、這一步的最新觀察。模型的思考過程用完就丟，只把「狀態該怎麼改」的結論留下來。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: 測試分兩類：論文自己設計的合成測試台 SkillExecBench，可以把任務長度（要走幾步）從 T=10 拉到 T=200，底下分成倉儲管理（500 個獨立、互不重疊的貨架）和軟體版本庫（Git 分支、commit、PR、CI 狀態彼此深度關聯）；以及兩個別人設計的公開 benchmark：InterCode CTF 和 Sierra τ-Bench（零售與航空兩個領域）
  source_quotes:
  - "論文的測試分成兩類：自己設計的合成測試台 SkillExecBench，以及兩個別人設計的公開 benchmark。"
  - "它可以把任務長度，也就是要走幾步（論文稱為 horizon），從 \\( T=10 \\) 一路拉到 \\( T=200 \\)。底下分成倉儲和軟體版本庫："
  - "倉儲管理：500 個獨立、互不重疊的貨架"
  - "軟體版本庫：Git 分支、commit、PR、CI 狀態彼此深度關聯"
  - "兩個公開 benchmark 是 InterCode CTF（Yang et al., 2023）和 Sierra τ-Bench（Yao et al., 2024）。"
  - "分零售和航空兩個領域"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 2
  status: normal
- id: c4
  role: context
  text: 架構層面的對照組有三個：Prompt(ReAct) 是每一步的觀察、推理、動作全部往後疊加；Memory(Summary) 保留最近三輪的原文，再加上一份定期更新的自然語言摘要；Stateful(LangGraph) 有結構化的狀態區塊，但同時保留完整的滾動對話紀錄
  source_quotes:
  - "架構層面的對照組有三個。Prompt(ReAct) 是最原始的做法，每一步的觀察、推理、動作全部往後疊加。Memory(Summary) 保留最近三輪的原文，再加上一份定期更新的自然語言摘要。Stateful(LangGraph) 仿照 LangGraph（一個 agent 開發框架，可以在對話之外維護一份結構化狀態）的做法，有結構化的狀態區塊，但同時保留完整的滾動對話紀錄。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 2
  status: normal
- id: c5
  role: anchor
  text: 倉儲環境 T=200 時，Stateful 用掉 5,041,164 個 token，SKILL.state 只用 122,384 個，差了 41 倍；真正壓倒性的是 token，差距主要在成本，不在準確率
  source_quotes:
  - "Table 1 是倉儲環境的主表"
  - "真正壓倒性的是 token：\\( T=200 \\) 時 Stateful 用掉 5,041,164 個，SKILL.state 只用 122,384 個，差了 41 倍。差距主要在成本，不在準確率。"
  anchor_type: 實驗結果
  comparison_target: 同一環境、同樣 T=200 的 Stateful 對照組
  qualifiers:
  - text: 最有說服力的長任務數字，全部來自論文自己設計、自己控制的合成環境
    source_quote: "最有說服力的長任務數字，全部來自自己設計、自己控制的合成環境。"
  figures:
  - file: figures/skill-state/table1.png
    article: skill-state
    src: table1.png
    caption: 表 1 — 倉儲環境的長任務 scaling：準確率與 token 消耗隨任務長度的變化（來源：原始論文 Table 1。）
    sha256: 3a1e13c1b1b813134db90665b0a95693a5109cf947fdf86bf1d7599d3753f237
  importance: 2
  status: normal
- id: c6
  role: anchor
  text: 倉儲環境的準確率：短任務（T=10）沒有準確率優勢，主要對照組 Memory、Stateful 和 SKILL.state 都是 1.00，打平；優勢只在長任務浮現，而且不算壓倒性，T=200 時是 0.94 對 0.88，差 6 個百分點
  source_quotes:
  - "Table 1 是倉儲環境的主表"
  - "短任務（\\( T=10 \\)）沒有準確率優勢：主要對照組 Memory、Stateful 和 SKILL.state 都是 1.00，打平。優勢只在長任務浮現，而且不算壓倒性：\\( T=200 \\) 時是 0.94 對 0.88，差 6 個百分點。"
  - "可是準確率只是 0.94 對 0.88（只留狀態對保留歷史）。"
  anchor_type: 實驗結果
  comparison_target: 主要對照組（T=10 為 Memory 與 Stateful；T=200 的 0.88 為保留歷史的對照組）
  qualifiers:
  - text: 這組倉儲結果用的是論文測過最強的模型 Gemini-3-Flash
    source_quote: "即使用論文測過最強的模型 Gemini-3-Flash"
  - text: 換成公開權重的 Gemma-4-31B，SKILL.state 在 T=100 的倉儲任務上準確率只剩 0.42
    source_quote: "換成公開權重的 Gemma-4-31B，SKILL.state 在 \\( T=100 \\) 的倉儲任務上準確率只剩 0.42。"
  - text: 最有說服力的長任務數字，全部來自論文自己設計、自己控制的合成環境
    source_quote: "最有說服力的長任務數字，全部來自自己設計、自己控制的合成環境。"
  figures:
  - file: figures/skill-state/table1.png
    article: skill-state
    src: table1.png
    caption: 表 1 — 倉儲環境的長任務 scaling：準確率與 token 消耗隨任務長度的變化（來源：原始論文 Table 1。）
    sha256: 3a1e13c1b1b813134db90665b0a95693a5109cf947fdf86bf1d7599d3753f237
  importance: 2
  status: normal
- id: c7
  role: evidence
  text: 倉儲環境裡對照組的準確率隨 T 變長而下降、標準差跟著放大：Prompt 從 T=10 的 0.90±0.02 跌到 T=200 的 0.74±0.14，SKILL.state 則相對穩定。更精確的講法是「對照組會隨執行時間拉長而退化，SKILL.state 不太退化」，而不是「SKILL.state 準確率大幅領先」
  source_quotes:
  - "對照組的準確率也隨 \\( T \\) 變長而下降，標準差（多次執行的分數有多分散）跟著放大：Prompt 從 \\( T=10 \\) 的 \\( 0.90\\pm0.02 \\) 跌到 \\( T=200 \\) 的 \\( 0.74\\pm0.14 \\)，SKILL.state 則相對穩定。所以更精確的講法是「對照組會隨執行時間拉長而退化，SKILL.state 不太退化」，而不是「SKILL.state 準確率大幅領先」。"
  - "Table 1 是倉儲環境的主表"
  anchor_type: 實驗結果
  comparison_target: 同一做法（Prompt）在 T=10 時的準確率
  figures:
  - file: figures/skill-state/table1.png
    article: skill-state
    src: table1.png
    caption: 表 1 — 倉儲環境的長任務 scaling：準確率與 token 消耗隨任務長度的變化（來源：原始論文 Table 1。）
    sha256: 3a1e13c1b1b813134db90665b0a95693a5109cf947fdf86bf1d7599d3753f237
  qualifiers:
  - text: 這組倉儲結果用的是論文測過最強的模型 Gemini-3-Flash
    source_quote: "即使用論文測過最強的模型 Gemini-3-Flash"
  - text: 換成公開權重的 Gemma-4-31B，SKILL.state 在 T=100 的倉儲任務上準確率只剩 0.42
    source_quote: "換成公開權重的 Gemma-4-31B，SKILL.state 在 \\( T=100 \\) 的倉儲任務上準確率只剩 0.42。"
  - text: 最有說服力的長任務數字，全部來自論文自己設計、自己控制的合成環境
    source_quote: "最有說服力的長任務數字，全部來自自己設計、自己控制的合成環境。"
  importance: 3
  status: normal
- id: c8
  role: anchor
  text: 在別人設計的公開 benchmark 上三個任務都贏：比起表現最好的對照組，InterCode CTF 的 pass@1（第一次嘗試就解出來的比例）高 7.8 個百分點，τ-Bench 零售高 6.6 個百分點，航空高 4.3 個百分點；因為不是論文自己出的題，這是全篇最有說服力的準確率證據
  source_quotes:
  - "因為不是論文自己出的題，這是全篇最有說服力的準確率證據。"
  - "三個任務都贏：比起表現最好的對照組，CTF 的 pass@1 高 7.8 個百分點，τ-Bench 零售高 6.6 個百分點，航空高 4.3 個百分點。"
  - "InterCode CTF 用 pass@1，也就是第一次嘗試就解出來的比例"
  anchor_type: 實驗結果
  comparison_target: 各任務上表現最好的對照組
  qualifiers:
  - text: Memory 在 τ-Bench 零售上崩得很慘，只有 29.9%，比 Prompt 的 48.2% 還低將近 20 個百分點，論文沒有討論；零售這一欄的比較基準不穩定，解讀時要看清楚對照組是誰
    source_quote: "Memory 在 τ-Bench 零售上崩得很慘，只有 29.9%，比 Prompt 的 48.2% 還低將近 20 個百分點。論文沒有討論這個異常值；我的推論是，摘要式記憶可能把交易細節搞丟了。這代表零售這一欄的比較基準不穩定：SKILL.state 贏的是表現最好的對照組還是最差的，差距很大，解讀時要看清楚對照組是誰。"
  - text: 這張表證明的是「整體上表現比較好」，回答不了「長任務在真實世界成立嗎」，範圍比論文摘要暗示的窄
    source_quote: "這張表也回答不了看數字之前提過的「長任務在真實世界成立嗎」這個疑慮；它證明的是「整體上表現比較好」，範圍比論文摘要暗示的窄。"
  - text: InterCode CTF 和 τ-Bench 兩節，論文完全沒有報告一個任務平均要走幾步
    source_quote: "但 InterCode CTF 和 τ-Bench 兩節，論文完全沒有報告一個任務平均要走幾步。"
  figures:
  - file: figures/skill-state/table4.png
    article: skill-state
    src: table4.png
    caption: 表 4 — 公開互動式 benchmark 的成功率與 token 消耗（來源：原始論文 Table 4。）
    sha256: 2259d49da0fcbb7866463422611c4708da8629c75299b27e3fd910801224f71c
  importance: 2
  status: normal
- id: c9
  role: anchor
  text: 軟體版本庫環境（狀態彼此高度關聯）是全篇最重要的反例：T=10 時 Stateful 和 SKILL.state 都是 1.00±0.00，打平；T=25 時 SKILL.state（0.88±0.08）反而輸給 Stateful（0.94±0.03）6 個百分點；T=50 才贏回來（0.86 對 0.74），T=100 領先擴大到 15 個百分點（0.78 對 0.63）
  source_quotes:
  - "軟體版本庫是 SkillExecBench 的第二個子環境，狀態彼此高度關聯。Table 6 是它在四個任務長度下的結果，也是全篇最重要的反例。"
  - "\\( T=10 \\) 時 Stateful 和 SKILL.state 都是 \\( 1.00\\pm0.00 \\)，打平。到了 \\( T=25 \\)，SKILL.state（\\( 0.88\\pm0.08 \\)）反而輸給 Stateful（\\( 0.94\\pm0.03 \\)）6 個百分點。\\( T=50 \\) 才贏回來（0.86 對 0.74），\\( T=100 \\) 領先擴大到 15 個百分點（0.78 對 0.63）。"
  anchor_type: 實驗結果
  comparison_target: 同一任務長度的 Stateful 對照組
  qualifiers:
  - text: SKILL.state 在這張表的標準差也偏大（±0.08），結果不算穩定
    source_quote: "SKILL.state 在這張表的標準差也偏大（\\( \\pm0.08 \\)），結果不算穩定。"
  figures:
  - file: figures/skill-state/table6.png
    article: skill-state
    src: table6.png
    caption: 表 6 — 軟體版本庫環境的長任務 scaling：短任務打平，中段一度落後，長任務才領先（來源：原始論文 Table 6。）
    sha256: 1ba1fbcd312e340fac296fde92536afb8727f3a87c4cc92e545e0981f1b211aa
  importance: 2
  status: normal
- id: c10
  role: evaluation
  text: 這個反例跟論文自己的宣稱矛盾：論文摘要說 SKILL.state「improves task accuracy... across diverse datasets」，正文說它「matches or exceeds baseline accuracy across all horizons」，但「across all horizons」只在倉儲環境成立，換到軟體版本庫就有 T=25 這個反例，論文正文完全沒有提到
  source_quotes:
  - "論文摘要說 SKILL.state「improves task accuracy... across diverse datasets」，正文說它「matches or exceeds baseline accuracy across all horizons」。但「across all horizons」只在倉儲環境成立，換到軟體版本庫就有 \\( T=25 \\) 這個反例，論文正文完全沒有提到。"
  - "到了 \\( T=25 \\)，SKILL.state（\\( 0.88\\pm0.08 \\)）反而輸給 Stateful"
  anchor_type: 部落格判斷
  comparison_target: T=25 時的 Stateful 對照組（SKILL.state 輸給它）
  importance: 2
  status: normal
- id: c11
  role: evaluation
  text: blog 推論 T=25 的反例很可能跟軟體版本庫的密集依賴有關：單一動作可能連帶影響多個分支，一旦某次 patch（模型輸出的狀態差異，描述這一步要對狀態做哪些修改）沒有正確捕捉到連帶影響，錯誤可能一路延續到後面的步驟，因為沒有原始歷史文字可以回頭核對
  source_quotes:
  - "我的推論是，這跟軟體版本庫的密集依賴有關。單一動作可能連帶影響多個分支；一旦某次 patch 沒有正確捕捉到連帶影響（例如合併了 PR，卻漏了更新相依分支的狀態），錯誤可能一路延續到後面的步驟，因為沒有原始歷史文字可以回頭核對。"
  - "這正好是前面說的驗證盲區，\\( T=25 \\) 的反例很可能就是這個風險真的發生了。"
  - '\( \Delta\Sigma_t \) 是狀態的「差異」，一個 JSON 字典，描述這一步要對狀態做哪些修改。'
  - '`state_patch` 就是 \( \Delta\Sigma_t \)'
  - "到了 \\( T=25 \\)，SKILL.state（\\( 0.88\\pm0.08 \\)）反而輸給 Stateful"
  anchor_type: 部落格推論
  comparison_target: T=25 時的 Stateful 對照組（SKILL.state 輸給它）
  importance: 3
  status: normal
- id: c12
  role: qualifier
  text: 最有說服力的長任務數字，全部來自論文自己設計、自己控制的合成環境：InterCode CTF 和 τ-Bench 兩節，論文完全沒有報告一個任務平均要走幾步；SWE-bench、WebArena / Mind2Web、GAIA、OSWorld 這些專門測長任務的公開 benchmark，論文一個都沒用，也沒有解釋為什麼。這不代表數字是假的，而是「長任務的做法在真實世界也成立」這個宣稱，證據比表面看起來薄
  source_quotes:
  - "但 InterCode CTF 和 τ-Bench 兩節，論文完全沒有報告一個任務平均要走幾步。"
  - "業界其實有專門測長任務、真實世界 agent 能力的公開 benchmark，這篇論文一個都沒用："
  - "SWE-bench：修真實 GitHub issue 的任務"
  - "WebArena / Mind2Web：長距離的網頁操作任務。"
  - "GAIA：需要多步驟串接工具推理的通用助理任務。"
  - "OSWorld：真實作業系統的操作任務。"
  - "論文沒有解釋為什麼不用這些更有代表性的長任務 benchmark。這不代表論文的數字是假的，而是「長任務的做法在真實世界也成立」這個宣稱，證據比表面看起來薄：最有說服力的長任務數字，全部來自自己設計、自己控制的合成環境。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c13
  role: evidence
  text: 雜訊實驗：在無關訊息很多的高雜訊環境，Prompt 的準確率從 0.68 掉到 0.53，SKILL.state 全程維持 0.97 到 1.00
  source_quotes:
  - "在無關訊息很多的高雜訊環境，Prompt 的準確率從 0.68 掉到 0.53，SKILL.state 全程維持 0.97 到 1.00。"
  anchor_type: 實驗結果
  comparison_target: Prompt 對照組自己的前後變化（從 0.68 掉到 0.53），以及 SKILL.state 對比 Prompt 對照組
  qualifiers:
  - text: blog 認為這個結果其實可以預期：雜訊不會被寫進 state patch，自然不影響後續決策，是架構設計的直接推論，不算意外發現
    source_quote: "這個結果其實可以預期：雜訊不會被寫進 state patch，自然不影響後續決策，是架構設計的直接推論，不算意外發現。"
  - text: 這是倉儲環境的雜訊實驗
    source_quote: "表 2 — 倉儲環境的雜訊魯棒性（來源：原始論文 Table 2。）"
    source: figure_caption
  figures:
  - file: figures/skill-state/table2.png
    article: skill-state
    src: table2.png
    caption: 表 2 — 倉儲環境的雜訊魯棒性（來源：原始論文 Table 2。）
    sha256: d2c007de13ae8d7ecc6cf440917e2de46d3553555ab9194752ec708b55007cc5
  importance: 4
  status: normal
- id: c14
  role: evidence
  text: 狀態恢復實驗：外部環境悄悄改變了世界（例如有人搬走了貨），保留歷史的對照組需要 5 到 8 步才能從錯誤的舊認知中恢復，SKILL.state 需要 0 步
  source_quotes:
  - "第二個是狀態恢復：外部環境悄悄改變了世界（例如有人搬走了貨），保留歷史的對照組需要 5 到 8 步才能從錯誤的舊認知中恢復，SKILL.state 需要 0 步。"
  anchor_type: 實驗結果
  comparison_target: 保留歷史的對照組
  qualifiers:
  - text: blog 認為這個結果接近同義反覆：SKILL.state 本來就不保留歷史文字，「被舊觀察蓋過新事實」在架構上不可能發生，只要修正性的觀察能成功寫進 patch，恢復步數邏輯上必然是 0
    source_quote: "這個結果同樣接近同義反覆：SKILL.state 本來就不保留歷史文字，「被舊觀察蓋過新事實」在架構上不可能發生，只要修正性的觀察能成功寫進 patch，恢復步數邏輯上必然是 0。"
  importance: 4
  status: normal
- id: c15
  role: evaluation
  text: 論文常把準確率和成本包裝成同一個賣點，但兩者的證據力不對等；讀任何宣稱「又快又準」的論文，都可以把兩個宣稱拆開分別檢查，通常其中一個會明顯比另一個強
  source_quotes:
  - "論文常把準確率和成本包裝成同一個賣點，但兩者的證據力不對等。讀任何宣稱「又快又準」的論文，都可以把兩個宣稱拆開分別檢查，通常其中一個會明顯比另一個強。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c16
  role: evaluation
  text: 找全稱宣稱的反例：看到「across all X」，就去找跨資料集或跨環境的反例，像軟體版本庫的 T=25；全稱宣稱通常只在最有利的環境成立，附錄或次要表格反而常藏著誠實的反例
  source_quotes:
  - "找全稱宣稱的反例：看到「across all X」，就去找跨資料集或跨環境的反例，像軟體版本庫的 \\( T=25 \\)。全稱宣稱通常只在最有利的環境成立，附錄或次要表格反而常藏著誠實的反例。"
  - "到了 \\( T=25 \\)，SKILL.state（\\( 0.88\\pm0.08 \\)）反而輸給 Stateful"
  anchor_type: 部落格判斷
  comparison_target: T=25 時的 Stateful 對照組（SKILL.state 輸給它）
  importance: 3
  status: normal
```
