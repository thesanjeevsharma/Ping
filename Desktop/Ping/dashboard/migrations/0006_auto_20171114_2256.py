# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-14 17:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20171114_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
