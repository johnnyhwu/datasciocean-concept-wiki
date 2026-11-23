---
id: clm-results-tight-budget-not-across-the-board
title: CLM 的證據能相信的是「緊預算下以較低成本達到相當或稍好的準確率」，不是論文摘要給人的「全面大幅領先」：摘要的大數字多是相對值或單一最好看的設定，預算放寬到 128K 準確率優勢就消失
type_hint: 判斷
context_type: bound_to_source
sources:
- article: context-language-models
  article_title: "Context Language Models 解析：讓 agent 用 Bash 改自己的 context"
  url: https://datasciocean.com/paper-intro/context-language-models/
  sections:
  - context 爆了，誰來決定留什麼？CLM 讓模型自己改
  - 要注意：「何時編輯」其實有 harness 在幫忙
  - 編輯 context 的成本：位置決定要重算多少
  - 主要證據：現成模型零樣本對上最強的固定流程
  - BrowseComp-Plus 與 TerminalBench：相對 11.4% 其實約 6 點
  - EdgeBench-10：預算決定優勢大小
  - 其餘實驗：補充證據與 CLM 的依賴
  - 模型估不準自己用了多少 context
  - 整體評價：概念值得試，證據只夠說明有潛力
  - 論文摘要的宣稱，換成乾淨版本
  - 整篇共有的弱點
  - 把自由度交給模型，什麼條件下划算
  first_appearance: true
parent: null
related:
  - clm-context-as-editable-file
  - success-gated-efficiency-advantage
  - clm-text-steering-and-skill-evolution
  - verifier-results-how-to-read
  - ragu-results-peeling-confounds
  - skillstate-results-cost-vs-accuracy
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: 可以相信的是「緊預算下，CLM 以較低成本達到相當或稍好的準確率」，不能相信的是論文摘要給人的那種「全面大幅領先」的印象；blog 把論文摘要的宣稱逐列換成乾淨版本，表中每一列，論文摘要用的都是當下最好看的相對值或設定
  source_quotes:
  - "可以相信的是「緊預算下，CLM 以較低成本達到相當或稍好的準確率」，不能相信的是論文摘要給人的那種「全面大幅領先」的印象。表中每一列，論文摘要用的都是當下最好看的相對值或設定。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 成本是論文公式算出來的理論 FLOPs，不是實測延遲或帳單
    source_quote: "論文通篇的「少 X% FLOPs」都是這個公式算出來的理論值，不是實測延遲或帳單。"
  - text: 沒有任何實驗把「自由編輯」的功勞從 harness 的輔助設計裡拆出來，所以能說的是「整套設計」在緊預算下划算，還不能說「context 是檔案」這個想法本身就是主因
    source_quote: "最弱的是：沒有任何實驗把「自由編輯」的功勞，從 harness 的輔助設計裡拆出來；預算放寬到 128K，準確率優勢也消失，只剩省成本。所以能說的是「整套設計」在緊預算下划算，還不能說「context 是檔案」這個想法本身就是主因。"
  importance: 1
  status: normal
- id: c2
  role: context
  text: Context Language Models 論文提出的 CLM 把模型當前的 context 鏡像成一個檔案，模型用 Bash 想改哪裡就改哪裡。論文的主證據是零樣本實驗：不訓練、不演化，直接把現成模型換成 CLM 的玩法，與其他 context 管理方法比
  source_quotes:
  - "Context Language Models 這篇論文提出的做法叫 CLM：把模型當前的 context 鏡像成一個檔案，模型用 Bash 想改哪裡就改哪裡"
  - "論文的主證據是零樣本實驗：不訓練、不演化，直接把現成模型換成 CLM 的玩法，與其他 context 管理方法比。"
  anchor_type: 設計參數
  importance: 2
  status: normal
- id: c3
  role: context
  text: BrowseComp-Plus（BCP，在固定語料上搜尋並回答難題的深度研究基準）與 TerminalBench 2.1（TB2.1，89 個終端機任務，每題只看通過或失敗；TBLite 是它的輕量版）上，所有方法用同一個模型（Qwen3.6-27B）、同一個 agent 框架（Mini-SWE-Agent）、32K 預算、100 輪上限，對手有 Base（不做任何管理）、Summary（Codex 風格的摘要 harness）、MEM1、Self-Compact、ACM、RLM
  source_quotes:
  - "BCP（BrowseComp-Plus）：在固定語料上搜尋並回答難題的深度研究基準，測準確率。"
  - "TB2.1（TerminalBench 2.1）：89 個終端機任務，每題只看通過或失敗。TBLite 是它的輕量版。"
  - "所有方法用同一個模型（Qwen3.6-27B）、同一個 agent 框架（Mini-SWE-Agent）、32K 預算、100 輪上限，對手有 Base（不做任何管理）、Summary、MEM1、Self-Compact、ACM、RLM"
  - "論文沒說明對手（如 Codex 風格的摘要 harness，下文稱 Summary）"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 3
  status: normal
- id: c4
  role: evidence
  text: 對最強對手 Summary，BCP 上 CLM 59.4%、Summary 約 53.3%，絕對差約 +6.1 點，CLM 的 FLOPs 少 21.5%；Summary 的數字是 blog 由「相對高 11.4%」反推的
  source_quotes:
  - "乾淨對照是 CLM 對最強對手 Summary："
  - "BCP | 59.4% | 約 53.3%（由「相對高 11.4%」反推） | 約 +6.1 點 | 少 21.5%"
  anchor_type: 實驗結果
  comparison_target: 最強對手 Summary
  qualifiers:
  - text: FLOPs 是論文公式算出來的理論值，不是實測延遲或帳單
    source_quote: "論文通篇的「少 X% FLOPs」都是這個公式算出來的理論值，不是實測延遲或帳單。"
  - text: CLM 享有編輯回合不計輪數、超預算退回重試、剩 2,048 tokens 提醒，對手是否同樣未說明
    source_quote: "CLM 享有編輯回合不計輪數、超預算退回重試、剩 2,048 tokens 提醒，對手是否同樣未說明"
  figures:
  - file: figures/context-language-models/figure5.png
    article: context-language-models
    src: figure5.png
    caption: 圖 10 — 在編碼與深度研究任務上，CLM 以較低成本勝過 action-based 與 harness 定義的基線。（來源：原始論文 Figure 5。）
    sha256: e7bad7a0e7a05f2c3222e15e62fa1a7a565e150d2bebc9602513135ab6646bf7
  importance: 4
  status: normal
- id: c5
  role: evidence
  text: TB2.1 上 CLM 與 Summary 準確率打平，FLOPs 少 29.5%；TBLite 上 CLM 73.7%、Summary 67.0%，+6.7 點，FLOPs 少 9%
  source_quotes:
  - "TB2.1 | 與 Summary 打平 | 同左 | 約 0 | 少 29.5%"
  - "TBLite | 73.7% | 67.0% | +6.7 點 | 少 9%"
  anchor_type: 實驗結果
  comparison_target: 最強對手 Summary
  qualifiers:
  - text: FLOPs 是論文公式算出來的理論值，不是實測延遲或帳單
    source_quote: "論文通篇的「少 X% FLOPs」都是這個公式算出來的理論值，不是實測延遲或帳單。"
  - text: CLM 享有 harness 輔助，對手有沒有，論文沒說明，無法排除這些設計也貢獻了一部分分數
    source_quote: "CLM 享有前面提過的 harness 輔助，對手有沒有，論文沒說明，所以無法排除這些設計也貢獻了一部分分數。"
  figures:
  - file: figures/context-language-models/figure5.png
    article: context-language-models
    src: figure5.png
    caption: 圖 10 — 在編碼與深度研究任務上，CLM 以較低成本勝過 action-based 與 harness 定義的基線。（來源：原始論文 Figure 5。）
    sha256: e7bad7a0e7a05f2c3222e15e62fa1a7a565e150d2bebc9602513135ab6646bf7
  importance: 5
  status: normal
- id: c6
  role: evaluation
  text: 論文摘要與引言的「高 11.4%」是相對值，換成絕對點數約 6 點；準確率真正贏的是 BCP 和 TBLite，TB2.1 只贏在成本
  source_quotes:
  - "論文摘要與引言的「高 11.4%」是相對值，換成絕對點數約 6 點。準確率真正贏的是 BCP 和 TBLite；TB2.1 只贏在成本。"
  anchor_type: 部落格考證
  comparison_target: 最強對手 Summary（11.4% 是相對 Summary 的準確率）
  importance: 6
  status: normal
- id: c7
  role: qualifier
  text: 這不完全是「自主」對「固定流程」：CLM 享有 harness 輔助（剩 2,048 tokens 時的編輯提醒；BCP 上編輯回合不算進輪數上限、請求超出預算時退回上一輪重試），對手有沒有，論文沒說明，所以無法排除這些設計也貢獻了一部分分數
  source_quotes:
  - "CLM 享有前面提過的 harness 輔助，對手有沒有，論文沒說明，所以無法排除這些設計也貢獻了一部分分數。"
  - "離預算上限還剩 2,048 tokens 時，harness 會送出「該編輯 context 了」的提醒。"
  - "CLM 的編輯回合不算進 100 輪的輪數上限；請求超出預算時，harness 會退回上一輪並重試，最多六次。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 7
  status: normal
- id: c8
  role: context
  text: EdgeBench-10 是從 EdgeBench 挑 10 個程式庫優化任務：agent 在一個程式庫上連續優化 12 小時，容器沒有網路，每次提交的評分範圍是 0 到 100，一個 run 的分數取「最好的提交」與「最終程式庫」兩者較高者；每個任務跑三次，取最好的一次（best-of-three）。比較對象是 Base、Codex 風格摘要、CLM，以及 CLM 加最多五個同時運作的子 agent；PF 指每次試驗的平均 prefix-reuse PFLOPs
  source_quotes:
  - "EdgeBench-10：從 EdgeBench 挑 10 個程式庫優化任務，跑 12 小時，評分 0 到 100。"
  - "agent 在一個程式庫上連續優化 12 小時，容器沒有網路；每次提交由 EdgeBench 評分器打 0 到 100 分，一個 run 的分數取「最好的提交」與「最終程式庫」兩者較高者。每個任務跑三次（三個隨機種子，seed），取最好的一次（best-of-three）。PF 指每次試驗的平均 prefix-reuse PFLOPs。比較對象是 Base、Codex 風格摘要、CLM，以及 CLM 加最多五個同時運作的子 agent。"
  anchor_type: 設計參數
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 8
  status: normal
- id: c9
  role: evidence
  text: EdgeBench-10、32K 預算、Qwen3.6-27B：CLM 44.6（179 PF）、Summary 42.3（437 PF），CLM 高 2.3 點、成本只要約 4 成。論文摘要的「高 5%、少 59% FLOPs」對應的就是這一格（44.6 除以 42.3 約 +5.4%；179 除以 437 約 41%），是單一最好看的設定
  source_quotes:
  - "32K，Qwen3.6-27B | 44.6（179 PF） | 42.3（437 PF） | 44.2（181 PF） | CLM 較準，只用約 41% 算力"
  - "32K 時 CLM 明顯贏：Qwen 上 +2.3 點、成本只要約 4 成。論文摘要的「高 5%、少 59% FLOPs」對應的就是這一格（44.6 除以 42.3 約 +5.4%；179 除以 437 約 41%），是單一最好看的設定。"
  anchor_type: 實驗結果
  comparison_target: Summary（Codex 風格摘要），同一預算與模型
  qualifiers:
  - text: 論文實驗裡 when 由模型決定但靠 harness 輔助；論文沒說明對手（如 Summary）有沒有享受同樣的待遇
    source_quote: "how 完全交給模型，when 由模型決定但靠 harness 輔助。論文沒說明對手（如 Codex 風格的摘要 harness，下文稱 Summary）有沒有享受同樣的待遇"
  - text: 分數是 best-of-three，不是平均，沒有變異數可看，約 2 點以內的差距分不出是真差距還是雜訊
    source_quote: "分數是 best-of-three，不是平均，各方法同樣處理，但沒有變異數可看，約 2 點以內的差距分不出是真差距還是雜訊。"
  - text: PF 是論文公式算出來的理論計算量，不是實測延遲或帳單
    source_quote: "論文通篇的「少 X% FLOPs」都是這個公式算出來的理論值，不是實測延遲或帳單。"
  figures:
  - file: figures/context-language-models/figure6.png
    article: context-language-models
    src: figure6.png
    caption: 圖 11 — 長時間程式庫優化：CLM 勝過 Summary（Codex 風格的摘要 harness）。(a) EdgeBench-10（32K）；(b) Software World（272K）。（來源：原始論文 Figure 6。）
    sha256: a3a775faa0b65e8f22adba9f3d0caa4ccf1534fd5f1461e754412d438f9c4fcc
  importance: 9
  status: normal
- id: c10
  role: evidence
  text: EdgeBench-10、32K 預算、Claude 4.6 Sonnet：CLM 51.0、Summary 42.3
  source_quotes:
  - "32K，Claude 4.6 Sonnet | 51.0 | 42.3 | 50.4 | Summary 在 Qwen 與 Claude 上都是 42.3，論文原文如此"
  anchor_type: 實驗結果
  comparison_target: Summary（Codex 風格摘要），同一預算與模型
  qualifiers:
  - text: 論文實驗裡 when 由模型決定但靠 harness 輔助；論文沒說明對手（如 Summary）有沒有享受同樣的待遇
    source_quote: "how 完全交給模型，when 由模型決定但靠 harness 輔助。論文沒說明對手（如 Codex 風格的摘要 harness，下文稱 Summary）有沒有享受同樣的待遇"
  - text: Summary 在 Qwen 與 Claude 上都是 42.3，blog 註明論文原文如此
    source_quote: "Summary 在 Qwen 與 Claude 上都是 42.3，論文原文如此"
  - text: 分數是 best-of-three，沒有變異數可看
    source_quote: "分數是 best-of-three，不是平均，各方法同樣處理，但沒有變異數可看，約 2 點以內的差距分不出是真差距還是雜訊。"
  figures:
  - file: figures/context-language-models/figure6.png
    article: context-language-models
    src: figure6.png
    caption: 圖 11 — 長時間程式庫優化：CLM 勝過 Summary（Codex 風格的摘要 harness）。(a) EdgeBench-10（32K）；(b) Software World（272K）。（來源：原始論文 Figure 6。）
    sha256: a3a775faa0b65e8f22adba9f3d0caa4ccf1534fd5f1461e754412d438f9c4fcc
  importance: 10
  status: normal
- id: c11
  role: evidence
  text: EdgeBench-10 預算放寬到 128K（Qwen3.6-27B）時準確率優勢消失：CLM 47.3 對 Summary 47.8，只剩約 36% 的算力節省（(222 − 142) / 222）
  source_quotes:
  - "128K，Qwen3.6-27B | 47.3（142 PF） | 47.8（222 PF） | 50.2（219 PF） | CLM 與 Summary 打平，只省算力"
  - "128K 時準確率優勢消失：CLM 47.3 對 Summary 47.8，只剩約 36% 的算力節省（\\( (222 - 142) / 222 \\)）。合理的推論（非論文原文）：預算寬裕時，管理壓力小，管理策略的差距也縮小。"
  anchor_type: 實驗結果
  comparison_target: Summary（Codex 風格摘要），同一預算與模型
  qualifiers:
  - text: blog 推論（非論文原文）：預算寬裕時，管理壓力小，管理策略的差距也縮小
    source_quote: "合理的推論（非論文原文）：預算寬裕時，管理壓力小，管理策略的差距也縮小。"
  - text: 分數是 best-of-three，沒有變異數可看，約 2 點以內的差距分不出是真差距還是雜訊
    source_quote: "分數是 best-of-three，不是平均，各方法同樣處理，但沒有變異數可看，約 2 點以內的差距分不出是真差距還是雜訊。"
  - text: 算力是論文公式算出來的理論值，不是實測延遲或帳單
    source_quote: "論文通篇的「少 X% FLOPs」都是這個公式算出來的理論值，不是實測延遲或帳單。"
  importance: 11
  status: normal
- id: c12
  role: evidence
  text: 子 agent 沒有穩定好處：EdgeBench-10 上 32K 時 CLM 加子 agent 沒有增益（44.2 對 CLM 的 44.6），128K 時 +2.9 點（50.2）但算力與 Summary 相當；論文自己也說單一程式庫上子 agent 幫助不大
  source_quotes:
  - "子 agent 沒有穩定好處：32K 時沒有增益，128K 時 +2.9 點但算力與 Summary 相當。論文自己也說單一程式庫上子 agent 幫助不大。"
  - "32K，Qwen3.6-27B | 44.6（179 PF） | 42.3（437 PF） | 44.2（181 PF）"
  - "128K，Qwen3.6-27B | 47.3（142 PF） | 47.8（222 PF） | 50.2（219 PF）"
  anchor_type: 實驗結果
  comparison_target: 同設定下不加子 agent 的 CLM 與 Summary
  qualifiers:
  - text: 分數是 best-of-three，沒有變異數可看，約 2 點以內的差距分不出是真差距還是雜訊
    source_quote: "分數是 best-of-three，不是平均，各方法同樣處理，但沒有變異數可看，約 2 點以內的差距分不出是真差距還是雜訊。"
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: blog 在 EdgeBench 那一節的總結：CLM 的優勢在「預算緊、context 壓力大」時最明顯，預算放寬就收斂成省成本，這比論文摘要寫的「全面領先」窄得多
  source_quotes:
  - "把這兩組實驗放在一起看：CLM 的優勢在「預算緊、context 壓力大」時最明顯，預算放寬就收斂成省成本。這比論文摘要寫的「全面領先」窄得多。"
  anchor_type: 部落格判斷
  qualifiers:
  - text: 成本是論文公式算出來的理論 FLOPs，不是實測延遲或帳單
    source_quote: "論文通篇的「少 X% FLOPs」都是這個公式算出來的理論值，不是實測延遲或帳單。"
  - text: 預算放寬的證據是 EdgeBench 的 128K 設定
    source_quote: "在 EdgeBench 上把預算放寬到 128K，準確率優勢就消失，只剩省成本。"
  importance: 13
  status: normal
- id: c14
  role: evidence
  text: Software World（6 個互相依賴的程式庫由 agent swarm 優化 24 小時）在 17 個沒見過的下游基準上的幾何平均加速，CLM 約 1.044、Summary 約 1.026，絕對多出約 1.8 個百分點；論文寫的「多 65%」是相對說法，建在很小的基期
  source_quotes:
  - "Software World：6 個互相依賴的程式庫由 agent swarm 優化 24 小時，在沒見過的下游套件上量加速比。"
  - "17 個沒見過的基準上的幾何平均加速，圖上標 CLM 約 1.044、Summary 約 1.026；絕對多出約 1.8 個百分點，論文寫的「多 65%」是相對說法。"
  - "相對值建在很小的基期"
  anchor_type: 實驗結果
  comparison_target: Summary（agent swarm 版）
  qualifiers:
  - text: 模型是 GPT-5.6-Sol、context 預算 272K，不是前面的 32K 設定；文字沒交代跑了幾次
    source_quote: "提醒：模型是 GPT-5.6-Sol、context 預算 272K，不是前面的 32K 設定；文字沒交代跑了幾次。"
  figures:
  - file: figures/context-language-models/figure6.png
    article: context-language-models
    src: figure6.png
    caption: 圖 11 — 長時間程式庫優化：CLM 勝過 Summary（Codex 風格的摘要 harness）。(a) EdgeBench-10（32K）；(b) Software World（272K）。（來源：原始論文 Figure 6。）
    sha256: a3a775faa0b65e8f22adba9f3d0caa4ccf1534fd5f1461e754412d438f9c4fcc
  importance: 14
  status: normal
- id: c15
  role: evidence
  text: 數學優化問題上，通用 agent 加 CLM 對上專用的演化流程 OpenEvolve，四題 CLM 都最好：圓填充 2.618 對 2.541（+3.0%），Heilbronn 0.03653 對 0.03127（+16.8%），另兩題差距只在小數點第三到第四位
  source_quotes:
  - "數學優化 vs OpenEvolve（表 3）：想證明通用 agent 加 CLM 能贏專用的演化流程。四題 CLM 都最好：圓填充 2.618 對 2.541（+3.0%），Heilbronn 0.03653 對 0.03127（+16.8%），另兩題差距只在小數點第三到第四位。"
  - "OpenEvolve（一套專為這類問題設計的演化式工作流程）"
  anchor_type: 實驗結果
  comparison_target: OpenEvolve
  qualifiers:
  - text: 每個方法只跑一次，取最好結果；差距很小的兩題不能當證據，Heilbronn 的 16.8% 是相對值
    source_quote: "提醒：每個方法只跑一次，取最好結果；差距很小的兩題不能當證據，Heilbronn 的 16.8% 是相對值。"
  importance: 15
  status: normal
- id: c16
  role: evidence
  text: CLM 的效果取決於模型自己會不會判斷何時編輯：Qwen3.5-9B 在 TB2.1 平均只編輯 1.4 次，一半任務完全不編輯，Qwen3.6-27B 平均編輯 2.6 次；9B 的 context 峰值中位數 30.2K（上限 32K），27B 是 17.6K
  source_quotes:
  - "模型大小比較（論文 Figure 17、Appendix F）：說明 CLM 的效果取決於模型自己會不會判斷何時編輯。Qwen3.5-9B 在 TB2.1 平均只編輯 1.4 次，一半任務完全不編輯；Qwen3.6-27B 平均編輯 2.6 次。9B 的 context 峰值中位數 30.2K（上限 32K），27B 是 17.6K。"
  anchor_type: 實驗結果
  comparison_target: Qwen3.5-9B 對 Qwen3.6-27B；context 上限 32K
  qualifiers:
  - text: 9B 的零樣本結果不能和 RL 章的訓練前結果混讀
    source_quote: "提醒：9B 的零樣本結果不能和 RL 章的訓練前結果混讀，說明見下一段。"
  importance: 16
  status: normal
- id: c17
  role: evaluation
  text: blog 認為整篇最關鍵的弱點是沒有拆開「自由編輯」與「harness 輔助」的功勞：CLM 同時享有編輯回合不計輪數、退回重試、剩 2,048 tokens 的提醒，沒有任何實驗把這些輔助關掉；零樣本實驗中 CLM 的 system prompt 與 skill 內容也沒給，看不出有多少功勞來自提示寫得好
  source_quotes:
  - "沒有拆開「自由編輯」與「harness 輔助」的功勞：CLM 同時享有編輯回合不計輪數、退回重試、剩 2,048 tokens 的提醒，沒有任何實驗把這些輔助關掉；零樣本實驗中 CLM 的 system prompt 與 skill 內容也沒給，看不出有多少功勞來自提示寫得好。這是最關鍵的一條，它決定能不能把「CLM 勝出」歸因給想法本身。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  importance: 17
  status: normal
- id: c18
  role: evaluation
  text: 其他共有的弱點：缺變異數與重複次數，約 2 點以內的小勝都不該當證據；證據是拼起來的，零樣本用 Qwen3.6-27B 與 Claude 4.6 Sonnet、RL 用 Qwen3.5-9B、skill 演化用 Opus 5 或 Fable 5.1 當 proposer、Software World 用 GPT-5.6-Sol，沒有任何一個模型從頭走到尾；ContextBench 是作者自建的，FLOPs 是自訂的理論值
  source_quotes:
  - "約 2 點以內的小勝都不該當證據。"
  - "證據是拼起來的，沒有串成一條線：零樣本用 Qwen3.6-27B 與 Claude 4.6 Sonnet，RL 用 Qwen3.5-9B，skill 演化用 Opus 5 或 Fable 5.1 當 proposer，Software World 用 GPT-5.6-Sol。沒有任何一個模型從頭走到尾。"
  - "自建基準與自訂指標：ContextBench 是作者自建的；FLOPs 是自訂的理論值，不等於實際延遲或帳單。"
  anchor_type: 部落格判斷
  numeric_kind: non_comparative
  numeric_reason: 名稱
  importance: 18
  status: normal
- id: c19
  role: evaluation
  text: blog 對「什麼條件下值得把自由度交給模型」的判斷：預算緊有直接證據（EdgeBench 32K 時 CLM 較準又省，128K 時只剩省成本），是最強的；模型夠強只有間接證據（不同模型、不同設定的比較）；任務長沒有實驗單獨驗證；目前也不是完全放手，仍需 harness 輔助作外部保險。即使預算寬鬆，CLM 仍可能省成本
  source_quotes:
  - "什麼時候值得把自由度交給模型？以下是我整合論文證據得出的判斷，推論，非論文原文："
  - "預算緊 | EdgeBench 32K 時 CLM 較準又省；128K 時準確率打平，只剩省成本（圖 11、論文 Figure 19） | 直接，最強"
  - "模型夠強 | 9B 很少編輯 context，一半任務完全不編輯（論文 Appendix F）；訓練前 CLM 落後 Summary（表 2） | 間接，是不同模型、不同設定的比較"
  - "任務長 | 沒有實驗單獨改變任務長度 | 弱，論文未驗證"
  - "目前不是完全放手，仍需外部保險"
  - "即使預算寬鬆，CLM 仍可能省成本。"
  anchor_type: 部落格推論
  numeric_kind: non_comparative
  numeric_reason: 規格上限
  qualifiers:
  - text: 成本是論文公式算出來的理論 FLOPs，不是實測延遲或帳單
    source_quote: "論文通篇的「少 X% FLOPs」都是這個公式算出來的理論值，不是實測延遲或帳單。"
  - text: 「長任務、預算緊、模型夠強三者同時成立」是 blog 編的組合，論文沒測過三者的交互作用，只是決定從哪裡開始試的經驗法則，不是必要條件
    source_quote: "還有一個講過頭要避開的地方：「三者同時成立」是我編的組合，論文沒測過三者的交互作用，它只是決定「從哪裡開始試」的經驗法則，不是必要條件。"
  importance: 19
  status: normal
```
