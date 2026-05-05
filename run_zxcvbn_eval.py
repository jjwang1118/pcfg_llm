import os
import numpy as np
import pandas as pd

from src.config import load_config
from src.jaccard import read_jsonl, calculate_jaccard_distance, cut_position, cut_position_with_tags
from src.zxcvbn import zxcvbn_to_segments
from src import draw_result


if __name__ == "__main__":
    # 1. 載入配置
    config = load_config()
    zxcvbn_cfg = config.get("zxcvbn_eval", {})
    gen_dir = config["output"]["gen_dir"]

    model = zxcvbn_cfg.get("model", config["active_model"])
    exp = zxcvbn_cfg.get("exp", config["output"]["experiment_number"])

    # 2. 決定輸入路徑（優先用 _structured.jsonl，template 7 的後處理結果）
    structured_path = os.path.join(gen_dir, model, f"exp_{exp}_structured.jsonl")
    raw_path = os.path.join(gen_dir, model, f"exp_{exp}.jsonl")
    input_path = structured_path if os.path.exists(structured_path) else raw_path
    print(f"讀取: {input_path}")

    # 3. 輸出目錄
    out_dir = os.path.join(config["output"]["statistics_dir"], "zxcvbn", model, f"exp_{exp}")
    os.makedirs(out_dir, exist_ok=True)

    # 4. 讀取 LLM 輸出
    data_llm = read_jsonl(input_path)

    # 5. 對每個密碼跑 zxcvbn
    data_zxcvbn = [(pwd, zxcvbn_to_segments(pwd)) for pwd, _ in data_llm]

    # 6. 計算 Jaccard Distance
    passwords = []
    jac_distances = []
    for (pwd, llm_segs), (_, zx_segs) in zip(data_llm, data_zxcvbn):
        llm_cuts = set(cut_position(pwd, llm_segs))
        zx_cuts = set(cut_position(pwd, zx_segs))
        dist = round(calculate_jaccard_distance(llm_cuts, zx_cuts), 6)
        passwords.append(pwd)
        jac_distances.append(dist)

    # 7. 儲存 CSV
    csv_path = os.path.join(out_dir, "jaccard_distance.csv")
    pd.DataFrame({"password": passwords, "jaccard_distance": jac_distances}).to_csv(csv_path, index=False)
    print(f"CSV 已儲存: {csv_path}")

    # 8. 繪圖
    draw_result.draw_histogram(jac_distances, os.path.join(out_dir, "jaccard_histogram.png"), model, "zxcvbn")
    draw_result.draw_heatmap(jac_distances, os.path.join(out_dir, "jaccard_heatmap.png"), model, "zxcvbn")
    draw_result.draw_sorted_bar(passwords, jac_distances, os.path.join(out_dir, "jaccard_sorted_bar.png"))

    # 9. 統計摘要
    print("\n" + "=" * 50)
    print("統計摘要")
    print("=" * 50)
    print(f"密碼總數:     {len(jac_distances)}")
    print(f"平均距離:     {np.mean(jac_distances):.4f}")
    print(f"中位數:       {np.median(jac_distances):.4f}")
    print(f"標準差:       {np.std(jac_distances):.4f}")
    print(f"最小值:       {np.min(jac_distances):.4f}")
    print(f"最大值:       {np.max(jac_distances):.4f}")
    print(f"完全一致 (0): {sum(1 for d in jac_distances if d == 0)} 個")
    print("=" * 50)

    # 10. 列出有差異的密碼
    diff_list = []
    for i, d in enumerate(jac_distances):
        if d > 0:
            pwd = passwords[i]
            diff_list.append({
                "index": i,
                "password": pwd,
                "jaccard": d,
            })
    diff_list.sort(key=lambda x: x["jaccard"], reverse=True)

    print("\n" + "=" * 80)
    print("所有有差異的密碼列表 (Jaccard Distance > 0)")
    print("=" * 80)
    for item in diff_list:
        seg_llm = " | ".join(s["text"] for s in data_llm[item["index"]][1])
        seg_zx = " | ".join(s["text"] for s in data_zxcvbn[item["index"]][1])
        print(f"\n[{item['index']:03d}] 密碼: {item['password']}")
        print(f"      Jaccard Distance: {item['jaccard']:.4f}")
        print(f"      {model} 切割:  {seg_llm}")
        print(f"      zxcvbn 切割: {seg_zx}")
    print("\n" + "=" * 80)
    print(f"共有 {len(diff_list)} 個密碼有切割差異")
    print("=" * 80)

    # 11. 產生有差異的視覺化圖片
    draw_result.draw_all_different_passwords(
        diff_list, data_llm, data_zxcvbn,
        cut_position, calculate_jaccard_distance, cut_position_with_tags,
        os.path.join(out_dir, "single_passwords"),
        first_model_name=model,
        second_model_name="zxcvbn",
    )
