from models.embedding_models.bge_m3 import BGEM3
from models.embedding_models.openai_em import openai_embedding_model


def get_embedding_model(model_type: str = "bge-m3"): 
    """
    Options of model_type: 
        1. bge-m3(default)
        2. openai
    
    returns the embedding model which you choose.
    """
    
    if model_type == "bge-m3": 
        return BGEM3(model_name="BAAI/bge-m3")

    elif model_type == "openai":
        return openai_embedding_model()
    
    else: 
        raise ValueError("Invalid Choice! Please either choose 'bge-m3' or 'openai'.")