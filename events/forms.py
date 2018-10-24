from django import forms
from django.contrib.auth.models import User
from .models import Event, Booking, Profile

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['owner',]

        widgets = {
        	'date': forms.DateInput(attrs={'type':'date'}),
        	'starting_time': forms.TimeInput(attrs={'type':'time'}),
        }


class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }

class UserUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['event','user']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']