from django.urls import path, re_path
from . import views

urlpatterns = [
    path("weather/", views.weather, name="weather"),
    path("weather/get-countries/", views.get_countries, name="get_countries"),
    path("weather/add-country/", views.add_country, name="add_country"),
    re_path(r"^weather/(?P<country>[\w-]+)/$", views.city_weather, name="city_weather"),
    re_path(r"^weather/(?P<country>[\w-]+)/(?P<city>[\w-]+)/$", views.weather_info, name="weather_info"),
]