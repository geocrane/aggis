# Generated by Django 4.2.13 on 2024-06-21 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MapWorker', '0003_layer_alter_city_name_alter_city_population_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='layer_type',
            field=models.CharField(choices=[('markers', 'Маркеры'), ('polygon', 'Полигоны'), ('routes', 'Маршруты')], default='markers', max_length=256, verbose_name='Типы полей'),
        ),
    ]
