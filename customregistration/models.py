import random

from django.db import models
from django.conf import settings

from teextme.sms import send_sms

class ActivationProfileManager(models.Manager):
    def create_activation(self, user):
        #generate random code
        code = str(random.randint(10000, 99999))
        activation = self.create(user=user, code=code)

        print("ACTIVATION CODE: " + code)
        #send activation code to sms
        phone = user.country_code + user.phone_number
        response = send_sms(settings.SITE_NAME, phone, settings.ACTIVATION_MESSAGE+code)

        return activation

class ActivationProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    code = models.CharField(max_length=5)

    objects = ActivationProfileManager()
