# Generated by Django 2.1 on 2018-10-21 07:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=120)),
                ('price', models.DecimalField(decimal_places=3, max_digits=6)),
                ('available_tickets', models.IntegerField()),
                ('date', models.DateField()),
                ('starting_time', models.TimeField()),
                ('logo', models.ImageField(blank=True, null=True, upload_to='event_logos')),
                ('event_type', models.CharField(choices=[('cars gathering', 'Cars Gathering'), ('party', 'Party'), ('concert', 'Concert'), ('conference', 'Conference'), ('expo', 'Expo'), ('business', 'Business'), ('year end functions', 'Year End Functions'), ('seminars', 'Seminars'), ('product launches', 'Product Launches'), ('team building events', 'Team Building Events'), ('golf event', 'Golf Event'), ('vip event', 'Vip Event'), ('award ceremonies', 'Award Ceremonies')], default='cars gathering', max_length=2)),
                ('owner', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]