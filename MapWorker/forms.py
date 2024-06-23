from django import forms

from .models import Layer


class LayerUploadForm(forms.ModelForm):
    class Meta:
        model = Layer
        fields = ("title", "layer_type", "csv_layer")
