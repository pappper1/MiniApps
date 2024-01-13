import os

from django.shortcuts import render, redirect

from MiniApps import settings
from .currency_parser import CurrencyParser


def index(request):
    return render(request, "currency_converter/index.html")


def converter(request):
    file_path = os.path.join(settings.BASE_DIR, 'currency_converter', 'static', 'texts', 'currency_list.txt')
    with open(file_path, "r") as file:
        currencies = [currency.strip() for currency in file.readlines()]
    if request.method == "POST":
        from_currency = request.POST.get("from_currency")
        to_currency = request.POST.get("to_currency")
        amount = request.POST.get("amount")
        parser = CurrencyParser(from_currency, to_currency)
        try:
            exchange_rate = parser.get_exchange_rate()
            if exchange_rate:
                result = round(int(amount) * parser.get_exchange_rate(), 2)
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
        except:
            return redirect("error")
    else:
        return render(request, "currency_converter/converter.html", {"currencies": currencies})


def error_500(request):
	return render(request, 'currency_converter/error.html', status=500)