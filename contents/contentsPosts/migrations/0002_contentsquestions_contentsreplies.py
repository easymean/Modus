# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2020-07-23 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentsPosts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentsQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='ContentsReplies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.CharField(max_length=1000)),
            ],
        ),
    ]