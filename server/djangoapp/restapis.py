import os
import requests
import json
import urllib.parse
from dotenv import load_dotenv
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions

load_dotenv()

def get_request(url, **kwargs):
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                            params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    json_data = json.loads(response.text)
    return json_data


def get_dealers(url, **kwargs):
    results = []
    try:
        state = kwargs['state']
    except:
        state=""
    json_result = get_request(url, state=state)
    if json_result:
        dealers = json_result["rows"]
        for dealer in dealers:
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], state=dealer["state"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results

def get_reviews(url, **kwargs):
    results = []
    try:
        dealerId = kwargs['dealerId']
    except:
        dealerId=""
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        try:
            reviews = json_result["reviews"]
            for review in reviews:

                if (review["sentiment"]==""):
                    try:
                        sentiment = analyze_review_sentiments(review["review"])
                    except:
                        sentiment = ""
                else:
                    sentiment = review["sentiment"]

                review_obj = DealerReview(
                                            name=review["name"],             
                                            dealership=review["dealership"], review=review["review"],
                                            purchase=review["purchase"], purchase_date=review["purchase_date"],
                                            car_make=review["car_make"], car_model=review["car_model"],
                                            car_year=review["car_year"], sentiment=sentiment)
                results.append(review_obj)
                print(review_obj)
            return results
        except:
            return json_result
            
def analyze_review_sentiments(text):
    text = urllib.parse.quote(text)
    url = os.environ.get('url')+"/v1/analyze?version=2022-04-07&text="+text+"&features=keywords&keywords.sentiment=true&keywords.limit=1"
    print(url)
    apikey =  os.environ.get('key')
 
    response = requests.get(url, auth=HTTPBasicAuth('apikey', apikey))
    response = json.loads(response.text)
    sentiment = response["keywords"][0]["sentiment"]["label"] 
    return sentiment
    
def post_request(url, json_payload, **kwargs):
    print(json_payload)
    try:
        response = requests.post(url, json=json_payload, params=kwargs) 
    except:
        print("Network exception occurred")
    status_code = response.status_code
    json_data = json.loads(response.text)
    return json_data    




