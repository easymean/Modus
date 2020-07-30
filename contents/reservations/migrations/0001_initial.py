# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2020-07-23 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_num', models.IntegerField(default=1)),
                ('is_allowed', models.BooleanField(default=False)),
                ('payment_type', models.CharField(choices=[('CD', 'Card'), ('PH', 'Phone'), ('CS', 'Cash')], max_length=2)),
            ],
        ),
    ]
