def get_existing_hashes(vector_store) -> set: 

    """
    Collects the hash values of all documents in the existing FAISS database.
    This way, we can avoid adding duplicates when adding new documents.
    """
    
    hashes = set() 

    for doc in vector_store.docstore._dict.values():
        doc_hash = doc.metadata.get("hash")
        if doc_hash:
            hashes.add(doc_hash)
    return hashes