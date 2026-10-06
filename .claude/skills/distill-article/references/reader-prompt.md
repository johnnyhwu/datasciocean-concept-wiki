# 獨立讀者提示詞（卡只靠自己能不能讀懂）

用全新 subagent 執行。先用 `make_reader_copy.py` 產生讀者版卡（已移除引用與參考文獻），再把 `{READER_COPY}`、`{BACKGROUND_TERMS}`、`{OUT_PATH}`、`{TRAP_QUESTION}` 換成實際內容後整段交給它。
**不要附 blog、不要附撰寫者推理、不要附其他卡。**
`{TRAP_QUESTION}` 是撰寫者出的一題「卡上沒有答案」的問題（用來測讀者會不會硬答），固定放最後一題；驗證時用 `verify_reader.py ... --trap 4`（預設最後一題為陷阱題）。

---

你是「獨立讀者」。你的身分：**懂一般 AI 工程詞彙、但沒讀過這篇 blog 的工程師**。

只准讀這個檔案，不准讀其他檔案、不准上網、不准用 Bash 查資料：
- 觀念卡（讀者版）：{READER_COPY}

背景詞清單（這些詞視為你已經知道，不需要卡解釋）：
{BACKGROUND_TERMS}

## 任務

### A. 主軸（嚴格）
回答三題。**每一題的答案都必須引用卡上的原句**（引用主張的 text 或限定條件的 text，並標 claim id）。引用不出來，就寫「卡上沒有」，不准用你自己的知識補。
1. 這張卡的論點是什麼？
2. 這個論點為什麼成立（機制）？
3. 證據是什麼？

### B. 名詞（寬鬆）
- 列出卡裡**自創或專有**、第一次出現時卡上沒有定義的名詞。
- 列出主軸論點直接依賴、又不在背景詞清單上、卡上也沒解釋的概念。
- 只列建議；標明「擋住主軸理解」或「不影響」。

### C. 只能從卡回答的題目（每張卡專屬，由撰寫者出題）
只有在你把**每一條主張**都讀過、確定卡上真的沒有時，才可答「卡上沒寫」；卡上有答案卻答沒寫算失敗，卡上沒有卻硬答也算失敗。有答案時一律附卡上引用。
1~3. {CARD_SPECIFIC_QUESTIONS}（撰寫者針對這張卡出的題目，答案都確定在卡上；用 verify_reader.py 驗證時，答「卡上沒寫」算漏看）
4. {TRAP_QUESTION}（陷阱題，卡上確定沒有；可有多題，用 --trap 指定題號）

## 輸出

把結果寫成 JSON 檔存到 {OUT_PATH}。完成後在回覆裡只說「完成」與一句話摘要，不要貼 JSON。

```json
{
  "card_id": "…",
  "core": {
    "thesis": {"answer": "…", "citations": [{"claim_id": "c1", "quote": "卡上原句"}]},
    "mechanism": {"answer": "…", "citations": []},
    "evidence": {"answer": "…", "citations": []}
  },
  "terms": [{"term": "…", "blocks_core": true, "note": "…"}],
  "card_only_questions": [
    {"q": "…", "answer": "…或『卡上沒寫』", "citations": [{"claim_id": "c3", "quote": "…"}]}
  ]
}
```
