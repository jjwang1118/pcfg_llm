from zxcvbn import zxcvbn

def zxcvbn_to_segments(password: str) -> list:
    result = zxcvbn(password)
    segments = []
    cursor = 0
    for match in result["sequence"]:
        # 補上 sequence 沒有覆蓋到的空隙
        if match["i"] > cursor:
            segments.append({"text": password[cursor:match["i"]], "tag": "X"})
        segments.append({"text": match["token"], "tag": match["pattern"].upper()})
        cursor = match["j"] + 1
    # 補上尾端空隙
    if cursor < len(password):
        segments.append({"text": password[cursor:], "tag": "X"})
    return segments
