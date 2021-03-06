# Generated by Django 3.0.8 on 2020-08-12 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('file', models.ImageField(upload_to='')),
                ('caption', models.CharField(max_length=140)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=250)),
                ('price', models.IntegerField(help_text='won per night')),
                ('lat', models.DecimalField(decimal_places=6, max_digits=10)),
                ('lng', models.DecimalField(decimal_places=6, max_digits=10)),
                ('check_in', models.TimeField(default='00:00:00')),
                ('check_out', models.TimeField(default='00:00:00')),
                ('instant_book', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
    ]
