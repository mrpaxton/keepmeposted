# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-26 02:11
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(max_length=500)),
                ('title', models.CharField(max_length=250, unique=True)),
                ('url', models.CharField(max_length=200)),
                ('url_to_image', models.CharField(max_length=200)),
                ('source', models.CharField(max_length=100)),
                ('published', models.DateTimeField(auto_now=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('FINANCE', 'Finance'), ('GENERAL', 'General'), ('SPORTS', 'Sports'), ('TECHNOLOGY', 'Technology')], default='GENERAL', max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Keyphrase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100, unique=True)),
                ('score', models.DecimalField(decimal_places=5, default=Decimal('0.00000'), max_digits=10)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photos/originals/%Y/%m/')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='news.Article')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, to='news.Category'),
        ),
    ]
