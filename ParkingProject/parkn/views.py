from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Booking
from .forms import UserForm
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
    if request.method == "POST":
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