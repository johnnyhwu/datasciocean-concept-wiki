---
id: context-chunk-keep-offload-compress-delete
title: 一塊 context 該留、存檔、壓成摘要、原地改還是刪，看它之後要不要原文、有多大、會不會一直小改；只有摘要的 harness 缺的是「存檔」和「原地編輯」
type_hint: 判斷
context_type: evidence_from_single_source
sources:
- article: context-language-models
  article_title: "Context Language Models 解析：讓 agent 用 Bash 改自己的 context"
  url: https://datasciocean.com/paper-intro/context-language-models/
  sections:
  - context 爆了，誰來決定留什麼？CLM 讓模型自己改
  - context 管理：從固定規則到模型自己動手
  - ContextBench：現有方法連簡單的管理任務都做不好
  - 一塊 context 該留、壓、存檔，還是刪
  - 模型估不準自己用了多少 context
  first_appearance: true
parent: null
related:
  - clm-context-as-editable-file
  - claude-code-extension-and-context
  - intermediate-results-out-of-context
  - skillstate-state-replaces-history
  - discard-history-relevance-at-the-time
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: context 滿了，要決定對哪一塊做什麼：之後要逐字用到而且不大的，留在 context；之後要逐字用到但很大的，存到檔案，context 只留指標，要用時再 grep；只需要大意的，壓成摘要；已經沒用的，直接刪；結構固定、常常只改一小處的，原地編輯
  source_quotes:
  - "context 滿了，面前有一堆內容，到底該對哪一塊做什麼？"
  - "之後要逐字用到，而且不大 | 留在 context"
  - "之後要逐字用到，但很大 | 存到檔案，context 只留指標，要用時再 grep"
  - "只需要大意 | 壓成摘要"
  - "已經沒用 | 直接刪"
  - "結構固定、常常只改一小處 | 原地編輯"
  anchor_type: 部落格推論
  qualifiers:
  - text: 依據是論文歸納的三個失敗原因；整理成決策表是 blog 的整合，推論，非論文原文
    source_quote: "依據是論文歸納的三個失敗原因（摘要會遺漏或編造、沒有原地編輯就得重寫整盤、只能存檔卻不能從 live context 踢掉）。整理成決策表是我的整合，推論，非論文原文。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: 這張表出自 blog 對 Context Language Models 論文的導讀。論文提出的 CLM 把模型當前的 context 鏡像成一個檔案，模型用 Bash 想改哪裡就改哪裡。表上用到的詞：compaction（壓縮）是把舊歷史改寫成較短的摘要；offloading（卸載）與 retrieval（檢索）是把內容存到外部檔案，context 裡只留一個指標，需要時再撈回來
  source_quotes:
  - "Context Language Models 這篇論文提出的做法叫 CLM：把模型當前的 context 鏡像成一個檔案，模型用 Bash 想改哪裡就改哪裡"
  - "compaction（壓縮）：把舊歷史改寫成較短的摘要。"
  - "offloading（卸載）與 retrieval（檢索）：把內容存到外部檔案，context 裡只留一個指標，需要時再撈回來。"
  anchor_type: 背景說明
  importance: 2
  status: normal
- id: c3
  role: mechanism
  text: 每一格的理由：之後要逐字用到而且不大的，任何改寫都可能失真；很大的，摘要有損，存檔無損；只需要大意的，省空間，失真可以接受；沒用的，留著只佔空間；結構固定常常小改的，重寫整份又貴又容易抄錯
  source_quotes:
  - "留在 context | 任何改寫都可能失真"
  - "存到檔案，context 只留指標，要用時再 grep | 摘要有損，存檔無損"
  - "壓成摘要 | 省空間，失真可以接受"
  - "直接刪 | 留著只佔空間"
  - "原地編輯 | 重寫整份又貴又容易抄錯"
  anchor_type: 部落格推論
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 判斷順序：先問「之後還要不要原文」，再問「多大」，最後問「會不會一直小改」
  source_quotes:
  - "判斷順序寫成虛擬碼如下：先問「之後還要不要原文」，再問「多大」，最後問「會不會一直小改」。"
  anchor_type: 部落格推論
  qualifiers:
  - text: 同一段的虛擬碼裡，「會不會一直小改」之後還有兩步：只需要大意就壓成摘要，其餘直接刪
    source_quote: "return EDIT_IN_PLACE                              # 例如棋盤、狀態表 if chunk.only_gist_needed: return SUMMARIZE return DELETE"
  - text: 這個判斷順序是 blog 整合論文三個失敗原因與 ContextBench 四個任務得出的，非論文原文
    source_quote: "推論：整合論文三個失敗原因與 ContextBench 四個任務得出的判斷順序（非論文原文）"
  importance: 4
  status: pending_author_confirmation
- id: c5
  role: evaluation
  text: 這張表也能用來檢查任何一套 harness 缺了哪一格：只有摘要的 harness，缺的是「存檔」和「原地編輯」
  source_quotes:
  - "這張表也能用來檢查任何一套 harness 缺了哪一格：只有摘要的 harness，缺的是「存檔」和「原地編輯」。"
  anchor_type: 部落格推論
  importance: 5
  status: normal
- id: c6
  role: context
  text: 表的另一個依據是 ContextBench：作者自建的小測試，專門量 context 管理本身，用來展示現有方法連簡單任務都做不好。設計上刻意不需要推理或知識：任務指令已經明講該做什麼，所以能把全部內容記住的 agent 一定全對，分數差異只反映管理能力
  source_quotes:
  - "作者先自建一個小測試 ContextBench，專門量 context 管理本身，用來展示現有方法連簡單任務都做不好。設計上刻意不需要推理或知識：任務指令已經明講該做什麼，所以能把全部內容記住的 agent 一定全對，分數差異只反映管理能力。"
  anchor_type: 設計參數
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: ContextBench 的難度用 context pressure（情境壓力）調整：整段任務輸入的總量除以 context 上限（32K）。1× 代表全部保留剛好塞滿，24× 代表輸入量是上限的 24 倍；低於 1× 的是對照組，全部留著也放得下
  source_quotes:
  - "難度用 context pressure（情境壓力） 調整：整段任務輸入的總量除以 context 上限（32K）。1× 代表全部保留剛好塞滿，24× 代表輸入量是上限的 24 倍；低於 1× 的是對照組，全部留著也放得下。"
  anchor_type: 設計參數
  comparison_target: context 上限（32K）
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: ContextBench 四個任務：Needle Retention 考選擇性保留（每個區塊有 2～8 行重要句和 140 行雜訊，要原文保留重要句、丟掉雜訊）；Sudoku Sketchpad 考原地小改（16×16 數獨棋盤，每回合下一步，只改一格，不重寫整盤）；KV Store 考卸載與檢索（一批批 SET 資料，要先存到檔案，之後 24 次 GET 查詢時撈回來）；Log Triage 也考卸載與檢索（一批批 log，之後 24 次查詢與計數）
  source_quotes:
  - "Needle Retention | 選擇性保留 | 每個區塊有 2～8 行重要句（needle）和 140 行雜訊，要原文保留 needle、丟掉雜訊"
  - "Sudoku Sketchpad | 原地小改 | 16×16 數獨棋盤，每回合下一步，只改一格，不重寫整盤"
  - "KV Store | 卸載與檢索 | 一批批 SET 資料，要先存到檔案，之後 24 次 GET 查詢時撈回來"
  - "Log Triage | 卸載與檢索 | 一批批 log，之後 24 次查詢與計數"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  figures:
  - file: figures/context-language-models/table3.png
    article: context-language-models
    src: table3.png
    caption: 表 1 — ContextBench 四個任務的定義與評分方式。（來源：原始論文 Table 3。）
    sha256: 81c8b3e3b515460bb2e4ee4d93af3e2f3896507b8e34ddc0f2a98a4f7575d1b0
  importance: 8
  status: normal
- id: c9
  role: mechanism
  text: 決策表每一格在 ContextBench 的對應：留在 context 對應 Needle Retention；存檔對應 KV Store、Log Triage；直接刪對應 Needle 的雜訊區塊；原地編輯對應 Sudoku Sketchpad；壓成摘要沒有對應的任務
  source_quotes:
  - "任何改寫都可能失真 | Needle Retention"
  - "摘要有損，存檔無損 | KV Store、Log Triage"
  - "省空間，失真可以接受 | 無"
  - "留著只佔空間 | Needle 的雜訊區塊"
  - "重寫整份又貴又容易抄錯 | Sudoku Sketchpad"
  anchor_type: 部落格推論
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: ContextBench 的評分一律只看 agent 的 context 內容：只存在檔案裡、沒留在 context 的答案不算分
  source_quotes:
  - "評分一律只看 agent 的 context 內容：只存在檔案裡、沒留在 context 的答案不算分。"
  anchor_type: 設計參數
  importance: 10
  status: normal
- id: c11
  role: evidence
  text: 在 ContextBench 上，CLM 的表現明顯高於其他方法，接近滿分
  source_quotes:
  - "結果直接看下圖：CLM 的表現明顯高於其他方法，接近滿分。"
  anchor_type: 實驗結果
  qualifiers:
  - text: "ContextBench 上的 CLM 帶有一份 skill，摘錄（論文 Table 4）中有 harness 提供的 [context: ~N/M tokens] 用量讀數"
    source_quote: "以及 ContextBench skill 摘錄（論文 Table 4）中的 [context: ~N/M tokens] 讀數，都是在補這個缺口。"
  - text: 這組比較的設定是 GPT-5.4、32K 上限
    source_quote: "圖 1 — ContextBench 的四個任務，以及 CLM 與各基線方法（GPT-5.4、32K 上限）的準確率比較。（來源：原始論文 Figure 2。）"
    source: figure_caption
  - text: blog 推論這只證明 CLM 的操作範圍夠大，不是管理策略比較聰明；它在論文裡的角色是動機，不是主要證據
    source_quote: "所以 CLM 接近滿分，證明的是操作範圍夠大，不是管理策略比較聰明。它在論文裡的角色是動機，不是主要證據。"
  figures:
  - file: figures/context-language-models/figure2.png
    article: context-language-models
    src: figure2.png
    caption: 圖 1 — ContextBench 的四個任務，以及 CLM 與各基線方法（GPT-5.4、32K 上限）的準確率比較。（來源：原始論文 Figure 2。）
    sha256: eb445730af35737731f52fcb7171504ffa25fcd5726c5d855e5ef8565a543dfa
  importance: 11
  status: normal
- id: c12
  role: evidence
  text: 論文歸納了現有方法的三個失敗原因：摘要式壓縮會遺漏或編造資訊（Needle、Sudoku）；沒有原地編輯的方法，每改一格都得重寫整盤數獨；一般工具能把資料存到檔案，卻沒辦法把它從 live context 主動踢掉
  source_quotes:
  - "論文歸納了三個失敗原因："
  - "摘要式壓縮會遺漏或編造資訊（Needle、Sudoku）。"
  - "沒有原地編輯的方法，每改一格都得重寫整盤數獨。"
  - "一般工具能把資料存到檔案，卻沒辦法把它從 live context 主動踢掉。"
  anchor_type: 原作者解讀
  qualifiers:
  - text: 這是在 ContextBench 上歸納的；blog 推論 ContextBench 證明的是操作範圍夠大，不是管理策略比較聰明
    source_quote: "所以 CLM 接近滿分，證明的是操作範圍夠大，不是管理策略比較聰明。"
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: blog 對 ContextBench 的打折：因為指令已經明講要把某段內容從 context 刪掉，測的是「做不做得到」，不是「判斷該留什麼」；這個 benchmark 由同一團隊設計，任務形式正好需要 CLM 才有的「從 live context 刪除、原地修改」
  source_quotes:
  - "因為指令已經明講「把這整段 filler 從你的 context 刪掉」，測的是「做不做得到」，不是「判斷該留什麼」。這個 benchmark 由同一團隊設計，任務形式正好需要 CLM 才有的「從 live context 刪除、原地修改」"
  anchor_type: 部落格推論
  importance: 13
  status: normal
- id: c14
  role: evaluation
  text: blog 的小結：現有方法要嘛由程式定死，要嘛讓模型從人設計的選單裡挑；選單裡少了「原地改」和「從 context 踢掉」，連簡單任務都會失手
  source_quotes:
  - "小結：現有方法要嘛由程式定死，要嘛讓模型從人設計的選單裡挑；選單裡少了「原地改」和「從 context 踢掉」，連簡單任務都會失手。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: "ContextBench 上的 CLM 帶有一份 skill，摘錄（論文 Table 4）中有 harness 提供的 [context: ~N/M tokens] 用量讀數"
    source_quote: "以及 ContextBench skill 摘錄（論文 Table 4）中的 [context: ~N/M tokens] 讀數，都是在補這個缺口。"
  - text: 這個結論來自同一團隊自建、測「做不做得到」的 ContextBench
    source_quote: "因為指令已經明講「把這整段 filler 從你的 context 刪掉」，測的是「做不做得到」，不是「判斷該留什麼」。這個 benchmark 由同一團隊設計"
  importance: 14
  status: normal
```
