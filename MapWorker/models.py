from django.db import models
from django.apps import apps

LAYERS_TYPES = [
    ("markers", "Маркер"),
    ("polygons", "Полигон"),
    ("routes", "Маршрут"),
    ("heatmap", "Тепловая карта"),
]


class City(models.Model):
    name = models.CharField(max_length=256, verbose_name="Город")
    slug = models.SlugField(unique=True, verbose_name="Идентификатор города")
    population = models.IntegerField(verbose_name="Численность")
    size = models.IntegerField(verbose_name="Размер")
    center_x = models.FloatField(verbose_name="Координата Х центра")
    center_y = models.FloatField(verbose_name="Координата Y центра")

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return self.name


class Layer(models.Model):
    title = models.CharField(max_length=256, verbose_name="Название слоя")
    city = models.ForeignKey(
        City,
        related_name="cities",
        on_delete=models.CASCADE,
        verbose_name="Метки для города",
    )
    csv_layer = models.FileField(upload_to="csv_layers", verbose_name="Путь к файлу")
    layer_type = models.CharField(
        max_length=256, choices=LAYERS_TYPES, verbose_name="Тип слоя", default="markers"
    )

    class Meta:
        verbose_name = "Метка"
        verbose_name_plural = "Метки"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apps.get_app_config("MapWorker").ready()

    def __str__(self):
        return self.title
