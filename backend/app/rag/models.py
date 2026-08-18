from dataclasses import dataclass

@dataclass
class Source:
    title: str
    filename: str
    source: str
    document_url: str | None = None

@dataclass
class RAGResults: 
    question: str
    answer: str
    sources: list[Source]