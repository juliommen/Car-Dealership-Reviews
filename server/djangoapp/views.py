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
    if request.method == "GET":
        url = "https://eebe52d6.us-south.apigw.appdomain.cloud/api/dealership/"
        dealerships = get_dealers(url)
        return HttpResponse(dealerships)

def filter_dealers(request, state):
    if request.method == "GET":
        url = "https://eebe52d6.us-south.apigw.appdomain.cloud/api/dealership/"
        dealerships = get_dealers(url, state=state)
        return HttpResponse(dealerships)


def get_dealer_reviews(request, dealerId):
    if request.method == "GET":
        url = "https://eebe52d6.us-south.apigw.appdomain.cloud/api/review/"
        reviews = get_reviews(url, dealerId=dealerId)
        return HttpResponse(reviews)

def add_review(request, dealerId):
    user = request.user
    if user.is_authenticated:
        review=dict()
        review.name = request.name
        review.dealership = dealer_id
        review.review = request.review
        review.puchase_date = request.purchase_date
        review.car_make = request.car_make
        review.car_model = request.car_model
        review.car_year = request.car_year
        review.sentiment = analyze_review_sentiments(review)
        json_payload = {"review": review}
        url = "https://eebe52d6.us-south.apigw.appdomain.cloud/api/review/"
        response = post_request(url, json_payload, dealerId=dealer_id)
        return HttpResponse(response)




'''
def check_if_enrolled(user, course):
    is_enrolled = False
    if user.id is not None:
        # Check if user enrolled
        num_results = Enrollment.objects.filter(user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    is_enrolled = check_if_enrolled(user, course)
    if not is_enrolled and user.is_authenticated:
        # Create an enrollment
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()
    return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id,)))

def submit(request,course_id):
    submitted_anwsers =  extract_answers(request)
    username = request.user.username
    user = User.objects.get(username=username)
    enrollment = Enrollment.objects.get(user=user,course=course_id)
    submission = Submission.objects.create(
        enrollment=enrollment)
    for choice in submitted_anwsers:
        submission.choices.add(choice)
    #print(submission.choices.filter(id=choice).)
    context = show_exam_result(course_id, submission)
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)


def extract_answers(request):
    submitted_anwsers = []
    for key in request.POST:
        if key.startswith('choice'):
            value = request.POST[key]
            choice_id = int(value)
            submitted_anwsers.append(choice_id)
    return submitted_anwsers


def show_exam_result(course_id, submission):
    course = Course.objects.get(id=course_id)
    choices = submission.choices.all()
    questions = course.question_set.all()
    correct = 0
    total = 0
    for question in questions:
        if (Question.is_get_score(question,choices)):
            correct = correct + 1
        total = total + 1
    grade = correct * 100 / total
    grade = int(grade)
    context={'course':course, 'submission':submission,'grade':grade}
    return context
'''
    