import os
from supabase import create_client
from dotenv import load_dotenv

_loaded = False
_supabase = None

def get_supabase():
    """Get or create Supabase client (lazy initialization)."""
    global _loaded, _supabase
    if not _loaded:
        # Load environment variables using absolute path
        env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env.crawler')
        load_dotenv(env_path)
        SUPABASE_URL = os.getenv('SUPABASE_URL')
        SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')

        if not SUPABASE_URL or not SUPABASE_ANON_KEY:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env.crawler")

        _supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        _loaded = True
    return _supabase


def insert_article(article_dict: dict) -> bool:
    """
    Insert an article into Supabase if it doesn't already exist (by dedup_hash).
    Returns True if inserted, False if duplicate.
    """
    try:
        supabase = get_supabase()
        # Check for existing article by dedup_hash
        existing = supabase.table('articles').select('id').eq('dedup_hash', article_dict['dedup_hash']).execute()

        if existing.data and len(existing.data) > 0:
            print(f"Duplicate article found: {article_dict.get('title')}")
            return False

        result = supabase.table('articles').insert(article_dict).execute()
        print(f"Inserted article: {article_dict.get('title')}")
        return True
    except Exception as e:
        # Use ASCII-safe error message
        title = article_dict.get('title', 'Unknown')
        title_ascii = title.encode('ascii', errors='replace').decode('ascii')
        print(f"Error inserting article '{title_ascii}': {e}")
        return False


def test_connection():
    """Test Supabase connection."""
    try:
        supabase = get_supabase()
        response = supabase.table('categories').select('*').limit(1).execute()
        print("Supabase connection successful!")
        return True
    except Exception as e:
        print(f"Supabase connection failed: {e}")
        return False


if __name__ == "__main__":
    test_connection()
