from django.contrib import admin
from .models import Event, Booking, EventType, Profile, Following

admin.site.register(Event)
admin.site.register(Booking)
admin.site.register(EventType)
admin.site.register(Profile)
admin.site.register(Following)