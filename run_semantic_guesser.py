"""
使用 semantic-guesser 的 BackoffTagger 對密碼進行分段與詞性標記，
輸出與 LLM 推論結果相同格式的 JSONL，方便後續 Jaccard 比較。

執行方式：
    conda run -n pcfgllm python run_semantic_guesser.py
"""

import sys
import os
import json
import re

# 將 semantic-guesser 加入 import 路徑
SG_PATH = os.path.join(os.path.dirname(__file__), 'model', 'semantic-guesser')
if SG_PATH not in sys.path:
    sys.path.insert(0, SG_PATH)

import wordsegment as ws
from learning.train import getchunks, pos_tag, POSBlacklist
from learning.pos import BackoffTagger
from src.config import load_config, build_paths
from src.record import write_record
from main import load_passwords
from src.clean_data import clean


def derive_tag(chunk: str) -> str:
    """對 pos_tag 回傳 None 的 chunk，依內容推導基礎 tag。"""
    if re.fullmatch(r'[0-9]+', chunk):
        return 'NUMBER'
    if re.fullmatch(r'[\W_]+', chunk):
        return 'SPEC'
    return 'X'


def process_password(password: str, tagger, blacklist) -> list:
    """
    回傳 segments 列表，每個元素為 {"text": ..., "tag": ...}。
    tag 使用 CLAWS7 詞性標記（非字母 token 以 NUMBER / SPEC / X 補足）。
    """
    chunks = getchunks(password)
    if not chunks:
        return [{"text": password, "tag": "X"}]

    tagged = pos_tag(chunks, tagger, blacklist)

    segments = []
    for text, claws_tag in tagged:
        tag = claws_tag if claws_tag is not None else derive_tag(text)
        segments.append({"text": text, "tag": tag})

    return segments


def main():
    config = load_config()
    config["active_model"] = "semantic-guesser"  # 讓 build_paths 產生正確的輸出路徑
    paths  = build_paths(config)

    # 讀取密碼清單（與 main.py 完全相同的邏輯）
    data_cfg  = paths["data"]
    passwords = load_passwords(data_cfg["datasets"], data_cfg["max_passwords"])
    passwords = clean(passwords, batch_flag=True)
    passwords = passwords[:data_cfg["analysis_sample"]]

    # 初始化 semantic-guesser tagger
    print("載入 BackoffTagger（需要幾秒）...")
    ws.load()
    tagger   = BackoffTagger.from_pickle()
    blacklist = POSBlacklist()
    print("BackoffTagger 載入完成。")

    # 輸出路徑：與 main.py 相同方式，由 build_paths 統一管理
    exp_num     = config["output"]["experiment_number"]
    output_path = paths["output"]["pw_seg"]
    os.makedirs(paths["output"]["dir"], exist_ok=True)

    # 清空舊檔
    if os.path.exists(output_path):
        os.remove(output_path)

    # 寫入實驗紀錄
    write_record(
        record_path="record.csv",
        experiment_name=f"exp_{exp_num}",
        model_name="semantic-guesser",
        datasets=data_cfg["datasets"],
        template_id=0,
    )

    print(f"處理 {len(passwords)} 筆密碼 → {output_path}")

    with open(output_path, 'a', encoding='utf-8') as out_f:
        for i, pw in enumerate(passwords):
            try:
                segments = process_password(pw, tagger, blacklist)
            except Exception as e:
                segments = [{"text": pw, "tag": "X"}]
                print(f"[警告] 密碼 {pw!r} 處理失敗：{e}")

            record = {"password": pw, "segments": segments}
            out_f.write(json.dumps(record, ensure_ascii=False) + '\n')

            if (i + 1) % 10 == 0:
                print(f"  進度：{i+1}/{len(passwords)}")

    print(f"\n完成！輸出至 {output_path}")


if __name__ == '__main__':
    main()
