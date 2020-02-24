# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-12 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='slug',
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(help_text="Slug will be automatically generated from the post's title", unique=True),
        ),
    ]