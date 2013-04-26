from django.forms import ModelForm

from messaging.models import Message

class MessageForm(ModelForm):
  
    class Meta:
        model = Message
        exclude = ('user', 'sender', 'recepient', 'date_sent', 'date_received', 'other_message')
    
    def __init__(self, user, contact, *args, **kwargs):
        self.user = user
        self.recepient_contact = contact
        super(MessageForm, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super(MessageForm, self).save(commit=False)
        if self.user: #in ostala polja k jih je treba narest:
            instance.user = self.user
            instance.recepient = self.recepient_contact
            #in ostala polja
            instance.save()
            instance.send()
        return instance