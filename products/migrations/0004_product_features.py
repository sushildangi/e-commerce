# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-01 14:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='features',
            field=models.BooleanField(default=False),
        ),
    ]