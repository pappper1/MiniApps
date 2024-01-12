from django.shortcuts import render


def index(request):
	navbar = {
		'Конвертер валют': 'converter',
	}
	return render(request=request, template_name="currency_converter/index.html", context={"navbar": navbar})


def converter(request):
	navbar = {
		'Конвертер валют':'converter',
	}
	return render(request=request, template_name="currency_converter/converter.html", context={"navbar": navbar})