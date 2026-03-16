### **System Requirements: Backend & Database Development**

This document outlines the technical specifications and mandatory tasks for the Backend Developer. The objective is to build a robust, accessible, and cost-effective API and database layer for the **Suffolk County Accessible News** portal.

#### **1. Technical Stack & Hosting**
*   **Framework**: **Next.js (TypeScript)** using App Router for API routes.
*   **Database**: **Supabase (PostgreSQL)**.
*   **Hosting**: **Vercel**.
*   **External Integration**: Weather data must be fetched from **open-meteo.com**.

#### **2. Database Schema (`articles` table)**
The database must support AI-generated summaries and semantic de-duplication. The schema should include:
*   **`id`**: UUID, Primary Key.
*   **`title`**: String.
*   **`content`**: Text (Full raw article).
*   **`summary`**: Text (**AI-generated summary**) stored directly in the article row.
*   **`source_name`**: String (e.g., "Newsday," "Patch Suffolk").
*   **`url`**: String (Link to the original source).
*   **`is_active`**: Boolean (Default: `true`). Used to "disable" articles older than 90 days rather than hard-deleting them.
*   **`created_at`**: Timestamp.
*   **`search_vector`**: **tsvector** for PostgreSQL **full-text search**.

##### **Database Schema Specification**

```sql
-- 1. Create the Categories Table
-- This supports the three mandatory categories identified in the MVP.
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Create the Articles Table
-- This table is designed for semantic de-duplication and a 90-day retention policy.
CREATE TABLE articles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    summary TEXT, -- Stores AI-generated summaries directly
    source_name TEXT NOT NULL, -- Replaces the author field
    url TEXT UNIQUE, -- Ensures basic URL-level de-duplication
    is_active BOOLEAN DEFAULT TRUE, -- Used for the 90-day content retention policy
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- search_vector: For PostgreSQL full-text search (tsvector)
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english', title || ' ' || summary)
    ) STORED
);

-- 3. Create a GIN Index for Search Performance
-- Essential for providing fast keyword search results as required for the MVP.
CREATE INDEX idx_articles_search_vector ON articles USING GIN (search_vector);

-- 4. Insert Initial Mandatory Categories
INSERT INTO categories (name) VALUES 
('Local News'), 
('News for the Disabled'), 
('Weather');
```

### **Key Implementation Details for the Developer**
*   **De-duplication**: The `url` field is set to `UNIQUE` to prevent the same link from being saved twice. For semantic de-duplication (matching similar content from different URLs), your Python crawler should compare its new AI summary against the existing entries in the `summary` column before inserting.
*   **90-Day Retention**: The `is_active` boolean allows you to "disable" articles older than 90 days. This makes it easy to filter them out of the public `GET /api/articles` endpoint while keeping the data available for admin audit or re-activation.
*   **Full-Text Search**: The `search_vector` is a "generated column" that automatically combines the `title` and `summary` into a searchable format. This ensures that when a user searches for a keyword, the system checks both the headline and the AI-generated gist.


#### **3. API Endpoint Specifications**
All endpoints must use **offset-based pagination**.

**Public Endpoints:**
*   `GET /api/articles`: Returns only active articles (`is_active: true`).
*   `GET /api/articles/[id]`: Returns full details for a single article.
*   `GET /api/categories`: Returns the three mandatory categories: **Local News**, **News for the Disabled**, and **Weather**.
*   `GET /api/articles?category=[id]`: Filters articles by category.
*   **Keyword Search**: `GET /api/articles?search=[query]` using PostgreSQL full-text search.
*   **Weather**: `GET /api/weather` to fetch real-time Suffolk County data from Open-Meteo.

**Admin Endpoints (Protected):**
*   **Security**: Use a **fixed API key in the request header** for authentication.
*   `GET /api/articles/all`: Lists all articles, including inactive ones.
*   `POST /api/articles`: Create a new article (used by the Python crawler).
*   `PUT /api/articles/[id]`: Update existing article details.
*   **Status Toggle**: `PATCH /api/articles/[id]/toggle-active` to manually flip the `is_active` status.
*   `DELETE /api/articles/[id]`: Hard delete (restricted use).

#### **4. Core Logic & Constraints**
*   **No-Login Policy**: There are **no user accounts**. Do not build user tables or authentication for end-users. Personalization (like bookmarks) will be handled via **browser cookies** on the frontend.
*   **Retention Policy**: Content must be retained for **90 days**. After this period, articles should be marked `is_active: false`. This threshold must be **configurable** (e.g., via a config file or environment variable).
*   **Language**: The system is **strictly English only** [from project policy].
*   **Accessibility Support**: Ensure all API responses include semantic data (e.g., proper category names and detailed descriptions) to support the frontend's **WCAG 2.2 AAA** requirements.

#### **5. Implementation Tasks (What to do)**
1.  **Initialize Supabase Project**: Set up the PostgreSQL instance and the `articles` table with the `tsvector` index.
2.  **Develop Next.js API Routes**: Build the CRUD and filtering logic using TypeScript.
3.  **Implement Retention Script**: Create a cron-ready function (or Supabase Edge Function) to automatically toggle `is_active` for articles older than 90 days.
4.  **Security Integration**: Implement a middleware or header check for the fixed admin API key.
5.  **Weather Proxy**: Write the proxy logic for the Open-Meteo API to ensure the frontend doesn't need to handle external API keys or complex formatting.