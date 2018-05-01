import random
import os
from django.db import models
from django.db.models.signals import pre_save

from common.utils import unique_slug_generator


# Create your models here.

def get_filename_extension(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_extension(filename)
    final_name = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'product/{0}'.format(final_name)


class ProductQuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(features=True, active=True)


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    image = models.ImageField(upload_to=upload_image_path,
                              null=True,
                              blank=True)
    features = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    objects = ProductManager()

    def get_absolute_url(self):
        return "/products/{slug}/".format(slug=self.slug)

    def __str__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)
