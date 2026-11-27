---
id: pg-local-subgraph-vs-full-graph
title: 推論時局部子圖加生成式提示在三個 benchmark 上都是最高，把整張圖唸給 agent 聽反而會傷害（尤其嚴格動作順序的 ALFWorld）；但就算只取局部，每步多一次 LLM 呼叫仍讓 token 是無圖的 1.33 到 1.85 倍
type_hint: 發現
context_type: evidence_from_single_source
sources:
  - article: procedural-graphs
    article_title: "把流程畫成圖，AI Agent 就不會迷路？Procedural Graphs 解析"
    url: https://datasciocean.com/paper-intro/procedural-graphs/
    sections:
      - agent 做長任務，為什麼會迷路？
      - 推論時：每一步只看腳邊兩跳
      - 四個要記得的性質
      - 實驗二：整張圖會傷害，只取附近才有效
      - 實驗三：手寫專家圖可能崩盤，演化救得回來
      - 一個 benchmark 一張圖
    first_appearance: true
parent: null
related:
  - pg-structure-and-inference
  - pg-results-and-expert-graph-collapse
  - propose-validate-reject-evolution-loop
  - evoontology-query-over-prompt-stuffing
  - single-loop-progressive-disclosure
status: active
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: 局部子圖加生成式提示在 MultiChallenge、GDPval、ALFWorld 三個 benchmark 上都是最高，整張圖會傷害（尤其是需要嚴格動作順序的 ALFWorld）；不過就算只取附近，局部子圖的 token 成本一直比無圖高，是無圖的 1.33 到 1.85 倍
    source_quotes:
      - "局部子圖加生成式提示，在三個 benchmark 上都是最高；整張圖會傷害，尤其是需要嚴格動作順序的 ALFWorld。"
      - "局部子圖的成本一直比無圖高。它的 token 是無圖的 1.33 到 1.85 倍。"
      - "這就是「導航只報下一兩個路口」的證據：只取附近的子圖，比把整張圖唸給 agent 聽更好。不過就算只取附近，成本還是比不用圖高。"
    anchor_type: 實驗結果
    comparison_target: 無圖、整張圖＋原文塞入、整張圖＋生成式（分數）；無圖（token 倍數）
    qualifiers:
      - text: 實驗二只用同一張圖與同一個模型（Gemini 3.5 Flash），在 MultiChallenge、GDPval、ALFWorld 三個 benchmark 上測
        source_quote: "同一張圖、同一個模型（Gemini 3.5 Flash），只改兩件事：給 agent 看整張圖還是局部子圖，以及圖是原文塞進去，還是先讓 \\( \\Psi \\) 翻成提示。"
      - text: 局部取子圖作為「無關的圖內容有害」的緩解辦法，只有在定位成功、鄰域本身不混雜時才成立
        source_quote: "局部取子圖是它的緩解辦法，但只有在定位成功、鄰域本身不混雜時才成立。"
    figures:
      - file: figures/procedural-graphs/table3.png
        article: procedural-graphs
        src: table3.png
        caption: 表 4 — 使用方式消融（Gemini 3.5 Flash）。（來源：原始論文 Table 3。）
        sha256: da136382d69fd745aa395713e58ef977fd9b69fe6ea5ed97de8e20338cc1d652
    importance: 1
    status: normal

  - id: c2
    role: context
    text: Google 論文 Procedural Graphs 把 agent 的做事流程存成可編輯的有向圖（PG）；推論時先判斷上一步做完哪個節點，取往後 2 跳的子圖交給 guidance model（Ψ，與 solver 同底層模型的另一個 LLM）翻成提示附加給 solver（負責選下一步動作的 LLM）
    source_quotes:
      - "這篇整理 Google 的論文 *Procedural Graphs: Self-Evolving Execution Structures for LLM Agents*（arXiv 2609.09153v1，2026 年九月）。"
      - "把 agent 的「做事流程」存成一張可編輯的有向圖（節點是步驟，箭頭指向下一步）。"
      - "推論時的做法是：每一步決策前，先判斷 agent 剛做完圖上的哪個節點，只取那個節點往後 2 跳（沿著箭頭走兩步）的小圖，由另一個 LLM 轉成一小段「現在該做什麼、要避開什麼」的文字，附加到 solver 的 prompt。"
      - "solver：實際選下一步動作的 LLM，也就是 ReAct 迴圈裡的 agent 本人。guidance model（\\( \\Psi \\)）：另一個 LLM，負責把子圖翻成提示。論文說它和 solver 用同一個底層模型（Section 4）。"
    anchor_type: 設計參數
    numeric_kind: non_comparative
    numeric_reason: 定義
    qualifiers:
      - text: 推論時圖是凍結的，不會更新
        source_quote: "推論時圖是凍結的，不會更新（Section 3.2）。"
      - text: 提示只是偏向 solver 的下一步動作，不會強制
        source_quote: "論文摘要說提示會 bias solver 的下一步動作，但不會 dictate 它。論文沒有任何機制檢查 solver 的動作是不是真的走在圖上。"
    importance: 2
    status: normal

  - id: c3
    role: context
    text: 實驗二是論文唯一直接檢驗「局部取子圖、再由 Ψ 翻成提示」核心設計的實驗，用同一張圖與 Gemini 3.5 Flash，在 MultiChallenge、GDPval、ALFWorld 比較四種組合：無圖、整張圖＋原文塞入（不經 Ψ）、整張圖＋生成式（交給 Ψ 翻成提示）、局部子圖＋生成式（完整做法）
    source_quotes:
      - "這是唯一直接檢驗核心設計（局部取子圖、再由 \\( \\Psi \\) 翻成提示）的實驗（Section 5.5）。"
      - "同一張圖、同一個模型（Gemini 3.5 Flash），只改兩件事：給 agent 看整張圖還是局部子圖，以及圖是原文塞進去，還是先讓 \\( \\Psi \\) 翻成提示。比較四種組合：無圖：不用 PG。整張圖＋原文塞入：整張圖序列化後直接放進 prompt，不經 \\( \\Psi \\)。整張圖＋生成式：整張圖交給 \\( \\Psi \\) 翻成提示。局部子圖＋生成式：論文的完整做法。"
    anchor_type: 設計參數
    numeric_kind: non_comparative
    numeric_reason: 名稱
    qualifiers:
      - text: 實驗二與實驗三在 MultiChallenge 上用的題目子集不同（表 4 的 caption 寫明是 fixed subsets），數字不能跨實驗比較
        source_quote: "同樣用 Gemini 3.5 Flash、同樣不用圖，MultiChallenge 的基準在實驗二是 80.27、在這裡是 87.50，原因是兩個實驗用的題目子集不同（表 4 的 caption 寫明是 fixed subsets），數字不能跨實驗比較。"
    importance: 3
    status: normal

  - id: c4
    role: anchor
    text: 在表現分數上，局部子圖＋生成式在三個 benchmark 都最高：MultiChallenge 89.31（高過第二名整張圖＋生成式 87.35 共 1.96 分）、GDPval 63.99（高過第二名整張圖＋原文塞入 57.17 共 6.82 分）、ALFWorld 81.53（高過第二名無圖 72.58 共 8.95 分）
    source_quotes:
      - "局部子圖在三個 benchmark 都最高，比各自的第二名高 1.96、6.82、8.95 分。"
      - "無圖 | 80.27 | 54.80 | 72.58"
      - "整張圖＋原文塞入 | 86.60 | 57.17 | 70.34"
      - "整張圖＋生成式 | 87.35 | 56.75 | 54.48"
      - "局部子圖＋生成式 | 89.31 | 63.99 | 81.53"
    anchor_type: 實驗結果
    comparison_target: 各 benchmark 的第二名設定（MultiChallenge 為整張圖＋生成式 87.35、GDPval 為整張圖＋原文塞入 57.17、ALFWorld 為無圖 72.58）
    qualifiers:
      - text: 使用 Gemini 3.5 Flash
        source_quote: "同一張圖、同一個模型（Gemini 3.5 Flash）"
      - text: 表 4 的 caption 寫明是 fixed subsets，實驗二與實驗三的 MultiChallenge 數字不能跨實驗比較
        source_quote: "原因是兩個實驗用的題目子集不同（表 4 的 caption 寫明是 fixed subsets），數字不能跨實驗比較。"
    figures:
      - file: figures/procedural-graphs/table3.png
        article: procedural-graphs
        src: table3.png
        caption: 表 4 — 使用方式消融（Gemini 3.5 Flash）。（來源：原始論文 Table 3。）
        sha256: da136382d69fd745aa395713e58ef977fd9b69fe6ea5ed97de8e20338cc1d652
    importance: 4
    status: normal

  - id: c5
    role: anchor
    text: 在 ALFWorld 上整張圖反而會傷害表現：無圖是 72.58，整張圖＋原文塞入降到 70.34，整張圖＋生成式掉到 54.48，同時 token 暴增至無圖的 5.34 倍
    source_quotes:
      - "無圖 | 80.27 | 54.80 | 72.58"
      - "整張圖＋原文塞入 | 86.60 | 57.17 | 70.34"
      - "整張圖＋生成式 | 87.35 | 56.75 | 54.48"
      - "整張圖會傷害。ALFWorld 從 72.58 掉到 54.48，同時 token 是無圖的 5.34 倍。"
    anchor_type: 實驗結果
    comparison_target: 無圖（72.58 分與無圖的每題平均 token 數）
    qualifiers:
      - text: 使用 Gemini 3.5 Flash；在 MultiChallenge 與 GDPval 上，整張圖＋原文塞入與整張圖＋生成式的分數仍高於無圖，傷害主要出現在 ALFWorld
        source_quote: "實驗二顯示整張圖加生成式提示是最差的設定（主要是在 ALFWorld，也就是虛擬家庭任務上）"
    figures:
      - file: figures/procedural-graphs/table3.png
        article: procedural-graphs
        src: table3.png
        caption: 表 4 — 使用方式消融（Gemini 3.5 Flash）。（來源：原始論文 Table 3。）
        sha256: da136382d69fd745aa395713e58ef977fd9b69fe6ea5ed97de8e20338cc1d652
    importance: 5
    status: normal

  - id: c6
    role: evaluation
    text: blog 推測 ALFWorld 掉分的原因是：ALFWorld 要求嚴格的動作順序，整張圖裡不相干的分支，guidance model（Ψ）還是會把它們寫進提示；論文只給結果，沒給機制
    source_quotes:
      - "我的推測是：ALFWorld 要求嚴格的動作順序，整張圖裡不相干的分支，\\( \\Psi \\) 還是會把它們寫進提示。論文只給結果，沒給機制。"
    anchor_type: 部落格推論
    importance: 6
    status: normal

  - id: c7
    role: anchor
    text: 在成本上，每題平均 token 數（含 Ψ 的呼叫）以局部子圖＋生成式對比無圖，在 MultiChallenge 是 1.85 倍、GDPval 是 1.33 倍、ALFWorld 是 1.55 倍，三者都比無圖高
    source_quotes:
      - "兩個成本指標都是越低越好：Avg. Tok 是每題平均用掉的 token 數（包含 \\( \\Psi \\) 的呼叫），Avg. Step 是每題 solver 平均走幾步。"
      - "成本：token 相對無圖的倍數（由表 4 的原始 token 數計算）："
      - "局部子圖＋生成式 | 1.85 倍 | 1.33 倍 | 1.55 倍"
      - "局部子圖的成本一直比無圖高。它的 token 是無圖的 1.33 到 1.85 倍。"
    anchor_type: 部落格考證
    comparison_target: 無圖設定的每題平均 token 數
    qualifiers:
      - text: 使用 Gemini 3.5 Flash，由表 4 的原始 token 數計算
        source_quote: "成本：token 相對無圖的倍數（由表 4 的原始 token 數計算）"
    figures:
      - file: figures/procedural-graphs/table3.png
        article: procedural-graphs
        src: table3.png
        caption: 表 4 — 使用方式消融（Gemini 3.5 Flash）。（來源：原始論文 Table 3。）
        sha256: da136382d69fd745aa395713e58ef977fd9b69fe6ea5ed97de8e20338cc1d652
    importance: 7
    status: normal

  - id: c8
    role: anchor
    text: 整張圖＋原文塞入的 token 相對無圖在 MultiChallenge 是 1.53 倍、GDPval 是 0.96 倍、ALFWorld 是 1.17 倍；整張圖＋生成式則是 2.18 倍、1.63 倍、5.34 倍
    source_quotes:
      - "整張圖＋原文塞入 | 1.53 倍 | 0.96 倍 | 1.17 倍"
      - "整張圖＋生成式 | 2.18 倍 | 1.63 倍 | 5.34 倍"
    anchor_type: 部落格考證
    comparison_target: 無圖設定的每題平均 token 數
    qualifiers:
      - text: 使用 Gemini 3.5 Flash，由表 4 的原始 token 數計算
        source_quote: "成本：token 相對無圖的倍數（由表 4 的原始 token 數計算）"
    figures:
      - file: figures/procedural-graphs/table3.png
        article: procedural-graphs
        src: table3.png
        caption: 表 4 — 使用方式消融（Gemini 3.5 Flash）。（來源：原始論文 Table 3。）
        sha256: da136382d69fd745aa395713e58ef977fd9b69fe6ea5ed97de8e20338cc1d652
    importance: 8
    status: normal

  - id: c9
    role: evidence
    text: 局部子圖＋生成式對比無圖的每題平均步數（Avg. Step）在 GDPval 從 28.20 降到 18.57、在 ALFWorld 從 21.84 降到 18.80，MultiChallenge 反而從 3.87 升到 4.22
    source_quotes:
      - "Avg. Step 是每題 solver 平均走幾步。"
      - "步數則在 GDPval（28.20 降到 18.57）與 ALFWorld（21.84 降到 18.80）下降，MultiChallenge 反而從 3.87 升到 4.22。"
    anchor_type: 實驗結果
    comparison_target: 無圖設定的每題平均步數（GDPval 28.20、ALFWorld 21.84、MultiChallenge 3.87）
    qualifiers:
      - text: 使用 Gemini 3.5 Flash
        source_quote: "同一張圖、同一個模型（Gemini 3.5 Flash）"
    figures:
      - file: figures/procedural-graphs/table3.png
        article: procedural-graphs
        src: table3.png
        caption: 表 4 — 使用方式消融（Gemini 3.5 Flash）。（來源：原始論文 Table 3。）
        sha256: da136382d69fd745aa395713e58ef977fd9b69fe6ea5ed97de8e20338cc1d652
    importance: 9
    status: normal

  - id: c10
    role: evaluation
    text: 推論時若節點比對失敗會退回整張圖，代價很高（整張圖加生成式提示在實驗二是 ALFWorld 最差設定），但論文沒給比對失敗的頻率，所以不知道這條退回路徑實際被走到多少次
    source_quotes:
      - "比對失敗退回整張圖，代價很高。實驗二顯示整張圖加生成式提示是最差的設定（主要是在 ALFWorld，也就是虛擬家庭任務上），但論文沒給比對失敗的頻率，所以不知道這條路徑實際被走到多少次。"
    anchor_type: 部落格判斷
    importance: 10
    status: normal

  - id: c11
    role: evaluation
    text: 論文確實顯示過「無關的圖內容有害」，局部取子圖是它的緩解辦法，但只有在定位成功、鄰域本身不混雜時才成立
    source_quotes:
      - "論文確實顯示過「無關的圖內容有害」：表 4（Gemini 3.5 Flash）裡，整張圖加生成式提示是最差設定，ALFWorld 成功率 54.48，局部子圖是 81.53。局部取子圖是它的緩解辦法，但只有在定位成功、鄰域本身不混雜時才成立。"
    anchor_type: 部落格判斷
    importance: 11
    status: normal
```
