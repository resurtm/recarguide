import base64

from celery import shared_task
from django.conf import settings

from recarguide.cars.models import Photo
from recarguide.common.tools import boto3_client


@shared_task
def process_photo(photo_id):
    photo = Photo.objects.get(pk=photo_id)

    body = base64.standard_b64decode(photo.filedata)
    key = 'cars-photos/{dir}/{filename}'.format(dir=photo.uid,
                                                filename=photo.filename)
    boto3_client().put_object(Bucket=settings.AWS_S3_BUCKET_NAME,
                              Body=body,
                              Key=key)

    photo.ready = True
    photo.filedata = None
    photo.save()

    return 'Photo done: {id}, {uid}, {filename}'.format(id=photo.id,
                                                        uid=photo.uid,
                                                        filename=photo.filename)
