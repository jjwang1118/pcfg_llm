# PCFG-LLM：基於大型語言模型的密碼語意分析

本專案探索使用大型語言模型（LLM）對密碼進行 **PCFG（機率上下文無關文法）** 風格的語意切割與標記，並與傳統工具 [semantic-guesser](https://github.com/RUB-SysSec/semantic-guesser) 的結果進行量化比較。

---

## 專案目標

給定一個密碼（如 `john1990!`），讓模型將其切割為有意義的片段，並為每個片段標記語意標籤：

```
john1990! → [john, MALE_NAME] [1990, YEAR] [!, SPEC]
```

此方法擴展了傳統 PCFG 模型，加入多語言詞性識別與更豐富的語意類別。

---

## 支援模型

| 模型 | 說明 |
|---|---|
| `Llama-3.1-8B-Instruct` | Meta Llama 3.1 8B 指令微調版本 |
| `Qwen3-8B` | 阿里雲 Qwen3 8B 模型 |
| `semantic-guesser` | 傳統 NLP 工具，作為比較基線 |

---

## 語意標籤系統

本專案定義了 **46 種**語意標籤，涵蓋以下類別：

### 詞性標籤（多語言）
- **英文**（11 種）：`ENGLISH_NOUN`、`ENGLISH_VERB`、`ENGLISH_PRON`、`ENGLISH_ADJ` 等
- **德文**（5 種）：`GERMAN_NOUN`、`GERMAN_ADJ` 等
- **法文**（5 種）：`FRENCH_NOUN`、`FRENCH_VERB` 等

### 專有名詞與實體
`MALE_NAME`、`FEMALE_NAME`、`CN_NAME_ABBR`、`WKNE`、`UBE`、`LOCATION`

### 日期與數字模式
`YEAR`、`DATE_6DIGIT`、`DATE_8DIGIT`、`MONTH`、`CN_MOBILE`、`NUMBER`

### 字串結構模式
`EMAIL`、`URL`、`KB`（鍵盤序列）、`LEET`（Leet speak）、`PY`（拼音）、`SPEC`（特殊符號）等

---

## 目錄結構

```
pcfg_llm/
├── main.py                  # 主程式：LLM 密碼語意分析推論
├── run_jaccard.py            # 計算兩模型輸出的 Jaccard 距離
├── run_semantic_guesser.py   # 執行 semantic-guesser 基線推論
├── show_prompt.py            # 顯示 prompt 內容
├── config.yaml               # 統一設定檔
├── requirements.txt          # Python 依賴套件
├── data/                     # 密碼資料集
│   ├── rockyou-35.txt
│   └── 000webhost.txt
├── gen/                      # 各模型推論輸出（JSONL 格式）
│   ├── Llama-3.1-8B-Instruct/
│   ├── Qwen3-8B/
│   └── semantic-guesser/
├── model/                    # 模型權重與工具
│   ├── Llama-3.1-8B-Instruct/
│   ├── Qwen3-8B/
│   └── semantic-guesser/
├── src/                      # 核心模組
│   ├── config.py             # 設定載入與路徑建構
│   ├── inference.py          # LLM 推論與輸出解析
│   ├── prompt.py             # Prompt 樣板產生
│   ├── tag.py                # 語意標籤定義
│   ├── jaccard.py            # Jaccard 距離計算
│   ├── draw_result.py        # 結果視覺化
│   ├── model_loader.py       # 模型載入
│   ├── clean_data.py         # 資料清洗
│   └── record.py             # 實驗紀錄
├── statistics/               # 統計分析輸出（圖表、CSV）
└── docs/                     # 實驗設計文件
```

---

## 安裝

### 環境需求

- Python 3.10+
- CUDA（建議 GPU >= 16GB VRAM）
- Conda（建議）

### 建立環境

```bash
conda create -n pcfgllm python=3.10
conda activate pcfgllm
pip install -r requirements.txt
```

### 下載模型

將模型權重放置於 `model/` 目錄下，對應資料夾名稱需與 `config.yaml` 的 `active_model` 一致：

```
model/
├── Llama-3.1-8B-Instruct/   # Meta Llama 模型檔案
└── Qwen3-8B/                # Qwen3 模型檔案
```

---

## 使用方式

### 1. 修改設定

編輯 `config.yaml`，設定要使用的模型、資料集與推論參數：

```yaml
active_model: "Qwen3-8B"   # 使用的模型

data:
  datasets:
    - "rockyou-35.txt"       # 要分析的密碼資料集

prompt:
  template: 1                # 0=預設, 1=開放, 2=嚴格, 3=簡化
  enable_thinking: false     # 是否啟用 Qwen 的 thinking 模式

output:
  experiment_number: 1       # 實驗編號，輸出至 gen/{model}/exp_1.jsonl
```

### 2. LLM 推論

```bash
# 使用 config.yaml 中指定的資料集
conda run -n pcfgllm python main.py

# 指定資料集
conda run -n pcfgllm python main.py --datasets rockyou-35.txt 000webhost.txt

# 列出可用資料集
conda run -n pcfgllm python main.py --list-datasets
```

### 3. semantic-guesser 基線

```bash
conda run -n pcfgllm python run_semantic_guesser.py
```

### 4. 模型比較（Jaccard 分析）

```bash
conda run -n pcfgllm python run_jaccard.py
```

在 `config.yaml` 中設定要比較的兩個模型：

```yaml
jaccard:
  first_model: "semantic-guesser"
  first_exp: 1
  second_model: "Qwen3-8B"
  second_exp: 1
```

---

## 輸出格式

推論結果以 **JSONL** 格式儲存於 `gen/{model}/exp_{N}.jsonl`，每行為一筆密碼分析結果：

```json
{
  "password": "john1990!",
  "thinking": "",
  "result": {
    "password": "john1990!",
    "segments": [
      {"text": "john", "tag": "MALE_NAME"},
      {"text": "1990", "tag": "YEAR"},
      {"text": "!", "tag": "SPEC"}
    ]
  }
}
```

---

## 評估指標

### Jaccard 距離

比較兩個模型對同一密碼的切割差異，輸出直方圖、熱圖與排序長條圖：

```
statistics/jaccard/{first_model}_vs_{second_model}/exp_{a}_vs_exp_{b}/
├── jaccard_distance.csv
├── jaccard_histogram.png
├── jaccard_heatmap.png
├── jaccard_sorted_bar.png
└── single_passwords/        # 每個密碼的個別比較圖
```

---

## Prompt 樣板

本專案提供 4 種 Prompt 樣板（透過 `config.yaml` 的 `prompt.template` 設定）：

| ID | 說明 |
|---|---|
| 0 | 預設（含範例，開放 X 標籤） |
| 1 | 開放式（允許自訂 X 標籤並說明） |
| 2 | 嚴格式（禁止使用預定義以外的標籤） |
| 3 | 簡化式（精簡 prompt） |

---

## 實驗文件

詳細的實驗設計請參閱 `docs/` 目錄：

- [experiment_design.md](docs/experiment_design.md)：原始兩階段實驗設計
- [new_experiment_design.md](docs/new_experiment_design.md)：簡化單流程設計
- [pattern.md](docs/pattern.md)：標籤模式說明
- [refactoring_decisions.md](docs/refactoring_decisions.md)：重構決策記錄

---

## 授權

本專案僅供學術研究使用。

- Llama 模型：請遵守 [Meta Llama License](https://llama.meta.com/llama-downloads/)
- Qwen3 模型：請遵守 [Qwen License](https://huggingface.co/Qwen/Qwen3-8B/blob/main/LICENSE)
- semantic-guesser：請參閱 `model/semantic-guesser/LICENSE.txt`
