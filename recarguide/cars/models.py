from itertools import chain

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.utils.text import slugify

from recarguide.cars.search.queries import find_popular_makes
from recarguide.common.tools import boto3


class Category(models.Model):
    name = models.CharField(max_length=50, default='')
    slug = models.SlugField(max_length=50, default='')

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True,
                               default=None)

    def __str__(self):
        return self.name


class MakeManager(models.Manager):
    def find_popular_makes(self, count=28):
        res = find_popular_makes(count)
        m1 = self.filter(name__in=res).all()
        m2 = self.exclude(name__in=res).all()[:count - len(res)]
        return list(chain(m1, m2))


class Make(models.Model):
    objects = MakeManager()

    name = models.CharField(max_length=50, default='')
    slug = models.SlugField(max_length=50, default='')

    website = models.CharField(max_length=250, default='')
    facebook = models.CharField(max_length=250, default='')
    twitter = models.CharField(max_length=250, default='')
    youtube = models.CharField(max_length=250, default='')
    instagram = models.CharField(max_length=250, default='')

    in_since = models.PositiveIntegerField(default=0)
    out_since = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Model(models.Model):
    name = models.CharField(max_length=50, default='')
    slug = models.SlugField(max_length=50, default='')

    make = models.ForeignKey('Make', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.name


class Trim(models.Model):
    name = models.CharField(max_length=100, default='')
    slug = models.SlugField(max_length=100, default='')

    make = models.ForeignKey('Make', on_delete=models.CASCADE, default=None)
    model = models.ForeignKey('Model', on_delete=models.CASCADE, default=None)


class CarManager(models.Manager):
    def find_by_id_and_slug(self, id, slug):
        car = self.get(id=id)
        if car.slug != slug:
            raise Car.DoesNotExist()
        return car


class Car(models.Model):
    objects = CarManager()

    name = models.CharField(max_length=250, default='')
    slug = models.SlugField(max_length=250, default='')

    make = models.ForeignKey('Make', on_delete=models.PROTECT, default=None)
    model = models.ForeignKey('Model', on_delete=models.PROTECT, default=None)
    trim = models.ForeignKey('Trim', on_delete=models.PROTECT, default=None,
                             null=True)
    trim_name = models.CharField(max_length=100, default='')
    category = models.ForeignKey('Category', on_delete=models.PROTECT,
                                 default=None)

    price = models.PositiveIntegerField(default=0)
    year = models.PositiveSmallIntegerField(default=0)
    mileage = models.PositiveIntegerField(default=0)

    description = models.TextField(max_length=10000, default='')

    def __str__(self):
        return self.name

    @property
    def full_category_name(self):
        if not self.category.parent_id:
            return self.category.name
        return '{}, {}'.format(self.category.parent.name, self.category.name)


class Photo(models.Model):
    sell_process = models.ForeignKey('sale.SellProcess',
                                     on_delete=models.PROTECT, default=None,
                                     related_name='photos')
    car = models.ForeignKey('Car', on_delete=models.PROTECT, null=True,
                            default=None, related_name='photos')

    ready = models.BooleanField(default=False)
    uid = models.CharField(max_length=16)
    filename = models.CharField(max_length=250)
    filedata = models.TextField(null=True, default=None)

    user = models.ForeignKey('auth.User', on_delete=models.PROTECT,
                             default=None)

    @property
    def storage_key(self):
        return 'cars-photos/{}/{}'.format(self.uid, self.filename)

    @property
    def thumb_storage_key(self):
        return 'cars-photos/{}/thumb_{}'.format(self.uid, self.filename)

    @property
    def url(self):
        tpl = '//s3.{}.amazonaws.com/{}/{}'
        return tpl.format(settings.AWS_S3_REGION_NAME,
                          settings.AWS_S3_BUCKET_NAME, self.storage_key)

    @property
    def thumb_url(self):
        tpl = '//s3.{}.amazonaws.com/{}/{}'
        return tpl.format(settings.AWS_S3_REGION_NAME,
                          settings.AWS_S3_BUCKET_NAME,
                          self.thumb_storage_key)


def pre_save_category_receiver(instance, *args, **kwargs):
    instance.slug = slugify(instance.name)


def pre_save_make_receiver(instance, *args, **kwargs):
    instance.slug = slugify(instance.name)


def pre_save_model_receiver(instance, *args, **kwargs):
    instance.slug = slugify(instance.name)


def pre_save_trim_receiver(instance, *args, **kwargs):
    instance.slug = slugify(instance.name)


def pre_save_car_receiver(instance, *args, **kwargs):
    tpl = '{make} {model} {trim} {year}'
    instance.name = tpl.format(make=instance.make.name,
                               model=instance.model.name,
                               trim=instance.trim_name,
                               year=instance.year)
    instance.slug = slugify(instance.name)


def pre_delete_photo_receiver(instance, *args, **kwargs):
    boto3().delete_object(Bucket=settings.AWS_S3_BUCKET_NAME,
                          Key=instance.storage_key)
    boto3().delete_object(Bucket=settings.AWS_S3_BUCKET_NAME,
                          Key=instance.thumb_storage_key)


pre_save.connect(pre_save_category_receiver, sender=Category)
pre_save.connect(pre_save_make_receiver, sender=Make)
pre_save.connect(pre_save_model_receiver, sender=Model)
pre_save.connect(pre_save_trim_receiver, sender=Trim)
pre_save.connect(pre_save_car_receiver, sender=Car)
pre_delete.connect(pre_delete_photo_receiver, sender=Photo)
