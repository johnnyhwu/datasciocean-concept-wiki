---
id: pairwise-eval-swap-order-twice
title: LLM 做二選一時有 position bias；二選一的評測要每題考兩次，第二次把兩個選項的順序完全對調，兩次都答對才算對
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: tasteful-agent
  article_title: "The Tasteful Agent 解析：用 agent 跑過的軌跡，量測並訓練 AI 的決策品味"
  url: https://datasciocean.com/paper-intro/tasteful-agent/
  sections:
  - agent 的中途決策沒人量過，這篇論文用跑過的軌跡免費出題
  - 同任務、同前綴，結果的差異才能歸給判斷
  - 評分方式：順序對調考兩次，隨機基準是 25%
  - 帶走二（脫離論文也成立）：二選一的評測要對調順序考兩次
  first_appearance: true
parent: null
related:
  - taste-fork-outcome-labels
  - taste-bench-frontier-results
  - shared-context-batched-judgments
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: LLM 做二選一時有 position bias；二選一的評測要每題考兩次，第二次把兩個選項的順序完全對調，兩次都答對才算對
  source_quotes:
  - "LLM 做二選一時有 position bias。"
  - "做法是每題考兩次，第二次把兩個選項的順序完全對調，兩次都答對才算對："
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: position bias（位置偏誤）是模型傾向選第一個或第二個選項，跟內容無關；二選一的題目最容易受它影響，光是對調順序，很多模型的答案就會改變
  source_quotes:
  - "目的是排除 position bias（位置偏誤）：模型傾向選第一個或第二個選項，跟內容無關。二選一的題目最容易受它影響，光是對調順序，很多模型的答案就會改變。"
  anchor_type: 背景說明
  importance: 2
  status: normal
- id: c3
  role: context
  text: The Tasteful Agent 論文的 Taste-Bench（502 題、每題從兩個候選方向中選一個的評測集）就用這個計分：第一次用每題固定的種子順序呈現 A、B（所有模型共用同一個順序），第二次完全反過來，兩次都答對這題才算對，無法解析出答案的回應算錯
  source_quotes:
  - "The Tasteful Agent 這篇論文"
  - "用這個方法，論文造出一個 502 題的評測集 Taste-Bench。"
  - "只問模型「這兩個方向，你選哪個？」"
  - "第一次：用每題固定的種子順序呈現 A、B（所有模型共用同一個順序）。"
  - "第二次：完全反過來。"
  - "兩次都答對，這題才算對。無法解析出答案的回應算錯。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 如果只考一次，一個永遠回答「A」的模型，在 A、B 各半的題庫上會得到 50%，而這個 50% 完全不代表它有判斷力；偏誤只有部分的模型也一樣，分數裡混了「碰巧順序對自己有利」的成分
  source_quotes:
  - "如果只考一次，一個永遠回答「A」的模型，在 A、B 各半的題庫上會得到 50%，而這個 50% 完全不代表它有判斷力。偏誤只有部分的模型也一樣，分數裡混了「碰巧順序對自己有利」的成分。"
  anchor_type: 部落格推論
  comparison_target: A、B 各半的題庫上，只考一次的計分
  importance: 2
  status: normal
- id: c5
  role: anchor
  text: 兩次都對才算對的計分下，每次各 1/2 機率亂猜得 25%，永遠選同一個位置得 0%（兩次中必有一次錯）；所以這個指標的隨機基準線是 25%，不是 50%
  source_quotes:
  - "兩次都答對，這題才算對。"
  - "| 每次各 1/2 的機率亂猜 | \\( \\frac{1}{2} \\times \\frac{1}{2} = 25\\% \\) |"
  - "| 永遠選同一個位置 | 0%（兩次中必有一次錯） |"
  - "所以這個指標的隨機基準線是 25%，不是 50%。"
  anchor_type: 數學推導
  comparison_target: 只考一次時的隨機基準 50%
  importance: 2
  status: normal
- id: c6
  role: mechanism
  text: 答案會隨順序翻轉的題，不算作有品味
  source_quotes:
  - "答案會隨順序翻轉的題，不算作有品味。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c7
  role: anchor
  text: 用論文的數字看效果：GPT-5.6 Sol 兩次都對 292 題、只有第一次對 25 題、只有第二次對 29 題、兩次都錯 156 題，共 502 題，502 題直接合併的嚴格準確率是 292/502 = 58.2%；只對一次的 25 + 29 = 54 題（10.8%）答案會隨順序改變，單考一次這些題會有一半被算成答對，嚴格計分把它們全部排除
  source_quotes:
  - "用 GPT-5.6 Sol 驗算（見表 3）：兩次都對（CC）292 題、只有第一次對（CW）25 題、只有第二次對（WC）29 題、兩次都錯（WW）156 題，加起來 502 題。直接合併的嚴格準確率是 \\( 292 / 502 = 58.2\\% \\)。"
  - "用論文的數字看效果：GPT-5.6 Sol 只對一次的 \\( 25 + 29 = 54 \\) 題（10.8%）答案會隨順序改變，單考一次這些題會有一半被算成答對，嚴格計分把它們全部排除。"
  anchor_type: 部落格考證
  comparison_target: 全部 502 題
  qualifiers:
  - text: 58.2% 是 502 題直接合併的嚴格準確率；論文開頭的 59.7% 是 Average（工程 56.9%、研究 62.5% 取 1:1 平均），兩者不同
    source_quote: "直接合併的嚴格準確率是 \\( 292 / 502 = 58.2\\% \\)。開頭的 59.7% 是 Average：工程 56.9%、研究 62.5%，取 1:1 平均得"
  figures:
  - file: figures/tasteful-agent/table4.png
    article: tasteful-agent
    src: table4.png
    caption: 表 3 — 14 個模型的完整結果。P 與 D 代表平行與繞路，Eng 與 Res 代表工程與研究；Unparsed 是 1,004 次作答中無法解析出答案的次數。（來源：原始論文 Table 4。）
    sha256: 6d4876dedbf2cbbdcdb278efc8e06c54d72f5d2d977e9b64768dc09036e9c829
  importance: 3
  status: normal
- id: c8
  role: context
  text: 論文報告三個指標：accuracy（嚴格準確率，兩次都答對的題數占全部題數的比例，主要指標）；mean accuracy（把 502 × 2 = 1,004 次作答各自計分，只對一次的題也算一半，比較寬鬆）；Average（研究類與工程類各自算嚴格準確率後取 1:1 平均）
  source_quotes:
  - "accuracy（嚴格準確率）： 兩次都答對的題數占全部題數的比例，這是主要指標。"
  - "mean accuracy： 把 \\( 502 \\times 2 = 1{,}004 \\) 次作答各自計分，只對一次的題也算一半，比較寬鬆。"
  - "Average： 研究類與工程類各自算嚴格準確率後，取 1:1 平均。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 4
  status: normal
- id: c9
  role: evaluation
  text: 代價是推論成本加倍，分數會比習慣的數字低；可以另外報告「兩次作答各自計分」的較寬鬆版本，兩個數字的差距本身就反映模型對位置的敏感度
  source_quotes:
  - "代價是推論成本加倍，分數會比習慣的數字低；可以另外報告「兩次作答各自計分」的較寬鬆版本，兩個數字的差距本身就反映模型對位置的敏感度。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c10
  role: evaluation
  text: 任何兩兩比較的 LLM 評審（pairwise judge、A/B 偏好評測）都可以套用這個做法
  source_quotes:
  - "任何兩兩比較的 LLM 評審（pairwise judge、A/B 偏好評測）都可以套用。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
```
