from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50, default='')
    slug = models.SlugField(max_length=50, default='')

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True,
                               default=None)

    def __str__(self):
        return '{name} {slug}'.format(name=self.name, slug=self.slug)


class Make(models.Model):
    name = models.CharField(max_length=50, default='')
    slug = models.SlugField(max_length=50, default='')

    def __str__(self):
        return '{name} {slug}'.format(name=self.name, slug=self.slug)


class Model(models.Model):
    name = models.CharField(max_length=50, default='')
    slug = models.SlugField(max_length=50, default='')

    make = models.ForeignKey('Make', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return '{name} {slug}'.format(name=self.name, slug=self.slug)


class Car(models.Model):
    name = models.CharField(max_length=250, default='')
    slug = models.SlugField(max_length=250, default='')

    make = models.ForeignKey('Make', on_delete=models.PROTECT, default=None)
    model = models.ForeignKey('Model', on_delete=models.PROTECT, default=None)
    category = models.ForeignKey('Category', on_delete=models.PROTECT,
                                 default=None)

    price = models.PositiveIntegerField(default=0)
    year = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return '{name} {slug}'.format(name=self.name, slug=self.slug)


def pre_save_category_receiver(instance, *args, **kwargs):
    instance.slug = slugify(instance.name)


def pre_save_make_receiver(instance, *args, **kwargs):
    instance.slug = slugify(instance.name)


def pre_save_model_receiver(instance, *args, **kwargs):
    instance.slug = slugify(instance.name)


def pre_save_car_receiver(instance, *args, **kwargs):
    tpl = '{make} {model} {year}'
    instance.name = tpl.format(make=instance.make.name,
                               model=instance.model.name,
                               year=instance.year)
    instance.slug = slugify(instance.name)


pre_save.connect(pre_save_category_receiver, sender=Category)
pre_save.connect(pre_save_make_receiver, sender=Make)
pre_save.connect(pre_save_model_receiver, sender=Model)
pre_save.connect(pre_save_car_receiver, sender=Car)
