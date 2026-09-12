import uuid

from .supabase import supabase


BUCKET_NAME = "media"


def upload_file(file, folder="uploads"):
    extension = file.name.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    path = f"{folder}/{filename}"

    supabase.storage.from_(BUCKET_NAME).upload(
        path,
        file.read(),
        {
            "content-type": file.content_type,
        },
    )

    return path