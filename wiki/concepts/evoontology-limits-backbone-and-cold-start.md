---
id: evoontology-limits-backbone-and-cold-start
title: EvoOntology 是值得借用的設計，不是建一次到處通用的系統：換 backbone 要重新演化，冷啟動只從查詢文字反推概念、沒被問過的就學不到，停止規則等細節也要自己補上
type_hint: 判斷
context_type: bound_to_source
sources:
- article: evoontology
  article_title: "EvoOntology 解析：在 data agent 與資料之間，加一層會自己演化的 ontology"
  url: https://datasciocean.com/paper-intro/evoontology/
  sections:
  - data agent 每次都從零摸資料，把說明整包塞進 prompt 還可能更糟
  - 冷啟動：不靠人工、不看標準答案，生出第一版 ontology
  - propose、probe、verify、construct：概念要被真實資料驗證才收進來
  - workload-driven 冷啟動的盲點：沒被問過就永遠學不到
  - workload 怎麼分給不同用途，以及 split-and-swap 評估法
  - Diagnose 與 Attribute：先判斷問題出在 Content、Tool 還是 Schema
  - Patch：一次候選修補只能動一層
  - Gate：候選要在同條件下贏過父版本至少 τ 分才轉正
  - 演化到底跑了幾輪：因 backbone 與 benchmark 而異
  - 跨 backbone 遷移：換底層模型，ontology 幾乎要重新演化
  - 評價：貢獻中等偏架構層面，細節缺口不小
  - 帶得走的收穫：該不該整包塞，看量有多大；自我演化的骨架，閘門先行
  first_appearance: true
parent: null
related:
  - evoontology-three-layer-ontology
  - evoontology-evolution-loop-gate-first
  - evoontology-query-over-prompt-stuffing
  - skill-pack-vs-ontology-graph
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: EvoOntology 是值得借用的設計，不是建一次到處通用的系統；換 backbone 要重新演化，冷啟動與停止規則等細節也要自己補上
  source_quotes:
  - "**存疑**：EvoOntology 是值得借用的設計，不是建一次到處通用的系統；換 backbone 要重新演化，冷啟動與停止規則等細節也要自己補上。"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: "EvoOntology 出自論文《EvoOntology: A Self-Evolving Ontology Layer for Data Agents》：data agent（根據自然語言指令操作資料庫表格、CSV、文件、log 這類異質資料的 AI agent）事前不認識資料、每次都要重新摸索，EvoOntology 在 agent 與資料之間放一層可查詢、會演化的 ontology（blog 建議先把它理解成一份結構化的領域知識），由 Schema、Content、Tool 三層組成。backbone 指驅動 agent 的底層 LLM"
  source_quotes:
  - "EvoOntology: A Self-Evolving Ontology Layer for Data Agents"
  - "一種根據自然語言指令，去操作資料庫表格、CSV、文件、log 這類異質資料的 AI agent"
  - "EvoOntology 想解決的是 data agent 事前不認識資料、每次都要重新摸索的問題，做法是在 agent 與資料之間放一層可查詢、會演化的 ontology，由 Schema、Content、Tool 三層組成。"
  - "先把它理解成一份結構化的領域知識"
  - "backbone（驅動 agent 的底層 LLM）"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: 冷啟動：builder agent 不靠人工、也完全不看標準答案，直接從訓練用的查詢集合（workload）加上原始資料源，自動生出第一版 ontology。流程分四步：propose 從 workload 提出候選概念，probe 對每個候選實際發探測查詢到資料源，verify 檢查探測結果的型別、值分佈與語意一致性，符合才通過，construct 把通過驗證的候選依 Schema Layer 的規則實例化成初始 Content Layer
  source_quotes:
  - "builder agent 怎麼不靠人工，也完全不看標準答案（gold answer），直接從訓練用的查詢集合（workload）加上原始資料源，自動生出第一版 ontology。"
  - "**propose**：從 workload \\( W \\) 提出候選概念集合 \\( C \\)，例如 Cost、Revenue、Profit、Time。"
  - "**probe**：對每個候選 \\( c \\)，實際發探測查詢到資料源 \\( D \\)。"
  - "**verify**：檢查探測結果的型別、值分佈與語意一致性是否符合預期，符合才通過。"
  - "**construct**：把通過驗證的候選，依 Schema Layer 的規則實例化成初始 Content Layer。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3b
  role: context
  text: 冷啟動之後還有自我演化迴圈：回頭看 agent 過去實際執行任務的一批紀錄（軌跡，指 agent 執行任務時留下的完整過程），找出重複出現的失敗模式，判斷是 ontology 的哪個部分沒做好，再生出修補方案；候選修補要和還沒改之前的版本放在完全相同的條件下比一次，贏得夠多分才准轉正
  source_quotes:
  - "要做的事是回頭看 agent 過去實際執行任務的一批紀錄，找出重複出現的失敗模式，並判斷這個失敗是 ontology 的哪個部分沒做好"
  - "演化迴圈用的軌跡（agent 執行任務時留下的完整過程）"
  - "針對歸因完成的訊號，真的動手生出一個修補方案"
  - "系統把候選與「還沒改之前的版本」放在完全相同的條件下比一次，贏得夠多分才准轉正。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c4
  role: evidence
  text: 同一套流程，換不同 backbone（GPT-5.5、GPT-5.6-sol、Claude-Sonnet-5、Claude-Opus-4.8 這四個）各自演化出一套 ontology；在這四個 backbone 之間，把 A backbone 演化出來的 ontology 拿去給 B backbone 用，表現全面下滑，沒有例外
  source_quotes:
  - "同一套流程，換不同 backbone（GPT-5.5、GPT-5.6-sol、Claude-Sonnet-5、Claude-Opus-4.8）各自演化出一套 ontology。把 A backbone 演化出來的 ontology 拿去給 B backbone 用，表現**全面下滑"
  - "沒有例外。"
  anchor_type: 實驗結果
  numeric_kind: non_comparative
  numeric_reason: 名稱
  figures:
  - file: figures/evoontology/figure5.png
    article: evoontology
    src: figure5.png
    caption: 圖 6 — 演化出的 ontology 在不同 backbone 之間的泛化：(a) 兩兩 Term 重疊度，(b) 跨 backbone 遷移表現。（來源：原始論文 Figure 5。）
    sha256: e8875c9c1d12f7631716d976c475cb24c98aa88a8d260d5a7f7648b22e53a83e
  importance: 2
  status: normal
- id: c5
  role: evidence
  text: blog 寫跨 backbone 遷移平均掉 6.6（Sonnet-5）到 10.9（GPT-5.5）分
  source_quotes:
  - "平均掉 6.6（Sonnet-5）到 10.9（GPT-5.5）分"
  anchor_type: 實驗結果
  figures:
  - file: figures/evoontology/figure5.png
    article: evoontology
    src: figure5.png
    caption: 圖 6 — 演化出的 ontology 在不同 backbone 之間的泛化：(a) 兩兩 Term 重疊度，(b) 跨 backbone 遷移表現。（來源：原始論文 Figure 5。）
    sha256: e8875c9c1d12f7631716d976c475cb24c98aa88a8d260d5a7f7648b22e53a83e
  importance: 5
  status: pending_author_confirmation
- id: c6
  role: evidence
  text: 不同 backbone 演化出的 Term 集合，彼此重疊並不高：論文指出沒有任何一對的重疊度超過 0.62，兩個 Claude 之間的重疊（0.55）甚至比兩個 GPT 之間還低
  source_quotes:
  - "圖 6(a) 顯示不同 backbone 演化出的 Term 集合，彼此重疊並不高：論文指出沒有任何一對超過 0.62，兩個 Claude 之間的重疊（0.55）甚至比兩個 GPT 之間還低。"
  anchor_type: 實驗結果
  comparison_target: 0.62 是所有 backbone 兩兩之間的上限；0.55 對比兩個 GPT 之間的重疊
  figures:
  - file: figures/evoontology/figure5.png
    article: evoontology
    src: figure5.png
    caption: 圖 6 — 演化出的 ontology 在不同 backbone 之間的泛化：(a) 兩兩 Term 重疊度，(b) 跨 backbone 遷移表現。（來源：原始論文 Figure 5。）
    sha256: e8875c9c1d12f7631716d976c475cb24c98aa88a8d260d5a7f7648b22e53a83e
  importance: 3
  status: normal
- id: c7
  role: evaluation
  text: blog 的判斷：這不是一套「建一次、到處通用」的系統，換底層模型，等於要重新跑一次演化；這是部署時一個實質的成本與限制，論文的摘要沒有強調
  source_quotes:
  - "**這不是一套「建一次、到處通用」的系統。** 換底層模型，等於要重新跑一次演化。這是部署時一個實質的成本與限制，論文的摘要沒有強調。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c8
  role: mechanism
  text: 冷啟動的 propose 完全是 bottom-up，只從查詢文字反推概念，沒有主動去掃資料庫 schema，找「可能存在但 workload 沒問到」的候選；blog 指出這對應到 text-to-SQL 領域的 schema linking 問題（把問題裡的詞對應到資料庫的表與欄位）
  source_quotes:
  - "propose 完全是 bottom-up，只從查詢文字反推概念，**沒有主動去掃資料庫 schema，找「可能存在但 workload 沒問到」的候選**。這正好對應到 text-to-SQL 領域的 schema linking 問題（把問題裡的詞對應到資料庫的表與欄位）"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c9
  role: evaluation
  text: blog 推論的死角：如果一個複雜的多層關係在冷啟動時就漏掉，而且從來沒被使用者問過，它也不會出現在執行軌跡裡，演化迴圈根本沒有機會去補這個洞；這個「沒被問過就永遠學不到」的死角，論文沒有討論
  source_quotes:
  - "破綻在於，如果一個複雜的多層關係在冷啟動時就漏掉，而且從來沒被使用者問過，它也不會出現在執行軌跡裡，演化迴圈根本沒有機會去補這個洞。這個「沒被問過就永遠學不到」的死角，論文同樣沒有討論。"
  anchor_type: 部落格推論
  qualifiers:
  - text: blog 也提出一個緩解、但仍有破綻的推論：論文的設計哲學可能是不指望初始化一次到位，靠後面的自我演化迴圈事後修補
    source_quote: "有一個緩解、但仍有破綻的推論（不是論文明講的）：論文的設計哲學可能是不指望初始化一次到位，靠後面的自我演化迴圈事後修補。"
  importance: 2
  status: normal
- id: c10
  role: evaluation
  text: 論文的實質缺口：所有 baseline 與 ablation 比的，都是「workload-driven 機制內部拿掉某個步驟」，沒有任何一組實驗拿 schema-driven 的冷啟動來對照
  source_quotes:
  - "論文的實質缺口是：所有 baseline 與 ablation（消融實驗：逐一拿掉系統的某個部分，看分數掉多少）比的，都是「workload-driven 機制內部拿掉某個步驟」，**沒有任何一組實驗拿 schema-driven 的冷啟動來對照**。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c11
  role: evaluation
  text: blog 比較兩種冷啟動：workload-driven（論文做法）的候選概念來自查詢裡反覆出現的字眼，天生對齊真實使用場景、不會生出用不到的概念，但 workload 沒覆蓋到的查詢模式，系統天生沒有對應概念，適合 workload 有代表性時；schema-driven（直接給資料庫 schema、範例查詢與領域知識）覆蓋率完整，但容易生出從沒被用過的概念，多層 join 關係依然不會自動解決，適合 workload 稀疏或已有現成 schema 文件時；兩者也可混用
  source_quotes:
  - "Workload-driven（論文做法） | Schema-driven（替代做法：直接給資料庫 schema、範例查詢與領域知識）"
  - "候選概念從哪來 | 查詢裡反覆出現的字眼 | 資料庫結構本身，加上既有文件與 DBA（資料庫管理員）的知識"
  - "優點 | 天生對齊真實使用場景，不會生出用不到的概念 | 覆蓋率完整，不會漏掉 workload 沒問到、但系統確實存在的欄位或概念"
  - "缺點 | workload 沒覆蓋到的查詢模式，系統天生沒有對應概念 | 容易生出從沒被用過的概念；多層 join 關係依然不會自動解決"
  - "適用時機 | workload 有代表性、覆蓋主要查詢類型 | workload 稀疏，或已有現成 schema 文件；兩者也可混用"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c12
  role: evaluation
  text: Profit 這種沒有實體欄位、是算式推導出來的概念，冷啟動時怎麼被 verify，論文完全沒交代
  source_quotes:
  - "但像 Profit 這種沒有實體欄位、是算式推導出來的概念，怎麼被 verify，論文完全沒交代。"
  anchor_type: 部落格判斷
  importance: 4
  status: normal
- id: c13
  role: evidence
  text: 演化跑了幾輪因 backbone、因 benchmark 而不同，不是固定的超參數：DDR-Bench 跑 0 到 5 輪、InsightBench 跑 0 到 3 輪、BIRD 跑 0 到 4 輪，而且不同 backbone 停在不同輪次
  source_quotes:
  - "圖 4 顯示 DDR-Bench 跑 0 到 5 輪、InsightBench 跑 0 到 3 輪、BIRD 跑 0 到 4 輪，而且不同 backbone 停在不同輪次。"
  - "所以論文有報告輪數，但**因 backbone、因 benchmark 而不同，不是固定的超參數**。"
  anchor_type: 實驗結果
  numeric_kind: non_comparative
  numeric_reason: 計數
  qualifiers:
  - text: 論文沒有在正式的實驗設定段落明講演化了幾輪之後拿最終版本去評分，這個資訊散落在 Analyses 章節裡
    source_quote: "論文沒有在正式的實驗設定段落明講「演化了 N 輪之後拿最終版本去評分」，但這個資訊散落在 Analyses 章節裡。"
  importance: 3
  status: normal
- id: c14
  role: evaluation
  text: 至於什麼時候停，論文說曲線在最後兩輪打平（failure signature 變少），卻沒有明講這是不是明確的停止規則，還是研究者看趨勢打平就不繼續跑了
  source_quotes:
  - "至於什麼時候停，論文說曲線在最後兩輪「flatten（打平）」，原文是 *\"the trajectories flatten by the last two rounds, which is consistent with the failure signatures becoming rarer\"*，卻沒有明講這是不是明確的停止規則（例如連續 N 次沒有候選通過就停），還是研究者看趨勢打平就不繼續跑了。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c15
  role: evaluation
  text: blog 列出方法論沒交代清楚、而且是「這套系統真的能不能落地跑」的核心工程細節：冷啟動與演化迴圈用的是同一批查詢還是再切分過；同一輪抓出多個訊號時處理順序怎麼決定；被拒絕候選的日誌怎麼影響之後的修補；演化的停止規則是什麼
  source_quotes:
  - "這些不是枝微末節，而是「這套系統真的能不能落地跑」的核心工程細節："
  - "冷啟動與演化迴圈用的是同一批查詢，還是再切分過。"
  - "同一輪抓出多個訊號時，處理順序怎麼決定。"
  - "被拒絕候選的日誌，怎麼影響之後的修補。"
  - "演化的停止規則是什麼。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c16
  role: evaluation
  text: blog 的整體評價是研究貢獻中等偏低：核心骨架（結構化知識層、從失敗軌跡歸因、驗證閘門）與同類的「agent 自我演化知識庫或技能庫」論文在架構精神上同構，不是原創突破
  source_quotes:
  - "整體來看，研究貢獻中等偏低。核心骨架（結構化知識層、從失敗軌跡歸因、驗證閘門）與同類的「agent 自我演化知識庫或技能庫」論文"
  - "在架構精神上同構，不是原創突破。"
  anchor_type: 部落格判斷
  importance: 4
  status: normal
```
