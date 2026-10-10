# 觀念卡格式（Concept Card Format）

這份文件是 **Stage 1（本 repo）與 Stage 2（`datasciocean-social-media` repo）之間唯一的契約**。Stage 2 把本 repo 當 submodule，只讀 `wiki/` 與本文件；Stage 1 完全不知道 Stage 2 怎麼用卡。改這份文件等於改契約，要同步檢查 Stage 2 repo 的 `cardlib.py` 與 `references/anchor-writing-rules.md`。

## 1. 設計原則

| 原則 | 內容 |
|---|---|
| 解耦 | 卡只放「觀念本身」，不放任何發布格式、貼文狀態、系列的欄位。這些屬於 Stage 2 repo。新增 Reels、Shorts 都不用改卡 |
| 卡是上限 | 下游的內容是卡的子集，不得加入卡上沒有的判斷、數字、缺席型主張 |
| 唯一來源 | 卡上所有內容只能來自 blog。模型自己的背景知識不得混進卡 |
| 單向 | 下游不會把問題退回 Stage 1，也不修改卡 |
| 多對多 | 一個觀念可來自多篇文章；一篇文章可提煉多個觀念 |
| 純文字 | markdown 加 YAML，人看得懂、git 可追版本、Claude Code 可直接讀寫 |

## 2. 目錄結構

```
wiki/
  index.md                    每個觀念一行：id、一句話論點、parent、related、status（程式產生，不手改）
  concepts/<concept-id>.md    觀念卡
config/
  params.yaml                 Stage 1 的所有可調參數
  background-terms.md         背景詞清單（人維護）
```

## 3. 卡檔案格式

檔名等於 `id`。檔案 = YAML frontmatter + 一個 `## 主張` 標題，底下一個含 `claims:` 的 ```yaml 區塊。程式只認「frontmatter」與「含 `claims` 鍵的 yaml 區塊」，標題文字與區塊外的說明文字自由。

```markdown
---
id: confound-three-questions
title: 看效能倍數之前，先問分母、比法、標準答案        # 一句話論點（thesis）
type_hint: 可遷移原則      # 常見：方法、發現、判斷、可遷移原則。只當參考，不是封閉分類
context_type: evidence_from_single_source   # 見 §3.1
sources:
  - article: jev-overview                    # blog 文章 slug
    article_title: "TypeSafe AI 的 Jev 號稱快 193.6 倍？第三方實測只到約 25 倍"   # 必須與 blog front matter 的 title 一致（程式驗證）
    url: https://datasciocean.com/ai-concept/jev-overview/
    sections:                                # 小節標題文字（不是章節編號），引文必須落在這些小節內
      - 任何效能對比數字出現之前，先問三個問題
    first_appearance: true
parent: null               # 上層觀念 id（見 §7）
related: []                # 相關觀念 id，無方向
status: active             # active | retired
---

## 主張

```yaml
claims:
  - id: c1
    role: thesis
    text: 效能對比數字出現之前，先問三個問題：分母怎麼選、評測公不公平、參考答案偏不偏
    source_quotes:
      - "任何效能對比數字出現之前，先問三個問題：…"
    anchor_type: 部落格判斷
    importance: 1
    status: normal
  - id: c2
    role: anchor
    text: TypeSafe 官網頭條宣稱快 193.6 倍、便宜 444.6 倍
    source_quotes: ["官方最常被引用的兩個數字是快 193.6 倍、便宜 444.6 倍"]
    anchor_type: 官方宣稱
    comparison_target: 前沿模型            # 含數字的主張必填
    qualifiers: []
    importance: 3
    status: author_confirmed
    confirmation: { date: 2026-10-01, note: "作者確認，寫法取保守" }
```
```

### 3.1 context_type（下游決定「脈絡」怎麼寫）

| 值 | 意思 | 例子 |
|---|---|---|
| `bound_to_source` | 綁在某篇論文或產品上（概覽、論文發現） | 某方法的概覽 |
| `evidence_from_single_source` | 通用觀念，但證據只來自單一來源 | 從某篇論文得到的通用做法 |
| `standalone_classic` | 獨立的經典概念，來源只是出現場合 | Decision Transformer、Bradley-Terry |

## 4. 主張（claim）欄位

| 欄位 | 必填 | 說明 |
|---|---|---|
| `id` | 是 | 卡內唯一，例如 c1、c2b |
| `role` | 是 | `thesis`（恰好一條）、`context`（至少一條，說明「這是什麼」）、`mechanism`、`anchor`、`evidence`、`evaluation`、`qualifier` |
| `text` | 是 | 用自己的話寫，但**盡量直接用 blog 的字**（改寫得越概括，越容易被審查者退回） |
| `source_quotes` | 是 | 從 blog 逐字複製的原文，可多段。可用「…」省略中間，每個片段都必須逐字且依序出現 |
| `anchor_type` | 是 | 見 §6，開放清單 |
| `comparison_target` | 含數字時必填 | 這個數字是跟誰比的。blog 沒寫就留空並標 `pending_author_confirmation`，或不使用 |
| `numeric_kind` / `numeric_reason` | 否 | 含數字但不是比較數字時，標 `numeric_kind: non_comparative` 並寫 `numeric_reason`（規格上限、日期、示範題、定義、名稱、假設題設），免填 `comparison_target`。**倍數、百分比、分數、價格不得豁免。** 所有豁免都會列給審查者逐條確認 |
| `qualifiers` | 否 | 綁在這條主張上的限定條件，每項含 `text` 與 `source_quote`。**使用這條主張的下游內容必須同時帶出它的限定條件** |
| `importance` | 是 | 數字越小越重要（thesis 必為 1）。下游依此由上往下取子集 |
| `status` | 是 | `normal`、`pending_author_confirmation`、`author_confirmed` |
| `confirmation` | status 為 author_confirmed 時必填 | `date` 與 `note`（已知疑慮） |

規則：
- 評價永遠跟它評價的觀念同一張卡，不獨立成卡，role 標 `evaluation`。
- 缺席型主張（「論文沒有提到…」）只有在 blog **明確寫出**時才能記。blog 沉默不等於不存在。
- 卡不記「卡的來源是 blog」這類資訊；來源只放在 `sources`。

### 4.1 status 的意思（下游必須遵守）

| status | 意思 | 下游怎麼用 |
|---|---|---|
| `normal` | 通過審查 | 可用 |
| `pending_author_confirmation` | 主張有疑慮（多半是 blog 自己前後矛盾），等作者決定 | **一律不用** |
| `author_confirmed` | 作者確認過，附已知疑慮 | 可用，寫法取保守的一邊，不得比卡上的句子更強 |

## 5. 背景詞清單

`config/background-terms.md` 由人維護，列出「讀者預設已經知道、卡不必解釋」的一般 AI 工程詞彙。一定要在卡上定義的只有兩類：blog 或論文自創的名詞；主軸論點直接依賴、又不在清單上的概念。下游（Stage 2）的讀者審查也讀這份清單，所以它是契約的一部分。

## 6. 錨點類型（開放清單）

清單在 `config/params.yaml` 的 `wiki.anchor_types`。**新增類型時，必須同時在 `datasciocean-social-media` repo 的 `references/anchor-writing-rules.md` 定義 Stage 2 的寫法規則**，否則下游不知道該怎麼寫。

| 類型 | 定義 |
|---|---|
| 實驗結果 | 論文或研究實際量到的數字 |
| 設計參數 | 方法提出者選的設定值，沒有證據顯示最佳 |
| 官方宣稱 | 產品方或公司自己公布的說法 |
| 第三方實測 | 獨立第三方的量測 |
| 數學推導 | 可自行驗算的計算 |
| 外部研究引用 | blog 引用的他人研究 |
| 原作者解讀 | 論文或官方對結果的詮釋 |
| 部落格推論 | blog 已明標為推論的內容 |
| 部落格考證 | blog 作者對官方或第三方資料的換算、解讀 |
| 部落格判斷 | blog 作者的評價 |
| 背景說明 | blog 對既有領域概念或方法的說明（RLHF 做什麼、某指標的定義）。若是這篇文章的核心論點，或是在描述本文方法自己的設計，則不適用，改標其他類型（描述設計標設計參數） |
| 部落格舉例 | blog 自己設計的假設情境或示範例子 |
| 社群評論 | blog 引用的社群留言或討論（如 Hacker News 最高票留言） |

標錯類型是常見錯誤（例如把設計參數標成實驗結果）；「官方宣稱」標錯會直接擋下，因為下游的主詞規則依賴它。

## 7. 觀念之間的關係

| 關係 | 欄位 | 說明 |
|---|---|---|
| 上下層 | `parent` | 一個觀念可以有上層觀念。結構是圖，不是樹 |
| 相關 | `related` | 無方向的橫向連結 |

**由下往上長**：一開始每個觀念都是獨立條目，同類觀念累積出兩三個實例後，才建立上層觀念。

**去重流程（寫卡時）**
1. 讀 `wiki/index.md`，找出相似觀念。
2. 提議關係：重複（把新來源追加到既有卡的 `sources`，不新建）、實例（新建卡並設 `parent`）、相關（設 `related`）、全新。
3. **由人確認**後才寫入。判斷錯誤會汙染整個 wiki。
4. 觀念第一次出現的文章記 `first_appearance: true`，之後出現追加一筆來源。

## 8. 結構驗證（`validate_card.py`，每次寫入前執行）

- `id` 全 wiki 唯一且等於檔名；`parent`、`related` 指向的觀念存在
- frontmatter 必填：`id`、`title`、`context_type`、`sources`、`status`；`sources` 每項含 `article`、`article_title`、`url`、`sections`、`first_appearance`
- `article_title` 與 blog front matter 的 `title` 一致；`sections` 都是 blog 存在的小節標題（同名小節全部比對）
- 每張卡恰好一條 `thesis`（importance 為 1）、至少一條 `context`
- claim `id` 卡內唯一；`role`、`status` 在允許值內；`anchor_type` 在清單內
- 含數字的主張必有 `comparison_target`，否則狀態必須是 `pending_author_confirmation`；例外：`numeric_kind: non_comparative` 搭配允許清單內的 `numeric_reason`，且主張不得含倍數、百分比、分數、價格寫法
- `source_quotes` 與 `qualifiers[].source_quote` 不為空，且**逐字出現在 blog**、落在 `sources.sections` 列出的小節內
- `author_confirmed` 必有 `confirmation.date`
- （Stage 1 內部檢查，不屬於卡格式契約）`--claim-count`：每張卡主張數須在 `config/params.yaml` 的 `wiki.card_claim_range`（預設 10 到 20，含 pending 主張）。只在合併階段使用，提案階段不檢查

逐字比對的正規化（`wikilib.normalize`）：NFKC 統一全半形、去掉 markdown 標記（粗體、表格線、標題與清單記號、連結語法、shortcode）、去掉引號字元、去掉所有空白。blog 與引文用同一個函式。引文裡的「…」把引文切成片段，每個片段都必須逐字出現且依序。

主張裡的數字沒出現在它的來源原文時，只標 HINT，不退回（寫法可能不同，例如「八分之一」與 1/8），交給審查者。

## 9. 讀寫權限

| 內容 | Stage 1 | 下游（Stage 2） | 人 |
|---|---|---|---|
| frontmatter 與 claims | 寫 | 讀（submodule，唯讀） | 放行、確認去重關係、確認 `author_confirmed` |
| `wiki/index.md` | 程式產生 | 讀 | |
| `config/background-terms.md` | 讀 | 讀 | 維護 |

## 10. 升級到資料庫的觸發條件

markdown 永遠是唯一的真相來源，資料庫只是從它重建的查詢索引。符合下列任一條件才考慮升級：
- 觀念數量大到 `index.md` 一次讀不完，去重需要向量檢索
- 需要跨條目的複雜查詢
- 要匯入成效數據做分析（未來的獨立分析系統）
