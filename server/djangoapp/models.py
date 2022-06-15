import sys
from django.db import models
from django.utils.timezone import now
from django.conf import settings
import uuid

# Course model
class CarMake(models.Model):
    car_make = models.CharField(null=False, max_length=30)
    description = models.CharField(max_length=1000)
    def __str__(self):
        return "Name: " + self.car_make + "," + \
               "Description: " + self.description


class CarModel(models.Model):
    car_make_id = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    car_model = models.CharField(null=False, max_length=30)
    dealership_id = models.IntegerField(null=False)
    CAR_TYPES = [('sedan', 'Sedan'),('suv', 'SUV'),('wagon', 'Wagon'),('hatch', 'Hatch'),('truck','Truck')]
    car_type =  models.CharField(null=False, max_length=5, choices=CAR_TYPES, default='hatch')
    car_year = models.DateField(null=False)
    def __str__(self):
        return "Name: " + self.car_model



# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
