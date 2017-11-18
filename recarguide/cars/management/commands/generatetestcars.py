import csv
import os

from django.core.management.base import BaseCommand
from django.db import connection

from recarguide.cars.models import Category, Make, Model, Trim, Car, Photo
from recarguide.sale.models import SellProcess, Contact


class Command(BaseCommand):
    help = 'Generates testing cars data'

    CATS = [
        ('Sedan', []),
        ('SUV', []),
        ('Hatchback', []),
        ('Category #1', ['Sub-Category #1', 'Sub-Category #2']),
        ('Parent Cat 1', ['Child Cat 2', 'Child Cat 2', 'Child Cat 3']),
    ]

    CARS = [
        ('Toyota', 'Camry', 'LE', 'Sedan', '', 15000, 2006),
        ('Toyota', 'Camry', 'LE', 'Sedan', '', 15500, 2007),
        ('Toyota', 'Camry', 'LE', 'Sedan', '', 7950, 1999),
        ('Toyota', 'Camry', 'LE All Trac', 'Sedan', '', 19900, 2009),
        ('Toyota', 'Camry', 'LE All Trac', 'SUV', '', 21900, 2010),
        ('Toyota', 'Land Cruiser', 'TX L Package', 'Category #1',
         'Sub-Category #1', 9885, 2001),
        ('Toyota', 'Land Cruiser', 'TX L Package', 'Parent Cat 1',
         'Child Cat 2', 14400, 2006),
        ('Nissan', '200SX', '2 Dr SE-R Coupe', 'Parent Cat 1', 'Child Cat 2',
         16600, 2007),
    ]

    def __init__(self):
        super(Command, self).__init__()

        self.cats = {}
        self.makes = {}
        self.models = {}
        self.trims = {}

    def handle(self, *args, **options):
        result = input('Old data will be completely removed, '
                       'are you sure you want to do this [y/yes or n/no]: ')
        result = result.lower()
        if result != 'y' and result != 'yes':
            self.stdout.write(self.style.SUCCESS('Did nothing'))
            return

        self.stdout.write('Generating testing cars data...')

        self.delete_old_data()
        self.reset_sequences()

        self.gen_cats()
        self.gen_makes()
        self.gen_models()
        self.gen_trims()
        self.gen_cars()

        self.stdout.write(self.style.SUCCESS('Done!'))

    def delete_old_data(self):
        Photo.objects.all().delete()
        Contact.objects.all().delete()
        SellProcess.objects.all().delete()
        Car.objects.all().delete()
        Category.objects.all().delete()
        Trim.objects.all().delete()
        Model.objects.all().delete()
        Make.objects.all().delete()

    def reset_sequences(self):
        if connection.vendor != 'postgresql':
            raise NotImplementedError('Only PostgreSQL DB supported')
        with connection.cursor() as cursor:
            cursor.execute('ALTER SEQUENCE cars_photo_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE sale_contact_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE sale_sellprocess_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE cars_car_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE cars_category_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE cars_trim_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE cars_make_id_seq RESTART')
            cursor.execute('ALTER SEQUENCE cars_model_id_seq RESTART')

    def gen_cats(self):
        for name, children in self.CATS:
            parent = Category(name=name)
            parent.save()
            self.cats[name] = parent
            for name2 in children:
                child = Category(name=name2, parent=parent)
                child.save()
                self.cats['{}-{}'.format(name, name2)] = child

    def read_csv(self, file_name, row_processor):
        file_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(file_path, 'data', file_name)
        with open(file_path) as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                row_processor(row)

    def gen_makes(self):
        self.read_csv('makes.csv', self.gen_make)

    def gen_make(self, row):
        if row[0] == 'name':
            return
        m = Make(name=row[0], website=row[1], facebook=row[2], twitter=row[3],
                 youtube=row[4], instagram=row[7],
                 in_since=self.intconv(row[5]), out_since=self.intconv(row[6]))
        m.save()
        self.makes[row[0]] = m

    def gen_models(self):
        self.read_csv('models.csv', self.gen_model)

    def gen_model(self, row):
        if row[0] == 'make_name':
            return
        m = Model(name=row[1], make=self.makes[row[0]])
        m.save()
        self.models['{}-{}'.format(row[0], row[1])] = m

    def gen_trims(self):
        self.read_csv('trims.csv', self.gen_trim)

    def gen_trim(self, row):
        if row[0] == 'make_name':
            return
        m = Trim(name=row[2], make=self.makes[row[0]],
                 model=self.models['{}-{}'.format(row[0], row[1])])
        m.save()
        self.trims['{}-{}-{}'.format(row[0], row[1], row[2])] = m

    def gen_cars(self):
        for ma, mo, tr, ca, su, pr, ye in self.CARS:
            cat = self.cats['{}-{}'.format(ca, su)] if su else self.cats[ca]
            m = Car(make=self.makes[ma],
                    model=self.models['{}-{}'.format(ma, mo)],
                    trim=self.trims['{}-{}-{}'.format(ma, mo, tr)],
                    category=cat,
                    price=pr,
                    year=ye)
            m.save()

    def intconv(self, val):
        try:
            res = int(val)
        except ValueError:
            res = 0
        return res
