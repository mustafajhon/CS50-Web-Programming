from django import forms
from .models import Passenger


class NewPassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields=['first','last']

