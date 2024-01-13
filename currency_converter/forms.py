from django import forms

class CurrencyForm(forms.Form):
    from_currency = forms.CharField()
    to_currency = forms.CharField()
    amount = forms.DecimalField()