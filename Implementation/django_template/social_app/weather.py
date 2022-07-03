# views file for weather functionality @Kerstin
from django.db import models


# choices is django's equivalent of enums
class WeatherState(models.TextChoices):
    # test
    sun = 'sun'
    rain = 'rain'
    wind = 'wind'
    thunder = 'thunder'
    snow = 'snow'
    none = 'none'
