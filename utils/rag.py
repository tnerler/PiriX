from utils.summarize_and_clarify import summarize_and_clarify
from dotenv import load_dotenv
from utils.state import State
from utils._faiss import FAISSVectorDatabase
from models.llm_models.openai_llm import get_llm
from operator import itemgetter
from langchain.prompts import (ChatPromptTemplate, 
                               HumanMessagePromptTemplate, 
                               MessagesPlaceholder, 
                               SystemMessagePromptTemplate)
from models.cross_encoder import get_cross_encoder
from utils.session_history import get_session_history
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import time
from utils.md_data_loader import markdown_loader

class PiriXChatbot: 

    def __init__(self, session_id: str = None):
        
        self.docs = markdown_loader()
        # faiss store
        self.vector_store = self._build_store(self.docs)

        # llm + history
        self.chain = self._build_chain()
        self.chain_with_history = RunnableWithMessageHistory(self.chain,
                                                             get_session_history,
                                                             input_messages_key="question",
                                                             history_messages_key="history")
        
        # cross encoder
        self.cross_encoder = get_cross_encoder()

        # session
        self.session_id = session_id

    def _build_store(self, docs=None): 

        faiss_db = FAISSVectorDatabase()
        faiss_db.load_or_create_store()

        if docs is not None: 
            faiss_db.add_documents(docs)
            
        else: 
            print(f"[i] Docs parameter is None, so vector database is empty!")

        store = faiss_db.get_store() 
        return store

    def _build_chain(self): 

        template = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            """
            Sen PiriX'sin, Piri Reis Üniversitesi'nin bilgi asistanısın. Temel görevin: Okul hakkında kısa, doğru ve anlaşılır bilgiler vermek. 
            ÖNEMLİ KURALLAR:
            1. Sadece Piri Reis Üniversitesi ile ilgili bilgi sorularına yanıt ver. Diğer konularda: "Ben sadece Piri Reis Üniversitesi hakkında bilgi verebilirim 💙 Diğer konular için başka bir asistana sormanı öneririm!"
            2. Bilmediğin konularda: "Bu konuda şu anda elimde bilgi yok. Detaylı bilgi için çağrı merkezimizi arayabilirsiniz: +90 216 581 00 50"
            3. Samimi ve arkadaşça konuş, robot gibi yanıtlardan kaçın. Emoji kullanabilirsin 😊
            4. Fiyat bilgilerinde şunu ekle: "Daha fazla detay için: https://aday.pirireis.edu.tr/ucretler/"
            5. Bölüm/kulüp listeleri sorulursa, verilen bilgilere sadık kalarak numaralı liste kullan. Uydurma.
            6. Okul tanıtımı sorularında güçlü yönleri vurgula ama abartma.
            7. Yanıtlar her zaman doğru, kısa ve net olmalı.
            8. 'Okulun resmi web sitesinden (https://www.pirireis.edu.tr/) ve sosyal medya hesaplarından (https://www.instagram.com/pirireisuni/) bilgi alabilirsin.' diyebilirsin.
            9. Rektör sorulursa: "Rektörü överken, onun liderlik özelliklerini ve üniversiteye katkılarını vurgula"
            10. **ÖNEMLİ**: Önceki konuşma geçmişini dikkate al ve konu bağlamını koru. Kullanıcı daha önce bir konu hakkında soru sorduysa, yeni sorularını o bağlamda değerlendir.
            11. Tercih indirimi sorulursa: "Tercih indirimleri her yıl geçerli olur."
            12. Burslarla ilgili sorularda: "Burslar hakkında detaylı bilgi için: https://aday.pirireis.edu.tr/burslar/"
            """
        ),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template(
            "Bağlam:{context}\n\nSoru:{question}\n\nCevap:"
        ),
    ])
        chain = template | get_llm()
        return chain
    

    def create_enhanced_query(self, current_question: str, history: ChatMessageHistory):
        if not history.messages:
            return current_question
        
        messages = []

        for msg in history.messages[-3:]:
            role = "Kullanıcı" if getattr(msg, "type", "") == "human" else "PiriX"
            messages.append(f"{role}: {msg.content}")

            _, clarified_question = summarize_and_clarify(messages, current_question)
            print(f"😊 Clarified Question: {clarified_question}")
            return clarified_question
    
    def retrieve(self, state: State): 
        query = state["question"]
        history = get_session_history(self.session_id) if self.session_id else ChatMessageHistory()
        enhanced_query = self.create_enhanced_query(query, history)

        results = self.vector_store.similarity_search_with_score(enhanced_query, k=20)
        top_docs = [doc for doc, _ in results]

        cross_encoder_inputs = [(enhanced_query, doc.page_content) for doc in top_docs]
        scores = self.cross_encoder.predict(cross_encoder_inputs)

        reranked_pairs = sorted(
            zip(top_docs, scores),
            key=itemgetter(1),
            reverse=True
        )

        reranked_docs = list(map(itemgetter(0), reranked_pairs[:12]))

        return {
            "context": reranked_docs,
            "question": query,
            "clarified_question": enhanced_query
        }

    def generate(self, state: State): 
        docs_content = "\n".join(doc.page_content for doc in state["context"])
        config = {"configurable": {"session_id": self.session_id}}

        input_data = {
            "question": state.get("clarified_question", state["question"]),
            "context": docs_content
        }
        answer = self.chain_with_history.invoke(input_data, config=config)
        return {"answer": answer.content}