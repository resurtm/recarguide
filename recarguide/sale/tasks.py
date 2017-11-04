from base64 import standard_b64decode

from celery import shared_task

from recarguide.cars.models import Photo
from recarguide.cars.tools import generate_thumbnails


@shared_task
def process_photo(photo_id):
    photo = Photo.objects.get(pk=photo_id)
    generate_thumbnails(photo, standard_b64decode(photo.filedata))
    photo.ready = True
    photo.filedata = None
    photo.save()

    return 'Photo done: {}, {}, {}'.format(photo.id, photo.uid, photo.filename)
