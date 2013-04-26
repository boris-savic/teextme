from django.forms import ModelForm

from contacts.models import Contact


class ContactForm(ModelForm):

    class Meta:
        model = Contact
        exclude = ('user', 'contact_user')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ContactForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(ContactForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
            instance.save()
        return instance
