from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager

# Create your models here.
CATEGORY_CHOICES = (
    (1, 'WOMEN'),
    (2, 'MEN'),
    (3, 'KIDS'),
)

SEASON_CHOICES = (
    (1, '春'),
    (2, '夏'),
    (3, '秋'),
    (4, '冬')
)


class Post(models.Model):
    username = models.CharField(max_length=30, blank=False, null=False)
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    temperature = models.IntegerField(blank=False, null=False)
    season = models.IntegerField(choices=SEASON_CHOICES, null=True)
    text = models.TextField(blank=True, null=True)
    brands_tops = models.CharField(max_length=30, blank=True, null=True)
    brands_bottoms = models.CharField(max_length=30, blank=True, null=True)
    brands_onpiece = models.CharField(max_length=30, blank=True, null=True)
    brands_shoes = models.CharField(max_length=30,blank=True, null=True)
    brands_outer = models.CharField(max_length=30, blank=True, null=True)
    brands_accesory = models.CharField(max_length=30, blank=True, null=True)
    brands_bag = models.CharField(max_length=30, blank=True, null=True)
    photo = models.ImageField(upload_to = 'static/media/posts', blank=False, null=False)

class Advice(models.Model):
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    start_temp = models.IntegerField(blank=False, null=False)
    end_temp = models.IntegerField(blank=False, null=False)
    season = models.IntegerField(choices=SEASON_CHOICES, null=True)
    text = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to = 'static/media/advices', blank=False, null=False)