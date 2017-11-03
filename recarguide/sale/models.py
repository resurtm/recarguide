from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db import transaction
from django.db.models.signals import pre_save
from django.utils.text import slugify

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

    @property
    def stripe_price(self):
        return self.price * 100


class SellProcess(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT,
                             default=None)
    car = models.ForeignKey('cars.Car', on_delete=models.PROTECT, null=True,
                            default=None)

    step = models.PositiveSmallIntegerField(default=1)
    package_plan = models.ForeignKey('PackagePlan', on_delete=models.PROTECT,
                                     null=True, default=None)

    finished = models.BooleanField(default=False)
    payment = JSONField(default=None, null=True)

    def __str__(self):
        return 'User ID: {uid}, car ID: {cid}'.format(uid=self.user_id,
                                                      cid=self.car_id)

    def publish(self):
        with transaction.atomic():
            for photo in self.photos.all():
                photo.car_id = self.car.id
                photo.save()
            self.finished = True
            self.save()


class Contact(models.Model):
    sell_process = models.ForeignKey('SellProcess', on_delete=models.PROTECT,
                                     default=None, related_name='contacts')

    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')

    address = models.CharField(max_length=75, default='')
    address2 = models.CharField(max_length=75, default='')
    city = models.CharField(max_length=75, default='')
    country = models.CharField(max_length=2, default='')
    zip = models.CharField(max_length=10, default='')
    phone = models.CharField(max_length=25, default='')

    contact_method = models.CharField(max_length=1, default='')

    def __str__(self):
        return '{fn} {ln}'.format(fn=self.first_name,
                                  ln=self.last_name)


def pre_save_package_plan_receiver(instance, *args, **kwargs):
    instance.slug = slugify(instance.name)


pre_save.connect(pre_save_package_plan_receiver, sender=PackagePlan)
