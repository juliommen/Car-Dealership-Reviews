import sys
from django.db import models
from django.utils.timezone import now
from django.conf import settings
import uuid


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
    car_year = models.IntegerField(null=False)
    def __str__(self):
        return "Name: " + self.car_model


class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, state, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.state = state
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:

    def __init__(self, name, dealership, review, purchase_date, car_make, car_model, car_year,sentiment):
        self.name = name
        self.dealership = dealership
        self.review = review
        self.puchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment

    def __str__(self):
        return "Review: " + self.review
