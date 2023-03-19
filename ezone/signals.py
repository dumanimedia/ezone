from django.db.models.signals import pre_save
from django.utils.text import slugify
from .models import Category, Product, Brand
from userprofile.models import Userprofile


def category_pre_save(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)


def brand_pre_save(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)


def product_pre_save(sender, instance, *args, **kwargs):
    instance.slug = slugify(instance.title)


def userprofile_pre_save(sender, instance, *args, **kwargs):
    pass  # What you need todo before saving a user in the Database


pre_save.connect(userprofile_pre_save, sender=Userprofile)
pre_save.connect(category_pre_save, sender=Category)
pre_save.connect(product_pre_save, sender=Product)
pre_save.connect(brand_pre_save, sender=Brand)
