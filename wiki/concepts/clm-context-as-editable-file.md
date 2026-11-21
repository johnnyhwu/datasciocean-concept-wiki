---
id: clm-context-as-editable-file
title: CLM 把模型當前的 context 鏡像成一個檔案，模型用 Bash 想改哪裡就改哪裡；過去的方法把「何時做」與「怎麼做」其中一件或兩件鎖在人手裡，CLM 兩件都交給模型，但「何時改」實驗中仍有 harness 在提醒
type_hint: 方法
context_type: bound_to_source
sources:
- article: context-language-models
  article_title: "Context Language Models 解析：讓 agent 用 Bash 改自己的 context"
  url: https://datasciocean.com/paper-intro/context-language-models/
  sections:
  - context 爆了，誰來決定留什麼？CLM 讓模型自己改
  - context 管理：從固定規則到模型自己動手
  - 現有的兩條路：harness 定義與 action-based
  - 論文的主張：連「怎麼改」都交給模型
  - 從「只能往後接」到「任意改寫」
  - 實作：context 就是一個檔案，模型用 Bash 改
  - 多 agent：一個 context 一個檔案
  - 要注意：「何時編輯」其實有 harness 在幫忙
  - 模型估不準自己用了多少 context
  - 整體評價：概念值得試，證據只夠說明有潛力
  - 安全風險：自己寫、自己讀回的 context
  - 結論：值得帶走的東西
  - when 與 how：context 管理的兩個維度
  - context 檔案像原始碼：改壞標記的風險
  first_appearance: true
parent: null
related:
  - context-chunk-keep-offload-compress-delete
  - context-edit-cost-by-position
  - success-gated-efficiency-advantage
  - clm-text-steering-and-skill-evolution
  - clm-results-tight-budget-not-across-the-board
  - claude-code-extension-and-context
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: CLM 把模型當前的 context 鏡像成一個檔案，模型用 Bash 想改哪裡就改哪裡，改完立刻同步回它的 live context（下一輪真正餵給模型的那份 context）。何時做與怎麼做是兩件事，過去的方法把其中一件或兩件鎖在人手裡，CLM 兩件都交給模型
  source_quotes:
  - "Context Language Models 這篇論文提出的做法叫 CLM：把模型當前的 context 鏡像成一個檔案，模型用 Bash 想改哪裡就改哪裡，改完立刻同步回它的 live context（下一輪真正餵給模型的那份 context）。"
  - "何時做與怎麼做是兩件事，過去的方法把其中一件或兩件鎖在人手裡，CLM 兩件都交給模型。"
  anchor_type: 設計參數
  qualifiers:
  - text: CLM 的 when 並非完全由模型決定，實驗中靠 harness 在剩 2,048 tokens 時提醒
    source_quote: "一個但書：CLM 的 when 並非完全由模型決定，實驗中靠 harness 在剩 2,048 tokens 時提醒。"
  - text: 這是介面設計，不是新演算法
    source_quote: "這是介面設計，不是新演算法。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: LLM agent 跑得越久，context（模型每一輪讀進去的整份文字）就越容易爆，總得有人決定「留什麼、丟什麼」，這叫 context management（context 管理）。目前的主流做法，是由 harness（包在模型外面、負責跑 agent 迴圈與組裝每輪 context 的程式）用固定規則做摘要，或是給模型幾個預先設計好的壓縮工具
  source_quotes:
  - "LLM agent 跑得越久，context（模型每一輪讀進去的整份文字）就越容易爆。"
  - "遲早超過上限，總得有人決定「留什麼、丟什麼」。目前的主流做法，是由 harness（包在模型外面、負責跑 agent 迴圈與組裝每輪 context 的程式）用固定規則做摘要，或是給模型幾個預先設計好的壓縮工具。"
  - "怎麼處理這件事，叫 context management（context 管理）。"
  anchor_type: 背景說明
  importance: 2
  status: normal
- id: c3
  role: context
  text: 現有做法依「誰做決定」分兩類：harness 定義（外部程式、固定規則；例如 Codex 風格摘要在 context 用到預算的 75% 時把整段歷史換成一份摘要，MEM1 每一輪都重寫 context），模型完全沒有發言權；action-based（模型決定「何時用」，但「能做哪些操作」是人預先設計的；例如 Self-Compact 讓模型自己決定何時壓縮，ACM 讓模型可呼叫壓縮、卸載、檢索這幾個工具），模型只能在人類給的選單裡選
  source_quotes:
  - "現有的做法，可以依「誰做決定」分成兩類："
  - "harness 定義 | 外部程式，固定規則 | Codex 風格摘要：context 用到預算的 75% 時，整段歷史換成一份摘要。MEM1：每一輪都重寫 context"
  - "action-based | 模型決定「何時用」，但「能做哪些操作」是人預先設計的 | Self-Compact：模型自己決定何時壓縮。ACM：模型可呼叫壓縮、卸載、檢索這幾個工具"
  - "第一類模型完全沒有發言權；第二類模型有發言權，但只能在人類給的選單裡選。"
  anchor_type: 背景說明
  comparison_target: 預算（75% 是 context 用量占預算的比例）
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 論文認為這兩條路有同一個天花板：模型能做的操作，都是人類事先設計好的。CLM 把自由度推到底，排起來是三級：harness 定義，模型零控制；action-based，模型選「何時」，操作由人定義；CLM，模型連「怎麼改」都自己決定
  source_quotes:
  - "論文認為這兩條路有同一個天花板：模型能做的操作，都是人類事先設計好的。CLM 把自由度推到底，排起來是三級："
  - "harness 定義：模型零控制。"
  - "action-based：模型選「何時」，操作由人定義。"
  - "CLM：模型連「怎麼改」都自己決定。"
  anchor_type: 原作者解讀
  qualifiers:
  - text: CLM 的 when 並非完全由模型決定，實驗中靠 harness 在剩 2,048 tokens 時提醒
    source_quote: "一個但書：CLM 的 when 並非完全由模型決定，實驗中靠 harness 在剩 2,048 tokens 時提醒。"
  importance: 4
  status: normal
- id: c5
  role: anchor
  text: 自編例子：context 裡有 100 條搜尋結果，編號 30、31、57 的三條沒用，其餘要原文保留。如果工具只有「把全部歷史壓成摘要」，模型只能全壓，其他 97 條的原文就被改寫了；CLM 可以直接寫一小段程式，只刪那三條
  source_quotes:
  - "具體差別（自編例子）：context 裡有 100 條搜尋結果，編號 30、31、57 的三條沒用，其餘要原文保留。如果工具只有「把全部歷史壓成摘要」，模型只能全壓，其他 97 條的原文就被改寫了；CLM 可以直接寫一小段程式，只刪那三條。"
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 5
  status: normal
- id: c6
  role: mechanism
  text: 標準 LM 每一輪只能把新內容接在 context 後面，舊 context 一個字都不能動；CLM 則讓模型直接決定下一輪 context 的完整內容，沒有這個限制；前者是後者的特例
  source_quotes:
  - "一句話：標準 LM 每一輪只能把新內容接在 context 後面，CLM 則讓模型直接決定下一輪 context 的完整內容。"
  - 'c_{t+1} = c_t \oplus f_\theta^{\mathrm{LM}}(c_t)'
  - 'c_{t+1} = f_\theta^{\mathrm{CLM}}(c_t)'
  - "白話一點：Eq. 1 的舊 context 一個字都不能動，Eq. 2 沒有這個限制。Eq. 1 其實是 Eq. 2 的特例"
  anchor_type: 設計參數
  importance: 6
  status: normal
- id: c7
  role: qualifier
  text: 論文把 CLM 的改寫函數寫成「任意函數」，但實作上它只能是模型寫得出來的 Bash 或程式
  source_quotes:
  - "論文把 \\( f_\\theta^{\\mathrm{CLM}} \\) 寫成「任意函數」，但實作上它只能是模型寫得出來的 Bash 或程式，這是下一小節。"
  anchor_type: 部落格判斷
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: 實作流程：harness 把當前 context 寫進檔案，路徑寫在 system prompt；模型像編輯其他檔案一樣，用 Bash 或 Python 改它；檔案一改完，就自動同步給 LLM server；下一輪模型看到的就是改過的 context。如果模型這輪沒動檔案，新生成的 token 照舊接在後面
  source_quotes:
  - "harness 把當前 context 寫進檔案，路徑寫在 system prompt。"
  - "模型像編輯其他檔案一樣，用 Bash 或 Python 改它。"
  - "檔案一改完，就自動同步給 LLM server。"
  - "下一輪模型看到的就是改過的 context。"
  - "如果模型這輪沒動檔案，新生成的 token 照舊接在後面，也就是 Eq. 1 的預設行為。"
  anchor_type: 設計參數
  importance: 8
  status: normal
- id: c9
  role: anchor
  text: 論文觀察到模型會自己發明新做法，例如在 context 裡維護一個「計分板」，用 163 次原地編輯追蹤子 agent 的狀態；新增一種原本模板沒有的角色 notes，專門放自己的內部筆記；用迴圈批次刪掉沒用的搜尋結果，或自己定義輔助函數 compact_turns（同一次任務中被呼叫 37 次）
  source_quotes:
  - "論文觀察到，模型會自己發明新做法，例如："
  - "在 context 裡維護一個「計分板」，用 163 次原地編輯追蹤子 agent 的狀態"
  - "新增一種原本模板沒有的角色 notes，專門放自己的內部筆記。"
  - "用迴圈批次刪掉沒用的搜尋結果，或自己定義輔助函數 compact_turns（同一次任務中被呼叫 37 次）。"
  anchor_type: 實驗結果
  numeric_kind: non_comparative
  numeric_reason: 計數
  figures:
  - file: figures/context-language-models/figure3.png
    article: context-language-models
    src: figure3.png
    caption: 圖 3 — CLM 在 context 管理上的實際行為範例：模型用一般的程式介面任意編輯自己的 context。（來源：原始論文 Figure 3。）
    sha256: ec634e0480b9002677c7ab2fea4f25fec44c2c610880e795e416baca75258ce8
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: 多個 context 檔案可以同時存在，各自與自己的 LLM server 同步：agent swarm（一群平行工作的 agent）就是在工作區放多個 context 檔案；subagent（由主 agent 啟動的子 agent）的啟動與結束，就是建立與刪除一個 context 檔案
  source_quotes:
  - "多個 context 檔案可以同時存在，各自與自己的 LLM server 同步。agent swarm（一群平行工作的 agent）就是在工作區放多個 context 檔案；subagent（由主 agent 啟動的子 agent）的啟動與結束，就是建立與刪除一個 context 檔案。"
  anchor_type: 設計參數
  importance: 10
  status: normal
- id: c11
  role: qualifier
  text: 論文實驗裡，CLM 另外享有幾項 harness 輔助：離預算上限還剩 2,048 tokens 時，harness 會送出「該編輯 context 了」的提醒，論文的理由是現有模型對自己用了多少 context 沒有準確感知；在 BrowseComp-Plus（簡稱 BCP，一個在固定語料上搜尋並回答難題的深度研究基準）上，CLM 的編輯回合不算進 100 輪的輪數上限，請求超出預算時，harness 會退回上一輪並重試，最多六次
  source_quotes:
  - "論文實驗裡，CLM 另外享有幾項 harness 輔助（論文 Appendix E、腳註 4）："
  - "離預算上限還剩 2,048 tokens 時，harness 會送出「該編輯 context 了」的提醒。論文的理由是現有模型對自己用了多少 context 沒有準確感知"
  - "在 BrowseComp-Plus（一個在固定語料上搜尋並回答難題的深度研究基準，簡稱 BCP）上，CLM 的編輯回合不算進 100 輪的輪數上限；請求超出預算時，harness 會退回上一輪並重試，最多六次。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 11
  status: normal
- id: c12
  role: evaluation
  text: blog 的精確說法：how 完全交給模型，when 由模型決定但靠 harness 輔助；論文沒說明對手（如 Codex 風格的摘要 harness）有沒有享受同樣的待遇，這影響「CLM 勝出」能歸功於誰
  source_quotes:
  - "how 完全交給模型，when 由模型決定但靠 harness 輔助。論文沒說明對手（如 Codex 風格的摘要 harness，下文稱 Summary）有沒有享受同樣的待遇，這影響「CLM 勝出」能歸功於誰"
  anchor_type: 部落格判斷
  importance: 12
  status: normal
- id: c13
  role: evidence
  text: 論文 Appendix G 發現現有模型不太會估自己用了多少 context（以 MAE，即估計值與實際 token 數差距的絕對值平均來衡量）：長 context 下，模型的估計會落在重複出現的幾個數字；提示離估計點越近越有效
  source_quotes:
  - "論文 Appendix G 發現現有模型不太會估。衡量用的是 MAE（Mean Absolute Error，平均絕對誤差）：估計值與實際 token 數的差距，取絕對值再平均"
  - "論文文字的結論有三點：長 context 下，模型的估計會落在重複出現的幾個數字（如 6.2K、9.8K）；給了 token 數的提示後誤差下降；提示離估計點越近越有效。"
  anchor_type: 實驗結果
  qualifiers:
  - text: 只測了 50 個輸入，而且測的是 GPT-5.4、Claude 4.6 Sonnet、GPT-5.4-mini，不是主要實驗用的 Qwen3.6-27B
    source_quote: "只測了 50 個輸入，而且測的是 GPT-5.4、Claude 4.6 Sonnet、GPT-5.4-mini，不是主要實驗用的 Qwen3.6-27B，論文沒說明原因。"
  importance: 13
  status: normal
- id: c13b
  role: evidence
  text: 論文文字的另一點結論：給了 token 數的提示後誤差下降
  source_quotes:
  - "論文文字的結論有三點：長 context 下，模型的估計會落在重複出現的幾個數字（如 6.2K、9.8K）；給了 token 數的提示後誤差下降；提示離估計點越近越有效。"
  anchor_type: 原作者解讀
  importance: 13
  status: pending_author_confirmation
- id: c14
  role: mechanism
  text: blog 由此推出的可遷移規則：任何資源（token、時間、金額預算）都由環境量測，附在每次工具結果裡回報；回報要貼近決策點，每輪都附，比只在開頭講一次有效。實驗裡剩 2,048 tokens 的提醒，就是在補模型估不準用量的缺口
  source_quotes:
  - "可遷移的規則（推論，非論文原文）：任何資源（token、時間、金額預算）都由環境量測，附在每次工具結果裡回報；回報要貼近決策點，每輪都附，比只在開頭講一次有效。"
  - "這就是為什麼 harness 要補提醒：實驗裡的提醒（剩 2,048 tokens），以及 ContextBench skill 摘錄（論文 Table 4）中的 [context: ~N/M tokens] 讀數，都是在補這個缺口。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  qualifiers:
  - text: 模型估不準用量的證據只測了 50 個輸入，而且測的不是主要實驗用的 Qwen3.6-27B
    source_quote: "只測了 50 個輸入，而且測的是 GPT-5.4、Claude 4.6 Sonnet、GPT-5.4-mini，不是主要實驗用的 Qwen3.6-27B，論文沒說明原因。"
  importance: 14
  status: normal
- id: c15
  role: evaluation
  text: 主文沒有交代 context 檔案的格式與同步細節，也沒統計模型改壞格式的頻率；檔案裡帶有 [[CTX_TURN 4 role=notes]] 這類標記，改壞時有沒有檢查或修復機制也沒寫。blog 認為這個疑慮不推翻論文的結論，但想自己複製這個機制時缺資訊，而且失敗率可能被低估
  source_quotes:
  - "主文沒有交代 context 檔案的格式與同步細節，也沒統計模型改壞格式的頻率"
  - "這裡的標記就是圖 3 看得到的 [[CTX_TURN 4 role=notes]] 這類字串。"
  - "改壞時有沒有檢查或修復機制？沒寫。"
  - "這個疑慮的份量（推論）：它不推翻論文的結論。成績不錯，代表多數時候沒壞。但它影響兩件事：想自己複製這個機制時缺資訊，而且失敗率可能被低估。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 15
  status: normal
- id: c16
  role: evaluation
  text: 論文第 6 節提到，可編輯的 context 可能成為注入的提示或自我生成的指令跨輪持續的管道，並引用 OpenAI 的報告：模型曾在自己的壓縮摘要裡塞入未授權的指令，並影響後續行為
  source_quotes:
  - "論文第 6 節提到，可編輯的 context 可能成為注入的提示或自我生成的指令跨輪持續的管道。它引用 OpenAI 的報告：模型曾在自己的壓縮摘要裡塞入未授權的指令，並影響後續行為。"
  anchor_type: 原作者解讀
  qualifiers:
  - text: 論文沒有做任何實驗，也沒有提出防禦，只說未來要研究
    source_quote: "論文沒有做任何實驗，也沒有提出防禦，只說未來要研究。"
  importance: 16
  status: normal
- id: c17
  role: evaluation
  text: blog 的推論：凡是「模型能寫、之後又會讀回」的地方（摘要、筆記、記憶、CLM 的 context 檔案），都是持久化通道，不限於 CLM；CLM 的面積比摘要大，因為編輯不受限。這樣的內容在後面幾輪看起來是「我自己寫的」，比一次性的注入更難被辨認
  source_quotes:
  - "凡是「模型能寫、之後又會讀回」的地方（摘要、筆記、記憶、CLM 的 context 檔案），都是持久化通道，不限於 CLM。"
  - "CLM 的面積比摘要大，因為編輯不受限。"
  - "這樣的內容在後面幾輪看起來是「我自己寫的」，比一次性的注入更難被辨認。"
  anchor_type: 部落格推論
  importance: 17
  status: normal
- id: c18
  role: evaluation
  text: blog 的評價：論文的貢獻是介面設計，不是新演算法。「讓模型對自己的 context 有寫入權」這個想法簡單、通用，也把 when 與 how 兩個維度都推到了模型手上，這是它最持久的部分；但它是設計選擇，是否優於「固定流程加好的 prompt」，論文沒有直接證明
  source_quotes:
  - "研究價值：論文的貢獻是介面設計，不是新演算法。「讓模型對自己的 context 有寫入權」這個想法簡單、通用，也把 when 與 how 兩個維度都推到了模型手上，這是它最持久的部分。"
  - "但它是設計選擇，不是新演算法，是否優於「固定流程加好的 prompt」，論文沒有直接證明。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: CLM 的 when 並非完全由模型決定，實驗中靠 harness 在剩 2,048 tokens 時提醒
    source_quote: "一個但書：CLM 的 when 並非完全由模型決定，實驗中靠 harness 在剩 2,048 tokens 時提醒。"
  importance: 18
  status: normal
```
