# Generated by Django 3.2.9 on 2022-03-10 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yohou', '0013_seasonicon'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SeasonIcon',
            new_name='WeatherIcon',
        ),
        migrations.RenameField(
            model_name='weathericon',
            old_name='season',
            new_name='weather',
        ),
        migrations.RenameField(
            model_name='weathericon',
            old_name='season_icon',
            new_name='weather_icon',
        ),
    ]