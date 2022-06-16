from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel
from .restapis import get_dealers, get_reviews, analyze_review_sentiments, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


def get_dealerships(request):
    context={}
    if request.method == "GET":
        url = "https://eebe52d6.us-south.apigw.appdomain.cloud/api/dealership/"
        dealerships = get_dealers(url)
        context['dealerships'] = dealerships
        return render(request, 'djangoapp/index.html', context)

def get_dealer_reviews(request, dealerId):
    context={}
    context['dealerId']=dealerId
    if request.method == "GET":
        url = "https://eebe52d6.us-south.apigw.appdomain.cloud/api/review/"
        reviews = get_reviews(url, dealerId=dealerId)
        if (type(reviews)==dict):
            context['message'] = "No reviews found for this dealership."   
        else:
            context['reviews'] = reviews    
        return render(request, 'djangoapp/dealer_reviews.html', context)

def add_review(request, dealerId):
    user = request.user
    if request.method != "GET":
        if user.is_authenticated:
            review={}
            review["name"] = request.POST['reviewer_name']
            review["dealership"] = dealerId
            review["purchase_date"] = request.POST['purchasedate']
            review["review"] = request.POST['review']

            car_id = request.POST['car']
            car = CarModel.objects.get(pk=car_id)
            review["car_make"] = CarMake.objects.get(id=car.car_make_id.pk).car_make
            review["car_model"] = car.car_model
            review["car_year"] = car.car_year

            review["sentiment"] = analyze_review_sentiments(request.POST['review'])

            json_payload = {"review": review}          
            url = "https://eebe52d6.us-south.apigw.appdomain.cloud/api/review/"
            post_request(url=url, json_payload=json_payload)        
            return redirect('djangoapp:dealer_reviews',dealerId=dealerId)
    else: 
        car_models = CarModel.objects.filter(dealership_id=dealerId).all()
        cars =[]
        context={}
        for car in car_models:
            id = car.pk
            model = car.car_model
            year = car.car_year
            car_make = CarMake.objects.get(id=car.car_make_id.pk).car_make
            cars.append({"id":id,"model":model,"year":year,"car_make":car_make})
        context['dealerId']=dealerId
        context['cars'] = cars
        return render(request, 'djangoapp/add_review.html', context)
