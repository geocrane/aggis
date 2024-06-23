from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import City, Layer


class CityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "center_x",
        "center_y",
        "population",
        "size",
    )


class LayerAdmin(admin.ModelAdmin):
    list_display = ("title", "layer_type", "csv_layer")


admin.site.register(City, CityAdmin)
admin.site.register(Layer, LayerAdmin)

admin.site.unregister(Group)
admin.site.unregister(User)
