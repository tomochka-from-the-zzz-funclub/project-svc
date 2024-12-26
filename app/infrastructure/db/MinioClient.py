import boto3
from botocore.exceptions import NoCredentialsError
from fastapi.responses import StreamingResponse
from io import BytesIO

from app.infrastructure.db.Settings import settings


def get_s3_client():
    """Создает и возвращает клиента S3."""
    return boto3.client(
        's3',
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        region_name=settings.S3_REGION_NAME
    )

def get_video_from_s3(bucket_name: str, file_name: str):
    """Получает видеофайл из S3."""
    s3_client = get_s3_client()
    
    try:
        file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_name)
        return file_obj['Body']
    except NoCredentialsError:
        raise ValueError("Credentials for S3 not found")
    except Exception as e:
        raise ValueError(f"Error retrieving video from S3: {e}")