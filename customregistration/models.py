import random
import logging

from django.db import models
from django.conf import settings

from teextme.sms import send_sms

logger = logging.getLogger(__name__)

class ActivationProfileManager(models.Manager):
    def create_activation(self, user):
        # generate random code
        code = str(random.randint(10000, 99999))
        activation = self.create(user=user, code=code)

        phone = user.full_number

        try:
            send_sms(settings.SITE_NAME, phone, settings.ACTIVATION_MESSAGE % code)
        except Exception, e:
            logger.error('Activation code %s could not be sent to %s: ', code, phone, exc_info=True)
            raise e

        return activation

class ActivationProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    code = models.CharField(max_length=5)

    objects = ActivationProfileManager()
