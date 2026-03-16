import os
from dotenv import load_dotenv

# Load environment variables using absolute path
env_path = os.path.join(os.path.dirname(__file__), '.env.crawler')
load_dotenv(env_path)

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
NEXTJS_API_URL = os.getenv('NEXTJS_API_URL')

# RSS sources from 2-second-meeting.md
RSS_SOURCES = [
    'https://www.helenkeller.org/hksb',
    'https://www.siloinc.org',
    'http://www.vips-li.org',
    'https://visionsvcb.org',
    'https://www.suffolkcountyny.gov/Departments/Disability-Services',
    'https://www.esboces.org',
    'https://www.stonybrook.edu/events',
    'https://calendar.stonybrook.edu',
    'https://healthprofessions.stonybrookmedicine.edu/calendars',
    'https://www.suffolknet.org/events',
]

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 60  # seconds
