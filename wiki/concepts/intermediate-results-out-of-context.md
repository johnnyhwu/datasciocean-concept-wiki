---
id: intermediate-results-out-of-context
title: 進了上下文的每個 token，之後每一輪都要再付一次錢；讓大量的中間資料留在模型之外，是最直接的省法
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: is-bash-all-you-need
  article_title: "Is Bash All You Need？只給 agent 一個 shell，比整套專用工具更準又更省"
  url: https://datasciocean.com/paper-intro/is-bash-all-you-need/
  sections:
  - 只給 agent 一個 shell，分數反而更高
  - 五種工具介面
  - 同一件事，三種介面各怎麼做
  - PTC：省了 token，分數沒跟上
  - 該怎麼選：先問合規，再問能不能隔離
  - 延伸：為什麼中間結果不進上下文就能省 token
  - 延伸：typed tools 加 exec 的混合架構，論文沒測到什麼
  first_appearance: true
parent: null
related:
  - bash-vs-typed-tools-results
  - bash-add-ons-no-detectable-gain
  - ptc-batching-vs-reach
  - baseline-who-built-it
  - context-chunk-keep-offload-compress-delete
  - context-edit-cost-by-position
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 模型每一輪都要把前面的全部內容重新讀一遍，所以進了上下文的每個 token，之後每一輪都要再付一次錢；讓大量的中間資料留在模型之外，是最直接的省法
  source_quotes:
  - "模型每一輪都要把前面的全部內容重新讀一遍，所以進了上下文的每個 token，之後每一輪都要再付一次錢；讓大量的中間資料留在模型之外，是最直接的省法。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 這個機制屬一般知識，不是論文內容，論文只提供 PTC 的 token 拆解表作為旁證
    source_quote: "本節的機制屬一般知識，不是論文內容，論文只提供表 6 的旁證。"
  - text: 實際系統通常有快取，前綴相同的部分以較低單價重讀；它降低單價，但沒有減少 token 數，論文結果表的輸入 token 也包含快取讀取；所以有快取時這個價值仍成立，只是金額差距變小
    source_quote: "實際系統通常有快取（prompt caching）：前綴相同的部分以較低單價重讀。它降低單價，但沒有減少 token 數；論文結果表（表 1）的輸入 token 也包含快取讀取。所以「別讓大量資料進上下文」的價值在有快取時仍成立，只是金額差距變小。"
  - text: 結果小或之後每輪都要參考原文時，就直接放進上下文
    source_quote: "結果小或之後每輪都要參考原文，就直接放進上下文。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: 上下文（context）是模型每次被呼叫時讀入的全部文字，包含 system prompt、任務描述、過去每一輪的動作，以及每個工具回傳的結果；無狀態是指模型本身沒有跨呼叫的記憶，每一輪系統都要把整份上下文重新送給模型，模型才「記得」之前發生了什麼
  source_quotes:
  - "上下文（context）：模型每次被呼叫時讀入的全部文字，包含 system prompt、任務描述、過去每一輪的動作，以及每個工具回傳的結果。"
  - "無狀態：模型本身沒有跨呼叫的記憶。每一輪，系統都要把整份上下文重新送給模型，模型才「記得」之前發生了什麼。"
  anchor_type: 背景說明
  importance: 2
  status: normal
- id: c3
  role: context
  text: "論文〈Is Bash All You Need? An Empirical Study of Tool Interfaces for Enterprise Digital Worker Agents〉（Microsoft、CMU）比較企業 agent 的工具介面，包括 Tool-only（只有 typed tools，也就是預先定義好名稱與參數格式的函式，每個動作一次獨立呼叫）、Bash（只有 shell，可以用 pipe、迴圈把多個動作串成一次呼叫），以及 PTC（Programmatic Tool Calling，模型寫一小段程式，程式只能呼叫預先定義的工具）"
  source_quotes:
  - "Is Bash All You Need? An Empirical Study of Tool Interfaces for Enterprise Digital Worker Agents（Microsoft、CMU"
  - "一端是 typed tool：預先定義好名稱與參數格式的函式"
  - "Tool-only | 只有 typed tools | 每個動作一次獨立呼叫，是基準線"
  - "Bash | 只有 shell | 可以用 pipe（"
  - "迴圈把多個動作串成一次呼叫"
  - "PTC（Programmatic Tool Calling，程式化工具呼叫：模型寫一小段程式，程式只能呼叫預先定義的工具）"
  - "論文比的是工具介面（tool interface）"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c4
  role: anchor
  text: 自編例子：找出某個 GitLab 專案裡標題含「bug」的 open issue 標題，假設專案有 500 個 open issue、其中 20 個符合。Tool-only 呼叫 gitlab_list_issues，500 筆 issue 的完整內容全部回到模型的上下文；Bash 用 curl 加 jq 加 grep 的 pipe，只有 20 行標題回到上下文；PTC 送出一段 Python，500 筆留在程式裡，只有 20 個標題回到模型
  source_quotes:
  - "用一個自編例子看三種介面的差別。任務：找出某個 GitLab 專案裡，標題含「bug」的 open issue 標題。假設專案有 500 個 open issue，其中 20 個符合。"
  - "-> 500 筆 issue 的完整內容全部回到模型的上下文"
  - "-> 只有 20 行標題回到上下文"
  - "# 500 筆，留在程式裡"
  - "# 只有 20 個標題回到模型"
  - "curl -s $GITLAB/api/.../issues?state=opened | jq -r '.[].title' | grep -i bug"
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 假設題設
  importance: 2
  status: normal
- id: c5
  role: mechanism
  text: 一筆工具結果在第 s 輪進來，之後到最後一輪都要再讀一次，所以它的成本是「大小乘以剩餘輪數」；總輸入 token 是每一輪讀入的上下文長度加總，每一輪的長度是起始上下文，加上之前每一輪模型的輸出與工具結果，所以省工具結果的 token，效果會被輪數放大
  source_quotes:
  - "所以它的成本是「大小乘以剩餘輪數」。寫成式子，總輸入 token 就是每一輪讀入的上下文長度加總，而每一輪的長度是起始上下文，加上之前每一輪模型的輸出與工具結果："
  - '\text{總輸入 token} = \sum_{t=1}^{T} L_t, \qquad L_t = L_0 + \sum_{s<t} (a_s + r_s)'
  - '所以省 \( r_s \) 的效果，會被輪數放大。'
  - '\( r_s \)：第 \( s \) 輪工具結果進入上下文的 token 數。'
  - '一筆工具結果在第 \( s \) 輪進來，之後第 \( s+1 \) 到第 \( T \) 輪都要再讀一次'
  anchor_type: 數學推導
  importance: 2
  status: normal
- id: c6
  role: anchor
  text: 逐步試算（自編例子，數字都是假設，不是論文的實驗結果）：沿用 GitLab 任務，假設每筆完整 issue 約 200 token、每個標題約 20 token、起始上下文 5,000 token、取得結果之後還要 9 輪；Tool-only 首輪後進入上下文的結果是 100,000 token，之後 9 輪合計約 945,000；Bash 或 PTC 只有 400 token 進上下文，之後 9 輪合計約 48,600；差約 19 倍
  source_quotes:
  - "逐步試算（自編例子）。 沿用前面的 GitLab 任務：500 筆 issue、其中 20 筆符合條件。假設每筆完整 issue 約 200 token，每個標題約 20 token，起始上下文 5,000 token，取得結果之後還要 9 輪才完成任務"
  - "Tool-only（500 筆完整結果進上下文） | 500 × 200 = 100,000 token | 約 105,000 | 約 945,000"
  - "Bash 或 PTC（只有 20 個標題進上下文） | 20 × 20 = 400 token | 約 5,400 | 約 48,600"
  - "差約 19 倍（這裡的數字都是假設，不是論文的實驗結果）。"
  anchor_type: 部落格舉例
  comparison_target: 同一任務下，只讓 20 個標題進上下文的 Bash 或 PTC 對比讓 500 筆完整結果進上下文的 Tool-only
  qualifiers:
  - text: 試算假設兩種做法模型自己的輸出相同，所以忽略模型輸出的 token
    source_quote: '兩種做法模型自己的輸出相同，所以忽略 \( a_s \)。'
  - text: 首輪的 5,000 兩種做法相同，比較的是之後 9 輪
    source_quote: "首輪的 5,000 兩種做法相同，比較的是之後 9 輪"
  importance: 2
  status: normal
- id: c7
  role: evidence
  text: 論文的旁證是 PTC 的 token 拆解：相對 Tool-only，未快取輸入與快取讀取都大幅減少，輸出幾乎不變，而平均每次執行只包 2.0 個呼叫，所以省下的主要不是「呼叫次數」
  source_quotes:
  - "旁證是 PTC 那一節的表 6：相對 Tool-only，未快取輸入與快取讀取都大幅減少，輸出幾乎不變，而平均每次執行只包 2.0 個呼叫，所以省下的主要不是「呼叫次數」。"
  - "表 6 — PTC 的批次化程度與 token 效率（相對 Tool-only 的差，依任務與模型配對）"
  anchor_type: 部落格考證
  comparison_target: Tool-only，依任務與模型配對
  importance: 3
  status: normal
- id: c8
  role: evidence
  text: PTC 的 token 拆解數字：TheAgentCompany 上相對 Tool-only，每次執行包 2.0 個呼叫，未快取輸入少 97.6k、快取讀取少 86.8k、輸出 +0.2k；APEX-Agents 上是 2.0 個呼叫，未快取輸入少 45.4k、快取讀取少 44.0k、輸出 −0.4k
  source_quotes:
  - "TheAgentCompany | 2.0 | −4.0 | −97.6k | −86.8k | +0.2k"
  - "APEX-Agents | 2.0 | −3.0 | −45.4k | −44.0k | −0.4k"
  - "Benchmark | 每次執行包的呼叫數 | 呼叫次數差 | 未快取輸入 token 差 | 快取讀取 token 差 | 輸出 token 差"
  - "表 6 拆解了 PTC 的批次化程度與 token 變化（相對 Tool-only 的差"
  - "表 6 — PTC 的批次化程度與 token 效率（相對 Tool-only 的差，依任務與模型配對）"
  anchor_type: 實驗結果
  comparison_target: Tool-only，依任務與模型配對
  importance: 3
  status: normal
- id: c9
  role: qualifier
  text: 論文作者的解釋是：中間結果在程式裡處理，只回傳選出的輸出，後續各輪攜帶的上下文因此縮短；原文措辭是「可能」，沒有做直接驗證
  source_quotes:
  - "論文作者的解釋是：中間結果在程式裡處理，只回傳選出的輸出，後續各輪攜帶的上下文因此縮短。原文措辭是「可能」（"
  - "），沒有做直接驗證。"
  anchor_type: 原作者解讀
  importance: 3
  status: normal
- id: c10
  role: evaluation
  text: 降低進入上下文的 token 的做法（一般知識）：工具端先整理輸出（在 typed tool 內篩選、挑欄位、截斷、分頁再回傳，適合你能控制工具的實作時，代價是每個工具都要設計，整理不當會丟掉需要的資訊）；讓 agent 寫程式處理（Bash 的 pipe 或 PTC 的 Python，中間結果留在程式裡，適合資料量大、處理步驟固定時，代價是需要執行環境與安全控管）
  source_quotes:
  - "降低進入上下文的 token 的其他做法（一般知識）："
  - "工具端先整理輸出 | 在 typed tool 內做篩選、挑欄位、截斷、分頁再回傳 | 你能控制工具的實作 | 每個工具都要設計，整理不當會丟掉需要的資訊"
  - "讓 agent 寫程式處理 | Bash 的 pipe 或 PTC 的 Python，中間結果留在程式裡 | 資料量大、處理步驟固定 | 需要執行環境與安全控管"
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c11
  role: evaluation
  text: 其他做法（一般知識）：上下文壓縮（對話太長時用摘要取代舊內容，適合長時間任務，摘要可能遺失細節）；子 agent（把大量閱讀交給另一個獨立上下文，只回傳結論，適合需要大量搜尋或閱讀時，有額外的協調成本）；快取（重複讀取的前綴用較低單價，適合前綴穩定的長對話，只降單價、不減 token 數）
  source_quotes:
  - "降低進入上下文的 token 的其他做法（一般知識）："
  - "上下文壓縮 | 對話太長時，用摘要取代舊內容 | 長時間任務 | 摘要可能遺失細節"
  - "子 agent | 把大量閱讀交給另一個獨立上下文，只回傳結論 | 需要大量搜尋或閱讀 | 額外的協調成本"
  - "快取 | 重複讀取的前綴用較低單價 | 前綴穩定的長對話 | 只降單價，不減 token 數"
  anchor_type: 背景說明
  importance: 4
  status: normal
- id: c12
  role: evaluation
  text: 判斷規則：先問「這筆結果大不大、之後會不會再用到原文」；大，而且之後只需要其中一小部分，就別讓它整份進上下文，從工具端整理輸出、讓 agent 寫程式處理、上下文壓縮三種擇一；結果小或之後每輪都要參考原文，就直接放進上下文
  source_quotes:
  - "判斷規則：先問「這筆結果大不大、之後會不會再用到原文」。大，而且之後只需要其中一小部分，就別讓它整份進上下文，用上表的前三種擇一；結果小或之後每輪都要參考原文，就直接放進上下文。"
  - "工具端先整理輸出 | 在 typed tool 內做篩選"
  - "讓 agent 寫程式處理 | Bash 的 pipe 或 PTC 的 Python"
  - "上下文壓縮 | 對話太長時，用摘要取代舊內容"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c13
  role: evaluation
  text: 一個輸出設計良好的 typed tool，可以拿到 PTC 與 Bash 靠別的方式拿到的 token 節省，並且多一個可預期的輸入格式（blog 的推論）
  source_quotes:
  - "我的推論是：一個輸出設計良好的 typed tool，可以拿到 PTC 與 Bash 靠別的方式拿到的 token 節省，並且多一個可預期的輸入格式。"
  anchor_type: 部落格推論
  importance: 4
  status: normal
- id: c14
  role: context
  text: 這是 blog 讀這篇論文的過程裡整理出來的幾個判斷方法之一，blog 說這些判斷方法脫離這篇論文也成立
  source_quotes:
  - "比較耐用的是讀它的過程裡整理出來的幾個判斷方法"
  - "下面這些判斷方法脫離這篇論文也成立"
  - "省 token 的關鍵是別讓大量中間資料進上下文：進了上下文的每個 token，之後每一輪都要再付一次。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
```
