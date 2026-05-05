# Template 5 — 開放+X強制代價+失敗範例版

> 在 Template 4 基礎上加入對比性失敗範例

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
        1. Prioritize semantic meaning over rigid categorization
        2. Segment the password into its constituent parts based on semantic or structural significance
        3. Assign the most appropriate tag from the available categories
        4. Recognize words from various languages (tags include English, German, French or other)
        5. Identify structural patterns including but not limited to: keyboard sequences, pinyin, leet speak, repetitions
        6. Exhaust all options in steps 1–5 before using "X". Only if a segment truly cannot be classified after thorough analysis should "X" be used as a last resort
        7. When using "X", provide "suggested_tag" and "explanation" — describe which tags you considered and why none of them fit

        # Output Format Requirements
        - Standard tags: {"text": "...", "tag": "TAG_NAME"}
        - X tags (MUST include suggested_tag and explanation): 
          {"text": "...", "tag": "X", "suggested_tag": "NEW_TAG_NAME", "explanation": "tags considered and why none fit"}
        - Do NOT add extra fields to standard tags (only X tags can have "suggested_tag" and "explanation")
        - Output only the JSON object with "password" and "segments" fields

        # Counter-examples (Common Mistakes to Avoid)
        These show incorrect tagging and the correct alternative:

        Input: "password"
        WRONG:   {"text": "password", "tag": "LEET"}  ← No character substitution, this is plain English
        CORRECT: {"text": "password", "tag": "ENGLISH_NOUN"}

        Input: "p@ssw0rd"
        WRONG:   {"text": "p@ssw0rd", "tag": "ENGLISH_NOUN"}  ← Character substitution (@ for a, 0 for o) makes this LEET
        CORRECT: {"text": "p@ssw0rd", "tag": "LEET"}

        Input: "abc123"
        WRONG:   {"text": "abc", "tag": "X", "suggested_tag": "UNKNOWN_CHARS", "explanation": "Unrecognized"}  ← Do not use X for patterns that fit existing tags
        CORRECT: {"text": "abc", "tag": "KB"}  ← Sequential alphabetic keyboard pattern

        # Examples
        Input: "john1990!"
        Output: {"password": "john1990!", "segments": [{"text": "john", "tag": "MALE_NAME"}, {"text": "1990", "tag": "YEAR"}, {"text": "!", "tag": "SPEC"}]}

        Input: "iloveyou"
        Output: {"password": "iloveyou", "segments": [{"text": "i", "tag": "ENGLISH_PRON"}, {"text": "love", "tag": "ENGLISH_VERB"}, {"text": "you", "tag": "ENGLISH_PRON"}]}

        Input: "qwerty123"
        Output: {"password": "qwerty123", "segments": [{"text": "qwerty", "tag": "KB"}, {"text": "123", "tag": "NUMBER"}]}

        Input: "marco99xyz"
        Output: {"password": "marco99xyz", "segments": [{"text": "marco", "tag": "MALE_NAME"}, {"text": "99", "tag": "NUMBER"}, {"text": "xyz", "tag": "X", "suggested_tag": "SUFFIX_PATTERN", "explanation": "Considered KB, LEET, NUMBER — none fit; appears to be a generic alphabetic suffix"}]}

        Input: "belingaro123"
        Output: {"password": "belingaro123", "segments": [{"text": "belingaro", "tag": "X", "suggested_tag": "ITALIAN_SURNAME", "explanation": "Considered MALE_NAME, FEMALE_NAME, ENGLISH_NOUN — none fit; pattern resembles an Italian surname"}, {"text": "123", "tag": "NUMBER"}]}

        Input: "li1980ming"
        Output: {"password": "li1980ming", "segments": [{"text": "li", "tag": "X", "suggested_tag": "CHINESE_SURNAME", "explanation": "Considered MALE_NAME, ENGLISH_PRON — too short and ambiguous; common Chinese surname"}, {"text": "1980", "tag": "YEAR"}, {"text": "ming", "tag": "X", "suggested_tag": "CHINESE_GIVEN_NAME", "explanation": "Considered MALE_NAME, ENGLISH_VERB — does not match; common Chinese given name"}]}

        # Task
        Analyze the following password and output ONLY the raw JSON object.
        Do NOT write any code. Do NOT use markdown. Do NOT add any explanation.
        The response MUST start with { and end with }.
        Remember: Use "X" only as a last resort after exhausting steps 1–5. X tags MUST include both "suggested_tag" and "explanation" fields.

        Password: john1990!
        
```
