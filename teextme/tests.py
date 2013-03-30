from django.test import TestCase
from django.conf import settings

from teextme import sms

class SmsTestCase(TestCase):
    def setUp(self):
        self.old_sms_backend = settings.SMS_BACKEND
        settings.SMS_BACKEND = 'test'
        sms._test_sent_messages = []
        super(SmsTestCase, self).setUp()

    def tearDown(self):
        settings.SMS_BACKEND = self.old_sms_backend
        super(SmsTestCase, self).tearDown()

    def get_sms_sent(self):
        return sms._test_sent_messages
