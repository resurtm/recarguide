from django.core.management.base import BaseCommand
from django.db import connection

from recarguide.sale.models import PackagePlan


class Command(BaseCommand):
    help = 'Generates testing package plans data'

    __PACKAGE_PLANS = [
        ('Starter Kit', 7, 10, 6, 3, False,
         'Initial starter kit for your listing'),
        ('Medium Plan', 15, 20, 12, 1, False,
         'Choose this if you want slightly better options'),
        ('Maximum', 20, 35, 30, 2, True,
         'The best possible options and features!'),
    ]

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, *args, **options):
        result = input('Old data will be completely removed, '
                       'are you sure you want to do this [y/yes or n/no]: ')
        result = result.lower()
        if result != 'y' and result != 'yes':
            self.stdout.write(self.style.SUCCESS('Did nothing'))
            return

        self.stdout.write('Generating testing package plans data...')

        self.__remove_old_data()
        self.__generate_new_data()

        self.stdout.write(self.style.SUCCESS('Done!'))

    def __remove_old_data(self):
        PackagePlan.objects.all().delete()
        if connection.vendor == 'postgresql':
            with connection.cursor() as cursor:
                cursor.execute('ALTER SEQUENCE sale_packageplan_id_seq RESTART')

    def __generate_new_data(self):
        for plan in self.__PACKAGE_PLANS:
            plan = PackagePlan(name=plan[0],
                               price=plan[1],
                               featured_days=plan[2],
                               max_photos=plan[3],
                               order=plan[4],
                               primary=plan[5],
                               description=plan[6])
            plan.save()
