from django import forms

class UserForm(forms.Form):
    email = forms.EmailField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

class BookingForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    startTime = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    duration = forms.IntegerField(min_value=1)