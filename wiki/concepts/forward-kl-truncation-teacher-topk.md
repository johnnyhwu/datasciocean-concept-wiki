---
id: forward-kl-truncation-teacher-topk
title: forward KL 以老師的機率加權，蒸餾時截斷詞表要保留老師機率最高的前 K 名；The Tasteful Agent 論文取的卻是學生的前 100 名
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: tasteful-agent
  article_title: "The Tasteful Agent 解析：用 agent 跑過的軌跡，量測並訓練 AI 的決策品味"
  url: https://datasciocean.com/paper-intro/tasteful-agent/
  sections:
  - agent 的中途決策沒人量過，這篇論文用跑過的軌跡免費出題
  - 設定：同一個模型，老師多看一段答案
  - 為什麼學推理、用什麼損失：forward KL
  - 帶走三（脫離論文也成立）：forward KL 截斷時保留老師的前 K 名
  - 一句話總結
  - forward KL 在實作時怎麼截斷
  first_appearance: true
parent: null
related:
  - taste-fork-outcome-labels
  - taste-privileged-teacher-distillation
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: forward KL 截斷時，保留老師機率最高的前 K 名；判斷規則是截斷時保留「加權那一方」的高機率項
  source_quotes:
  - "forward KL 截斷時保留老師機率最高的前 K 名。"
  - "判斷規則（我的判斷，論文沒有對照實驗）：截斷時，保留「加權那一方」的高機率項。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 這是 blog 的判斷，論文沒有對照實驗
    source_quote: "判斷規則（我的判斷，論文沒有對照實驗）"
  importance: 1
  status: normal
- id: c2
  role: context
  text: 蒸餾時，學生要靠近老師的下一個 token 機率分布。詞表有十幾萬個 token，逐一算 KL 太貴，所以實作會截斷：只保留一部分 token，其餘合併成一格「其他」，機率總和仍是 1，沒有被丟掉
  source_quotes:
  - "蒸餾時，學生要靠近老師的下一個 token 機率分布。詞表有十幾萬個 token，逐一算 KL 太貴，所以實作會截斷：只保留一部分 token，其餘合併成一格「其他」。"
  - "其餘的合成一格「其他」，機率總和仍是 1，沒有被丟掉。"
  anchor_type: 背景說明
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 2
  status: normal
- id: c3
  role: mechanism
  text: 關鍵在於 forward KL 以老師的機率加權：D_KL(p_T ‖ p_S) 的每一項都乘上老師的機率 p_T(v)。老師給的機率很小的 token，貢獻幾乎是 0，可以安全地捨棄；老師給的機率高的 token，才是損失的主要來源
  source_quotes:
  - "關鍵在於 forward KL 是以老師的機率加權的："
  - "D_{KL}(p_T \\,\\|\\, p_S) = \\sum_{v} p_T(v) \\log \\frac{p_T(v)}{p_S(v)}"
  - "每一項都乘上 \\( p_T(v) \\)。老師給的機率很小的 token，貢獻幾乎是 0，可以安全地捨棄；老師給的機率高的 token，才是損失的主要來源。"
  anchor_type: 數學推導
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 2
  status: normal
- id: c4
  role: mechanism
  text: 一般知識：reverse KL 是以學生的機率加權，那種情況下保留學生的前 K 名才是自然的做法
  source_quotes:
  - "（一般知識：reverse KL 是以學生的機率加權，那種情況下保留學生的前 K 名才是自然的做法。）"
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c5
  role: context
  text: The Tasteful Agent 論文的蒸餾，老師與學生是同一個模型，老師的輸入多了正確答案；損失用 forward KL，在推理位置取的是學生機率最高的前 100 名，加上一格「其他」
  source_quotes:
  - "The Tasteful Agent 這篇論文"
  - "老師和學生是同一個模型，差別只在輸入內容。"
  - "privileged teacher（有特權資訊的老師）： 老師的輸入裡多了學生拿不到的資訊，這裡就是正確答案。"
  - "損失函數用的是 forward KL。"
  - "論文取的卻是學生的前 100 名，加上一格「其他」。"
  - "論文在推理位置保留的是學生機率最高的前 100 名"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 2
  status: normal
- id: c6
  role: mechanism
  text: 取學生前 100 名的缺口：如果老師想要的 token 不在學生的前 100 名（學生給它很低的機率），這個 token 就被併進「其他」，學生只被告知「榜外該多給一點機率」，不知道是哪個 token
  source_quotes:
  - "如果老師想要的 token 不在學生的前 100 名（學生給它很低的機率），這個 token 就被併進「其他」，學生只被告知「榜外該多給一點機率」，不知道是哪個 token。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 2
  status: normal
- id: c7
  role: anchor
  text: blog 自編的例子：學生給甲、乙、丁的機率是 0.5、0.3、0.01，老師是 0.2、0.1、0.6。用學生的前 2 名（甲、乙）分格，丁被併進「其他」，KL 約 0.58；用老師的前 3 名分格，丁自己一格，KL 約 2.10，這個例子的 token 已經全部列出，2.10 就是不截斷的完整 KL。用學生的前 K 名分格，在老師最在意的 token 上把損失低估了 3.6 倍，而且梯度指向的是整個「其他」，不是丁
  source_quotes:
  - "| 甲 | 0.5 | 0.2 |"
  - "| 乙 | 0.3 | 0.1 |"
  - "| 丁 | 0.01 | 0.6 |"
  - "用學生的前 2 名（甲、乙）分格，丁被併進「其他」（學生 0.20、老師 0.70）：KL \\( \\approx 0.2 \\ln(0.2/0.5) + 0.1 \\ln(0.1/0.3) + 0.7 \\ln(0.7/0.2) \\approx 0.58 \\)。"
  - "用老師的前 3 名（丁、甲、乙）分格，丁自己一格："
  - "\\approx 2.10 \\)。因為這個例子的 token 已經全部列出，2.10 就是不截斷的完整 KL。"
  - "也就是說，在這個例子裡，用學生的前 K 名分格，在老師最在意的 token 上把損失低估了 3.6 倍；而且梯度指向的是整個「其他」，不是丁。"
  anchor_type: 部落格舉例
  comparison_target: 不截斷的完整 KL 2.10
  importance: 3
  status: normal
- id: c8
  role: mechanism
  text: blog 推論：梯度會把所有榜外 token 依各自目前的機率比例一起抬高，老師想要的 token 本來機率就小，被抬高的幅度也小，所以學得慢
  source_quotes:
  - "我的推論：梯度會把所有榜外 token 依各自目前的機率比例一起抬高，老師想要的 token 本來機率就小，被抬高的幅度也小，所以學得慢。"
  anchor_type: 部落格推論
  importance: 4
  status: normal
- id: c9
  role: mechanism
  text: 依 KL 的方向決定截斷時保留誰的前 K 名：forward KL（以老師為目標，以 p_T 加權）保留老師的前 K 名；reverse KL（以 p_S 加權）保留學生的前 K 名；不確定、想保險時，取兩邊前 K 名的聯集，再加一格「其他」
  source_quotes:
  - "| forward KL（以老師為目標） | \\( p_T \\) | 老師的前 K 名 |"
  - "| reverse KL | \\( p_S \\) | 學生的前 K 名 |"
  - "| 不確定、想保險 | 無 | 兩邊前 K 名的聯集，再加一格「其他」 |"
  - "判斷規則（我的判斷，論文沒有對照實驗）"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c10
  role: evaluation
  text: 論文取學生前 100 名的原因沒有交代；blog 的猜測（推論，不是論文寫的）是，訓練時學生的 logits 本來就在手上，直接取它的前 100 名實作最簡單
  source_quotes:
  - "論文取學生前 100 名的原因沒有交代；一個合理的猜測是，訓練時學生的 logits 本來就在手上，直接取它的前 100 名實作最簡單。這個猜測是我的推論，不是論文寫的。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 4
  status: normal
- id: c11
  role: evaluation
  text: 論文原文只說「student 的前 100 名加一格剩餘機率」，沒有說老師那一邊怎麼處理；blog 推論，KL 是逐格比較老師和學生給同一格多少機率，兩邊的格子必須一樣才比得了，所以合理的做法是老師的分布也在同樣這 100 個 token 上讀出機率，剩下的也加總成「其他」
  source_quotes:
  - "論文原文只說「student 的前 100 名加一格剩餘機率」，沒有說老師那一邊怎麼處理。"
  - "我的推論：KL 是逐格比較「老師給這一格多少、學生給這一格多少」，兩邊的格子必須一樣才比得了，所以合理的做法是老師的分布也在同樣這 100 個 token 上讀出機率，剩下的也加總成「其他」。這是推論，不是論文明講的。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 4
  status: normal
- id: c12
  role: evaluation
  text: 截斷本身可以接受：forward KL 以老師的機率加權，老師機率很小的 token 貢獻幾乎是 0，所以只要保留的格子涵蓋了老師真正在意的 token，截斷損失得不多；問題出在「保留誰的前 100 名」
  source_quotes:
  - "為什麼截斷也能接受。 forward KL 以老師的機率加權，老師機率很小的 token 貢獻幾乎是 0，所以只要保留的格子涵蓋了老師真正在意的 token，截斷損失得不多。問題出在「保留誰的前 100 名」"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 3
  status: normal
- id: c13
  role: context
  text: 論文的其他省算力簡化：最後的選擇位置只比 A 和 B 兩格；推理位置的 KL 與選擇位置的 KL 各乘以 1 再相加；老師的推理最長可到 3,072 個 token，所以平均挑最多 512 個位置來算
  source_quotes:
  - "第二，最後的選擇位置：只比 A 和 B。"
  - "第三，總損失。 推理位置的 KL 與選擇位置的 KL 各乘以 1，再相加。"
  - "第四，長推理要抽樣。 老師的推理最長可到 3,072 個 token，全部位置都算太吃記憶體，所以平均挑最多 512 個位置來算。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 4
  status: normal
```

## 名詞補充（通用知識，非 blog 內容）

- KL 散度（KL divergence）：衡量兩個機率分布差多少的量，兩個分布完全相同時為 0，差越多越大；它不對稱，D_KL(P‖Q) 和 D_KL(Q‖P) 一般不相等。
- forward KL／reverse KL：蒸餾時以老師分布 p_T 為第一個參數的 D_KL(p_T‖p_S) 稱 forward KL，反過來的 D_KL(p_S‖p_T) 稱 reverse KL。
- 蒸餾（distillation）：訓練一個學生模型去模仿老師模型的輸出分布。
