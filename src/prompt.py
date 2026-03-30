from src.tag import password_tag


def tag_description(a :int=0):
    """Generate tag descriptions for prompt."""
    tag = password_tag()
    lines = []
    if (a==0):
        # 1. Linguistic POS Tags
        pos = tag["linguistic_pos_tags"]
        lines.append("## Linguistic POS Tags")
        for lang in ["english", "german", "french"]:
            if lang not in pos:
                continue
            lines.append(f"### {lang.capitalize()}:")
            lang_prefix = lang
            for t in pos[lang]["tags"]:
                desc = pos[lang].get("descriptions", {}).get(t, t)
                lines.append(f"  - {lang_prefix}_{t}: {desc}")

        # 2. Named Entities
        lines.append("\n## Named Entities")
        for t, desc in tag["proper_nouns_entities"]["tags"].items():
            lines.append(f"  - {t}: {desc}")

        # 3. Date & Number
        lines.append("\n## Date and Number Patterns")
        for t, desc in tag["date_and_number"]["tags"].items():
            lines.append(f"  - {t}: {desc}")

        # 4. String Patterns
        lines.append("\n## String Patterns")
        for t, desc in tag["string_patterns_structure"]["tags"].items():
            lines.append(f"  - {t}: {desc}")

        # 5. Special
        lines.append("\n## Special")
        lines.append("  - X: Catch-all for unrecognized segments (suggest a name if used)")

        return "\n".join(lines)
    elif (a==1):
        # 1. Linguistic POS Tags
        pos = tag["linguistic_pos_tags"]
        lines.append("## Linguistic POS Tags")
        for lang in ["english", "german", "french"]:
            if lang not in pos:
                continue
            lines.append(f"### {lang.capitalize()}:")
            lang_prefix = lang
            for t in pos[lang]["tags"]:
                desc = pos[lang].get("descriptions", {}).get(t, t)
                lines.append(f"  - {lang_prefix}_{t}: {desc}")

        # 2. Named Entities
        lines.append("\n## Named Entities")
        for t, desc in tag["proper_nouns_entities"]["tags"].items():
            lines.append(f"  - {t}: {desc}")

        # 3. Date & Number
        lines.append("\n## Date and Number Patterns")
        for t, desc in tag["date_and_number"]["tags"].items():
            lines.append(f"  - {t}: {desc}")

        # 4. String Patterns
        lines.append("\n## String Patterns")
        for t, desc in tag["string_patterns_structure"]["tags"].items():
            lines.append(f"  - {t}: {desc}")

        # 5. Special
        #lines.append("\n## Special")
        lines.append("\n## Important: You must choose from the existing tags above. Do not create new tags.")
        
        return "\n".join(lines)


def prompt_template(password: str,tag_summary:int=0,prompt_template:int=1) -> str:

    if prompt_template == 0:
        prompt = f"""You are a password semantic analyzer. Your task is to segment passwords into meaningful components and tag each segment based on PCFG (Probabilistic Context-Free Grammar) model.

        # Available Tags
        {tag_description(tag_summary)}

        # Instructions
        1. Segment the password into meaningful parts (words, numbers, patterns, symbols)
        2. Assign the most appropriate tag to each segment
        3. Consider multiple languages (English, German, French) for word recognition
        4. Identify patterns like keyboard sequences, pinyin, leet speak, repeated strings
        5. If a segment doesn't match any predefined tag, use "X" tag

        # Output Format Requirements
        - Each segment MUST use exactly this structure: {{"text": "...", "tag": "..."}}
        - Do NOT add any extra fields (no "note", "description", "explanation", etc.)

        # Examples
        Input: "john1990!"
        Output: {{"password": "john1990!", "segments": [{{"text": "john", "tag": "MALE_NAME"}}, {{"text": "1990", "tag": "YEAR"}}, {{"text": "!", "tag": "SPEC"}}]}}

        Input: "iloveyou"
        Output: {{"password": "iloveyou", "segments": [{{"text": "i", "tag": "ENGLISH_PRON"}}, {{"text": "love", "tag": "ENGLISH_VERB"}}, {{"text": "you", "tag": "ENGLISH_PRON"}}]}}

        Input: "qwerty123"
        Output: {{"password": "qwerty123", "segments": [{{"text": "qwerty", "tag": "KB"}}, {{"text": "123", "tag": "NUMBER"}}]}}

        Input: "p@ssw0rd"
        Output: {{"password": "p@ssw0rd", "segments": [{{"text": "p@ssw0rd", "tag": "LEET"}}]}}

        # Task
        Analyze the following password and output ONLY the raw JSON object.
        Do NOT write any code. Do NOT use markdown. Do NOT add any explanation.
        The response MUST start with {{ and end with }}.

        Password: {password}
        """
        return prompt
    
    elif prompt_template == 1:
        # 開放版本 - 鼓勵探索新模式，X標籤需要解釋
        prompt = f"""You are a password semantic analyzer. Your task is to segment passwords into meaningful components and tag each segment based on PCFG (Probabilistic Context-Free Grammar) model.

        # Available Tags
        {tag_description(tag_summary)}

        # Instructions
        1. Segment the password into its constituent parts based on semantic or structural significance
        2. Assign the most appropriate tag from the available categories
        3. Recognize words from various languages (tags include English, German, French or other)
        4. Identify structural patterns including but not limited to: keyboard sequences, pinyin, leet speak, repetitions
        5. For unrecognized patterns, use "X" tag and provide a "note" field with suggested tag name or explanation
        6. Prioritize semantic meaning over rigid categorization

        # Output Format Requirements
        - Standard tags: {{"text": "...", "tag": "TAG_NAME"}}
        - X tags (MUST include suggested_tag and explanation): 
          {{"text": "...", "tag": "X", "suggested_tag": "NEW_TAG_NAME", "explanation": "why this pattern/what it represents"}}
        - Do NOT add extra fields to standard tags (only X tags can have "suggested_tag" and "explanation")
        - Output only the JSON object with "password" and "segments" fields

        # Examples
        Input: "john1990!"
        Output: {{"password": "john1990!", "segments": [{{"text": "john", "tag": "MALE_NAME"}}, {{"text": "1990", "tag": "YEAR"}}, {{"text": "!", "tag": "SPEC"}}]}}

        Input: "iloveyou"
        Output: {{"password": "iloveyou", "segments": [{{"text": "i", "tag": "ENGLISH_PRON"}}, {{"text": "love", "tag": "ENGLISH_VERB"}}, {{"text": "you", "tag": "ENGLISH_PRON"}}]}}

        Input: "qwerty123"
        Output: {{"password": "qwerty123", "segments": [{{"text": "qwerty", "tag": "KB"}}, {{"text": "123", "tag": "NUMBER"}}]}}

        Input: "marco99xyz"
        Output: {{"password": "marco99xyz", "segments": [{{"text": "marco", "tag": "MALE_NAME"}}, {{"text": "99", "tag": "NUMBER"}}, {{"text": "xyz", "tag": "X", "suggested_tag": "SUFFIX_PATTERN", "explanation": "Common 3-letter suffix pattern"}}]}}

        Input: "belingaro123"
        Output: {{"password": "belingaro123", "segments": [{{"text": "belingaro", "tag": "X", "suggested_tag": "ITALIAN_SURNAME", "explanation": "Appears to be an Italian surname pattern"}}, {{"text": "123", "tag": "NUMBER"}}]}}

        Input: "li1980ming"
        Output: {{"password": "li1980ming", "segments": [{{"text": "li", "tag": "X", "suggested_tag": "CHINESE_SURNAME", "explanation": "Common Chinese surname"}}, {{"text": "1980", "tag": "YEAR"}}, {{"text": "ming", "tag": "X", "suggested_tag": "CHINESE_GIVEN_NAME", "explanation": "Common Chinese given name"}}]}}

        # Task
        Analyze the following password and output ONLY the raw JSON object.
        Do NOT write any code. Do NOT use markdown. Do NOT add any explanation.
        The response MUST start with {{ and end with }}.
        Remember: X tags MUST include both "suggested_tag" and "explanation" fields.

        Password: {password}
        """
        return prompt
    
    elif prompt_template == 2:
        # 嚴格版本 - 只使用現有標籤
        prompt = f"""You are a password semantic analyzer. Your task is to segment passwords into meaningful components and tag each segment based on PCFG (Probabilistic Context-Free Grammar) model.

        # Available Tags
        {tag_description(1)}

        # Instructions
        1. Segment the password into meaningful parts
        2. Each segment MUST use one of the predefined tags listed above
        3. If a segment doesn't clearly match any tag, break it down further or group it with adjacent segments
        4. Avoid using "X" tag unless absolutely necessary

        # Output Format Requirements
        - Each segment MUST use exactly this structure: {{"text": "...", "tag": "..."}}
        - Do NOT add any extra fields (no "note", "description", "explanation", etc.)

        # Examples
        Input: "john1990!"
        Output: {{"password": "john1990!", "segments": [{{"text": "john", "tag": "MALE_NAME"}}, {{"text": "1990", "tag": "YEAR"}}, {{"text": "!", "tag": "SPEC"}}]}}

        Input: "iloveyou"
        Output: {{"password": "iloveyou", "segments": [{{"text": "i", "tag": "ENGLISH_PRON"}}, {{"text": "love", "tag": "ENGLISH_VERB"}}, {{"text": "you", "tag": "ENGLISH_PRON"}}]}}

        # Task
        Analyze the following password and output ONLY the raw JSON object.
        Do NOT write any code. Do NOT use markdown. Do NOT add any explanation.
        The response MUST start with {{ and end with }}.

        Password: {password}
        """
        return prompt
    
    elif prompt_template == 3:
        # 簡化版本 - 最少指令
        prompt = f"""Segment the password into meaningful parts and tag each segment.

# Tags
{tag_description(tag_summary)}

# Output Format
{{"password": "{password}", "segments": [{{"text": "...", "tag": "..."}}]}}

Do NOT write any code. Do NOT use markdown. Output ONLY the raw JSON object starting with {{ and ending with }}.

Password: {password}
"""
        return prompt
    
    else:
        # 預設使用 template 0
        return prompt_template(password, tag_summary, 0)


def prompt_template_batch(passwords: list) -> str:
    """
    Generate prompt for batch password analysis.
    
    Args:
        passwords: List of passwords to analyze
    
    Returns:
        Complete prompt string
    """
    pwd_list = "\n".join([f"  {i+1}. {p}" for i, p in enumerate(passwords)])
    
    prompt = f"""You are a password semantic analyzer. Segment each password and tag the components.

# Available Tags
{tag_description(0)}

# Output Format Requirements
- Return a JSON array with analysis for each password
- Each segment MUST use exactly: {{"text": "...", "tag": "..."}}
- Do NOT add extra fields like "note", "description", or "explanation"
- Structure: [{{"password": "...", "segments": [{{"text": "...", "tag": "..."}}]}}]

# Passwords to Analyze
{pwd_list}

Do NOT write any code. Do NOT use markdown. Output ONLY the raw JSON array starting with [ and ending with ].
"""
    return prompt


def prompt_explain_unknown_tags(segments: list) -> str:
    """
    Generate prompt to explain unknown tags and suggest whether they should be added.
    
    Args:
        segments: List of segments with undefined tags, e.g., 
                  [{"text": "mn", "tag": "INITIALS", "password": "306187mn"}, ...]
    
    Returns:
        Prompt string
    """
    # 不在這裡限制數量，由調用方控制批次大小
    examples = "\n".join([f"  - \"{s['text']}\" tagged as \"{s.get('tag', 'X')}\" (from password: {s['password']})" for s in segments])
    
    prompt = f"""You are a password pattern analyst. Analyze the following password segments that were tagged with undefined categories.

# Known Tag Categories
{tag_description(0)}

# Segments with Undefined Tags
{examples}

# Task
For each segment and its assigned tag:
1. Is the tag name meaningful and appropriate?
2. Does this pattern warrant a new tag category?
3. Should it be merged with an existing tag?

# Output Format (JSON)
{{
    "analysis": [
        {{
            "text": "segment_text",
            "original_tag": "the tag model assigned",
            "password": "original_password",
            "likely_meaning": "explanation of what this might represent",
            "recommendation": "ADD_NEW_TAG | MERGE_WITH_EXISTING | KEEP_AS_X",
            "merge_with": "existing tag name if merging, else null",
            "suggested_tag": {{
                "name": "NEW_TAG_NAME",
                "description": "Description of the new tag"
            }}
        }}
    ],
    "new_tags_summary": [
        {{
            "name": "TAG_NAME",
            "description": "Description",
            "examples": ["example1", "example2"]
        }}
    ]
}}

Output ONLY valid JSON:
"""
    return prompt


