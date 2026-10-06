---
id: judge-readable-vs-derive
title: 判官能不能用，先問「答案能不能被讀出來或核對」；沒有東西可核對時，信心再高也不可靠
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: jev-as-a-judge
  article_title: 便宜判官先判、沒把握才找 GPT-6：JEV 串接真的省錢嗎？
  url: https://datasciocean.com/paper-intro/jev-as-a-judge/
  sections:
  - 先弄清楚什麼是 LLM 判官
  - 整體評價
  - 針對 JEV 1.13 量出來的適用界線
  - 判官能不能用，先問「答案能不能被讀出來或核對」
  - 信心很高，不代表可靠，尤其在判官手上沒有東西可核對的時候
  - 沒有參考答案的文章是什麼意思、為什麼信心會失效
  - 信心 q：定義與驗證
  - AUROC：用排隊看懂它
  - 串接分流與門檻怎麼選
  - 串接的價值，來自「兩個判官錯在不同的題」
  first_appearance: true
parent: null
related:
- jev-cascade-overview
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 判官的工作是比對，不是從頭解題：答案能直接從文字讀出，小模型就夠；需要自己重新推導才知道對錯，小模型就不及；而且判官沒有證據可核對時，仍然會給一個很有把握的答案
  source_quotes:
  - 判官的工作是比對，不是從頭解題。答案能直接從文字讀出，小模型就夠；需要自己重新推導才知道對錯，小模型就不及。
  - 判官沒有證據可核對時，它仍然會給一個很有把握的答案。
  anchor_type: 部落格判斷
  importance: 1
  status: normal
  qualifiers:
  - text: 只有 200 題；論文自己說只能證明結果跟任務有關，不能斷言差別純粹來自有沒有證據
    source_quote: 限制：只有 200 題，論文自己說只能證明結果跟任務有關，不能斷言差別純粹來自有沒有證據。
- id: c2
  role: context
  text: LLM 判官是拿一個 LLM 去評另一個模型的輸出，例如「這兩個回答哪個比較好」，或「這個答案有沒有被給定的證據支持」
  source_quotes:
  - '**[LLM 判官](../chateval/)**是拿一個 LLM 去評另一個模型的輸出，例如「這兩個回答哪個比較好」，或「這個答案有沒有被給定的證據支持」。'
  anchor_type: 背景說明
  importance: 2
  status: normal
- id: c3
  role: context
  text: 「沒有參考答案」指判官只拿到問題加回答，手上沒有任何證據文件或標準答案可以對照，要完全靠自己的知識判斷這段回答有沒有胡說（幻覺）
  source_quotes:
  - 「沒有參考答案」指判官只拿到「問題加回答」，手上沒有任何證據文件或標準答案可以對照，要完全靠自己的知識判斷這段回答有沒有胡說（幻覺）。
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: context
  text: JEV 是 TypeSafe AI 的託管模型，屬決策型判官：只輸出判決與每個標籤的機率，不產生任何文字，便宜、快；論文測的是 1.13 版
  source_quotes:
  - 決策型判官（decision-only judge） | 只輸出判決與每個標籤的機率，不產生任何文字 | 便宜、快。**[JEV](../../ai-concept/jev-overview/)**（TypeSafe AI 的託管模型，論文測的是 1.13 版）就是這類
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 信心 q 是 JEV 所有標籤機率中最大的那一個，也就是它對自己所選判決的把握
  source_quotes:
  - \( q \) 是 JEV 所有標籤機率中最大的那一個，也就是它對自己所選判決的把握
  anchor_type: 設計參數
  importance: 5
  status: normal
- id: c6
  role: context
  text: AUROC 衡量 q 排序錯題的能力：隨機抽一題答錯的、一題答對的，答錯那題的 q 比較低的機率；0.5 等於亂猜，1 等於完美
  source_quotes:
  - AUROC 只問一件事：把所有題目照 \( q \) 從低到高排成一排，答錯的題是不是排得比答對的題前面？
  - 白話意思是：隨機抽一題答錯的、一題答對的，答錯那題的 \( q \) 比較低的機率。0.5 等於亂猜，1 等於完美。
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 6
  status: normal
- id: c7
  role: context
  text: 串接是便宜判官先判全部題目，沒把握的才交給強判官；被接受的題用第一階段的答案，被轉出的題用強判官的答案
  source_quotes:
  - 便宜判官先判全部題目，沒把握的才交給強判官
  - 串接的結果是，被接受的題用第一階段的答案，被轉出的題用強判官的答案。
  anchor_type: 背景說明
  importance: 7
  status: normal
- id: c8
  role: anchor
  text: 自編例子：「這個回答有沒有拒絕使用者？」讀一遍就知道；「這段程式有沒有 bug？」要在腦中執行一遍才知道
  source_quotes:
  - 自編例子：「這個回答有沒有拒絕使用者？」讀一遍就知道；「這段程式有沒有 bug？」要在腦中執行一遍才知道。
  anchor_type: 部落格舉例
  importance: 8
  status: normal
- id: c9
  role: anchor
  text: 答案能讀出的任務，JEV 跟 GPT-6 差在 2 點內；需要推導的任務落後很多：知識 −7.0、程式 −12.9、數學 −14.3、邏輯謎題 −27.6（JEV 減 GPT-6 的準確度，單位為百分點）
  source_quotes:
  - 答案能讀出的任務，JEV 跟 GPT-6 差在 2 點內。需要推導的任務落後很多：知識 −7.0、程式 −12.9、數學 −14.3、邏輯謎題 −27.6（JEV 減 GPT-6 的準確度，單位為百分點）。
  anchor_type: 實驗結果
  comparison_target: GPT-6（同任務的準確度，差值為 JEV 減 GPT-6，單位為百分點）
  qualifiers:
  - text: 這個界線是針對特定版本（JEV 1.13）量的，新版本出來就可能移動
    source_quote: 這個界線是針對特定版本量的，新版本出來就可能移動
  - text: 對照組是低推理強度的 GPT-6，不是它的最強設定
    source_quote: 對照組是低推理強度的 GPT-6，不是它的最強設定
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: 上線前先把任務分成三類：讀得出答案，便宜判官夠用；需要推導，預期要大量轉給強判官；沒有證據可對照，信心不可靠
  source_quotes:
  - 上線前的做法：先把任務分成三類。讀得出答案，便宜判官夠用；需要推導，預期要大量轉給強判官；沒有證據可對照，見下一項。
  - 模型的機率反映的是「它對自己輸出的把握」，不是「這個答案跟事實的距離」。
  anchor_type: 部落格判斷
  importance: 10
  status: normal
  qualifiers:
  - text: 只有 200 題；論文自己說只能證明結果跟任務有關，不能斷言差別純粹來自有沒有證據
    source_quote: 限制：只有 200 題，論文自己說只能證明結果跟任務有關，不能斷言差別純粹來自有沒有證據。
- id: c11
  role: anchor
  text: 200 題沒有證據可對照的回答，二選一，丟硬幣是 50%；三個判官都接近丟硬幣卻都很有把握：JEV 準確度 53.5%、平均最高機率 0.91，GPT-4.1 mini 是 54.0%、0.94，GPT-5.4 是 56.0%、0.96；JEV 的 AUROC 是 0.498，信心完全分不出對錯
  source_quotes:
  - 附錄有一組直接的數字：200 題沒有證據可對照的回答，二選一，丟硬幣是 50%。三個判官都接近丟硬幣，卻都很有把握。JEV 的 AUROC 是 0.498，信心完全分不出對錯。
  - JEV | 53.5% | 0.91
  - GPT-4.1 mini | 54.0% | 0.94
  - GPT-5.4 | 56.0% | 0.96
  anchor_type: 實驗結果
  comparison_target: 丟硬幣的 50%（二選一的隨機基準）；AUROC 的亂猜基準是 0.5
  qualifiers:
  - text: 只有 200 題，95% 信賴區間 [46.5, 60.5]
    source_quote: 只有 200 題，95% 信賴區間 [46.5, 60.5]
  - text: 論文自己說，這組跟有證據的那組在內容和標籤來源上都不同，所以只能說「結果跟任務有關」，不能斷言差別純粹來自有沒有證據
    source_quote: 論文自己說，這組跟有證據的那組在內容和標籤來源上都不同，所以只能說「結果跟任務有關」，不能斷言差別純粹來自有沒有證據
  importance: 11
  status: normal
- id: c12
  role: mechanism
  text: 沒有證據可對照時串接會失效：分流的前提是「q 低的題比較容易錯」，但這裡 q 都很高、高低跟對錯無關，沒有任何門檻能把該轉的題挑出來；就算轉出去，強判官 GPT-5.4 也只有 56%
  source_quotes:
  - 這會讓串接失效，因為分流的前提是「\( q \) 低的題比較容易錯」。這裡 \( q \) 都很高，而且高低跟對錯無關，所以沒有任何門檻能把該轉的題挑出來。而且就算轉出去，強判官 GPT-5.4 也只有 56%，轉了也沒用。
  anchor_type: 部落格判斷
  comparison_target: 丟硬幣的 50%
  importance: 12
  status: normal
  qualifiers:
  - text: 只有 200 題；論文自己說只能證明結果跟任務有關，不能斷言差別純粹來自有沒有證據
    source_quote: 限制：只有 200 題，論文自己說只能證明結果跟任務有關，不能斷言差別純粹來自有沒有證據。
- id: c13
  role: evaluation
  text: 論文的結論是「沒有任何受測判官能用在這類題目上」，所以這不是 JEV 特有的問題
  source_quotes:
  - 論文的結論是「沒有任何受測判官能用在這類題目上」，所以這不是 JEV 特有的問題。
  anchor_type: 原作者解讀
  importance: 13
  status: normal
- id: c14
  role: evaluation
  text: 信心分流的前提是「信心低的題比較容易錯」，上線前先用標註題量 AUROC 驗證；AUROC 接近 0.5 時，不要用信心分流，轉出去也沒用，因為強判官也一樣近乎亂猜
  source_quotes:
  - 信心分流的前提是「信心低的題比較容易錯」，上線前先用標註題量 AUROC 驗證
  - AUROC 接近 0.5 時，不要用信心分流；轉出去也沒用，因為強判官也一樣近乎亂猜
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 14
  status: normal
  qualifiers:
  - text: 只有 200 題；論文自己說只能證明結果跟任務有關，不能斷言差別純粹來自有沒有證據
    source_quote: 限制：只有 200 題，論文自己說只能證明結果跟任務有關，不能斷言差別純粹來自有沒有證據。
```
