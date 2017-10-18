from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.utils.text import slugify

from recarguide.common.tools import boto3_client


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
    mileage = models.PositiveIntegerField(default=0)

    description = models.TextField(max_length=10000, default='')

    def __str__(self):
        return '{name} {slug}'.format(name=self.name, slug=self.slug)


class Photo(models.Model):
    sell_process = models.ForeignKey('sale.SellProcess',
                                     on_delete=models.PROTECT, default=None)
    car = models.ForeignKey('Car', on_delete=models.PROTECT, null=True,
                            default=None)

    ready = models.BooleanField(default=False)
    uid = models.CharField(max_length=16)
    filename = models.CharField(max_length=250)
    filedata = models.TextField(null=True, default=None)

    @property
    def s3_key(self):
        return 'cars-photos/{dir}/{fn}'.format(dir=self.uid,
                                               fn=self.filename)


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


def pre_delete_photo_receiver(instance, *args, **kwargs):
    boto3_client().delete_object(Bucket=settings.AWS_S3_BUCKET_NAME,
                                 Key=instance.s3_key)


pre_save.connect(pre_save_category_receiver, sender=Category)
pre_save.connect(pre_save_make_receiver, sender=Make)
pre_save.connect(pre_save_model_receiver, sender=Model)
pre_save.connect(pre_save_car_receiver, sender=Car)
pre_delete.connect(pre_delete_photo_receiver, sender=Photo)
