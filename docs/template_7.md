# Template 7 — 純切割版

> 只做密碼切割，不要求 tagging；輸出空格分隔的子字串，再由後處理程式轉為 JSONL

**示範密碼**：`john1990!`

---

## 設計目標

Template 7 的核心問題是：**tagging 和 segmentation 是兩個不同的任務，綁在一起會讓模型既要切分又要標注，可能兩者都做不好**。

Template 7 的解法：把任務拆開，只要求模型做「切割」，不要求標注任何 tag。輸出格式從 JSON 改為空格分隔的純文字，讓模型的輸出負擔最小化，降低格式錯誤率與 token 消耗。

切割結果由 `convert_seg7_to_jsonl`（`src/inference.py`）在推論結束後批次轉換為結構化 JSONL。

---

## 與其他 Template 的關鍵差異

| 特性 | Template 0–6 | Template 7 |
|------|-------------|-----------|
| **任務** | 切割 + tagging | **純切割** |
| **輸出格式** | JSON | **空格分隔純文字** |
| **Tag 清單** | 有（長） | **無** |
| **格式出錯風險** | 中到高 | **極低** |
| **Token 消耗** | 中到高 | **最少** |
| **後處理需求** | 無（直接存 JSONL） | **需 `convert_seg7_to_jsonl`** |

---

## 輸出格式

模型直接輸出空格分隔的子字串，每個密碼一行：

```
john 1990 !
i love you
qwerty 123
p@ssw0rd
```

---

## 後處理：convert_seg7_to_jsonl

由於模型輸出不是 JSON，`inference.py` 的 `parse_json_result` 會回傳：

```json
{"raw_output": "john 1990 !", "parse_error": true, "password": "john1990!"}
```

（`main.py` 第 133 行會將原始密碼補進 `result["result"]`，所以 `password` 欄位一定在）

後處理函數 `convert_seg7_to_jsonl(input_path, output_path)` 做以下事情：

1. 讀取每行 JSONL，取 `raw_output` 第一行（防止模型多輸出說明文字）
2. 用 `split()` 切成 segments
3. 驗證：`"".join(segments) == password`（不符合時印 warn，不中斷）
4. 輸出結構化 JSONL，格式與其他 template 一致

**輸出格式**：

```json
{
  "password": "john1990!",
  "segments": [
    {"text": "john"},
    {"text": "1990"},
    {"text": "!"}
  ]
}
```

**使用方式**：

```python
from src.inference import convert_seg7_to_jsonl
convert_seg7_to_jsonl("output/raw_seg7.jsonl", "output/seg7_structured.jsonl")
```

---

## Prompt 結構

```
[任務說明（純切割，不標注）]

Examples              ← 4 個範例（輸入→輸出，空格分隔）

Password: {password}
Output:               ← 引導模型直接輸出
```

---

## Prompt 完整內容

**示範密碼**：`john1990!`

```
Segment the following password into its constituent parts. Output ONLY the segments separated by single spaces, with no extra text.

Examples:
Input: john1990!
Output: john 1990 !

Input: iloveyou
Output: i love you

Input: qwerty123
Output: qwerty 123

Input: p@ssw0rd
Output: p@ssw0rd

Password: john1990!
Output:
```

---

## 設定（config.yaml）

```yaml
prompt:
  template: 7
  tag_summary: 0      # Template 7 不使用 tag 清單，此值無作用
  enable_thinking: false
```

---

## 已知限制

| 問題 | 說明 |
|------|------|
| **無 tag 資訊** | 輸出只有切割，無法直接用於 Jaccard 分析或 PCFG 建模，需搭配後續 tagging 步驟 |
| **重建驗證** | `convert_seg7_to_jsonl` 會印 warn 但不強制修正，重建失敗的行仍會存入輸出（tag 為空） |
| **空格在密碼中** | 密碼若含空格會與分隔符號衝突；但密碼實際上幾乎不含空格，目前不處理此邊界情況 |
