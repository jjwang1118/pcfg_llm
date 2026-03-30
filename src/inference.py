import os
import re
import json


def parse_model_output(output_ids, tokenizer, enable_thinking: bool = False):
    """解析模型原始輸出，分離 thinking 和 content"""
    if enable_thinking:
        try:
            # 找到 </think> token (151668)
            index = len(output_ids) - output_ids[::-1].index(151668)
        except ValueError:
            index = 0
        thinking = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
        content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")
    else:
        thinking = ""
        content = tokenizer.decode(output_ids, skip_special_tokens=True).strip()
    return thinking, content


def clean_json_output(content: str) -> str:
    """移除模型輸出中的 Markdown 代碼塊標記"""
    content = re.sub(r'^```json\s*', '', content)
    content = re.sub(r'^```\s*', '', content)
    content = re.sub(r'\s*```$', '', content)
    return content.strip()


def parse_json_result(content: str) -> dict:
    """將清理後的字串解析為 JSON"""
    content = clean_json_output(content)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"raw_output": content, "parse_error": True}


def analyze_password(password: str, model, tokenizer, prompt_text: str,
                     max_new_tokens: int, temperature: float, top_p: float,
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
