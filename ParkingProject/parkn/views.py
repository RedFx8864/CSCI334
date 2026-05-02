from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User #Django's default model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Booking, ParkingSpot, ParkingZone
from .forms import UserForm, BookingForm, SelectParkingSpotForm
from datetime import datetime

# Create your views here.

#home page
@login_required
def indexPage(request):
    users = User.objects.all()
    bookings = Booking.objects.all()
    context = {'users':users, 'bookings':bookings}
    return render(request, 'index.html', context)

#Login Page
def loginPage(request):
    error = None
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error = 'Invalid credentials'
    return render(request, 'login.html', {'error': error})

@login_required
def logoutPage(request):
    logout(request)
    return redirect('login')

#register Account page
def registerPage(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            #temporary: using email as username
            User.objects.create_user(username=email, password=password)
    else:
        form = UserForm()
    context={'form':form}
    return render(request, 'register.html', context)

@login_required
def createBookingPage(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            #save data so session
            request.session["bookingData"] = {
                "zoneId": form.cleaned_data["zone"].id,
                "date": str(form.cleaned_data["date"]),
                "startTime": str(form.cleaned_data["startTime"]),
                "duration": form.cleaned_data["duration"]
            }
            return redirect('booking/selectParkingSpot')

    else:
        form = BookingForm()

    return render(request, 'booking/createBooking.html', {'form': form})

@login_required
def selectParkingSpot(request):
    bookingData = request.session.get("bookingData")

    if not bookingData:
        return redirect("booking/createBookingPage")

    #get data from session
    zone = ParkingZone.objects.get(id=bookingData["zoneId"])
    date = datetime.strptime(bookingData["date"], "%Y-%m-%d").date()
    startTime = datetime.strptime(bookingData["startTime"], "%H:%M:%S").time()
    duration = bookingData["duration"]

    #check available spots during the time frame
    availableSpots = ParkingSpot.getAvailableSpots(zone, date, startTime, duration)

    if request.method == "POST":
        form = SelectParkingSpotForm(request.POST)
        form.fields['parkingSpot'].queryset = availableSpots

        if form.is_valid():
            spot = form.cleaned_data["parkingSpot"]

            Booking.createBooking(request.user, spot, date, startTime, duration)
            #clean session data
            del request.session["bookingData"]

            return redirect("index") #or to a confirmation page, which i dont think we need

    else:
        form = SelectParkingSpotForm()
        form.fields['parkingSpot'].queryset = availableSpots

    return render(request, "booking/selectParkingSpot.html", {
        "form": form,
        "availableSpots": availableSpots
    })

# @login_required
# def updateBookingPage(request):
#     if request.method == "POST":
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             #save data so session
#             request.session["bookingData"] = {
#                 "zoneId": form.cleaned_data["zone"].id,
#                 "date": str(form.cleaned_data["date"]),
#                 "startTime": str(form.cleaned_data["startTime"]),
#                 "duration": form.cleaned_data["duration"]
#             }
#             return redirect('booking/updateParkingSpot')

#     else:
#         form = BookingForm()

#     return render(request, 'booking/updateBooking.html', {'form': form})

# @login_required
# def updateParkingSpot(request):
#     bookingData = request.session.get("bookingData")

#     if not bookingData:
#         return redirect("booking/updateBookingPage")

#     #get data from session
#     zone = ParkingZone.objects.get(id=bookingData["zoneId"])
#     date = datetime.strptime(bookingData["date"], "%Y-%m-%d").date()
#     startTime = datetime.strptime(bookingData["startTime"], "%H:%M:%S").time()
#     duration = bookingData["duration"]

#     #check available spots during the time frame
#     availableSpots = ParkingSpot.getAvailableSpots(zone, date, startTime, duration)

#     if request.method == "POST":
#         form = SelectParkingSpotForm(request.POST)
#         form.fields['parkingSpot'].queryset = availableSpots

#         if form.is_valid():
#             spot = form.cleaned_data["parkingSpot"]

#             Booking.createBooking(request.user, spot, date, startTime, duration)
#             #clean session data
#             del request.session["bookingData"]

#             return redirect("index") #or to a confirmation page, which i dont think we need

#     else:
#         form = SelectParkingSpotForm()
#         form.fields['parkingSpot'].queryset = availableSpots

#     return render(request, "booking/updateParkingSpot.html", {
#         "form": form,
#         "availableSpots": availableSpots
#     })
