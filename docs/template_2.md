# Template 2 — 嚴格限制版

> 只使用現有標籤，避免創建新標籤

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

## Important: You must choose from the existing tags above. Do not create new tags.

        # Instructions
        1. Segment the password into meaningful parts
        2. Each segment MUST use one of the predefined tags listed above
        3. If a segment doesn't clearly match any tag, break it down further or group it with adjacent segments
        4. Avoid using "X" tag unless absolutely necessary

        # Output Format Requirements
        - Each segment MUST use exactly this structure: {"text": "...", "tag": "..."}
        - Do NOT add any extra fields (no "note", "description", "explanation", etc.)

        # Examples
        Input: "john1990!"
        Output: {"password": "john1990!", "segments": [{"text": "john", "tag": "MALE_NAME"}, {"text": "1990", "tag": "YEAR"}, {"text": "!", "tag": "SPEC"}]}

        Input: "iloveyou"
        Output: {"password": "iloveyou", "segments": [{"text": "i", "tag": "ENGLISH_PRON"}, {"text": "love", "tag": "ENGLISH_VERB"}, {"text": "you", "tag": "ENGLISH_PRON"}]}

        # Task
        Analyze the following password and output ONLY the raw JSON object.
        Do NOT write any code. Do NOT use markdown. Do NOT add any explanation.
        The response MUST start with { and end with }.

        Password: john1990!
        
```
