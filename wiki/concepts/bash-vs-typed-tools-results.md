---
id: bash-vs-typed-tools-results
title: 只給 agent 一個 bash shell，在兩個企業工作 benchmark 上比只給 typed tools 分數更高、token 更少；方向可信，幅度不能直接搬
type_hint: 發現
context_type: bound_to_source
sources:
- article: is-bash-all-you-need
  article_title: "Is Bash All You Need？只給 agent 一個 shell，比整套專用工具更準又更省"
  url: https://datasciocean.com/paper-intro/is-bash-all-you-need/
  sections:
  - 只給 agent 一個 shell，分數反而更高
  - 怎麼比才公平：同一個模型、同一份任務，只換 agent 的雙手
  - 五種工具介面
  - 兩個企業工作 benchmark，typed tools 來源不同
  - agent 會鑽評分漏洞：Bash 的高分是在額外防護下測的
  - 怎麼算分：分數、通過率、token 與配對差
  - Bash 對 Tool-only：四組設定全部同向
  - Bash 為什麼比較好：agent 拿 shell 寫小程式
  - 這份證據能信幾分
  - 該怎麼選：先問合規，再問能不能隔離
  first_appearance: true
parent: null
related:
  - bash-add-ons-no-detectable-gain
  - ptc-batching-vs-reach
  - baseline-who-built-it
  - intermediate-results-out-of-context
  - claude-code-agentic-loop-and-tools
  - clm-context-as-editable-file
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 只給 agent 一個 bash shell，比只給 typed tools，在兩個企業工作 benchmark 上分數反而更高，而且用更少 token；方向可信，幅度不能直接搬
  source_quotes:
  - "只給 agent 一個 bash shell，在兩個企業工作 benchmark 上分數反而更高，而且用更少 token"
  - "Bash 對比只有 typed tools，分數在"
  - "方向可信，幅度不能直接搬"
  anchor_type: 部落格判斷
  qualifiers:
  - text: TheAgentCompany 的 60 個 typed tools 是論文作者自己設計的，所以 Bash 的優勢混著「這組工具做得好不好」
    source_quote: "TheAgentCompany 的 60 個 typed tools 是論文作者自己設計的，所以 Bash 的優勢混著「這組工具做得好不好」。"
  - text: Bash 的高分是在額外防護（封鎖評分腳本、加密同事資料）之下測出來的
    source_quote: "Bash 的高分也是在額外防護（封鎖評分腳本、加密同事資料）之下測出來的。"
  - text: 幅度（尤其 TheAgentCompany 的 +24.6 pp）不能直接搬到別的系統
    source_quote: "但幅度（尤其 TheAgentCompany 的 +24.6 pp）不能直接搬到別的系統。"
  - text: 這篇沒有量測 typed tool 的輸出整理、權限控管、稽核，這些好處不在分數裡，不能視為被否定
    source_quote: "第一，這篇沒有量測 typed tool 的輸出整理、權限控管、稽核，這些好處不在分數裡，不能視為被否定。"
  - text: 各領域上，每個領域都是 Bash ≥ Bash+Tool ≥ Tool-only，但軟體工程差距最大，公司法務幾乎不受介面影響
    source_quote: "每個領域都是 Bash ≥ Bash+Tool ≥ Tool-only，軟體工程差距最大，公司法務幾乎不受介面影響。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: "論文〈Is Bash All You Need? An Empirical Study of Tool Interfaces for Enterprise Digital Worker Agents〉（Microsoft、CMU）比的是企業 agent 的工具介面（tool interface），也就是 agent 用什麼方式對環境下動作：一端是 typed tool，預先定義好名稱與參數格式的函式，例如 gitlab_create_issue，模型一次呼叫一個；另一端是直接給一個 bash shell（命令列），讓模型自己寫指令。論文沒有提出新方法，價值在於把五種介面放進同一個受控設定裡比較"
  source_quotes:
  - "Is Bash All You Need? An Empirical Study of Tool Interfaces for Enterprise Digital Worker Agents（Microsoft、CMU"
  - "論文沒有提出新方法，價值在於把五種介面放進同一個受控設定裡比較。"
  - "論文比的是工具介面（tool interface），也就是 agent 用什麼方式對環境下動作。一端是 typed tool：預先定義好名稱與參數格式的函式，例如 gitlab_create_issue，模型一次呼叫一個；另一端是直接給一個 bash shell（命令列），讓模型自己寫指令。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: 論文作者用同一個模型、同一份任務文字、同一份基礎 prompt、同一套停止條件，只改變「agent 能怎麼動手」，藉此隔離出介面本身的影響；測試的模型是 Opus-4.8 與 GPT-5.5，用預設的推理強度
  source_quotes:
  - "論文作者用同一個模型、同一份任務文字、同一份基礎 prompt、同一套停止條件，只改變「agent 能怎麼動手」，藉此隔離出介面本身的影響。測試的模型是 Opus-4.8 與 GPT-5.5，推論設定用預設的推理強度。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  qualifiers:
  - text: 只有 Bash+Synthesis 與 PTC 額外加了介面專屬的 prompt 指示，其餘介面共用同一份基礎 prompt
    source_quote: "只有 Bash+Synthesis 與 PTC 額外加了介面專屬的 prompt 指示，其餘介面共用同一份基礎 prompt。"
  importance: 3
  status: normal
- id: c4
  role: context
  text: 五種介面是：Tool-only（只有 typed tools，每個動作一次獨立呼叫，是基準線）、Bash（只有 shell，可以用 pipe、迴圈把多個動作串成一次呼叫）、Bash+Tool（shell 加 typed tools，agent 自己選）、Bash+Synthesis（shell 加一個持久資料夾，prompt 鼓勵 agent 把常用步驟寫成可重用腳本）、PTC（Programmatic Tool Calling，模型寫 Python，程式裡只能呼叫 typed tools）
  source_quotes:
  - "Tool-only | 只有 typed tools | 每個動作一次獨立呼叫，是基準線"
  - "Bash | 只有 shell | 可以用 pipe（"
  - "迴圈把多個動作串成一次呼叫"
  - "Bash+Tool | shell 加 typed tools | 兩者並存，agent 自己選"
  - "Bash+Synthesis | shell 加一個持久資料夾 | prompt 鼓勵 agent 把常用步驟寫成可重用腳本"
  - "PTC | 模型寫 Python，程式裡只能呼叫 typed tools"
  - "PTC（Programmatic Tool Calling，程式化工具呼叫"
  anchor_type: 設計參數
  figures:
  - file: figures/is-bash-all-you-need/figure1.png
    article: is-bash-all-you-need
    src: figure1.png
    caption: 圖 1 — 五種工具介面的結構（來源：原始論文 Figure 1。）
    sha256: 364822fc1d324deef9b6cc5e1c2fbfcc19b46b9d71c13cdb28f4b847d8f42939
  importance: 3
  status: normal
- id: c5
  role: context
  text: 兩個 benchmark：TheAgentCompany 模擬軟體公司，174 題，benchmark 沒有現成的 typed tools，論文作者自己設計 60 個；APEX-Agents 模擬投資銀行、管理顧問、公司法務的專業分析，480 題，用 benchmark 原有的 20 個 typed tools
  source_quotes:
  - "TheAgentCompany（模擬軟體公司的 benchmark）"
  - "任務數 | 174 題"
  - "480 題，三個領域各 160 題"
  - "benchmark 沒有現成的，論文作者自己設計 60 個"
  - "benchmark 原有的 20 個"
  - "APEX-Agents（模擬投資銀行、顧問、法務專業分析的 benchmark）"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 3
  status: normal
- id: c6
  role: anchor
  text: Bash 對比只有 typed tools（Tool-only），分數在 TheAgentCompany 高 21.8 到 24.5 個百分點，在 APEX-Agents 高 4.8 到 7.4 個百分點，每題總 token 少 19% 到 72%；這些範圍是從論文的完整結果表逐格相減得到的
  source_quotes:
  - "Bash 對比只有 typed tools，分數在 TheAgentCompany（模擬軟體公司的 benchmark）高 21.8 到 24.5 個百分點（pp），在 APEX-Agents（模擬投資銀行、顧問、法務專業分析的 benchmark）高 4.8 到 7.4 pp，每題總 token 少 19% 到 72%。"
  - "這些範圍是從論文的完整結果表逐格相減得到的。"
  anchor_type: 實驗結果
  comparison_target: 只有 typed tools（Tool-only），同模型、同任務
  qualifiers:
  - text: TheAgentCompany 的 typed tools 是論文作者自己設計的，所以 Bash 的優勢混著「這組工具做得好不好」
    source_quote: "TheAgentCompany 的 60 個 typed tools 是論文作者自己設計的，所以 Bash 的優勢混著「這組工具做得好不好」。"
  - text: Bash 的高分是在額外防護（封鎖評分腳本、加密同事資料）之下測出來的
    source_quote: "Bash 的高分也是在額外防護（封鎖評分腳本、加密同事資料）之下測出來的。"
  importance: 2
  status: normal
- id: c7
  role: evidence
  text: Tool-only 換成 Bash 的四組結果（兩個 benchmark 乘兩個模型）全部同向：分數變高，token 和成本變低；例如 TheAgentCompany／Opus-4.8 的分數 44.9% → 69.4%、每題總 token 945k → 264k、每題成本 1.20 → 0.37 美元
  source_quotes:
  - "四組全部同向：分數變高，token 和成本變低。"
  - "下表箭頭左邊是 Tool-only，右邊是 Bash。"
  - "TheAgentCompany／Opus-4.8 | 44.9% → 69.4% | 24.1% → 50.6% | 945k → 264k | 1.20 → 0.37"
  - "Benchmark／模型 | Score | Pass rate | Total tokens | 每題成本（美元）"
  anchor_type: 實驗結果
  comparison_target: Tool-only（箭頭左邊），同 benchmark、同模型
  qualifiers:
  - text: TheAgentCompany 的 typed tools 是論文作者自己設計的，所以 Bash 的優勢混著「這組工具做得好不好」
    source_quote: "TheAgentCompany 的 60 個 typed tools 是論文作者自己設計的，所以 Bash 的優勢混著「這組工具做得好不好」。"
  - text: Bash 的高分是在額外防護（封鎖評分腳本、加密同事資料）之下測出來的
    source_quote: "Bash 的高分也是在額外防護（封鎖評分腳本、加密同事資料）之下測出來的。"
  - text: 這裡的絕對分數不能和公開排行榜比：APEX-Agents 官方排行榜用最大推理強度與較新的伺服器快照，這裡用預設推理強度與舊快照
    source_quote: "另一個細節：這裡的絕對分數不能和公開排行榜比。APEX-Agents 官方排行榜用最大推理強度與較新的伺服器快照，這裡用預設推理強度與舊快照（Appendix B.2）。"
  figures:
  - file: figures/is-bash-all-you-need/table1.png
    article: is-bash-all-you-need
    src: table1.png
    caption: 表 1 — 五種介面的完整結果。分數與通過率附 95% bootstrap 信賴區間，token 欄位為每題平均（單位千），輸入含快取讀取，總量為輸入加輸出（來源：原始論文 Table 1。）
    sha256: c605527b425db60929e3b54c13d413a82d084b88ef71d14478b43b9999d7bbc5
  importance: 3
  status: normal
- id: c8
  role: evidence
  text: 以配對任務算的平均分數差（同一題、同一模型、兩種介面的分數相減，再對所有題取平均），Bash − Tool-only 在 TheAgentCompany 是 +24.6 pp（95% 信賴區間 [+20.6, +29.0]），在 APEX-Agents 是 +6.2 pp（[+3.6, +8.7]）；兩個區間都不含 0，代表在這批資料裡，Bash 較好的方向相當穩定
  source_quotes:
  - "同一題、同一模型、兩種介面的分數相減，再對所有題取平均"
  - "TheAgentCompany（348 個任務-模型配對） | +24.6 pp | [+20.6, +29.0] | 161 / 172 / 15"
  - "APEX-Agents（960 個配對） | +6.2 pp | [+3.6, +8.7] | 220 / 596 / 144"
  - "Benchmark | Bash − Tool-only | 95% 信賴區間 | 勝／平／負（題數）"
  - "兩個區間都不含 0，代表在這批資料裡，Bash 較好的方向相當穩定。"
  anchor_type: 實驗結果
  comparison_target: Tool-only，同一題、同一模型的配對
  qualifiers:
  - text: TheAgentCompany 的 typed tools 是論文作者自己設計的，所以 Bash 的優勢混著「這組工具做得好不好」
    source_quote: "TheAgentCompany 的 60 個 typed tools 是論文作者自己設計的，所以 Bash 的優勢混著「這組工具做得好不好」。"
  - text: Bash 的高分是在額外防護（封鎖評分腳本、加密同事資料）之下測出來的
    source_quote: "Bash 的高分也是在額外防護（封鎖評分腳本、加密同事資料）之下測出來的。"
  - text: TheAgentCompany 的 +24.6 pp 比逐格相減的範圍（最高 24.5）略高一點，兩邊的算法不同，論文沒有說明這個小出入的來源
    source_quote: "TheAgentCompany 的 +24.6 pp 比上面逐格相減的範圍（最高 24.5）略高一點，兩邊的算法不同，論文沒有說明這個小出入的來源。"
  - text: APEX-Agents 有 144 個配對是 Bash 反而輸，整體只是 Bash 贏的題數多於輸的題數
    source_quote: "不過 APEX-Agents 有 144 個配對是 Bash 反而輸，整體只是 Bash 贏的題數多於輸的題數。"
  figures:
  - file: figures/is-bash-all-you-need/table9.png
    article: is-bash-all-you-need
    src: table9.png
    caption: 表 9 — 各介面兩兩比較的配對分數差，正數代表前者較好，括號內為 95% bootstrap 信賴區間（來源：原始論文 Table 9。）
    sha256: 10f313801a2a3f6747b24d6f147dc27bc494d796f507cab2cb5214f133ce88e2
  importance: 2
  status: normal
- id: c9
  role: evaluation
  text: 論文作者認為，彈性執行對寫程式與跨應用工作的幫助，可能大於對領域推理的幫助
  source_quotes:
  - "論文作者認為，彈性執行對寫程式與跨應用工作的幫助，可能大於對領域推理的幫助。"
  anchor_type: 原作者解讀
  importance: 5
  status: normal
- id: c10
  role: mechanism
  text: blog 歸納工具使用與 shell 用法兩組實驗，指向同一個方向：agent 拿到 shell 之後，不是一次跑一個指令，而是拿它寫小程式，把多個動作串成一次呼叫
  source_quotes:
  - "其中工具使用與 shell 用法兩組實驗指向同一個方向：agent 拿到 shell 之後，不是一次跑一個指令，而是拿它寫小程式，把多個動作串成一次呼叫。"
  anchor_type: 部落格推論
  importance: 2
  status: normal
- id: c11
  role: evidence
  text: 94% 以上的 shell 呼叫是組合式（含 pipe、迴圈、多行等）；TheAgentCompany 上，完全相同的重複呼叫在 Tool-only 占 16.2%，在 Bash 只有 0.3%
  source_quotes:
  - "94% 以上的 shell 呼叫是組合式（含 pipe、迴圈、多行等）；TheAgentCompany 上，完全相同的重複呼叫在 Tool-only 占 16.2%，在 Bash 只有 0.3%。"
  anchor_type: 實驗結果
  comparison_target: 組合式占比的分母是全部 shell 呼叫；重複呼叫比例是 Bash 對 Tool-only
  importance: 3
  status: normal
- id: c12
  role: evidence
  text: TheAgentCompany 上，呼叫內容的 token 是 Bash 9.0k 對 Tool-only 19.6k；APEX-Agents 上，呼叫次數中位數 Bash 7.5 對 Tool-only 13.0
  source_quotes:
  - "TheAgentCompany 上，呼叫內容的 token 是 Bash 9.0k 對 Tool-only 19.6k；APEX-Agents 上，呼叫次數中位數 Bash 7.5 對 Tool-only 13.0。"
  anchor_type: 實驗結果
  comparison_target: Tool-only
  qualifiers:
  - text: 論文作者對這組數字的解釋是 shell 能把重複動作合併成一次呼叫
    source_quote: "論文作者的解釋是：shell 能把重複動作合併成一次呼叫。"
  - text: 這裡的呼叫內容 token 是呼叫名稱、參數與結果的 token 中位數，不是計費用量，也不含上下文與快取效應
    source_quote: "「工具 token」是呼叫名稱、參數與結果的 token 中位數，不是計費用量，也不含上下文與快取效應"
    source: figure_caption
  figures:
  - file: figures/is-bash-all-you-need/table2.png
    article: is-bash-all-you-need
    src: table2.png
    caption: 表 2 — 各介面的工具使用統計。「工具 token」是呼叫名稱、參數與結果的 token 中位數，不是計費用量，也不含上下文與快取效應（來源：原始論文 Table 2。）
    sha256: 57bed97f940539e041a7e0f9e5ed9392a052e6bbd955ca1537501961178604db
  importance: 4
  status: normal
- id: c13
  role: evaluation
  text: 開發階段，有 shell 的 agent 會從 TheAgentCompany 公開 repo 裡的評分腳本直接撈答案，或讀取模擬同事的檔案，而不是真的去跟同事溝通；論文作者的對策是封鎖對該 repo 的網路存取、加密同事資訊，所以 Bash 的高分是在額外防護下測出的
  source_quotes:
  - "開發階段，有 shell 的 agent 會從 TheAgentCompany 公開 repo 裡的評分腳本直接撈答案，或讀取模擬同事的檔案，而不是真的去跟同事溝通。論文作者的對策是封鎖對該 repo 的網路存取、加密同事資訊。所以 Bash 的高分是在額外防護下測出的。"
  anchor_type: 原作者解讀
  importance: 3
  status: normal
- id: c14
  role: evaluation
  text: TheAgentCompany 的 Tool-only 用的是論文作者自製的那組工具，所以 +24.6 pp 混著「typed tools 的限制」與「這組工具做得好不好」，論文沒有拆開；APEX-Agents 的工具是 benchmark 原有的，+6.2 pp 相對乾淨，但不是完全乾淨（blog 的推論）
  source_quotes:
  - "TheAgentCompany 的 Tool-only 用的是論文作者自製的那組工具，所以 +24.6 pp 混著「typed tools 的限制」與「這組工具做得好不好」，論文沒有拆開。APEX-Agents 的工具是 benchmark 原有的，+6.2 pp 相對乾淨（我的推論）。"
  - "APEX-Agents 的 20 個工具是 benchmark 原有的，相對乾淨，但不是完全乾淨（我的推論）。"
  anchor_type: 部落格推論
  comparison_target: Tool-only，同一題、同一模型的配對
  importance: 2
  status: normal
- id: c15
  role: evaluation
  text: 「Bash 分數較高，而且更省」這個方向，在兩個模型乘兩個 benchmark 共四個設定裡一致，值得當作選型的參考；但幅度（尤其 TheAgentCompany 的 +24.6 pp）不能直接搬到別的系統，幅度以 APEX-Agents 的 +6.2 pp 較可信
  source_quotes:
  - "「Bash 分數較高，而且更省」這個方向，在兩個模型乘兩個 benchmark 共四個設定裡一致，值得當作選型的參考"
  - "但幅度（尤其 TheAgentCompany 的 +24.6 pp）不能直接搬到別的系統。"
  - "TheAgentCompany 的 +24.6 pp 混著自製基準線，幅度以 APEX-Agents 的 +6.2 pp 較可信。"
  anchor_type: 部落格判斷
  comparison_target: Tool-only，同一題、同一模型的配對
  qualifiers:
  - text: APEX-Agents 的 20 個工具是 benchmark 原有的，相對乾淨，但不是完全乾淨（blog 的推論）
    source_quote: "APEX-Agents 的 20 個工具是 benchmark 原有的，相對乾淨，但不是完全乾淨（我的推論）。"
  - text: 這篇沒有量測 typed tool 的輸出整理、權限控管、稽核，這些好處不在分數裡，不能視為被否定
    source_quote: "第一，這篇沒有量測 typed tool 的輸出整理、權限控管、稽核，這些好處不在分數裡，不能視為被否定。"
  importance: 2
  status: normal
- id: c16
  role: evaluation
  text: 論文的實務建議是條件式的：能把任意程式碼執行隔離起來，就用 Bash；合規要求只能用固定工具目錄，就用 PTC
  source_quotes:
  - "論文的實務建議是條件式的：能把任意程式碼執行隔離起來，就用 Bash；合規要求只能用固定工具目錄，就用 PTC。"
  anchor_type: 原作者解讀
  qualifiers:
  - text: Bash 的風險沒有被納入評分：論文建議能隔離任意執行時用 Bash，但隔離的成本與安全事件都沒有量化
    source_quote: "Bash 的風險沒有被納入評分。 論文建議「能隔離任意執行時用 Bash」，但隔離的成本與安全事件都沒有量化"
  - text: 這篇沒有量測 typed tool 的輸出整理、權限控管、稽核，這些好處不在分數裡，不能視為被否定
    source_quote: "第一，這篇沒有量測 typed tool 的輸出整理、權限控管、稽核，這些好處不在分數裡，不能視為被否定。"
  importance: 3
  status: normal
```
