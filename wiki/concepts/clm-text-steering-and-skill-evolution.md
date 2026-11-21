---
id: clm-text-steering-and-skill-evolution
title: context 管理變成模型自己的行為後，不必改 harness 程式，用一段文字就能引導，也能讓另一個模型自動改寫這段文字；但證據只說明可控性與「有 skill 比沒 skill 好」，而用來挑 skill 的 dev 分數不能拿來報成績
type_hint: 方法
context_type: bound_to_source
sources:
- article: context-language-models
  article_title: "Context Language Models 解析：讓 agent 用 Bash 改自己的 context"
  url: https://datasciocean.com/paper-intro/context-language-models/
  sections:
  - context 爆了，誰來決定留什麼？CLM 讓模型自己改
  - 不動權重：用一段文字引導與演化管理策略
  - 一句話就能改變管理行為
  - 讓另一個模型自動改寫指令
  - 用來挑選的資料，不能用來報成績
  - 論文實際使用的三段引導指令
  - 零樣本、skill 演化、RL：三組互不重疊的證據
  - 論文摘要的宣稱，換成乾淨版本
  first_appearance: true
parent: null
related:
  - clm-context-as-editable-file
  - clm-results-tight-budget-not-across-the-board
  - skillopt-overview
  - skillopt-blind-acceptance-gate
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 既然 context 管理變成模型自己的行為，想改變它的策略，不必改 harness 程式，直接用文字告訴模型就行；再進一步，讓另一個模型看 agent 的成功與失敗紀錄，自動把這段文字改寫得更好，一輪輪重複；演化的目標是模型權重和 harness 都不動，只搜尋「哪段文字讓 agent 平均得分最高」
  source_quotes:
  - "既然 context 管理變成模型自己的行為，想改變它的策略，不必改 harness 程式，直接用文字告訴模型就行。"
  - "這一步讓另一個模型看 agent 的成功與失敗紀錄，自動把 \\( s \\) 改寫得更好，一輪輪重複。"
  - "目標是：模型權重和 harness 都不動，只搜尋「哪段文字讓 agent 平均得分最高」。"
  anchor_type: 設計參數
  qualifiers:
  - text: 引導實驗量的是「模型有沒有照指令做」，沒有報任務正確率，證明的是可控性，不是這些策略比較好
    source_quote: "這三個實驗量的是「模型有沒有照指令做」，沒有報任務正確率，所以證明的是可控性，不是這些策略比較好（我的觀察，論文沒有明講）。"
  - text: 演化的起點是「完全沒有指令」，量到的是「有 skill 比沒 skill 好」
    source_quote: "起點是「完全沒有指令」，所以量到的是「有 skill 比沒 skill 好」"
  importance: 1
  status: normal
- id: c2
  role: context
  text: 這是 Context Language Models 論文的一部分。論文提出的 CLM 把模型當前的 context 鏡像成一個檔案，模型用 Bash 想改哪裡就改哪裡，改完立刻同步回它的 live context（下一輪真正餵給模型的那份 context）
  source_quotes:
  - "Context Language Models 這篇論文提出的做法叫 CLM：把模型當前的 context 鏡像成一個檔案，模型用 Bash 想改哪裡就改哪裡，改完立刻同步回它的 live context（下一輪真正餵給模型的那份 context）。"
  anchor_type: 設計參數
  qualifiers:
  - text: 這是介面設計，不是新演算法
    source_quote: "這是介面設計，不是新演算法。"
  importance: 2
  status: normal
- id: c2b
  role: context
  text: harness 是包在模型外面、負責跑 agent 迴圈與組裝每輪 context 的程式。目前的主流做法，是由 harness 用固定規則做摘要，或是給模型幾個預先設計好的壓縮工具
  source_quotes:
  - "目前的主流做法，是由 harness（包在模型外面、負責跑 agent 迴圈與組裝每輪 context 的程式）用固定規則做摘要，或是給模型幾個預先設計好的壓縮工具。"
  anchor_type: 背景說明
  importance: 2
  status: normal
- id: c3
  role: mechanism
  text: 引導的做法是在 context 裡放一段指令或 skill 文件（skill 在這裡就是一份教模型怎麼做事的文字說明）；和論文 Eq. 2 唯一的差別，是模型多讀了這段文字，沒有任何新機制
  source_quotes:
  - "做法很直接：在 context 裡放一段指令或 skill 文件（skill 在這裡就是一份教模型怎麼做事的文字說明）。和 Eq. 2 唯一的差別，是模型多讀了這段文字；它沒有任何新機制。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 3
  status: normal
- id: c4
  role: evidence
  text: 論文用 BrowseComp-Plus 的題目與 Claude 4.6 Sonnet，各用一句附加在任務訊息後面的指令測三種行為：「超過 Y tokens 就壓縮到約 4K」，Y 設 16K／24K／32K，第一次壓縮時的 context 大小（中位數）約在 16.0K／23.6K／30.9K，貼著指令走；「只在子任務邊界壓縮」，邊界附近兩輪內有壓縮的比例從 0.40 升到 0.88；「每次編輯前先備份到新資料夾」，編輯前有完整備份的比例從 0.00 升到 0.68
  source_quotes:
  - "論文用 BrowseComp-Plus 的題目與 Claude 4.6 Sonnet，各用一句附加在任務訊息後面的指令，測三種行為"
  - "超過 \\( Y \\) tokens 就壓縮到約 4K | 壓縮時機 | 第一次壓縮時的 context 大小（中位數） | \\( Y \\) 設 16K／24K／32K，第一次壓縮約在 16.0K／23.6K／30.9K，貼著指令走"
  - "只在子任務邊界壓縮 | 壓縮位置 | 邊界附近兩輪內有壓縮的比例 | 0.40 升到 0.88"
  - "每次編輯前先備份到新資料夾 | 備份習慣 | 編輯前有完整備份的比例 | 0.00 升到 0.68"
  anchor_type: 實驗結果
  comparison_target: 指令設定的門檻 Y（壓縮時機）；無指令對照組（0.40、0.00）
  qualifiers:
  - text: 備份實驗的設定是 16,000 tokens 預算、200 道題
    source_quote: "指令三：備份…設定：16,000 tokens 預算，200 道題，其中 91 道配對分析。"
  - text: 子任務邊界實驗的設定是四個問題串在同一個 session、24,000 tokens 預算
    source_quote: "指令二：子任務邊界壓縮…設定：四個問題串在同一個 session，24,000 tokens 預算、1,000 輪上限，每個條件 189 個 session，其中 131 個在 session 內含有子任務邊界。"
  - text: 壓縮時機實驗的設定是 48,000 tokens 預算、200 輪上限、30 道較長的題目
    source_quote: "指令一：壓縮時機…設定：48,000 tokens 預算、200 輪上限，30 道較長的題目（輪數在無指令時達到第 60 百分位以上）。"
  - text: 量的是「模型有沒有照指令做」，沒有報任務正確率，證明的是可控性，不是這些策略比較好
    source_quote: "這三個實驗量的是「模型有沒有照指令做」，沒有報任務正確率，所以證明的是可控性，不是這些策略比較好（我的觀察，論文沒有明講）。"
  - text: 指令一和二都直接寫出了 context 檔案的路徑並附上具體做法的範例，比「一句話」更具體
    source_quote: "指令一和二都直接寫出了 context 檔案的路徑，並且附上具體做法的範例。所以這些指令比「一句話」更具體，是帶範例的操作說明。"
  - text: 指令一的實驗裡，模型知道自己用了多少，是 harness 把大小餵給它的；blog 推論指令一的成功有一部分要歸功於這個提示
    source_quote: "這個實驗裡模型知道自己用了多少，是 harness 把大小餵給它的，不是模型自己感知的。推論：指令一的成功有一部分要歸功於這個提示。"
  figures:
  - file: figures/context-language-models/figure7.png
    article: context-language-models
    src: figure7.png
    caption: 圖 6 — 一句話就能改變 context 管理策略：灰色是無指令對照，藍色是有指令的設定。（來源：原始論文 Figure 7。）
    sha256: c04d5d00b153bd41ddaa80183b3f4f3ee97bed582f638d460db189d9f8ca449f
  importance: 4
  status: normal
- id: c5
  role: evaluation
  text: blog 的觀察：這三個引導實驗量的是「模型有沒有照指令做」，沒有報任務正確率，所以證明的是可控性，不是這些策略比較好
  source_quotes:
  - "這三個實驗量的是「模型有沒有照指令做」，沒有報任務正確率，所以證明的是可控性，不是這些策略比較好（我的觀察，論文沒有明講）。"
  anchor_type: 部落格判斷
  importance: 5
  status: normal
- id: c6
  role: evaluation
  text: 指令 s 就放在 context 裡，而模型能改寫整份 context；它能不能把指令自己刪掉，論文沒有討論
  source_quotes:
  - "指令 \\( s \\) 就放在 context 裡，而模型能改寫整份 context。它能不能把指令自己刪掉？論文沒有討論。"
  anchor_type: 部落格判斷
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: 演化一輪的流程：目前的 skill 在訓練集跑 rollout（讓 agent 實際把整條任務跑完）；proposer（負責改寫 skill 的另一個模型）讀這些成功與失敗的軌跡，寫出多份新 skill 候選；候選先在 6 題訓練題初篩，過關再跑 12 題，最後在 102 題的開發集（dev）評分；選出下一輪的 skill，連續 5 次提案沒進步就停；最終 skill 在測試集（test）只評一次
  source_quotes:
  - "目前的 skill 在訓練集跑 rollout（讓 agent 實際把整條任務跑完）。"
  - "proposer（負責改寫 skill 的另一個模型）讀這些成功與失敗的軌跡，寫出多份新 skill 候選。"
  - "候選先在 6 題訓練題初篩，過關再跑 12 題，最後在 102 題的開發集（dev）評分。"
  - "選出下一輪的 skill，重複；連續 5 次提案沒進步就停。"
  - "最終 skill 在測試集（test）只評一次。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 7
  status: normal
- id: c8
  role: context
  text: 演化有兩種設定：assisted evolution 是 Qwen3.6-27B 當 agent、Claude Fable 5.1 當 proposer；self-evolution 是 Opus 5 同時當 agent 和 proposer
  source_quotes:
  - "兩種設定：assisted evolution 是 Qwen3.6-27B 當 agent、Claude Fable 5.1 當 proposer；self-evolution 是 Opus 5 同時當 agent 和 proposer。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 8
  status: normal
- id: c9
  role: evidence
  text: KV Store 任務、assisted 設定：起點完全沒有管理指令時 dev 22.3%、test 38.3%；演化後選出的 skill dev 83.8%、test 74.2%。dev 是用來挑 skill 的題目，test 是定案後才評一次、沒參與挑選的題目
  source_quotes:
  - "KV Store 任務、assisted 設定的結果如下。dev 是用來挑 skill 的題目，test 是定案後才評一次、沒參與挑選的題目："
  - "起點：完全沒有管理指令 | 22.3% | 38.3%"
  - "演化後選出的 skill | 83.8% | 74.2%"
  anchor_type: 實驗結果
  comparison_target: 起點：完全沒有管理指令
  qualifiers:
  - text: 這是 32K 預算下的結果
    source_quote: "圖 7 — KV Store（32K 預算）上的 skill 演化。Assisted 用 Qwen3.6-27B 搭配 Claude Fable 5.1 當 proposer，self-evolution 由 Opus 5 兼任兩個角色。（來源：原始論文 Figure 8。）"
    source: figure_caption
  - text: 起點是「完全沒有指令」，量到的是「有 skill 比沒 skill 好」；沒有演化出的 skill 與人手寫 skill 在同一個模型上的比較
    source_quote: "起點是「完全沒有指令」，所以量到的是「有 skill 比沒 skill 好」；我讀到的部分沒有演化出的 skill 全文，也沒有它與人手寫 skill 在同一個模型上的比較。"
  figures:
  - file: figures/context-language-models/figure8.png
    article: context-language-models
    src: figure8.png
    caption: 圖 7 — KV Store（32K 預算）上的 skill 演化。Assisted 用 Qwen3.6-27B 搭配 Claude Fable 5.1 當 proposer，self-evolution 由 Opus 5 兼任兩個角色。（來源：原始論文 Figure 8。）
    sha256: ce04d2ade4a1da8d9e18459598e6d28cd34d0ed257a9caac6a88be5d35753c64
  importance: 9
  status: normal
- id: c10
  role: evaluation
  text: 論文摘要的「最多提升 35.9 點」，剛好是 74.2 − 38.3，也就是 KV Store 單一任務、assisted 設定下 test 的最好結果；起點是「完全沒指令」，不是對人手寫 skill
  source_quotes:
  - "論文摘要的「最多提升 35.9 點」，剛好是 74.2 − 38.3，也就是 KV Store 單一任務、assisted 設定下 test 的最好結果（我的計算）。"
  - "KV Store 單一任務，test 38.3 到 74.2；起點是「完全沒指令」，不是對人手寫 skill"
  anchor_type: 部落格考證
  comparison_target: 起點：完全沒有管理指令（test 38.3%）
  qualifiers:
  - text: 這是 32K 預算下的結果
    source_quote: "圖 7 — KV Store（32K 預算）上的 skill 演化。Assisted 用 Qwen3.6-27B 搭配 Claude Fable 5.1 當 proposer，self-evolution 由 Opus 5 兼任兩個角色。（來源：原始論文 Figure 8。）"
    source: figure_caption
  figures:
  - file: figures/context-language-models/figure8.png
    article: context-language-models
    src: figure8.png
    caption: 圖 7 — KV Store（32K 預算）上的 skill 演化。Assisted 用 Qwen3.6-27B 搭配 Claude Fable 5.1 當 proposer，self-evolution 由 Opus 5 兼任兩個角色。（來源：原始論文 Figure 8。）
    sha256: ce04d2ade4a1da8d9e18459598e6d28cd34d0ed257a9caac6a88be5d35753c64
  importance: 10
  status: normal
- id: c11
  role: evidence
  text: 其他三個任務，文字只給 dev 數字：Needle Retention 97.6% 到 100.0%、Sudoku Sketchpad 45.3% 到 65.8%、Log Triage 0.0% 到 100.0%
  source_quotes:
  - "其他三個任務，文字只給 dev 數字：Needle Retention 97.6% 到 100.0%、Sudoku Sketchpad 45.3% 到 65.8%、Log Triage 0.0% 到 100.0%。"
  anchor_type: 實驗結果
  comparison_target: 各任務演化前的起點（dev）
  qualifiers:
  - text: dev 同時被用來選 skill，所以偏樂觀
    source_quote: "dev 同時被用來選 skill，所以偏樂觀。"
  importance: 11
  status: normal
- id: c12
  role: evidence
  text: self-evolution 設定下，Opus 5 起點就在 94% 到 100% 之間，演化後的 skill 要嘛在同樣準確率下降低成本，要嘛再提升準確率
  source_quotes:
  - "self-evolution：Opus 5 起點就在 94% 到 100% 之間，演化後的 skill 要嘛在同樣準確率下降低成本，要嘛再提升準確率。"
  anchor_type: 實驗結果
  comparison_target: Opus 5 演化前的起點
  importance: 12
  status: normal
- id: c13
  role: mechanism
  text: 用來挑選的資料不能用來報成績：在 dev（開發集）上試很多候選，再報最高的那個，分數會系統性偏高，因為挑的是「在這批題目上最幸運的」；這個現象叫 selection effect（也稱贏家的詛咒）
  source_quotes:
  - "在 dev（開發集）上試很多候選，再報最高的那個，分數會系統性偏高，因為挑的是「在這批題目上最幸運的」。"
  - "這個現象叫 selection effect（也稱贏家的詛咒）。"
  anchor_type: 背景說明
  importance: 13
  status: normal
- id: c14
  role: anchor
  text: 自編例子：100 份候選的真實水準都是 70%，dev 有 102 題，標準誤（量測雜訊的大小，約為真實準確率乘上錯誤率、除以題數再開根號）約 4.5 個百分點；100 份裡的最高分，期望值約高出 2.5 個標準誤，dev 上看起來約 81%，但真實仍是 70%
  source_quotes:
  - "量測本身有雜訊，標準誤（SE）衡量這個雜訊有多大，大約是真實準確率乘上錯誤率、除以題數，再開根號："
  - "自編例子：100 份候選的真實水準都是 70%，\\( n = 102 \\)，SE 約 4.5 個百分點。100 份裡的最高分，期望值約高出 2.5 個 SE，也就是 dev 上看起來約 81%，但真實仍是 70%。"
  anchor_type: 部落格舉例
  comparison_target: 候選的真實水準 70%
  importance: 14
  status: normal
- id: c15
  role: evaluation
  text: KV Store（assisted 設定）就是實例：dev 上從 22.3% 升到 83.8%（+61.5 點），定案後在沒參與挑選的 test 上只有 38.3% 到 74.2%（+35.9 點）
  source_quotes:
  - "論文的實例在 skill 演化那一節：KV Store（assisted 設定）dev 上從 22.3% 升到 83.8%（+61.5 點），定案後在沒參與挑選的 test 上只有 38.3% 到 74.2%（+35.9 點）。"
  anchor_type: 部落格考證
  comparison_target: 同一次演化的 dev 增幅對 test 增幅（+61.5 點對 +35.9 點）
  qualifiers:
  - text: 這是 32K 預算下的結果
    source_quote: "圖 7 — KV Store（32K 預算）上的 skill 演化。Assisted 用 Qwen3.6-27B 搭配 Claude Fable 5.1 當 proposer，self-evolution 由 Opus 5 兼任兩個角色。（來源：原始論文 Figure 8。）"
    source: figure_caption
  figures:
  - file: figures/context-language-models/figure8.png
    article: context-language-models
    src: figure8.png
    caption: 圖 7 — KV Store（32K 預算）上的 skill 演化。Assisted 用 Qwen3.6-27B 搭配 Claude Fable 5.1 當 proposer，self-evolution 由 Opus 5 兼任兩個角色。（來源：原始論文 Figure 8。）
    sha256: ce04d2ade4a1da8d9e18459598e6d28cd34d0ed257a9caac6a88be5d35753c64
  importance: 15
  status: normal
- id: c16
  role: mechanism
  text: 可遷移的規則：嘗試的候選越多，dev 數字越膨脹，要報成績就用沒參與挑選的 test；看到任何「取最好的一次」的數字都要打折，例如 best-of-three；任何自動優化 prompt、skill、超參數的迴圈都適用，不限於這篇論文
  source_quotes:
  - "嘗試的候選越多，dev 數字越膨脹。要報成績就用沒參與挑選的 test。"
  - "看到任何「取最好的一次」的數字都要打折，例如 best-of-three（EdgeBench 就是）。"
  - "任何自動優化 prompt、skill、超參數的迴圈都適用，不限於這篇論文。"
  anchor_type: 部落格判斷
  importance: 16
  status: normal
- id: c17
  role: evaluation
  text: skill 演化證明的是「有 skill 比沒 skill 好」，不是「演化出的 skill 比人手寫的好」；「演化後的 CLM 在 EdgeBench 這類長時間任務上更強」，論文沒有這組實驗。blog 的結論是：skill 演化說的是「可學習性」，不是「更強」
  source_quotes:
  - "但起點是「完全沒有管理指令」，所以證明的是「有 skill 比沒 skill 好」，不是「演化出的 skill 比人手寫的好」。"
  - "兩者都沒有在長時間任務上驗證：「訓練或演化後的 CLM，在 EdgeBench 這類任務上更強」，論文沒有這組實驗。"
  - "結論是：RL 與 skill 演化說的是「可學習性」，不是「更強」。"
  anchor_type: 部落格判斷
  importance: 17
  status: normal
```
