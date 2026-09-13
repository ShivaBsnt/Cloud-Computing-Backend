import uuid

from decouple import config
from supabase import create_client

SUPABASE_URL = config('SUPABASE_URL')
SUPABASE_SERVICE_KEY = config('SUPABASE_SERVICE_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

BUCKET_NAME = 'avatars'


def upload_profile_picture(file, user_id):
    
    file_extension = file.name.split('.')[-1]
    file_path = f"user_{user_id}.{file_extension}"

    file_bytes = file.read()

    supabase.storage.from_(BUCKET_NAME).upload(
        file_path,
        file_bytes,
        {
            "content-type": file.content_type,
            "upsert": "true",
        },
    )

    public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_path)
    return public_url