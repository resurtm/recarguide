import os
from io import BytesIO

from PIL import Image, ImageOps
from botocore.exceptions import ClientError
from django.conf import settings

from common.tools import boto3

_process_photo_exts = {
    '.jpg': 'JPEG',
    '.jpeg': 'JPEG',
    '.gif': 'GIF',
    '.png': 'PNG',
}


def _ensure_original_image_data(photo, data):
    if not data:
        try:
            resp = boto3().get_object(Bucket=settings.AWS_S3_BUCKET_NAME,
                                      Key=photo.storage_key)
        except ClientError:
            raise ValueError('Invalid photo model')
        data = resp['Body'].read()
    else:
        boto3().put_object(Bucket=settings.AWS_S3_BUCKET_NAME, Body=data,
                           Key=photo.storage_key)
    return data


def generate_thumbnails(photo, data=None):
    data = _ensure_original_image_data(photo, data)
    if not data:
        return False

    image_file = BytesIO()
    image_file.write(data)
    image = Image.open(image_file)
    image = ImageOps.fit(image, (225, 225), Image.ANTIALIAS)

    __, ext = os.path.splitext(photo.filename)
    ext = _process_photo_exts.get(ext.lower())
    if not ext:
        raise ValueError('Not supported file type')

    thumb_file = BytesIO()
    image.save(thumb_file, ext)
    thumb_file.seek(0)
    boto3().put_object(Bucket=settings.AWS_S3_BUCKET_NAME,
                       Body=thumb_file.getvalue(), Key=photo.thumb_storage_key)

    image_file.close()
    thumb_file.close()
    return True
