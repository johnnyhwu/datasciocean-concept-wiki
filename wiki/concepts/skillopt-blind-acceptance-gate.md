---
id: skillopt-blind-acceptance-gate
title: 候選修改要在優化器從沒看過的切分上「嚴格高於」現狀才收，平手也丟棄：不讓同一方既當球員又當裁判
type_hint: 可遷移原則
context_type: evidence_from_single_source
sources:
- article: skillopt
  article_title: "SkillOpt：把 AI Agent 的技能文件當成可訓練的權重來優化，不用碰模型本身"
  url: https://datasciocean.com/paper-intro/skillopt/
  sections:
  - 兩個模型，各司其職
  - 目標模型（M）
  - 優化器模型（O）
  - 資料隔離與嚴格的接受規則
  - 真正做出決定的守門員
  - 驗證守門機制真的挑得出贏家嗎？
  - 評分函式的瓶頸
  - 優化器強度：一定要前沿等級嗎？
  first_appearance: true
parent: null
related:
  - skillopt-overview
  - skillopt-bounded-edit-budget
  - skillopt-epoch-level-control
status: active
---

## 主張

```yaml
claims:
- id: c1
  role: thesis
  text: SkillOpt 整套設計裡最重要的工程紀律是資料隔離：優化器只能看到訓練集 D_tr 的執行軌跡，候選技能必須在它完全看不到的 D_sel 上，平均分數嚴格大於目前技能才被接受，平手不算
  source_quotes:
  - SkillOpt 整套設計裡最重要的一項工程紀律，就是資料隔離
  - 優化器模型永遠只能看到來自 \( D_{tr} \) 的執行軌跡——那是它取得「該改什麼」證據的地方。但它完全看不到 \( D_{sel} \)。任何一份在訓練期間產生的候選技能，都必須獨立地拿到 \( D_{sel} \) 上打分，而接受的規則非常嚴格：新技能的平均分數必須**嚴格大於**目前技能的分數，平手不算。
  anchor_type: 部落格判斷
  qualifiers:
  - text: 整套系統完全仰賴驗證守門機制，而驗證守門機制又完全仰賴一個便宜、可靠、自動化的評分方式
    source_quote: 整套系統完全仰賴驗證守門機制，而驗證守門機制又完全仰賴一個**便宜、可靠、自動化的評分方式**
  importance: 1
  status: normal
- id: c2
  role: context
  text: SkillOpt 把責任拆分給兩個獨立的模型，而不是要求同一個模型既要完成任務、又要幫自己的作業打分：凍結的目標模型負責實際執行工作，優化器模型只在離線訓練階段讀取目標模型的執行軌跡與分數，針對技能文件提出具體的修改建議
  source_quotes:
  - SkillOpt 把責任拆分給兩個獨立的模型，而不是要求同一個模型既要完成任務、又要幫自己的作業打分。
  - 目標模型是實際執行工作的那一方——回答問題、呼叫工具、寫程式碼
  - 它的權重與原生的 system prompt 在整個訓練過程中都保持凍結
  - 優化器模型完全不碰任務本身。它通常是一個能力更強的「前沿(frontier)」模型，而且只在離線訓練階段運作。它的工作是讀取目標模型的執行軌跡與分數，然後針對技能文件提出具體的修改建議
  anchor_type: 背景說明
  qualifiers:
  - text: 優化器也可以降級成跟目標模型一樣的模型，也就是目標模型自己優化自己
    source_quote: 即使把「教練」降級成跟目標模型一樣(規模小得多)的模型——也就是目標模型自己優化自己——有界更新加上驗證守門這套機制，依然足以挽回相較於前沿等級優化器所取得收益的 56% 到 74%。
  importance: 2
  status: normal
- id: c3
  role: context
  text: 資料切分直接借用自標準的機器學習實務：訓練集 D_tr、選擇／驗證集 D_sel，以及保留的測試集 D_test
  source_quotes:
  - 這個做法直接借用自標準的機器學習實務：訓練集(\( D_{tr} \))、選擇／驗證集(\( D_{sel} \))，以及保留的測試集(\( D_{test} \))。
  anchor_type: 背景說明
  importance: 3
  status: normal
- id: c4
  role: mechanism
  text: 套用修改後產生的候選技能並不會因為看起來合理就被信任，它必須靠著在優化器從未看過的 D_sel 上被盲測打分來爭取通過；只有分數嚴格大於目前技能，這個候選才會被寫入硬碟，成為新的目前技能
  source_quotes:
  - 並不會因為看起來合理就被信任——它必須靠著在 \( D_{sel} \) 上被盲測打分來爭取通過，而 \( D_{sel} \) 正是優化器從未看過的那個切分。只有當 \( \text{score}(\tilde{s}) \) **嚴格大於**目前技能的分數，這個候選才會被寫入硬碟，成為新的目前技能
  anchor_type: 設計參數
  qualifiers:
  - text: 整套系統完全仰賴驗證守門機制，而驗證守門機制又完全仰賴一個便宜、可靠、自動化的評分方式
    source_quote: 整套系統完全仰賴驗證守門機制，而驗證守門機制又完全仰賴一個**便宜、可靠、自動化的評分方式**
  importance: 4
  status: normal
- id: c5
  role: mechanism
  text: 候選技能的分數平手或下降，整個步驟都會被丟棄，先前的技能維持不變
  source_quotes:
  - 平手或分數下降，則整個步驟都會被丟棄，先前的技能維持不變。
  anchor_type: 設計參數
  importance: 5
  status: normal
- id: c6
  role: evaluation
  text: blog 認為「嚴格大於」的門檻，堵住了迭代式提示詞編輯最常見的失敗模式：一連串各自看起來都很合理的修改，累加起來卻只是增加了雜訊或讓文件膨脹，並沒有真正帶來幫助
  source_quotes:
  - 這條「嚴格大於」的門檻，堵住了迭代式提示詞編輯最常見的失敗模式——一連串各自看起來都很合理的修改，累加起來卻只是增加了雜訊或讓文件膨脹，並沒有真正帶來幫助。
  anchor_type: 部落格判斷
  importance: 6
  status: normal
- id: c7
  role: mechanism
  text: 被拒絕的步驟，連同它試圖修復的失敗模式、以及分數下降了多少，會被記錄進一個短期的被拒修改緩衝區；這份歷史紀錄會注入到下一個步驟的分析師與排序器呼叫裡，內容大致是「我們已經試過這個做法，而且它傷害了驗證分數——別再提出一樣的建議了」
  source_quotes:
  - 被拒絕的修改並不會就此浪費。任何一個被拒絕的步驟，連同它試圖修復的失敗模式、以及分數下降了多少，都會被記錄進一個短期的**被拒修改緩衝區**。這份歷史紀錄會被當成上下文，注入到**下一個**步驟的分析師與排序器呼叫裡，內容大致是：「我們已經試過這個做法，而且它傷害了驗證分數——別再提出一樣的建議了。」
  anchor_type: 設計參數
  importance: 7
  status: normal
- id: c8
  role: evaluation
  text: blog 認為被拒修改緩衝區是一個很小的機制，但它能阻止優化器一步一步重複嘗試同一個壞主意
  source_quotes:
  - 這是一個很小的機制，但它能阻止優化器一步一步重複嘗試同一個壞主意。
  anchor_type: 部落格判斷
  importance: 8
  status: normal
- id: c9
  role: mechanism
  text: 優化器提出的修改是透過精確字串比對套用的，LLM 偶爾會產生幻覺，提出一個並沒有逐字出現在文件裡的目標字串；這種修改會被標記為 skip 並記錄在日誌，不會讓整條管線崩潰，同一批次裡其他不受影響的修改仍會照常套用
  source_quotes:
  - 優化器提出的修改，是透過精確字串比對套用到技能文件上的，而 LLM 偶爾確實會產生幻覺，提出一個並沒有真的逐字出現在文件裡的目標字串。發生這種情況時，那一項修改會被標記為 `skip`，記錄在 `edit_apply_report.json` 這份日誌裡，而不會讓整條管線崩潰，同一批次裡其他不受影響的修改仍會照常套用。
  anchor_type: 設計參數
  importance: 10
  status: normal
- id: c10
  role: evidence
  text: 在三個基準測試上，驗證集分數的最高點跟測試集分數的最高點高度重合
  source_quotes:
  - 這種選擇性，還可以從另一個角度得到驗證：驗證集挑出來的 checkpoint，是不是真的跟未見過測試集上表現最好的那個 checkpoint 一致。
  - 在這三個基準測試上，驗證集分數(橘線)的最高點，跟測試集分數(綠線)的最高點高度重合。
  anchor_type: 實驗結果
  comparison_target: 測試集分數的最高點（未見過的測試集上表現最好的 checkpoint）
  qualifiers:
  - text: 只在三個基準測試上觀察到
    source_quote: 在這三個基準測試上，驗證集分數(橘線)的最高點，跟測試集分數(綠線)的最高點高度重合。
  importance: 9
  status: normal
- id: c11
  role: evaluation
  text: blog 認為驗證集與測試集最高點高度重合在統計上是一個很好的訊號：驗證守門機制真正挑出來的，是泛化能力最好的版本，而不是恰好在訓練批次上表現亮眼、但換個題目就現形的過擬合版本
  source_quotes:
  - 這在統計上是一個很好的訊號：代表驗證守門機制真正挑出來的，是泛化能力最好的版本，而不是恰好在訓練批次上表現亮眼、但換個題目就現形的過擬合版本。
  anchor_type: 部落格判斷
  qualifiers:
  - text: 只在三個基準測試上觀察到
    source_quote: 在這三個基準測試上，驗證集分數(橘線)的最高點，跟測試集分數(綠線)的最高點高度重合。
  importance: 11
  status: normal
- id: c12
  role: evaluation
  text: 整套系統完全仰賴驗證守門機制，而驗證守門機制又完全仰賴一個便宜、可靠、自動化的評分方式；對於有可驗證答案的任務（通過測試與否的程式碼、符合目標與否的試算表轉換），這是一個合理的假設
  source_quotes:
  - 整套系統完全仰賴驗證守門機制，而驗證守門機制又完全仰賴一個**便宜、可靠、自動化的評分方式**。對於有可驗證答案的任務——通過測試與否的程式碼、符合目標與否的試算表轉換——這是一個合理的假設。
  anchor_type: 部落格判斷
  importance: 12
  status: normal
- id: c13
  role: evaluation
  text: 對於開放式、主觀性高的任務（創意寫作、開放式的客服對話），要打造一個好到足以做為守門依據的評分器，老實說可能需要引入 LLM-as-judge 這類機制，而這又把這整套管線原本想避開的成本與雜訊給帶了回來
  source_quotes:
  - 但對於開放式、主觀性高的任務(創意寫作、開放式的客服對話)，要打造一個好到足以做為守門依據的評分器，老實說可能需要引入 LLM-as-judge 這類機制，而這又把這整套管線原本想避開的成本與雜訊給帶了回來。
  anchor_type: 部落格判斷
  qualifiers:
  - text: 「可能需要」引入 LLM-as-judge，是 blog 的推測語氣，不是確定的結論
    source_quote: 老實說可能需要引入 LLM-as-judge 這類機制
  importance: 13
  status: normal
```
