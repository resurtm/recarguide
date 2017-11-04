from django.core.management.base import BaseCommand

from recarguide.cars.models import Photo
from recarguide.cars.tools import generate_thumbnails
from recarguide.common.tools import batched_iterator


class Command(BaseCommand):
    help = 'Regenerates all the thumbnails of photos'

    BATCH_SIZE = 50

    def handle(self, *args, **options):
        result = input('Existing thumbnails will be completely replaced, '
                       'are you sure you want to do this [y/yes or n/no]: ')
        result = result.lower()
        if result != 'y' and result != 'yes':
            self.stdout.write(self.style.SUCCESS('Did nothing'))
            return
        self.stdout.write('Refreshing existing thumbnails...')
        self.__refresh_thumbnails()
        self.stdout.write(self.style.SUCCESS('Done!'))

    def __refresh_thumbnails(self):
        for photo in batched_iterator(Photo.objects.order_by('id'),
                                      self.BATCH_SIZE):
            try:
                generate_thumbnails(photo)
            except ValueError as e:
                self.stdout.write(self.style.WARNING(str(e)))
            self.stdout.write('Photo #{} finished'.format(photo.id))
