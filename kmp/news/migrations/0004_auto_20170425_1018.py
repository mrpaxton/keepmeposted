# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-25 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20170425_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='published',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
