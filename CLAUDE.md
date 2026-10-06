# CLAUDE.md

這個 repo 是 **Stage 1：把 DataSci Ocean（datasciocean.com）的繁體中文 AI 論文解析文章，提煉成觀念卡**，累積成觀念庫（concept wiki）。進入專案後先讀完這份。

```
blog 文章（blog/ submodule）──[Stage 1：提煉觀念]──> wiki/concepts/（觀念卡）
                                                          │ （被 submodule 進下游 repo，唯讀）
                                                          ▼
                                    datasciocean-social-media：Stage 2 把觀念做成 IG 輪播與 Threads 串文
```

- 本 repo 只做 Stage 1。**Stage 2 在另一個 repo**（`datasciocean-social-media`，它 submodule 了本 repo）。本 repo 不放任何貼文、系列、發布狀態、視覺設計的東西，也不讀寫它們。
- 兩個 repo 只透過**觀念卡格式**交接，契約是 `docs/card-format.md`。

## 每次開始前

1. `git submodule update --remote`（blog 要是最新的）。
2. 缺環境才跑 `uv sync`。環境全在 repo 內（`.venv/`、`.uv-cache/`，設定在 `pyproject.toml`），**不要裝任何東西到全域**。腳本一律 `uv run python <script>`。

## 要做什麼就讀什麼

| 要做的事 | 讀 |
|---|---|
| 處理一篇 blog 文章、建卡、審卡 | `.claude/skills/distill-article/SKILL.md`（流程與細節都從它往下讀） |
| 卡長什麼樣、欄位與驗證規則 | `docs/card-format.md`（契約，Stage 1 與 Stage 2 共用） |
| 調整參數 | `config/params.yaml`（輪數上限、錨點類型清單、數字豁免…） |
| 背景詞清單（人維護） | `config/background-terms.md` |

## 不可違反的規則

1. **blog 是唯一的真相來源。** 不讀原論文，不用自己的背景知識補內容。blog 沉默不等於「論文沒有做」。
2. **觀念卡不放任何格式欄位。** 不放發布狀態、貼文、系列、hook。卡只描述觀念本身。
3. **審查者要獨立、要嚴格。** 每輪用全新的 subagent，審查者看不到撰寫者的推理；對證者預設不通過、必須引用原文；撰寫者不能反駁審查者，只能標「爭議」交給人。
4. **能用程式強制的規則，就寫在程式裡，不靠 LLM。** 引文逐字比對、數字必有比較對象、結構驗證都在 `scripts/`。LLM 負責需要判斷的事。
5. **每個數字都要有比較對象；錨點類型要標對。** 「官方宣稱」標錯會直接擋下。
6. **限定條件綁在主張上**（`qualifiers`），下游用主張就必須帶出它的限定條件。
7. **寧可暫停，也不降低標準。** 輪數用完仍有 blocker，升級給人，不自動放行。
8. **不確定就停下來問人。** 寫卡前的提案清單、去重與關係、blog 內部矛盾、通用知識詞、爭議條目、新增的 pending，都由人決定。
9. **環境限縮在 repo 內。** uv 的快取與虛擬環境都在 repo 內。
10. **撰寫者寫卡時就要謹慎。** 審查是最後防線，不是替撰寫者找限定條件的工具；照 `card-writing.md` §11 自檢，避免審查者來回多次、甚至全文審查才抓到問題。

## 目錄

```
CLAUDE.md
.claude/skills/distill-article/   Stage 1 的流程、腳本、審查者提示詞
docs/                             card-format.md（契約，Stage 1 與 Stage 2 共用）、stage1-token-usage.md（實跑的 token 紀錄）
config/                           params.yaml、background-terms.md（人會改的放這裡）
wiki/                             index.md（程式產生）、concepts/<id>.md
blog/                             blog 的 submodule（唯讀）
tests/                            test_stage1_programs.py、fixtures/concepts/（測試用的卡，不是真實觀念庫）
```

為什麼 `config/` 不放進 skill：這是人會調整的設定與人維護的詞表，放在根目錄一眼找得到；流程知識（agent 怎麼做事）才放 `.claude/`。`docs/card-format.md` 也留在根目錄，因為它是給下游 repo 看的契約，不只是給本 repo 的 skill 看。

## 與下游 repo 的關係

- 下游以 submodule 讀 `wiki/` 與 `docs/card-format.md`；下游看到的卡 = 你 commit 並 push 的版本。commit 與 push 由人決定時機，**不要自己 commit 或 push**。
- 改 `docs/card-format.md`（欄位、狀態語意、錨點類型）等於改契約，要提醒人同步更新下游的 `cardlib.py` 與 `references/anchor-writing-rules.md`。
- 新增錨點類型必須同時在下游定義 Stage 2 的寫法規則，否則不得新增。

## 目前狀態

- 觀念庫有 5 張卡（來自 `jev-as-a-judge`，2026-10-06 第二次實跑，尚未 commit）。第一次實跑的 6 張卡（`jev-overview`）留在 `tests/fixtures/concepts/` 當測試資料，完整歷史在 git。
- 流程是：對證者只看引文與段落 → 讀者看移除引用的卡 → 全文審查每篇一次。第二次實跑量過 token，見 `docs/stage1-token-usage.md`。
- 2026-10-06 加入：寫卡前先給人看提案（提案階段不看主張數）→ 合併後檢查每張卡 10 到 20 條主張（`validate_card.py --claim-count`）→ 審查開始後不再併卡；補審合併成一個 subagent；只動限定條件不重跑讀者。

## 工作方式

- `docs/card-format.md` 與 skill 是依實測整理出來的；細節有疑問時以它們為準，沒寫到的先問人，不要自己決定。
- 修改任何程式檢查或審查流程後，跑 `uv run python tests/test_stage1_programs.py`；新增檢查要加「故意做壞的版本」確認抓得到。
- 範例資料：`tests/fixtures/concepts/confound-three-questions.md` 是完整範例卡。
