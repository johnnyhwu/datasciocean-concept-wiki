# 派發 subagent 的訊息範本

四種審查者共通的做法：

- 一律用 `Agent` 派 `general-purpose`、`run_in_background: true`、**全新** subagent；訊息只給提示詞路徑與變數，不貼提示詞全文、不附撰寫者推理或其他卡。提示詞裡「只准讀這個檔案」指資料檔，提示詞檔本身當然要讀。
- 提示詞檔在 `.claude/skills/distill-article/references/`；訊息裡的路徑一律用絕對路徑。
- 下面的 `S` 是本次工作 scratchpad 裡的 `review/`（不進 repo）；每張卡一個子資料夾：`S/<card>/aud.md`、`round<N>-auditor.json`、`reader.md`、`round<N>-reader.json`；全文審查放 `S/final/`；限定條件對照檔是 `S/limits.md`。
- 並行上限 20，派不完就分批。完成通知到了，**用對應的 `verify_*.py` 驗證**，不要直接採信 subagent 回報的摘要；派完用檔案數核對應到／實到。
- **每個 subagent 約有 40k 的固定成本**（讀提示詞與檔案），即使只審 1 條主張。所以同一輪能一起改完的主張湊齊再補審，多張卡併成一個 subagent（§2）。

## 1. 對證者

```
請照提示詞檔 <repo>/.claude/skills/distill-article/references/auditor-prompt.md 的「---」線以下的內容執行對證者任務（先讀這個提示詞檔）。變數：
- AUDITOR_COPY = S/<card>/aud.md
- OUT_PATH = S/<card>/round1-auditor.json
- ONLY_CLAIMS = 省略（審全部主張）
<有附圖> 副本裡有附圖的主張，用 Read 看圖檔並依提示詞寫 figure_checks。
<無附圖> 這張卡沒有附圖，figure_checks 全給空陣列。
除提示詞檔、AUDITOR_COPY 與其列出的圖檔外，不准讀其他檔案。
```

驗證：`verify_audit.py <card.md> <json> --copy <aud.md> [--only c6,c7]`。

## 2. 補審（可多張卡併成一個 subagent）

副本用 `make_auditor_copy.py ... --only <ids>` 產生（檔名 `aud-r2.md` 之類）。同一輪有幾份就列幾份，**一個** subagent 依序審：

```
請照提示詞檔 …/auditor-prompt.md 的「---」線以下的內容執行對證者任務（先讀這個提示詞檔）。這次要依序審 N 份副本，各寫各的 JSON，不要把一份的原文拿去支持另一份。每份都只審 ONLY_CLAIMS 列出的主張（其他主張已通過，不必審也不必列進 JSON，但主張互核仍要對照）。受審主張沒有附圖的，figure_checks 給空陣列。

1. AUDITOR_COPY = S/<card-a>/aud-r2.md；OUT_PATH = S/<card-a>/round2-auditor.json；ONLY_CLAIMS = c6, c7
2. AUDITOR_COPY = S/<card-b>/aud-r2.md；OUT_PATH = S/<card-b>/round2-auditor.json；ONLY_CLAIMS = c10
除提示詞檔與這些 AUDITOR_COPY 外，不准讀其他檔案。
```

驗證逐份跑，`--only` 與派發的清單相同。

## 3. 讀者

先 `make_reader_copy.py <card.md> S/<card>/reader.md`，再出題（規則見 `review-loop.md` 關卡 2）。

```
請照提示詞檔 …/reader-prompt.md 的「---」線以下的內容執行獨立讀者任務（先讀這個提示詞檔）。變數：
- READER_COPY = S/<card>/reader.md
- BACKGROUND_TERMS_PATH = <repo>/config/background-terms.md
- OUT_PATH = S/<card>/round1-reader.json
- CARD_SPECIFIC_QUESTIONS（第 1～3 題，答案都在卡上）：
  1. …
  2. …
  3. …
- TRAP_QUESTIONS（第 4、5 題，卡上沒有答案）：
  4. …
  5. …
驗證時陷阱題是第 4、5 題。
```

驗證：`verify_reader.py S/<card>/reader.md <json> --trap 4 5`。

## 4. 全文審查（每篇文章一次，整篇 blog 加這篇的所有卡）

```
請照提示詞檔 …/final-audit-prompt.md 的「---」線以下的內容執行全文審查者任務（先讀這個提示詞檔）。變數：
- BLOG_PATH = <repo>/blog/content/posts/<section>/<slug>/index.zh-tw.md
- CARD_PATHS =
  <repo>/wiki/concepts/<card-1>.md
  <repo>/wiki/concepts/<card-2>.md
- OUT_PATH = S/final/round1-final.json
article 欄位填 <slug>。不必看圖。除提示詞檔、BLOG_PATH 與 CARD_PATHS 外，不准讀其他檔案。
```

驗證：`verify_final_audit.py S/final/round1-final.json <card.md>...`。第 2 輪的 OUT_PATH 改 `round2-final.json`。
