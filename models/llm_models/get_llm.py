from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os 
from langchain_ollama import ChatOllama

load_dotenv()

def get_llm(model_provider="openai"):
    try:
        if model_provider=="openai":
            print("OpenAI is being used.")
            return init_chat_model(
                model="gpt-4o",
                model_provider="openai",
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.7,
                tracing=True,
            )

        elif model_provider=="ollama":
            print("Ollama is being used.")
            return ChatOllama(
                model="qwen2.5:14b-instruct-q4_K_M",
                temperature=0.7,
                num_ctx=16000,
                tracing=True,
            )
        else:
            raise ValueError(f"Unknown model provider: {model_provider}")
    except Exception as e:
        print(f"Error in starting LLM: {e}")
        raise
