# Semantic-Guesser 標記說明

## 標記類型

`run_semantic_guesser.py` 輸出的 JSONL 包含兩類標記：**CLAWS7 詞性標記**（來自 semantic-guesser）以及少數**自定義標記**（由腳本補充）。

---

### 自定義標記

| Tag | 意義 |
|-----|------|
| `NUMBER` | 純數字（`123`, `99` 等） |
| `SPEC` | 特殊符號（`!`, `@`, `=` 等） |
| `X` | 無法識別的字串 |

---

### CLAWS7 標記（名詞類）

| Tag | 意義 | 範例 |
|-----|------|------|
| `nn1` | 單數可數名詞 | *love, man, god* |
| `nn2` | 複數可數名詞 | *guns, people* |
| `np` / `np1` | 專有名詞（單數） | *Orlando, Gabriel* |
| `np2` | 專有名詞（複數） | *Vikings* |
| `npm1` | 月份名詞 | *Jan, Oktober* |

### CLAWS7 標記（代名詞類）

| Tag | 意義 | 範例 |
|-----|------|------|
| `ppio1` | 受格人稱代名詞（單數） | *me, him* |
| `ppho2` | 受格人稱代名詞（複數） | *them* |
| `ppis2` | 主格人稱代名詞（複數） | *we* |
| `pnqs` | 疑問代名詞 | *who* |

### CLAWS7 標記（動詞類）

| Tag | 意義 | 範例 |
|-----|------|------|
| `vvi` | 動詞不定式 | *love, win, kill* |
| `vvz` | 動詞第三人稱現在式 | *murders, loves* |
| `vbr` | be 動詞（are） | *are* |
| `vbi` | be 動詞（be） | *be* |
| `vbz` | be 動詞（is） | *is* |

### CLAWS7 標記（其他）

| Tag | 意義 | 範例 |
|-----|------|------|
| `jj` | 形容詞 | *black, mega* |
| `ii` | 介系詞 | *at, in, of* |
| `at1` | 不定冠詞 | *a, an* |
| `csa` | 次分類連接詞 | *as* |

---

## 規則來源

標記規則分散在三個地方：

### 1. `model/semantic-guesser/data/brown_clawstags.pickle`（最核心）

Brown 語料庫，人工標注了數百萬個英文詞的 CLAWS7 tags。這是整個 tagger 的訓練資料，以 pickle 預存，不需要重新訓練。

### 2. `model/semantic-guesser/learning/tagset_conversion.py`

Tag 對應表，把 Brown corpus 的標記系統（Brown tagset）轉換成 CLAWS7：

```python
'NN'  → 'NN1'   # 單數可數名詞
'NNS' → 'NN2'   # 複數可數名詞
'VB'  → 'VVI'   # 動詞不定式
...
```

### 3. `model/semantic-guesser/learning/pos.py`

Tagger 邏輯，由多層退回（backoff）組成，每層查不到才往下退：

```
TrigramTagger
  → BigramTagger
    → COCATagger       ← 查 COCA 詞頻字典 (data/coca_500k.csv)
      → NamesTagger    ← 查姓名清單 (data/names.txt 等)
        → WordNetTagger ← 查 WordNet 詞性
```

範例：
- `love → nn1`：來自 Brown corpus 的訓練結果
- `Orlando → np1`：來自 `data/mnames.txt`（男性名字清單）

---

## 與 LLM 標記的比較

| 面向 | semantic-guesser | LLM（Qwen3-8B / Llama） |
|------|-----------------|------------------------|
| 標記類型 | 詞性標記（CLAWS7） | 語意標記（自定義） |
| 範例 | `love → nn1` | `love → ENGLISH_VERB` |
| 標記來源 | Brown corpus + WordNet | 模型訓練時的語言理解 |
| 非英文詞 | 多數標為 `X` | 嘗試給語意標記（如 `MALE_NAME`, `LOCATION`） |

兩種切分結果的 Jaccard Distance 比較，可以反映 LLM 的語意理解與傳統 NLP 方法之間的異同。
