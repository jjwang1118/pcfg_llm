from src.prompt import prompt_template, prompt_template_batch, prompt_explain_unknown_tags


def show_template_summary():
    """顯示模板選項摘要"""
    print("=" * 80)
    print("PROMPT 模板參數說明")
    print("=" * 80)
    print("\n【prompt_template 參數】控制指令風格：")
    print("  0 = 預設版本 - 平衡的指令，允許使用 X 標籤")
    print("  1 = 開放版本 - 鼓勵探索新模式，考慮更多語言和結構")
    print("  2 = 嚴格版本 - 只使用現有標籤，避免創建新標籤")
    print("  3 = 簡化版本 - 最少指令，直接輸出")
    
    print("\n【tag_summary 參數】控制標籤說明：")
    print("  0 = 完整標籤列表 + 允許 X 標籤")
    print("  1 = 完整標籤列表 + 禁止創建新標籤")
    
    print("\n【推薦組合】：")
    print("  • 探索新模式：prompt_template(pwd, tag_summary=0, prompt_template=1)")
    print("  • 嚴格標註：  prompt_template(pwd, tag_summary=1, prompt_template=2)")
    print("  • 快速測試：  prompt_template(pwd, tag_summary=0, prompt_template=3)")
    print("=" * 80)
    print()


def show_prompt_templates():
    """顯示所有可用的PROMPT模板"""
    
    example_password = "john1990!"
    
    print("=" * 80)
    print("1. 單個密碼分析模板 - 預設版本 (prompt_template=0)")
    print("=" * 80)
    print(prompt_template(example_password, tag_summary=0, prompt_template=0))
    
    print("\n" + "=" * 80)
    print("2. 單個密碼分析模板 - 開放版本 (prompt_template=1)")
    print("   > 鼓勵探索新模式，考慮更多語言")
    print("=" * 80)
    print(prompt_template(example_password, tag_summary=0, prompt_template=1))
    
    print("\n" + "=" * 80)
    print("3. 單個密碼分析模板 - 嚴格版本 (prompt_template=2)")
    print("   > 只使用現有標籤，避免創建新標籤")
    print("=" * 80)
    print(prompt_template(example_password, tag_summary=1, prompt_template=2))
    
    print("\n" + "=" * 80)
    print("4. 單個密碼分析模板 - 簡化版本 (prompt_template=3)")
    print("   > 最少指令，直接輸出")
    print("=" * 80)
    print(prompt_template(example_password, tag_summary=0, prompt_template=3))
    
    print("\n" + "=" * 80)
    print("5. 批量密碼分析模板 (prompt_template_batch)")
    print("=" * 80)
    example_passwords = ["john1990!", "iloveyou", "qwerty123"]
    print(prompt_template_batch(example_passwords))
    
    print("\n" + "=" * 80)
    print("6. 未知標籤解釋模板 (prompt_explain_unknown_tags)")
    print("=" * 80)
    example_segments = [
        {"text": "mn", "tag": "INITIALS", "password": "306187mn"},
        {"text": "abc", "tag": "X", "password": "abc123"}
    ]
    print(prompt_explain_unknown_tags(example_segments))


if __name__ == "__main__":
    show_template_summary()
    
    print("\n")
    show_prompt_templates()
