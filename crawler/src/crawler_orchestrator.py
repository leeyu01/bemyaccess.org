"""
Main crawler orchestrator.
"""
import logging
from typing import List
from .crawlers.base_crawler import BaseCrawler
from .utils.helpers import setup_logging

# Import specific crawlers
# from .crawlers.helen_keller import HelenKellerCrawler
# TODO: Implement individual crawlers

logger = logging.getLogger(__name__)


class CrawlerOrchestrator:
    """Orchestrates crawling from all sources."""

    def __init__(self, crawlers: List[BaseCrawler]):
        self.crawlers = crawlers
        setup_logging()

    def run_all(self) -> List:
        """
        Run all crawlers and collect articles.
        Returns list of Article objects.
        """
        all_articles = []

        for crawler in self.crawlers:
            articles = crawler.run()
            all_articles.extend(articles)

        logger.info(f"Total articles crawled: {len(all_articles)}")
        return all_articles


def main():
    """Entry point for the crawler."""
    # TODO: Initialize all crawlers from config
    # orchestrator = CrawlerOrchestrator(crawlers)
    # articles = orchestrator.run_all()
    pass


if __name__ == "__main__":
    main()
