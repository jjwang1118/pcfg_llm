# Prompt Template 比較

## 快速總覽

| 項目 | Template 0 | Template 1 | Template 2 | Template 3 | Template 4 | Template 5 | Template 6 | Template 7 |
|------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
| **設計哲學** | 標準基準版 | 開放探索版 | 嚴格限制版 | 極簡版 | 開放+X強制代價版 | 開放+X強制代價+失敗範例版 | RAG 增強版 | **純切割版** |
| **任務** | 切割+tagging | 切割+tagging | 切割+tagging | 切割+tagging | 切割+tagging | 切割+tagging | 切割+tagging | **純切割** |
| **輸出格式** | JSON | JSON | JSON | JSON | JSON | JSON | JSON | **空格分隔純文字** |
| **X 標籤門檻** | 低（直接允許） | 中（需附說明） | 極高（幾乎禁止） | 低（直接允許） | 高（需窮舉後才可用） | 高（需窮舉後才可用） | 中（需說明） | **無（不做 tagging）** |
| **alt_tag** | 無 | 無 | 無 | 無 | 無 | 無 | **有（模糊時選填）** | 無 |
| **RAG 注入** | 無 | 無 | 無 | 無 | 無 | 無 | **有（動態依密碼撈取）** | 無 |
| **推論階段** | 單次 | 單次 | 單次 | 單次 | 單次 | 單次 | **兩階段（可選）** | **單次＋後處理** |
| **指令條數** | 5 | 6 | 4 | 僅格式樣板 | 7 | 7 | 7 | **0（僅範例）** |
| **失敗範例** | 無 | 無 | 無 | 無 | 無 | **有（3組對比）** | 無 | 無 |
| **正確範例數** | 4 個 | 6 個 | 2 個 | 0 個 | 6 個 | 6 個 | 3 個 | **4 個** |
| **Tag 說明來源** | `tag_description(tag_summary)` | `tag_description(tag_summary)` | 強制 `tag_description(1)` | `tag_description(tag_summary)` | `tag_description(tag_summary)` | `tag_description(tag_summary)` | `tag_description(tag_summary)` | **無** |
| **提示詞長度** | 中等 | 長 | 中等 | 最短 | 長 | 最長 | 依 RAG 結果（中到很長） | **最短** |

---

## 各模板詳述

### Template 0 — 標準基準版

- **目的**：作為對照基準，指令完整但不偏激
- **X 標籤**：允許使用，無需附加任何說明或解釋
- **格式**：嚴格 `{"text": "...", "tag": "..."}` 僅兩欄位，禁止多餘欄位
- **範例**：4 個（涵蓋名字年份、代詞動詞、鍵盤序列、LEET）
- **特點**：指令第 5 條明確說「不匹配就用 X」；`tag_description` 中保有 X 定義及括號提示

### Template 1 — 開放探索版

- **目的**：最大化語意發現能力，探索標籤系統的不足之處
- **X 標籤**：**強制**附帶 `suggested_tag`（建議新標籤名稱）與 `explanation`（解釋原因），不可省略
- **格式**：二合一格式——一般標籤僅兩欄，X 標籤四欄
- **範例**：6 個（額外包含 X 標籤使用示範三例：字尾模式、義大利姓氏、中文名字）
- **特點**：指令強調「語意優先於死板分類」；結尾再次提醒 X 標籤必填欄位
- **潛在問題**：X 的使用門檻不夠高，"unrecognized" 定義模糊，模型可能在嘗試前四步前就短路給 X

### Template 2 — 嚴格限制版

- **目的**：確保輸出標籤完全在預定義系統內，適合需要嚴格量化比較的實驗
- **X 標籤**：**應極力避免**；遇到不確定時應「進一步拆分」或「與相鄰片段合併」
- **格式**：嚴格兩欄，`tag_description` 強制傳入 `1`（尾端改為「必須從現有標籤選擇，禁止建立新標籤」警告）
- **範例**：最少，僅 2 個
- **特點**：從資訊層面封鎖 X 標籤使用
- **潛在問題**：模型為了避免 X 可能強行套用不合適的標籤，導致標錯但表面乾淨

### Template 3 — 極簡版

- **目的**：以最少約束測試模型自主推斷能力，觀察無詳細引導下的輸出品質
- **X 標籤**：允許，無任何額外要求
- **格式**：直接在提示詞中嵌入輸出格式當作樣板，無詳細範例
- **範例**：**0 個**
- **特點**：無角色設定、無逐步指令、無多語言提醒；適合測試模型基礎能力下限

### Template 4 — 開放+X強制代價版

- **目的**：在 Template 1 基礎上強化 X 標籤的使用成本，降低模型偷懶直接給 X 的情況
- **X 標籤**：**最後手段**，強制要求在 `explanation` 中說明「考慮過哪些標籤、為何每個都不適用」
- **格式**：與 Template 1 相同（標準兩欄 / X 標籤四欄）
- **範例**：6 個（X 標籤範例的 `explanation` 改為「Considered A, B — none fit because...」格式）
- **與 Template 1 的關鍵差異**：
  1. **指令順序**：第 1 條改為「語意優先」（定錨效應），讓模型在切割前就以語意視角觀察密碼
  2. **X 的前提條件**：明確要求「窮舉步驟 1–5 後仍無法分類才可使用」
  3. **X 的 explanation 格式**：從「why this pattern」改為「which tags were considered and why eliminated」，強制 chain-of-thought
  4. **條數調整**：6 條 → 7 條（原第 6 條語意優先移至第 1 條，新增 X 的排除分析要求）

### Template 6 — RAG 增強版

- **目的**：動態注入與密碼最相關的 tag 定義（含正例、反例），讓模型在更豐富的語意上下文下做決策
- **X 標籤**：中等門檻，需附 `suggested_tag` 與 `explanation`（同 Template 1）
- **alt_tag**：新增選填欄位，僅在對某 segment 真正不確定時使用，保留 PCFG 多路徑可能性
- **RAG 注入位置**：`# Examples` 之後、`# Task` 之前（recency bias，越靠近任務模型越重視）
- **兩階段推論**（`two_pass: true` 時）：
  1. 第一次用 Template 1 讓模型自主切分
  2. 用各 segment 文字（不含 tag）分別查詢 RAG
  3. 第二次帶 RAG context 用 Template 6 重新標注
- **RAG 為空時**：`# Reference Definitions` 區塊不出現，行為等同 Template 1
- **潛在問題**：
  - 語意空間錯位——密碼字串與 tag 定義文章的 embedding 空間不同，RAG 分數偏低（0.1–0.2），但相對排序仍有意義
  - 兩階段誤差放大——若第一次切分錯，RAG 撈到的定義也會偏錯
  - 速度約為 Template 1 的兩倍

詳細說明見 [docs/template_6.md](template_6.md)。

### Template 7 — 純切割版

- **目的**：只做密碼切割，不標注任何 tag；任務拆解後讓模型專注於 segmentation，降低輸出負擔
- **輸出格式**：空格分隔純文字（`john 1990 !`），不是 JSON
- **Tag 清單**：無（省略整個 `# Available Tags` 區塊，大幅減少 prompt 長度與 token 消耗）
- **後處理**：推論結束後由 `convert_seg7_to_jsonl`（`src/inference.py`）批次轉換為結構化 JSONL
  - 取 `raw_output` 第一行，`split()` 切分
  - 驗證重建完整性（`"".join(segments) == password`）
  - 輸出 `{"password": "...", "segments": [{"text": "..."}]}` 格式
- **適用場景**：只需切割結果（不需要 tag）；或作為兩步驟流程的第一步（先切割，再另外標注）

詳細說明見 [docs/template_7.md](template_7.md)。

### Template 5 — 開放+X強制代價+失敗範例版

- **目的**：在 Template 4 基礎上加入對比性失敗範例，透過「正誤對比」明確邊界情況
- **X 標籤**：與 Template 4 相同
- **格式**：與 Template 4 相同
- **範例**：6 個正確範例 + **3 組失敗範例對比**
- **失敗範例設計**：

  | 輸入 | 錯誤標籤 | 正確標籤 | 說明的核心概念 |
  |------|---------|---------|--------------|
  | `password` | `LEET` | `ENGLISH_NOUN` | 無字元替換 ≠ LEET，視覺相似不等於語意相同 |
  | `p@ssw0rd` | `ENGLISH_NOUN` | `LEET` | 有字元替換（`@`→a、`0`→o）才算 LEET |
  | `abc`（來自`abc123`） | `X` | `KB` | 有既有標籤可用時不能用 X，強化「最後手段」 |

- **與 Template 4 的關鍵差異**：唯一差異是在 `# Examples` 之前插入 `# Counter-examples` 區塊
- **潛在優勢**：對比性示範讓模型更清楚邊界，尤其對 LEET vs ENGLISH_NOUN 這類視覺相似但語意不同的情況
- **潛在代價**：Prompt 長度最長，對較小的模型可能造成注意力分散；失敗範例增多可能讓模型過度關注錯誤模式

---

## Template 1 → 4 → 5 演進比較

| 改動點 | Template 1 | Template 4 | Template 5 |
|--------|-----------|-----------|-----------|
| 指令第 1 條 | 切割密碼 | **語意優先**（前移） | 語意優先（同 4） |
| X 使用條件 | "For unrecognized patterns" | "Only after exhausting steps 1–5, as last resort" | 同 4 |
| X 的 explanation 要求 | 說明這個模式是什麼 | 說明考慮過哪些標籤及排除原因 | 同 4 |
| 失敗範例 | 無 | 無 | **有 3 組對比** |
| 主要防止的問題 | — | 模型在未嘗試前就給 X | 模型混淆視覺相似標籤（如 LEET/ENGLISH） |

---

## 設計軸線

```
嚴格限制 ←——————————————————————————————→ 開放探索
Template 2    Template 0    Template 3    Template 1/6  Template 4/5
（禁X）      （標準）      （極簡）      （需說明）    （X須代價）

詳細引導 ←——————————————————————————————→ 精簡
Template 5    Template 4    Template 1    Template 6    Template 0    Template 2    Template 3    Template 7
（6例+3反例） （6例）       （6例）       （3例+RAG）  （4例）       （2例）       （0例）       （4例，無tag清單）

X 使用成本 ←—————————————————————————————→ 低
Template 2    Template 4/5  Template 1/6  Template 0/3  Template 7
（幾乎封鎖）  （最後手段）  （需說明）    （自由使用）  （不做tagging）

外部知識注入 ←————————————————————————————→ 無
Template 6    Template 0/1/2/3/4/5/7
（RAG動態撈取）（僅靜態 tag 清單或無清單）
```
