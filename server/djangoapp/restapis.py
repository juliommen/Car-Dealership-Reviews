import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
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
                print(review)
                review_obj = DealerReview(
                                            id=review["id"], name=review["name"],             
                                            dealership=review["dealership"], review=review["review"],
                                            purchase=review["purchase"], purchase_date=review["purchase_date"],
                                            car_make=review["car_make"], car_model=review["car_model"],
                                            car_year=review["car_year"], sentiment=review["sentiment"])
                results.append(review_obj)
            return results
        except:
            return json_result
            
        
    


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



