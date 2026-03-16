import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Type definitions based on the database schema
export interface Category {
  id: number;
  name: string;
  description?: string;
}

export interface Article {
  id: number;
  title: string;
  content: string;
  summary?: string;
  source_url?: string;
  category_id: number;
  source_name: string;
  published_at: string;
  crawled_at: string;
  dedup_hash?: string;
  is_active: boolean;
  category?: Category;
}

export interface PaginationParams {
  page: number;
  limit: number;
  offset: number;
}
