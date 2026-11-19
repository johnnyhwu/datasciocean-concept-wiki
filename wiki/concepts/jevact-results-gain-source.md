---
id: jevact-results-gain-source
title: JevAct 的增益主要來自程式檢查，Kev 的額外貢獻依 agent 而定，Telecom 的大幅進步要打折看；看到「加了裁判模型就進步」時，先問安慰劑組和純程式組的分數
type_hint: 發現
context_type: bound_to_source
sources:
- article: jevact
  article_title: "JevAct：讓 AI Agent 三思而後行的執行前閘門"
  url: https://datasciocean.com/paper-intro/jevact/
  sections:
  - LLM agent 最怕做錯事：JevAct 在動手前加一道閘門
  - 一張地圖：兩層、兩個 gate
  - 決策迴圈：被擋的提案帶著回饋重來
  - Kev 只在 95% 有把握時才說「不」
  - hand-off check 怎麼判
  - BFCL：沒有政策文件時的通用檢查
  - 實驗：增益主要來自程式，不是 Kev
  - 三個指標：做不做得到、穩不穩定
  - 主結果：Telecom 大進步，但要打折
  - 功勞拆解：大部分是計算機的功勞
  - 盲區：題目只看政策，看不到使用者要什麼
  - 其他實驗與還沒回答的問題
  - 結論：回顧全文與值得帶走的重點
  - 審核表：文字說明與範例對不上
  first_appearance: true
parent: null
related:
  - jevact-pre-execution-gate
  - policy-split-derive-questions-rules
  - handoff-checklist-not-discussed-not-ruled-out
  - policy-checks-blind-to-user-request
  - decisionrag-results-gain-source
  - verifier-results-how-to-read
  - ragu-results-peeling-confounds
  - jevmem-results-gain-source
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 增益主要來自程式檢查；Kev 的額外貢獻依 agent 而定；Telecom 的大幅進步要打折看
  source_quotes:
  - "先講結論：增益主要來自程式檢查；Kev 的額外貢獻依 agent 而定；Telecom 的大幅進步要打折看。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 「增益主要來自程式」的根據是在 Airline 上以 GPT-4.1 為 agent 做的一次單次 write gate 消融
    source_quote: "論文在 Airline 上以 GPT-4.1 為 agent，做了一次單次 write gate 的消融"
  - text: 消融只在 50 題上跑一次
    source_quote: "消融只在 50 題上跑一次。"
  - text: 換用 gpt-oss-120b 當使用者模擬器時，Telecom 的增益消失
    source_quote: "換用 gpt-oss-120b 當使用者模擬器時，…區間跨過 0），增益消失。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: JevAct 是 IBM SIL 提出的方法，在 LLM agent「提出動作」和「執行動作」之間加一道閘門，只攔寫入型工具呼叫（write call，會改變資料庫的呼叫）與放棄或轉接真人（hand-off）兩類動作；擔任裁判的是 Kev，一個便宜的外部開源決策模型，只跑一次 forward pass 就直接給出每個固定選項的機率。檢查寫入的 write gate 用三種材料：計算機（編譯器寫出的 derive 函式，從工具紀錄計算事實）、閱讀員（給 Kev 回答的單一事實 yes/no 題）、審核表（把 Kev 的答案組合起來的布林規則）；檢查放棄的關卡叫 hand-off check
  source_quotes:
  - "IBM SIL 的 Iftach Shoham、Yuval David 等人提出的 JevAct，在 agent「提出動作」和「執行動作」之間加了一道閘門，只攔兩類難以挽回的動作：寫入型工具呼叫（write call），也就是會改變資料庫的呼叫；以及放棄或轉接真人（hand-off）。"
  - "擔任裁判的不是另一個大型 LLM，而是 Kev：一個便宜的外部開源決策模型。它讀一段 prompt，只跑一次 forward pass（模型把輸入從頭算過一遍；這裡只做讀入輸入的 prefill，不生成任何文字），就直接給出每個固定選項的機率。"
  - "檢查寫入的關卡叫 write gate，檢查放棄的關卡叫 hand-off check。write gate 用三種材料：計算機（編譯器寫出的 derive 函式，從工具紀錄計算事實）、閱讀員（給 Kev 回答的單一事實 yes/no 題）、審核表（把 Kev 的答案組合起來的布林規則）。"
  anchor_type: 設計參數
  qualifiers:
  - text: hand-off check 只在 Telecom 啟用，原因是 Airline 誤擋
    source_quote: "hand-off check 只在 Telecom 啟用，原因就是開頭提到的 Airline 誤擋。"
  - text: 論文實際的 cancel_reservation 規則交給 Kev 的是一題總結題（至少符合一項條件），不是單一條件題
    source_quote: "但它附上的 `cancel_reservation` 實際規則裡沒有 or，而是交給 Kev 一題總結題來回答。"
  importance: 2
  status: normal
- id: c3
  role: context
  text: 實驗用了三個 benchmark：τ²-bench 的 Airline（航空客服）與 Telecom（電信客服），以及 BFCL（工具呼叫能力測試）；τ²-bench 的使用者由另一個 LLM 扮演，稱為使用者模擬器。論文用的是 BFCL 的多輪版本，沒有政策文件，不跑編譯器，改用兩個固定問題的通用檢查，分別是 write gate 與 hand-off check 的簡化版
  source_quotes:
  - "實驗用了三個 benchmark：\\( \\tau^2 \\)-bench 的 Airline（航空客服）與 Telecom（電信客服），以及 BFCL（工具呼叫能力測試）。"
  - "\\( \\tau^2 \\)-bench 的使用者由另一個 LLM 扮演，稱為使用者模擬器。"
  - "論文用它的多輪版本：沒有政策文件，使用者每一輪說什麼都是事先寫死的。因此 BFCL 上不跑編譯器，改用兩個固定問題的通用檢查，分別是 write gate 與 hand-off check 的簡化版。"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c4
  role: context
  text: 每個任務跑 3 次，用三個指標看結果：pass@3 是 3 次中至少成功 1 次的任務比例（做不做得到），pass^3 是 3 次全部成功的任務比例（穩不穩定），pass^1 是單次執行的平均成功率。所有比較都是同一個 agent LLM 分別跑 ReAct（提出動作就直接執行、中間沒有閘門的標準 agent 迴圈）與 JevAct，只差在包在模型外面、負責執行迴圈的那層程式（harness）
  source_quotes:
  - "每個任務跑 3 次，用三個指標看結果："
  - "pass@3：3 次中至少成功 1 次的任務比例，量的是「做不做得到」。"
  - "3 次全部成功的任務比例，量的是「穩不穩定」。"
  - "單次執行的平均成功率。"
  - "所有比較都是同一個 agent LLM 分別跑 ReAct 與 JevAct，只差在包在模型外面、負責執行迴圈的那層程式（harness）。"
  - "ReAct 是提出動作就直接執行、中間沒有閘門的標準 agent 迴圈，也是本文實驗的對照組。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 3
  status: normal
- id: c5
  role: evidence
  text: Telecom（114 題）上 8 個 agent 兩項指標全部進步，平均 pass@3 +16.0、pass^3 +16.9 個百分點
  source_quotes:
  - "| Telecom（114 題） | 8 個 agent 兩項指標全部進步；平均 pass@3 +16.0、\\( \\text{pass}^3 \\) +16.9 個百分點 | 見下方兩點 |"
  - "所有比較都是同一個 agent LLM 分別跑 ReAct 與 JevAct"
  anchor_type: 實驗結果
  comparison_target: 同一個 agent LLM 跑 ReAct
  qualifiers:
  - text: 換用 gpt-oss-120b 當使用者模擬器時，pass^3 的變化是 −1.8（95% 信賴區間 −7.9 到 +4.4，跨過 0），增益消失；論文沒說明這一組用的是哪個 agent
    source_quote: "換用 gpt-oss-120b 當使用者模擬器時，…的變化是 −1.8（95% 信賴區間 −7.9 到 +4.4，區間跨過 0），增益消失。論文未說明這一組用的是哪個 agent。"
  - text: 放棄前清單在一次結果檢討後修改過，但論文沒說檢討了哪些任務；blog 推論如果其中包含測試集，Telecom 的數字會偏高
    source_quote: "附錄 A.1 末段另外提到，放棄前清單在一次結果檢討後修改過，但沒說檢討了哪些任務。（我的推論）如果其中包含測試集，Telecom 的數字會偏高。"
  figures:
  - file: figures/jevact/table2.png
    article: jevact
    src: table2.png
    caption: 表 1 — 主結果（%），每組比較使用同一個 LLM，只差在 harness（來源：原始論文 Table 2。）
    sha256: 6ef8ef3231a980b33e5f4b87dda7c25cd1b72d56a83c0eacd35a3ea732976ca8
  importance: 2
  status: normal
- id: c6
  role: qualifier
  text: Telecom 的第一個打折因素是換用 gpt-oss-120b 當使用者模擬器時，pass^3 的變化是 −1.8（95% 信賴區間 −7.9 到 +4.4，區間跨過 0），增益消失；論文沒說明這一組用的是哪個 agent
  source_quotes:
  - "Telecom 的數字有兩個打折因素："
  - "換用 gpt-oss-120b 當使用者模擬器時，…的變化是 −1.8（95% 信賴區間 −7.9 到 +4.4，區間跨過 0），增益消失。論文未說明這一組用的是哪個 agent。"
  - "所有比較都是同一個 agent LLM 分別跑 ReAct 與 JevAct"
  anchor_type: 實驗結果
  comparison_target: 同一個 agent LLM 跑 ReAct
  importance: 2
  status: normal
- id: c7
  role: qualifier
  text: Telecom 的第二個打折因素是放棄前清單在一次結果檢討後修改過，但論文沒說檢討了哪些任務；blog 推論如果其中包含測試集，Telecom 的數字會偏高
  source_quotes:
  - "附錄 A.1 末段另外提到，放棄前清單在一次結果檢討後修改過，但沒說檢討了哪些任務。（我的推論）如果其中包含測試集，Telecom 的數字會偏高。"
  anchor_type: 部落格推論
  importance: 3
  status: normal
- id: c8
  role: evidence
  text: Airline（50 題）上 pass^3 有 4 個 agent 進步、2 個退步；1 題就差 2 個百分點，看不出差異
  source_quotes:
  - "| Airline（50 題） | \\( \\text{pass}^3 \\) 有 4 個 agent 進步、2 個退步 | 1 題就差 2 個百分點，看不出差異 |"
  - "所有比較都是同一個 agent LLM 分別跑 ReAct 與 JevAct"
  anchor_type: 實驗結果
  comparison_target: 同一個 agent LLM 跑 ReAct
  figures:
  - file: figures/jevact/table2.png
    article: jevact
    src: table2.png
    caption: 表 1 — 主結果（%），每組比較使用同一個 LLM，只差在 harness（來源：原始論文 Table 2。）
    sha256: 6ef8ef3231a980b33e5f4b87dda7c25cd1b72d56a83c0eacd35a3ea732976ca8
  importance: 3
  status: normal
- id: c9
  role: evidence
  text: BFCL（800 題）上 pass^3 九個 agent 全部進步（+0.1 到 +9.6），但 pass@3 有 5 個退步；blog 的解讀是變穩了，但沒有多解出新題
  source_quotes:
  - "| BFCL（800 題） | \\( \\text{pass}^3 \\) 九個 agent 全部進步（+0.1 到 +9.6） | pass@3 有 5 個退步：變穩了，但沒有多解出新題 |"
  - "所有比較都是同一個 agent LLM 分別跑 ReAct 與 JevAct"
  anchor_type: 實驗結果
  comparison_target: 同一個 agent LLM 跑 ReAct
  figures:
  - file: figures/jevact/table2.png
    article: jevact
    src: table2.png
    caption: 表 1 — 主結果（%），每組比較使用同一個 LLM，只差在 harness（來源：原始論文 Table 2。）
    sha256: 6ef8ef3231a980b33e5f4b87dda7c25cd1b72d56a83c0eacd35a3ea732976ca8
  importance: 3
  status: normal
- id: c10
  role: evidence
  text: 論文在 Airline 上以 GPT-4.1 為 agent 做了一次單次 write gate 的消融，pass^1 是 ReAct（無 gate）50.0、只用計算機 68.0、完整 JevAct 72.0；對照用的「安慰劑」組每個寫入都擋一次、不看對錯，用來檢驗「光是多一次重來的機會」值多少分，結果是 50.0
  source_quotes:
  - "論文在 Airline 上以 GPT-4.1 為 agent，做了一次單次 write gate 的消融（來源：原始論文 Table 3）。其中的「安慰劑」組是對照：每個寫入都擋一次，不看對錯，用來檢驗「光是多一次重來的機會」值多少分。"
  - "| ReAct（無 gate） | 50.0 |"
  - "| 只用計算機 | 68.0 |"
  - "| 完整 JevAct | 72.0 |"
  - "| 安慰劑：每個寫入都擋一次，不看對錯 | 50.0 |"
  anchor_type: 實驗結果
  comparison_target: ReAct（無 gate）的 50.0
  qualifiers:
  - text: 消融只在 50 題上跑一次
    source_quote: "消融只在 50 題上跑一次。"
  importance: 2
  status: normal
- id: c11
  role: evaluation
  text: 22 個百分點的增益中，計算機單獨就貢獻 18 點；Kev 在計算機之上再多 4 點，相當於 50 題中的 2 題，落在雜訊範圍內
  source_quotes:
  - "22 個百分點的增益中，計算機單獨就貢獻 18 點；Kev 在計算機之上再多 4 點，相當於 50 題中的 2 題，落在雜訊範圍內。"
  - "| ReAct（無 gate） | 50.0 |"
  anchor_type: 部落格考證
  comparison_target: 增益是對 ReAct（無 gate）；Kev 的 4 點是對「只用計算機」
  qualifiers:
  - text: 這是 Airline、GPT-4.1 為 agent 的單次 write gate 消融
    source_quote: "論文在 Airline 上以 GPT-4.1 為 agent，做了一次單次 write gate 的消融"
  - text: 消融只在 50 題上跑一次
    source_quote: "消融只在 50 題上跑一次。"
  importance: 2
  status: normal
- id: c12
  role: evidence
  text: 另一組跑 3 次的補充實驗（使用者模擬器固定為 gpt-oss-120b，數字都是 pass^3）：GPT-4.1 起點（無 gate）26、安慰劑 28（幾乎無效）、完整 gate 40；gpt-oss-120b 起點 32、安慰劑 42、以 gate 相同比例隨機擋 42、完整 gate 42
  source_quotes:
  - "論文正文另有一組跑 3 次的補充實驗，使用者模擬器固定為 gpt-oss-120b，比較兩個 agent，數字都是 \\( \\text{pass}^3 \\)。"
  - "| agent | 起點（無 gate） | 安慰劑 | 以 gate 相同比例隨機擋 | 完整 gate | 解讀 |"
  - "| GPT-4.1 | 26 | 28（幾乎無效） | — | 40 | Kev 的判斷有貢獻 |"
  - "| gpt-oss-120b | 32 | 42 | 42 | 42 | 功勞全來自「多一次重來的機會」 |"
  anchor_type: 實驗結果
  comparison_target: 同一個 agent 的起點（無 gate）、安慰劑與隨機擋
  importance: 3
  status: normal
- id: c13
  role: evaluation
  text: 在另一組跑 3 次的補充實驗裡（不是 Airline 單次 write gate 的那次消融），Kev 有沒有用取決於 agent：對 GPT-4.1 來說，每個寫入都擋一次（安慰劑）幾乎沒用，Kev 的判斷確實有貢獻；對 gpt-oss-120b 來說，不管是安慰劑、隨機擋還是讓 Kev 判斷，結果都一樣，進步只來自多了一次重來的機會
  source_quotes:
  - "論文正文另有一組跑 3 次的補充實驗，使用者模擬器固定為 gpt-oss-120b，比較兩個 agent，數字都是 \\( \\text{pass}^3 \\)。結果顯示 Kev 有沒有用取決於 agent："
  - "白話：對 GPT-4.1 來說，每個寫入都擋一次（安慰劑）幾乎沒用，Kev 的判斷確實有貢獻；對 gpt-oss-120b 來說，不管是安慰劑、隨機擋還是讓 Kev 判斷，結果都一樣，進步只來自多了一次重來的機會。"
  anchor_type: 部落格判斷
  comparison_target: 同一個 agent 的起點（無 gate）、安慰劑與隨機擋
  qualifiers:
  - text: 這組補充實驗的使用者模擬器固定為 gpt-oss-120b，只比較兩個 agent
    source_quote: "使用者模擬器固定為 gpt-oss-120b，比較兩個 agent"
  importance: 2
  status: normal
- id: c14
  role: evidence
  text: judge 大小的結果（檢查與門檻全都固定為 Kev-27B 設定的版本，只換 Kev 的大小；Kev 有 0.8B、9B、27B 三種）是模型越大不一定越好，Telecom 上小 Kev 常常更好；而在同一批 Telecom 轉接狀態的離線重播裡，9B 與 27B 的決策一致率是 97.0%
  source_quotes:
  - "Kev 有 0.8B、9B、27B 三種尺寸"
  - "檢查與門檻全都固定為 Kev-27B 設定的版本，只換 Kev 的大小"
  - "表 4 則是離線重播：同一批 Telecom 轉接狀態交給三種大小的 Kev，看各自擋下幾次、和 Kev-27B 的決策有多一致"
  - "| judge 大小（表 3、表 4） | 模型越大不一定越好，Telecom 上小 Kev 常常更好；9B 與 27B 的決策一致率 97.0% | 線上分數的差異，無法用判斷品質解釋 |"
  anchor_type: 實驗結果
  comparison_target: 一致率是 9B 對 Kev-27B 的決策；「小 Kev 更好」是對 Kev-27B 的線上分數
  figures:
  - file: figures/jevact/table5.png
    article: jevact
    src: table5.png
    caption: 表 3 — judge 大小消融，編譯出的檢查與門檻都固定為 Kev-27B 設定的版本（來源：原始論文 Table 5。）
    sha256: d8181c637f606c4625e72dbaea7c14d85b6bc69712b1a88d3d4f1f0fdab2d9a2
  - file: figures/jevact/table7.png
    article: jevact
    src: table7.png
    caption: 表 4 — 三種 Kev 大小離線重播同一批 Telecom 轉接狀態（來源：原始論文 Table 7。）
    sha256: 259b07dffe8dcbeb405f47abe2320e7d069d692c5b445e609d8af72d44754bb5
  importance: 3
  status: normal
- id: c15
  role: evaluation
  text: 模型大小的結果互相矛盾，論文也沒有解釋；blog 推論，Telecom 上小 Kev 的分數常常更好，但 9B 與 27B 的決策一致率高達 97.0%，分數差異不像是來自判斷品質
  source_quotes:
  - "模型大小的結果互相矛盾，論文也沒有解釋。（我的推論）例如上方總結表的 judge 大小那一列：Telecom 上小 Kev 的分數常常更好，但 9B 與 27B 的決策一致率高達 97.0%，分數差異不像是來自判斷品質。"
  anchor_type: 部落格推論
  comparison_target: 一致率是 9B 對 Kev-27B 的決策
  importance: 3
  status: normal
- id: c16
  role: evidence
  text: 長輸入的比較把 Airline 開發階段 260 個人工標註的寫入呼叫依輸入是否超過 8,192 tokens 分成兩組；在長輸入上，9B 的 AUROC 是 0.61，27B 是 0.85（AUROC 是把「錯誤呼叫排在正確呼叫前面」的能力量成 0 到 1 的分數，不需要設門檻，0.5 等於亂猜）。0.8B 與 9B 驗證過的 context 長度是 8,192 tokens，27B 是 65,536 tokens
  source_quotes:
  - "長輸入的比較在表 5，把 260 個標註寫入呼叫依輸入是否超過 8,192 tokens 分成兩組"
  - "在長輸入上，9B 的 AUROC 是 0.61，27B 是 0.85 | 小模型主要輸在 context 長度；在短輸入上重調門檻可以補回一部分"
  - "是把「錯誤呼叫排在正確呼叫前面」的能力量成 0 到 1 的分數，不需要設門檻；0.5 等於亂猜。"
  - "驗證過的 context 長度：0.8B 與 9B 為 8,192 tokens，27B 為 65,536 tokens；這點在後面的長輸入實驗會用到。"
  - "資料來自 Airline 開發階段 260 個人工標註的寫入呼叫"
  anchor_type: 實驗結果
  comparison_target: 同一組長輸入上 9B 對 27B
  qualifiers:
  - text: blog 的解讀是小模型主要輸在 context 長度
    source_quote: "小模型主要輸在 context 長度"
  - text: 在短輸入上重調門檻可以補回一部分
    source_quote: "在短輸入上重調門檻可以補回一部分"
  figures:
  - file: figures/jevact/table8.png
    article: jevact
    src: table8.png
    caption: 表 5 — 260 個標註寫入呼叫上的離線比較，分短輸入與長輸入兩組（來源：原始論文 Table 8。）
    sha256: 94f852f1bb879e0a8e5cc90fd4f1289a9dac33238ff48564606e91c9f9e7d49f
  importance: 4
  status: normal
- id: c17
  role: evaluation
  text: 論文的核心問題是「決策模型能不能當驗證器」，但數據沒有好好回答它
  source_quotes:
  - "論文的核心問題是「決策模型能不能當驗證器」，但數據沒有好好回答它。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c18
  role: evaluation
  text: 看到「加了裁判模型就進步」時，先問安慰劑組和純程式組的分數；這篇在 Airline 上的答案是大部分功勞屬於計算機
  source_quotes:
  - "第二，看到「加了裁判模型就進步」時，先問安慰劑組和純程式組的分數，這篇在 Airline 上的答案是大部分功勞屬於計算機"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 消融只在 50 題上跑一次
    source_quote: "消融只在 50 題上跑一次。"
  importance: 2
  status: normal
```
