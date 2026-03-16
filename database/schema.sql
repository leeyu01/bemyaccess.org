# Supabase tables

## categories
| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| name | VARCHAR(100) | NOT NULL, UNIQUE |
| description | TEXT | |

Seed data:
- 'Local News'
- 'News for the Disabled'
- 'Weather'

## articles
| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| title | VARCHAR(300) | NOT NULL |
| content | TEXT | NOT NULL |
| summary | TEXT | AI-generated summary for TTS |
| source_url | VARCHAR(500) | Original RSS source |
| category_id | INTEGER | FOREIGN KEY → categories(id) |
| source_name | VARCHAR(200) | e.g., 'Newsday', 'Patch Suffolk' |
| published_at | TIMESTAMPTZ | NOT NULL |
| crawled_at | TIMESTAMPTZ | DEFAULT NOW() |
| dedup_hash | VARCHAR(64) | SHA-256 for de-duplication |
| is_active | BOOLEAN | DEFAULT TRUE |

## tags (optional - may not be needed)
## article_tags (optional)
