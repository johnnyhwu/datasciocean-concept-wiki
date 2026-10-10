# 目前狀態

每次實跑後更新這份；CLAUDE.md 只放連結，不放會過期的數字。token 用量另記在 `stage1-token-usage.md`。

## 觀念庫

- 共 10 張卡，尚未 commit：
  - `jev-as-a-judge`（2026-10-06，第二次實跑）：5 張。
  - `skillopt`（2026-10-10，第三次實跑）：5 張（`skillopt-overview`、`skillopt-batch-evidence-minibatch`、`skillopt-bounded-edit-budget`、`skillopt-blind-acceptance-gate`、`skillopt-epoch-level-control`），2 條 pending（概覽卡 c9、編輯預算卡 c4）。
- 第一次實跑的 6 張卡（`jev-overview`）留在 `tests/fixtures/concepts/` 當測試資料，完整歷史在 git。

## 流程現況

- 對證者只看引文與段落 → 讀者看移除引用的卡 → 全文審查每篇一次。
- 2026-10-06 加入：寫卡前先給人看提案（提案階段不看主張數）→ 合併後檢查每張卡 10 到 20 條主張（`validate_card.py --claim-count`）→ 審查開始後不再併卡；補審合併成一個 subagent；只動限定條件不重跑讀者。
- 2026-10-10（第三次實跑後）：同一篇文章共用的脈絡連同限定條件複製到每張卡；圖說裡才有的比較對象或範圍在提案階段先標出；脈絡主張描述本文方法時標「設計參數」；來自 blog 措辭的跨卡矛盾交人決定後不再擋第 3 輪判斷。
