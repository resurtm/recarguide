from django.core.management.base import BaseCommand

from cars.models import Car
from cars.search.elastic import reindex_car
from common.tools import batched_iterator


class Command(BaseCommand):
    help = 'Reindices all the cars'

    BATCH_SIZE = 50

    def handle(self, *args, **options):
        self.stdout.write('Reindexing cars...')
        for car in batched_iterator(Car.objects.order_by('id'),
                                    self.BATCH_SIZE):
            reindex_car(car)
        self.stdout.write(self.style.SUCCESS('Done!'))
