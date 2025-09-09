import hashlib

def compute_hash(content: str) -> str: 
    """
    ## -- Why is this necessary? --
    ### This script is used to generate a unique hash value for a given piece of data.
    ### By hashing content, we can:
    ###     1. Detect and remove duplicate documents during preprocessing.
    ###     2. Ensure data integrity when storing and retrieving from embeddings or databases.
    ###     3. Create consistent identifiers for chunks, making it easier to track, cache or update them

    ### Without hashing, we would need to store or compare entire raw documents, which is inefficient.

    ## -- What it returns? --
    ### An id (hash) for the data we gave
    """
    id = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return id
