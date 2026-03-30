import os
import yaml


def load_config(config_path: str = "config.yaml") -> dict:
    """載入 YAML 配置檔"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def discover_models(model_dir: str = "model") -> list[str]:
    """自動掃描 model/ 目錄下的所有模型資料夾"""
    if not os.path.isdir(model_dir):
        return []
    return sorted([
        name for name in os.listdir(model_dir)
        if os.path.isdir(os.path.join(model_dir, name))
    ])


def discover_datasets(data_dir: str = "data", extensions: tuple = (".txt", ".csv")) -> list[str]:
    """自動掃描 data/ 目錄下所有指定副檔名的檔案"""
    if not os.path.isdir(data_dir):
        return []
    return sorted([
        name for name in os.listdir(data_dir)
        if os.path.isfile(os.path.join(data_dir, name))
        and os.path.splitext(name)[1].lower() in extensions
    ])


def get_model_params(config: dict, model_name: str) -> dict:
    """取得模型參數（預設值 + 模型覆寫）"""
    params = dict(config.get("model_defaults", {}))
    overrides = config.get("model_overrides") or {}
    if model_name in overrides:
        params.update(overrides[model_name])
    return params


def build_paths(config: dict) -> dict:
    """根據配置建構所有需要的路徑"""
    paths = {}

    # --- 模型 ---
    model_name = config["active_model"]
    model_path = os.path.join("model", model_name)
    params = get_model_params(config, model_name)
    paths["model"] = {
        "name": model_name,
        "path": model_path,
        **params,
    }

    # --- 資料集 ---
    input_dir = config["data"]["input_dir"]
    datasets_cfg = config["data"].get("datasets") or []
    if not datasets_cfg:
        datasets_cfg = discover_datasets(input_dir)
    paths["data"] = {
        "datasets": [os.path.join(input_dir, ds) for ds in datasets_cfg],
        "max_passwords": config["data"]["processing"]["max_passwords"],
        "analysis_sample": config["data"]["processing"]["analysis_sample"],
        "batch_size": config["data"]["processing"]["batch_size"],
    }

    # --- Prompt ---
    prompt_cfg = config.get("prompt", {})
    paths["prompt"] = {
        "template": prompt_cfg.get("template", 1),
        "tag_summary": prompt_cfg.get("tag_summary", 0),
        "enable_thinking": prompt_cfg.get("enable_thinking", False),
    }

    # --- 輸出 gen/{model_name}/exp_{number}.jsonl ---
    gen_dir = config["output"]["gen_dir"]
    exp_num = config["output"]["experiment_number"]
    output_dir = os.path.join(gen_dir, model_name)
    paths["output"] = {
        "dir": output_dir,
        "pw_seg": os.path.join(output_dir, f"exp_{exp_num}.jsonl"),
    }

    # --- 統計 ---
    stats_dir = config["output"]["statistics_dir"]
    stats_exp_dir = os.path.join(stats_dir, model_name, f"exp_{exp_num}")
    paths["statistics"] = {
        "dir": stats_exp_dir,
        "csv": os.path.join(stats_exp_dir, "jaccard_distance.csv"),
        "histogram": os.path.join(stats_exp_dir, "jaccard_histogram.png"),
        "heatmap": os.path.join(stats_exp_dir, "jaccard_heatmap.png"),
        "sorted_bar": os.path.join(stats_exp_dir, "jaccard_sorted_bar.png"),
        "single_passwords_dir": os.path.join(stats_exp_dir, "single_passwords"),
    }

    return paths
