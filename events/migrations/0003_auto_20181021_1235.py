# Generated by Django 2.1 on 2018-10-21 12:35

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_auto_20181021_0929'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Participant',
            new_name='Booking',
        ),
    ]