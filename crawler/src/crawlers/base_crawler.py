"""
Base crawler interface.
"""
from abc import ABC, abstractmethod
from typing import List
from ..models.article import Article


class BaseCrawler(ABC):
    """Abstract base class for all crawlers."""

    def __init__(self, source_name: str, base_url: str):
        self.source_name = source_name
        self.base_url = base_url

    @abstractmethod
    def crawl(self) -> List[Article]:
        """
        Crawl the source and return a list of articles.
        Must be implemented by subclasses.
        """
        pass

    def run(self) -> List[Article]:
        """
        Execute the crawl with error handling and logging.
        """
        try:
            print(f"Starting crawl: {self.source_name} ({self.base_url})")
            articles = self.crawl()
            print(f"Completed crawl: {self.source_name} - {len(articles)} articles found")
            return articles
        except Exception as e:
            print(f"Error crawling {self.source_name}: {e}")
            return []
