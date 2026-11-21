---
id: tree-routing-bounded-by-node-descriptions
title: 樹狀導航時，上層只看得到節點的短描述；描述看不出某個分支有答案，那個分支就會被剪掉而且救不回來，所以描述的品質直接決定整個系統的召回上限
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: decision-rag
  article_title: "DecisionRAG：讓決策模型沿著語料樹找資料，準確度追平 GPT-5 重排、快一個數量級"
  url: https://datasciocean.com/paper-intro/decision-rag/
  sections:
  - RAG 裡最跟不上的一環，是檢索器
  - DecisionRAG 怎麼找資料：沿著語料樹一層層出題
  - 先建一棵樹，再一層層往下篩
  - 讀表前要知道的資料集與指標
  - 走一遍：Nolan 這題在三個階段各看到什麼
  - 剪錯就救不回來，所以留了兩個後門
  - 語料樹從哪來
  - 主表：真正的對手是 GPT-5 重排
  - 拿來用之前要知道的限制
  - 樹狀導航的上限，由節點描述決定
  - 重點回顧：DecisionRAG 換掉了什麼、證明了什麼
  first_appearance: true
parent: null
related:
  - decisionrag-tree-navigation-decision-model
  - universalrag-router-design-and-rollout
  - rag-planner-single-round-vs-agentic
  - single-loop-progressive-disclosure
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 上層做決定時，審查員只看得到節點的短描述，看不到底下的內容；描述看不出某個分支有答案，那個分支就會被剪掉，而且救不回來，所以描述的品質直接決定整個系統的召回上限
  source_quotes:
  - "上層做決定時，審查員只看得到節點的短描述，看不到底下的內容。描述看不出某個分支有答案，那個分支就會被剪掉，而且救不回來。所以描述的品質直接決定整個系統的召回上限。"
  anchor_type: 部落格推論
  qualifiers:
  - text: 論文在 Limitations 承認了這點，但沒有量化
    source_quote: "論文在 Limitations 承認了這點，但沒有量化。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: 這個觀念出自 DecisionRAG：它把語料整理成一棵樹，從上往下每一層都由一個模型（論文稱為決策模型，下文稱審查員）判斷哪些分支值得往下翻；離線先把語料整理成「分群 → 頁面 → 段落」這類階層樹，每個節點配一段短描述，上線時審查員在每一層對所有候選各出一題是非題（這個候選值不值得往下看？），只留前幾名
  source_quotes:
  - "把語料整理成一棵樹，從上往下每一層都由一個模型判斷哪些分支值得往下翻"
  - "這個模型論文稱為決策模型"
  - "離線（只建一次）：把語料整理成「分群 → 頁面 → 段落」這類階層樹，每個節點配一段短描述"
  - "決策模型（下文稱「審查員」）在每一層對所有候選各出一題是非題（這個候選值不值得往下看？），只留前幾名"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: mechanism
  text: 剪枝是不可逆的：被剪掉的分支，這個查詢就不會再看了，所以 DecisionRAG 每層的預算刻意放寬，用成本換召回
  source_quotes:
  - "剪枝是不可逆的：被剪掉的分支，這個查詢就不會再看了。所以每層的預算刻意放寬，用成本換召回。"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c4
  role: evidence
  text: 純導航會漏：Natural Questions 的 R@10（正確段落中有幾成出現在前 10 名），DecisionRAG 純導航版是 86.7，低於「向量檢索前 100 + Qwen3-Reranker-8B」的 89.0，blog 認為這就是剪枝不可逆的代價；混入向量檢索候選的混合版補回到 88.9
  source_quotes:
  - "純導航會漏。NQ 的 R@10，純導航是 86.7，低於 Qwen3-Reranker 的 89.0，這就是剪枝不可逆的代價；混合版補回到 88.9。"
  - "R@k（Recall@k）：正確段落中有幾成出現在前 \\( k \\) 名"
  - "Natural Questions（NQ）"
  - "Dense 前 100 + Qwen3-Reranker-8B"
  anchor_type: 實驗結果
  comparison_target: 「Dense 前 100 + Qwen3-Reranker-8B」（向量檢索撈前 100 段，再用 8B 專用 reranker 重排）
  importance: 2
  status: normal
- id: c5
  role: context
  text: 每個節點都要有一段短描述給審查員判斷：段落用內文，頁面用標題（有些資料集再加章節標題），群用一句摘要
  source_quotes:
  - "每個節點都要有一段短描述給審查員判斷：段落用內文，頁面用標題（有些資料集再加章節標題），群用一句摘要。"
  anchor_type: 設計參數
  importance: 3
  status: normal
- id: c6
  role: anchor
  text: 頁面的描述依資料集而定：MD2D 與 MTRAG 用標題加章節標題，CQA 用標題加最上層章節標題，NQ 只用標題；NQ 在頁面層之前還多一層「主題分群」，MD2D 則在頁面層之上多一層「說明中心」
  source_quotes:
  - "頁面的描述依資料集而定：MD2D 與 MTRAG 用標題加章節標題，CQA 用標題加最上層章節標題，NQ 只用標題"
  - "NQ 在階段 ① 之前還多一層「主題分群」，做法相同；MD2D 則在頁面層之上多一層「說明中心」。"
  - "階段 ①：頁面層是非題"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 5
  status: normal
- id: c7
  role: mechanism
  text: 有現成結構就沿用，例如 metadata 欄位、HTML 的 h1／h2、網址路徑；樹不必處處一樣深，MTRAG 只替超過 60 段的長頁多插一層章節
  source_quotes:
  - "有現成結構就沿用，例如 metadata 欄位、HTML 的 h1／h2、網址路徑。樹不必處處一樣深，MTRAG 只替超過 60 段的長頁多插一層章節。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 4
  status: normal
- id: c8
  role: mechanism
  text: 沒有現成結構時（論文在 Wikipedia 上的做法，Appendix A.4、B.5）：每頁取「標題 + 第一句」轉成向量（e5-base-v2）；用 k-means（把向量自動分成指定數量群組的經典演算法）分成 1,000 群；請 LLM（Qwen3-8B）讀每群的頁面標題，寫一句 30 字內的描述
  source_quotes:
  - "沒有現成結構時怎麼建（論文在 Wikipedia 上的做法，Appendix A.4、B.5）："
  - "每頁取「標題 + 第一句」，轉成向量（e5-base-v2）。"
  - "用 k-means（把向量自動分成指定數量群組的經典演算法）分成 1,000 群。"
  - "請 LLM（Qwen3-8B）讀每群的頁面標題，寫一句 30 字內的描述。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  qualifiers:
  - text: 查詢時不需要第一階段檢索器的是純導航版
    source_quote: "純導航版查詢時也不需要第一階段檢索器"
  - text: 用了 dense 候選就需要事先建好向量索引，系統不再是「無檢索器」
    source_quote: "用了它就需要事先建好向量索引，系統不再是「無檢索器」"
  - text: 查詢時不需要向量檢索，但建樹時可能會用 embedding 來分群
    source_quote: "查詢時不需要向量檢索，但建樹時可能會用 embedding（把文字轉成的向量）來分群。"
  importance: 3
  status: normal
- id: c9
  role: mechanism
  text: 群的描述必須點名比較不典型的成員：摘要天生會描述多數成員的主題，少數成員就從描述裡消失了，審查員也就不會為它們保留這一群
  source_quotes:
  - "描述必須點名比較不典型的成員。摘要天生會描述多數成員的主題，少數成員就從描述裡消失了，審查員也就不會為它們保留這一群。"
  anchor_type: 設計參數
  qualifiers:
  - text: 這個 prompt 設計沒有做消融驗證（沒有拿掉這條要求來比較）
    source_quote: "這個 prompt 設計沒有做消融驗證（沒有拿掉這條要求來比較）。"
  importance: 2
  status: normal
- id: c10
  role: qualifier
  text: blog 在使用前的限制裡列出：召回上限受節點描述限制，論文沒有量化
  source_quotes:
  - "召回上限受節點描述限制，論文沒有量化"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c11
  role: evaluation
  text: blog 推論任何「看描述選分支」的路由問題都適用，例如 agent 依工具描述選工具、依 skill 描述選 skill、多 agent 之間分派任務、RAPTOR 的摘要樹、PageIndex 的目錄導航；路由器再強，也受限於它看到的選項描述
  source_quotes:
  - "（推論）任何「看描述選分支」的路由問題都適用，例如 agent 依工具描述選工具、依 skill 描述選 skill、多 agent 之間分派任務、RAPTOR 的摘要樹、PageIndex 的目錄導航。路由器再強，也受限於它看到的選項描述。"
  anchor_type: 部落格推論
  importance: 2
  status: normal
- id: c12
  role: evaluation
  text: blog 的建議：設計任何靠描述選分支的系統（工具、skill、文件樹）時，把力氣花在描述上
  source_quotes:
  - "設計任何靠描述選分支的系統（工具、skill、文件樹）時，把力氣花在描述上。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
```


## 名詞補充（通用知識，非 blog 內容）

以下是很基本的通用詞，blog 沒有解釋，由撰寫者以一般知識補充；它們不是卡上的主張，不能當作 blog 的說法引用。
- **recall（召回率）**：該找回來的東西裡，實際找回了幾成；「召回上限」指系統最多能找回幾成。
