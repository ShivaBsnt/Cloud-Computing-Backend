from decouple import config
from supabase import create_client

supabase = create_client(
    config('SUPABASE_URL'),
    config('SUPABASE_SERVICE_KEY'),
)