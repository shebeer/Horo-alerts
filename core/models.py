from datetime import date
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Prediction(models.Model):
    zodiac = models.CharField(max_length=100)
    prediction = models.CharField(max_length=1000)

class Zodiac(models.Model):
    date = models.DateTimeField(unique=True)
    zodiac = models.ManyToManyField(Prediction,related_name="zodiactoprediction")

class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name="userprofiletoUser")
    sex = models.BooleanField(default=False)  #True for male
    mobile = models.CharField(max_length=100)
    zodiac = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country =models.CharField(max_length=100)






