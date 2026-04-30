from django.contrib import admin
from .models import User, Booking, ParkingZone, ParkingSpot

# Register your models here.
admin.site.register(Booking)
admin.site.register(ParkingZone)
admin.site.register(ParkingSpot)