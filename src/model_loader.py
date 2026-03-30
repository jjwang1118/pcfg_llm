from transformers import AutoModelForCausalLM, AutoTokenizer


def load_model(model_path: str):
    """載入模型與 tokenizer"""
    print(f"Loading model: {model_path}")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype="auto",
        device_map="auto",
    )
    print("Model loaded successfully!\n")
    return model, tokenizer
