import os
import numpy as np
import pandas as pd

from src.config import load_config, build_paths
from src.jaccard import (
    read_jsonl, calculate_jaccard_distance,
    cut_position, cut_position_with_tags,
)
from src import draw_result


def build_jaccard_paths(first_file: str, second_file: str, statistics_dir: str,
                        first_model: str, first_exp: int,
                        second_model: str, second_exp: int) -> dict:
    """建構 Jaccard 比較所需的輸入/輸出路徑"""
    comparison_name = f"{first_model}_vs_{second_model}"
    exp_name = f"exp_{first_exp}_vs_exp_{second_exp}"
    jaccard_dir = os.path.join(statistics_dir, "jaccard", comparison_name, exp_name)
    return {
        "input": {
            "first_result": first_file,
            "second_result": second_file,
        },
        "output": {
            "csv": os.path.join(jaccard_dir, "jaccard_distance.csv"),
            "dir": jaccard_dir,
            "histogram": os.path.join(jaccard_dir, "jaccard_histogram.png"),
            "heatmap": os.path.join(jaccard_dir, "jaccard_heatmap.png"),
            "sorted_bar": os.path.join(jaccard_dir, "jaccard_sorted_bar.png"),
            "single_passwords_dir": os.path.join(jaccard_dir, "single_passwords"),
        },
    }


if __name__ == "__main__":
    # 1. 載入配置
    config = load_config()
    base_paths = build_paths(config)

    # 2. 從 config.yaml 的 jaccard 區塊取得比較設定
    jaccard_cfg = config.get("jaccard", {})
    gen_dir = config["output"]["gen_dir"]

    first_model = jaccard_cfg.get("first_model", config["active_model"])
    first_exp = jaccard_cfg.get("first_exp", config["output"]["experiment_number"])
    second_model = jaccard_cfg.get("second_model", first_model)
    second_exp = jaccard_cfg.get("second_exp", first_exp)

    first_file = os.path.join(gen_dir, first_model, f"exp_{first_exp}.jsonl")
    second_file = os.path.join(gen_dir, second_model, f"exp_{second_exp}.jsonl")
    first_name = first_model
    second_name = second_model

    print(f"比較對象:")
    print(f"  第一個: {first_file}")
    print(f"  第二個: {second_file}")

    paths = build_jaccard_paths(
        first_file, second_file,
        statistics_dir=config["output"]["statistics_dir"],
        first_model=first_model, first_exp=first_exp,
        second_model=second_model, second_exp=second_exp,
    )
    OUT = paths["output"]

    # 3. 讀取資料
    data_first = read_jsonl(paths["input"]["first_result"])
    data_second = read_jsonl(paths["input"]["second_result"])

    # 4. 計算 Jaccard Distance
    password = []
    jac_distance = []
    for index in range(len(data_first)):
        p_first_set = set(cut_position(data_first[index][0], data_first[index][1]))
        p_second_set = set(cut_position(data_second[index][0], data_second[index][1]))
        dist = round(calculate_jaccard_distance(p_first_set, p_second_set), 6)
        jac_distance.append(dist)
        password.append(data_first[index][0])

    # 5. 儲存 CSV
    os.makedirs(OUT["dir"], exist_ok=True)
    pd.DataFrame({"password": password, "jaccard_distance": jac_distance}).to_csv(
        OUT["csv"], index=False
    )

    # 6. 繪圖
    draw_result.draw_histogram(jac_distance, OUT["histogram"])
    draw_result.draw_heatmap(jac_distance, OUT["heatmap"])
    draw_result.draw_sorted_bar(password, jac_distance, OUT["sorted_bar"])

    # 7. 統計摘要
    print("\n" + "=" * 50)
    print("統計摘要")
    print("=" * 50)
    print(f"密碼總數:     {len(jac_distance)}")
    print(f"平均距離:     {np.mean(jac_distance):.4f}")
    print(f"中位數:       {np.median(jac_distance):.4f}")
    print(f"標準差:       {np.std(jac_distance):.4f}")
    print(f"最小值:       {np.min(jac_distance):.4f}")
    print(f"最大值:       {np.max(jac_distance):.4f}")
    print(f"完全一致 (0): {sum(1 for d in jac_distance if d == 0)} 個")
    print("=" * 50)

    # 8. 列出有差異的密碼
    print("\n" + "=" * 80)
    print("所有有差異的密碼列表 (Jaccard Distance > 0)")
    print("=" * 80)

    diff_list = []
    for i, d in enumerate(jac_distance):
        if d > 0:
            pw = password[i]
            seg_first = " | ".join([s["text"] for s in data_first[i][1]])
            seg_second = " | ".join([s["text"] for s in data_second[i][1]])
            cuts_tags_first = cut_position_with_tags(pw, data_first[i][1])
            cuts_tags_second = cut_position_with_tags(pw, data_second[i][1])
            dup_first = {pos: tags for pos, tags in cuts_tags_first.items() if len(tags) > 1}
            dup_second = {pos: tags for pos, tags in cuts_tags_second.items() if len(tags) > 1}
            diff_list.append({
                "index": i,
                "password": pw,
                "jaccard": d,
                "seg_first": seg_first,
                "seg_second": seg_second,
                "cuts_tags_first": cuts_tags_first,
                "cuts_tags_second": cuts_tags_second,
                "dup_first": dup_first,
                "dup_second": dup_second,
            })

    diff_list.sort(key=lambda x: x["jaccard"], reverse=True)

    for item in diff_list:
        print(f"\n[{item['index']:03d}] 密碼: {item['password']}")
        print(f"      Jaccard Distance: {item['jaccard']:.4f}")
        print(f"      {first_name} 切割: {item['seg_first']}")
        print(f"      {second_name} 切割: {item['seg_second']}")
        print(f"      {first_name} 位置(tags): {item['cuts_tags_first']}")
        print(f"      {second_name} 位置(tags): {item['cuts_tags_second']}")
        if item["dup_first"]:
            print(f"      *** {first_name} 重複切割: {item['dup_first']}")
        if item["dup_second"]:
            print(f"      *** {second_name} 重複切割: {item['dup_second']}")

    dup_first_count = sum(1 for item in diff_list if item["dup_first"])
    dup_second_count = sum(1 for item in diff_list if item["dup_second"])

    print("\n" + "=" * 80)
    print(f"共有 {len(diff_list)} 個密碼有切割差異")
    print(f"其中 {first_name} 模型有重複切割: {dup_first_count} 個")
    print(f"其中 {second_name} 模型有重複切割: {dup_second_count} 個")
    print("=" * 80)

    # 9. 產生有差異的視覺化圖片
    draw_result.draw_all_different_passwords(
        diff_list, data_first, data_second,
        cut_position, calculate_jaccard_distance, cut_position_with_tags,
        OUT["single_passwords_dir"],
    )
