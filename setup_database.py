#!/usr/bin/env python3
"""
Database setup script for Supabase.
Run this to create the initial tables and seed data.
"""
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv('.env.local')

SUPABASE_URL = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('NEXT_PUBLIC_SUPABASE_ANON_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def create_tables():
    """Create the core tables."""
    print("Creating tables...")

    # Create categories table
    try:
        supabase.table('categories').insert([
            {"name": "Local News", "description": "News relevant to Suffolk County"},
            {"name": "News for the Disabled", "description": "News and resources for visually impaired"},
            {"name": "Weather", "description": "Weather updates for Suffolk County"},
        ]).execute()
        print("Categories seeded successfully!")
    except Exception as e:
        print(f"Categories might already exist: {e}")


def check_tables():
    """Check if tables exist and show current data."""
    print("\nChecking categories table:")
    try:
        result = supabase.table('categories').select('*').execute()
        print(f"Categories: {result.data}")
    except Exception as e:
        print(f"Error: {e}")

    print("\nChecking articles table count:")
    try:
        result = supabase.table('articles').select('*', count='exact').execute()
        print(f"Total articles: {len(result.data)}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("=== Be My Access - Database Setup ===\n")
    check_tables()
    print("\nRunning setup...")
    create_tables()
    print("\nSetup complete!")
    check_tables()
