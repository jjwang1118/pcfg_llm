import datasets
from datasets import load_dataset

from src.config import load_config, build_paths
from src.model_loader import load_model
from src.inference import analyze_password, save_result
from src.prompt import prompt_template
from src.clean_data import clean
from src.record import write_record


def load_passwords(data_paths: list, max_passwords: int) -> list:
    """載入並合併所有資料集，回傳密碼列表"""
    all_datasets = []
    for path in data_paths:
        ds = load_dataset("text", data_files={"train": path})
        all_datasets.append(ds["train"])
    combined = datasets.concatenate_datasets(all_datasets)
    return combined["text"][:max_passwords]


if __name__ == "__main__":

    # 1. 載入配置
    config = load_config()
    paths = build_paths(config)

    # 2. 載入模型
    model, tokenizer = load_model(paths["model"]["path"])

    # 3. 載入資料集並清洗
    passwords = load_passwords(paths["data"]["datasets"], paths["data"]["max_passwords"])
    passwords = clean(passwords, batch_flag=True)

    # 4. 取得推論參數
    max_new_tokens = paths["model"]["max_new_tokens"]
    temperature = paths["model"]["temperature"]
    top_p = paths["model"]["top_p"]
    enable_thinking = paths["prompt"]["enable_thinking"]
    template_id = paths["prompt"]["template"]
    tag_summary_id = paths["prompt"]["tag_summary"]
    output_path = paths["output"]["pw_seg"]

    # 6. 寫入實驗紀錄
    exp_name = f"exp_{config['output']['experiment_number']}"
    write_record(
        record_path="record.csv",
        experiment_name=exp_name,
        model_name=config["active_model"],
        datasets=paths["data"]["datasets"],
        template_id=template_id,
    )

    # 7. 逐筆推論
    for pwd in passwords:
        prompt_text = prompt_template(pwd, tag_summary=tag_summary_id, prompt_template=template_id)
        result = analyze_password(
            password=pwd,
            model=model,
            tokenizer=tokenizer,
            prompt_text=prompt_text,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            enable_thinking=enable_thinking,
        )
        save_result(result["result"], output_path)

