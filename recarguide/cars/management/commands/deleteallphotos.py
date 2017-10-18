from django.core.management.base import BaseCommand
from django.db import connection

from recarguide.cars.models import Photo


class Command(BaseCommand):
    help = 'Deletes all the car photos'

    BATCH_SIZE = 5

    def handle(self, *args, **options):
        result = input('Photos will be completely removed, '
                       'are you sure you want to do this [y/yes or n/no]: ')
        result = result.lower()
        if result != 'y' and result != 'yes':
            self.stdout.write(self.style.SUCCESS('Did nothing'))
            return

        self.stdout.write('Deleting photos...')
        self.__delete_photos()
        self.stdout.write(self.style.SUCCESS('Done!'))

    def __delete_photos(self):
        while True:
            for photo in Photo.objects.all()[:self.BATCH_SIZE]:
                photo.delete()
            if not Photo.objects.count():
                break
        with connection.cursor() as cursor:
            cursor.execute('ALTER SEQUENCE cars_photo_id_seq RESTART')
