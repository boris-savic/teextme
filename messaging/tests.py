from teextme import sms
from teextme.tests import SmsTestCase
from customauth.models import MyUser
from contacts.models import Contact
from messaging.models import Message

class MessagingTest(SmsTestCase):
    def test_contact_to_contact(self):
        joe = MyUser.objects.create(country_code='+1', phone_number='1')
        jack = MyUser.objects.create(country_code='+1', phone_number='2')

        joe_contact_jack = Contact.objects.create(user=joe, first_name='Jack', last_name='Last', phone_number='+12')
        jack_contact_joe = Contact.objects.create(user=jack, first_name='Joe', last_name='Last', phone_number='+11')

        message = Message.objects.create(
            user=joe,
            sender=None,
            recepient=joe_contact_jack,
            message='Lorem ipsum'
        )

        message.send()

        self.assertIsNotNone(message.date_sent)
        self.assertIsNotNone(message.other_message)

        other_message = message.other_message

        self.assertEqual(other_message.user, jack)
        self.assertEqual(other_message.sender, jack_contact_joe)
        self.assertIsNone(other_message.recepient)
        self.assertEqual(other_message.message, message.message)
        self.assertIsNotNone(other_message.date_sent)
        self.assertEqual(other_message.other_message, message)

        self.assertEqual(len(self.get_sms_sent()), 0)

    def test_contact_to_noncontact(self):
        joe = MyUser.objects.create(country_code='+1', phone_number='1')
        jack = MyUser.objects.create(country_code='+1', phone_number='2')

        joe_contact_jack = Contact.objects.create(user=joe, first_name='Jack', last_name='Last', phone_number='+12')

        message = Message.objects.create(
            user=joe,
            sender=None,
            recepient=joe_contact_jack,
            message='Lorem ipsum'
        )

        message.send()

        self.assertIsNotNone(message.date_sent)
        self.assertIsNotNone(message.other_message)

        other_message = message.other_message

        self.assertEqual(other_message.user, jack)
        self.assertIsNone(other_message.sender)
        self.assertIsNone(other_message.recepient)
        self.assertEqual(other_message.message, message.message)
        self.assertIsNotNone(other_message.date_sent)
        self.assertEqual(other_message.other_message, message)

        self.assertEqual(len(self.get_sms_sent()), 0)

    def test_contact_to_nonuser(self):
        joe = MyUser.objects.create(country_code='+1', phone_number='1')

        joe_contact_jack = Contact.objects.create(user=joe, first_name='Jack', last_name='Last', phone_number='+12')

        message = Message.objects.create(
            user=joe,
            sender=None,
            recepient=joe_contact_jack,
            message='Lorem ipsum'
        )

        message.send()

        self.assertIsNotNone(message.date_sent)
        self.assertIsNone(message.other_message)

        self.assertEqual(len(self.get_sms_sent()), 1)

        self.assertEqual(self.get_sms_sent()[0], {
            'from': '+11',
            'to': '+12',
            'text': 'Lorem ipsum'
        })
