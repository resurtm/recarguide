from django.contrib.auth.models import User
from django.db import models

from recarguide.cars.models import Car


class PackagePlan(models.Model):
    name = models.CharField(max_length=50, default='')
    slug = models.SlugField(max_length=50, default='')

    price = models.PositiveIntegerField(default=0)
    max_listings = models.PositiveSmallIntegerField(default=0)
    max_photos = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return '{name}, {price}'.format(name=self.name, price=self.price)


class SellProcess(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None)
    car = models.ForeignKey(Car, on_delete=models.PROTECT, null=True,
                            default=None)
