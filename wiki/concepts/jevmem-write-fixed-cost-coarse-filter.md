---
id: jevmem-write-fixed-cost-coarse-filter
title: Jev-Mem 寫入時先用便宜的規則粗篩最多 10 個候選，Jev 只判斷這幾對要不要建邊，所以每句的 Jev 成本固定；代價是粗篩沒選上的舊記憶永遠建不了邊
type_hint: 方法
context_type: bound_to_source
sources:
- article: jev-mem
  article_title: "Jev-Mem：讓小模型打分數管 AI agent 記憶，建構速度進步 8.9 倍"
  url: https://datasciocean.com/paper-intro/jev-mem/
  sections:
  - agent 的記憶裡，藏著一大串小判斷
  - System One 判斷、System Two 作答
  - Jev 不寫字，只回答一批是非題
  - 記憶長什麼樣：一句話一個節點，加上四種邊
  - 邊的用途：把前因後果一起帶出來
  - 用符號寫下一筆觀察與整份記憶
  - 四種邊各自怎麼建
  - 寫入：每句話的 Jev 成本固定
  - 全部收下，挑選留到之後
  - 替每句話打類型分數
  - 便宜的規則先挑候選
  - Jev 判斷要不要建邊
  - 每隔一段時間做一次整理
  - 拿來用之前要知道的限制
  - 類型分數到底有沒有用
  - 實體抽取與時間邊
  - 定期整理只檢查第二十句
  - Jev 的輸入長什麼樣子
  first_appearance: true
parent: null
related:
  - jevmem-small-scorer-controls-memory
  - jevmem-read-plan-expand-stop
  - jevmem-results-gain-source
  - sag-tradeoffs-price-paid
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: Jev-Mem 寫入每一句話時，先用便宜的訊號替所有舊記憶打粗分，規則挑出最多 10 個候選，Jev 再仔細判斷這 10 個要不要建邊（先粗篩、再精排）；所以每句最多 2 次 Jev 呼叫，不會隨記憶庫變大而增加。好處是每句的 Jev 成本固定，代價是粗篩沒選上的舊記憶永遠建不了邊
  source_quotes:
  - '全部比太貴，所以先用便宜的訊號替所有舊記憶打一個粗分，只取前 \( K_w = 10 \) 名當候選'
  - "規則挑最多 10 個候選"
  - "每句最多 2 次 Jev 呼叫，不會隨記憶庫變大而增加。"
  - "這是「先粗篩、再精排」的兩段式：規則先大略篩出 10 個，Jev 再仔細判斷這 10 個。好處是每句的 Jev 成本固定；代價是：粗篩沒選上的舊記憶，永遠建不了邊。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  qualifiers:
  - text: 時間邊由規則建，不看內容，也不受 10 個候選的限制
    source_quote: "時間邊會連到無關的句子：規則不看內容，也不受 10 個候選的限制。"
  - text: 每 20 次寫入另做一次整理，由 Jev 判斷
    source_quote: "每 20 次寫入做一次整理，只針對第 20 句和它的候選，原句一律保留。Jev 要判斷這兩組問題："
  - text: blog 推論定期整理降頻是為了成本：每句都做的話，寫入的 Jev 呼叫會從最多 2 次變 3 次
    source_quote: "（推論）降頻是為了成本。每句都做的話，寫入的 Jev 呼叫會從最多 2 次變 3 次，而寫入速度正是這篇主打的賣點。"
  - text: 沒進前 10 名候選的舊記憶建不了的是語意、因果、實體邊
    source_quote: "沒進前 10 名候選的舊記憶建不了語意、因果、實體邊"
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
  text: Jev-Mem 的記憶是一張圖：一句話一個節點，只存一份；節點之間有四種邊，同一對節點可以同時有好幾種。節點另外還存 embedding、實體清單（句子提到的人名、地名等）和四個類型分數；整份記憶另有兩個讀取時找記憶的入口：向量索引（用 embedding 找意思相近的句子）與關鍵字索引（找用字相同的句子）
  source_quotes:
  - "記憶是一張圖：一句話一個節點，只存一份；節點之間有四種邊，同一對節點可以同時有好幾種。"
  - "節點另外還存 embedding"
  - "實體清單（句子提到的人名、地名等）和四個類型分數。"
  - "再加兩個「索引」，也就是讀取時找記憶的入口"
  - '\( I^{\text{vec}}_t \) 是向量索引（用 embedding 找意思相近的句子），\( I^{\text{lex}}_t \) 是關鍵字索引（找用字相同的句子）'
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c4
  role: mechanism
  text: 四種邊各自的意思和建法：語意邊是兩句在講同一個具體主題或事實，由 Jev 判斷；因果邊是一句導致或解釋另一句、有方向，由 Jev 判斷，正反兩個方向各問一題；實體邊是提到同一個對象，名稱相同用規則、寫法不同才問 Jev；時間邊是時間上相鄰、不代表有關係，依程式碼由規則建
  source_quotes:
  - "| 語意 | 兩句在講同一個具體主題或事實 | Jev 判斷 |"
  - "| 因果 | 一句導致或解釋另一句，有方向 | Jev 判斷，正反兩個方向各問一題 |"
  - "| 實體 | 提到同一個對象 | 名稱相同用規則；寫法不同才問 Jev |"
  - "| 時間 | 時間上相鄰，不代表有關係 | 規則（依程式碼） |"
  anchor_type: 設計參數
  qualifiers:
  - text: 依程式碼，實體邊大致等於「同一個說話者」，時間邊等於「時間相鄰」
    source_quote: "實體與時間邊都是便宜的固定規則，而且連得很寬：實體邊大致等於「同一個說話者」，時間邊等於「時間相鄰」。論文兩者都沒寫清楚，以下依程式碼。"
  importance: 3
  status: normal
- id: c5
  role: mechanism
  text: 每來一句話的寫入流程是：全部收下 → 打類型分數 → 規則挑最多 10 個候選 → 判斷並建邊。候選指的是最可能和新句子有關、值得仔細比對的舊記憶
  source_quotes:
  - "每來一句話：全部收下 → 打類型分數 → 規則挑最多 10 個候選 → 判斷並建邊。"
  - "候選指的是最可能和新句子有關、值得仔細比對的舊記憶。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 2
  status: normal
- id: c6
  role: mechanism
  text: 附錄的設定關閉了「要不要存」的過濾，所有非空的句子都會成為節點，理由是有些話當下不重要，要等之後的問題出現才知道它有用。「挑選」被移到建邊與讀取兩處，所以 Jev 判斷錯，頂多少一條邊，原句還在
  source_quotes:
  - "附錄的設定關閉了「要不要存」的過濾，所有非空的句子都會成為節點。理由是：有些話當下不重要，要等之後的問題出現才知道它有用。「挑選」被移到建邊與讀取兩處，所以 Jev 判斷錯，頂多少一條邊，原句還在。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c7
  role: mechanism
  text: 依程式碼，粗篩分數是四個訊號相加：向量相似度給 2 × 相似度（只加給向量搜尋前 10 名）、共同實體加 2、關鍵字重疊比例最多加 1、時間接近給 0.25 ÷（1 + 相差天數）
  source_quotes:
  - '（依程式碼）粗篩分數 \( s_{\text{cand}} \) 是四個訊號相加：'
  - "| 向量相似度 | 2 × 相似度（只加給向量搜尋前 10 名） |"
  - "| 共同實體 | 2 分 |"
  - "| 關鍵字重疊比例 | 最多 1 |"
  - "| 時間接近 | 0.25 ÷（1 + 相差天數） |"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 4
  status: normal
- id: c8
  role: qualifier
  text: "粗篩的副作用是：只要是同一個說話者，就會因為共同實體拿到同樣的 +2，因為每句存成「[Mira]: …」的形式，說話者名字一定被抽成實體"
  source_quotes:
  - "副作用是：只要是同一個說話者，就會因為共同實體拿到同樣的 +2（每句存成「[Mira]: …」，說話者名字一定被抽成實體"
  anchor_type: 部落格考證
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 4
  status: normal
- id: c9
  role: mechanism
  text: 寫入時的第 2 次 Jev 呼叫，把新記憶和 10 個候選之間的語意、雙向因果（必要時加實體別名）合成一批題目一次問完；Jev 判斷「新句和候選之間有某種關係」的分數至少要 0.60 才建這條邊。實體名稱相同、時間相鄰這兩種則由規則直接建
  source_quotes:
  - "這是第 2 次 Jev 呼叫（論文式 9）。新記憶和 10 個候選之間的語意、雙向因果（必要時加實體別名）合成一批題目一次問完，分數到門檻才建邊："
  - 'P(g \mid v, u) \ge \theta_{\text{rel}} = 0.60'
  - '式子的意思是：Jev 判斷「新句 \( v \) 和候選 \( u \) 之間有第 \( g \) 種關係」的分數，至少要 0.60 才建這條邊。實體名稱相同、時間相鄰這兩種則由規則直接建。'
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  qualifiers:
  - text: 分數不保證經過校準，門檻都是工程設定，不能讀成「有 60% 把握」
    source_quote: "附錄 B.1 明說它們不保證經過校準。所以後文出現的 0.60、0.95 這些門檻都是工程設定，不能讀成「有 60% 把握」。"
  importance: 2
  status: normal
- id: c10
  role: qualifier
  text: 依程式碼，規則建的邊連得很寬：實體邊大致等於「同一個說話者」（同一個說話者的句子之間幾乎都有實體邊，仍限於 10 個候選之內），時間邊等於「時間相鄰」，時間邊的規則不看內容，也不受 10 個候選的限制；在 LoCoMo 上，同一場對話的每句話時間戳都是同一個場次日期，新句子幾乎一定連到前 9 句
  source_quotes:
  - "實體與時間邊都是便宜的固定規則，而且連得很寬：實體邊大致等於「同一個說話者」，時間邊等於「時間相鄰」。論文兩者都沒寫清楚，以下依程式碼。"
  - "說話者名字一定被抓到，所以同一個說話者的句子之間幾乎都有實體邊（仍限於 10 個候選之內）。"
  - "時間邊會連到無關的句子：規則不看內容，也不受 10 個候選的限制。"
  - "在 LoCoMo 上這更明顯：同一場對話的每句話，時間戳都是同一個場次日期，時間差為 0，新句子幾乎一定連到前 9 句。"
  anchor_type: 部落格考證
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 3
  status: normal
- id: c11
  role: evaluation
  text: blog 推論，因果邊只在「文字裡看得出因果」時才會建立，而明講因果的句子通常會提到同一件事，本來就容易被相似度找到；所以邊的價值主要是「把前因後果一起帶出」，而不是「找到相似度完全找不到的句子」
  source_quotes:
  - "（推論）因果邊只在「文字裡看得出因果」時才會建立"
  - "而明講因果的句子通常會提到同一件事，本來就容易被相似度找到。所以邊的價值主要是「把前因後果一起帶出」，而不是「找到相似度完全找不到的句子」。"
  anchor_type: 部落格推論
  importance: 3
  status: normal
- id: c12
  role: mechanism
  text: 每 20 次寫入做一次整理，只針對第 20 句和它的候選，原句一律保留。Jev 判斷它們之間是否重複、矛盾、過時，或值得補一條連結，並在「分開／合併／歸納／不確定」中選一個；只有在合併或歸納的分數 ≥ 0.85、矛盾 < 0.85，而且系統有提供摘要器（另外接上、負責把幾句話寫成一條摘要的 LLM）時，才會請它寫出新條目
  source_quotes:
  - "每 20 次寫入做一次整理，只針對第 20 句和它的候選，原句一律保留。Jev 要判斷這兩組問題："
  - "它們之間是否重複、矛盾、過時，或值得補一條連結？"
  - "該怎麼處理：在「分開／合併／歸納／不確定」中選一個。"
  - "只有在合併或歸納的分數 ≥ 0.85、矛盾 < 0.85，而且系統有提供摘要器（另外接上、負責把幾句話寫成一條摘要的 LLM）時，才會請它寫出新條目。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  qualifiers:
  - text: 分數不保證經過校準，門檻都是工程設定，不能讀成「有 60% 把握」
    source_quote: "附錄 B.1 明說它們不保證經過校準。所以後文出現的 0.60、0.95 這些門檻都是工程設定，不能讀成「有 60% 把握」。"
  - text: 附錄原文只說「每成功寫入 20 次，評估一次候選配對」，有兩種讀法，文字無法判定
    source_quote: "附錄原文只說「每成功寫入 20 次，評估一次候選配對」，有兩種讀法，文字無法判定："
  - text: 只檢查第 20 句與它的候選，是程式碼的做法
    source_quote: "| A（程式碼的做法） | 只檢查第 20 句與它的候選 |"
  importance: 3
  status: normal
- id: c13
  role: evaluation
  text: 為什麼每 20 次整理一次、為什麼只檢查一句，論文都沒給理由；附錄原文只說「每成功寫入 20 次，評估一次候選配對」，文字無法判定是只檢查第 20 句與它的候選（程式碼的做法），還是這 20 句都檢查。論文沒有「關掉整理」的對照實驗，也沒說實驗時有沒有提供摘要器，所以這個機制對準確度的貢獻未知
  source_quotes:
  - "為什麼是 20、為什麼只檢查一句，論文都沒給理由"
  - "附錄原文只說「每成功寫入 20 次，評估一次候選配對」，有兩種讀法，文字無法判定："
  - "| A（程式碼的做法） | 只檢查第 20 句與它的候選 |"
  - "| B | 這 20 句都檢查 |"
  - "論文沒有「關掉整理」的對照實驗，也沒說實驗時有沒有提供摘要器，所以這個機制對準確度的貢獻未知。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 3
  status: normal
- id: c14
  role: qualifier
  text: blog 推論，定期整理降頻是為了成本：每句都做的話，寫入的 Jev 呼叫會從最多 2 次變 3 次，而寫入速度正是這篇主打的賣點
  source_quotes:
  - "（推論）降頻是為了成本。每句都做的話，寫入的 Jev 呼叫會從最多 2 次變 3 次，而寫入速度正是這篇主打的賣點。"
  anchor_type: 部落格推論
  comparison_target: 每句都做整理 vs. 不做整理時的寫入 Jev 呼叫次數
  importance: 4
  status: normal
- id: c15
  role: evaluation
  text: 寫入時的第 1 次 Jev 呼叫替每句話打類型分數：四道是非題一次問完，分別問這句話像不像「發生過的事件」「一般性事實」「做事的步驟」「個人喜好」，只是四個是非題標籤，可以同時都高。依程式碼，類型分數有算、有存，但在找候選、判斷關係、讀取打分三處都沒被使用；交給 System Two 的內容與定期整理是否用到，筆記作者沒檢視這兩段程式碼
  source_quotes:
  - "這是第 1 次 Jev 呼叫（論文式 7）：四道是非題一次問完，分別問這句話像不像「發生過的事件」「一般性事實」「做事的步驟」「個人喜好」："
  - "只是四個是非題標籤，可以同時都高。"
  - "類型分數有算、有存，但在找候選、判斷關係、讀取打分三處都沒被使用"
  - "（依程式碼）各環節的使用情況："
  - "| 交給 System Two 的內容、定期整理 | 未確認 | 筆記作者沒檢視這兩段程式碼 |"
  anchor_type: 部落格考證
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 3
  status: normal
- id: c16
  role: evaluation
  text: 論文只說類型分數「標注在節點上」。blog 推論它是預留欄位，代價是每次寫入的兩次 Jev 呼叫中，有一次的產出沒有影響後續結果
  source_quotes:
  - "論文只說分數「標注在節點上」。（推論）它是預留欄位；代價是每次寫入的兩次 Jev 呼叫中，有一次的產出沒有影響後續結果。"
  anchor_type: 部落格推論
  qualifiers:
  - text: 交給 System Two 的內容與定期整理有沒有用到類型分數，未確認
    source_quote: "（推論）每句兩次 Jev 呼叫中，有一次的產出沒影響後續（交給 System Two 的內容與定期整理未確認"
  importance: 3
  status: normal
- id: c17
  role: evaluation
  text: blog 不建議拿類型分數當硬門檻、只跟同類型的舊記憶比，原因有三：會漏掉跨類型的關係（自編例子：「我討厭塞車」（喜好）和「我改騎腳踏車上班了」（事件）之間有一條有價值的因果邊，同類型篩選會讓這一對永遠不被比較）；類型是分數不是標籤，一句話可以同時是事件與喜好，「同類型」還得另訂門檻；粗篩的目標是不漏，粗篩沒選上的永遠建不了邊，再加硬過濾只會漏更多。同類型加一點分，則同類型優先、跨類型仍有機會，但加分幅度需要調
  source_quotes:
  - "那能不能拿它來篩候選，只跟同類型的舊記憶比？不建議當硬門檻，原因有三："
  - "會漏掉跨類型的關係。"
  - "（自編）「我討厭塞車」（喜好）和「我改騎腳踏車上班了」（事件）之間有一條有價值的因果邊，同類型篩選會讓這一對永遠不被比較。"
  - "類型是分數不是標籤。"
  - "一句話可以同時是事件與喜好，「同類型」還得另訂門檻。"
  - "粗篩的目標是不漏。"
  - "粗篩沒選上的永遠建不了邊，再加硬過濾只會漏更多。"
  - "| 同類型加一點分 | 同類型優先，跨類型仍有機會 | 加分幅度需要調 |"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 沒進前 10 名候選的舊記憶建不了的是語意、因果、實體邊
    source_quote: "沒進前 10 名候選的舊記憶建不了語意、因果、實體邊"
  importance: 2
  status: normal
```
