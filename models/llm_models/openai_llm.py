from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os 

load_dotenv()

def get_llm(): 

    try:
        llm = init_chat_model(model="gpt-4o",
                            model_provider="openai",
                            api_key=os.getenv("OPENAI_API_KEY"),
                            temperature=0.7,)
        return llm
    except Exception as e:
        print(f"Error in starting LLM: {e}")
        raise