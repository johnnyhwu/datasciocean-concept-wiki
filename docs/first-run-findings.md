# 第一次實跑（jev-overview）發現的問題：Stage 1 部分

這是**歷史紀錄**。走完第一次實跑後回頭檢討時，所有發現都已處理並併入下表的位置；表格內「規格已改」欄是當時（重構前）的狀態，現在以 skill 與 `docs/card-format.md` 為準。Stage 2 的發現（#33–45）已移到 `datasciocean-social-media` repo 的 `docs/first-run-findings.md`。

## 重構後的處理對照

| 發現 | 現在放在哪 |
|---|---|
| #1 目錄與腳本位置 | skill 結構：`.claude/skills/distill-article/`；環境見 `SKILL.md`「開始前」 |
| #2 數字豁免、#3 三個新錨點類型 | `docs/card-format.md` §4、§6；`config/params.yaml` |
| #4 claims 要用 fenced yaml、#5 sections 記標題文字 | `docs/card-format.md` §3 |
| #6–#8 同名小節、小節範圍、省略號 | `docs/card-format.md` §8；`wikilib.py` |
| #9 Stage 2 區塊標題誤判 | 不再需要：Stage 2 區塊已從卡移除，Stage 2 狀態改放下游 repo |
| #10–#14、#16–#18 審查者運作、blog 矛盾、應到實到、並行上限、提示詞放 references | `references/review-loop.md`、`references/*-prompt.md` |
| #11 讀者的「只能從卡回答」題目 | `references/review-loop.md` 關卡 2（撰寫者出題、含陷阱題）；自動出題見 `docs/backlog.md` #1 |
| #12 讀者抓到的名詞缺口 | `references/card-writing.md` §5（卡必須自足） |
| #15 blog 內部矛盾清單 | 本文件 #15（blog 沒修，卡用保守寫法） |
| #19–#23 pending、輪數上限、審查者自己的錯、不收斂 | `references/review-loop.md`（分級、pending 不擋、輪數、升級） |
| #24 審查成本 | `references/review-loop.md`「成本參考」；改進見 `docs/backlog.md` |
| #25 合併規則 R1–R5 | `references/mining-and-filtering.md` |
| #26 分級退回、#27 指紋重審 | `references/review-loop.md`；`verify_audit.py`、`claim_fingerprints.py` |
| #28 讀者題目的獨立性 | `docs/backlog.md` #1 |
| #29–#31 放行、通用知識、關係 | `references/release.md`；`config/background-terms.md` |
| #32 迴圈通過後自動進下一階段 | `references/release.md` §2（改為：迴圈通過、無待人處理項目就直接寫入 wiki）。兩個 repo 拆開後，「進入 Stage 2」變成人到下游 repo 更新 submodule |
| 對證者只看引文、依序審查、全文審查（重構新增） | `references/review-loop.md`；`make_auditor_copy.py`、`verify_final_audit.py` |
| `article_title`（下游發現缺欄位，#37 的處理） | `docs/card-format.md` §3、§8；`validate_card.py` 驗證與 blog 標題一致 |


## 規格與目錄

| # | 發現 | 處理 | 規格已改 |
|---|---|---|---|
| 1 | `config/params.yaml`、`wiki/` 不存在；M1/M2 的檢查程式也沒有 | 補 params.yaml；程式放 `.claude/skills/concept-wiki/scripts/`（使用者指定走 skill 標準結構，用 `uv run` 搭配內嵌依賴） | 是（目錄） |
| 2 | 「含數字必有 comparison_target」誤傷非比較數字（規格上限、日期、示範題、定義內的 0/1） | 人決定：加 `numeric_kind: non_comparative` + `numeric_reason` 豁免，倍數/百分比/分數/價格不得豁免，豁免列給對證者 | 是（01 §4、§13） |
| 3 | 10 種錨點類型接不住三種主張：領域概念說明、blog 自設假設例子、社群評論 | 人決定：新增「背景說明」「部落格舉例」「社群評論」並定義 Stage 2 寫法 | 是（01 §5） |
| 4 | 規格 §3 範例的 claims 直接寫在 markdown 本文，沒有 code fence，不可解析 | 人決定：兩個區塊各用標題加 ```yaml fenced block | 否（範例仍是舊寫法，待改） |
| 5 | `sources.sections` 範例是章節編號（6.1…），blog 標題沒有編號 | 人決定：記小節標題文字，程式驗證標題存在且引用落在該小節 | 否（範例待改） |
| 6 | blog 有同名小節（「拆解問題不能只拆『窄』，還要拆『淺』」出現兩次） | 程式比對所有同名小節 | 否 |
| 7 | 小節範圍：程式只算小節自己的文字、不含子小節，才能精確驗證引用位置；代價是 sections 要列得更細 | 實作決定 | 否 |
| 8 | 來源原文的省略符號「…」：規格範例用了，但沒定義比對方式 | 實作決定：以「…」切片段，每段須逐字出現且依序 | 否 |
| 9 | 卡的 Stage 2 區塊標題括號裡含「Stage 1」，用字串包含判斷會誤認區塊 | 解析只看標題開頭 | 否（建議標題改成不含另一階段字樣） |

## Stage 1 審查迴圈（第 1 輪，11 張卡全退回）

| # | 發現 | 處理 | 規格已改 |
|---|---|---|---|
| 10 | 試跑卡（confound）顯示對證者能獨立抓到：措辭放大、錨點類型標錯、來源沒涵蓋、blog 算式矛盾；引用皆經程式驗證為逐字原文 | 流程可用 | — |
| 11 | 02 §7.2「只能從卡回答的題目」要求「答對『卡上沒寫』算通過」，但程式不知道哪題才是真的沒有答案；通用題（比較對象、限定條件、提出者）在沒有該項的卡上，「沒寫」是正確答案，會誤殺，反之漏看抓不到 | 改成：每張卡由撰寫者出題並標預期是否在卡上（含一題陷阱題）。`verify_reader.py` 目前只支援陷阱題編號，需再擴充 | 否 |
| 12 | 讀者標「擋住主軸」的名詞多為真缺口：Jev、state、校準、非自回歸、一致率、座標圖。卡自足性不能假設「同一篇文章的別張卡有講」 | 逐張補脈絡主張 | 否 |
| 13 | 對證者會把 blog 自己的矛盾列成「主張互核矛盾」，需人工區分卡的錯與 blog 的錯 | 驗證輸出分開列「blog 內部矛盾」，彙整給人 | 否 |
| 14 | 02 §9 規定 blog 矛盾由人決定「修 blog 或確認通過」。本次人決定：不修 blog，卡用保守寫法（有矛盾的主張標 pending_author_confirmation 或不使用） | 照辦 | — |
| 15 | blog 內部矛盾清單（6 項明確錯誤）：193.6 倍算法對不上；「第三方 5–25 倍」涵蓋成本卻與表格 580x/8.6x/1.6x 衝突；0.3298 應為 0.3299；「85 到 95 折」與表格換算不符；「兩種 0%」只說明一種；「500 vs 1,530」應為 530 | 見各卡 | — |
| 16 | 我（撰寫者）漏發 5 個讀者 subagent 而不自知：多 agent 並行時要有「應到/實到」清單 | 補發；之後用檔案計數核對 | 否 |
| 17 | subagent 並行上限是 20；一輪 11 張卡 × 2 位審查者 = 22 個，超過上限，最後 2 個發不出去 | 分批派發：先發對證者，有完成再補讀者；以檔案計數核對「應到／實到」 | 否（流程需寫明批次大小） |
| 18 | 審查者提示詞放在 skill 的 `references/`，派發時只傳路徑變數，subagent 可直接讀取使用，派發訊息大幅縮短 | 採用 | — |
| 19 | `pending_author_confirmation` 的主張必然含 blog 矛盾，對證者每輪都會對它報錯，導致整張卡永遠過不了 | `verify_audit.py`：pending 主張的問題降為備註（疑似捏造引用除外）。規格 02 §9 應補寫：pending 主張不計入審查通過條件 | 否 |
| 20 | 第 2 輪（修卡後）：對證者 1/11 通過、讀者 7/11 通過；剩餘多為「來源引用沒涵蓋」「錨點類型邊界」與我改寫時範圍過頭 | 第 3 輪前逐條修 | — |
| 21 | 第 3 輪（輪數上限）：對證者 1/11 通過（agreement-rate，第 2 輪通過後未改動）、讀者 9/11 通過。其餘 10 張對證者仍有退回，依 02 §7.3 升級給人，不自動放行 | 見交付報告 | — |
| 22 | 第 3 輪剩餘退回分四類：(a) 措辭小幅放大或掉限定（可直接修）；(b) 錨點類型邊界判斷（同一句在不同輪被不同方向挑，例如「官方明講」歸屬）；(c) 「主張互核矛盾」其實是 blog 自己的矛盾（580x vs 238x、單次前向傳播 vs 嚴格說不是）；(d) 審查者自己的錯：reward-source c1 的「疑似捏造」是審查者把省略號片段順序顛倒，程式照規則擋下，卡本身沒錯 | 需人裁決 (b)(c)；(a) 可修；(d) 應在 verify_audit 區分「審查者引用錯誤」與「卡的引用錯誤」 | 否 |
| 23 | 嚴格對證者每輪都能找到新的措辭瑕疵，3 輪不保證收斂；退回數雖逐輪下降，但 (b) 類在輪與輪之間會反覆翻轉 | 02 §7.3 的 3 輪上限需搭配「(b)(c) 類改交人裁決，不計入退回」的規則 | 否 |
| 24 | 審查成本：依各 subagent 回報的 usage 加總，對證者每個約 8～9 萬 token（要讀完整篇 blog 約 3 萬字、跑重算、寫 JSON），讀者每個約 4 萬；一輪 11 卡約 130～140 萬，三輪（共 64 個 subagent）合計約 400 萬。審查成本遠高於寫卡（先前版本寫成 250 萬是低估）。主要成因：每輪全新審查者全面重審、blog 全文每次重讀、預設不通過、卡寫得過粗導致多輪 | 規格 §7 應評估：讀者只審 §7.2 主軸題、陷阱題改用程式抽樣；對證者只重審有改動的主張；blog 全文改為按小節切片給審查者 | 否 |

## 人決定採用的調整（本次先照做，規格與 skill 待流程結束後一起改）

| # | 調整 | 做法 | 規格已改 |
|---|---|---|---|
| 25 | 觀念太多：一篇 blog 提煉出 11 張，且 7 張剛好對應 blog 末段「脫離這篇報告也成立」的 7 個小標題（機械式一標題一卡），其餘 4 張是 Jev 專屬 | 採用合併規則：(R1) 同錨點合併；(R2) 產品綁定的清單型內容降級併入產品概覽；(R3) 一卡一個「所以呢」；(R4) blog 的摘要段落只用來交叉驗證，不一節一卡；(R5) 軟上限，單篇先以 5～6 張為準。11 張合併為 6 張：jev-overview（吸收 failure-modes）、schema-valid-not-correct、confound-three-questions（吸收 agreement-rate）、honest-probability-training（rlhf + reward-source + proper-scoring）、decompose-narrow-and-shallow（吸收 kv-cache）、efficiency-accuracy-error-cost。合併前快照在 scratchpad `old-cards-round3/` | 否（02 §3、§4 需補寫 R1–R5） |
| 26 | 審查過嚴：「一個原子不是完全支持就整張退回」不分輕重，第 2、3 輪多為低價值退回 | 分級：blocker（不支持/找不到、捏造、數字錯、範圍或因果放大、改變用法的限定掉了、標官方宣稱卻非官方）才擋；minor（措辭差異、來源引用沒涵蓋但 blog 有支持、相鄰錨點邊界、blog 自身矛盾、審查者引用錯誤）只記錄。以此重算第 3 輪：11 卡中 7 卡無 blocker | 否（02 §7.1） |
| 27 | 每輪全面重審浪費：已通過的主張被重複審 | `claim_fingerprints.py`：依主張內容指紋，只重審新增或改過的主張；auditor-prompt 加 `{ONLY_CLAIMS}`；`verify_audit.py --only` | 否（02 §7.3） |
| 28 | 先前把 43 萬讀者 token 稱為「白費」是誇大：那是第 1 輪讀者全部成本，其中名詞缺口發現有用，浪費的只有通用題部分。讀者題目由撰寫者出仍削弱獨立性，建議改程式自動出題（每個有 comparison_target 的數字自動問比較對象；陷阱題從 blog 取卡未收的事實） | 本次沿用人工出題；自動出題列為待做 | 否（02 §7.2） |

## Stage 1 放行（2026-10-04）

| # | 項目 | 內容 |
|---|---|---|
| 29 | 放行 | 人放行 6 張卡（108 條主張，8 條 pending 維持不用）。審查最終狀態：分級規則下 6 張無 blocker、讀者 6 張通過。唯一未重審的是 decompose c3 的限定條件（審查者指定、blog 逐字引用、程式驗證） |
| 30 | 通用知識 | 加進背景詞清單：guardrail、prompt injection、jailbreak、schema、parse/parsing、regex、GPU、batch、attention。MTok、rubric、map-reduce 不加 |
| 31 | 關係 | 設 related（jev-overview 與其餘 5 張互連；confound 與 efficiency、schema-valid 互連），不設 parent |
| 32 | 人的偏好（待併入規格 02 §8） | 人說：之後 Stage 1 審核迴圈通過，就可以自動進入 Stage 2（不必每次等人放行）。與 CLAUDE.md「每做完一個階段先請人看過」衝突，需在整理 skill 時明定：迴圈通過的條件、哪些情況仍要人（blocker 升級、爭議、pending 新增、通用知識、去重關係） |

## 重構後的煙霧測試（2026-10-04，新審查流程第一次用 subagent 跑）

目的：確認新提示詞與驗證程式能實際運作。對象是已放行的卡，**沒有修改任何卡**（卡是已放行的成品，改動要走審查迴圈並由人決定）。

| 測試 | 結果 | token（subagent 回報） |
|---|---|---|
| 對證者（只看卡副本，paragraph 模式）審 `schema-valid-not-correct` 全部 9 條主張 | 輸出格式正確，`verify_audit.py --copy` 通過（blocker 0）；只有 c2b 一則 minor「錨點類型標錯」，審查者引用全部出自副本 | 約 4.5 萬（舊流程每個對證者約 8～9 萬；這張是最小的卡，只是一個資料點） |
| 全文審查（讀整篇 blog，一次審 6 張卡） | 輸出格式正確、引用全部逐字驗證通過；`verify_final_audit.py` 退回：2 個 blocker、2 個交人裁決、2 則備註 | 約 11.9 萬 |

全文審查的發現（**已放行的卡裡有尚未處理的問題，等人決定**）：
- blocker：`efficiency-accuracy-error-cost` c6 把一致率差距當成準確率損失，卻沒帶「一致率只量像不像參考模型」的限定（同樣的限定 c4 有帶）。
- blocker：`decompose-narrow-and-shallow` c2 把輸出型別這句整條標「官方宣稱」，但 `jev-overview` 卡把同一件事標「部落格考證」，blog 原句是作者自己的整理，只有輸入結構明寫「官方明講」。
- 備註：`decompose-narrow-and-shallow` c8 與 `jev-overview` c22 的破折號後「多步驟推理」可能是 blog 作者的詮釋，卡整句標第三方實測。
- 交人：blog 一處說 RLCD 的 reward 是 proper scoring rule 公式、另一處說 reward 設計全數未公開（相關 `honest-probability-training` c13）；blog 一處說單次前向傳播、另一處說嚴格說不是（相關 `decompose-narrow-and-shallow` c3、c14）。
- 全文審查另外重算出的兩個 blog 算式問題（193.6 倍的算法、Every 成本倍數 580 倍高於官方頭條 444.6 倍）都已是 `confound-three-questions` 的 pending 主張（c4、c16）。

觀察：新流程的全文審查在這批「舊流程已放行」的卡裡仍找出 2 個 blocker，包含**跨卡**不一致（同一句話在兩張卡標了不同錨點類型）與限定條件落差——這類問題只看單張卡的引文是看不出來的，是保留全文審查的理由。這只是一次煙霧測試，不是回歸測試；審查者嚴格度的量測見 `.claude/skills/distill-article/references/regression-tests.md` §2。
