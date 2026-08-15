from dataclasses import dataclass

@dataclass
class RAGResults: 
    question: str
    answer: str
    sources: list[str]