from django.contrib import admin
from .models import * # замените на имена ваших моделей

admin.site.register(Country)
admin.site.register(City)