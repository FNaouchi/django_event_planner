# Generated by Django 2.1 on 2018-10-22 05:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_booking_seats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='seats',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(200), django.core.validators.MinValueValidator(1)]),
        ),
    ]
