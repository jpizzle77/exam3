# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-18 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0002_user_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateTimeField(),
        ),
    ]
