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
        self.save()

    #cancel booking
    @classmethod
    def cancelBooking(cls, bookingId):
        booking = Booking.objects.get(id=bookingId)
        bookingStart = datetime.combine(booking.date, booking.startTime)
        timeDiff = bookingStart - datetime.now()
        #cant cancel if booking starts in less than 120 mins
        if timeDiff.total_seconds() < 120*60: #link to some kind of admin panel so it cna be configured
            return False
        else:
            booking.delete()
            return True

    #check if booking is active
    @property
    def isActive(self):
        bookingEnd = datetime.combine(
            self.date,
            self.startTime
        ) + timedelta(minutes=self.duration)

        return datetime.now() < bookingEnd

    #return booking info for testing 
    def __str__(self):
        return f"Booking ID: {self.id}\nUserID: {self.user.id}\nParkingSpot: [{self.parkingSpot}]\nDate: {self.date}\nTime: {self.startTime}\nDuration: {self.duration} minutes"
    
class HourAvailability(models.Model):
    timedate = models.DateTimeField()
    unavailabilityPercent = models.IntegerField()

    def __str__(self):
        return f"{self.timedate},{self.unavailabilityPercent}"

    #Create Recorded Timeslots
    @classmethod
    def createHourAvailability(cls, timedate, unavailabilityPercent):
        hourAvail = cls(timedate=timedate, unavailabilityPercent=unavailabilityPercent)
        hourAvail.save()
        return hourAvail

class Recommendation(models.Model):

    def calculateRecommendation(self):
        currentd = datetime.now()
        hourAvailabilities = HourAvailability.objects.all()
        
        if hourAvailabilities:
            print("hour availabilities found")
            datestr = "2025-01-01 00:00:00"
            fcode = "%Y-%m-%d %H:%M:%S"
            rec1 = HourAvailability()
            rec1.timedate = datetime.strptime(datestr, fcode)
            rec1.unavailabilityPercent = 100
            rec2 = HourAvailability()
            rec2.timedate = datetime.strptime(datestr, fcode)
            rec2.unavailabilityPercent = 100
            rec3 = HourAvailability()
            rec3.timedate = datetime.strptime(datestr, fcode)
            rec3.unavailabilityPercent = 100

            j = 0

            print("individual looping precheck...")
            for hourAvail in hourAvailabilities:
                    if (hourAvail.timedate.month == currentd.month) & (hourAvail.timedate.day == currentd.day):
                        if (hourAvail.timedate.time() > currentd.time()) & (hourAvail.timedate.weekday() == currentd.weekday() -1):
                            print("date and week check success")
                            if hourAvail.unavailabilityPercent < rec1.unavailabilityPercent:
                                print("spot 1 check success")
                                rec1.unavailabilityPercent = hourAvail.unavailabilityPercent
                                rec1.timedate = hourAvail.timedate
                                print("spot 1 store success")
                            elif hourAvail.unavailabilityPercent < rec2.unavailabilityPercent:
                                print("spot 2 check success")
                                rec2.unavailabilityPercent = hourAvail.unavailabilityPercent
                                rec2.timedate = hourAvail.timedate
                                print("spot 2 store success")
                            elif hourAvail.unavailabilityPercent < rec3.unavailabilityPercent:
                                print("spot 3 check success")
                                rec3.unavailabilityPercent = hourAvail.unavailabilityPercent
                                rec3.timedate = hourAvail.timedate
                                print("spot 3 store success")

            set = [rec1, rec2, rec3]
            data = {}
            i=0
            while i<3:
                data.update({"time":set[i].timedate.strftime('%H:%M:%S'), "percent":set[i].unavailabilityPercent})
                i+=1
            return data
        else:
            print("No houravailabilities to reference")