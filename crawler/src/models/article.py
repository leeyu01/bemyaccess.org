"""
Data models for the crawler.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    """Represents a news article to be inserted into Supabase."""
    title: str
    content: str
    summary: Optional[str] = None
    source_url: Optional[str] = None
    category_id: int = 1  # Default to Local News
    source_name: str = ""
    published_at: Optional[datetime] = None
    dedup_hash: Optional[str] = None
    is_active: bool = True

    def to_dict(self):
        """Convert to dictionary for Supabase insertion."""
        return {
            'title': self.title,
            'content': self.content,
            'summary': self.summary,
            'source_url': self.source_url,
            'category_id': self.category_id,
            'source_name': self.source_name,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'dedup_hash': self.dedup_hash,
            'is_active': self.is_active,
        }
