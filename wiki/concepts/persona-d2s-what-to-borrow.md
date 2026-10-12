---
id: persona-d2s-what-to-borrow
title: Persona-Aware-D2S 值得借鑑的是不需要訓練的兩塊：先字面後語意的兩段式章節過濾，和摘要加重排；各有代價，過濾不可逆、重排的證據偏薄
type_hint: 判斷
context_type: evidence_from_single_source
sources:
- article: persona-aware-d2s
  article_title: "拆解 Persona-Aware-D2S：同一份文件，怎麼依受眾和長度長出不同簡報"
  url: https://datasciocean.com/paper-intro/persona-aware-d2s/
  sections:
  - 前言
  - 第一步：高 recall 的章節過濾器（不動用 LLM）
  - 省下的 API 成本，代價是什麼
  - Stage 3：摘要與邏輯重排
  - 工程落地：哪些該抄，哪些別碰
  first_appearance: true
parent: null
related:
  - persona-d2s-task-and-pipeline
  - persona-d2s-training-design-flaws
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: Persona-Aware-D2S 可以直接借鑑的是兩個不需要訓練的部分：Stage 2 第一步的兩段式檢索，以及 Stage 3 的摘要重排，遷移成本接近零；但章節過濾的篩選不可逆，摘要重排的證據樣本偏小、評分者也不是獨立第三方
  source_quotes:
  - 可以直接借鑑：Stage 2 第一步的兩段式檢索，以及 Stage 3 的摘要重排。兩者都不需要訓練，遷移成本接近零。
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  qualifiers:
  - text: 章節過濾這一步的篩選不可逆：被這一步濾掉的句子，後面的 Stage 再也看不到
    source_quote: 關鍵在於這一步的篩選**不可逆**：被這一步濾掉的句子，後面的 Stage 再也看不到。
  - text: 章節過濾的門檻是在只有 5 篇論文的 dev split 上調出來的，樣本數小到換個 domain（章節命名習慣不同）多半得重調
    source_quote: 是在只有 **5 篇論文**的 dev split 上調出來的，樣本數小到換個 domain（章節命名習慣不同）多半得重調。
  - text: 整套章節過濾機制高度依賴文件有標準化的 section 結構，拿去處理非結構化文件，字面比對那一段會直接失效
    source_quote: 整套機制高度依賴文件有標準化的 section 結構；拿去處理會議記錄、PRD 這類非結構化文件，字面比對那一段會直接失效，全部 fallback 到語意比對。
  - text: 摘要重排的消融實驗樣本數只有 10 篇，評分者也不是獨立第三方
    source_quote: 不過樣本數只有 10 篇，評分者也不是獨立第三方。
  importance: 1
  status: normal
- id: c2
  role: context
  text: Persona-Aware-D2S 是三階段 pipeline：大綱生成（Stage 1）→ 內容抽取（Stage 2）→ 摘要與重排（Stage 3）
  source_quotes:
  - 三階段 pipeline（大綱生成 → 內容抽取 → 摘要與重排）
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 2
  status: normal
- id: c3
  role: context
  text: Stage 2 第一步是不動用 LLM 的高 recall 章節過濾器，先用便宜的方式縮小範圍：把整篇論文直接丟給 LLM 挑句子，一來成本高，二來塞不進 GPT-3.5-turbo 的 4096 token 限制
  source_quotes:
  - 為什麼需要這一步？把整篇論文直接丟給 LLM 挑句子，一來成本高，二來塞不進 GPT-3.5-turbo 的 4096 token 限制。所以論文先用便宜的方式縮小範圍
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 3
  status: pending_author_confirmation
- id: c4
  role: mechanism
  text: 兩段式檢索的第一段：每個投影片標題跟論文的 section headings 做 fuzzy match（字面相似度），取相似度超過門檻的 top-k
  source_quotes:
  - 跟論文的 section headings 做 fuzzy match（字面相似度），取相似度超過門檻 … 的 top-k。
  anchor_type: 設計參數
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 兩段式檢索的第二段：如果沒有任何 section 過得了門檻，改用 Sentence-BERT 算語意相似度，挑最接近的 section；選定 section 之後，把該 section 的所有句子與 caption 全部串接起來
  source_quotes:
  - 如果沒有任何 section 過得了門檻，改用 Sentence-BERT（Reimers & Gurevych, 2019）算語意相似度，挑最接近的 section。
  - 選定 section 之後，把該 section 的所有句子與 caption 全部串接成
  anchor_type: 設計參數
  importance: 5
  status: normal
- id: c6
  role: evaluation
  text: 「先用便宜的字面匹配，字面匹配失敗才動用語意模型」的兩段式檢索，是很經典的 retrieve-then-rerank 思路，也是整篇論文裡最值得直接借鑑的設計；成熟、可遷移，確實解決省 API 成本的真實痛點，落地可行性高
  source_quotes:
  - 說白了就是「先用便宜的字面匹配，字面匹配失敗才動用語意模型」的兩段式檢索——很經典的 retrieve-then-rerank 思路，也是整篇論文裡我認為最值得直接借鑑的設計。
  - 成熟、可遷移、確實解決真實痛點（省 API 成本），跟通用 RAG 的 retrieve-then-rerank 思路一致
  anchor_type: 部落格判斷
  qualifiers:
  - text: 章節過濾這一步的篩選不可逆：被這一步濾掉的句子，後面的 Stage 再也看不到
    source_quote: 關鍵在於這一步的篩選**不可逆**：被這一步濾掉的句子，後面的 Stage 再也看不到。
  - text: 章節過濾的門檻是在只有 5 篇論文的 dev split 上調出來的，樣本數小到換個 domain（章節命名習慣不同）多半得重調
    source_quote: 是在只有 **5 篇論文**的 dev split 上調出來的，樣本數小到換個 domain（章節命名習慣不同）多半得重調。
  - text: 整套章節過濾機制高度依賴文件有標準化的 section 結構，拿去處理非結構化文件，字面比對那一段會直接失效
    source_quote: 整套機制高度依賴文件有標準化的 section 結構；拿去處理會議記錄、PRD 這類非結構化文件，字面比對那一段會直接失效，全部 fallback 到語意比對。
  importance: 6
  status: normal
- id: c7
  role: anchor
  text: 論文宣稱這套候選過濾能把 GPT 呼叫次數壓到約八分之一，blog 說這個宣稱有數據支撐，但也有代價
  source_quotes:
  - 論文宣稱這套候選過濾能把 GPT 呼叫次數壓到約八分之一。這個宣稱有數據支撐，但也有代價
  - 幾乎用整篇論文 | 約 8.2 次 | 100%
  anchor_type: 原作者解讀
  comparison_target: 幾乎用整篇論文的做法（平均約 8.2 次 GPT 呼叫）
  qualifiers:
  - text: 用八分之一的呼叫成本換掉五分之一的內容涵蓋度划不划算，得看應用能容忍多少遺漏
    source_quote: 用八分之一的呼叫成本換掉五分之一的內容涵蓋度划不划算，得看你的應用能容忍多少遺漏。
  importance: 7
  status: normal
- id: c8
  role: anchor
  text: 候選過濾的成本與 recall 取捨，呼叫次數愈多，recall 愈高：論文提出的輕量 filter 平均約 1 次 GPT 呼叫、recall 78.89%；中等範圍候選約 5.3 次、81.34%；幾乎用整篇論文約 8.2 次、100%
  source_quotes:
  - 候選過濾的成本與 recall 取捨（原文 Table 10）：呼叫次數愈多，recall 愈高。
  - 論文提出的輕量 filter | 約 1 次 | 78.89%
  - 中等範圍候選 | 約 5.3 次 | 81.34%
  - 幾乎用整篇論文 | 約 8.2 次 | 100%
  anchor_type: 實驗結果
  comparison_target: 三種策略互相比較：輕量 filter、中等範圍候選、幾乎用整篇論文
  qualifiers:
  - text: 原文 Table 10 還有一個 precision 欄位，blog 沒有列出，數值看起來不合常理，懷疑是欄位錯位，引用前建議回頭核對原始 PDF；Recall 的數字看起來正常
    source_quote: 這張表（原文 Table 10）還有一個 precision 欄位，本文沒有列出，數值是 6.73、5.93、5.88，看起來不合常理，precision 通常應該落在 0–1 或百分比區間。懷疑是原文表格的欄位錯位，要引用這幾個數字前建議回頭核對原始 PDF。Recall 的數字則看起來正常。
  importance: 8
  status: normal
- id: c9
  role: evaluation
  text: 章節過濾這一步的篩選不可逆：被這一步濾掉的句子，後面的 Stage 再也看不到
  source_quotes:
  - 論文宣稱這套候選過濾能把 GPT 呼叫次數壓到約八分之一。
  - 關鍵在於這一步的篩選不可逆：被這一步濾掉的句子，後面的 Stage 再也看不到。
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 9
  status: normal
- id: c10
  role: evaluation
  text: 因為篩選不可逆，輕量 filter 沒選到的約 21% 相關內容不是「暫時沒被選上」，而是永久消失
  source_quotes:
  - 所以那 21% 的相關內容不是「暫時沒被選上」，是永久消失。
  - 論文提出的輕量 filter | 約 1 次 | 78.89%
  anchor_type: 部落格考證
  comparison_target: 幾乎用整篇論文的做法（recall 100%）
  importance: 10
  status: pending_author_confirmation
- id: c11
  role: evaluation
  text: 章節過濾的門檻是在只有 5 篇論文的 dev split 上調出來的，樣本數小到換個 domain（章節命名習慣不同）多半得重調
  source_quotes:
  - 是在只有 5 篇論文的 dev split 上調出來的，樣本數小到換個 domain（章節命名習慣不同）多半得重調。
  anchor_type: 部落格判斷
  comparison_target: blog 只判斷 5 篇樣本數小到換 domain 多半得重調，沒有給具體的對照數字
  importance: 11
  status: normal
- id: c12
  role: evaluation
  text: 整套章節過濾機制高度依賴文件有標準化的 section 結構；拿去處理會議記錄、PRD 這類非結構化文件，字面比對那一段會直接失效，全部 fallback 到語意比對
  source_quotes:
  - 更根本的是，整套機制高度依賴文件有標準化的 section 結構；拿去處理會議記錄、PRD 這類非結構化文件，字面比對那一段會直接失效，全部 fallback 到語意比對。
  anchor_type: 部落格判斷
  importance: 12
  status: normal
- id: c13
  role: mechanism
  text: Stage 3 完全沒有做任何客製化訓練，純靠 prompting
  source_quotes:
  - Stage 1 和 Stage 2 都投入大量心力做 SFT 加偏好微調，但對使用者體驗影響最直接的 Stage 3，完全沒有做任何客製化訓練，純靠 prompting。
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 13
  status: normal
- id: c14
  role: evaluation
  text: Stage 3（摘要加重排，不需訓練）落地可行性最高：成本最低（只多兩次 LLM 呼叫），消融實驗證實有明確效果提升，是全篇投入產出比最好的部分
  source_quotes:
  - Stage 3（摘要 + 重排，不需訓練） | 最高 | 成本最低（只多兩次 LLM 呼叫），消融實驗證實有明確效果提升，是全篇投入產出比最好的部分
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  qualifiers:
  - text: 摘要重排的消融實驗樣本數只有 10 篇，評分者也不是獨立第三方
    source_quote: 不過樣本數只有 10 篇，評分者也不是獨立第三方。
  importance: 14
  status: normal
- id: c15
  role: anchor
  text: 論文做了 before/after 消融實驗（10 篇論文，Stage 2 的抽取版 vs Stage 3 的摘要重排版）：Coherence +0.5、Readability +1.0、Coverage -0.05（幾乎不變）、Relevance 0（不變）
  source_quotes:
  - 論文做了 before/after 的消融實驗（10 篇論文，Stage 2 的抽取版 vs Stage 3 的摘要重排版）
  - Coherence | +0.5
  - Readability | +1.0
  - Coverage | -0.05（幾乎不變）
  - Relevance | 0（不變）
  anchor_type: 實驗結果
  comparison_target: Stage 2 的抽取版（摘要與重排之前）
  qualifiers:
  - text: 樣本數只有 10 篇，評分者也不是獨立第三方
    source_quote: 不過樣本數只有 10 篇，評分者也不是獨立第三方。
  importance: 15
  status: normal
- id: c16
  role: evaluation
  text: 這是全篇論文裡證據力相對紮實的一個實驗：直接的 before/after 對照，證實摘要加重排確實提升了可讀性與連貫性，而且沒有明顯犧牲內容涵蓋度
  source_quotes:
  - 這是全篇論文裡證據力相對紮實的一個實驗：直接的 before/after 對照，證實摘要加重排確實提升了可讀性與連貫性，而且沒有明顯犧牲內容涵蓋度。
  anchor_type: 部落格判斷
  qualifiers:
  - text: 樣本數只有 10 篇，評分者也不是獨立第三方
    source_quote: 不過樣本數只有 10 篇，評分者也不是獨立第三方。
  importance: 16
  status: pending_author_confirmation
- id: c17
  role: evaluation
  text: 附錄 D–G 提供了 zero-shot / few-shot 版本的大綱生成與內容抽取完整 prompt，但沒有提供 Stage 3 用的 prompt template；Stage 3 是唯一無法從附錄還原的一步
  source_quotes:
  - 附錄 D–G 提供了 zero-shot / few-shot 版本的大綱生成與內容抽取完整 prompt，但沒有提供 Stage 3 用的 prompt template。四個模組裡，這是唯一無法從附錄還原的一步——偏偏它還是最容易直接搬來用的那一步。
  anchor_type: 部落格考證
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 17
  status: normal
- id: c18
  role: mechanism
  text: 論文沒有做自動化事實查核，而是讓標註者對「內容相關性」評分，用這個分數間接代表有沒有幻覺
  source_quotes:
  - 論文沒有做自動化事實查核，而是讓標註者對「內容相關性」評分，用這個分數間接代表有沒有幻覺。
  anchor_type: 部落格考證
  importance: 18
  status: normal
- id: c19
  role: evaluation
  text: 用相關性 proxy 幻覺並不嚴謹：一段內容完全可以「跟標題高度相關」同時「捏造論文沒講過的細節」，這種類型的幻覺在這套評測下會直接漏掉
  source_quotes:
  - 一段內容完全可以「跟標題高度相關」同時「捏造論文沒講過的細節」，這種類型的幻覺在這套評測下會直接漏掉。
  anchor_type: 部落格判斷
  importance: 19
  status: normal
- id: c20
  role: mechanism
  text: Stage 3 用兩步驟 prompting 整理前兩階段抽出的零散句子片段：先把抽出的內容摘要成 bullet points，再把這些 bullet points 丟回 LLM，要求它在同一標題內部、或跨標題之間重新排列，讓順序更符合聽眾的理解節奏；例如把「實驗結果」那張投影片裡先丟數字、後補實驗設定的順序倒過來，或把定義類的 bullet 提到應用類的前面
  source_quotes:
  - 前兩階段抽出來的是零散的句子片段，直接貼上投影片會很難讀。
  - 機制是兩步驟 prompting：先把 … 的內容摘要成 bullet points，再把這些 bullet points 丟回 LLM，要求它在同一標題內部、或跨標題之間重新排列，讓順序更符合聽眾的理解節奏。具體來說，就是把「實驗結果」那張投影片裡先丟數字、後補實驗設定的順序倒過來，或把定義類的 bullet 提到應用類的前面。
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 8
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

以下是很基本的通用詞，blog 沒有解釋，由撰寫者以一般知識補充；它們不是卡上的主張，不能當作 blog 的說法引用。

- **recall（召回率）**：所有真正相關的內容中，被找出來的比例。「高 recall 的過濾器」代表寧可多留一些候選，也不要漏掉相關內容；recall 78.89% 就是約有 21% 的相關內容沒被選進來。
- **precision（精確率）**：被選出來的內容中，真正相關的比例。
- **fuzzy match**：容許字面上有些差異的字串比對，例如標題與章節標題用字略有不同仍算相近。
- **Sentence-BERT**：把句子轉成向量，用向量距離衡量語意相似度的模型。
- **retrieve-then-rerank**：先用便宜的方法撈出一批候選，再用較精細的方法重新排序或挑選。
- **幻覺（hallucination）**：模型生成了原文或事實中沒有的內容。
- **proxy**：用一個容易量測的指標，間接代表真正想測的東西。
- **PRD**：產品需求文件（product requirements document）。
- **GPT-3.5-turbo 的 4096 token 限制**：模型一次能處理的輸入加輸出長度上限。
