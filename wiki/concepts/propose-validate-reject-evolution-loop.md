---
id: propose-validate-reject-evolution-loop
title: 最值得帶走的離線改進迴圈是「提案、獨立驗證集把關、被拒記錄回灌」，不依賴圖、可套在任何可編輯文字資產上；但落地要提防爬山法卡局、驗證集太小收雜訊、約束只寫在 prompt 等三個限制
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
  - article: procedural-graphs
    article_title: "把流程畫成圖，AI Agent 就不會迷路？Procedural Graphs 解析"
    url: https://datasciocean.com/paper-intro/procedural-graphs/
    sections:
      - agent 做長任務，為什麼會迷路？
      - 圖由什麼組成
      - 離線演化：讓 LLM 改圖，驗證集把關
      - refiner 怎麼提出修改
      - 驗證閘門：決定改圖會不會越改越糟
      - 拒絕記憶：記下被丟的修改
      - 改進迴圈：提案、獨立驗證、被拒回灌
      - 使用時要記得的限制
      - 怎麼選閘門
      - refiner 的輸入與被拒絕的歷史
    first_appearance: true
parent: null
related:
  - pg-structure-and-inference
  - pg-local-subgraph-vs-full-graph
  - pg-results-and-expert-graph-collapse
  - evoontology-evolution-loop-gate-first
  - skillopt-blind-acceptance-gate
  - subagent-fold-eval-gated-migration
  - clm-text-steering-and-skill-evolution
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: blog 認為 Procedural Graphs 最值得帶走的不是圖，而是它的改進迴圈——「提案、獨立驗證集把關、被拒記錄回灌」：讓 LLM 提出對文字資產（prompt、規則、skill、圖）的修改，用沒看過的資料量化新舊版本、沒變差才採用，被拒的記下來下次提案時一併給它看；這個做法與圖無關，任何可編輯的文字資產都能套
    source_quotes:
      - "我自己覺得最值得帶走的不是圖，而是它的改進迴圈：提案、用獨立驗證集把關、把被拒的記錄回灌給提案者。這個迴圈可以套在任何可編輯的文字資產上"
      - "讓 LLM 提出對某份文字資產（prompt、規則、skill、圖）的修改，用一組它沒看過的資料量化新舊版本，沒變差才採用，被拒的記下來，下一次提案時一併給它看。這個做法與圖無關，任何可編輯的文字資產都能套。"
    anchor_type: 部落格判斷
    qualifiers:
      - text: 套用到自己的資產時，要留意三個限制：爬山法走不出需要先變差才能到達的設計、驗證集太小時閘門收的多半是雜訊、只寫在 prompt 而驗證器不檢查的約束等於沒有約束
        source_quote: "爬山法走不出需要先變差才能到達的設計。驗證集太小時，閘門收的多半是雜訊。只寫在 prompt、驗證器不檢查的約束等於沒有約束"
    importance: 1
    status: normal

  - id: c2
    role: context
    text: 這個迴圈出自 Google 論文 Procedural Graphs（PG）的離線演化階段：先用目前保留的圖讓 solver（負責選動作的 LLM）在訓練題上跑一批並留下軌跡與分數，refiner（專門改圖、與 solver 同底層模型的 LLM）讀軌跡提出修改清單套用到圖的副本，經結構檢查與獨立驗證集把關，不比舊圖差才採用，被拒的寫進拒絕記憶（H_rejected）供下一輪 refiner 參考
    source_quotes:
      - "這篇整理 Google 的論文 *Procedural Graphs: Self-Evolving Execution Structures for LLM Agents*（arXiv 2609.09153v1，2026 年九月）。"
      - "同一個模型、同一個 solver（負責選動作的那個 LLM）"
      - "離線的部分是這樣：先讓 solver 在訓練題上跑一批，留下成功與失敗的軌跡；refiner（專門改圖的 LLM，與 solver 同一個底層模型）讀軌跡，輸出一份修改清單，套用到圖的副本得到候選圖；候選圖在獨立驗證集上不比目前的圖差才採用，被拒的記下來（這份記錄叫拒絕記憶），下一輪給 refiner 看（Section 3.3、Algorithm 1）。"
      - "做結構檢查，沒過就丟，不跑驗證。"
    anchor_type: 設計參數
    importance: 2
    status: normal

  - id: c3
    role: mechanism
    text: refiner 不是重畫一張新圖，而是輸出包含 Add（補節點或邊）與 Delete（刪節點或邊）兩種操作的修改清單 ΔG_k，套用到上一輪保留的圖 G_{k-1} 副本得到候選圖；要改邊的屬性，就是刪掉再用新屬性加回去
    source_quotes:
      - "refiner 不是重畫一張新圖，而是開一張修改清單，套用到圖的副本上，得到候選圖。"
      - "G_k^{cand} = G_{k-1} \\oplus \\Delta G_k"
      - "修改只有兩種：Add（補節點或邊，例如補一個驗證步驟）與 Delete（刪掉老是把軌跡帶進失敗的節點或邊）。要改邊的屬性，就是刪掉再用新屬性加回去。"
    anchor_type: 設計參數
    numeric_kind: non_comparative
    numeric_reason: 定義
    importance: 3
    status: normal

  - id: c4
    role: mechanism
    text: 結構檢查只看三件事：邊的端點必須存在、節點與關係型別合法、每個節點都有路徑走得到終點節點（沒有往外邊的節點才算終點），沒通過的候選直接丟掉、不跑驗證
    source_quotes:
      - "做結構檢查，沒過就丟，不跑驗證。"
      - "結構檢查（Appendix B.6）只看三件事：邊的端點必須存在、節點與關係型別合法、每個節點都有路徑走得到終點節點（沒有往外邊的節點才算終點）。沒通過的候選直接丟掉。"
    anchor_type: 設計參數
    qualifiers:
      - text: 結構檢查有一個漏洞：refiner prompt 要求 ACTION 節點必須是真實的工具名，但驗證器不檢查這點，只靠 prompt 約束，只能靠下一步的驗證分數擋
        source_quote: "refiner prompt 要求 ACTION 節點必須是真實的工具名，但驗證器不檢查這點，只靠 prompt 約束。refiner 若編出不存在的工具節點，結構檢查擋不住，只能靠下一步的驗證分數擋。"
    importance: 4
    status: normal

  - id: c5
    role: mechanism
    text: 驗證閘門在獨立驗證集 D_val（和訓練批、測試集分開）上計算候選圖平均分 S_val(G_k^cand)，採用規則是 S_val(G_k^cand) ≥ S_val(G_{k-1})（持平也收，舊圖分數快取不重跑），否則留著舊圖；需要獨立驗證集是因為 refiner 看過訓練軌跡才提修改，在訓練批有效不代表真的有效
    source_quotes:
      - "S_{val}(G) = \\frac{1}{|D_{val}|} \\sum_{(q,y) \\in D_{val}} S\\big(f_{solver}(q \\mid G),\\, y\\big)"
      - "G_k = \\begin{cases} G_k^{cand}, & S_{val}(G_k^{cand}) \\ge S_{val}(G_{k-1}) \\\\ G_{k-1}, & \\text{otherwise} \\end{cases}"
      - "\\( D_{val} \\)：驗證集，和訓練批、測試集都分開。"
      - "比較用的是 \\( \\ge \\)，持平也收。舊圖的分數是快取的，不重跑。"
      - "為什麼要獨立的驗證集？因為 refiner 是看過訓練軌跡才提出修改的，在訓練批上有效，不代表真的有效。"
    anchor_type: 設計參數
    numeric_kind: non_comparative
    numeric_reason: 定義
    qualifiers:
      - text: 持平也收且驗證集太小時，雜訊也可能把圖往前推
        source_quote: "持平也收，所以雜訊也可能把圖往前推。"
    importance: 5
    status: normal

  - id: c6
    role: mechanism
    text: 被拒的候選會寫進拒絕記憶 H_rejected 當作下一輪 refiner 的負面證據，圖不變，下一輪用同一張圖在下一批訓練題上重跑，迴圈固定跑 K 輪、不會因被拒提早停止；存進去的訓練軌跡是用被拒前的舊圖 G_{k-1} 跑出來的，候選圖在驗證集跑出的軌跡不存、只留分數
    source_quotes:
      - "被拒的修改不會憑空消失。下一輪 refiner 提修改時，除了目前的圖和新一批軌跡，還會看到被拒過的候選，當作「別再提這種」的提醒。"
      - "被拒之後的處理很單純：圖不變，記一筆，下一輪用同一張圖在下一批訓練題上重跑，再讓 refiner 重新提修改。迴圈固定跑 \\( K \\) 輪，不會因為被拒而提早停止。"
      - "要注意的是，存進去的軌跡是用被拒之前的那張圖 \\( G_{k-1} \\) 跑出來的，refiner 就是看了這批軌跡才提出那份被拒的修改；候選圖本身在驗證集上跑出的軌跡不會存，只留下分數。所以記錄的是「當初為什麼這樣改」的證據。"
    anchor_type: 設計參數
    numeric_kind: non_comparative
    numeric_reason: 定義
    qualifiers:
      - text: 真正餵給 refiner 的是 H_rejected 的哪一部分，論文有兩種說法沒有判定（Section 3.3 說整筆都進，Appendix B.6 說 SerializeRejections 只交候選圖加驗證分數或結構錯誤診斷）
        source_quote: "真正餵給 refiner 的是哪一部分？論文有兩種說法，沒有判定：…Section 3.3 Step 4 | 整筆都進 \\( H_{rejected} \\)，refiner 收到 \\( H_{rejected} \\)…Appendix B.6 | SerializeRejections 只交「候選圖加驗證分數（或結構錯誤診斷）」，訓練軌跡留在記錄裡，沒提 \\( \\Delta G \\)"
      - text: H_rejected 本身沒有上限、摘要或淘汰機制，演算法裡只有 append、從不清空（論文有限制長度的只有訓練軌跡 C_k）
        source_quote: "論文有限制長度的只有訓練軌跡 \\( C_k \\)（超過 \\( L_{max} \\) 就砍開頭，\\( L_{max} \\) 的數值論文沒給）；\\( H_{rejected} \\) 本身沒有上限、摘要或淘汰機制，演算法裡只有 append，從不清空。"
    importance: 6
    status: normal

  - id: c7
    role: anchor
    text: 在 EnterpriseArena（財務模擬環境，撐滿 132 個月不破產）用 Gemini 3.5 Flash 做的十輪自我演化中，驗證存活率（分母 20 個 episode，1 個等於 5 個百分點）從起始空圖 0.0% 一路只升不降到 R8 與 R9 的 90.0%，期間 R3、R4、R6 驗證較低被丟，R5 結構檢查沒過被丟，R7（80.0%）與 R9（90.0%）持平被收，R10 訓練 90.0% 但驗證 85.0% 被擋下
    source_quotes:
      - "EnterpriseArena，一個財務模擬環境，agent 扮演 CFO（財務長）管理公司現金，目標是撐滿 132 個月不破產。"
      - "表 2 是 Appendix E 的 Table 11，在 EnterpriseArena 上用 Gemini 3.5 Flash 做的自我演化。…分母是驗證集的 20 個 episode（一次完整的模擬），1 個 episode 等於 5 個百分點；存活率指撐滿 132 個月沒破產的比例。"
      - "R1 | 45.0%（9/20） | 0.0%（起始空圖） | 收 | R1"
      - "R2 | 80.0%（16/20） | 45.0% | 收 | R2"
      - "R5 | 結構檢查沒過，沒跑驗證 | 80.0% | 丟 | R2"
      - "R7 | 80.0%（16/20） | 80.0% | 持平，收 | R7"
      - "R8 | 90.0%（18/20） | 80.0% | 收 | R8"
      - "R9 | 90.0%（18/20） | 90.0% | 持平，收 | R9"
      - "R10 的訓練存活率是 90.0%，驗證只有 85.0%，被擋下的就是只在訓練批上有效的改動（Appendix E.2）。"
    anchor_type: 實驗結果
    comparison_target: 前一輪保留圖的驗證存活率（起始空圖 0.0% 至 R9 90.0%）
    qualifiers:
      - text: 論文沒寫這個實驗的 S_val 用哪個指標，是 blog 依表 2 決策推測閘門實際看的是存活率
        source_quote: "論文沒寫這個實驗的 \\( S_{val} \\) 用哪個指標。但表 2 的決策只對得上存活率。這是我的推測：閘門實際看的是存活率。"
      - text: 驗證集只有 20 個 episode，差 1 個就是 5 個百分點；論文自己說一次接受或拒絕只差一兩個 episode，只能當搜尋過程記錄，不能當統計顯著性檢定
        source_quote: "20 個 episode 差 1 個就是 5 個百分點。論文自己也說，一次接受或拒絕只差一兩個 episode，只能當作搜尋過程的記錄，不能當作統計上的顯著性檢定（Section 5.4）。"
    figures:
      - file: figures/procedural-graphs/table11.png
        article: procedural-graphs
        src: table11.png
        caption: 表 2 — 十輪自我演化的逐輪指標（Gemini 3.5 Flash，EnterpriseArena）。（來源：原始論文 Table 11。）
        sha256: 659e32f71647d2cc0a3e27289c857d702a4f59c5e437963f22f11e92b383977b
    importance: 7
    status: normal

  - id: c8
    role: evidence
    text: EnterpriseArena 的 R3 是獨立驗證集把關並丟棄修改的實例：R3 把觸發募資的現金門檻調低，在訓練種子上有效，在驗證集上卻造成過早稀釋與現金不足，驗證存活率從 80.0% 掉到 65.0% 而被丟
    source_quotes:
      - "再看 Appendix E.2 的一輪：R3 把觸發募資的現金門檻調低，在訓練種子（可以理解成模擬的隨機起點）上有效，在驗證集上卻造成過早稀釋與現金不足，驗證存活率從 80.0% 掉到 65.0%，被丟。"
    anchor_type: 實驗結果
    comparison_target: 目前保留圖 R2 的驗證存活率 80.0%
    qualifiers:
      - text: 使用 Gemini 3.5 Flash，EnterpriseArena 驗證集共 20 個 episode
        source_quote: "表 2 是 Appendix E 的 Table 11，在 EnterpriseArena 上用 Gemini 3.5 Flash 做的自我演化。…分母是驗證集的 20 個 episode"
    figures:
      - file: figures/procedural-graphs/table11.png
        article: procedural-graphs
        src: table11.png
        caption: 表 2 — 十輪自我演化的逐輪指標（Gemini 3.5 Flash，EnterpriseArena）。（來源：原始論文 Table 11。）
        sha256: 659e32f71647d2cc0a3e27289c857d702a4f59c5e437963f22f11e92b383977b
    importance: 8
    status: normal

  - id: c9
    role: evaluation
    text: 限制一（一般知識類比，非論文內容）：只接受不比現在差的改動就是爬山法，分數只升不降，但也走不出需要先變差才能到達的更好設計
    source_quotes:
      - "這整套機制就是爬山法（每一步只往更高處走，不回頭下坡）：只接受不比現在差的改動，所以分數只升不降，但也走不出需要先變差才能到達的更好設計。"
      - "爬山法走不出需要先變差才能到達的設計。"
    anchor_type: 背景說明
    importance: 9
    status: normal

  - id: c10
    role: evaluation
    text: 限制二：驗證集太小時，接受與拒絕大半是雜訊（例如 20 個 episode 差 1 個就是 5 個百分點），加上持平也收，雜訊也可能把資產往前推
    source_quotes:
      - "驗證集太小時，接受與拒絕大半是雜訊。20 個 episode 差 1 個就是 5 個百分點。…持平也收，所以雜訊也可能把圖往前推。"
      - "驗證集太小時，閘門收的多半是雜訊。"
    anchor_type: 部落格判斷
    comparison_target: 驗證集共 20 個 episode 中 1 個 episode 佔總體的比例（5 個百分點）
    importance: 10
    status: normal

  - id: c11
    role: evaluation
    text: 限制三：只寫在 prompt、驗證器不檢查的約束等於沒有約束（例如 refiner prompt 要求 ACTION 節點必須是真實工具名，但結構驗證器不查）；套用到自己的資產時，最先該檢查的是驗證集夠不夠大，以及約束有沒有被程式檢查
    source_quotes:
      - "只寫在 prompt、驗證器不檢查的約束等於沒有約束（refiner 編出不存在的工具節點，就是例子）。"
      - "套用到自己的資產時，最先該檢查的是驗證集夠不夠大，以及約束有沒有被程式檢查。"
    anchor_type: 部落格判斷
    importance: 11
    status: normal

  - id: c12
    role: evaluation
    text: 選閘門的一般知識建議（非論文內容）：先用貪心閘門（只接受不比現在差的版本）；只有驗證分數連續多輪不動、而且驗證資料夠大時，才考慮能接受較差版本、或同時保留多個候選的做法
    source_quotes:
      - "這是一般知識，不是論文內容：先用這種貪心（只接受不比現在差的版本）閘門；只有驗證分數連續多輪不動、而且驗證資料夠大時，才考慮能接受較差版本、或同時保留多個候選的做法。"
    anchor_type: 背景說明
    importance: 12
    status: normal
```
