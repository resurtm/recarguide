import os
from base64 import standard_b64decode
from io import BytesIO

from PIL import Image, ImageOps
from celery import shared_task
from django.conf import settings

from recarguide.cars.models import Photo
from recarguide.common.tools import boto3

_process_photo_exts = {
    '.jpg': 'JPEG',
    '.jpeg': 'JPEG',
    '.gif': 'GIF',
    '.png': 'PNG',
}


@shared_task
def process_photo(photo_id):
    photo = Photo.objects.get(pk=photo_id)
    photo_data = standard_b64decode(photo.filedata)
    boto3().put_object(Bucket=settings.AWS_S3_BUCKET_NAME, Body=photo_data,
                       Key=photo.storage_key)

    image_file = BytesIO()
    image_file.write(photo_data)
    image = Image.open(image_file)
    image = ImageOps.fit(image, (150, 150), Image.ANTIALIAS)

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

    photo.ready = True
    photo.filedata = None
    photo.save()

    return 'Photo done: {}, {}, {}'.format(photo.id, photo.uid, photo.filename)
