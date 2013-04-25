from django.test import TestCase

from customauth.models import MyUser


class MyUserTest(TestCase):
    def test_full_number(self):
        joe = MyUser.objects.create(country_code='+386',
                                    phone_number='12345678')

        self.assertEqual(joe.full_number, '+38612345678')

    def test_full_number_leading_zero(self):
        joe = MyUser.objects.create(country_code='+386',
                                    phone_number='012345678')

        self.assertEqual(joe.full_number, '+38612345678')
