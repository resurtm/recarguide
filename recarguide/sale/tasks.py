import os
from base64 import standard_b64decode
from io import BytesIO

from PIL import Image, ImageOps
from celery import shared_task
from django.conf import settings

from recarguide.cars.models import Photo
from recarguide.common.tools import boto3_client


@shared_task
def process_photo(photo_id):
    photo = Photo.objects.get(pk=photo_id)

    data = standard_b64decode(photo.filedata)
    boto3_client().put_object(Bucket=settings.AWS_S3_BUCKET_NAME,
                              Body=data,
                              Key=photo.s3_key)

    # resize - start
    file = BytesIO()
    file.write(data)
    image = Image.open(file)
    # image.thumbnail((150, 150), Image.ANTIALIAS)
    image = ImageOps.fit(image, (150, 150), Image.ANTIALIAS)

    thumb_name, thumb_extension = os.path.splitext(photo.filename)
    thumb_extension = thumb_extension.lower()

    if thumb_extension in ['.jpg', '.jpeg']:
        FTYPE = 'JPEG'
    elif thumb_extension == '.gif':
        FTYPE = 'GIF'
    elif thumb_extension == '.png':
        FTYPE = 'PNG'
    else:
        raise ValueError

    temp_thumb = BytesIO()
    image.save(temp_thumb, FTYPE)
    temp_thumb.seek(0)
    boto3_client().put_object(Bucket=settings.AWS_S3_BUCKET_NAME,
                              Body=temp_thumb.getvalue(),
                              Key=photo.s3_key_thumb)
    temp_thumb.close()
    # resize - end

    photo.ready = True
    photo.filedata = None
    photo.save()

    return 'Photo done: {id}, {uid}, {filename}'.format(id=photo.id,
                                                        uid=photo.uid,
                                                        filename=photo.filename)
