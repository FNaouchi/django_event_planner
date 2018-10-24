from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class EventType(models.Model):
    name = models.CharField(max_length=120)
    
    def __str__(self):
        return self.name


class Event(models.Model):
    owner = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField()
    location = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=6, decimal_places=3)
    available_tickets = models.IntegerField()
    date = models.DateField()
    starting_time = models.TimeField()
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='event_logos', null=True, blank=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seats = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.event.name


class Profile(models.Model):
    user = models.OneToOneField(User, default=1, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='event_logos', null=True, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Following(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)