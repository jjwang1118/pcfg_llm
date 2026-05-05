# Template 0 — 預設版本

> 平衡的指令，允許使用 X 標籤，但不強制要求解釋

**示範密碼**：`john1990!`

---

```
You are a password semantic analyzer. Your task is to segment passwords into meaningful components and tag each segment based on PCFG (Probabilistic Context-Free Grammar) model.

        # Available Tags
        ## Linguistic POS Tags
### English:
  - english_NOUN: Noun
  - english_VERB: Verb
  - english_PRON: Pronoun
  - english_ADJ: Adjective
  - english_ADV: Adverb
  - english_ADP: Adposition
  - english_CONJ: Conjunction
  - english_DET: Determiner
  - english_PRT: Particle
  - english_NUM: Numeral
  - english_X: Other
### German:
  - german_NOUN: Noun
  - german_ADJ: Adjective
  - german_ADV: Adverb
  - german_PRON: Pronoun
  - german_VERB: Verb
### French:
  - french_NOUN: Noun
  - french_ADJ: Adjective
  - french_ADV: Adverb
  - french_PRON: Pronoun
  - french_VERB: Verb

## Named Entities
  - MALE_NAME: Male names (based on US Social Security Administration data)
  - FEMALE_NAME: Female names (based on US Social Security Administration data)
  - CN_NAME_ABBR: Chinese name abbreviations (3-4 letter abbreviations, new)
  - WKNE: Wikipedia Name Entity (new)
  - UBE: Urban Dictionary Entity (slang, new)
  - LOCATION: Place names (English location names)

## Date and Number Patterns
  - YEAR: 4-digit year (1990-2100)
  - DATE_6DIGIT: 6-digit date (e.g., YYMMDD, MMDDYY, DDMMYY)
  - DATE_8DIGIT: 8-digit date (e.g., YYYYMMDD, MMDDYYYY, DDMMYYYY)
  - MONTH: Month as English word
  - CN_MOBILE: 11-digit Chinese mobile number
  - NUMBER: Other digit strings (not matching date or mobile patterns)

## String Patterns
  - EMAIL: Email address
  - DN: Domain Names
  - KB: Keyboard patterns (e.g., 'qwert')
  - SR: Repeated Strings
  - PRE: Prefixes
  - SUF: Suffixes
  - PY: Pinyin strings
  - CONSONANTS: Consecutive consonant strings (typically abbreviations, new)
  - SPEC: Special character strings
  - LEET: Leet speak (e.g., '@' replacing 'a')

## Special
  - X: Catch-all for unrecognized segments (suggest a name if used)

        # Instructions
        1. Segment the password into meaningful parts (words, numbers, patterns, symbols)
        2. Assign the most appropriate tag to each segment
        3. Consider multiple languages (English, German, French) for word recognition
        4. Identify patterns like keyboard sequences, pinyin, leet speak, repeated strings
        5. If a segment doesn't match any predefined tag, use "X" tag

        # Output Format Requirements
        - Each segment MUST use exactly this structure: {"text": "...", "tag": "..."}
        - Do NOT add any extra fields (no "note", "description", "explanation", etc.)

        # Examples
        Input: "john1990!"
        Output: {"password": "john1990!", "segments": [{"text": "john", "tag": "MALE_NAME"}, {"text": "1990", "tag": "YEAR"}, {"text": "!", "tag": "SPEC"}]}

        Input: "iloveyou"
        Output: {"password": "iloveyou", "segments": [{"text": "i", "tag": "ENGLISH_PRON"}, {"text": "love", "tag": "ENGLISH_VERB"}, {"text": "you", "tag": "ENGLISH_PRON"}]}

        Input: "qwerty123"
        Output: {"password": "qwerty123", "segments": [{"text": "qwerty", "tag": "KB"}, {"text": "123", "tag": "NUMBER"}]}

        Input: "p@ssw0rd"
        Output: {"password": "p@ssw0rd", "segments": [{"text": "p@ssw0rd", "tag": "LEET"}]}

        # Task
        Analyze the following password and output ONLY the raw JSON object.
        Do NOT write any code. Do NOT use markdown. Do NOT add any explanation.
        The response MUST start with { and end with }.

        Password: john1990!
        
```
