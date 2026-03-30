# LLM 密碼語意標籤識別實驗（簡化版）

> 參考文件：[experiment_design.md](experiment_design.md)

---

## 實驗概述

將原本兩階段的實驗簡化為單一流程，讓模型一次完成切割與語意標註。

### 流程步驟

0. 定義 43 種或更多語意標籤
1. 給予 prompt 讓模型學習 PCFG 切割規則
2. 讓模型切割並判斷語意，生成指定格式輸出
3. 評估模型的切割和語意判斷能力

---

## 1. Prompt 設計

```
你是一個 PCFG 密碼分析模型。請將以下密碼切割成有意義的片段，並為每個片段標註語意標籤。

規則：
- 字母與數字之間需切開
- 特殊符號單獨成段
- 完整單詞/拼音保持不切

輸出格式：原始密碼,<片段1,標籤1><片段2,標籤2>...

範例：
john1990! → john1990!,<john,MALE_NAME><1990,YEAR><!,SPEC>
```

---

## 2. 輸出格式

```
origin_pw,<Semantic_pw,tag><Semantic_pw,tag>...
```

### 範例

| 原始密碼 | 輸出 |
|---------|------|
| john1990! | john1990!,\<john,MALE_NAME\>\<1990,YEAR\>\<!,SPEC\> |
| qwerty123 | qwerty123,\<qwerty,KB\>\<123,NUMBER\> |
| zhangsan888 | zhangsan888,\<zhangsan,PY\>\<888,NUMBER\> |

---

## 3. 評估指標

| 指標 | 說明 |
|------|------|
| 切割準確率 | 切割邊界與 PCFG Ground Truth 的匹配程度 |
| 標籤準確率 | 語意標籤的正確率（Top-1 / Top-K） |
| 格式正確率 | 輸出是否符合指定格式 |
| 邊界 F1 | 切割邊界位置的 Precision / Recall / F1 |

---

## 4. 語意標籤清單（43 種）

### A. 專有名詞與實體類 (6 種)
| 標籤 | 說明 |
|------|------|
| MALE_NAME | 男性名字 |
| FEMALE_NAME | 女性名字 |
| CN_NAME_ABBR | 中文名字縮寫 |
| WKNE | 知名實體 |
| UBE | 未知實體 |
| LOCATION | 地名 |

### B. 日期與數字類 (6 種)
| 標籤 | 說明 |
|------|------|
| YEAR | 年份 (如 1990, 2023) |
| DATE_6 | 6 位日期 (如 900101) |
| DATE_8 | 8 位日期 (如 19900101) |
| MONTH | 月份 |
| CN_MOBILE | 中國手機號 |
| NUMBER | 一般數字 |

### C. 字符串模式與結構類 (10 種)
| 標籤 | 說明 |
|------|------|
| EMAIL | 電子郵件格式 |
| DN | 域名 |
| KB | 鍵盤模式 (如 qwerty, asdf) |
| SR | 字符重複 |
| PRE | 前綴 |
| SUF | 後綴 |
| PY | 拼音 |
| CONSONANTS | 子音串 |
| SPEC | 特殊符號 |
| LEET | Leet 替換 (如 @ → a, 0 → o) |

### D. 語言學詞性類 (21 種)
**英語 (11 種)**
NOUN, VERB, PRON, ADJ, ADV, ADP, CONJ, DET, PRT, NUM, X

**德語 (5 種)**
NOUN_DE, ADJ_DE, ADV_DE, PRON_DE, VERB_DE

**法語 (5 種)**
NOUN_FR, ADJ_FR, ADV_FR, PRON_FR, VERB_FR

---

## 5. 資料來源

- **輸入**：密碼列表
- **Ground Truth**：PCFG 模型的切割結果 + 規則/詞典產生的標籤