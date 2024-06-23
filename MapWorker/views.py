import json

from django.http import HttpResponseRedirect
from django.db.models import Q, BooleanField, Value, Case, When
from django.shortcuts import render

from .forms import LayerUploadForm
from .models import City, Layer
from .service import read_coords_from_csv, validate_csv_file


def index(request):
    cities = City.objects.all()
    return render(request, "index.html", {"cities": cities})


def city_map(request, city_slug):
    city = City.objects.get(slug=city_slug)
    form = LayerUploadForm()
    layers_data = []
    layers_selected = []

    # Check Layers
    if request.method == "POST":
        selected_mark_ids = request.POST.getlist("layers")
        if selected_mark_ids:
            layers_selected = Layer.objects.filter(
                Q(id__in=[int(id) for id in selected_mark_ids])
            )
            layers_data = [
                read_coords_from_csv(layer.csv_layer.path, layer.layer_type)
                for layer in layers_selected
            ]

    layers_selected_ids = (
        layers_selected.values_list("id", flat=True) if layers_selected else []
    )

    layers = Layer.objects.filter(city=city).annotate(
        selected=Case(
            When(id__in=layers_selected_ids, then=Value(True)),
            default=Value(False),
            output_field=BooleanField(),
        )
    )

    map_data = {
        "zoom": 12,
        "tiles_city": city_slug,
        "center_x": city.center_x,
        "center_y": city.center_y,
        "layers_data": layers_data,
    }

    context = {
        "form": form,
        "city": city,
        "layers": layers,
        "map_data": json.dumps(map_data),
        "csv_error_message": "",
    }

    # CSV loader
    if request.method == "POST" and not layers_data:
        form = LayerUploadForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            csv = form.save(commit=False)
            csv.city = city

            # IF VALIDATE BEFORE LOADING <===========
            if not validate_csv_file(csv.csv_layer.path):
                context["csv_error_message"] = (
                    "Структура CSV-файла не подходит для выбранного типа слоя!"
                )
                return render(request, "city_map.html", context)

            csv = form.save()

            # OR VALIDATE AFTER LOADING <===========
            if not validate_csv_file(csv.csv_layer.path):
                context["csv_error_message"] = (
                    "Структура CSV-файла не подходит для выбранного типа слоя!"
                )
                return render(request, "city_map.html", context)

        return HttpResponseRedirect(request.path_info)
    return render(request, "city_map.html", context)
