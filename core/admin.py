from django.contrib import admin
from .models import Prediction,Zodiac,UserProfile

# Register your models here.
admin.site.register(Prediction)
admin.site.register(Zodiac)
admin.site.register(UserProfile)
