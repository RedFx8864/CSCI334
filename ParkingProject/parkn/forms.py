from django import forms
from .models import ParkingSpot, ParkingZone

class UserForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class BookingForm(forms.Form):
    zone = forms.ModelChoiceField(queryset=ParkingZone.objects.all())

    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    startTime = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    duration = forms.IntegerField(min_value=1)

class SelectParkingSpotForm(forms.Form):
    parkingSpot = forms.ModelChoiceField(
        queryset=ParkingSpot.objects.none(), #update depending on info
        required=True
    )