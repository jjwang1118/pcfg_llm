import json
import re


def _try_repair_json(raw: str) -> dict | None:
    """嘗試修復常見 LLM JSON 語法錯誤後解析。回傳 dict 或 None。"""
    # 直接解析
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    # 修復：字串值後直接接下一個鍵（缺逗號），如 "value" "key":
    fixed = re.sub(r'("(?:[^"\\]|\\.)*")(\s+)("(?:[^"\\]|\\.)*"\s*:)', r'\1,\2\3', raw)
    try:
        return json.loads(fixed)
    except json.JSONDecodeError:
        pass
    # 修復：結尾字串未用雙引號閉合，如 "explanation": "some text'}]}
    fixed2 = re.sub(r'("(?:[^"\\]|\\.)*)(}]\})\s*$', r'\1"\2', raw.strip())
    try:
        return json.loads(fixed2)
    except json.JSONDecodeError:
        pass
    return None


def read_jsonl(file_path: str) -> list:
    """讀取 JSONL 檔案，回傳 (password, segments) 列表。
    - 支援 JSON 值中含嵌入換行符的情況（串流解析）
    - 若記錄為 {raw_output, parse_error} 格式，嘗試解析/修復 raw_output
    """
    results = []
    decoder = json.JSONDecoder()
    content = open(file_path, 'r', encoding='utf-8').read()
    pos = 0
    while pos < len(content):
        while pos < len(content) and content[pos] in ' \t\n\r':
            pos += 1
        if pos >= len(content):
            break
        try:
            data, end = decoder.raw_decode(content, pos)
            pos = end
        except json.JSONDecodeError:
            pos += 1
            continue
        if not isinstance(data, dict):
            continue
        # 正常格式
        if 'password' in data and 'segments' in data:
            results.append((data['password'], data['segments']))
            continue
        # raw_output/parse_error 格式：嘗試修復並轉換
        if 'raw_output' in data:
            repaired = _try_repair_json(data['raw_output'])
            if repaired and 'password' in repaired and 'segments' in repaired:
                results.append((repaired['password'], repaired['segments']))
    return results


def calculate_jaccard_distance(set1: set, set2: set) -> float:
    """計算兩個集合的 Jaccard Distance"""
    if len(set1) == 0 and len(set2) == 0:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    similarity = intersection / union
    return 1 - similarity


def cut_position(password: str, segments: list) -> list:
    """從 segments 取得切割位置（不含最後位置）"""
    final = ""
    cut_p = []
    for s in segments:
        final += s['text'].strip()
        cut_p.append(len(final))
    return cut_p[:-1]


def cut_position_with_tags(password: str, segments: list) -> dict:
    """回傳切割位置及對應的 tags，格式: {位置: [tag1, tag2, ...]}"""
    result = {}
    current_pos = 0
    positions = []

    for seg in segments:
        text = seg['text'].strip()
        tag = seg.get('tag', 'X')
        current_pos += len(text)
        positions.append((current_pos, tag))

    if positions:
        positions = positions[:-1]

    for pos, tag in positions:
        if pos not in result:
            result[pos] = []
        result[pos].append(tag)

    return result
