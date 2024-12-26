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


def upload_to_s3(file_path, bucket_name, object_name):
    """
    Загружает файл в S3 (или MinIO) в указанный бакет и с указанным именем объекта.

    :param file_path: Путь к локальному файлу, который нужно загрузить.
    :param bucket_name: Название бакета в S3.
    :param object_name: Имя объекта (файла) в S3.
    """
    try:
        s3 = get_s3_client()

        if s3 is None:
            print("S3 client initialization failed.")
            return

        # Загружаем файл в S3
        s3.upload_file(file_path, bucket_name, object_name)
        print(f"File uploaded successfully to {bucket_name}/{object_name}")
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except NoCredentialsError:
        print("Credentials not available.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

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