from django.core.management.base import BaseCommand
from django.db import connection

from recarguide.cars.models import Category, Make, Model, Car


class Command(BaseCommand):
    help = 'Generates testing cars data'

    __CATEGORIES = [
        ('Sedan', []),
        ('SUV', []),
        ('Hatchback', []),
        ('Category #1', ['Sub-Category #1', 'Sub-Category #2']),
        ('Parent Cat 1', ['Child Cat 2', 'Child Cat 2', 'Child Cat 3']),
    ]

    __MAKES = ['Toyota', 'Nissan', 'Mazda', 'Mercedes', 'Audi', 'Skoda',
               'Chevrolet', 'BMW', 'Fiat', 'Peugeot']

    __MODELS = [
        ('Toyota', 'Land Cruiser 100'),
        ('Toyota', 'Land Cruiser 120'),
        ('Toyota', 'Land Cruiser 150'),
        ('Toyota', 'Land Cruiser 200'),
        ('Nissan', 'Patrol 160'),
        ('Nissan', 'Patrol 260'),
        ('Toyota', 'Camry XV30'),
        ('Toyota', 'Camry XV40'),
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
        self.__generate_cars()

        self.stdout.write(self.style.SUCCESS('Done!'))

    def __remove_old_data(self):
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
        for make_name in self.__MAKES:
            make = Make(name=make_name)
            make.save()
            self.__makes[make_name] = make

    def __generate_models(self):
        for make_name, model_name in self.__MODELS:
            assert make_name in self.__makes

            mdl = Model(name=model_name, make=self.__makes[make_name])
            mdl.save()
            self.__models[model_name] = mdl

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
