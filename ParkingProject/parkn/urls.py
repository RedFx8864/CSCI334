from django.urls import path
from . import views

urlpatterns = [
    path("", views.indexPage, name="index"),
    path("login/", views.loginPage, name="login"),
    path("register/", views.registerPage, name="register"),
    path("logout/", views.logoutPage, name="logout"),
    path("createBooking/", views.createBookingPage, name="createBooking"),
    path("selectParkingSpot/", views.selectParkingSpot, name="selectParkingSpot"),
    path("viewBookings/", views.viewBookings, name="viewBookings"),
    path("updateBooking/<int:bookingId>", views.updateBookingPage, name="updateBooking"),
    path("updateParkingSpot/<int:bookingId>", views.updateParkingSpot, name="updateParkingSpot"),
]
