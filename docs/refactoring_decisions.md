# 專案重構決策記錄

> 日期：2026-03-30

---

## 1. 配置格式

- 將 `config.json` 改為 `config.yaml`，提升可讀性與註解支援。

## 2. 自動發現功能

### 模型自動發現
- 掃描 `model/` 目錄下的子資料夾，自動發現所有本地模型。
- 所有模型皆位於 `model/{模型名稱}` 下。

### 資料集自動發現
- 掃描 `data/` 目錄下所有 `.txt` 和 `.csv` 檔案，自動建立資料集列表。

## 3. 目錄結構調整

### 重命名
- `stastic/` → `statistics/`（修正拼寫）。

### 輸出結構
- 輸出路徑從 `gen/{experiment_name}/` 改為 `gen/{模型名稱}/exp_{第幾次}.jsonl`。
- 範例：`gen/Qwen3-8B/exp_1.jsonl`

## 4. 模組拆分

原本 `main.py` 混合了配置管理、模型載入、推論邏輯、輸出寫入，拆分為：

| 模組 | 職責 |
|------|------|
| `config.py` | 統一配置載入、路徑建構、自動發現 |
| `model_loader.py` | 模型與 tokenizer 載入 |
| `inference.py` | 推論邏輯（`analyze_password`, `parse_model_output`） |
| `main.py` | 流程串接（僅做 orchestration） |

- 移除 `stastic/jaccard_distance.py` 中重複的 `load_config`，統一使用 `config.py`。

## 5. Prompt 配置

- `prompt_template` 和 `tag_summary` 參數納入 `config.yaml`，可由使用者在設定檔中切換。

## 6. 專案結構重整 — `src/` 模組化

將所有功能模組移入 `src/`，根目錄僅保留執行入口與配置。

### 最終結構

```
pcfg_llm/
├── main.py              # 主推論流程入口
├── run_jaccard.py       # Jaccard 分析入口
├── show_prompt.py       # Prompt 預覽工具
├── config.yaml          # 配置檔
├── requirements.txt     # 依賴（新增 pyyaml）
├── src/                 # 所有功能模組
│   ├── __init__.py
│   ├── config.py        # 配置載入 + 自動發現
│   ├── model_loader.py  # 模型與 tokenizer 載入
│   ├── inference.py     # 推論邏輯
│   ├── prompt.py        # Prompt 模板
│   ├── tag.py           # 標籤定義
│   ├── clean_data.py    # 資料清洗
│   ├── jaccard.py       # Jaccard 計算函式
│   └── draw_result.py   # 視覺化繪圖
├── data/                # 資料集（自動掃描 .txt/.csv）
├── model/               # 模型（自動掃描子資料夾）
├── gen/                 # 生成輸出
├── statistics/          # 統計輸出（純輸出目錄）
└── docs/                # 文件
```

### 已刪除的檔案/目錄

| 項目 | 原因 |
|------|------|
| `config.json` | 已由 `config.yaml` 取代 |
| `process/` | `clean_data.py` 移至 `src/`，目錄不再需要 |
| `statistics/*.py` | 函式移至 `src/jaccard.py` 與 `src/draw_result.py`，執行邏輯移至 `run_jaccard.py` |
| `__pycache__/` | 快取，不需保留 |

### 新增的入口腳本

| 腳本 | 用途 |
|------|------|
| `run_jaccard.py` | 取代原 `statistics/jaccard_distance.py` 的 `__main__` 區塊 |

### 驗證結果（2026-03-30）

在 conda 環境 `llm_semocfg` 下驗證通過：

- 所有 `src.*` 模組 import 正常
- `config.yaml` 載入成功，自動發現模型 `Qwen3-0.6B`, `Qwen3-8B`
- 自動發現資料集 `000webhost.txt`, `rockyou-35.txt`
- 輸出路徑正確：`gen/Qwen3-8B/exp_1.jsonl`
- `show_prompt.py` 執行正常（exit 0）
- `clean_data` 清洗邏輯正常
