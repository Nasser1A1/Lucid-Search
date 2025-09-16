from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np
# 1. Load a pretrained Sentence Transformer model

class SortSearchService:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def sort_results(self, query: str, results: List[dict]):
        relevant_docs = []
        query_embedding = self.model.encode([query])[0]  # shape: (384,)
        for result in results:
            res = result.get("content", "")
            if not res:
                continue
            result_embedding = self.model.encode(result.get("content", ""))
            print("Finding similarity between Query and Result")
            similarity = np.dot(query_embedding, result_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(result_embedding)
            )
            result["relevence_score"] = float(similarity)  # ✅ Convert to Python float
            if similarity > 0.3:
                relevant_docs.append(result)
            
        return sorted(relevant_docs, key=lambda x: x["relevence_score"], reverse=True)
