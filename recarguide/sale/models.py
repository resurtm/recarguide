from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

from recarguide.cars.models import Car

CONTACT_METHODS = (
    ('e', 'Email Only'),
    ('p', 'Email & Phone'),
)


class PackagePlan(models.Model):
    name = models.CharField(max_length=50, default='')
    slug = models.SlugField(max_length=50, default='')

    price = models.PositiveIntegerField(default=0)
    featured_days = models.PositiveSmallIntegerField(default=0)
    max_photos = models.PositiveSmallIntegerField(default=0)

    order = models.PositiveSmallIntegerField(default=0)
    primary = models.BooleanField(default=False)
    description = models.CharField(max_length=250, default='')

    def __str__(self):
        return '{name}, {price}'.format(name=self.name, price=self.price)


class SellProcess(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    car = models.ForeignKey(Car, on_delete=models.PROTECT, null=True,
                            default=None)

    step = models.PositiveSmallIntegerField(default=1)
    package_plan = models.ForeignKey('PackagePlan', on_delete=models.PROTECT,
                                     null=True, default=None)


class Contact(models.Model):
    sell_process = models.ForeignKey('SellProcess', on_delete=models.PROTECT,
                                     default=None)

    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')

    address = models.CharField(max_length=75, default='')
    address2 = models.CharField(max_length=75, default='')
    city = models.CharField(max_length=75, default='')
    country = models.CharField(max_length=2, default='')
    phone = models.CharField(max_length=25, default='')

    contact_method = models.CharField(max_length=1, default='')


def pre_save_package_plan_receiver(instance, *args, **kwargs):
    instance.slug = slugify(instance.name)


pre_save.connect(pre_save_package_plan_receiver, sender=PackagePlan)
