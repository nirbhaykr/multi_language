from django.db import models

# Create your models here.

class Country(models.Model):
    country = models.CharField(max_length=100)
    
class City(models.Model): 
    country = models.ForeignKey(Country)
    city = models.CharField(max_length=100)

class UserLocation(models.Model):
    ip = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100,blank=True)
    city = models.ForeignKey(City)
