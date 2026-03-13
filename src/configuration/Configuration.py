# Environment Setting
from dotenv import load_dotenv
import os 

# DB
load_dotenv()
SupabaseUrl = os.getenv("SUPABASE_URL")
SupabaseKey = os.getenv("SUPABASE_KEY")