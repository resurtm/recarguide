from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generates testing users data'

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, *args, **options):
        result = input('Old data will be completely removed, '
                       'are you sure you want to do this [y/yes or n/no]: ')
        result = result.lower()
        if result != 'y' and result != 'yes':
            self.stdout.write(self.style.SUCCESS('Did nothing'))
            return

        self.stdout.write('Generating testing users data...')

        # tbd

        self.stdout.write(self.style.SUCCESS('Done!'))
