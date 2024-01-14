import logging

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.cache import cache

from .models import *
from .weather_parser import WeatherParser
from .forms import AddCountryForm


logger = logging.getLogger(__name__)

def get_world_countries():
    try:
        world_countries = cache.get('world_countries')
        if not world_countries:
            world_countries_obj = WorldCountries.objects.all()
            world_countries = [country.name.lower() for country in world_countries_obj]
            cache.set('world_countries', world_countries, 60)
        return world_countries
    except Exception as e:
        logger.error(f"Ошибка при получении списка стран мира: {e}")
        return redirect('error')


def weather(request):
    try:
        countries = Country.objects.all().order_by('name')
        if request.method == 'POST':
            country_id = int(request.POST.get('country'))
            return redirect('city_weather', country=country_id)
        return render(request, 'weather/weather.html', {'countries': countries})
    except Exception as e:
        logger.error(f"Ошибка при получении списка стран: {e}")
        return redirect('error')


def city_weather(request, country: int):
    try:
        country_info = Country.objects.get(id=country)
        cities = City.objects.filter(country=country_info).order_by('name')
        if request.method == 'POST':
            city_id = int(request.POST.get('city'))
            return redirect('weather_info', country=country, city=city_id)

        return render(request, 'weather/city_choose.html', {'cities': cities, 'country': country_info.name.capitalize()})
    except Exception as e:
        logger.error(f"Ошибка при получении списка городов: {e}")
        return redirect('error')

def weather_info(request, country: int, city: int):
    try:
        parse = WeatherParser()
        weather_info = parse.get_weather(City.objects.get(id=city).url)
        if not weather_info:
            return render(request, 'weather/weather_info.html', {'error_message': 'Не удалось получить информацию о погоде.'})

        context = {
            'country': Country.objects.get(id=country).name.capitalize(),
            'city': City.objects.get(id=city).name.capitalize(),
            'weather_info': weather_info,
        }
        return render(request, 'weather/weather_info.html', context)
    except Exception as e:
        logger.error(f"Ошибка при получении информации о погоде: {e}")
        return redirect('error')


def add_country(request):
    try:
        success = False
        error_message = ''
        if request.method == "POST":
            parser = WeatherParser()
            form = AddCountryForm(request.POST)
            if form.is_valid():
                country_name = form.cleaned_data["country_name"].lower()
                world_countries = get_world_countries()
                if country_name not in world_countries:
                    error_message = 'Страна не входит в список стран мира.'
                elif not Country.objects.filter(name__iexact=country_name).exists():
                    country = Country.objects.create(name=country_name.capitalize())
                    cities = parser.get_cities(country_name)
                    if cities:
                        city_objects = [City(name=city['name'], url=city['url'], country=country) for city in cities]
                        City.objects.bulk_create(city_objects)
                        success = True
                    else:
                        error_message = 'Не удалось получить города для заданной страны.'
                else:
                    error_message = 'Страна уже существует.'

        return render(request, 'weather/add_country.html', {'success': success, 'error_message': error_message})
    except Exception as e:
        logger.error(f"Ошибка при добавлении страны: {e}")
        return redirect('error')