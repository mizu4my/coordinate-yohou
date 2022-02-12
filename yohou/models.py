from django.db import models
from django.conf import settings

# Create your models here.
CATEGORY_CHOICES = (
    (1, 'WOMEN'),
    (2, 'MEN'),
    (3, 'KIDS'),
)

WEATHER_CHOICES = (
    (1, '晴れ'),
    (2, '曇り'),
    (3, '雨')
)


class Post(models.Model):
    author = models.CharField(max_length=30, blank=False, null=False)
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    temperature = models.IntegerField(blank=False, null=False)
    weather = models.IntegerField(choices=WEATHER_CHOICES)
    title = models.CharField(max_length=30)
    text = models.TextField(blank=True, null=True)
    brands_tops = models.CharField(max_length=30, blank=True, null=True)
    brands_bottoms = models.CharField(max_length=30, blank=True, null=True)
    brands_shoes = models.CharField(max_length=30,blank=True, null=True)
    brands_outer = models.CharField(max_length=30, blank=True, null=True)
    brands_accesory = models.CharField(max_length=30, blank=True, null=True)
    photo = models.FileField(upload_to = 'static/media/posts', blank=False, null=False)