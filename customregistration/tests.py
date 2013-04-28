from teextme.tests import SmsTestCase
from customauth.models import MyUser
from customregistration.models import ActivationProfile


class ActivationProfileTest(SmsTestCase):
    def test_full_number(self):
        joe = MyUser.objects.create(
            country_code='+386',
            phone_number='12345678')
        activation = ActivationProfile.objects.create_activation(joe)

        self.assertTrue(10000 <= int(activation.code) < 99999)

        self.assertEqual(len(self.get_sms_sent()), 1)

        self.assertEqual(self.get_sms_sent()[0], {
            'from': 'TeextMe',
            'to': '+38612345678',
            'text': 'Welcome to TeextMe, your activation code is: %s'
                    % activation.code
        })
