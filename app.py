from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient
from bson import ObjectId
import uuid
import os

from dotenv import load_dotenv
from utils.rag import PiriXChatbot

# --- Load env ---
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE = os.getenv("DATABASE")

# --- FastAPI init ---
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
# --- Mongo init ---
client = MongoClient(MONGO_URI)
db = client[DATABASE]

# --- Chatbot init ---
chatbot = PiriXChatbot()


# --- Models --- 
class AskMessage(BaseModel): 
    question: str
    session_id: str | None = None

class FeedBackMessage(BaseModel):
    feedback_id: str
    feedback_type: str
    session_id: str | None = None


# --- Routes --- 
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    session_id = str(uuid.uuid4())
    with open("templates/index.html") as f:
        html_content = f.read()
    html_content = html_content.replace("{{ session_id }}", session_id)
    return HTMLResponse(content=html_content)


@app.post("/ask")
def ask(msg: AskMessage): 
    session_id = msg.session_id or str(uuid.uuid4())
    state = {"question": msg.question, "context": [], "clarified_question": "", "answer": ""}

# retrieve & generate
    retrieval_result = chatbot.retrieve(state)
    state["context"] = retrieval_result["context"]
    state["clarified_question"] = retrieval_result.get("clarified_question", msg.question)

    generation_result = chatbot.generate(state)
    state["answer"] = generation_result["answer"]

    # feedback kaydet
    feedback_doc = {
        "session_id": session_id,
        "question": msg.question,
        "clarified_question": state["clarified_question"],
        "retrieved_contexts": [doc.page_content for doc in state["context"]],
        "answer": state["answer"],
        "feedback_type": "pending"
    }
    result = db.feedback.insert_one(feedback_doc)

    print("Inserted ID:", result.inserted_id)  # yeni ekle
    print("Feedback count:", db.feedback.count_documents({}))

    feedback_id = str(result.inserted_id)

    return {
        "answer": state["answer"],
        "feedback_id": feedback_id,
        "session_id": session_id
    }


@app.post("/feedback")
def save_feedback(msg: FeedBackMessage):
    if msg.feedback_type not in ("like", "dislike"):
        return {"error": "Feedback tipi like/dislike olmalı"}

    result = db.feedback.update_one(
        {"_id": ObjectId(msg.feedback_id)},  # ObjectId fix
        {"$set": {"feedback_type": msg.feedback_type}}
    )
    if result.modified_count > 0:
        return {"success": True}
    else:
        return {"error": "Kayıt bulunamadı"}