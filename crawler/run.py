#!/usr/bin/env python3
"""
Main entry point for the crawler.
Run: python run.py
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.crawler_orchestrator import CrawlerOrchestrator
from src.supabase_client import insert_article
from config import RSS_SOURCES

def main():
    """Run all crawlers and insert articles into Supabase."""
    print("=== Be My Access Crawler ===\n")

    # Import here to ensure env is loaded first
    from src.crawlers.simple_crawler import SimpleTestCrawler

    # For now, use the simple test crawler on all sources
    crawlers = [SimpleTestCrawler(source_name=f"Source {i}", base_url=url) for i, url in enumerate(RSS_SOURCES)]

    orchestrator = CrawlerOrchestrator(crawlers)
    articles = orchestrator.run_all()

    print(f"\nFetched {len(articles)} articles")

    # Insert into Supabase
    inserted = 0
    for article in articles:
        article_dict = article.to_dict()
        if insert_article(article_dict):
            inserted += 1

    print(f"\nInserted {inserted} new articles")
    print("Crawler completed!")

if __name__ == "__main__":
    main()
