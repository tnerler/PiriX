from sentence_transformers import SentenceTransformer
from typing import List
from langchain_core.embeddings import Embeddings

class BGEM3(Embeddings):
    """
    Application compatible with LangChain using sentence transformers for the BGE-M3 model.
    Otherwise, it won't work with LangChain.
    """

    def __init__(self, model_name: str = "BAAI/bge-m3"): 
        self.model = SentenceTransformer(model_name, trust_remote_code=True)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embedding for multiple documents.
        """
        embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        return embeddings.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """
        Embedding for just One Query.
        """
        embedding = self.model.encode([text], convert_to_numpy=True)
        return embedding[0].tolist()

        