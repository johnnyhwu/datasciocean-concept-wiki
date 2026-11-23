---
id: bash-add-ons-no-detectable-gain
title: 在 Bash 上再加 typed tools 或自造工具，沒看到分數好處、只多花 token；但「看不出差異」不等於「沒有差異」，能排除的只是大於約 2 到 3 pp 的好處
type_hint: 判斷
context_type: bound_to_source
sources:
- article: is-bash-all-you-need
  article_title: "Is Bash All You Need？只給 agent 一個 shell，比整套專用工具更準又更省"
  url: https://datasciocean.com/paper-intro/is-bash-all-you-need/
  sections:
  - 只給 agent 一個 shell，分數反而更高
  - 怎麼比才公平：同一個模型、同一份任務，只換 agent 的雙手
  - 五種工具介面
  - 兩個企業工作 benchmark，typed tools 來源不同
  - 怎麼算分：分數、通過率、token 與配對差
  - Bash 對 Tool-only：四組設定全部同向
  - 在 Bash 上再加工具，沒有加分，只多花 token
  - Bash 為什麼比較好：agent 拿 shell 寫小程式
  - 這份證據能信幾分
  - 該怎麼選：先問合規，再問能不能隔離
  - 延伸：typed tools 加 exec 的混合架構，論文沒測到什麼
  - 延伸：看不出差異不等於沒有差異
  first_appearance: true
parent: null
related:
  - bash-vs-typed-tools-results
  - ptc-batching-vs-reach
  - baseline-who-built-it
  - intermediate-results-out-of-context
  - claude-code-permission-blast-radius
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 在 Bash 上再加東西，沒看到分數好處：typed tools 與自造工具都只是讓 token 變多；但「看不出差異」不等於「沒有差異」，加 typed tools 或自造工具在分數上「看不出差異」，能排除的只是「大於約 2 到 3 pp 的好處」，比這小的效果，這個實驗不能證明也不能否定
  source_quotes:
  - "在 Bash 上再加東西，沒看到分數好處。 typed tools 與自造工具都只是讓 token 變多"
  - "「看不出差異」不等於「沒有差異」"
  - "加 typed tools 或自造工具，在分數上「看不出差異」，能排除的只是「大於約 2 到 3 pp 的好處」；比這小的效果，這個實驗不能證明也不能否定。"
  anchor_type: 部落格判斷
  comparison_target: 只有 Bash（純 Bash），同一題、同一模型的配對
  qualifiers:
  - text: token 變多有一個例外：八格裡只有 TheAgentCompany／Opus-4.8 的 Bash+Synthesis 比純 Bash 便宜，論文自己也把它列為唯一例外
    source_quote: "八格裡只有 TheAgentCompany／Opus-4.8 的 Bash+Synthesis 比純 Bash 便宜，論文自己也把它列為唯一例外，其餘都是 token 變多。"
  - text: 這篇沒有量測 typed tool 的輸出整理、權限控管、稽核，這些好處不在分數裡，不能視為被否定
    source_quote: "第一，這篇沒有量測 typed tool 的輸出整理、權限控管、稽核，這些好處不在分數裡，不能視為被否定。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: "論文〈Is Bash All You Need? An Empirical Study of Tool Interfaces for Enterprise Digital Worker Agents〉（Microsoft、CMU）比的是企業 agent 的工具介面（tool interface），也就是 agent 用什麼方式對環境下動作：一端是 typed tool，預先定義好名稱與參數格式的函式，模型一次呼叫一個；另一端是直接給一個 bash shell（命令列），讓模型自己寫指令。論文作者用同一個模型、同一份任務文字、同一份基礎 prompt、同一套停止條件，只改變「agent 能怎麼動手」"
  source_quotes:
  - "Is Bash All You Need? An Empirical Study of Tool Interfaces for Enterprise Digital Worker Agents（Microsoft、CMU"
  - "論文比的是工具介面（tool interface），也就是 agent 用什麼方式對環境下動作。一端是 typed tool：預先定義好名稱與參數格式的函式，例如 gitlab_create_issue，模型一次呼叫一個；另一端是直接給一個 bash shell（命令列），讓模型自己寫指令。"
  - "論文作者用同一個模型、同一份任務文字、同一份基礎 prompt、同一套停止條件，只改變「agent 能怎麼動手」"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: 這裡比較的三種介面：Bash 只有 shell；Bash+Tool 是 shell 加 typed tools，兩者並存，agent 自己選；Bash+Synthesis 是 shell 加一個持久資料夾，prompt 鼓勵 agent 把常用步驟寫成可重用腳本，後續任務直接呼叫，任務依序執行，資料夾會保留
  source_quotes:
  - "Bash | 只有 shell"
  - "Bash+Tool | shell 加 typed tools | 兩者並存，agent 自己選"
  - "Bash+Synthesis | shell 加一個持久資料夾 | prompt 鼓勵 agent 把常用步驟寫成可重用腳本，後續任務直接呼叫，藉此減少重新摸索的成本；任務依序執行，資料夾會保留"
  anchor_type: 設計參數
  qualifiers:
  - text: Bash+Synthesis 額外加了介面專屬的 prompt 指示，Bash 與 Bash+Tool 共用同一份基礎 prompt
    source_quote: "只有 Bash+Synthesis 與 PTC 額外加了介面專屬的 prompt 指示，其餘介面共用同一份基礎 prompt。"
  importance: 2
  status: normal
- id: c4
  role: context
  text: 兩個企業工作 benchmark：TheAgentCompany 模擬軟體公司，typed tools 由論文作者自己設計；APEX-Agents 模擬投資銀行、管理顧問、公司法務的專業分析，typed tools 是 benchmark 原有的。測試的模型是 Opus-4.8 與 GPT-5.5
  source_quotes:
  - "TheAgentCompany（模擬軟體公司的 benchmark）"
  - "APEX-Agents（模擬投資銀行、顧問、法務專業分析的 benchmark）"
  - "benchmark 沒有現成的，論文作者自己設計 60 個"
  - "benchmark 原有的 20 個"
  - "測試的模型是 Opus-4.8 與 GPT-5.5"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 3
  status: normal
- id: c5
  role: context
  text: 配對分數差是同一題、同一模型、兩種介面的分數相減，再對所有題取平均，單位 pp 是百分點；信賴區間用 bootstrap 算，是從配對任務重複抽樣、重算平均差，看結果散布的範圍
  source_quotes:
  - "配對分數差（pp） | 同一題、同一模型、兩種介面的分數相減，再對所有題取平均 | 兩種介面的淨差距；pp 是百分點"
  - "95% bootstrap 信賴區間 | 從配對任務重複抽樣、重算平均差，看結果散布的範圍"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 定義
  importance: 3
  status: normal
- id: c6
  role: evidence
  text: 加 typed tools（Bash+Tool − Bash）的配對分數差：TheAgentCompany −0.6 pp [−3.0, +1.9]，APEX-Agents −0.2 pp [−2.4, +1.9]
  source_quotes:
  - "Bash+Tool − Bash（加 typed tools） | −0.6 pp [−3.0, +1.9] | −0.2 pp [−2.4, +1.9]"
  - "加了什麼 | TheAgentCompany | APEX-Agents"
  - "下表是分數差，正數代表加了比較好："
  anchor_type: 實驗結果
  comparison_target: 純 Bash，同一題、同一模型的配對
  figures:
  - file: figures/is-bash-all-you-need/table9.png
    article: is-bash-all-you-need
    src: table9.png
    caption: 表 9 — 各介面兩兩比較的配對分數差，正數代表前者較好，括號內為 95% bootstrap 信賴區間（來源：原始論文 Table 9。）
    sha256: 10f313801a2a3f6747b24d6f147dc27bc494d796f507cab2cb5214f133ce88e2
  importance: 2
  status: normal
- id: c7
  role: evidence
  text: 加自造腳本（Bash+Synthesis − Bash）的配對分數差：TheAgentCompany −1.6 pp [−3.6, +0.3]，APEX-Agents −0.2 pp [−2.4, +2.0]
  source_quotes:
  - "Bash+Synthesis − Bash（加自造腳本） | −1.6 pp [−3.6, +0.3] | −0.2 pp [−2.4, +2.0]"
  - "加了什麼 | TheAgentCompany | APEX-Agents"
  - "下表是分數差，正數代表加了比較好："
  anchor_type: 實驗結果
  comparison_target: 純 Bash，同一題、同一模型的配對
  figures:
  - file: figures/is-bash-all-you-need/table9.png
    article: is-bash-all-you-need
    src: table9.png
    caption: 表 9 — 各介面兩兩比較的配對分數差，正數代表前者較好，括號內為 95% bootstrap 信賴區間（來源：原始論文 Table 9。）
    sha256: 10f313801a2a3f6747b24d6f147dc27bc494d796f507cab2cb5214f133ce88e2
  importance: 2
  status: normal
- id: c8
  role: evaluation
  text: 這四個區間都跨過 0，看不出差異；但「看不出」不等於「證明沒有」：以這些區間的寬度，這個實驗只能排除大於約 2 到 3 pp 的好處，比這小的效果它量不出來
  source_quotes:
  - "四個區間都跨過 0，看不出差異。但「看不出」不等於「證明沒有」：以這些區間的寬度，這個實驗只能排除大於約 2 到 3 pp 的好處，比這小的效果它量不出來。"
  anchor_type: 部落格考證
  comparison_target: 純 Bash，同一題、同一模型的配對
  qualifiers:
  - text: 似乎每個「任務乘模型」只跑一次（blog 的推論，論文未說明），信賴區間是對任務取樣，「看不出差異」的那幾組結論能排除的效果大小因此有限
    source_quote: "似乎每個「任務乘模型」只跑一次（我的推論，論文未說明）。信賴區間是對任務取樣，「看不出差異」的那幾組結論（加 typed tools、自造工具）能排除的效果大小因此有限。"
  importance: 2
  status: normal
- id: c9
  role: evidence
  text: 加了東西之後，每題總 token 多半變多，例如 TheAgentCompany／Opus-4.8 從 Bash 的 264k 變成 Bash+Tool 的 569k；八格裡只有 TheAgentCompany／Opus-4.8 的 Bash+Synthesis（249k）比純 Bash 便宜，論文自己也把它列為唯一例外，其餘都是 token 變多
  source_quotes:
  - "設定 | Bash | Bash+Tool | Bash+Synthesis"
  - "TheAgentCompany／Opus-4.8 | 264k／0.37 | 569k／0.55 | 249k／0.35"
  - "加了東西之後的 token 與成本（每格為 Total tokens／每題成本，單位美元）："
  - "八格裡只有 TheAgentCompany／Opus-4.8 的 Bash+Synthesis 比純 Bash 便宜，論文自己也把它列為唯一例外，其餘都是 token 變多。"
  anchor_type: 實驗結果
  comparison_target: 純 Bash，同 benchmark、同模型
  importance: 3
  status: normal
- id: c10
  role: evidence
  text: 有了 typed tools，剩下的 shell 呼叫沒有更可靠：shell 呼叫的失敗率 Bash+Tool 對純 Bash 是 10.8% 對 7.9%（TheAgentCompany）、9.3% 對 4.4%（APEX-Agents）；加 typed tools 只是少用 shell，剩下的沒變好
  source_quotes:
  - "有了 typed tools，剩下的 shell 呼叫沒有更可靠。失敗率 Bash+Tool 對純 Bash 是 10.8% 對 7.9%（TheAgentCompany）、9.3% 對 4.4%（APEX-Agents）。加 typed tools 只是少用 shell，剩下的沒變好。"
  anchor_type: 實驗結果
  comparison_target: 純 Bash
  importance: 3
  status: normal
- id: c11
  role: evidence
  text: Opus-4.8 在 TheAgentCompany 創造了 21 個工具，其中 12 個在後續任務再被用到；有呼叫自造工具的任務，相對純 Bash 的平均分數差是 −0.6 pp（TheAgentCompany）與 +0.1 pp（APEX-Agents），APEX-Agents 的 token 中位數還多 31.4k；這份資料裡看不到自造工具的價值
  source_quotes:
  - "Opus-4.8 在 TheAgentCompany 創造了 21 個工具，其中 12 個在後續任務再被用到；有呼叫自造工具的任務，相對純 Bash 的平均分數差是 −0.6 pp（TheAgentCompany）與 +0.1 pp（APEX-Agents），APEX-Agents 的 token 中位數還多 31.4k。這份資料裡看不到自造工具的價值。"
  anchor_type: 實驗結果
  comparison_target: 純 Bash
  qualifiers:
  - text: 有沒有呼叫自造工具的分組比較，是兩個模型合併計算
    source_quote: "Bash+Synthesis 相對 Bash 的配對差，依該任務有沒有呼叫自造工具分組，兩個模型合併計算"
    source: figure_caption
  figures:
  - file: figures/is-bash-all-you-need/table5.png
    article: is-bash-all-you-need
    src: table5.png
    caption: 表 5 — Bash+Synthesis 相對 Bash 的配對差，依該任務有沒有呼叫自造工具分組，兩個模型合併計算（來源：原始論文 Table 5。）
    sha256: 1f17fa0af65b7f3141cf76591a3fe16b6a2b143aa615e9f1a1ee2c9cc3a0dc4a
  importance: 4
  status: normal
- id: c12
  role: mechanism
  text: 實驗只能說「兩種做法的分數差異，在這批資料裡沒有明顯到能確認」，不能說「保證沒有影響」；信賴區間的寬度，就是這個實驗能偵測到的最小差距的粗略尺度
  source_quotes:
  - "實驗只能說「兩種做法的分數差異，在這批資料裡沒有明顯到能確認」，不能說「保證沒有影響」；信賴區間的寬度，就是這個實驗能偵測到的最小差距的粗略尺度。"
  - "〈這份證據能信幾分〉的評估與延伸段落的判斷方法是筆記作者的看法"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c13
  role: anchor
  text: 類比：一個只能量到正負 2 公斤的體重計，吃了一餐、多了 0.5 公斤，它顯示不出來，但這不代表沒變重，只是儀器的雜訊比變化本身大；任務與模型本身的隨機性，會讓平均差有一個抖動範圍，效果小於這個抖動就被淹沒
  source_quotes:
  - "類比：一個只能量到正負 2 公斤的體重計。你吃了一餐、多了 0.5 公斤，它顯示不出來，但這不代表你沒變重，只是儀器的雜訊比變化本身大。這個類比成立的原因是：任務與模型本身的隨機性，會讓平均差有一個抖動範圍，效果小於這個抖動就被淹沒。"
  anchor_type: 部落格舉例
  numeric_kind: non_comparative
  numeric_reason: 假設題設
  importance: 3
  status: normal
- id: c14
  role: evaluation
  text: 單次執行的隨機性沒有被單獨量化：配對任務數 348 = 174 × 2、960 = 480 × 2，似乎每個「任務乘模型」只跑一次（blog 的推論，論文未說明）；信賴區間是對任務取樣，「看不出差異」的那幾組結論（加 typed tools、自造工具）能排除的效果大小因此有限
  source_quotes:
  - "單次執行的隨機性沒有被單獨量化。 配對任務數 348 = 174 × 2、960 = 480 × 2，似乎每個「任務乘模型」只跑一次（我的推論，論文未說明）。信賴區間是對任務取樣，「看不出差異」的那幾組結論（加 typed tools、自造工具）能排除的效果大小因此有限。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 3
  status: normal
- id: c15
  role: evaluation
  text: 給 agent 一組 typed tools 再加一個 exec（執行 shell 指令）的工具，是常見的實務架構，也就是論文的 Bash+Tool；論文的數據說它比只有 typed tools 好很多、和純 Bash 沒有可偵測的差別，但論文測的 typed tools 不一定是精心整理過輸出的那種
  source_quotes:
  - "給 agent 一組 typed tools，再加一個 exec（執行 shell 指令）的工具，是常見的實務架構，也就是論文的 Bash+Tool。論文的數據說它比只有 typed tools 好很多、和純 Bash 沒有可偵測的差別，但論文測的 typed tools 不一定是精心整理過輸出的那種。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c16
  role: evaluation
  text: 論文沒有測到三件事：typed tool 的輸出有沒有被整理（論文未說明）、穩定度（沒有報告重複執行同一任務的變異）、權限管控與稽核（不在分數裡）；所以「有做輸出處理的 typed tool 帶來穩定度」這個實務論點，論文既沒有支持，也沒有反駁
  source_quotes:
  - "typed tool 的輸出有沒有被整理：論文說明了工具清單，但沒有說明工具回傳的內容做過多少處理（論文未說明）。"
  - "穩定度：論文報告平均分數與信賴區間，沒有報告重複執行同一任務的變異"
  - "權限管控與稽核：這些不在分數裡。"
  - "所以「有做輸出處理的 typed tool 帶來穩定度」這個實務論點，論文既沒有支持，也沒有反駁。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c17
  role: evaluation
  text: 只要 agent 手上有 exec，typed tool 就不能單獨當作權限邊界：agent 可以直接用 curl 打同一個 API，繞過 typed tool 的限制；選 typed tools 的目的若是權限控管或稽核，就要確保 exec 拿不到同樣的憑證與網路路徑（blog 的推論）
  source_quotes:
  - "安全面的一個提醒（我的推論）。只要 agent 手上有 exec，typed tool 就不能單獨當作權限邊界：agent 可以直接用 curl 打同一個 API，繞過 typed tool 的限制。如果選 typed tools 的目的是權限控管或稽核，就要確保 exec 拿不到同樣的憑證與網路路徑，否則兩者並存等於沒有限制。"
  anchor_type: 部落格推論
  importance: 4
  status: normal
```
