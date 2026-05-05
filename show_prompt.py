import os
from src.prompt import prompt_template, prompt_explain_unknown_tags

EXAMPLE_PASSWORD = "john1990!"

TEMPLATES = [
    (0, "預設版本", "平衡的指令，允許使用 X 標籤，但不強制要求解釋", 0),
    (1, "開放探索版", "鼓勵探索新模式，X 標籤需要解釋", 0),
    (2, "嚴格限制版", "只使用現有標籤，避免創建新標籤", 1),
    (3, "極簡版", "最少指令，直接輸出", 0),
    (4, "開放+X強制代價版", "語意優先，X 標籤須窮舉後才可使用，需說明排除原因", 0),
    (5, "開放+X強制代價+失敗範例版", "在 Template 4 基礎上加入對比性失敗範例", 0),
]


def show_template_summary():
    """顯示模板選項摘要"""
    print("=" * 80)
    print("PROMPT 模板參數說明")
    print("=" * 80)
    print("\n【prompt_template 參數】控制指令風格：")
    for tid, name, desc, _ in TEMPLATES:
        print(f"  {tid} = {name} - {desc}")

    print("\n【tag_summary 參數】控制標籤說明：")
    print("  0 = 完整標籤列表 + 允許 X 標籤")
    print("  1 = 完整標籤列表 + 禁止創建新標籤")

    print("\n【推薦組合】：")
    print("  • 探索新模式：  prompt_template(pwd, tag_summary=0, prompt_template=1)")
    print("  • 嚴格標註：    prompt_template(pwd, tag_summary=1, prompt_template=2)")
    print("  • 快速測試：    prompt_template(pwd, tag_summary=0, prompt_template=3)")
    print("  • 低X率探索：   prompt_template(pwd, tag_summary=0, prompt_template=4)")
    print("  • 含對比示範：  prompt_template(pwd, tag_summary=0, prompt_template=5)")
    print("=" * 80)
    print()


def show_prompt_templates():
    """顯示所有可用的 PROMPT 模板"""
    for tid, name, desc, tag_sum in TEMPLATES:
        print("\n" + "=" * 80)
        print(f"Template {tid} — {name}")
        print(f"  > {desc}")
        print("=" * 80)
        print(prompt_template(EXAMPLE_PASSWORD, tag_summary=tag_sum, prompt_template=tid))

    print("\n" + "=" * 80)
    print("未知標籤解釋模板 (prompt_explain_unknown_tags)")
    print("=" * 80)
    example_segments = [
        {"text": "mn", "tag": "INITIALS", "password": "306187mn"},
        {"text": "abc", "tag": "X", "password": "abc123"},
    ]
    print(prompt_explain_unknown_tags(example_segments))


def save_all_templates(output_dir: str = "docs"):
    """將每個模板的輸出儲存至 docs/template_{id}.md"""
    os.makedirs(output_dir, exist_ok=True)
    for tid, name, desc, tag_sum in TEMPLATES:
        content = prompt_template(EXAMPLE_PASSWORD, tag_summary=tag_sum, prompt_template=tid)
        filepath = os.path.join(output_dir, f"template_{tid}.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Template {tid} — {name}\n\n")
            f.write(f"> {desc}\n\n")
            f.write(f"**示範密碼**：`{EXAMPLE_PASSWORD}`\n\n")
            f.write("---\n\n")
            f.write("```\n")
            f.write(content)
            f.write("\n```\n")
        print(f"已儲存：{filepath}")


if __name__ == "__main__":
    show_template_summary()
    show_prompt_templates()
    print("\n" + "=" * 80)
    print("儲存各模板至 docs/template_{id}.md ...")
    print("=" * 80)
    save_all_templates()
