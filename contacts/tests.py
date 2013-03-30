from django.test import TestCase

from customauth.models import MyUser
from contacts.models import Contact

class ContactsTest(TestCase):
    def test_contact_existing_user(self):
        joe = MyUser.objects.create(country_code='+1', phone_number='1')
        jack = MyUser.objects.create(country_code='+1', phone_number='2')

        joe_contact_jack = Contact.objects.create(user=joe, first_name='Jack', last_name='Last', phone_number='+12')
        jack_contact_joe = Contact.objects.create(user=jack, first_name='Joe', last_name='Last', phone_number='+11')

        self.assertEqual(joe.full_number, '+11')
        self.assertEqual(jack.full_number, '+12')

        self.assertEquals(joe_contact_jack.contact_user, jack)

        self.assertEquals(jack_contact_joe.contact_user, joe)

    def test_contact_nonexisting_user(self):
        joe = MyUser.objects.create(country_code='+1', phone_number='1')

        joe_contact_jack = Contact.objects.create(user=joe, first_name='Jack', last_name='Last', phone_number='+12')

        self.assertEqual(joe.full_number, '+11')

        self.assertIsNone(joe_contact_jack.contact_user)
