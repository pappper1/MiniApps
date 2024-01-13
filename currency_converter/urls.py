from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("converter/", views.converter, name="converter"),
    path("error/", views.error_500, name="error"),
]