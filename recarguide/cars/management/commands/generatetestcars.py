import csv
import os

from django.core.management.base import BaseCommand
from django.db import connection

from recarguide.cars.models import Category, Make, Model, Car, Photo
from recarguide.sale.models import SellProcess, Contact


class Command(BaseCommand):
    help = 'Generates testing cars data'

    __CATEGORIES = [
        ('Sedan', []),
        ('SUV', []),
        ('Hatchback', []),
        ('Category #1', ['Sub-Category #1', 'Sub-Category #2']),
        ('Parent Cat 1', ['Child Cat 2', 'Child Cat 2', 'Child Cat 3']),
    ]

    __CARS = [
        ('Toyota', 'Camry XV30', 'Sedan', 15000, 2006),
        ('Toyota', 'Camry XV30', 'Sedan', 15500, 2007),
        ('Toyota', 'Camry XV30', 'Sedan', 7950, 1999),
        ('Toyota', 'Camry XV40', 'Sedan', 19900, 2009),
        ('Toyota', 'Camry XV40', 'SUV', 21900, 2010),
        ('Toyota', 'Land Cruiser 100', 'Sub-Category #1', 9885, 2001),
        ('Toyota', 'Land Cruiser 100', 'Child Cat 2', 14400, 2006),
        ('Nissan', 'Patrol 260', 'Child Cat 2', 16600, 2007),
    ]

    def __init__(self):
        super(Command, self).__init__()

        self.__categories = {}
        self.__makes = {}
        self.__models = {}

    def handle(self, *args, **options):
        result = input('Old data will be completely removed, '
                       'are you sure you want to do this [y/yes or n/no]: ')
        result = result.lower()
        if result != 'y' and result != 'yes':
            self.stdout.write(self.style.SUCCESS('Did nothing'))
            return

        self.stdout.write('Generating testing cars data...')

        self.__remove_old_data()
        self.__reset_sequences()

        self.__generate_categories()
        self.__generate_makes()
        self.__generate_models()
        # self.__generate_cars()

        self.stdout.write(self.style.SUCCESS('Done!'))

    def __remove_old_data(self):
        Photo.objects.all().delete()
        Contact.objects.all().delete()
        SellProcess.objects.all().delete()
        Car.objects.all().delete()

        Category.objects.all().delete()
        Model.objects.all().delete()
        Make.objects.all().delete()

    def __reset_sequences(self):
        if connection.vendor == 'postgresql':
            with connection.cursor() as cursor:
                cursor.execute('ALTER SEQUENCE cars_car_id_seq RESTART')
                cursor.execute('ALTER SEQUENCE cars_category_id_seq RESTART')
                cursor.execute('ALTER SEQUENCE cars_make_id_seq RESTART')
                cursor.execute('ALTER SEQUENCE cars_model_id_seq RESTART')

    def __generate_categories(self):
        for name, children in self.__CATEGORIES:
            parent = Category(name=name)
            parent.save()
            self.__categories[name] = parent

            for child_name in children:
                child = Category(name=child_name, parent=parent)
                child.save()
                self.__categories[child_name] = child

    def __generate_makes(self):
        file_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(file_path, 'data', 'makes.csv')
        with open(file_path) as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] == 'name':
                    continue
                make = Make(name=row[0], website=row[1], facebook=row[2],
                            twitter=row[3], youtube=row[4], instagram=row[7],
                            in_since=self.__intconv(row[5]),
                            out_since=self.__intconv(row[6]))
                make.save()
                self.__makes[make.name] = make

    def __generate_models(self):
        file_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(file_path, 'data', 'models.csv')
        with open(file_path) as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row[0] == 'make_name':
                    continue
                mdl = Model(name=row[1], make=self.__makes[row[0]])
                mdl.save()
                self.__models[mdl.name] = mdl

    def __generate_cars(self):
        for make, mdl, category, price, year in self.__CARS:
            assert make in self.__makes
            assert mdl in self.__models
            assert category in self.__categories

            car = Car(make=self.__makes[make],
                      model=self.__models[mdl],
                      category=self.__categories[category],
                      price=price,
                      year=year)
            car.save()

    def __intconv(self, val):
        try:
            res = int(val)
        except ValueError:
            res = 0
        return res
