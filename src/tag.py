
def password_tag():

    return {
        "linguistic_pos_tags": {
            "description": "Part-of-speech tags using NLP techniques",
            "total": 21,
            "english": {
                "count": 11,
                "tags": ["NOUN", "VERB", "PRON", "ADJ", "ADV", "ADP", "CONJ", "DET", "PRT", "NUM", "X"],
                "descriptions": {
                    "NOUN": "Noun",
                    "VERB": "Verb",
                    "PRON": "Pronoun",
                    "ADJ": "Adjective",
                    "ADV": "Adverb",
                    "ADP": "Adposition",
                    "CONJ": "Conjunction",
                    "DET": "Determiner",
                    "PRT": "Particle",
                    "NUM": "Numeral",
                    "X": "Other"
                }
            },
            "german": {
                "count": 5,
                "tags": ["NOUN", "ADJ", "ADV", "PRON", "VERB"],
                "new": True,
                "descriptions": {
                    "NOUN": "Noun",
                    "ADJ": "Adjective",
                    "ADV": "Adverb",
                    "PRON": "Pronoun",
                    "VERB": "Verb",
                    "X": "Other"
                }
            },
            "french": {
                "count": 5,
                "tags": ["NOUN", "ADJ", "ADV", "PRON", "VERB"],
                "new": True,
                "descriptions": {
                    "NOUN": "Noun",
                    "ADJ": "Adjective",
                    "ADV": "Adverb",
                    "PRON": "Pronoun",
                    "VERB": "Verb",
                    "X": "Other"
                }
            }
        },
        "proper_nouns_entities": {
            "description": "Proper nouns and named entities",
            "total": 6,
            "tags": {
                "MALE_NAME": "Male names (based on US Social Security Administration data)",
                "FEMALE_NAME": "Female names (based on US Social Security Administration data)",
                "CN_NAME_ABBR": "Chinese name abbreviations (3-4 letter abbreviations, new)",
                "WKNE": "Wikipedia Name Entity (new)",
                "UBE": "Urban Dictionary Entity (slang, new)",
                "LOCATION": "Place names (English location names)"
            }
        },
        "date_and_number": {
            "description": "Date and numeric patterns",
            "total": 6,
            "tags": {
                "YEAR": "4-digit year (1990-2100)",
                "DATE_6DIGIT": "6-digit date (e.g., YYMMDD, MMDDYY, DDMMYY)",
                "DATE_8DIGIT": "8-digit date (e.g., YYYYMMDD, MMDDYYYY, DDMMYYYY)",
                "MONTH": "Month as English word",
                "CN_MOBILE": "11-digit Chinese mobile number",
                "NUMBER": "Other digit strings (not matching date or mobile patterns)"
            }
        },
        "string_patterns_structure": {
            "description": "String patterns and structural elements",
            "total": 10,
            "tags": {
                "EMAIL": "Email address",
                "DN": "Domain Names",
                "KB": "Keyboard patterns (e.g., 'qwert')",
                "SR": "Repeated Strings",
                "PRE": "Prefixes",
                "SUF": "Suffixes",
                "PY": "Pinyin strings",
                "CONSONANTS": "Consecutive consonant strings (typically abbreviations, new)",
                "SPEC": "Special character strings",
                "LEET": "Leet speak (e.g., '@' replacing 'a')"
            }
        }
    }


def get_all_valid_tags() -> set:
    """獲取所有合法的標籤名稱"""
    tag = password_tag()
    valid_tags = set()
    
    # Linguistic POS tags (帶語言前綴: ENGLISH_VERB, GERMAN_NOUN, etc.)
    pos = tag["linguistic_pos_tags"]
    for lang in ["english", "german", "french"]:
        if lang in pos:
            lang_prefix = lang.upper()
            for t in pos[lang]["tags"]:
                valid_tags.add(f"{lang_prefix}_{t}")  # e.g., ENGLISH_VERB
    valid_tags.add("X")  # 確保 X 也在裡面
    
    # Other categories
    for category in ["proper_nouns_entities", "date_and_number", "string_patterns_structure"]:
        if "tags" in tag[category]:
            valid_tags.update(tag[category]["tags"].keys())
    
    return valid_tags