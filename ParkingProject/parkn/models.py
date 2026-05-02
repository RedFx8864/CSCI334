from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your models here.

#Using Django's Default User model which contains:
# username – CharField (max 150, unique)
# password – hashed password (CharField)
# email – EmailField
# first_name – Charfield
# last_name – CharField
# add a user profile link it to User for additional attributes if needed (which is gonna be needed)

class ParkingZone(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    totalSpots = models.IntegerField()

    def __str__(self):
        return self.name

class ParkingSpot(models.Model):
    zone = models.ForeignKey(ParkingZone, on_delete=models.CASCADE, related_name='parkingSpots')
    xCoord = models.IntegerField()
    yCoord = models.IntegerField()    

    @classmethod
    def getAvailableSpots(cls, zone, date, startTime, duration):
        endTime = (datetime.combine(date, startTime) + timedelta(minutes=duration)).time()

        spots = cls.objects.filter(zone=zone)

        availableSpotIds = []

        for spot in spots:
            bookings = spot.bookings.filter(date=date)
            conflict = False
            for booking in bookings:
                bookingEnd = (datetime.combine(date, booking.startTime) + timedelta(minutes=booking.duration)).time()
                if not (endTime <= booking.startTime or startTime >= bookingEnd):
                    conflict = True
                    break

            if not conflict:
                availableSpotIds.append(spot.id)
        return cls.objects.filter(id__in=availableSpotIds)
    
    def __str__(self):
        return f"{self.xCoord},{self.yCoord}"

class Booking(models.Model):
    #id auto generated
    #reference to user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    parkingSpot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    startTime = models.TimeField()
    duration = models.IntegerField()

    #create booking
    @classmethod
    def createBooking(cls, user, parkingSpot, date, startTime, duration):
        booking = cls(user=user, parkingSpot=parkingSpot, date=date, startTime=startTime, duration=duration)
        booking.save()
        return booking

    #update booking
    def updateBooking(self, parkingSpot, date, startTime, duration):
        self.parkingSpot = parkingSpot
        self.date = date
        self.startTime = startTime
        self.duration = duration

    #return booking info for testing 
    def __str__(self):
        return f"Booking ID: {self.id}\nUserID: {self.user.id}\nParkingSpot: {self.parkingSpot}]\nDate: {self.date}\nTime: {self.startTime}\nDuration: {self.duration} minutes"