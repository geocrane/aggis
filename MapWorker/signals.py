from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Layer


@receiver(pre_delete, sender=Layer)
def delete_layer_file(sender, instance, **kwargs):
    """
    Удаляет CSV файл, связанный с объектом Layer перед его удалением.
    """
    try:
        instance.csv_layer.delete()
    except AttributeError:
        pass
