from abc import ABC, abstractmethod


class BaseCrawler(ABC):

    @abstractmethod
    def fetch(self, url: str | None = None):
        pass

    @abstractmethod
    def get_links(self, html: str):
        pass

    @abstractmethod
    def get_pdf_links(self, links: list[str]):
        pass