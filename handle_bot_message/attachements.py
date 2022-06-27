import os
from typing import Tuple

from telegram import File, PhotoSize

from aws import get_s3_client
from localization import file_too_large_message_id
from telegram_bot import get_bot


class AttachmentException(Exception):
    pass


def upload_attachment(attachment: PhotoSize) -> Tuple[str, str]:
    if isinstance(attachment, list):
        attachment = attachment[-1]

    if attachment.file_size > 10 * 1024 * 1024:
        raise AttachmentException(file_too_large_message_id)

    file = get_bot().get_file(attachment.file_id)
    file_name = get_original_file_name(file)
    _, suffix = os.path.splitext(file_name)

    unique_file_name = f"{attachment.file_unique_id}{suffix}"

    base_url = os.environ.get('AWS_S3_BOT_UPLOADS_BASE_URL')
    url = f"{base_url}/{unique_file_name}"

    file_path = local_tmp_download(file, unique_file_name)

    # Upload with public read access
    get_s3_client().upload_file(
        file_path,
        'donnation-tracker-bot-upploads',
        unique_file_name,
        ExtraArgs={'ACL': 'public-read'})

    return file_name, url


def get_original_file_name(file: File) -> str:
    return os.path.basename(file.file_path)


def local_tmp_download(file: File, unique_file_name: str) -> str:
    tmp_dir = '/tmp' if os.path.exists('/tmp') else '.'
    file_path = f"{tmp_dir}/{unique_file_name}"
    file.download(file_path)
    return file_path
