# Template 3 — 極簡版

> 最少指令，直接輸出

**示範密碼**：`john1990!`

---

```
Segment the password into meaningful parts and tag each segment.

# Tags
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

# Output Format
{"password": "john1990!", "segments": [{"text": "...", "tag": "..."}]}

Do NOT write any code. Do NOT use markdown. Output ONLY the raw JSON object starting with { and ending with }.

Password: john1990!

```
