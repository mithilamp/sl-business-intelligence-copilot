from dataclasses import dataclass

@dataclass
class Source:
    title: str
    filename: str
    source: str
    document_url: str | None = None
    category: str | None = None
    document_type: str | None = None
    published_date: str | None = None
    chunks: list[dict] | None = None

@dataclass
class RAGResults: 
    question: str
    answer: str
    sources: list[Source]