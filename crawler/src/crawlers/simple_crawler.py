"""
Simple crawler implementation for testing.
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from ..models.article import Article
from .base_crawler import BaseCrawler
from ..utils.helpers import compute_dedup_hash


class SimpleTestCrawler(BaseCrawler):
    """A simple test crawler that fetches a webpage and extracts text."""

    def crawl(self):
        """Fetch the source URL and extract article-like content."""
        try:
            response = requests.get(self.base_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Simple extraction - just get all paragraph text
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text(strip=True) for p in paragraphs[:5]])

            if not content:
                return []

            # Use current time as published_at since it's not in the HTML
            article = Article(
                title=self.source_name,
                content=content[:5000],  # Limit length
                source_name=self.source_name,
                source_url=self.base_url,
                published_at=datetime.now(),
            )
            article.dedup_hash = compute_dedup_hash(article.content)

            return [article]
        except Exception as e:
            print(f"Error in SimpleTestCrawler for {self.source_name}: {e}")
            return []
