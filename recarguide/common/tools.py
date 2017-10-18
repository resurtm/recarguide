import boto3
import stripe
from django.conf import settings


def ensure_stripe_api_key():
    stripe.api_key = settings.STRIPE['SECRET_KEY']


def boto3_client():
    return boto3.client(
        's3',
        aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
