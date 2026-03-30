import json


def read_jsonl(file_path: str) -> list:
    """讀取 JSONL 檔案，回傳 (password, segments) 列表"""
    results = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                results.append((data['password'], data['segments']))
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
