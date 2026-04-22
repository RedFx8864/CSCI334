from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User #Django's default model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Booking
from .forms import UserForm, BookingForm

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
def createBooking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            user = request.user
            date = form.cleaned_data['date']
            startTime = form.cleaned_data['startTime']
            duration = form.cleaned_data['duration']

            Booking.createBooking(user, date, startTime, duration)
            return redirect('index')
    else:
        form = BookingForm()
    context ={'form':form}
    return render(request, 'createBooking.html', context)