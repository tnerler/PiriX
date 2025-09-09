import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS 
from models.embedding_models.load_model import get_embedding_model
import os 
from utils.compute_hash import compute_hash
from utils.existing_hashes import get_existing_hashes
import time

class FAISSVectorDatabase:
    """

    Usage: 
    faiss_vd = FAISSVectorDatabase()
    faiss_vd.load_or_create_store()
    docs = markdown_loader() # --> our markdown_loader() function.
    faiss_vd.add_documents(docs)
    store = faiss_vd.get_store()

    """
    def __init__(self, persist_path="vector_db", batch_size=250):
        self.persist_path = persist_path
        self.batch_size = batch_size
        self.embedding_model = get_embedding_model(model_type="bge-m3")
        self.vector_store = None
        self.existing_hashes = set()

    def load_or_create_store(self): 
        if os.path.exists(self.persist_path): 
            print(f"[i] Founded FAISS vector store, loading...")
            self.vector_store = FAISS.load_local(self.persist_path, self.embedding_model, allow_dangerous_deserialization=True)
            self.existing_hashes = get_existing_hashes(self.vector_store)

        else: 
            print(f"[i] Was not found any FAISS vector store, creating new...")
            embedding_dim = len(self.embedding_model.embed_query("pirireis"))
            index = faiss.IndexFlatIP(embedding_dim)
            self.vector_store = FAISS(
                embedding_function=self.embedding_model,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
            )
            self.existing_hashes = set()

    def add_documents(self, docs): 
        print(f"[i] Chunking is starting...")

        processed_docs = []
        skipped = 0
        start_time = time.time()

        for split in docs: 
            chunk_hash = compute_hash(split.page_content)
            if chunk_hash in self.existing_hashes:
                skipped += 1
                continue
            split.metadata["hash"] = chunk_hash
            processed_docs.append(split)
        print(f"Adding {len(processed_docs)} docs, skipped {skipped} already in store.")

        for i in range(0, len(processed_docs), self.batch_size): 
            batch = processed_docs[i:i+self.batch_size]
            print(f"[i] Embedding batch {i} -> {i+len(batch)}")
            self.vector_store.add_documents(batch)
        
        self.vector_store.save_local(self.persist_path)
        print(f"[DONE] Update finished in {round(time.time() - start_time, 2)}s.")
    
    def get_store(self): 
        return self.vector_store
    