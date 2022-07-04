from django.db import models


# choices is django's equivalent of enums
class WeatherState(models.TextChoices):
    sun = 'sun'
    rain = 'rain'
    wind = 'wind'
    thunder = 'thunder'
    snow = 'snow'
    none = 'none'
