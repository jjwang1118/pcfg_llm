# Template 6 — RAG 增強版

> 結合 Retrieval-Augmented Generation（RAG）與兩階段推論，動態注入與密碼最相關的 tag 定義作為參考

**示範密碼**：`john1990!`

---

## 設計目標

Template 6 的核心問題是：**模型對標籤定義的理解不夠精確**。  
前幾版 template 都把完整的 tag 清單放進 prompt，但清單只有名稱與簡短描述，對模糊案例（例如 `john` 是 `MALE_NAME` 還是 `ENGLISH_NOUN`？）幫助有限。

Template 6 的解法：在模型推論前，先用 RAG 根據密碼內容撈出最相關的 tag 定義（含正例、反例、定義原文），插入 prompt 作為「參考資料」，讓模型在有更多語意上下文的情況下做決策。

---

## 與其他 Template 的關鍵差異

| 特性 | Template 1 | Template 4/5 | Template 6 |
|------|-----------|-------------|-----------|
| **X 標籤門檻** | 中（需說明） | 高（須窮舉） | 中（需說明） |
| **alt_tag** | 無 | 無 | **有**（選填，模糊時才加） |
| **RAG 注入** | 無 | 無 | **有**（動態依密碼撈取） |
| **推論階段** | 單次 | 單次 | **兩階段**（可選） |
| **Prompt 長度** | 長 | 最長 | 依 RAG 結果而定（中到很長） |
| **指令條數** | 6 | 7 | 7 |

---

## RAG 注入機制

### 知識庫

知識庫位於 `docs/tag_rag.md`，以 `##` 區分每個 tag，每個 tag 包含：

```markdown
## ENGLISH_NOUN
**Category**: Linguistic POS  
**Language**: English  
**Definition**: 英文名詞，指人、地、事、物…

**正例**（密碼語境下）：
- "dragon" in "dragon123" → ENGLISH_NOUN
- …

**反例**：
- "john" → 雖可能是英文詞，但在密碼中通常為人名 → 優先考慮 MALE_NAME
```

### 索引建置（離線）

`src/rag_index_offline.py` 讀取 `tag_rag.md`，用 `MarkdownHeaderTextSplitter` 依 `##` 切分，再手動將 tag 名稱加回 `page_content`（因為 splitter 預設只把標題放到 metadata），用 `BAAI/bge-m3` embedding 模型建立 FAISS 向量索引，儲存至 `faiss_index/`。

索引有 hash cache：若 `tag_rag.md` 未修改，跳過重建。

### 線上檢索（每筆密碼）

由 `src/rag_retrieval.py` 的 `RAGRetriever` 執行：

1. 用密碼字串（或各 segment 文字）做語意查詢
2. 取 `top_k`（預設 3）個最相近的 tag 定義
3. 過濾 `score_threshold`（預設 0.17）以下的結果
4. 將命中的 tag 定義以 `---` 分隔合併，注入 prompt

---

## 兩階段推論（Two-Pass）

`config.yaml` 中 `RAG.retrieval.two_pass: true` 時啟用。

```
密碼
  │
  ▼
第一次推論（template 1，無 RAG）
  │  → 得到初步切分，例如：
  │    [{"text": "john", "tag": "MALE_NAME"},
  │     {"text": "1990", "tag": "YEAR"},
  │     {"text": "!", "tag": "SPEC"}]
  │
  ▼
逐 segment 查詢 RAG（只用 text，不用 tag）
  │  → "john" → 撈出 MALE_NAME、ENGLISH_NOUN 定義
  │  → "1990" → 撈出 YEAR、NUMBER 定義
  │
  ▼
第二次推論（template 6，帶 RAG context）
  │  → 模型看到更精確的 tag 定義再做標注
  ▼
最終輸出（含 alt_tag）
```

**為什麼查詢時只用 `text`，不用 `tag`？**  
若把第一次推論的 tag 丟進 RAG 查詢，等於告訴模型「答案是這個 tag」，會放大第一次的錯誤。只用 segment 文字查詢，讓 RAG 提供相關定義，由模型自行決定最終標籤。

---

## alt_tag（替代標籤）

Template 6 新增 `alt_tag` 欄位，用於**真正模糊的 segment**。

- **規則**：只在對某個 segment 真的不確定時才加，不是每個都要加
- **格式**：`{"text": "john", "tag": "MALE_NAME", "alt_tag": "ENGLISH_NOUN"}`
- **用途**：保留 PCFG 多路徑的可能性，後續 Jaccard 分析或 PCFG 建模可參考

---

## 輸出格式

```
# 標準標籤
{"text": "...", "tag": "TAG_NAME"}

# 模糊標籤（選填 alt_tag）
{"text": "...", "tag": "TAG_NAME", "alt_tag": "ALTERNATIVE_TAG"}

# X 標籤（必填 suggested_tag 與 explanation）
{"text": "...", "tag": "X", "suggested_tag": "NEW_TAG_NAME", "explanation": "原因"}
```

完整輸出範例：

```json
{
  "password": "john1990!",
  "segments": [
    {"text": "john", "tag": "MALE_NAME", "alt_tag": "ENGLISH_NOUN"},
    {"text": "1990", "tag": "YEAR"},
    {"text": "!", "tag": "SPEC"}
  ]
}
```

---

## Prompt 結構

```
[角色設定]

# Available Tags          ← 完整 tag 清單（同 Template 1）

# Instructions            ← 7 條指令（含 alt_tag 使用規則）

# Output Format Requirements

# Examples                ← 3 個範例（含 alt_tag 示範）

# Reference Definitions   ← 【RAG 注入位置】放在 Examples 之後、Task 之前
  …RAG 撈出的 tag 定義…   （recency bias：越靠近 Task，模型越重視）

# Task
Password: {password}
```

---

## Prompt 完整內容（有 RAG 注入時）

**示範密碼**：`john1990!`  
**示範 RAG context**（假設撈出 MALE_NAME、YEAR 定義）：

```
You are a password semantic analyzer. Your task is to segment passwords into meaningful components and tag each segment based on PCFG (Probabilistic Context-Free Grammar) model.

        # Available Tags
        ## Linguistic POS Tags
### English:
  - ENGLISH_NOUN: Noun
  ...（完整 tag 清單）

        # Instructions
        1. Segment the password into its constituent parts based on semantic or structural significance
        2. Assign the most appropriate tag from the Available Tags list
        3. Recognize words from various languages (tags include English, German, French or other)
        4. Identify structural patterns including but not limited to: keyboard sequences, pinyin, leet speak, repetitions
        5. For unrecognized patterns, use "X" tag and provide "suggested_tag" and "explanation"
        6. Prioritize semantic meaning over rigid categorization
        7. If a segment is genuinely ambiguous between two tags, add "alt_tag" with the second most likely tag — only when truly uncertain, not for every segment

        # Output Format Requirements
        - Standard tags: {"text": "...", "tag": "TAG_NAME"}
        - Ambiguous segment (add alt_tag only when uncertain):
          {"text": "...", "tag": "TAG_NAME", "alt_tag": "ALTERNATIVE_TAG"}
        - X tags (MUST include suggested_tag and explanation):
          {"text": "...", "tag": "X", "suggested_tag": "NEW_TAG_NAME", "explanation": "why this pattern/what it represents"}
        - Output only the JSON object with "password" and "segments" fields

        # Examples
        Input: "john1990!"
        Output: {"password": "john1990!", "segments": [{"text": "john", "tag": "MALE_NAME", "alt_tag": "ENGLISH_NOUN"}, {"text": "1990", "tag": "YEAR"}, {"text": "!", "tag": "SPEC"}]}

        Input: "iloveyou"
        Output: {"password": "iloveyou", "segments": [{"text": "i", "tag": "ENGLISH_PRON"}, {"text": "love", "tag": "ENGLISH_VERB", "alt_tag": "ENGLISH_NOUN"}, {"text": "you", "tag": "ENGLISH_PRON"}]}

        Input: "qwerty123"
        Output: {"password": "qwerty123", "segments": [{"text": "qwerty", "tag": "KB"}, {"text": "123", "tag": "SR"}]}

        # Reference Definitions (Retrieved for This Password)
        The following definitions are retrieved based on this password's content.
        Use them as reference — if a retrieved definition does not match any segment, ignore it and rely on Available Tags.
        ## MALE_NAME
        **Category**: Named Entity
        ...（RAG 撈出的定義）
        ---
        ## YEAR
        ...

        # Task
        Analyze the following password and output ONLY the raw JSON object.
        Do NOT write any code. Do NOT use markdown. Do NOT add any explanation.
        The response MUST start with { and end with }.

        Password: john1990!
```

---

## 設定（config.yaml）

```yaml
prompt:
  template: 6         # 使用 template 6
  tag_summary: 0      # 完整 tag 清單（允許 X）
  enable_thinking: false

RAG:
  enabled: true
  index:
    knowledge_base: "docs/tag_rag.md"
    embedding_model: "BAAI/bge-m3"
    device: "cuda"
    normalize_embeddings: true
    index_path: "faiss_index"
  retrieval:
    top_k: 3
    score_threshold: 0.17
    inject_position: "before_examples"   # 目前實作放在 Examples 後（recency bias）
    max_context_tokens: 512
    two_pass: true    # false = 單次推論直接用密碼字串查 RAG
```

---

## 已知限制

| 問題 | 說明 |
|------|------|
| **語意空間錯位** | 密碼字串（如 `john`）與 tag 定義文章的 embedding 空間不同，RAG 分數普遍偏低（0.1–0.2），但相對排序仍有意義 |
| **兩階段誤差放大** | 若第一次推論切錯，第二次 RAG 撈到的定義也會偏錯，但只影響模糊案例，明確段落影響不大 |
| **速度** | 兩階段推論時間約為 Template 1 的兩倍，另加 RAG 查詢開銷 |
| **RAG 為空時** | `rag_context` 為空字串時，`# Reference Definitions` 區塊不出現，行為等同 Template 1 |
