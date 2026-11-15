---
id: small-extractor-saturation-not-scale
title: 「pipeline 裡讀懂並搬運資訊的元件，小模型通常夠用」可以接受，但理由是任務簡單、落在 scaling 的飽和區，不是規模無效；RAGU 的「7B 就夠了」假說證據有灌水，也是為既定決定補的事後理由
type_hint: 判斷
context_type: bound_to_source
sources:
- article: ragu
  article_title: "RAGU：一篇替 GraphRAG 量出天花板的論文"
  url: https://datasciocean.com/paper-intro/ragu/
  sections:
  - 前言
  - GraphRAG 在解什麼問題
  - 「7B 就夠了」這個假說，還有它的問題
  - 真正該有的說法：任務落在飽和區
  - 為什麼論文非要這個假說不可
  - 實驗：把混淆變因一層層剝掉
  - Meno-Lite-0.1：一個尷尬的結果
  - 結論
  first_appearance: true
parent: null
related:
  - ragu-results-peeling-confounds
  - retrieval-recall-not-answer-quality
  - entity-resolution-not-clustering
  - graph-vs-vector-clustering-modularity
  - ragu-pipeline-two-stage-extraction-consolidation
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: blog 認為實務推論是一樣的——pipeline 內部負責「讀懂並搬運資訊」的元件，小模型通常夠用；但理由是「任務簡單」（任務難度低到落在 scaling 的飽和區），不是「規模無效」；搞錯理由，會把它錯誤地套用到真正需要推理的環節上
  source_quotes:
  - "這個 pipeline 裡的任務難度太低，低到落在 scaling 的飽和區。"
  - "實務推論是一樣的——pipeline 內部負責「讀懂並搬運資訊」的元件，小模型通常夠用。但理由是「任務簡單」，不是「規模無效」。搞錯理由，你會把它錯誤地套用到真正需要推理的環節上。"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: RAGU 是 ITMO University 團隊的 GraphRAG 引擎（先請 LLM 把文件裡的實體跟關係抽出來建成知識圖），附帶一個 7B 的抽取模型 Meno-Lite-0.1，兩者都開源；RAGU 認為現有系統預設要用 GPT-4 等級的模型做抽取，成本太高
  source_quotes:
  - "RAGU 是 ITMO University 團隊在 2026 年 7 月[放上 arXiv](https://arxiv.org/abs/2607.11683)的 GraphRAG 引擎，附帶一個 7B 的抽取模型 Meno-Lite-0.1，兩者都開源"
  - "GraphRAG 的解法是先請 LLM 把文件裡的實體（人、組織、產品）跟關係抽出來建成知識圖"
  - "預設要用 GPT-4 等級的模型做抽取，成本太高"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 2
  status: normal
- id: c3
  role: context
  text: 論文最核心的科學主張是：LLM 在 RAG pipeline 裡做的事——讀懂 context、抽實體、摘要、從 context 生答案——屬於語言能力，而不是世界知識；語言能力隨模型規模成長很慢，世界知識成長很快，所以抽取端用 7B 就夠
  source_quotes:
  - "論文最核心的科學主張是：LLM 在 RAG pipeline 裡做的事——讀懂 context、抽實體、摘要、從 context 生答案——屬於語言能力，而不是世界知識。語言能力隨模型規模成長很慢，世界知識成長很快。所以抽取端用 7B 就夠。"
  anchor_type: 原作者解讀
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 3
  status: normal
- id: c4
  role: anchor
  text: 論文的證據：CheGeKa 是俄語常識問答，沒有 context，純粹考背下來的知識；MultiQ 是多跳問答，所有事實都在 context 裡；論文報的是 0.5B 到 72B 之間，CheGeKa 成長 21.1 倍，MultiQ 只有 4 倍
  source_quotes:
  - "CheGeKa 是俄語常識問答，沒有 context，純粹考背下來的知識；MultiQ 是多跳問答，所有事實都在 context 裡。論文報的數字是 0.5B 到 72B 之間，CheGeKa 成長 21.1 倍，MultiQ 只有 4 倍。"
  comparison_target: 各自在 0.5B 模型上的分數（0.5B 到 72B 的成長倍數）
  qualifiers:
  - text: blog 認為這個倍數比法有灌水成分
    source_quote: "這個比法有灌水成分。"
  - text: blog 認為真正站得住腳的是同一張圖裡的 log-linear 斜率 0.65 對 0.26
    source_quote: "真正站得住腳的是同一張圖裡的 log-linear 斜率 0.65 對 0.26，至少是同一個尺度上的比較。"
  - text: 論文的證據來自 Qwen2.5-Instruct，2024 年的非 reasoning 模型
    source_quote: "論文的證據來自 Qwen2.5-Instruct，2024 年的非 reasoning 模型。"
  - text: 兩個 benchmark 都是俄語
    source_quote: "兩個 benchmark 都是俄語，CheGeKa 更是俄國文化常識題"
  anchor_type: 實驗結果
  importance: 4
  status: normal
  figures:
  - file: figures/ragu/figure1.png
    article: ragu
    src: figure1.png
    caption: 圖一 — 世界知識（CheGeKa）與語言能力（MultiQ）兩類任務隨模型規模的成長差異。（來源：原始論文 Figure 1）
    sha256: dd0a7225e7454d495f901670adf46d12b2233fdc2f80f72c4e6864623905a09d
- id: c5
  role: evaluation
  text: blog 認為這個比法有灌水成分：CheGeKa 在 0.5B 時 F1 幾乎貼地（約 0.015），分母趨近於零，任何成長換算成倍數都會很誇張；MultiQ 起點高（約 0.12），而且大概在 32B 就打到天花板（約 0.57 之後持平），倍數小有一部分是因為它飽和了
  source_quotes:
  - "這個比法有灌水成分。CheGeKa 在 0.5B 時 F1 幾乎貼地（約 0.015），分母趨近於零，任何成長換算成倍數都會很誇張；MultiQ 起點高（約 0.12），而且大概在 32B 就打到天花板（約 0.57 之後持平），倍數小有一部分是因為它飽和了。"
  comparison_target: 0.5B 的起點分數（倍數的分母）
  anchor_type: 部落格考證
  importance: 5
  status: normal
  figures:
  - file: figures/ragu/figure1.png
    article: ragu
    src: figure1.png
    caption: 圖一 — 世界知識（CheGeKa）與語言能力（MultiQ）兩類任務隨模型規模的成長差異。（來源：原始論文 Figure 1）
    sha256: dd0a7225e7454d495f901670adf46d12b2233fdc2f80f72c4e6864623905a09d
- id: c6
  role: evaluation
  text: blog 認為真正站得住腳的是同一張圖裡的 log-linear 斜率 0.65 對 0.26，至少是同一個尺度上的比較；論文卻把「21.1 倍 vs 4 倍」放進 abstract 當主打
  source_quotes:
  - "真正站得住腳的是同一張圖裡的 log-linear 斜率 0.65 對 0.26，至少是同一個尺度上的比較。論文卻把「21.1 倍 vs 4 倍」放進 abstract 當主打。"
  comparison_target: CheGeKa 的斜率 0.65 對 MultiQ 的斜率 0.26
  anchor_type: 部落格判斷
  importance: 6
  status: normal
- id: c7
  role: evaluation
  text: blog 指出的第一個問題：MultiQ 測的是「讀 context 回答問題」，但 pipeline 真正的關鍵動作是抽出結構化的實體與關係，而論文自己的資訊抽取實驗顯示，純 Qwen2.5 家族在抽取上是單調隨規模上升的（7B 0.356 → 14B 0.396 → 32B 0.416）
  source_quotes:
  - "第一，MultiQ 測的是「讀 context 回答問題」，但 pipeline 真正的關鍵動作是抽出結構化的實體與關係——而論文自己的資訊抽取實驗顯示，純 Qwen2.5 家族在抽取上是單調隨規模上升的（7B 0.356 → 14B 0.396 → 32B 0.416）。"
  comparison_target: Qwen2.5 家族 7B、14B、32B 三個規模之間
  anchor_type: 部落格考證
  importance: 7
  status: normal
- id: c8
  role: evaluation
  text: blog 指出的第二個問題：兩個 benchmark 都是俄語，CheGeKa 更是俄國文化常識題，拿來代表「world knowledge」再推論到英語醫療語料，跨度不算小
  source_quotes:
  - "第二，兩個 benchmark 都是俄語，CheGeKa 更是俄國文化常識題，拿來代表「world knowledge」再推論到英語醫療語料，跨度不算小。"
  anchor_type: 部落格判斷
  importance: 8
  status: normal
- id: c9
  role: evaluation
  text: blog 認為「語言能力不隨規模成長」這句話跟現實是矛盾的：現在的 SOTA 模型明顯就是 scaling law 的展現，推理能力隨模型與資料規模一路變強
  source_quotes:
  - "「語言能力不隨規模成長」這句話跟現實是矛盾的。現在的 SOTA 模型明顯就是 scaling law 的展現，推理能力隨模型與資料規模一路變強。"
  anchor_type: 部落格判斷
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: 差別在天花板效應：「把這句話裡的人名抽出來」這種任務的難度分佈集中在容易區，7B 可能已經 85 分、72B 也只有 90 分，本來就沒有空間讓規模發揮；AIME（數學競賽題）、GPQA（研究生等級的科學問答）那種多步推導才有難尾巴，7B 拿 5 分、大模型拿 80 分，規模的效果才看得出來
  source_quotes:
  - "差別在天花板效應。「把這句話裡的人名抽出來」這種任務的難度分佈集中在容易區，7B 可能已經 85 分、72B 也只有 90 分，本來就沒有空間讓規模發揮；AIME（數學競賽題）、GPQA（研究生等級的科學問答）那種多步推導才有難尾巴，7B 拿 5 分、大模型拿 80 分，規模的效果才看得出來。"
  comparison_target: 同一類任務上 7B 對 72B（或大模型）的分數（blog 舉的示意數字）
  anchor_type: 部落格舉例
  importance: 10
  status: normal
- id: c11
  role: qualifier
  text: 論文的證據來自 Qwen2.5-Instruct，2024 年的非 reasoning 模型；blog 指出現代推理模型的主要 gain 來自 RL post-training 這條軸線，論文完全沒碰到
  source_quotes:
  - "順帶一提，論文的證據來自 Qwen2.5-Instruct，2024 年的非 reasoning 模型。現代推理模型的主要 gain 來自 RL post-training 這條軸線，論文完全沒碰到。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 日期
  importance: 11
  status: normal
- id: c12
  role: evaluation
  text: blog 認為論文非要這個假說不可，是因為沒有這個假說，Meno-Lite-0.1 就不是研究貢獻，只是省錢；abstract 裡那句 "A key insight motivates a compact extractor" 是為一個先有的決定補上事後的理論理由；這個判讀角度在讀其他 system paper 時也用得上
  source_quotes:
  - "這點值得單獨講，因為判讀其他 system paper 時也用得上：**沒有這個假說，Meno-Lite-0.1 就不是研究貢獻，只是省錢**。"
  - "abstract 裡那句 \"A key insight motivates a compact extractor\" 就是在做這件事：為一個先有的決定補上事後的理論理由。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: blog 認為這個假說同時撐起了成本敘事（只有在「小模型不犧牲品質」成立時才有說服力），並且在 Meno-Lite-0.1 的優勢消失時，提供一個把壞消息改寫成好消息的角度
  source_quotes:
  - "它同時還撐起了成本敘事（\\$0.001/doc vs \\$0.10/doc，只有在「小模型不犧牲品質」成立時才有說服力），並且在後面 Meno-Lite-0.1 的優勢消失時，提供一個把壞消息改寫成好消息的角度。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 13
  status: normal
- id: c14
  role: anchor
  text: 單獨測資訊抽取，7B 的 Meno-Lite-0.1 確實贏過 32B：HM（NER、Def、RE、RDef 四項的調和平均）是 0.468 對 Qwen2.5-32B 的 0.416，相對高出 12.5%，主要靠關係抽取（RE，F1）那一欄的 0.347 對 0.239
  source_quotes:
  - "單獨測資訊抽取，7B 的 Meno-Lite-0.1 確實贏過 32B："
  - "Meno-Lite-0.1 | 7B | 0.504 | 0.527 | **0.347** | 0.558 | **0.468**"
  - "Qwen2.5-32B | 32B | 0.536 | 0.528 | 0.239 | 0.599 | 0.416"
  - "欄位的意思是：NER 是實體辨識（F1）、RE 是關係抽取（F1）、Def 與 RDef 分別是實體與關係的描述生成品質（chrF++）、HM 是前四項的調和平均。整體 HM 相對高出 12.5%，主要靠關係抽取那一欄（0.347 對 0.239）。"
  comparison_target: Qwen2.5-32B
  qualifiers:
  - text: 表上 Qwen2.5-32B 的 NER、Def、RDef 分別是 0.536、0.528、0.599，三欄都高於 Meno-Lite-0.1 的 0.504、0.527、0.558；Meno-Lite-0.1 只在 RE 與 HM 領先
    source_quote: "Qwen2.5-32B | 32B | 0.536 | 0.528 | 0.239 | 0.599 | 0.416"
  - text: Meno-Lite-0.1 的微調用了 NEREL 的 train/validation split，而 IE benchmark 用的是 held-out test split；論文說重疊僅限於標註 schema 跟文本領域，但殘留優勢無法完全排除（論文在 Limitations 自己承認）
    source_quote: "還有一個 caveat 是論文自己在 Limitations 承認的：Meno-Lite-0.1 的微調用了 NEREL 的 train/validation split，而 IE benchmark 用的是 held-out test split。論文說重疊僅限於標註 schema 跟文本領域，但殘留優勢無法完全排除。"
  anchor_type: 實驗結果
  importance: 14
  status: normal
- id: c15
  role: anchor
  text: 這個優勢接到 end-to-end 就消失了：論文自己寫，Meno-Lite-0.1 巨大的單獨抽取優勢，到了 GraphRAG-Bench 的端到端問答上壓縮到 1 pp 以內；附錄的組態表更直接，3B 到 14B 的抽取模型換來換去，最終 AC（LLM-judge 判斷的答案正確度）只差 1.5 pp 以內
  source_quotes:
  - "問題是這個優勢接到 end-to-end 就消失了。論文自己寫：Meno-Lite-0.1 巨大的單獨抽取優勢，到了 GraphRAG-Bench 的端到端問答上壓縮到 1 pp 以內。附錄的組態表更直接——3B 到 14B 的抽取模型換來換去，最終 AC 只差 1.5 pp 以內。"
  - "AC | Answer Correctness | 答案語意上對不對（LLM-judge）"
  comparison_target: 其他抽取模型（端到端）；3B 到 14B 不同大小的抽取模型彼此之間
  qualifiers:
  - text: AC 是單一 judge 模型的單次評分，論文沒有 error bar、也沒有人工驗證 judge 準確度，blog 提醒個位數 pp 的差距不宜當結論
    source_quote: "AC 是單一 judge 模型的單次評分，論文沒有 error bar、也沒有人工驗證 judge 準確度，個位數 pp 的差距不宜當結論。"
  anchor_type: 實驗結果
  importance: 15
  status: normal
- id: c16
  role: evaluation
  text: blog 認為同一份證據既證明了「小模型夠用」，也證明了「抽取模型換誰都差不多」，連帶讓 Meno-Lite-0.1 本身的存在意義變薄；論文把它重新框架成 pipeline 的 robustness
  source_quotes:
  - "同一份證據既證明了「小模型夠用」，也證明了「抽取模型換誰都差不多」，連帶讓 Meno-Lite-0.1 本身的存在意義變薄。論文把它重新框架成 pipeline 的 robustness。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 16
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

- F1：precision（精確率，判為正確的結果中真的正確的比例）與 recall（召回率，所有正確答案中被找出來的比例）的調和平均。
- scaling law：模型表現隨參數量、資料量、計算量增加而改善的經驗規律。
- NER：named entity recognition，實體辨識。
- pp：percentage point，百分點。
- SOTA：state of the art，目前最先進的模型或方法。
