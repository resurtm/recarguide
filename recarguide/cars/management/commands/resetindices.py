from django.core.management.base import BaseCommand

from recarguide.cars.search.elastic import delete_indices, ensure_indices


class Command(BaseCommand):
    help = 'Resets all the ElasticSearch indices'

    BATCH_SIZE = 50

    def handle(self, *args, **options):
        self.stdout.write('Resetting all the indices...')
        delete_indices()
        ensure_indices()
        self.stdout.write(self.style.SUCCESS('Done!'))
