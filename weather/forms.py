from django import forms
from .models import Country

class CityForm(forms.Form):
    city = forms.CharField(max_length=100)


class AddCountryForm(forms.Form):
    country_name = forms.CharField(max_length=100)