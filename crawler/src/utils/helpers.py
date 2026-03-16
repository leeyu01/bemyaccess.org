"""
Utilities for the crawler.
"""
import hashlib
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def compute_dedup_hash(content: str) -> str:
    """
    Compute SHA-256 hash of content for de-duplication.
    """
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def clean_html(html: str) -> str:
    """
    Remove HTML tags from content. Stubbed for now - would use BeautifulSoup.
    """
    # TODO: Implement with BeautifulSoup
    return html


def setup_logging(level=logging.INFO):
    """Configure logging for the crawler."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
