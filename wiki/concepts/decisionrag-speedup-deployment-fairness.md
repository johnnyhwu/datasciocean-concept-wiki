---
id: decisionrag-speedup-deployment-fairness
title: DecisionRAG 對 reranker 與 GPT-5 重排的加速，部署條件不對等，只能當參考；同一棵樹上把逐字生成換成判斷那組比較才乾淨：準確度互有勝負，延遲差 34 到 145 倍
type_hint: 判斷
context_type: bound_to_source
sources:
- article: decision-rag
  article_title: "DecisionRAG：讓決策模型沿著語料樹找資料，準確度追平 GPT-5 重排、快一個數量級"
  url: https://datasciocean.com/paper-intro/decision-rag/
  sections:
  - RAG 裡最跟不上的一環，是檢索器
  - 現有補救做法，各自卡在一處
  - 準確度：和 GPT-5 重排大約打平，混合版小勝
  - 延遲與成本：倍數不是公平的加速比
  - 同一棵樹上，判斷比逐字生成快得多
  - 重點回顧：DecisionRAG 換掉了什麼、證明了什麼
  first_appearance: true
parent: null
related:
  - decisionrag-tree-navigation-decision-model
  - decisionrag-results-gain-source
  - shared-context-batched-judgments
  - prompt-repetition-free-lunch-latency
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 和 reranker、GPT-5 重排比的加速，部署條件不對等，只能當參考；同一棵樹上把逐字生成換成判斷的那組比較才乾淨，準確度互有勝負，延遲差 34 到 145 倍
  source_quotes:
  - "和 reranker、GPT-5 重排比的「快一個數量級」，部署條件不對等，只能當參考；同一棵樹上把逐字生成換成判斷的那組比較才乾淨，準確度互有勝負，延遲差 34 到 145 倍。"
  - "論文 6.3 節保持樹和預算不變，只把審查員換成 GPT-5（低推理強度），讓它讀完一層之後逐字寫出要保留的編號"
  anchor_type: 部落格判斷
  comparison_target: 同一棵樹、同樣預算下，改由 GPT-5（低推理強度）逐字寫出要保留編號的生成式導航
  qualifiers:
  - text: 34 到 145 倍是 GPT-5 生成式對 DecisionRAG 純導航版：CQA 上 GPT-5 生成式 28.2 秒
    source_quote: "| CQA：GPT-5 生成式 | 73.8 | 73.6 | 28.2 | 6.1 |"
  - text: CQA 上 DecisionRAG 純導航版 0.82 秒
    source_quote: "| CQA：DecisionRAG | 69.7 | 71.9 | 0.82 | 0.29 |"
  - text: NQ 上 GPT-5 生成式 250.8 秒
    source_quote: "| NQ：GPT-5 生成式 | 59.0 | 82.5 | 250.8 | 57.2 |"
  - text: NQ 上 DecisionRAG 純導航版 1.73 秒
    source_quote: "| NQ：DecisionRAG | 65.0 | 86.5 | 1.73 | 2.33 |"
  - text: 同樹比較的題數：CQA 271 題；NQ 只用前 100 題，也沒有信賴區間
    source_quote: "（CQA 271 題；NQ 只用前 100 題，也沒有信賴區間）"
  importance: 1
  status: normal
- id: c2
  role: context
  text: DecisionRAG 把語料整理成一棵樹，從上往下每一層都由一個決策模型（不逐字寫出答案，而是直接對每個選項給出機率）判斷哪些分支值得往下翻，全程不生成任何 token；論文用的決策模型是 Jev 1.13，是供應商的線上服務，只能透過 API 使用，模型大小未公開
  source_quotes:
  - "把語料整理成一棵樹，從上往下每一層都由一個模型判斷哪些分支值得往下翻，而且全程不生成任何 token。"
  - "這個模型論文稱為決策模型：它不逐字寫出答案，而是直接對每個選項給出機率。"
  - "論文用的 [Jev 1.13](../../ai-concept/jev-overview/) 是供應商的線上服務，只能透過 API 使用，模型大小未公開。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 2
  status: normal
- id: c3
  role: evidence
  text: 延遲（每查詢的中位數秒數，依序 MD2D、CQA、MTRAG、NQ）：「向量檢索 + Qwen3-Reranker」7.5、3.3、14.3、5.8；「向量檢索 + GPT-5 重排」11.8、14.4、12.2、15.0；DecisionRAG 0.68、0.82、1.76、1.73
  source_quotes:
  - "延遲是每查詢的中位數秒數，成本是每查詢的 API 費用（美分）。"
  - "|  | MD2D | CQA | MTRAG | NQ |"
  - "| 延遲：Dense + Qwen3-Reranker | 7.5 | 3.3 | 14.3 | 5.8 |"
  - "| 延遲：Dense + GPT-5 重排 | 11.8 | 14.4 | 12.2 | 15.0 |"
  - "| 延遲：DecisionRAG | 0.68 | 0.82 | 1.76 | 1.73 |"
  anchor_type: 實驗結果
  comparison_target: 「Dense + Qwen3-Reranker」與「Dense + GPT-5 重排」的延遲
  qualifiers:
  - text: DecisionRAG 的計時在四個資料集上只用了 48、50、24、100 個查詢
    source_quote: "DecisionRAG 的計時在四個資料集上只用了 48、50、24、100 個查詢（論文 Table 15）。"
  - text: 這些倍數不能當成公平控制下的加速比，兩邊的部署條件差很多
    source_quote: "這些倍數不能當成公平控制下的加速比，論文 Appendix F 自己也承認，因為兩邊的部署條件差很多："
  importance: 2
  status: normal
- id: c4
  role: evaluation
  text: 這些延遲倍數不能當成公平控制下的加速比（論文 Appendix F 自己也承認），因為兩邊的部署條件差很多：Qwen3-Reranker 那一列是 8B 專用 reranker、單張 RTX A6000 本機執行、100 段分批送進同一張 GPU；DecisionRAG 那一列是大小未公開的 Jev 1.13、供應商線上服務且硬體不明、每查詢最多同時 8 個請求
  source_quotes:
  - "這些倍數不能當成公平控制下的加速比，論文 Appendix F 自己也承認，因為兩邊的部署條件差很多："
  - "| 模型 | 8B 專用 reranker | Jev 1.13，大小未公開 |"
  - "| 硬體 | 單張 RTX A6000，本機執行 | 供應商線上服務，硬體不明 |"
  - "| 平行度 | 100 段分批送進同一張 GPU | 每查詢最多同時 8 個請求 |"
  anchor_type: 部落格判斷
  comparison_target: Qwen3-Reranker 那一列（本機單卡 8B reranker）與 DecisionRAG 那一列的部署條件互相比較
  importance: 2
  status: normal
- id: c5
  role: evaluation
  text: blog 比較保守的結論是：在論文的測試條件下，「Jev API + 沿樹導航」端到端比「本機單卡 8B reranker」和「GPT-5 重排」快一個數量級
  source_quotes:
  - "比較保守的結論是：在論文的測試條件下，「Jev API + 沿樹導航」端到端比「本機單卡 8B reranker」和「GPT-5 重排」快一個數量級"
  anchor_type: 部落格判斷
  comparison_target: 「本機單卡 8B reranker」（Dense + Qwen3-Reranker）與「Dense + GPT-5 重排」
  importance: 3
  status: pending_author_confirmation
- id: c6
  role: qualifier
  text: 至於決策模型這一類模型本身是不是比 reranker 快，這篇沒有證據
  source_quotes:
  - "至於決策模型這一類模型本身是不是比 reranker 快，這篇沒有證據。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c7
  role: mechanism
  text: blog 推論：從結構上看，把所有候選寫進同一個 context，等於把所有段落串成一條長序列，而 attention 計算量隨序列長度平方成長，所以這不一定比 cross-encoder（把問題和一段放在一起、逐對打分的 reranker 架構）省
  source_quotes:
  - "（推論）從結構上看，把所有候選寫進同一個 context，等於把所有段落串成一條長序列。模型裡讓每個 token 回頭看其他 token 的 attention 機制，計算量隨序列長度平方成長，所以這不一定比 cross-encoder（把問題和一段放在一起、逐對打分的 reranker 架構）省。"
  anchor_type: 部落格推論
  importance: 4
  status: normal
- id: c8
  role: evidence
  text: 成本（每查詢 API 費用，美分，依序 MD2D、CQA、MTRAG、NQ）：「向量檢索 + GPT-5 重排」1.40、1.20、1.90、1.40；DecisionRAG 0.22、0.29、1.73、2.33；成本只在小語料上佔優，大語料反而比較貴：NQ 每查詢 2.33 美分，高於 GPT-5 重排的 1.40，因為頁面層要判斷約 17,500 個標題
  source_quotes:
  - "成本是每查詢的 API 費用（美分）"
  - "|  | MD2D | CQA | MTRAG | NQ |"
  - "| 成本：Dense + GPT-5 重排 | 1.40 | 1.20 | 1.90 | 1.40 |"
  - "| 成本：DecisionRAG | 0.22 | 0.29 | 1.73 | 2.33 |"
  - "但成本只在小語料上佔優"
  - "NQ 每查詢 2.33 美分，高於 GPT-5 重排的 1.40，因為頁面層要判斷約 17,500 個標題。"
  anchor_type: 實驗結果
  comparison_target: 「Dense + GPT-5 重排」的每查詢成本
  importance: 2
  status: normal
- id: c9
  role: qualifier
  text: Jev 1.13 只能透過 API 使用，換成自訓模型之後的延遲和成本，論文沒有測
  source_quotes:
  - "另外 Jev 1.13 只能透過 API 使用，換成自訓模型之後的延遲和成本，論文沒有測。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 3
  status: normal
- id: c10
  role: context
  text: 同一棵樹上的比較（論文 6.3 節）：保持樹和預算不變，只把審查員換成 GPT-5（低推理強度），讓它讀完一層之後逐字寫出要保留的編號，也就是生成式導航（每一步都要等模型寫字）；兩邊都走 API，blog 認為這是全篇最乾淨的延遲比較
  source_quotes:
  - "論文 6.3 節保持樹和預算不變，只把審查員換成 GPT-5（低推理強度），讓它讀完一層之後逐字寫出要保留的編號，也就是前面說的生成式導航。兩邊都走 API，這是全篇最乾淨的延遲比較"
  - "生成式導航則讓 LLM 自己逐步搜尋，或沿著文件階層逐字寫出要保留的分支；找得回來，但每一步都要等模型寫字，很慢。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  qualifiers:
  - text: CQA 271 題；NQ 只用前 100 題，也沒有信賴區間
    source_quote: "（CQA 271 題；NQ 只用前 100 題，也沒有信賴區間）"
  importance: 2
  status: normal
- id: c11
  role: evidence
  text: 同樹比較的數字（Hit@1、R@10、延遲秒數、成本美分）：CQA 上 GPT-5 生成式 73.8、73.6、28.2、6.1，DecisionRAG 69.7、71.9、0.82、0.29，DecisionRAG + dense 73.4、76.3、0.85、0.29；NQ 上 GPT-5 生成式 59.0、82.5、250.8、57.2，DecisionRAG 65.0、86.5、1.73、2.33，DecisionRAG + dense 64.0、88.5、1.64、2.33
  source_quotes:
  - "|  | Hit@1 | R@10 | 延遲（秒） | 成本（美分） |"
  - "| CQA：GPT-5 生成式 | 73.8 | 73.6 | 28.2 | 6.1 |"
  - "| CQA：DecisionRAG | 69.7 | 71.9 | 0.82 | 0.29 |"
  - "| CQA：DecisionRAG + dense | 73.4 | 76.3 | 0.85 | 0.29 |"
  - "| NQ：GPT-5 生成式 | 59.0 | 82.5 | 250.8 | 57.2 |"
  - "| NQ：DecisionRAG | 65.0 | 86.5 | 1.73 | 2.33 |"
  - "| NQ：DecisionRAG + dense | 64.0 | 88.5 | 1.64 | 2.33 |"
  anchor_type: 實驗結果
  comparison_target: 同一棵樹上的 GPT-5 生成式導航
  qualifiers:
  - text: CQA 271 題；NQ 只用前 100 題，也沒有信賴區間
    source_quote: "（CQA 271 題；NQ 只用前 100 題，也沒有信賴區間）"
  importance: 3
  status: normal
- id: c12
  role: evidence
  text: 準確度互有勝負（CQA 上 GPT-5 多 4.1，NQ 上 DecisionRAG 多 6.0），但延遲差 34 到 145 倍，成本差 21 到 25 倍
  source_quotes:
  - "準確度互有勝負（CQA 上 GPT-5 多 4.1，NQ 上 DecisionRAG 多 6.0），但延遲差 34 到 145 倍，成本差 21 到 25 倍。"
  - "| CQA：GPT-5 生成式 | 73.8 | 73.6 | 28.2 | 6.1 |"
  - "| NQ：GPT-5 生成式 | 59.0 | 82.5 | 250.8 | 57.2 |"
  anchor_type: 實驗結果
  comparison_target: 同一棵樹上的 GPT-5 生成式導航（CQA 28.2 秒、6.1 美分；NQ 250.8 秒、57.2 美分）
  qualifiers:
  - text: NQ 上 DecisionRAG 純導航版的 Hit@1 65.0、1.73 秒、2.33 美分
    source_quote: "| NQ：DecisionRAG | 65.0 | 86.5 | 1.73 | 2.33 |"
  - text: CQA 上 DecisionRAG 純導航版的 Hit@1 69.7、0.82 秒、0.29 美分
    source_quote: "| CQA：DecisionRAG | 69.7 | 71.9 | 0.82 | 0.29 |"
  - text: CQA 271 題；NQ 只用前 100 題，也沒有信賴區間
    source_quote: "（CQA 271 題；NQ 只用前 100 題，也沒有信賴區間）"
  importance: 2
  status: normal
- id: c13
  role: mechanism
  text: NQ 上 GPT-5 每查詢要超過 4 分鐘：它得先讀完整層，再一個個寫出編號，分群層要選 150 個時還常常需要追問補齊
  source_quotes:
  - "NQ 上 GPT-5 每查詢要超過 4 分鐘：它得先讀完整層，再一個個寫出編號，分群層要選 150 個時還常常需要追問補齊。"
  - "| NQ：DecisionRAG | 65.0 | 86.5 | 1.73 | 2.33 |"
  - "沒有標示的是論文內容；標「（推論）」的是筆記作者的推測"
  anchor_type: 原作者解讀
  comparison_target: 同一查詢下 DecisionRAG 的 1.73 秒
  importance: 4
  status: normal
- id: c14
  role: evaluation
  text: blog 認為同樹比較是全篇最直接支持「決策模型適合做檢索決策」的證據
  source_quotes:
  - "這是全篇最直接支持「決策模型適合做檢索決策」的證據。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c15
  role: evaluation
  text: blog 的建議：看到「無檢索器」「快一個數量級」這類宣稱時，先問最佳成績是不是混了向量檢索、比較的部署條件是否對等
  source_quotes:
  - "看到「無檢索器」「快一個數量級」這類宣稱時，先問最佳成績是不是混了向量檢索、比較的部署條件是否對等"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
```


## 名詞補充（通用知識，非 blog 內容）

以下是很基本的通用詞，blog 沒有解釋，由撰寫者以一般知識補充；它們不是卡上的主張，不能當作 blog 的說法引用。
- **Hit@1**：排第一名的結果剛好是正確答案的題目比例。
- **R@10（Recall@10）**：正確答案中有幾成出現在排序的前 10 名。
- **reranker（重排序器）**：檢索器先撈一批候選後，再用另一個模型重新排名次。
