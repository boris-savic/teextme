import requests
import logging

from django.conf import settings

logger = logging.getLogger(__name__)

NEXMO_URL = 'https://rest.nexmo.com/sms/json'


def nexmo_send_sms(from_number, to_number, msg):
    params = {
        'api_key': settings.NEXMO_API_KEY,
        'api_secret': settings.NEXMO_API_SECRET,
        'from': from_number,
        'to': to_number,
        'text': msg
    }

    logger.info('Sending SMS from %s to %s: %s', from_number, to_number, msg)

    resp = requests.post(NEXMO_URL, params=params)

    result = resp.json()

    if result['messages'][0]['status'] != '0':
        raise Exception('SMS sending error: %s (%s)'
                        % (result['messages'][0]['error-text'], result))

_test_sent_messages = []


def test_send_sms(from_number, to_number, msg):
    sent_message = {
        'from': from_number,
        'to': to_number,
        'text': msg
    }

    logger.info('Sending test SMS from %s to %s: %s',
                from_number,
                to_number,
                msg)

    _test_sent_messages.append(sent_message)


def send_sms(from_number, to_number, msg):
    if settings.SMS_BACKEND == 'nexmo':
        nexmo_send_sms(from_number, to_number, msg)
    elif settings.SMS_BACKEND == 'test':
        test_send_sms(from_number, to_number, msg)
    else:
        raise Exception(
            'Configuration error: invalid settings.SMS_BACKEND: %s',
            settings.SMS_BACKEND)
