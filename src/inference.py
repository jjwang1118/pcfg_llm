import os
import re
import json


def parse_model_output(output_ids, tokenizer, enable_thinking: bool = False):
    """解析模型原始輸出，分離 thinking 和 content"""
    if enable_thinking:
        try:
            think_end_id = tokenizer.convert_tokens_to_ids("</think>")
            index = len(output_ids) - output_ids[::-1].index(think_end_id)
        except ValueError:
            index = 0
        thinking = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
        content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")
    else:
        thinking = ""
        content = tokenizer.decode(output_ids, skip_special_tokens=True).strip()
    return thinking, content


def clean_json_output(content: str) -> str:
    """移除模型輸出中的 Markdown 代碼塊標記，並嘗試抽取 JSON 物件"""
    # 處理所有 code block 標記（```python, ```json, ``` 等）
    content = re.sub(r'^```[a-zA-Z]*\s*', '', content.strip())
    content = re.sub(r'\s*```$', '', content)
    content = content.strip()

    # 嘗試直接解析
    try:
        json.loads(content)
        return content
    except json.JSONDecodeError:
        pass

    # fallback：掃描所有頂層 {} 區塊，逐一嘗試 json.loads，回傳第一個合法的 JSON
    pos = 0
    while pos < len(content):
        start = content.find('{', pos)
        if start == -1:
            break
        depth = 0
        for i, c in enumerate(content[start:], start):
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
            if depth == 0:
                candidate = content[start:i + 1]
                try:
                    json.loads(candidate)
                    return candidate.strip()
                except json.JSONDecodeError:
                    pass
                pos = i + 1
                break
        else:
            break  # 括號不平衡，放棄

    return content


def parse_json_result(content: str) -> dict:
    """將清理後的字串解析為 JSON"""
    content = clean_json_output(content)
    try:
        parsed = json.loads(content)
        if isinstance(parsed, dict):
            return parsed
        return {"raw_output": content, "parse_error": True}
    except json.JSONDecodeError:
        return {"raw_output": content, "parse_error": True}


def analyze_password(password: str, model, tokenizer, prompt_text: str,
                     max_new_tokens: int, temperature: float, top_p: float,
                     repetition_penalty: float = 1.1,
                     enable_thinking: bool = False) -> dict:
    """對單一密碼進行語意分析推論"""
    messages = [{"role": "user", "content": prompt_text}]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=enable_thinking,
    )

    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
    )

    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
    thinking, content = parse_model_output(output_ids, tokenizer, enable_thinking)
    result = parse_json_result(content)

    return {"thinking": thinking, "result": result}


def save_result(result: dict, output_path: str) -> None:
    """將單筆分析結果追加寫入 JSONL 檔案"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "a", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)
        f.write("\n")


def convert_seg7_to_jsonl(input_path: str, output_path: str) -> int:
    """
    將 template 7 的原始輸出 JSONL 轉換為結構化 segmentation JSONL。

    輸入格式（每行）：
      {"raw_output": "john 1990 !", "parse_error": true, "password": "john1990!"}
    輸出格式（每行）：
      {"password": "john1990!", "segments": [{"text": "john"}, {"text": "1990"}, {"text": "!"}]}

    回傳成功轉換的筆數。
    """
    converted = 0
    skipped = 0
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(input_path, encoding="utf-8") as f_in, \
         open(output_path, "w", encoding="utf-8") as f_out:
        for lineno, line in enumerate(f_in, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                print(f"[skip] line {lineno}: JSON parse error")
                skipped += 1
                continue

            password = record.get("password", "")
            raw = record.get("raw_output", "").strip()

            if not raw or not password:
                print(f"[skip] line {lineno}: missing password or raw_output")
                skipped += 1
                continue

            # 取第一行，避免模型多輸出說明文字
            raw = raw.splitlines()[0].strip()
            segments = [{"text": seg} for seg in raw.split() if seg]

            # 驗證：所有 segment 拼起來應等於原始密碼
            reconstructed = "".join(s["text"] for s in segments)
            if reconstructed != password:
                print(f"[warn] line {lineno}: '{password}' != reconstructed '{reconstructed}'")

            result = {"password": password, "segments": segments}
            json.dump(result, f_out, ensure_ascii=False)
            f_out.write("\n")
            converted += 1

    print(f"完成：{converted} 筆轉換，{skipped} 筆跳過 → {output_path}")
    return converted
