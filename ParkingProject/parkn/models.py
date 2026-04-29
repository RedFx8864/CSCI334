from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Using Django's Default User model which contains:
# username – CharField (max 150, unique)
# password – hashed password (CharField)
# email – EmailField
# first_name – Charfield
# last_name – CharField
# add a user profile link it to User for additional attributes if needed (which is gonna be needed)

class Booking(models.Model):
    #id auto generated
    #reference to user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    startTime = models.TimeField()
    duration = models.IntegerField()

    #create booking
    @classmethod
    def createBooking(cls, user, date, startTime, duration):
        booking = cls(user=user, date=date, startTime=startTime, duration=duration)
        booking.save()
        return booking

    #return booking info for testing 
    def __str__(self):
        return f"Booking ID: {self.id} for UserID: {self.user.id} on {self.date} at {self.startTime} for {self.duration} minutes"