---
id: ptc-batching-vs-reach
title: Bash 與 PTC 都能把多個動作合成一次模型呼叫，真正差別是能碰到什麼環境；PTC 是折衷：比只給 typed tools 省 token、分數大致持平，整體輸給 Bash，合規要求只能用固定工具目錄時才選它
type_hint: 判斷
context_type: bound_to_source
sources:
- article: is-bash-all-you-need
  article_title: "Is Bash All You Need？只給 agent 一個 shell，比整套專用工具更準又更省"
  url: https://datasciocean.com/paper-intro/is-bash-all-you-need/
  sections:
  - 只給 agent 一個 shell，分數反而更高
  - 企業 agent 的工具該怎麼給：兩條路各有代價
  - 怎麼比才公平：同一個模型、同一份任務，只換 agent 的雙手
  - 五種工具介面
  - 兩個企業工作 benchmark，typed tools 來源不同
  - Bash 對 Tool-only：四組設定全部同向
  - 同一件事，三種介面各怎麼做
  - 怎麼算分：分數、通過率、token 與配對差
  - PTC：省了 token，分數沒跟上
  - 這份證據能信幾分
  - 該怎麼選：先問合規，再問能不能隔離
  - 延伸：看到 A 贏 B，先檢查 B 是誰做的
  - 延伸：批次化不是 PTC 專屬，差別在能碰到的範圍
  first_appearance: true
parent: null
related:
  - bash-vs-typed-tools-results
  - bash-add-ons-no-detectable-gain
  - baseline-who-built-it
  - intermediate-results-out-of-context
  - claude-code-permission-blast-radius
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: Bash 與 PTC 都能把多個動作合成一次模型呼叫，它們的真正差別是能碰到什麼環境；PTC 是折衷：比只給 typed tools 省 token，分數大致持平，整體輸給 Bash，其中有一部分可能只是目錄覆蓋不夠
  source_quotes:
  - "Bash 與 PTC 都能把多個動作合成一次模型呼叫，它們的真正差別是能碰到什麼環境。"
  - "它比只給 typed tools 省 token，分數大致持平，整體輸給 Bash。"
  - "PTC 是折衷。 省 token、分數持平，輸給 Bash，其中有一部分可能只是目錄覆蓋不夠。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 「分數持平」有例外：PTC − Tool-only 的配對分數差在 TheAgentCompany 是 +3.5 pp [+0.8, +6.2]
    source_quote: "PTC − Tool-only：TheAgentCompany 是 +3.5 pp [+0.8, +6.2]，APEX-Agents 是 −1.5 pp [−3.9, +0.9]。"
  - text: 論文沒有把「做法」與「目錄覆蓋」拆開
    source_quote: "論文沒有把「做法」與「目錄覆蓋」拆開。"
  - text: 「目錄覆蓋不夠」這個混淆主要在目錄自製的 TheAgentCompany
    source_quote: "反過來，PTC 輸給 Bash 的那 +21.2 pp 與 +7.7 pp，有一部分可能只是目錄覆蓋不夠（Appendix B.1），而這個混淆主要在目錄自製的 TheAgentCompany。"
  - text: 跟 Bash 比，PTC 只在 TheAgentCompany／GPT-5.5 這一格比 Bash 省 token
    source_quote: "token：PTC 只在 TheAgentCompany／GPT-5.5 比 Bash 省（242k 對 377k）。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: "論文〈Is Bash All You Need? An Empirical Study of Tool Interfaces for Enterprise Digital Worker Agents〉（Microsoft、CMU）比的是企業 agent 的工具介面（tool interface），也就是 agent 用什麼方式對環境下動作：一端是 typed tool，預先定義好名稱與參數格式的函式，模型一次呼叫一個；另一端是直接給一個 bash shell（命令列），讓模型自己寫指令。論文作者用同一個模型、同一份任務文字、同一份基礎 prompt、同一套停止條件，只改變「agent 能怎麼動手」；Tool-only（只有 typed tools）是基準線"
  source_quotes:
  - "Is Bash All You Need? An Empirical Study of Tool Interfaces for Enterprise Digital Worker Agents（Microsoft、CMU"
  - "論文比的是工具介面（tool interface），也就是 agent 用什麼方式對環境下動作。一端是 typed tool：預先定義好名稱與參數格式的函式，例如 gitlab_create_issue，模型一次呼叫一個；另一端是直接給一個 bash shell（命令列），讓模型自己寫指令。"
  - "論文作者用同一個模型、同一份任務文字、同一份基礎 prompt、同一套停止條件，只改變「agent 能怎麼動手」"
  - "Tool-only | 只有 typed tools | 每個動作一次獨立呼叫，是基準線"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: PTC（Programmatic Tool Calling，程式化工具呼叫）是模型寫一小段 Python，程式裡只能呼叫預先定義的 typed tools；它介於兩者之間：保留固定工具目錄，又能 loop、串接、平行批次處理，但沒有 shell，也沒有其他能碰到環境的管道
  source_quotes:
  - "PTC（Programmatic Tool Calling，程式化工具呼叫：模型寫一小段程式，程式只能呼叫預先定義的工具）"
  - "PTC | 模型寫 Python，程式裡只能呼叫 typed tools | 介於兩者之間：保留固定工具目錄，又能 loop、串接、平行批次處理；但沒有 shell，也沒有其他能碰到環境的管道"
  anchor_type: 設計參數
  qualifiers:
  - text: PTC 額外加了介面專屬的 prompt 指示
    source_quote: "只有 Bash+Synthesis 與 PTC 額外加了介面專屬的 prompt 指示，其餘介面共用同一份基礎 prompt。"
  importance: 2
  status: normal
- id: c4
  role: context
  text: Anthropic 與 OpenAI 的 API 提供 PTC（受限在固定工具目錄內）
  source_quotes:
  - "Anthropic 與 OpenAI 的 API 提供 PTC（受限在固定工具目錄內）"
  anchor_type: 背景說明
  importance: 5
  status: normal
- id: c5
  role: context
  text: 批次化是一次模型呼叫（一個回合）完成多個對環境的動作，減少模型與工具之間的往返次數，也減少中間結果進入上下文；Tool-only 不能批次，每個動作是一次獨立呼叫；Bash 能用 pipe、&&、迴圈、heredoc、內嵌腳本；PTC 能用 Python 迴圈、串接、平行，但只能呼叫目錄內的函式
  source_quotes:
  - "先定義批次化。 一次模型呼叫（一個回合）完成多個對環境的動作，減少模型與工具之間的往返次數，也減少中間結果進入上下文"
  - "Tool-only | 不能，每個動作是一次獨立呼叫"
  - "Bash | 能：pipe、&&、迴圈、heredoc（在指令裡直接嵌入多行文字）、內嵌腳本"
  - "PTC | 能：Python 迴圈、串接、平行，但只能呼叫目錄內的函式"
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c6
  role: evidence
  text: Tool-only 換成 PTC，兩個 benchmark 乘兩個模型的四格 token 都下降（例如 TheAgentCompany／Opus-4.8 從 945k 降到 406k），但分數只有第一格明顯進步（44.9% → 52.9%），其餘持平或略降
  source_quotes:
  - "Tool-only 換成 PTC（箭頭左為 Tool-only，右為 PTC）："
  - "TheAgentCompany／Opus-4.8 | 44.9% → 52.9% | 945k → 406k | 1.20 → 0.64"
  - "Benchmark／模型 | Score | Total tokens | 每題成本（美元）"
  - "四格 token 都下降，但分數只有第一格明顯進步，其餘持平或略降。"
  anchor_type: 實驗結果
  comparison_target: Tool-only（箭頭左邊），同 benchmark、同模型
  qualifiers:
  - text: PTC 的受限 Python 執行環境是論文作者自己實作
    source_quote: "PTC 的受限 Python 執行環境也是論文作者自己實作"
  figures:
  - file: figures/is-bash-all-you-need/table1.png
    article: is-bash-all-you-need
    src: table1.png
    caption: 表 1 — 五種介面的完整結果。分數與通過率附 95% bootstrap 信賴區間，token 欄位為每題平均（單位千），輸入含快取讀取，總量為輸入加輸出（來源：原始論文 Table 1。）
    sha256: c605527b425db60929e3b54c13d413a82d084b88ef71d14478b43b9999d7bbc5
  importance: 2
  status: normal
- id: c7
  role: evidence
  text: 配對分數差（同一題、同一模型、兩種介面的分數相減再平均，pp 是百分點）：PTC − Tool-only 在 TheAgentCompany 是 +3.5 pp [+0.8, +6.2]，APEX-Agents 是 −1.5 pp [−3.9, +0.9]
  source_quotes:
  - "同一題、同一模型、兩種介面的分數相減，再對所有題取平均"
  - "pp 是百分點"
  - "PTC − Tool-only：TheAgentCompany 是 +3.5 pp [+0.8, +6.2]，APEX-Agents 是 −1.5 pp [−3.9, +0.9]。"
  anchor_type: 實驗結果
  comparison_target: Tool-only，同一題、同一模型的配對
  qualifiers:
  - text: PTC 的受限 Python 執行環境是論文作者自己實作
    source_quote: "PTC 的受限 Python 執行環境也是論文作者自己實作"
  figures:
  - file: figures/is-bash-all-you-need/table9.png
    article: is-bash-all-you-need
    src: table9.png
    caption: 表 9 — 各介面兩兩比較的配對分數差，正數代表前者較好，括號內為 95% bootstrap 信賴區間（來源：原始論文 Table 9。）
    sha256: 10f313801a2a3f6747b24d6f147dc27bc494d796f507cab2cb5214f133ce88e2
  importance: 3
  status: normal
- id: c8
  role: anchor
  text: Bash − PTC 的配對分數差是 +21.2 pp [+17.0, +25.5]（TheAgentCompany）與 +7.7 pp [+5.2, +10.2]（APEX-Agents），區間都不含 0，Bash 明顯較好
  source_quotes:
  - "Bash − PTC：+21.2 pp [+17.0, +25.5] 與 +7.7 pp [+5.2, +10.2]，區間都不含 0，Bash 明顯較好。"
  - "PTC − Tool-only：TheAgentCompany 是 +3.5 pp [+0.8, +6.2]，APEX-Agents 是 −1.5 pp [−3.9, +0.9]。"
  anchor_type: 實驗結果
  comparison_target: PTC，同一題、同一模型的配對
  qualifiers:
  - text: PTC 的受限 Python 執行環境是論文作者自己實作
    source_quote: "PTC 的受限 Python 執行環境也是論文作者自己實作"
  - text: PTC 輸給 Bash 的 +21.2 pp 與 +7.7 pp，有一部分可能只是目錄覆蓋不夠，這個混淆主要在目錄自製的 TheAgentCompany；論文沒有把「做法」與「目錄覆蓋」拆開
    source_quote: "反過來，PTC 輸給 Bash 的那 +21.2 pp 與 +7.7 pp，有一部分可能只是目錄覆蓋不夠（Appendix B.1），而這個混淆主要在目錄自製的 TheAgentCompany。論文沒有把「做法」與「目錄覆蓋」拆開。"
  figures:
  - file: figures/is-bash-all-you-need/table9.png
    article: is-bash-all-you-need
    src: table9.png
    caption: 表 9 — 各介面兩兩比較的配對分數差，正數代表前者較好，括號內為 95% bootstrap 信賴區間（來源：原始論文 Table 9。）
    sha256: 10f313801a2a3f6747b24d6f147dc27bc494d796f507cab2cb5214f133ce88e2
  importance: 2
  status: normal
- id: c9
  role: evidence
  text: 每題總 token 上，PTC 只在 TheAgentCompany／GPT-5.5 比 Bash 省（242k 對 377k）
  source_quotes:
  - "token：PTC 只在 TheAgentCompany／GPT-5.5 比 Bash 省（242k 對 377k）。"
  anchor_type: 實驗結果
  comparison_target: Bash，同 benchmark、同模型
  importance: 4
  status: normal
- id: c10
  role: evidence
  text: 相對 Tool-only，PTC 平均每次執行只包 2.0 個呼叫，批次化程度不高，但輸入與快取讀取 token 少了很多，輸出幾乎不變；例如 TheAgentCompany 上未快取輸入少 97.6k、快取讀取少 86.8k、輸出 +0.2k
  source_quotes:
  - "TheAgentCompany | 2.0 | −4.0 | −97.6k | −86.8k | +0.2k"
  - "Benchmark | 每次執行包的呼叫數 | 呼叫次數差 | 未快取輸入 token 差 | 快取讀取 token 差 | 輸出 token 差"
  - "批次化程度不高（平均每次執行只包 2 個呼叫），但輸入與快取讀取 token 少了很多，輸出幾乎不變。"
  - "表 6 拆解了 PTC 的批次化程度與 token 變化（相對 Tool-only 的差"
  - "表 6 — PTC 的批次化程度與 token 效率（相對 Tool-only 的差，依任務與模型配對）"
  anchor_type: 實驗結果
  comparison_target: Tool-only，依任務與模型配對
  importance: 3
  status: normal
- id: c11
  role: mechanism
  text: 論文作者推測（沒有驗證），PTC 省 token 是因為中間結果留在程式裡、只把選出的輸出交回模型，後續每輪要帶的上下文就變短；原文措辭是「可能」
  source_quotes:
  - "論文作者推測（沒有驗證），這是因為中間結果留在程式裡、只把選出的輸出交回模型，後續每輪要帶的上下文就變短"
  - "論文把 PTC 省 token 歸因於這個機制，但措辭是「可能」"
  anchor_type: 原作者解讀
  importance: 3
  status: normal
- id: c12
  role: evidence
  text: PTC 的工具呼叫成功率最低：TheAgentCompany 只有 65.2%，其他介面約 92%；APEX-Agents 是 86.2%，其他約 88% 到 91%
  source_quotes:
  - "PTC 的工具呼叫成功率最低（表 2）：TheAgentCompany 只有 65.2%，其他介面約 92%；APEX-Agents 是 86.2%，其他約 88% 到 91%。"
  anchor_type: 實驗結果
  comparison_target: 其他四種介面
  qualifiers:
  - text: 論文作者猜測原因是「在程式裡協調呼叫、處理中間失敗比較難」，沒有進一步驗證
    source_quote: "論文作者猜測是「在程式裡協調呼叫、處理中間失敗比較難」，沒有進一步驗證。"
  importance: 4
  status: normal
- id: c13
  role: evaluation
  text: PTC 輸給 Bash，有一部分可能是目錄覆蓋不夠：PTC 只能呼叫固定工具目錄裡的函式，而 TheAgentCompany 的自製目錄只涵蓋任務相關 API，所以 Bash − PTC 的差距混著「PTC 的做法」與「目錄能碰到的範圍」，論文沒有拆開
  source_quotes:
  - "PTC 只能呼叫固定工具目錄裡的函式，而 TheAgentCompany 的自製目錄只涵蓋任務相關 API（Appendix B.1）。所以 Bash − PTC 的差距，混著「PTC 的做法」與「目錄能碰到的範圍」，論文沒有拆開。"
  - "PTC 輸給 Bash 的那 +21.2 pp 與 +7.7 pp，有一部分可能只是目錄覆蓋不夠"
  anchor_type: 部落格推論
  qualifiers:
  - text: PTC 的受限 Python 執行環境也是論文作者自己實作
    source_quote: "PTC 的受限 Python 執行環境也是論文作者自己實作"
  importance: 2
  status: normal
- id: c14
  role: evaluation
  text: 能碰到的範圍：PTC 只有固定工具目錄裡的函式，安全控管靠固定的工具目錄（沒有 shell）；Bash 能碰到檔案系統、任意指令、網路，任何 shell 能碰到的東西，安全控管靠隔離環境、檔案系統限制、執行上限
  source_quotes:
  - "能碰到什麼 | 只有固定工具目錄裡的函式 | 檔案系統、任意指令、網路，任何 shell 能碰到的東西"
  - "安全控管靠什麼 | 固定的工具目錄（沒有 shell） | 隔離環境、檔案系統限制、執行上限"
  - "|  | PTC | Bash |"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c15
  role: evaluation
  text: 就算任務改成大量重複呼叫，優勢會同時屬於 Bash 與 PTC，PTC 沒有 Bash 做不到的批次能力，兩者之間不會因此翻盤（blog 的推論）
  source_quotes:
  - "所以就算任務改成大量重複呼叫，優勢會同時屬於 Bash 與 PTC，PTC 沒有 Bash 做不到的批次能力，兩者之間不會因此翻盤（我的推論）。"
  anchor_type: 部落格推論
  importance: 3
  status: normal
- id: c16
  role: evaluation
  text: 「這兩個 benchmark 的任務型態是不是不適合 PTC」有可能，但論文沒有直接驗證：Tool-only 每題呼叫次數的中位數只有 14.0（TheAgentCompany）與 13.0（APEX-Agents），PTC 平均每次執行只包 2.0 個呼叫，不是大量迴圈的工作型態；論文也沒有按呼叫次數拆 token 節省量
  source_quotes:
  - "有可能，但論文沒有直接驗證。"
  - "Tool-only 每題呼叫次數的中位數只有 14.0（TheAgentCompany）與 13.0（APEX-Agents），PTC 平均每次執行只包 2.0 個呼叫，不是大量迴圈的工作型態。"
  - "它沒有按呼叫次數拆 token 節省量，只拆了分數。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 計數
  qualifiers:
  - text: 部分呼應這個假設的證據：APEX-Agents 上呼叫次數高的區間，PTC 的平均分數差變成正的；但論文作者自己也說，PTC 的信賴區間在大多數區間都跨過 0，證據很弱
    source_quote: "部分呼應：在任務複雜度圖（圖 4）裡，APEX-Agents 上呼叫次數高的區間，PTC 的平均分數差變成正的。但論文作者自己也說，PTC 的信賴區間在大多數區間都跨過 0，證據很弱。"
  importance: 4
  status: normal
- id: c17
  role: evaluation
  text: 論文的實務建議是條件式的：能把任意程式碼執行隔離起來，就用 Bash；合規要求只能用固定工具目錄，就用 PTC
  source_quotes:
  - "論文的實務建議是條件式的：能把任意程式碼執行隔離起來，就用 Bash；合規要求只能用固定工具目錄，就用 PTC。"
  anchor_type: 原作者解讀
  importance: 2
  status: normal
- id: c18
  role: evaluation
  text: blog 把論文的建議整理成判斷順序：先問合規要求是否只能呼叫核准的固定工具，是就用 PTC；否則再問能不能把任意程式碼執行隔離起來，能就用 Bash
  source_quotes:
  - "論文的建議是條件式的，整理成判斷順序，是先問合規，再問能不能隔離："
  - "1 | 合規要求只能呼叫核准的固定工具嗎？ | 用 PTC | 往下問"
  - "2 | 能把任意程式碼執行隔離起來嗎？ | 用 Bash"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 不能隔離的情形論文沒有直接講，退回 Tool-only 是 blog 的推論
    source_quote: "論文沒有直接講這種情形，退回 Tool-only 是我的推論"
  importance: 2
  status: normal
```
