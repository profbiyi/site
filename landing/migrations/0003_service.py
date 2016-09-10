# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-10 20:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0002_auto_20160823_0458'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Service Name')),
                ('description', models.TextField(verbose_name='Description')),
            ],
        ),
    ]
