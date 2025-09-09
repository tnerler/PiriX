from langchain_community.chat_message_histories import ChatMessageHistory
import threading

store = {}
store_lock = threading.Lock()

def get_session_history(session_id: str): 

    """
    Returns a ChatMessageHistory Langchain object for each session.
    """

    with store_lock: 
        if session_id not in store:
            store[session_id] = ChatMessageHistory()
        return store[session_id]