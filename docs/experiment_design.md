# LLM 密碼語意標籤識別實驗

## 實驗目標

測試 LLM 是否能識別論文中定義的 46 種語意標籤

---

## 實驗流程

實驗分為兩個階段：

1. **階段 1：切割密碼** - 將密碼切成有意義的片段
2. **階段 2：語意分析** - 為每個片段產生候選語意標籤

---

## 階段 1：切割密碼

### 目標

將密碼切割成有意義的片段，並與 PCFG 模型的切割結果進行比較。

### 切割原則

1. 字母與數字之間切開
2. 特殊符號單獨成段
3. 完整單詞保持不切
4. 拼音、縮寫保持完整

### 範例

| 密碼 | 切割結果 |
|------|---------|
| john1990love! | john, 1990, love, ! |
| qwerty123 | qwerty, 123 |
| zhangsan888 | zhangsan, 888 |
| p@ssw0rd | p@ssw0rd |

### LLM vs PCFG 比較

使用現有 PCFG 模型（如論文中的模型或 PCFG Cracker）的切割結果作為 Ground Truth，比較 LLM 的切割能力。

**評估指標：**

| 指標 | 說明 |
|------|------|
| 完全匹配率 | LLM 切割與 PCFG 切割完全相同的比例 |
| 邊界 F1 | 切割邊界位置的 Precision / Recall / F1 |
| 片段 IoU | 預測片段與真實片段的交集/聯集比例 |

---

## 階段 2：語意分析

### 目標

對每個片段，產生可能的語意標籤候選（附帶機率/信心分數）。

### 方案 A：開放式標籤

讓 LLM 自行判斷每個片段的語意類別，不限制標籤範圍。模型可自由產生如「男性名字」、「年份」、「數字」等標籤。

### 方案 B：給定標籤配對

提供 46 種標籤定義，讓 LLM 從中選擇最適合的標籤。這種方式可控制標籤範圍，便於與論文結果比較。

### 取得標籤機率的方法

1. **Logprobs 方法（推薦）**：使用 API 的 logprobs 功能取得模型輸出每個 token 的真實機率。

2. **多次採樣方法**：對同一片段多次詢問，統計各標籤出現的頻率作為機率估計。

---

## Loss 函數設計

### 總 Loss 公式

$$\mathcal{L}_{total} = \alpha \cdot \mathcal{L}_{seg} + \beta \cdot \mathcal{L}_{sem}$$

其中：
- $\alpha$：切割任務的權重係數
- $\beta$：語意分析任務的權重係數
- $\mathcal{L}_{seg}$：階段 1 切割 Loss
- $\mathcal{L}_{sem}$：階段 2 語意 Loss

---

### 階段 1：切割 Loss

使用 **KL Divergence** 衡量 LLM 預測的切割分布與 PCFG Ground Truth 之間的差異：

$$\mathcal{L}_{seg} = D_{KL}(P_{LLM} \| P_{PCFG})$$

其中：
- $P_{LLM}$：LLM 預測的切割邊界機率分布
- $P_{PCFG}$：PCFG 模型的切割邊界分布（作為 Ground Truth）

KL Divergence 可以衡量兩個機率分布的差異程度，當 LLM 的切割越接近 PCFG 時，Loss 越小。

---

### 階段 2：語意 Loss

使用 **Cross Entropy Loss** 衡量 LLM 預測的標籤與目標標籤之間的差異：

$$\mathcal{L}_{sem} = -\sum_{i} y_i \log(\hat{y}_i)$$

其中：
- $y_i$：目標標籤的機率分布（由規則/詞典產生的軟標籤）
- $\hat{y}_i$：LLM 預測的標籤機率分布

由於缺乏語意標籤的 Ground Truth，可採用以下方式產生目標標籤：
1. **規則判斷**：如數字長度、年份範圍等
2. **詞典匹配**：如名字詞典、地名詞典等
3. **正則表達式**：如 EMAIL、日期格式等

---

### Loss 函數總結

| 階段 | Loss 類型 | 監督信號來源 |
|------|----------|-------------|
| 階段 1：切割 | KL Divergence × α | PCFG 模型切割結果 |
| 階段 2：語意 | Cross Entropy × β | 規則/詞典產生的軟標籤 |

---

## 評估指標

| 指標 | 說明 |
|------|------|
| 分段準確率 | 切割邊界是否正確（與 PCFG 比較）|
| Top-1 準確率 | 最高信心標籤的正確率 |
| Top-K 準確率 | 正確標籤在前 K 個候選中的比例 |
| 標籤覆蓋率 | LLM 產生的標籤與 46 種標籤的重合度 |

---

## 參考標籤體系 (46種)

### A. 語言學詞性類 (21 種)
- 英語：NOUN, VERB, PRON, ADJ, ADV, ADP, CONJ, DET, PRT, NUM, X
- 德語：NOUN, ADJ, ADV, PRON, VERB
- 法語：NOUN, ADJ, ADV, PRON, VERB

### B. 專有名詞與實體類 (6 種)
MALE NAME, FEMALE NAME, CN NAME ABBR, WKNE, UBE, LOCATION

### C. 日期與數字類 (6 種)
YEAR, DATE(6-digit), DATE(8-digit), MONTH, CN MOBILE, NUMBER

### D. 字符串模式與結構類 (10 種)
EMAIL, DN, KB, SR, PRE, SUF, PY, CONSONANTS, SPEC, LEET
