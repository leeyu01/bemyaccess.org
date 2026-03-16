from supabase_client import supabase

def test_connection():
    """Test Supabase connection."""
    try:
        response = supabase.table('categories').select('*').limit(1).execute()
        print("✓ Supabase connection successful!")
        print(f"Response: {response.data}")
        return True
    except Exception as e:
        print(f"✗ Supabase connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
