import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv('.env.local')  # Use the same env as Next.js

SUPABASE_URL = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('NEXT_PUBLIC_SUPABASE_ANON_KEY')

print(f"URL: {SUPABASE_URL}")
print(f"Key: {SUPABASE_ANON_KEY[:20]}...")

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

try:
    response = supabase.table('categories').select('*').limit(1).execute()
    print("SUPABASE CONNECTION SUCCESSFUL!")
    print(f"Response: {response.data}")
except Exception as e:
    print(f"SUPABASE CONNECTION FAILED: {e}")
