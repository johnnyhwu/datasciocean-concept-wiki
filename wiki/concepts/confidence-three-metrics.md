---
id: confidence-three-metrics
title: 評估會給信心的分類器要分三件事看：判決對不對、信心能排出誰會錯、信心數字能不能當機率讀；校準只動第三件事
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: jev-as-a-judge
  article_title: 便宜判官先判、沒把握才找 GPT-6：JEV 串接真的省錢嗎？
  url: https://datasciocean.com/paper-intro/jev-as-a-judge/
  sections:
  - 信心 q：定義與驗證
  - 評估「會給信心的分類器」，要分三件事看，三者互相獨立
  - AUROC：用排隊看懂它
  - 校準：機率說 90%，實際是不是 90%
  - Brier 分數：總共偏多少，一個數字
  - NLL（負對數似然）：特別嚴懲「很有把握卻答錯」
  - 校準只動數字，不動排序，而且校準綁在任務上
  - 為什麼模型常常校準不好
  - 二選一時 q 與 logit 差、溫度縮放、為什麼不改準確度與 AUROC
  - q 與 logit 差的關係
  - 溫度縮放怎麼做
  - 為什麼不改準確度與 AUROC
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
  text: 評估一個會給信心的分類器，要分三件事看：準確度看判決對不對；AUROC 只看 q 的順序；Brier 與 NLL 看 q 的數字大小；而溫度縮放（一種校準）只動數字這一件，二選一時不動排序與判決
  source_quotes:
  - 準確度看判決對不對；AUROC 只看 \( q \) 的順序；Brier 與 NLL 看 \( q \) 的數字大小。三者量的是不同的東西，所以一個判官可以在其中一項很好、另一項很差。
  - 看一個會給信心的分類器，AUROC 只回答「\( q \) 能不能排出誰比較可能錯」，不回答「\( q = 0.9 \) 是不是真的代表 90% 會對」，也不回答「判決對不對」。三者要分開看。
  - 溫度縮放把 logit 差 \( g \) 除以 \( T \)，再轉回機率。二選一時，新的信心是 \( g \) 的遞增函數，所以每題的先後順序、判決都不變
  - 調 \( T \) 之後，準確度與 AUROC 不變，Brier、NLL、ECE 會變
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 1
  status: normal
- id: c2
  role: context
  text: q 是 JEV 所有標籤機率中最大的那一個，也就是它對自己所選判決的把握
  source_quotes:
  - \( q \) 是 JEV 所有標籤機率中最大的那一個，也就是它對自己所選判決的把握
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: AUROC 衡量 q 排序錯題的能力：隨機抽一題答錯的、一題答對的，答錯那題的 q 比較低的機率；0.5 等於亂猜，1 等於完美
  source_quotes:
  - AUROC 只問一件事：把所有題目照 \( q \) 從低到高排成一排，答錯的題是不是排得比答對的題前面？
  - 白話意思是：隨機抽一題答錯的、一題答對的，答錯那題的 \( q \) 比較低的機率。0.5 等於亂猜，1 等於完美。
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 3
  status: normal
- id: c4
  role: context
  text: 校準（calibration）就是模型說有多少把握的那些題，實際上真的大約就有那麼高的比例是對的；信心 0.9 的題目，正確率就該是 0.9
  source_quotes:
  - 校準（calibration）就是模型說「有 90% 把握」的那些題，實際上真的大約有 90% 是對的
  - 白話：信心 0.9 的題目，正確率就該是 0.9
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 4
  status: normal
- id: c5
  role: context
  text: Brier 分數是「機率與實際對錯的平方差」的平均，越低表示機率越準
  source_quotes:
  - Brier 分數是「機率與實際對錯的平方差」的平均，越低表示機率越準。
  anchor_type: 背景說明
  importance: 5
  status: pending_author_confirmation
- id: c6
  role: context
  text: NLL 是每題取「模型給正確答案的機率 p」，算 −ln p，再對所有題平均，越低越好
  source_quotes:
  - 每題取「模型給正確答案的機率 \( p \)」，算 \( -\ln p \)，再對所有題平均，越低越好。
  anchor_type: 背景說明
  importance: 6
  status: normal
- id: c7
  role: context
  text: 溫度縮放是把機率整體調平或調尖的旋鈕：溫度 T 大於 1 把機率壓平，小於 1 把機率拉尖，T 等於 1 是原本的機率
  source_quotes:
  - 溫度縮放是把機率整體調平或調尖的旋鈕（溫度 \( T > 1 \) 壓平，\( T < 1 \) 拉尖，細節見後面的概念詳解）
  - \( T \)：溫度，一個正數；\( T = 1 \) 是原本的機率，\( T > 1 \) 把機率壓平，\( T < 1 \) 把機率拉尖
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 7
  status: normal
- id: c8
  role: mechanism
  text: AUROC 只看順序，不看 q 的大小；把 q 全部改成別的數字，只要順序不變，AUROC 就不變
  source_quotes:
  - '**AUROC 只看順序，不看 \( q \) 的大小。** 把上表的 \( q \) 全部改成 0.01、0.02、0.03……只要順序不變，AUROC 還是 0.78。'
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 示範題
  importance: 8
  status: normal
- id: c9
  role: mechanism
  text: 排序與校準是兩個獨立的性質：排序好、校準差，能排出錯題但數字不能直接讀；排序差、校準好，數字誠實但幫不上忙
  source_quotes:
  - 排序與校準是兩個獨立的性質：
  - '**排序好** | 理想 | 能排出錯題，但數字不能直接讀'
  - '**排序差** | 數字誠實，但幫不上忙 | 兩頭落空'
  anchor_type: 部落格判斷
  importance: 9
  status: normal
- id: c10
  role: mechanism
  text: 溫度縮放把兩個標籤的 logit 差 g 除以 T，再轉回機率；二選一時信心是 g 的遞增函數，所以題目之間 q 的先後順序不變，調 T 只是把機率整體壓平或拉高
  source_quotes:
  - 溫度縮放把 logit 差 \( g \) 除以 \( T \)，再轉回機率。二選一時，新的信心是 \( g \) 的遞增函數，所以每題的先後順序、判決都不變
  - 它看的是不同題目之間 \( q \) 的排序。二選一時，\( q \) 是 \( g \) 的遞增函數，調 \( T \) 只是把它整體壓平或拉高，題目之間的先後順序不變
  anchor_type: 背景說明
  qualifiers:
  - text: 以下針對二選一（論文的主要任務），內容是一般知識，除非特別註明
    source_quote: 以下針對二選一（論文的主要任務），內容是一般知識，除非特別註明。
  - text: 對 JEV 要小心：論文通篇沒有提到 logit，也沒說 JEV 內部怎麼產生機率，所以「JEV 是不是由 logit 差算出」論文沒有講
    source_quote: 論文通篇沒有提到 logit，也沒說 JEV 內部怎麼產生機率，所以「JEV 是不是由 logit 差算出」，論文沒有講。
  - text: 用機率反推 g 是 blog 的推論，論文沒有交代它實際怎麼對 JEV 做縮放
    source_quote: 第 2 步用機率反推 \( g \) 是我的推論，論文沒有交代它實際怎麼對 JEV 做縮放。
  importance: 10
  status: normal
- id: c11
  role: anchor
  text: 自編例子：6 題實際只答對一半，判官 X 與判官 Y 的排序一模一樣、AUROC 都是 7/9，但 Y 每題都宣稱有 95% 以上的把握，Brier 約 0.468，X 約 0.294；AUROC 完全看不出兩者的差別
  source_quotes:
  - 兩者排序一模一樣，AUROC 都是 7/9。但判官 Y 每題都宣稱有 95% 以上的把握，實際只對一半。AUROC 完全看不出兩者的差別
  - 判官 X 的 \( q \) 是 0.55、0.60、0.70、0.90、0.95、0.99，結果是 錯、對、錯、錯、對、對，Brier \( = (0.55^2 + 0.40^2 + 0.70^2 + 0.90^2 + 0.05^2 + 0.01^2) / 6 \approx 0.294 \)。判官 Y 的 \( q \) 是 0.95、0.96、0.97、0.98、0.985、0.99，同樣結果，Brier \( \approx 0.468 \)。排序一樣（AUROC 都是 0.78），Brier 卻差很多。
  anchor_type: 部落格舉例
  comparison_target: 判官 X 對判官 Y（blog 自編的 6 題例子，不是論文數字）
  qualifiers:
  - text: 這個 Brier 是簡化版，只看 q 對不對；論文的 Brier 對所有標籤的機率計算，細節略有不同
    source_quote: 這是簡化版，只看 \( q \) 對不對。論文的 Brier 對所有標籤的機率計算，細節略有不同。
  importance: 11
  status: pending_author_confirmation
- id: c12
  role: evidence
  text: 論文把排序能力（AUROC）與機率品質（Brier）分開量：JudgeBench 上 JEV 的 AUROC 是 0.745、GPT-6 是 0.907；Brier 是 JEV 0.297、GPT-6 0.095，JEV 不只排序弱，Brier 還差了三倍
  source_quotes:
  - 論文 7.2 節把排序能力（AUROC）與機率品質（Brier 分數，越低越好，見後面的概念詳解）分開量
  - JudgeBench | 0.745 | 0.907 | 0.297 | 0.095
  - JudgeBench 上 JEV 不只排序弱，Brier 還差了三倍。
  anchor_type: 實驗結果
  comparison_target: JEV 對 GPT-6（同一個 JudgeBench 任務；AUROC 越高越好、Brier 越低越好）
  qualifiers:
  - text: 表中的 AUROC 是單次呼叫的結果，跟兩順序平均的數字略有差異
    source_quote: 表中的 AUROC 是單次呼叫的結果，跟前面兩順序平均的數字略有差異。
  importance: 12
  status: pending_author_confirmation
- id: c13
  role: evidence
  text: 同樣是 q ≥ 0.9，不同任務上對應的錯誤率不同：RewardBench 是 1.8%（20／1,130 題），JudgeBench 是 5.7%（7／123 題），這是 q 的數字不能直接當機率讀的更直接證據
  source_quotes:
  - 更直接的證據是，同樣是 \( q \ge 0.9 \)，不同任務上對應的錯誤率不同：RewardBench 是 1.8%（20／1,130 題），JudgeBench 是 5.7%（7／123 題，題數少，數字不太穩）。
  anchor_type: 實驗結果
  comparison_target: RewardBench 對 JudgeBench（同為 q ≥ 0.9 的題）
  qualifiers:
  - text: JudgeBench 這組只有 123 題，題數少，數字不太穩
    source_quote: 7／123 題，題數少，數字不太穩
  importance: 13
  status: normal
- id: c14
  role: anchor
  text: 同一個 JEV、同一套溫度縮放流程，擬合出的 T 在三個任務上分別是 RewardBench 0.651、JudgeBench 2.148、HaluEval 4.452，方向不一致；NLL 在 RewardBench 由 0.192 變 0.216、JudgeBench 由 0.449 變 0.475，校準後反而變差，HaluEval 由 0.496 變 0.304，變好
  source_quotes:
  - 同一個 JEV，RewardBench 擬合出 \( T = 0.651 \)（NLL 由 0.192 變 0.216，變差），JudgeBench 是 \( T = 2.148 \)（0.449 變 0.475，變差），HaluEval 是 \( T = 4.452 \)（0.496 變 0.304，變好）。方向不一致，其中兩個任務校準後反而更糟。
  anchor_type: 實驗結果
  comparison_target: 各任務校準前（T = 1）的 NLL，以及三個任務擬合出的 T 彼此比較
  qualifiers:
  - text: T 是在選擇集（select set）上擬合，再到 held-out 驗收
    source_quote: 論文的做法是用 select set 擬合 \( T \)，再到 held-out 驗收（表 2）。
  importance: 14
  status: normal
- id: c15
  role: mechanism
  text: 校準是「對某一種題目」才成立的：在 A 類題目上調好的機率，換到 B 類題目就會跑掉，因為模型在不同題目上的難度與錯法不同
  source_quotes:
  - '**原因 3：校準是「對某一種題目」才成立的。** 在 A 類題目上調好的機率，換到 B 類題目就會跑掉，因為模型在不同題目上的難度與錯法不同。'
  anchor_type: 背景說明
  qualifiers:
  - text: 這一節是一般知識，不是論文內容
    source_quote: 以下是一般知識，不是論文內容。
  - text: 論文的直接證據在論文 7.2 節
    source_quote: 論文的直接證據在論文 7.2 節
  importance: 15
  status: normal
- id: c16
  role: evaluation
  text: 用途決定該看哪個指標：只要判決，看準確度；用信心挑出該複查的題（分流、人工覆核），看 AUROC；把信心當機率讀（風險估算、跟別的系統組合），看 Brier 與 NLL
  source_quotes:
  - 用途決定該看哪個指標：只要判決，看準確度；用信心挑出該複查的題（分流、人工覆核），看 AUROC；把信心當機率讀（風險估算、跟別的系統組合），看 Brier 與 NLL。
  anchor_type: 部落格判斷
  importance: 16
  status: normal
- id: c17
  role: evaluation
  text: 只做分流，不需要校準，排序夠好就行；要把 q 當機率讀，就要用「該任務自己的標註資料」另外校準
  source_quotes:
  - 實務上：只做分流，不需要校準，排序夠好就行；要把 \( q \) 當機率讀，就要用「該任務自己的標註資料」另外校準。
  anchor_type: 部落格判斷
  importance: 17
  status: normal
```
