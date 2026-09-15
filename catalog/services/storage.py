from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from supabase import create_client


def get_storage_bucket():
    client = create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_SECRET_KEY,
    )

    return client.storage.from_(
        settings.SUPABASE_BUCKET
    )



def upload_public_file(upload_file, folder):
    extension = Path(upload_file.name).suffix.lower()

    unique_name = f"{uuid4().hex}{extension}"
    object_path = f"{folder}/{unique_name}"

    storage_bucket = get_storage_bucket()

    upload_file.seek(0)
    file_content = upload_file.read()

    storage_bucket.upload(
        path=object_path,
        file=file_content,
        file_options={
            "content-type": (
                upload_file.content_type
                or "application/octet-stream"
            ),
            "upsert": "false",
        },
    )

    return storage_bucket.get_public_url(object_path)
