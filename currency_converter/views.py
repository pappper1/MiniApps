import os
from loguru import logger

from django.core.cache import cache
from django.shortcuts import render, redirect

from MiniApps import settings
from .currency_parser import CurrencyParser
from .forms import CurrencyForm
from .models import Currencies


def get_currencies():
    currencies = cache.get('currencies')
    if not currencies:
        currencies = Currencies.objects.all()
        cache.set('currencies', currencies, 60)
    return currencies

def index(request):
    return render(request, "currency_converter/index.html")

def converter(request):
    currencies = get_currencies()
    if request.method == "POST":
        form = CurrencyForm(request.POST)
        if form.is_valid():
            from_currency = form.cleaned_data["from_currency"]
            to_currency = form.cleaned_data["to_currency"]
            amount = form.cleaned_data["amount"]
            parser = CurrencyParser(from_currency, to_currency)
            try:
                exchange_rate = parser.get_exchange_rate()
                if exchange_rate:
                    result = round(int(amount) * exchange_rate, 2)
                else:
                    result = "Произошла ошибка при получении курса валюты"
                context = {
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "amount": amount,
                    "currencies": currencies,
                    "result": result
                }
                return render(request, "currency_converter/converter.html", context)
            except Exception as e:
                logger.exception(e)
                return redirect("error")
    else:
        return render(request, "currency_converter/converter.html", {"currencies": currencies})

def error_500(request):
    return render(request, 'currency_converter/error.html', status=500)