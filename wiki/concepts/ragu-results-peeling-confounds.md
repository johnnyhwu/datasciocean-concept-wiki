---
id: ragu-results-peeling-confounds
title: 把混淆變因一層層剝掉後，RAGU 對 HippoRAG 2 是追平或落後；整套 GraphRAG 相對於同程式、同 prompt、不用圖的 NaiveRAG，淨貢獻只有 1.2 到 4.3 pp；cross-over 主要是對手掉下去
type_hint: 發現
context_type: bound_to_source
sources:
- article: ragu
  article_title: "RAGU：一篇替 GraphRAG 量出天花板的論文"
  url: https://datasciocean.com/paper-intro/ragu/
  sections:
  - 前言
  - GraphRAG 在解什麼問題
  - 方法：六個步驟，原創的只有一格
  - 實驗：把混淆變因一層層剝掉
  - 第一層：答案格式
  - 第二層：NaiveRAG 才是照妖鏡
  - 第三層：所謂的 cross-over 是誰在動
  - 觀念三：檢索指標好，不等於答案好
  - 值得帶走的五件事
  - 結論
  first_appearance: true
parent: null
related:
  - retrieval-recall-not-answer-quality
  - entity-resolution-not-clustering
  - graph-vs-vector-clustering-modularity
  - small-extractor-saturation-not-scale
  - ragu-pipeline-two-stage-extraction-consolidation
  - multihop-vector-vs-graphrag-pain-points
  - sag-results-and-gain-source
  - decisionrag-results-gain-source
  - jevact-results-gain-source
  - clm-results-tight-budget-not-across-the-board
  - baseline-who-built-it
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 把 RAGU 的實驗混淆變因一層層剝掉之後，扣掉答案格式，RAGU 對 HippoRAG 2 是追平或落後、沒有任何一項贏；整套 GraphRAG 相對於純向量檢索（NaiveRAG）的淨貢獻只有 1.2 到 4.3 pp；最漂亮的 cross-over 敘事拆開來看，主要是對手掉下去，不是它爬上來
  source_quotes:
  - "扣掉格式後 RAGU 是追平或落後，沒有任何一項贏"
  - "整套 GraphRAG——兩階段抽取、DBSCAN consolidation、Leiden 分群、社群摘要——相對於純向量檢索的淨貢獻，就是這 1.2 到 4.3 pp。"
  - "最漂亮的 cross-over 敘事拆開來看主要是對手掉下去，不是它爬上來"
  comparison_target: 扣掉格式後（terse 設定的 AC）比 HippoRAG 2；淨貢獻比的是 NaiveRAG（同一套程式、同一個 generation prompt，但完全不用圖）
  qualifiers:
  - text: 「沒有任何一項贏」指的是扣掉格式之後 terse 設定下的 AC 對照（BioASQ、2Wiki、MuSiQue）
    source_quote: "扣掉格式之後，RAGU 對 HippoRAG 2 的真實對照（terse 設定下的 AC）是這樣："
  - text: 在 GraphRAG-Bench Medical 最難的 Creative Generation 層級，RAGU 以 59.0 對 56.9 贏 HippoRAG 2，blog 說這 2.1 pp 落在 LLM-judge 的雜訊範圍內
    source_quote: "何況最後那格贏的是 59.0 對 56.9，2.1 pp，落在 LLM-judge 的雜訊範圍內。"
  - text: AC 是單一 judge 模型的單次評分，論文沒有 error bar、也沒有人工驗證 judge 準確度，blog 提醒個位數 pp 的差距不宜當結論
    source_quote: "AC 是單一 judge 模型的單次評分，論文沒有 error bar、也沒有人工驗證 judge 準確度，個位數 pp 的差距不宜當結論。"
  - text: 淨貢獻是用 RAGU 自己的程式、自己的 prompt 做的對照
    source_quote: "用它自己的程式、自己的 prompt 做對照，整套圖的淨貢獻只有 1.2 到 4.3 pp"
  - text: cross-over 是在 GraphRAG-Bench Medical 的四個難度層級上比的 AC，都用 Meno-Lite-0.1（RAGU 附帶的抽取模型）建圖
    source_quote: "GraphRAG-Bench Medical 上四個難度層級的 AC（都用 Meno-Lite-0.1 建圖）："
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: RAGU 是 ITMO University 團隊在 2026 年 7 月放上 arXiv 的 GraphRAG 引擎；論文的主張是把知識圖的「抽取」跟「整併」拆成兩個階段，圖會更乾淨，檢索也會更完整
  source_quotes:
  - "RAGU 是 ITMO University 團隊在 2026 年 7 月[放上 arXiv](https://arxiv.org/abs/2607.11683)的 GraphRAG 引擎"
  - "論文的主張是：把知識圖的「抽取」跟「整併」拆成兩個階段，圖會更乾淨，檢索也會更完整。"
  anchor_type: 原作者解讀
  numeric_kind: non_comparative
  numeric_reason: 日期
  importance: 2
  status: normal
- id: c3
  role: context
  text: 標準的 RAG 把文件切成 chunk、轉成向量，提問時撈出最相似的幾塊，這種檢索是扁平的，看不到跨文件的關聯；GraphRAG 的解法是先請 LLM 把文件裡的實體（人、組織、產品）跟關係抽出來建成知識圖，檢索時可以沿著圖上的邊走，代表系統有 Microsoft GraphRAG、LightRAG 跟 HippoRAG 2
  source_quotes:
  - "標準的 RAG 做法是把文件切成 chunk、轉成向量存起來，使用者提問時撈出最相似的幾塊塞進 prompt。這種檢索是扁平的：每個 chunk 各自獨立，系統看不到跨文件的關聯。"
  - "GraphRAG 的解法是先請 LLM 把文件裡的實體（人、組織、產品）跟關係抽出來建成知識圖，檢索時可以沿著圖上的邊走。這條路線上的代表系統是 Microsoft GraphRAG、LightRAG 跟 HippoRAG 2。"
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 3
  status: normal
- id: c4
  role: context
  text: 實驗用四個 benchmark（GraphRAG-Bench Medical、BioASQ、MuSiQue、2WikiMultiHopQA），所有系統用同一個生成模型 gpt-4o-mini，只變建圖端的 LLM，評分用 gemini-3-flash-preview 當 judge；其中 AC（Answer Correctness）指標由 LLM-judge 判斷答案語意上對不對
  source_quotes:
  - "實驗設定本身是乾淨的：四個 benchmark（GraphRAG-Bench Medical、BioASQ、MuSiQue、2WikiMultiHopQA），所有系統用同一個生成模型 gpt-4o-mini，只變建圖端的 LLM，這樣才隔離得出建圖品質；評分用 gemini-3-flash-preview 當 judge，避免自己評自己。"
  - "AC | Answer Correctness | 答案語意上對不對（LLM-judge）"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 4
  status: normal
- id: c5
  role: qualifier
  text: AC 是單一 judge 模型的單次評分，論文沒有 error bar、也沒有人工驗證 judge 準確度，blog 認為個位數 pp 的差距不宜當結論
  source_quotes:
  - "AC 是單一 judge 模型的單次評分，論文沒有 error bar、也沒有人工驗證 judge 準確度，個位數 pp 的差距不宜當結論。"
  anchor_type: 部落格判斷
  importance: 5
  status: normal
- id: c6
  role: anchor
  text: 第一層混淆是答案格式（論文自己承認）：多跳 QA 的標準答案是短答案，RAGU 預設吐長答案，HippoRAG 2 預設吐短答案；同一套檢索、只把 generation prompt 從 verbose 改成 terse，AC 在 BioASQ 從 56.0 到 72.9（+16.9 pp），2Wiki 從 46.6 到 58.0（+11.4 pp），MuSiQue 從 43.5 到 40.1（−3.4 pp）
  source_quotes:
  - "這一層是論文自己承認的，值得肯定。多跳 QA 的標準答案是短答案（「Bell Laboratories」），RAGU 預設吐長答案，HippoRAG 2 預設吐短答案。"
  - "同一套檢索、只改 generation prompt 的效果："
  - "Benchmark | verbose AC | terse AC | 只改 prompt 的增益"
  - "BioASQ | 56.0 | 72.9 | +16.9 pp（百分點）"
  - "2Wiki | 46.6 | 58.0 | +11.4 pp"
  - "MuSiQue | 43.5 | 40.1 | −3.4 pp"
  comparison_target: 同一套檢索下的 verbose generation prompt
  qualifiers:
  - text: AC 是單一 judge 模型的單次評分，論文沒有 error bar、也沒有人工驗證 judge 準確度，blog 提醒個位數 pp 的差距不宜當結論
    source_quote: "AC 是單一 judge 模型的單次評分，論文沒有 error bar、也沒有人工驗證 judge 準確度，個位數 pp 的差距不宜當結論。"
  anchor_type: 實驗結果
  importance: 6
  status: normal
- id: c7
  role: evaluation
  text: blog 認為 BioASQ 的 +16.9 pp 是「換個 prompt」買來的，比論文任何一項方法貢獻都大
  source_quotes:
  - "+16.9 pp 是「換個 prompt」買來的，比論文任何一項方法貢獻都大。"
  comparison_target: 論文任何一項方法貢獻
  anchor_type: 部落格判斷
  importance: 7
  status: normal
- id: c8
  role: evidence
  text: 扣掉格式之後，terse 設定下的 AC，RAGU 對 HippoRAG 2 在 BioASQ 是 72.9 對 72.4（+0.5 pp，打平），2Wiki 是 58.0 對 63.5（−5.5 pp），MuSiQue 是 40.1 對 54.4（−14.3 pp）
  source_quotes:
  - "扣掉格式之後，RAGU 對 HippoRAG 2 的真實對照（terse 設定下的 AC）是這樣："
  - "Benchmark | RAGU | HippoRAG 2 | 差距"
  - "BioASQ | 72.9 | 72.4 | +0.5 pp（打平）"
  - "2Wiki | 58.0 | 63.5 | −5.5 pp"
  - "MuSiQue | 40.1 | 54.4 | −14.3 pp"
  comparison_target: HippoRAG 2（terse 設定下的 AC）
  qualifiers:
  - text: AC 是單一 judge 模型的單次評分，論文沒有 error bar、也沒有人工驗證 judge 準確度，blog 提醒個位數 pp 的差距不宜當結論
    source_quote: "AC 是單一 judge 模型的單次評分，論文沒有 error bar、也沒有人工驗證 judge 準確度，個位數 pp 的差距不宜當結論。"
  anchor_type: 實驗結果
  importance: 8
  status: normal
- id: c9
  role: evaluation
  text: 論文說這是「互補的強項而非全面壓制」，blog 認為這個說法站得住，但要注意扣掉格式後 RAGU 是追平或落後，沒有任何一項贏
  source_quotes:
  - "論文說這是「互補的強項而非全面壓制」，這個說法站得住——但要注意，扣掉格式後 RAGU 是追平或落後，沒有任何一項贏。"
  qualifiers:
  - text: 「沒有任何一項贏」指的是扣掉格式之後 terse 設定下的 AC 對照（BioASQ、2Wiki、MuSiQue）
    source_quote: "扣掉格式之後，RAGU 對 HippoRAG 2 的真實對照（terse 設定下的 AC）是這樣："
  - text: 在 GraphRAG-Bench Medical 最難的 Creative Generation 層級，RAGU 以 59.0 對 56.9 贏 HippoRAG 2，blog 說這 2.1 pp 落在 LLM-judge 的雜訊範圍內
    source_quote: "何況最後那格贏的是 59.0 對 56.9，2.1 pp，落在 LLM-judge 的雜訊範圍內。"
  anchor_type: 部落格判斷
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: NaiveRAG 就是 RAGU 自己的 NaiveSearchEngine——同一套程式、同一個 generation prompt，但完全不用圖；blog 認為「RAGU vs NaiveRAG」是全篇唯一乾淨的「圖到底有沒有用」對照，而論文正文一個字都沒分析
  source_quotes:
  - "這是同一張表裡最重要、但論文正文一個字都沒分析的對照。"
  - "NaiveRAG 就是 RAGU 自己的 `NaiveSearchEngine`——同一套程式、同一個 generation prompt，但完全不用圖。所以「RAGU vs NaiveRAG」是全篇唯一乾淨的「圖到底有沒有用」對照："
  anchor_type: 部落格判斷
  importance: 10
  status: normal
- id: c11
  role: anchor
  text: terse 設定下的 AC，NaiveRAG（不用圖）對 RAGU（用圖）在 BioASQ 是 71.7 對 72.9（圖的淨貢獻 +1.2 pp），2Wiki 是 53.7 對 58.0（+4.3 pp），MuSiQue 是 36.6 對 40.1（+3.5 pp）
  source_quotes:
  - "Benchmark（terse, AC） | NaiveRAG（不用圖） | RAGU（用圖） | 圖的淨貢獻"
  - "BioASQ | 71.7 | 72.9 | +1.2 pp"
  - "2Wiki | 53.7 | 58.0 | +4.3 pp"
  - "MuSiQue | 36.6 | 40.1 | +3.5 pp"
  comparison_target: NaiveRAG（RAGU 自己的 NaiveSearchEngine，同程式、同 generation prompt、不用圖）
  qualifiers:
  - text: AC 是單一 judge 模型的單次評分，論文沒有 error bar、也沒有人工驗證 judge 準確度，blog 提醒個位數 pp 的差距不宜當結論
    source_quote: "AC 是單一 judge 模型的單次評分，論文沒有 error bar、也沒有人工驗證 judge 準確度，個位數 pp 的差距不宜當結論。"
  anchor_type: 實驗結果
  importance: 11
  status: normal
- id: c12
  role: evidence
  text: 成本對比：建圖要跑一遍 LLM 抽取（論文估約 8k tokens/doc）、embedding、分群、社群摘要；NaiveRAG 只要切 chunk 加 embedding
  source_quotes:
  - "對比一下成本：建圖要跑一遍 LLM 抽取（論文估約 8k tokens/doc）、embedding、分群、社群摘要；NaiveRAG 只要切 chunk 加 embedding。"
  comparison_target: NaiveRAG（只要切 chunk 加 embedding）
  qualifiers:
  - text: 約 8k tokens/doc 是論文的估計，拿建圖跟 NaiveRAG 比成本是 blog 的對照
    source_quote: "對比一下成本：建圖要跑一遍 LLM 抽取（論文估約 8k tokens/doc）"
  anchor_type: 部落格考證
  importance: 12
  status: normal
- id: c13
  role: evidence
  text: 論文的 cross-over 敘事：在 GraphRAG-Bench Medical 的四個難度層級（Fact Retrieval、Complex Reasoning、Contextual Summarize、Creative Generation），RAGU 對 HippoRAG 2 的 AC 差距從 −18.2 單調收斂到 +2.1，論文說這是「越難越強」的證據
  source_quotes:
  - "論文最漂亮的敘事是 cross-over：任務越難，RAGU 越強，最後反超 HippoRAG 2。"
  - "GraphRAG-Bench Medical 上四個難度層級的 AC（都用 Meno-Lite-0.1 建圖）："
  - "任務 | LightRAG | HippoRAG 2 | RAGU"
  - "Fact Retrieval | 26.2 | 72.4 | 54.2"
  - "Complex Reasoning | 20.2 | 68.4 | 53.7"
  - "Contextual Summarize | 22.6 | 65.0 | 64.1"
  - "Creative Generation | 14.4 | 56.9 | 59.0"
  - "論文說 gap 從 −18.2 單調收斂到 +2.1，是「越難越強」的證據。"
  comparison_target: HippoRAG 2（同一難度層級的 AC）
  qualifiers:
  - text: 這四個難度層級的 AC 都用 Meno-Lite-0.1（RAGU 附帶的 7B 抽取模型）建圖
    source_quote: "GraphRAG-Bench Medical 上四個難度層級的 AC（都用 Meno-Lite-0.1 建圖）："
  anchor_type: 原作者解讀
  importance: 13
  status: normal
  figures:
  - file: figures/ragu/figure3.png
    article: ragu
    src: figure3.png
    caption: 圖四 — 依任務複雜度呈現的 cross-over。(a) 是 Answer Correctness，(b) 是 Evidence Recall。（來源：原始論文 Figure 3）
    sha256: bc2a410d1ff16f1acd80d16f5563cd590c6c40f4f5a5943f445c5d860f8d83a7
- id: c14
  role: evaluation
  text: blog 拆解這個 cross-over：RAGU 自己那一欄是 54.2 → 53.7 → 64.1 → 59.0，HippoRAG 2 則從 72.4 掉到 56.9、跌了 15.5 pp；所謂 cross-over 主要不是 RAGU 變強，而是 HippoRAG 2 往下掉，blog 認為準確的描述是 RAGU 的表現對任務難度不敏感、HippoRAG 2 敏感，所以在最難的一格被追過
  source_quotes:
  - "但看 RAGU 自己那一欄：54.2 → 53.7 → 64.1 → 59.0"
  - "所謂 cross-over，主要不是 RAGU 變強，而是 HippoRAG 2 從 72.4 掉到 56.9，跌了 15.5 pp。準確的描述應該是：RAGU 的表現對任務難度不敏感，HippoRAG 2 敏感，所以在最難的一格被追過。"
  comparison_target: HippoRAG 2 自己在 Fact Retrieval（72.4）與 Creative Generation（56.9）之間的變化
  qualifiers:
  - text: 這四個難度層級的 AC 都用 Meno-Lite-0.1 建圖
    source_quote: "GraphRAG-Bench Medical 上四個難度層級的 AC（都用 Meno-Lite-0.1 建圖）："
  anchor_type: 部落格考證
  importance: 14
  status: normal
  figures:
  - file: figures/ragu/figure3.png
    article: ragu
    src: figure3.png
    caption: 圖四 — 依任務複雜度呈現的 cross-over。(a) 是 Answer Correctness，(b) 是 Evidence Recall。（來源：原始論文 Figure 3）
    sha256: bc2a410d1ff16f1acd80d16f5563cd590c6c40f4f5a5943f445c5d860f8d83a7
- id: c15
  role: evaluation
  text: blog 認為「在難任務上更強」跟「在難任務上比較不會退步」是兩件事，論文的敘事把後者說成了前者；而且最難那格贏的是 59.0 對 56.9，2.1 pp，落在 LLM-judge 的雜訊範圍內
  source_quotes:
  - "「在難任務上更強」跟「在難任務上比較不會退步」是兩件事，論文的敘事把後者說成了前者。何況最後那格贏的是 59.0 對 56.9，2.1 pp，落在 LLM-judge 的雜訊範圍內。"
  comparison_target: HippoRAG 2（Creative Generation 的 AC）
  anchor_type: 部落格判斷
  importance: 15
  status: normal
- id: c16
  role: evaluation
  text: blog 把這篇當成一組讀論文檢查動作的示範，三個動作全部命中：找「乾淨對照」（誰跟誰只差一個變因），這裡找到 NaiveRAG；查「宣告了卻沒報的指標」，這裡是論文列為使用指標、卻在所有表格與圖裡都沒有數值的 Context Relevancy；查「核心賣點有沒有 ablation」，這裡論文的核心賣點 consolidation（Step 3，論文唯一的原創步驟 Deduplication & Summarization）沒有
  source_quotes:
  - "**五、一組讀論文的檢查動作。** 這篇論文三個動作全部命中，是判斷成色最快的方式：找「乾淨對照」（誰跟誰只差一個變因），這裡找到了 NaiveRAG；查「宣告了卻沒報的指標」，這裡是消失的 Context Relevancy；查「核心賣點有沒有 ablation」，這裡 consolidation 沒有。"
  - "論文列出使用的指標時包含了 Context Relevancy"
  - "但它在所有表格與圖裡全部沒有出現，全篇沒有任何一個數值"
  - "Step 3  Deduplication & Summarization  ★ 這篇唯一的原創處"
  - "**論文從頭到尾沒有做「有 Step 3 vs 沒 Step 3」的 ablation**。附錄的組態實驗只測了 ICL（in-context learning，要不要在 prompt 裡放範例）、validation、抽取模型大小三個開關，唯獨沒測它自己的核心賣點。所以 consolidation 究竟帶來多少 gain"
  anchor_type: 部落格判斷
  importance: 16
  status: normal
- id: c17
  role: evaluation
  text: blog 從格式這一層帶走混淆變因的量級感：在做任何檢索改動的評估之前，先問有沒有一個更無聊的變因（prompt、答案格式、chunk 大小、baseline 設定）在解釋這個差異
  source_quotes:
  - "**二、混淆變因的量級感。**"
  - "在做任何檢索改動的評估之前，先問：有沒有一個更無聊的變因（prompt、答案格式、chunk 大小、baseline 設定）在解釋這個差異？"
  anchor_type: 部落格判斷
  importance: 17
  status: normal
- id: c18
  role: evaluation
  text: blog 認為 RAGU 無意間量化了 GraphRAG 的天花板，而且這種「不要做什麼」的負面結果很少有人願意發表；對任何正在評估要不要導入 GraphRAG 的人來說，比論文想證明的東西有用得多
  source_quotes:
  - "真正值得記住的，是它無意間量化了 GraphRAG 的天花板"
  - "知道「不要做什麼」跟知道「要做什麼」一樣值錢，而且這種數字很少有人願意發表。"
  - "這對任何正在評估要不要導入 GraphRAG 的人來說，比論文想證明的東西有用得多。"
  qualifiers:
  - text: 這個天花板是用 RAGU 自己的程式、自己的 prompt 做對照量出來的
    source_quote: "用它自己的程式、自己的 prompt 做對照，整套圖的淨貢獻只有 1.2 到 4.3 pp"
  anchor_type: 部落格判斷
  importance: 18
  status: normal
```
