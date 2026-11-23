---
id: baseline-who-built-it
title: 看到「A 贏 B」，先檢查 B 是誰做的：觀察到的差距等於方法本身的功勞，加上 B 被做得多弱，當 B 是提案者自己設計的，第二項常被低估
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: is-bash-all-you-need
  article_title: "Is Bash All You Need？只給 agent 一個 shell，比整套專用工具更準又更省"
  url: https://datasciocean.com/paper-intro/is-bash-all-you-need/
  sections:
  - 只給 agent 一個 shell，分數反而更高
  - 五種工具介面
  - 兩個企業工作 benchmark，typed tools 來源不同
  - 怎麼算分：分數、通過率、token 與配對差
  - Bash 對 Tool-only：四組設定全部同向
  - PTC：省了 token，分數沒跟上
  - 這份證據能信幾分
  - 該怎麼選：先問合規，再問能不能隔離
  - 延伸：看到 A 贏 B，先檢查 B 是誰做的
  first_appearance: true
parent: null
related:
  - bash-vs-typed-tools-results
  - bash-add-ons-no-detectable-gain
  - ptc-batching-vs-reach
  - intermediate-results-out-of-context
  - ragu-results-peeling-confounds
  - decisionrag-speedup-deployment-fairness
  - stateful-and-budget-matched-controls
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 任何「新做法 A 贏過舊做法 B」的結果，都等於方法本身的功勞，加上 B 被做得多弱；當 B 是提案者自己設計的，第二項常被低估
  source_quotes:
  - "任何「新做法 A 贏過舊做法 B」的結果，都等於方法本身的功勞，加上 B 被做得多弱；當 B 是提案者自己設計的，第二項常被低估。"
  - "〈這份證據能信幾分〉的評估與延伸段落的判斷方法是筆記作者的看法"
  anchor_type: 部落格判斷
  importance: 1
  status: normal
- id: c2
  role: context
  text: "論文〈Is Bash All You Need? An Empirical Study of Tool Interfaces for Enterprise Digital Worker Agents〉（Microsoft、CMU）比較企業 agent 的工具介面，一端是 typed tool（預先定義好名稱與參數格式的函式），另一端是直接給一個 bash shell（命令列）；只有 typed tools 的 Tool-only 是基準線"
  source_quotes:
  - "Is Bash All You Need? An Empirical Study of Tool Interfaces for Enterprise Digital Worker Agents（Microsoft、CMU"
  - "論文比的是工具介面（tool interface）"
  - "一端是 typed tool：預先定義好名稱與參數格式的函式"
  - "另一端是直接給一個 bash shell（命令列）"
  - "Tool-only | 只有 typed tools | 每個動作一次獨立呼叫，是基準線"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: mechanism
  text: 拆解一個比較結果：觀察到的差距 = A 本身的功勞 + B 被做得多弱造成的落差 + 雜訊；A 本身的功勞是真正想知道的東西，B 被做得多弱造成的落差是基準線的設計、調校、覆蓋範圍不如 A 所造成的差距，雜訊是任務與模型的隨機性，用信賴區間估計
  source_quotes:
  - '\text{觀察到的差距} = \text{A 本身的功勞} + \text{B 被做得多弱造成的落差} + \text{雜訊}'
  - "A 本身的功勞：我們真正想知道的東西。"
  - "B 被做得多弱造成的落差：基準線的設計、調校、覆蓋範圍不如 A 所造成的差距。"
  - "雜訊：任務與模型的隨機性，用信賴區間估計。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c4
  role: mechanism
  text: 論文只能量到等號左邊、表格上看到的總差距；這個差距裡「A 本身的功勞」和「B 被做得多弱造成的落差」各占多少，要靠讀者判斷
  source_quotes:
  - "論文只能量到等號左邊、表格上看到的總差距（雜訊用信賴區間估計）；這個差距裡「A 本身的功勞」和「B 被做得多弱造成的落差」各占多少，要靠讀者判斷。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c5
  role: anchor
  text: 這篇論文裡的兩層混淆之一：Bash 對 Tool-only 在 TheAgentCompany 是 +24.6 pp，但 Tool-only 的 60 個工具是論文作者自己設計，只涵蓋任務相關的 API，不是 shell 能碰到的所有端點；相對乾淨的參考是 APEX-Agents，它的 20 個工具是 benchmark 原有的，差距只剩 +6.2 pp
  source_quotes:
  - "Bash 對 Tool-only（TheAgentCompany，+24.6 pp） | Tool-only 的 60 個工具是論文作者自己設計，只涵蓋任務相關的 API，不是 shell 能碰到的所有端點（Appendix B.1） | APEX-Agents 的 20 個工具是 benchmark 原有的，差距只剩 +6.2 pp"
  - "比較 | 混進去的其他變因 | 相對乾淨的參考"
  - "這篇論文裡的兩層混淆。"
  - "同一題、同一模型、兩種介面的分數相減，再對所有題取平均"
  - "下表是以配對任務算出的平均分數差（摘自表 9）。"
  - "APEX-Agents（960 個配對） | +6.2 pp | [+3.6, +8.7]"
  anchor_type: 部落格考證
  comparison_target: Tool-only，同一題、同一模型的配對（配對分數差）
  qualifiers:
  - text: +24.6 pp 是配對分數差，比逐格相減的範圍（最高 24.5）略高一點，兩邊的算法不同，論文沒有說明這個小出入的來源
    source_quote: "TheAgentCompany 的 +24.6 pp 比上面逐格相減的範圍（最高 24.5）略高一點，兩邊的算法不同，論文沒有說明這個小出入的來源。"
  - text: APEX-Agents 的 20 個工具相對乾淨，但不是完全乾淨（blog 的推論）
    source_quote: "APEX-Agents 的 20 個工具是 benchmark 原有的，相對乾淨，但不是完全乾淨（我的推論）。"
  importance: 2
  status: normal
- id: c6
  role: evidence
  text: 兩層混淆的另一層：Bash 對 PTC（模型寫 Python、程式裡只能呼叫 typed tools 的介面）是 +21.2 pp 與 +7.7 pp，PTC 只能呼叫目錄內的函式，所以差距混著「程式化呼叫的做法」與「目錄夠不夠用」；PTC 的受限 Python 執行環境也是論文作者自己實作；這一組論文沒有提供相對乾淨的參考
  source_quotes:
  - "Bash 對 PTC（+21.2 pp 與 +7.7 pp） | PTC 只能呼叫目錄內的函式，所以差距混著「程式化呼叫的做法」與「目錄夠不夠用」；PTC 的受限 Python 執行環境也是論文作者自己實作 | 論文沒有提供"
  - "比較 | 混進去的其他變因 | 相對乾淨的參考"
  - "PTC | 模型寫 Python，程式裡只能呼叫 typed tools"
  - "這篇論文裡的兩層混淆。"
  - "配對分數差（表 9）給出一致的結論："
  - "Bash − PTC：+21.2 pp [+17.0, +25.5] 與 +7.7 pp [+5.2, +10.2]"
  - "同一題、同一模型、兩種介面的分數相減，再對所有題取平均"
  anchor_type: 部落格考證
  comparison_target: PTC，同一題、同一模型的配對
  qualifiers:
  - text: 「目錄只涵蓋任務相關 API」只針對 TheAgentCompany 自建的那 60 個工具，所以這個混淆主要影響 TheAgentCompany 的結論
    source_quote: "範圍要記清楚：Appendix B.1 講的「目錄只涵蓋任務相關 API」只針對 TheAgentCompany 自建的那 60 個工具，所以這個混淆主要影響 TheAgentCompany 的結論。"
  importance: 3
  status: normal
- id: c7
  role: qualifier
  text: 範圍：「目錄只涵蓋任務相關 API」只針對 TheAgentCompany 自建的那 60 個工具，所以這個混淆主要影響 TheAgentCompany 的結論
  source_quotes:
  - "範圍要記清楚：Appendix B.1 講的「目錄只涵蓋任務相關 API」只針對 TheAgentCompany 自建的那 60 個工具，所以這個混淆主要影響 TheAgentCompany 的結論。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 計數
  importance: 3
  status: normal
- id: c8
  role: evaluation
  text: 兩個 benchmark 的差距差了四倍（+24.6 對 +6.2），論文沒有拆解原因；blog 推論至少有一部分來自「TheAgentCompany 的基準線是自製的」，另一部分來自任務類型不同（寫程式與跨系統，對上專業分析），兩者各占多少，這份資料回答不了
  source_quotes:
  - "兩個 benchmark 的差距差了四倍（+24.6 對 +6.2），論文沒有拆解原因。我的推論是：至少有一部分來自「TheAgentCompany 的基準線是自製的」，另一部分來自任務類型不同（寫程式與跨系統，對上專業分析）。兩者各占多少，這份資料回答不了。"
  anchor_type: 部落格推論
  comparison_target: APEX-Agents 的 +6.2 pp（兩者都是 Bash 對 Tool-only 的配對分數差）
  importance: 2
  status: normal
- id: c9
  role: mechanism
  text: 三問檢查法的前兩問：基準線是誰設計的？提案者自己做的基準線，要先假設它沒被調到最好；有沒有被投入同等的力氣？同樣的 prompt 調校、同樣的超參數搜尋、同樣的工具覆蓋範圍
  source_quotes:
  - "基準線是誰設計的？ 提案者自己做的基準線，要先假設它沒被調到最好。"
  - "有沒有被投入同等的力氣？ 同樣的 prompt 調校、同樣的超參數搜尋、同樣的工具覆蓋範圍。"
  - "三問檢查法。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c10
  role: mechanism
  text: 三問檢查法的第三問：有沒有另一個來源的基準線可以交叉驗證？兩個來源給出的差距差很多，就代表基準線品質在影響結果；這篇剛好有：自製目錄與 benchmark 原有目錄
  source_quotes:
  - "有沒有另一個來源的基準線可以交叉驗證？ 兩個來源給出的差距差很多，就代表基準線品質在影響結果。這篇剛好有：自製目錄與 benchmark 原有目錄。"
  anchor_type: 部落格判斷
  importance: 2
  status: normal
- id: c11
  role: context
  text: 其他常見的基準線陷阱（一般知識，不是論文內容）：基準線用預設超參數、提案方法卻調過；基準線的 prompt 沒有針對它調整；基準線用的模型較弱，或給的運算預算較少；兩邊用不同的 harness（執行環境與評分程式）
  source_quotes:
  - "其他常見的基準線陷阱（一般知識，不是論文內容）："
  - "基準線用預設超參數，提案方法卻調過。"
  - "基準線的 prompt 沒有針對它調整。"
  - "基準線用的模型較弱，或給的運算預算較少。"
  - "兩邊用不同的 harness（執行環境與評分程式）。"
  anchor_type: 背景說明
  importance: 4
  status: normal
- id: c12
  role: evaluation
  text: 在自己的評估裡，把基準線當成一個要認真對待的系統：給它與新方法相同的調校預算，並且盡量另找一個外部來源的基準線來對照；報告結果時，把「同一個條件下只差一個變因」的兩組數字挑出來，那組才是方法本身的功勞
  source_quotes:
  - "把基準線當成一個要認真對待的系統：給它與新方法相同的調校預算，並且盡量另找一個外部來源的基準線來對照。報告結果時，把「同一個條件下只差一個變因」的兩組數字挑出來，那組才是方法本身的功勞。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c13
  role: evaluation
  text: blog 認為這篇論文的研究價值偏低：論文沒有提出新方法，也沒有新的分析框架，貢獻是把五種介面放進同一個受控設定裡比較；這類論文的價值取決於基準線公不公平，而這一點正是它最弱的地方
  source_quotes:
  - "研究價值偏低。 論文沒有提出新方法，也沒有新的分析框架，貢獻是把五種介面放進同一個受控設定裡比較。這類論文的價值取決於基準線公不公平，而這一點正是它最弱的地方（見下面的缺點）。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
- id: c14
  role: evaluation
  text: 論文摘要沒有明顯誇大，摘要的 21.8 到 24.5 pp 與 4.8 到 7.4 pp 就是四格結果的範圍；但它把幅度較大、且基準線問題最嚴重的 TheAgentCompany 放在前面
  source_quotes:
  - "摘要有被包裝嗎？ 沒有明顯誇大：摘要的 21.8 到 24.5 pp 與 4.8 到 7.4 pp 就是四格結果的範圍。但它把幅度較大、且基準線問題最嚴重的 TheAgentCompany 放在前面。"
  - "Bash 對比只有 typed tools，分數在"
  anchor_type: 部落格判斷
  comparison_target: 只有 typed tools（Tool-only）
  importance: 4
  status: normal
- id: c15
  role: context
  text: 這是 blog 讀這篇論文的過程裡整理出來的幾個判斷方法之一，blog 說這些判斷方法脫離這篇論文也成立
  source_quotes:
  - "比較耐用的是讀它的過程裡整理出來的幾個判斷方法"
  - "下面這些判斷方法脫離這篇論文也成立"
  - "看到「A 贏 B」，先檢查 B 是誰做的：基準線被做得多弱，會混進比較結果裡。"
  anchor_type: 部落格判斷
  importance: 3
  status: normal
```
