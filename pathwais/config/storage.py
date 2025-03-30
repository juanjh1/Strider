
import boto3
from botocore.config import Config
from .config import R2_ENDPOINT,R2_ACCESS_KEY_ID,R2_SECRET_ACCESS_KEY

s3 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    config=Config(signature_version="s3v4"),
)