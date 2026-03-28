from django.urls import path
from . import views

urlpatterns = [
    path("", views.indexPage, name="index"),
    path("login", views.loginPage, name="login"),
    path("register", views.registerPage, name="register"),
]
