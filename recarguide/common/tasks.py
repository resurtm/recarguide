from celery import shared_task

from recarguide.cars.models import Photo


@shared_task
def process_photo(photo_id):
    photo = Photo.objects.get(pk=photo_id)

    return 'Photo done: {id} {uid} {filename}'.format(id=photo.id,
                                                      uid=photo.uid,
                                                      filename=photo.filename)
