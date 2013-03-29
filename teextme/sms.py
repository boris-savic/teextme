import urllib
import requests

from django.conf import settings

URL = 'https://rest.nexmo.com/sms/json'

def send_sms(from_number, to_number, msg):
    params = {
        'api_key': settings.API_KEY,
        'api_secret': settings.API_SECRET,
        'from': from_number,
        'to': to_number,
        'text': msg
    }

    return requests.post(URL, params=params)
