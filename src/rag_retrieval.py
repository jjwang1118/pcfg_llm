from pathlib import Path
import yaml
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from src.rag_index_offline import build_vectorstore


def load_config(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class RAGRetriever:
    def __init__(self, config=None):
        if config is None:
            config = load_config()

        self.cfg = config["RAG"]
        self.retrieval_cfg = self.cfg["retrieval"]
        self.index_cfg = self.cfg["index"]

        # index 不存在或 MD 有更新時自動重建
        build_vectorstore(config)

        embeddings = HuggingFaceEmbeddings(
            model_name=self.index_cfg["embedding_model"],
            model_kwargs={"device": self.index_cfg["device"]},
            encode_kwargs={"normalize_embeddings": self.index_cfg["normalize_embeddings"]},
        )
        self.vectorstore = FAISS.load_local(
            self.index_cfg["index_path"],
            embeddings,
            allow_dangerous_deserialization=True,
        )

    def retrieve(self, query: str) -> list[dict]:
        """
        回傳與 query 最相關的 tag 定義，過濾掉低於 score_threshold 的結果。
        每筆結果含 content 和 score。
        """
        top_k = self.retrieval_cfg["top_k"]
        threshold = self.retrieval_cfg["score_threshold"]

        results = self.vectorstore.similarity_search_with_relevance_scores(query, k=top_k)

        return [
            {"content": doc.page_content, "score": score}
            for doc, score in results
            if score >= threshold
        ]

    def retrieve_as_context(self, query: str) -> str:
        """回傳可直接注入 prompt 的純文字，結果之間以分隔線區隔。"""
        hits = self.retrieve(query)
        if not hits:
            return ""
        return "\n---\n".join(h["content"] for h in hits)

    def retrieve_from_segments(self, segments: list[dict]) -> str:
        """
        用第一次推論切出的 segments 逐一 query RAG，去重後合併回傳。
        segments 格式：[{"text": "dragon", "tag": "ENGLISH_NOUN"}, ...]
        """
        seen = set()
        parts = []
        for seg in segments:
            for hit in self.retrieve(seg["text"]):
                if hit["content"] not in seen:
                    seen.add(hit["content"])
                    parts.append(hit["content"])
        return "\n---\n".join(parts)


if __name__ == "__main__":
    import json

    retriever = RAGRetriever()

    # 從 jsonl 讀一筆範例
    jsonl_path = "gen/Llama-3.1-8B-Instruct/exp_2.jsonl"
    with open(jsonl_path, "r", encoding="utf-8") as f:
        example = json.loads(f.readline())

    password = example["password"]
    segments = example["segments"]

    print(f"密碼: {password}")
    print(f"既有 segments: {segments}\n")

    # 用每個 segment 的 text 分別 query RAG
    print("=== 各 segment 的 RAG 查詢分數 ===")
    for seg in segments:
        raw = retriever.vectorstore.similarity_search_with_relevance_scores(seg["text"], k=3)
        print(f"\n  query: '{seg['text']}' (原始 tag: {seg['tag']})")
        for doc, score in raw:
            header = doc.page_content[:60].replace("\n", " ")
            print(f"    score={score:.3f}  {header}")

    # 用 retrieve_from_segments 取得最終 context
    print("\n=== 最終注入 prompt 的 RAG context ===")
    context = retriever.retrieve_from_segments(segments)
    print(context if context else "（無 hit，context 為空）")
