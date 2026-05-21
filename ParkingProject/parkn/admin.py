from datetime import datetime, timedelta

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Booking, ParkingSpot, ParkingZone, Recommendation


# Here I`m showing a user`s bookings while editing a user.
class UserBookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    fields = ("parkingSpot", "date", "startTime", "duration")
    show_change_link = True


# here i am showing a parking spot`s bookings while editing a spot.
class SpotBookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    fields = ("user", "date", "startTime", "duration")
    show_change_link = True


# In this section i am showing parking spots while editing a zone.
class ParkingSpotInline(admin.TabularInline):
    model = ParkingSpot
    extra = 0
    fields = ("xCoord", "yCoord")
    show_change_link = True


@admin.register(ParkingZone)
class ParkingZoneAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "location",
        "totalSpots",
        "spot_count",
        "remaining_spots",
        "booking_count",
    )
    search_fields = ("name", "location")
    list_filter = ("location",)
    ordering = ("name",)
    inlines = [ParkingSpotInline]

    @admin.display(description="Spots")
    def spot_count(self, obj):
        # Counting how many spots are in this zone.
        return obj.parkingSpots.count()

    @admin.display(description="Remaining Spots")
    def remaining_spots(self, obj):
        return obj.totalSpots - obj.parkingSpots.count()

    @admin.display(description="Bookings")
    def booking_count(self, obj):
        # here we need to count all bookings that belong to spots in this zone.
        return Booking.objects.filter(parkingSpot__zone=obj).count()


@admin.register(ParkingSpot)
class ParkingSpotAdmin(admin.ModelAdmin):
    list_display = ("id", "zone", "xCoord", "yCoord", "booking_count")
    search_fields = ("zone__name", "zone__location", "xCoord", "yCoord")
    list_filter = ("zone",)
    ordering = ("zone__name", "xCoord", "yCoord")
    inlines = [SpotBookingInline]
    autocomplete_fields = ("zone",)
    list_select_related = ("zone",)

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
    autocomplete_fields = ("user", "parkingSpot")
    list_select_related = ("user", "parkingSpot", "parkingSpot__zone")
    readonly_fields = ("ends_at",)

    actions = ["cancel_selected_bookings"]

    def cancel_selected_bookings(self, request, queryset):
        """Admin action: cancel selected bookings if they start >= 120 minutes from now."""
        success = 0
        failed = 0
        for booking in queryset:
            if not booking.can_cancel(now=timezone.now()):
                failed += 1
            else:
                booking.delete()
                success += 1
        self.message_user(
            request,
            f"Cancelled {success} booking(s). {failed} booking(s) were within 120 minutes and were not cancelled.",
        )

    cancel_selected_bookings.short_description = (
        "Cancel selected bookings (respect 120-min window)"
    )

    @admin.display(description="Ends at")
    def ends_at(self, obj):
        # Working in the booking end time from start time and duration
        return (
            datetime.combine(obj.date, obj.startTime) + timedelta(minutes=obj.duration)
        ).time()


# Replacing default user admin so we can add booking info
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
    inlines = [UserBookingInline]
    list_select_related = ()

    @admin.display(description="Bookings")
    def booking_count(self, obj):
        return obj.bookings.count()

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "parkingSpot", "zone", "date", "startTime", "score", "reason", "timestamp")
    search_fields = ("user__username", "zone__name")
    list_filter = ("date", "zone")
    ordering = ("-timestamp",)
