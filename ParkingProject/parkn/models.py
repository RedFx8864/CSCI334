from django.db import models

# Create your models here.
class User(models.Model):
    #id auto generated
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    isAdmin = models.BooleanField(default=False)
    
    #create user
    @classmethod
    def createUser(cls, email, password, isAdmin):
        user = cls(password=password, email=email, isAdmin=isAdmin)
        user.save()
        return user

    #return user info (for testing)
    def __str__(self):
        return f"User ID: {self.id} Email: {self.email}"

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