from typing_extensions import TypedDict

class State(TypedDict): 
    question: str
    clarified_question: str
    context: str
    answer: str