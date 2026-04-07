# run_semantic_guesser.py 運作流程

以 `loveme99` 為例，說明完整處理流程。

---

## Step 1：getchunks — 切成字元類型區塊

先用 regex 把密碼拆成「字母」、「數字」、「符號」三類區塊：

```
"loveme99"  →  ["loveme", "99"]
```

接著對每個**字母區塊**呼叫 `wordsegment.segment()`：

- 技術：Google ngram **機率表**（靜態文字檔）+ 動態規劃
- 原理：找在真實英文裡出現機率最高的切法
- 例：`P("love","me") > P("lo","veme")` → 選 `["love", "me"]`

最終 chunks：`["love", "me", "99"]`

---

## Step 2：pos_tag — 詞性標記

`pos_tag` 判斷哪些 chunk 值得標記：
- 數字、符號 → 直接給 `None`
- 孤立短字母（如單一 `"q"`）→ 也給 `None`
- 相鄰的字母序列 → 送進 BackoffTagger

### BackoffTagger 查詢順序（找到就停止）

```
TrigramTagger（統計：看前後文的詞序共現次數）
  → BigramTagger（統計：看前一個詞）
    → COCATagger（查表：coca_500k.csv，50萬詞頻率）
      → NamesTagger（規則表：names.txt / mnames.txt / countries.txt）
        → WordNetTagger（詞典：WordNet 詞性資料庫）
```

結果：
```
"love"  →  nn1    （COCA 最常見詞性為名詞）
"me"    →  ppio1  （受格人稱代名詞）
"99"    →  None
```

---

## Step 3：derive_tag — 補全 None

`run_semantic_guesser.py` 對標記為 `None` 的 chunk，依內容補上自定義標記（純規則）：

```python
全數字  → NUMBER
全符號  → SPEC
其他   → X
```

```
"99"  →  全數字  →  NUMBER
```

---

## 最終輸出

```json
{"password": "loveme99", "segments": [
  {"text": "love", "tag": "nn1"},
  {"text": "me",   "tag": "ppio1"},
  {"text": "99",   "tag": "NUMBER"}
]}
```

---

## 各步驟技術類型總覽

| 步驟 | 工具 | 技術類型 | 知識來源 |
|------|------|----------|----------|
| 切分 | `wordsegment` | 統計機率表 | Google ngram 頻率 |
| 詞性標記（主） | `TrigramTagger` / `BigramTagger` | 統計模型 | Brown 語料庫（pickle） |
| 詞性標記（退回） | `COCATagger` | 查表 | `data/coca_500k.csv` |
| 詞性標記（退回） | `NamesTagger` | 規則表 | `data/names.txt` 等名單 |
| 詞性標記（退回） | `WordNetTagger` | 詞典查詢 | WordNet |
| 補全標記 | `derive_tag` | 純規則 | 自定義（NUMBER/SPEC/X） |

---

## 常見情況觀察

| 情況 | 行為 | 範例 |
|------|------|------|
| 英文常見詞 | 正確標記 | `chocolate → nn1`, `save → vvi` |
| 英文人名 | `np1`（來自 names.txt） | `gabriel → np1`, `orlando → np1` |
| 月份縮寫 | `npm1` | `jan → npm1` |
| 非英文字串 | wordsegment 強行切開 → 多半標 `X` 或誤判 | `taqiyudin → taqi(np1) + yudin(np1)` |
| 鍵盤走位 | 可能誤判 | `qwerty → jj`（誤判為形容詞） |
| 數字 | 直接 `NUMBER` | `99`, `2008` |
| 符號 | 直接 `SPEC` | `!@`, `=` |

---

## 與 LLM 的本質差異

| 面向 | semantic-guesser | LLM（Qwen3-8B 等） |
|------|-----------------|-------------------|
| 核心技術 | n-gram 統計 + 查頻率表 | Transformer 神經網路 |
| 硬體需求 | 純 CPU | GPU |
| 非英文處理 | 切分錯誤 → 多 `X` | 嘗試語意理解 |
| 標記類型 | CLAWS7 詞性 | 自定義語意標記 |
| 年代 | 2010 年代傳統 NLP | 2020 年代大語言模型 |
