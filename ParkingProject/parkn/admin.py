from datetime import datetime, timedelta

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Booking, ParkingSpot, ParkingZone


# Show a zone's bookings inside the admin page.
class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    fields = ("parkingSpot", "date", "startTime", "duration")


# Show parking spots while editing a zone.
class ParkingSpotInline(admin.TabularInline):
    model = ParkingSpot
    extra = 0
    fields = ("xCoord", "yCoord")


@admin.register(ParkingZone)
class ParkingZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "totalSpots", "spot_count", "booking_count")
    search_fields = ("name", "location")
    list_filter = ("location",)
    ordering = ("name",)
    inlines = [ParkingSpotInline]

    @admin.display(description="Spots")
    def spot_count(self, obj):
        # Count how many spots are in this zone.
        return obj.parkingSpots.count()

    @admin.display(description="Bookings")
    def booking_count(self, obj):
        # Count all bookings that belong to spots in this zone.
        return Booking.objects.filter(parkingSpot__zone=obj).count()


@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ("id", "zone", "xCoord", "yCoord", "booking_count")
    search_fields = ("zone__name", "zone__location", "xCoord", "yCoord")
    list_filter = ("zone",)
    ordering = ("zone__name", "xCoord", "yCoord")
    inlines = [BookingInline]

    @admin.display(description="Bookings")
    def booking_count(self, obj):
        return obj.bookings.count()


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "parkingSpot",
        "date",
        "startTime",
        "duration",
        "ends_at",
    )
    search_fields = (
        "user__username",
        "user__email",
        "parkingSpot__zone__name",
        "parkingSpot__xCoord",
        "parkingSpot__yCoord",
    )
    list_filter = ("date", "parkingSpot__zone", "user")
    date_hierarchy = "date"
    ordering = ("-date", "-startTime")
    raw_id_fields = ("user", "parkingSpot")

    @admin.display(description="Ends at")
    def ends_at(self, obj):
        # Work out the booking end time from start time and duration.
        return (
            datetime.combine(obj.date, obj.startTime) + timedelta(minutes=obj.duration)
        ).time()


# Replace default User admin so we can add booking info.
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "booking_count",
    )
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active", "is_superuser", "groups")
    ordering = ("username",)
    inlines = [BookingInline]

    @admin.display(description="Bookings")
    def booking_count(self, obj):
        return obj.bookings.count()
