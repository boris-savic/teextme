import urllib
import requests
import logging

from django.conf import settings

logger = logging.getLogger(__name__)

URL = 'https://rest.nexmo.com/sms/json'

def send_sms(from_number, to_number, msg):
    params = {
        'api_key': settings.NEXMO_API_KEY,
        'api_secret': settings.NEXMO_API_SECRET,
        'from': from_number,
        'to': to_number,
        'text': msg
    }

    logger.info('Sending SMS from %s to %s: %s', from_number, to_number, msg)

    resp = requests.post(URL, params=params)

    result = resp.json()

    print result

    if result['messages'][0]['status'] != '0':
        raise Exception('SMS sending error: %s (%s)'
            % (result['messages'][0]['error-text'], result))
