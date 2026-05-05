import hashlib
import json
import yaml
from pathlib import Path
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def load_config(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def split_markdown(text):
    headers = [("##", "h2")]
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers)
    chunks = splitter.split_text(text)
    # tag 名稱被 splitter 存進 metadata，補回 page_content 讓 embedding 能抓到
    for chunk in chunks:
        tag_name = chunk.metadata.get("h2", "")
        if tag_name:
            chunk.page_content = f"## {tag_name}\n{chunk.page_content}"
    return chunks


def build_embeddings(index_cfg):
    return HuggingFaceEmbeddings(
        model_name=index_cfg["embedding_model"],
        model_kwargs={"device": index_cfg["device"]},
        encode_kwargs={"normalize_embeddings": index_cfg["normalize_embeddings"]},
    )


def _md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def _hash_path(index_path: str) -> Path:
    return Path(index_path) / "source.hash"


def _is_up_to_date(index_path: str, current_hash: str) -> bool:
    hp = _hash_path(index_path)
    if not hp.exists():
        return False
    return json.loads(hp.read_text())["hash"] == current_hash


def _save_hash(index_path: str, current_hash: str):
    hp = _hash_path(index_path)
    hp.parent.mkdir(parents=True, exist_ok=True)
    hp.write_text(json.dumps({"hash": current_hash}))


def build_vectorstore(config=None, force=False):
    if config is None:
        config = load_config()

    index_cfg = config["RAG"]["index"]
    text = load_markdown(index_cfg["knowledge_base"])
    current_hash = _md5(text)

    if not force and _is_up_to_date(index_cfg["index_path"], current_hash):
        print("Index is up to date, skipping rebuild.")
        return

    chunks = split_markdown(text)
    embeddings = build_embeddings(index_cfg)
    vs = FAISS.from_documents(chunks, embeddings)
    vs.save_local(index_cfg["index_path"])
    _save_hash(index_cfg["index_path"], current_hash)
    print(f"Index saved to: {index_cfg['index_path']}  ({len(chunks)} chunks)")
    return vs


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="強制重建索引，忽略 hash 快取")
    args = parser.parse_args()
    build_vectorstore(force=args.force)
