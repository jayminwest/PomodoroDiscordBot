import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

# Geting discord token: 
TOKEN = os.getenv('DISCORD_TOKEN')

# Supabase Setup:
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_SECRET = os.getenv('SUPABASE_SECRET')

# Create a Supabase client:
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)