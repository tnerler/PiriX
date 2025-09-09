from langchain_openai import OpenAIEmbeddings
import os 
from dotenv import load_dotenv
#from tenacity import retry, wait_random_exponential, stop_after_attempt

load_dotenv()

#@retry(wait=wait_random_exponential(min=1,max=30),stop=stop_after_attempt(5))

def openai_embedding_model(): 

    """Returns the embedding model of OpenAI."""

    model = OpenAIEmbeddings(
        model="text-embedding-3-large",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    return model