---
id: bradley-terry-pairwise-preference
title: Bradley-Terry 把兩兩比較看成每個項目隱藏「實力值」的機率反映，是 RLHF reward model 的共同底層；成對比較比直接打分共識度高，但有傳遞性假設的缺陷
type_hint: 方法
context_type: standalone_classic
sources:
- article: persona-aware-d2s
  article_title: "拆解 Persona-Aware-D2S：同一份文件，怎麼依受眾和長度長出不同簡報"
  url: https://datasciocean.com/paper-intro/persona-aware-d2s/
  sections:
  - 偏好微調（P-F）
  - Bradley-Terry Model：從球隊排名到 RLHF 的共同底層
  first_appearance: true
parent: null
related:
  - persona-d2s-training-design-flaws
  - decision-transformer-reward-conditioning
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: Bradley-Terry model 的核心假設是每個項目都有一個看不見的「實力值」，而比較結果只是這個實力值的機率反映，不是絕對保證；它是 RLHF 領域最廣泛採用的偏好模型
  source_quotes:
  - 它的核心假設是：每個項目都有一個看不見的「實力值」，而比較結果只是這個實力值的機率反映，不是絕對保證。
  - 這是 RLHF 領域最廣泛採用的偏好模型
  anchor_type: 背景說明
  importance: 1
  status: normal
- id: c2
  role: context
  text: Bradley-Terry model（Bradley & Terry, 1952）是個很老的統計模型，原本處理的問題是「兩兩比較之後怎麼推算整體排名」，例如球隊戰績排序，跟 AI 一點關係都沒有
  source_quotes:
  - Bradley-Terry model（Bradley & Terry, 1952）是個很老的統計模型，原本處理的問題是「兩兩比較之後怎麼推算整體排名」，例如球隊戰績排序，跟 AI 一點關係都沒有。
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 日期
  importance: 2
  status: normal
- id: c3
  role: mechanism
  text: i 贏 j 的機率等於 i 的實力除以 i 與 j 的實力總和
  source_quotes:
  - P(i \text{ 贏 } j) = \frac{\text{實力}_i}{\text{實力}_i + \text{實力}_j}
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: anchor
  text: A 隊實力值 8、B 隊實力值 2，則 A 贏 B 的機率是 8/(8+2) = 0.8；A 實力強四倍，贏面八成，但 B 仍有兩成機率爆冷
  source_quotes:
  - 舉個具體的例子：A 隊實力值 8、B 隊實力值 2，則 \( P(A \text{ 贏 } B) = 8/(8+2) = 0.8 \)。A 實力強四倍，贏面八成，但 B 仍有兩成機率爆冷。
  anchor_type: 部落格舉例
  comparison_target: B 隊（實力值 2）
  importance: 4
  status: normal
- id: c5
  role: evaluation
  text: 這種容許不確定性的設計，正好適合套在「人類偏好」這種有雜訊、同一個人不同時候判斷也未必一致的場景
  source_quotes:
  - 這種容許不確定性的設計，正好適合套在「人類偏好」這種有雜訊、同一個人不同時候判斷也未必一致的場景。
  anchor_type: 部落格判斷
  importance: 5
  status: normal
- id: c6
  role: mechanism
  text: 把贏的機率重新參數化成指數形式（令實力 p_i = e^{r_i}），就會得到 reward model 訓練裡常見的 σ(r_i - r_j) 形式
  source_quotes:
  - 重新參數化成指數形式（令 \( p_i = e^{r_i} \)），就會得到 reward model 訓練裡常見的 \( \sigma(r_i - r_j) \) 形式
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: Persona-Aware-D2S 的 reward model 用 Bradley-Terry loss 訓練：L = -E[log σ(s_w - s_r)]，其中 s_w 是被選中（chosen）版本的分數，s_r 是被淘汰（rejected）版本的分數
  source_quotes:
  - 第二段是訓練 reward model，用的是 Bradley-Terry loss
  - \mathcal{L} = -\mathbb{E}_{x \sim \text{train}}\left[\log \sigma(s_w - s_r)\right]
  - 其中 \( s_w \) 是被選中（chosen）版本的分數，\( s_r \) 是被淘汰（rejected）版本的分數。
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 7
  status: normal
- id: c8
  role: anchor
  text: 從 Christiano et al. (2017) 的 RLHF 開山文獻、OpenAI 的 InstructGPT，一路到後來的 DPO，底層數學都是同一套 Bradley-Terry loss，差別只在怎麼用
  source_quotes:
  - 這是 RLHF 領域最廣泛採用的偏好模型，從 Christiano et al. (2017) 這篇 … OpenAI 的 InstructGPT，一路到後來的 … 底層數學都是同一套 Bradley-Terry loss，差別只在怎麼用。
  anchor_type: 外部研究引用
  numeric_kind: non_comparative
  numeric_reason: 日期
  importance: 8
  status: normal
- id: c9
  role: evaluation
  text: Persona-Aware-D2S 的 reward modeling 完全不是原創，是直接套用業界標準做法
  source_quotes:
  - 換句話說，Persona-Aware-D2S 的 reward modeling 完全不是原創，是直接套用業界標準做法。
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 9
  status: normal
- id: c10
  role: anchor
  text: reward model 對 chosen 版本打 3.5 分、rejected 打 1.0 分，則 s_w - s_r = 2.5，σ(2.5) ≈ 0.92，loss 是 -log(0.92) ≈ 0.08，很小，代表模型判斷準確
  source_quotes:
  - 實際訓練起來會長這樣：reward model 對 chosen 版本打 3.5 分、rejected 打 1.0 分，則 \( s_w - s_r = 2.5 \)，\( \sigma(2.5) \approx 0.92 \)，loss 是 \( -\log(0.92) \approx 0.08 \)——很小，代表模型判斷準確。
  anchor_type: 數學推導
  comparison_target: rejected 版本的 1.0 分（與 chosen 版本 3.5 分的差為 2.5）
  importance: 10
  status: normal
- id: c11
  role: anchor
  text: 反過來如果打分方向弄反（chosen 反而拿低分），loss 會飆到 2.53 左右，梯度就會用力把它修回來
  source_quotes:
  - 反過來如果打分方向弄反（chosen 反而拿低分），loss 會飆到 2.53 左右，梯度就會用力把它修回來。
  anchor_type: 數學推導
  comparison_target: 打分方向正確時（chosen 3.5 分、rejected 1.0 分）loss 約 0.08
  importance: 11
  status: pending_author_confirmation
- id: c12
  role: evaluation
  text: 用成對比較而不是直接打分：直接打分在標註者之間的一致性很低，每個人心裡的同一個分數意義不一樣；但「A 跟 B 哪個比較好」人類直覺上容易判斷，共識度高得多；這也是論文的標註流程設計成 pairwise ranking 的原因
  source_quotes:
  - 因為直接打分（像是「請給 1 到 10 分」）在標註者之間的一致性很低，每個人心裡的 7 分不一樣；但「A 跟 B 哪個比較好」人類直覺上容易判斷，共識度高得多。這也是為什麼論文的標註流程設計成 pairwise ranking。
  anchor_type: 部落格判斷
  comparison_target: 直接打分（請給 1 到 10 分）
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: Bradley-Terry 有個已知的方法論缺陷：它依賴傳遞性假設（A>B 且 B>C 則 A>C），但人類偏好經常不滿足這個假設
  source_quotes:
  - Bradley-Terry 有個已知的方法論缺陷：它依賴傳遞性假設（A>B 且 B>C 則 A>C），但人類偏好經常不滿足這個假設。
  anchor_type: 部落格判斷
  importance: 13
  status: normal
- id: c14
  role: evaluation
  text: Persona-Aware-D2S「只保留多數決有共識的樣本、丟棄無共識樣本」的做法，某種程度上是在迴避傳遞性假設的問題，而不是真正解決它
  source_quotes:
  - 這篇論文「只保留多數決有共識的樣本、丟棄無共識樣本」的做法，某種程度上是在迴避這個問題，而不是真正解決它。
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 14
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

以下是很基本的通用詞，blog 沒有解釋，由撰寫者以一般知識補充；它們不是卡上的主張，不能當作 blog 的說法引用。

- **σ（sigmoid）**：把任意實數壓進 0 到 1 之間的函數，σ(x) = 1/(1+e^(-x))；分數差越大，σ 越接近 1。
- **reward model**：給候選輸出打分的模型，分數代表人類偏好的程度。
- **RLHF、PPO**：見 persona-d2s-task-and-pipeline 卡的名詞補充；**DPO** 見 decision-transformer-reward-conditioning 卡的名詞補充。
- **chosen / rejected**：偏好資料裡，人類選中的版本與被淘汰的版本。
- **傳遞性**：若 A 優於 B、B 優於 C，則 A 一定優於 C；人類偏好有時會出現 A>B、B>C 卻 C>A 的循環。
