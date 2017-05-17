# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-11 00:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_auto_20170510_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='news.Article'),
        ),
    ]
