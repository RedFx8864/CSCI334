from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Booking
# Create your views here.

#home page
def indexPage(request):
    users = User.objects.all()
    bookings = Booking.objects.all()
    context = {"users":users, "bookings":bookings}
    return render(request, 'index.html', context)

#Login Page
def loginPage(request):
    return render(request, 'login.html')

#register Account page
def registerPage(request):
    return render(request, 'register.html')