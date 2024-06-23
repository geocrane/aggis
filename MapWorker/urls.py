from django.urls import path

from .views import index, city_map

app_name = "maps"

urlpatterns = [
    path("", index, name="index"),
    path("<slug:city_slug>/", city_map, name="city_map"),
]
