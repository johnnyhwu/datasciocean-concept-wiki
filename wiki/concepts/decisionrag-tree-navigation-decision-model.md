---
id: decisionrag-tree-navigation-decision-model
title: 檢索器漏掉的，生成模型再強也救不回來；DecisionRAG 讓決策模型沿著語料樹一層層出是非題剪枝、最後出一題決選題，全程不生成 token，但最佳成績都出自混入向量檢索的混合版
type_hint: 方法
context_type: bound_to_source
sources:
- article: decision-rag
  article_title: "DecisionRAG：讓決策模型沿著語料樹找資料，準確度追平 GPT-5 重排、快一個數量級"
  url: https://datasciocean.com/paper-intro/decision-rag/
  sections:
  - RAG 裡最跟不上的一環，是檢索器
  - 檢索器漏掉的，生成模型再強也救不回來
  - 現有補救做法，各自卡在一處
  - DecisionRAG 怎麼找資料：沿著語料樹一層層出題
  - 先建一棵樹，再一層層往下篩
  - 是非題：讀一次 context，同時回答每個候選
  - 決選題：最後一步只排第一名
  - 走一遍：Nolan 這題在三個階段各看到什麼
  - 剪錯就救不回來，所以留了兩個後門
  - 語料樹從哪來
  - 準確度：和 GPT-5 重排大約打平，混合版小勝
  - 主表：真正的對手是 GPT-5 重排
  - 拿來用之前要知道的限制
  - notepad 的段落是直接進段落層嗎？
  - 同一棵樹上，判斷比逐字生成快得多
  - 重點回顧：DecisionRAG 換掉了什麼、證明了什麼
  - 同一個 context 放越多候選，判斷會變差嗎？
  first_appearance: true
parent: null
related:
  - shared-context-batched-judgments
  - tree-routing-bounded-by-node-descriptions
  - decisionrag-results-gain-source
  - decisionrag-speedup-deployment-fairness
  - rag-planner-single-round-vs-agentic
  - universalrag-router-design-and-rollout
  - jevmem-small-scorer-controls-memory
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 檢索器漏掉的段落，生成答案的 LLM 再強也看不到；DecisionRAG 的做法是乾脆不讓檢索器先篩：把語料整理成一棵樹，從上往下每一層都由一個模型判斷哪些分支值得往下翻，而且全程不生成任何 token
  source_quotes:
  - "檢索器漏掉的段落，LLM 再強也看不到。DecisionRAG 的做法是乾脆不讓檢索器先篩：把語料整理成一棵樹，從上往下每一層都由一個模型判斷哪些分支值得往下翻，而且全程不生成任何 token。"
  anchor_type: 原作者解讀
  qualifiers:
  - text: 「最佳成績都出自混合版」只就主表而言：同一棵樹上的比較裡，CQA 的 GPT-5 生成式導航 Hit@1 是 73.8
    source_quote: "| CQA：GPT-5 生成式 | 73.8 | 73.6 | 28.2 | 6.1 |"
  - text: 同一組比較裡 CQA 的混合版 Hit@1 是 73.4
    source_quote: "| CQA：DecisionRAG + dense | 73.4 | 76.3 | 0.85 | 0.29 |"
  - text: 四個資料集的最佳成績，其實都出自「混入向量檢索候選」的混合版，blog 認為論文標榜的「retriever-free」（無檢索器）名不符實
    source_quote: "四個資料集的最佳成績，其實都出自「混入向量檢索候選」的混合版，論文標榜的「retriever-free」（無檢索器）名不符實。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: DecisionRAG 是 Cornell 與 ASAPP 的論文（arXiv，2026/10）；它用的模型論文稱為決策模型：不逐字寫出答案，而是直接對每個選項給出機率，問它「這頁值不值得翻？」，它回的是 yes 的機率而不是一段文字；論文用的是 Jev 1.13
  source_quotes:
  - "論文：[DecisionRAG（arXiv 2610.35868v1）](https://arxiv.org/abs/2610.35868v1)（Cornell、ASAPP，2026/10）"
  - "這個模型論文稱為決策模型：它不逐字寫出答案，而是直接對每個選項給出機率。問它「這頁值不值得翻？」，它回的是 yes 的機率，而不是一段文字。論文用的 [Jev 1.13](../../ai-concept/jev-overview/) 是供應商的線上服務"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  qualifiers:
  - text: Jev 1.13 是供應商的線上服務，只能透過 API 使用，模型大小未公開
    source_quote: "是供應商的線上服務，只能透過 API 使用，模型大小未公開。"
  importance: 2
  status: normal
- id: c3
  role: context
  text: 論文把問題稱為能力不對稱（capability asymmetry）：在 RAG 裡，決定生成模型能看到什麼的是檢索器，而檢索器遠比生成模型笨；檢索器漏掉的證據，生成模型再強也救不回來。生成答案的 LLM 越換越強，檢索器卻還是 BM25（比對字面關鍵字）或向量檢索
  source_quotes:
  - "在 RAG 裡，決定生成模型能看到什麼的是檢索器，而檢索器遠比生成模型笨。檢索器漏掉的證據，生成模型再強也救不回來。論文把這叫做能力不對稱（capability asymmetry）。"
  - "生成答案的 LLM 越換越強，負責決定「它能看到什麼」的檢索器卻還是 BM25（比對字面關鍵字的傳統做法）或向量檢索"
  anchor_type: 原作者解讀
  importance: 2
  status: normal
  figures:
  - file: figures/decision-rag/figure1.png
    article: decision-rag
    src: figure1.png
    caption: 圖 1 — 能力不對稱：簡單的檢索器成為強大 LLM 的瓶頸（a），改用決策模型做檢索讓兩邊能力拉平（b）（來源：原始論文 Figure 1。）
    sha256: 3d739120820b662ceade676edab63ef7d9634f89e90f6aaec1a7d72870512faf
- id: c4
  role: anchor
  text: 例子：「Christopher Nolan 2000 年那部電影的主角是誰？」要先推出 Nolan 的 2000 年作品是 Memento，才知道該去 Memento 頁面找介紹主角的段落，但「Memento」這個詞根本不在查詢裡；BM25 只比字面，會把標題剛好含「2000」和「film」的 Gladiator (2000 film) 排在 Memento 前面；向量檢索把查詢和段落分開轉成向量再比對，同樣沒有機會在讀過查詢之後做「先推出 Memento」這一步推理
  source_quotes:
  - "「Christopher Nolan 2000 年那部電影的主角是誰？」要答這題，得先推出「Nolan 的 2000 年作品是 Memento」，才知道該去 Memento 頁面找介紹主角 Leonard Shelby 的段落。麻煩的是，「Memento」這個詞根本不在查詢裡。"
  - "BM25 只比字面，會把標題剛好含「2000」和「film」的 Gladiator (2000 film) 排在 Memento 前面。"
  - "Dense retrieval（向量檢索）把查詢和段落分開轉成向量再比對，同樣沒有機會在讀過查詢之後做「先推出 Memento」這一步推理。"
  anchor_type: 原作者解讀
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 3
  status: normal
  figures:
  - file: figures/decision-rag/figure2.png
    article: decision-rag
    src: figure2.png
    caption: 圖 2 — 靠比對檢索與靠決策檢索的對照。(a) 的 BM25 分數只是示意（來源：原始論文 Figure 2。）
    sha256: bd0fad70db54bb3d88d67aff07e225fdfd799c665b85e56d90eea95b2bd41c13
- id: c5
  role: mechanism
  text: 現有的補救做法大致有兩條路：重排序讓強模型參與判斷，但它只能在第一階段撈回來的候選裡排，漏掉的找不回來；生成式導航讓 LLM 自己逐步搜尋，或沿著文件階層逐字寫出要保留的分支，找得回來，但每一步都要等模型寫字，很慢
  source_quotes:
  - "現有的補救做法大致有兩條路。重排序讓強模型參與判斷，但它只能在第一階段撈回來的候選裡排，漏掉的找不回來。生成式導航則讓 LLM 自己逐步搜尋，或沿著文件階層逐字寫出要保留的分支；找得回來，但每一步都要等模型寫字，很慢。"
  anchor_type: 背景說明
  importance: 4
  status: normal
- id: c6
  role: mechanism
  text: 從現有做法的對照可以整理出三個挑戰：不依賴第一階段檢索器（強模型要直接決定「看什麼」，而不只是重排別人挑好的）；不能逐字生成（每一步判斷都要快）；規模（語料可達數百萬段，不可能讓模型逐段讀過）
  source_quotes:
  - "從這張表可以整理出三個挑戰："
  - "不依賴第一階段檢索器：強模型要直接決定「看什麼」，而不只是重排別人挑好的。"
  - "不能逐字生成：每一步判斷都要快。"
  - "規模：語料可達數百萬段，不可能讓模型逐段讀過。"
  anchor_type: 原作者解讀
  importance: 4
  status: normal
- id: c7
  role: mechanism
  text: 離線只建一次：把語料整理成「分群 → 頁面 → 段落」這類階層樹，每個節點配一段短描述；上線時每個查詢都走一遍，決策模型在三個地方出題：前兩個是是非題（上層節點篩選、段落篩選），最後一個是決選題（排第一名）
  source_quotes:
  - "離線（只建一次）：把語料整理成「分群 → 頁面 → 段落」這類階層樹，每個節點配一段短描述"
  - "上線（每個查詢都走一遍）：審查員在三個地方出題。前兩個是是非題（上層節點篩選、段落篩選），最後一個是決選題（排第一名）。"
  anchor_type: 設計參數
  qualifiers:
  - text: 查詢時不需要第一階段檢索器的是純導航版
    source_quote: "純導航版查詢時也不需要第一階段檢索器"
  - text: 用了 dense 候選就需要事先建好向量索引，系統不再是「無檢索器」
    source_quote: "用了它就需要事先建好向量索引，系統不再是「無檢索器」"
  - text: 查詢時不需要向量檢索，但建樹時可能會用 embedding 來分群
    source_quote: "查詢時不需要向量檢索，但建樹時可能會用 embedding（把文字轉成的向量）來分群。"
  importance: 2
  status: normal
- id: c8
  role: mechanism
  text: 是非題：每個候選各自一題 yes／no，所有題目共用同一個 context（使用者問題加上所有候選的描述），並在一次 forward pass（不逐字生成）裡全部答完；每題的機率只在自己的 yes 和 no 之間分配，所以跨題加總不必是 1；因為每題獨立，候選數只受 context 長度限制，一層太大時就拆成多個平行請求，最後合併分數排序
  source_quotes:
  - "每個候選各自一題 yes／no，所有題目共用同一個 context（模型這一次讀進去的全部輸入，在這裡是使用者問題加上所有候選的描述），並在一次 forward pass（模型把輸入從頭算到尾、直接得出輸出，不逐字生成）裡全部答完。"
  - "每題的機率只在自己的 yes 和 no 之間分配，所以跨題加總不必是 1。"
  - "因為每題獨立，候選數只受 context 長度限制；一層太大時就拆成多個平行請求，最後合併分數排序。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 3
  status: normal
  figures:
  - file: figures/decision-rag/figure3.png
    article: decision-rag
    src: figure3.png
    caption: 圖 3 — 決策模型的兩種判斷方式，都在同一個只讀一次的共享 context 上進行：(a) 平行是非題，(b) 多選一重排（來源：原始論文 Figure 3。）
    sha256: 891de29e5a721da98e3765b88156c2680cb490e855673d908bef3ded60244e6b
- id: c9
  role: mechanism
  text: 每一層由是非題對所有候選打分，只留前幾名（例如固定前 k 名，或過某個機率門檻），到段落層留前 r 段；每個階段都重新組一個 context（使用者問題加上編號的候選描述），上一階段的分數不會帶進下一階段的輸入
  source_quotes:
  - "只留前幾名（例如固定前 \\( k \\) 名，或過某個機率門檻）；到段落層留前 \\( r \\) 段"
  - "每個階段都重新組一個 context：「使用者問題 + 編號的候選描述（依所屬頁面分組、按閱讀順序）」，後面接題目。上一階段的分數不會帶進下一階段的輸入（論文 Appendix B.1）。"
  anchor_type: 設計參數
  qualifiers:
  - text: 論文只測了排序；P(Yes) 的絕對值能不能拿來對門檻值，沒有被驗證過
    source_quote: "每題 yes／no 的絕對正確率論文沒測，只測了排序。"
  - text: blog 在限制裡也列出沒驗證「P(Yes) 絕對值能不能拿來對門檻」
    source_quote: "沒驗證的有候選在 context 內的順序偏差、\\( P(\\text{Yes}) \\) 絕對值能不能拿來對門檻"
  importance: 4
  status: normal
- id: c10
  role: mechanism
  text: 決選題只在最後一步：對前 m 段只出一題「哪一段最相關？」，所有候選搶同一份機率、加起來剛好是 1；是非題的目標是召回（不要漏），決選題的目標是第一名排對；決選題最多 255 個選項（Jev 的限制），實際設定是 m = 20（Natural Questions 為 5），前 m 名照決選機率重排，其餘維持是非題的排序
  source_quotes:
  - "到了最後，對前 \\( m \\) 段只出一題「哪一段最相關？」。這次不是每段各自回答 yes／no，而是所有候選搶同一份機率，加起來剛好是 1"
  - "| 目標 | 召回：不要漏 | 第一名排對 |"
  - "| 候選上限 | 只受 context 長度限制 | 最多 255 個選項（Jev 的限制） |"
  - "實際設定是 \\( m = 20 \\)（Natural Questions 為 5）。前 \\( m \\) 名照決選機率重排，其餘維持是非題的排序。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  qualifiers:
  - text: MTRAG 資料集比較特別，只把決選第一名提到最前面，原因論文未說明
    source_quote: "MTRAG 資料集比較特別，只把決選第一名提到最前面，原因論文未說明。"
  importance: 3
  status: normal
  figures:
  - file: figures/decision-rag/figure3.png
    article: decision-rag
    src: figure3.png
    caption: 圖 3 — 決策模型的兩種判斷方式，都在同一個只讀一次的共享 context 上進行：(a) 平行是非題，(b) 多選一重排（來源：原始論文 Figure 3。）
    sha256: 891de29e5a721da98e3765b88156c2680cb490e855673d908bef3ded60244e6b
- id: c11
  role: mechanism
  text: 剪枝（把分數低的分支剪掉，這個查詢不再往下看）是不可逆的：被剪掉的分支，這個查詢就不會再看了；所以每層的預算刻意放寬，用成本換召回
  source_quotes:
  - "拿來排序和剪枝（把分數低的分支剪掉，這個查詢不再往下看）。"
  - "剪枝是不可逆的：被剪掉的分支，這個查詢就不會再看了。所以每層的預算刻意放寬，用成本換召回。"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c12
  role: mechanism
  text: 為了補救剪錯，留了兩個可選的後門：dense 候選（另外用向量檢索撈一批段落補進來）和 notepad（多輪對話時記住最近用過的頁面），都把段落直接送回段落層
  source_quotes:
  - "兩個可選的補救後門：dense 候選（另外用向量檢索撈一批段落補進來）和 notepad（多輪對話時記住最近用過的頁面），都把段落直接送回段落層"
  anchor_type: 設計參數
  qualifiers:
  - text: notepad 的段落繞過頁面層、直接進段落層，是在 MultiDoc2Dial 上
    source_quote: "在 MultiDoc2Dial 上，最近 2 個 notepad 頁面的段落會繞過頁面層、直接進段落層。"
  - text: MTRAG 也用 notepad，但它是否也把段落直接加進段落層，論文沒說
    source_quote: "MTRAG 也用 notepad，但它是否也把段落直接加進段落層，論文沒說。"
  importance: 3
  status: normal
- id: c13
  role: mechanism
  text: dense 候選另外用向量檢索撈前 20 段（ConditionalQA 為 10 段），去重後依頁面與章節、按閱讀順序併入段落層；用了它就需要事先建好向量索引，系統不再是「無檢索器」，blog 認為比較準確的說法是「導航為主、向量檢索補漏」的混合版
  source_quotes:
  - "另外用向量檢索撈前 20 段（ConditionalQA 為 10 段），去重後依頁面與章節、按閱讀順序併入段落層。眉角在於：用了它就需要事先建好向量索引，系統不再是「無檢索器」，比較準確的說法是「導航為主、向量檢索補漏」的混合版。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 3
  status: normal
- id: c14
  role: evaluation
  text: blog 認為「retriever-free」名不符實：四個資料集的最佳成績都出自混入向量檢索候選的混合版，而混合版需要事先建好的向量索引
  source_quotes:
  - "「retriever-free」名不符實：四個資料集的最佳成績都出自混入向量檢索候選的混合版，它需要事先建好的向量索引"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 「最佳成績都出自混合版」只就主表而言：同一棵樹上的比較裡，CQA 的 GPT-5 生成式導航 Hit@1 是 73.8
    source_quote: "| CQA：GPT-5 生成式 | 73.8 | 73.6 | 28.2 | 6.1 |"
  - text: 同一組比較裡 CQA 的混合版 Hit@1 是 73.4
    source_quote: "| CQA：DecisionRAG + dense | 73.4 | 76.3 | 0.85 | 0.29 |"
  - text: 這裡的「最佳成績」指主表（沒有針對任務訓練過的各種方法、各資料集的主指標）；ConditionalQA 上混合版與「Dense 前 20 + GPT-5 重排」同為 73.4，是並列
    source_quote: "主表比的是沒有針對任務訓練過的各種方法。"
  - text: ConditionalQA 的並列，主表兩列的數字
    source_quote: "| Dense 前 20 + GPT-5 重排 | 47.5 | 73.4 | 31.8 | 60.8 |"
  - text: 混合版那一列
    source_quote: "| DecisionRAG + dense 候選 | 48.5 | 73.4 | 36.6 | 66.4 |"
  importance: 2
  status: normal
- id: c15
  role: mechanism
  text: notepad 只用在多輪對話資料集：它記錄最近幾個對話輪中排第一的段落所在頁面；在 MultiDoc2Dial 上，最近 2 個 notepad 頁面的段落會繞過頁面層、直接進段落層；後門保證段落「能被看到」，不保證「會被選上」，之後還得擠進前 m 名才進得了決選題
  source_quotes:
  - "notepad 只用在多輪對話資料集：它記錄最近幾個對話輪中排第一的段落所在頁面。在 MultiDoc2Dial 上，最近 2 個 notepad 頁面的段落會繞過頁面層、直接進段落層。"
  - "段落加入的是段落層的是非題，之後還得擠進前 \\( m \\) 名才進得了決選題。後門保證「能被看到」，不保證「會被選上」。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 計數
  qualifiers:
  - text: MTRAG 也用 notepad，但它是否也把段落直接加進段落層，論文沒說
    source_quote: "MTRAG 也用 notepad，但它是否也把段落直接加進段落層，論文沒說。"
  importance: 5
  status: normal
- id: c16
  role: evidence
  text: 結果是準確度和最強的「向量檢索 + GPT-5 重排序」大約打平（重排序：先讓檢索器撈一批候選，再交給更強的模型重新排名次），混合版小勝
  source_quotes:
  - "結果是準確度和最強的「向量檢索 + GPT-5 重排序」大約打平（重排序：先讓檢索器撈一批候選，再交給更強的模型重新排名次）"
  - "準確度和最強的「向量檢索 + GPT-5 重排」大約打平，混合版小勝"
  - "以及讓 GPT-5 重排向量檢索的前 20 段"
  anchor_type: 實驗結果
  comparison_target: 「Dense 前 20 + GPT-5 重排」（向量檢索撈前 20 段，再讓 GPT-5 重排）
  qualifiers:
  - text: 混合版對 GPT-5 重排的差距是 +1.0、0、+4.8、+5.6（MD2D、CQA、MTRAG、NQ），CQA 上是並列
    source_quote: "混合版是 +1.0、0、+4.8、+5.6。"
  - text: 「最佳成績都出自混合版」只就主表而言：同一棵樹上的比較裡，CQA 的 GPT-5 生成式導航 Hit@1 是 73.8
    source_quote: "| CQA：GPT-5 生成式 | 73.8 | 73.6 | 28.2 | 6.1 |"
  - text: 同一組比較裡 CQA 的混合版 Hit@1 是 73.4
    source_quote: "| CQA：DecisionRAG + dense | 73.4 | 76.3 | 0.85 | 0.29 |"
  - text: 混合版指混入向量檢索候選的版本，最佳成績都出自它
    source_quote: "四個資料集的最佳成績，其實都出自「混入向量檢索候選」的混合版"
  importance: 3
  status: normal
```
