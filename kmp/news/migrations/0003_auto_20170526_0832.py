# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-26 08:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20170526_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyphrase',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='keyphrases', to='news.Article'),
        ),
    ]