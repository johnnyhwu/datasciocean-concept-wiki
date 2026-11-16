---
id: decisionrag-results-gain-source
title: DecisionRAG 真正的對手是 GPT-5 重排，和它大約打平、混合版小勝；提升有一大塊來自 Jev 本身，沿樹導航只在兩個資料集有額外貢獻，而且贏在排得準、不在找得全
type_hint: 發現
context_type: bound_to_source
sources:
- article: decision-rag
  article_title: "DecisionRAG：讓決策模型沿著語料樹找資料，準確度追平 GPT-5 重排、快一個數量級"
  url: https://datasciocean.com/paper-intro/decision-rag/
  sections:
  - RAG 裡最跟不上的一環，是檢索器
  - 檢索器漏掉的，生成模型再強也救不回來
  - 先建一棵樹，再一層層往下篩
  - 讀表前要知道的資料集與指標
  - 主表：真正的對手是 GPT-5 重排
  - 提升來自沿樹導航，還是來自 Jev？
  - 拿來用之前要知道的限制
  - 重點回顧：DecisionRAG 換掉了什麼、證明了什麼
  - 同一棵樹上，判斷比逐字生成快得多
  first_appearance: true
parent: null
related:
  - decisionrag-tree-navigation-decision-model
  - decisionrag-speedup-deployment-fairness
  - ragu-results-peeling-confounds
  - verifier-results-how-to-read
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: DecisionRAG 和 GPT-5 重排大約打平，混合版小勝；光是讓 Jev 直接重排向量檢索的結果，就已經勝過專用 reranker（這是模型本身還是打分方式的功勞，論文沒拆開）；沿樹導航的額外貢獻只在 CQA 和 NQ 上看得到，而且贏在排序，不在召回
  source_quotes:
  - "DecisionRAG 和 GPT-5 重排大約打平，混合版小勝。光是讓 Jev 直接重排向量檢索的結果，就已經勝過專用 reranker（NQ 差 11.4 點、CQA 只差 1.1 點；這是模型本身還是打分方式的功勞，論文沒拆開）；沿樹導航的額外貢獻只在 CQA 和 NQ 上看得到，而且贏在排序，不在召回。"
  - "以及讓 GPT-5 重排向量檢索的前 20 段"
  - "| Hit@1（%） | Dense 前 100 + Qwen3-Reranker | Dense 前 100 + Jev 重排 | DecisionRAG + dense 候選 |"
  anchor_type: 部落格判斷
  comparison_target: 打平與小勝是對「Dense 前 20 + GPT-5 重排」；Jev 重排勝過的專用 reranker 是 Qwen3-Reranker-8B
  qualifiers:
  - text: 「最佳成績都出自混合版」只就主表而言：同一棵樹上的比較裡，CQA 的 GPT-5 生成式導航 Hit@1 是 73.8
    source_quote: "| CQA：GPT-5 生成式 | 73.8 | 73.6 | 28.2 | 6.1 |"
  - text: 同一組比較裡 CQA 的混合版 Hit@1 是 73.4
    source_quote: "| CQA：DecisionRAG + dense | 73.4 | 76.3 | 0.85 | 0.29 |"
  - text: CQA、NQ 上導航的額外貢獻（+7.7、+7.0）是混入向量檢索候選的版本（DecisionRAG + dense 候選）對「Dense 前 100 + Jev 重排」，不是純導航版
    source_quote: "| Hit@1（%） | Dense 前 100 + Qwen3-Reranker | Dense 前 100 + Jev 重排 | DecisionRAG + dense 候選 |"
  - text: 勝過專用 reranker 的幅度看資料：NQ 差 11.4 點，CQA 只差 1.1 點
    source_quote: "NQ 差 11.4 點、CQA 只差 1.1 點"
  - text: 四個資料集的最佳成績都出自混入向量檢索候選的混合版，blog 認為論文標榜的「retriever-free」名不符實
    source_quote: "四個資料集的最佳成績，其實都出自「混入向量檢索候選」的混合版，論文標榜的「retriever-free」（無檢索器）名不符實。"
  - text: 混合版對 GPT-5 重排的差距是 +1.0、0、+4.8、+5.6（MD2D、CQA、MTRAG、NQ），CQA 上是並列
    source_quote: "混合版是 +1.0、0、+4.8、+5.6。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: DecisionRAG 把語料整理成一棵樹，從上往下每一層都由一個決策模型（不逐字寫出答案，而是直接對每個選項給出機率）判斷哪些分支值得往下翻，全程不生成任何 token；純導航版查詢時不需要第一階段檢索器，混合版另外用向量檢索撈一批段落（dense 候選）補進段落層；論文用的決策模型是 Jev 1.13
  source_quotes:
  - "把語料整理成一棵樹，從上往下每一層都由一個模型判斷哪些分支值得往下翻，而且全程不生成任何 token。"
  - "這個模型論文稱為決策模型：它不逐字寫出答案，而是直接對每個選項給出機率。"
  - "dense 候選（另外用向量檢索撈一批段落補進來）"
  - "純導航版查詢時也不需要第一階段檢索器"
  - "論文用的 [Jev 1.13](../../ai-concept/jev-overview/) 是供應商的線上服務"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  qualifiers:
  - text: Jev 1.13 只能透過 API 使用，模型大小未公開
    source_quote: "只能透過 API 使用，模型大小未公開。"
  importance: 2
  status: normal
- id: c3
  role: context
  text: 論文在四個資料集上測：MultiDoc2Dial（MD2D，美國政府說明中心的多輪客服對話）、ConditionalQA（CQA，英國政府指南的情境題）、MTRAG（IBM Cloud 技術文件的多輪對話）、Natural Questions（NQ，真實搜尋問題，答案在 Wikipedia）；主指標是 MD2D 看 R@1、CQA 看 Hit@1、MTRAG 看 R@5、NQ 看 Hit@1。R@k 是正確段落中有幾成出現在前 k 名（有沒有找回來），Hit@1 是第一名剛好是正確段落之一的題目比例（第一名排對沒有）
  source_quotes:
  - "論文在四個資料集上測，涵蓋客服對話、政府指南、技術文件和 Wikipedia："
  - "| MultiDoc2Dial（MD2D） | 美國政府說明中心的多輪客服對話 |"
  - "| ConditionalQA（CQA） | 英國政府指南的情境題 |"
  - "| MTRAG | IBM Cloud 技術文件的多輪對話 |"
  - "| Natural Questions（NQ） | 真實搜尋問題，答案在 Wikipedia |"
  - "各資料集的主指標：MD2D 看 R@1、CQA 看 Hit@1、MTRAG 看 R@5、NQ 看 Hit@1。"
  - "R@k（Recall@k）：正確段落中有幾成出現在前 \\( k \\) 名，衡量「有沒有找回來」。"
  - "Hit@1：第一名剛好是正確段落之一的題目比例，衡量「第一名排對沒有」"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 3
  status: normal
- id: c4
  role: qualifier
  text: MTRAG 的數字要打折看：它的正確答案有一部分是 GPT-5 補標的，而 GPT-5 同時也是被比較的 baseline
  source_quotes:
  - "MTRAG 的正確答案有一部分是 GPT-5 補標的，而 GPT-5 同時也是被比較的 baseline（論文 Appendix A.3）。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 3
  status: normal
- id: c5
  role: evidence
  text: 主表（沒有針對任務訓練過的各種方法，各資料集主指標）裡真正的對手是「向量檢索前 20 + GPT-5 重排」：DecisionRAG 純導航版對它的差距依序是 −0.1、−3.7、+2.4、+4.6（MD2D、CQA、MTRAG、NQ），大約打平；混合版是 +1.0、0、+4.8、+5.6
  source_quotes:
  - "主表比的是沒有針對任務訓練過的各種方法。"
  - "| 方法 | MD2D R@1 | CQA Hit@1 | MTRAG R@5 | NQ Hit@1 |"
  - "以及讓 GPT-5 重排向量檢索的前 20 段"
  - "| Dense 前 20 + GPT-5 重排 | 47.5 | 73.4 | 31.8 | 60.8 |"
  - "真正的對手是 GPT-5 重排。純導航版對它的差距依序是 −0.1、−3.7、+2.4、+4.6，大約打平；混合版是 +1.0、0、+4.8、+5.6。"
  anchor_type: 實驗結果
  comparison_target: 「Dense 前 20 + GPT-5 重排」（MD2D 47.5、CQA 73.4、MTRAG 31.8、NQ 60.8）
  qualifiers:
  - text: MTRAG 的正確答案有一部分是 GPT-5 補標的，而 GPT-5 同時也是被比較的 baseline
    source_quote: "MTRAG 的正確答案有一部分是 GPT-5 補標的，而 GPT-5 同時也是被比較的 baseline（論文 Appendix A.3）。"
  importance: 2
  status: normal
- id: c6
  role: evaluation
  text: 論文摘要的數字挑了對手：摘要寫的「NQ Hit@1 +17.4」是對 Qwen3-Reranker 比；對同表最強的傳統做法（BGE 重排的 54.8）只有 +10.6
  source_quotes:
  - "論文摘要的數字挑了對手。摘要寫的「NQ Hit@1 +17.4」是對 Qwen3-Reranker 比；對同表最強的傳統做法（BGE 54.8）只有 +10.6。"
  anchor_type: 部落格考證
  comparison_target: 「Dense 前 100 + Qwen3-Reranker-8B」（NQ 48.0）與「Dense 前 100 + BGE 重排」（NQ 54.8）
  importance: 2
  status: normal
- id: c7
  role: evaluation
  text: NQ 上 BM25 的 Hit@1 只有 16.4，DecisionRAG 是 65.4，正好量化了能力不對稱（檢索器遠比生成模型笨）；但 BM25 不是 DecisionRAG 真正的對手，拿它來比只會放大提升幅度，要判斷這個方法值不值得用，該對照的是最強的「Dense + GPT-5 重排」
  source_quotes:
  - "至於 BM25 那一列，它正好量化了開頭說的能力不對稱：NQ 上 BM25 的 Hit@1 只有 16.4，DecisionRAG 是 65.4"
  - "不過 BM25 不是 DecisionRAG 真正的對手，拿它來比只會放大提升幅度。要判斷這個方法值不值得用，該對照的是最強的「Dense + GPT-5 重排」。"
  - "在 RAG 裡，決定生成模型能看到什麼的是檢索器，而檢索器遠比生成模型笨。"
  anchor_type: 部落格判斷
  comparison_target: BM25（NQ Hit@1 16.4）
  importance: 3
  status: normal
- id: c8
  role: context
  text: 為了分辨贏的是「沿著樹走」還是 Jev 這個模型本身，論文 6.5 節讓 Jev 直接重排向量檢索的前 100 段，打分方式和 DecisionRAG 最後一步完全相同，兩邊只差在「候選從哪來」
  source_quotes:
  - "贏的是「沿著樹走」這個做法，還是 Jev 這個模型本身？論文 6.5 節讓 Jev 直接重排向量檢索的前 100 段，打分方式和 DecisionRAG 最後一步完全相同，兩邊只差在「候選從哪來」。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 2
  status: normal
- id: c9
  role: evidence
  text: Hit@1（%）：CQA（271 題）上「Dense 前 100 + Qwen3-Reranker」64.6、「Dense 前 100 + Jev 重排」65.7（+1.1）、「DecisionRAG + dense 候選」73.4（再 +7.7，95% CI [2.6, 13.3]）；NQ（500 題）上依序 48.0、59.4（+11.4）、66.4（再 +7.0，95% CI [3.4, 10.8]）
  source_quotes:
  - "括號內是相對左邊一欄的差距"
  - "| Hit@1（%） | Dense 前 100 + Qwen3-Reranker | Dense 前 100 + Jev 重排 | DecisionRAG + dense 候選 |"
  - "| CQA（271 題） | 64.6 | 65.7（+1.1） | 73.4（+7.7，95% CI [2.6, 13.3]） |"
  - "| NQ（500 題） | 48.0 | 59.4（+11.4） | 66.4（+7.0，95% CI [3.4, 10.8]） |"
  anchor_type: 實驗結果
  comparison_target: 括號內的差距都是相對左邊一欄：Jev 重排對 Qwen3-Reranker，DecisionRAG + dense 候選對 Jev 重排
  importance: 2
  status: normal
- id: c10
  role: evidence
  text: 另外兩個資料集上，導航和 Jev 重排持平，兩邊的差距都不到 1.5 點（MD2D 1,000 輪抽樣上兩者的 R@1 是 49.9 和 51.2，MTRAG 只用官方原始標註時兩者的 R@5 是 38.3 和 38.7）；也就是說，四個資料集裡有兩個，導航本身沒有額外貢獻
  source_quotes:
  - "另外兩個資料集上，導航和 Jev 重排持平，也就是說，四個資料集裡有兩個，導航本身沒有額外貢獻。兩邊的差距都不到 1.5 點：MD2D（1,000 輪抽樣）上兩者的 R@1 分別是 49.9 和 51.2，MTRAG（只用官方原始標註）上兩者的 R@5 分別是 38.3 和 38.7"
  anchor_type: 實驗結果
  comparison_target: 同一資料集上「Dense 前 100 + Jev 重排」與 DecisionRAG 互相比較
  qualifiers:
  - text: blog 的資料來源沒有標明這兩組數字哪個屬於哪個方法
    source_quote: "不過本文的資料來源沒有標明哪個數字屬於哪個方法。"
  - text: 這兩組的評估範圍和主表不同，不能和主表的數字直接比
    source_quote: "這兩組的評估範圍和主表不同，所以不能和主表的數字直接比。"
  importance: 3
  status: normal
- id: c11
  role: evaluation
  text: 觀察一：Jev 重排勝過 Qwen3-Reranker。blog 認為這打破的不是「檢索之後要重排」，而是「重排就該用專門訓練的 reranker」；但兩者有兩個差別論文沒有拆開：一是模型本身（通用決策模型 vs 專用 8B reranker），二是打分方式（100 段放進同一個 context 一起判斷再加決選題 vs 每對問題與段落各自打分）
  source_quotes:
  - "觀察一：Jev 重排勝過 Qwen3-Reranker。這打破的不是「檢索之後要重排」，而是「重排就該用專門訓練的 reranker」。兩者其實有兩個差別，論文沒有拆開：一是模型本身（[通用決策模型](../jevact/) vs 專用 8B reranker），二是打分方式（100 段放進同一個 context 一起判斷再加決選題 vs 每對問題與段落各自打分）。"
  - "論文 6.5 節讓 Jev 直接重排向量檢索的前 100 段"
  anchor_type: 部落格判斷
  comparison_target: Jev 重排對 Qwen3-Reranker（專用 8B reranker），兩者都重排向量檢索的前 100 段
  qualifiers:
  - text: 幅度也看資料：NQ 差 11.4 點，CQA 只差 1.1 點
    source_quote: "幅度也看資料：NQ 差 11.4 點，CQA 只差 1.1 點。"
  importance: 2
  status: normal
- id: c12
  role: evidence
  text: 觀察二：導航勝在排得準，不是找得全。向量檢索的前 100 名其實更常包含正確段落（NQ 98.4% 對 94.0%；CQA 98.5% 對 91.1%）；但只看兩邊都包含正確段落的題目，導航把它排第一的比例更高（NQ 70.1% 對 61.9%；CQA 76.7% 對 67.3%）
  source_quotes:
  - "觀察二：導航勝在排得準，不是找得全。向量檢索的前 100 名其實更常包含正確段落（NQ 98.4% 對 94.0%；CQA 98.5% 對 91.1%）。但只看兩邊都包含正確段落的題目，導航把它排第一的比例更高（NQ 70.1% 對 61.9%；CQA 76.7% 對 67.3%）。"
  anchor_type: 實驗結果
  comparison_target: 包含率是向量檢索前 100 名對導航（前者較高）；排第一的比例（只看兩邊都包含正確段落的題目）是導航對向量檢索前 100 名（前者較高）
  importance: 2
  status: normal
- id: c13
  role: mechanism
  text: 論文作者推測，導航排得準的原因是導航把整頁段落按閱讀順序交給審查員，向量檢索給的卻是來自不同頁面的零散段落
  source_quotes:
  - "論文作者推測，原因是導航把整頁段落按閱讀順序交給審查員，向量檢索給的卻是來自不同頁面的零散段落；這個解釋沒有經過實驗驗證。"
  anchor_type: 原作者解讀
  qualifiers:
  - text: 這個解釋沒有經過實驗驗證
    source_quote: "這個解釋沒有經過實驗驗證。"
  importance: 3
  status: normal
- id: c14
  role: qualifier
  text: blog 在使用前的限制裡列出：導航不一定有額外貢獻，MD2D 和 MTRAG 上，導航和直接用 Jev 重排持平
  source_quotes:
  - "導航不一定有額外貢獻：MD2D 和 MTRAG 上，導航和直接用 Jev 重排持平"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
```


## 名詞補充（通用知識，非 blog 內容）

以下是很基本的通用詞，blog 沒有解釋，由撰寫者以一般知識補充；它們不是卡上的主張，不能當作 blog 的說法引用。
- **reranker（重排序器）**：檢索器先撈一批候選後，再用另一個模型重新排名次。
- **BM25**：比對字面關鍵字的傳統檢索打分方法。
