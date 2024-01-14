from django.urls import path, re_path
from . import views

urlpatterns = [
    path("weather/", views.weather, name="weather"),
    path("weather/add-country/", views.add_country, name="add_country"),
    path("weather/<int:country>/", views.city_weather, name="city_weather"),
    path("weather/<int:country>/<int:city>/", views.weather_info, name="weather_info"),
]