from django.contrib import admin

# Register your models here.
from .models import Booking, Event

admin.site.register(Booking)
admin.site.register(Event)
