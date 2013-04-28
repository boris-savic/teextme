from django import forms
from django.contrib.auth import get_user_model

from customauth.country import COUNTRY_CHOICES
from customregistration.models import ActivationProfile


class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.

    Validates that the requested phonenumber is not already in use, and
    requires the password to be entered twice to catch typos.
    """

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(RegistrationForm, self).__init__(*args, **kwargs)

    country_code = forms.ChoiceField(label="Country Code",
                                     choices=COUNTRY_CHOICES)
    phone_number = forms.RegexField(
        regex=r'^[0-9]+$',
        max_length=15,
        widget=forms.TextInput(),
        label="Phone Number",
        error_messages={'invalid': "This value may contain only numbers."})

    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput(render_value=False))

    def clean_phone_number(self):
        """
        Validate that the phonenumber is numeric and is not already
        in use.
        """
        existing = get_user_model().objects.filter(
            phone_number__iexact=self.cleaned_data['phone_number'])
        if existing.exists():
            raise forms.ValidationError(
                "A user with that phonenumber already exists.")
        else:
            return self.cleaned_data['phone_number']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        """
        if ('password1' in self.cleaned_data and
                'password2' in self.cleaned_data):
            if (self.cleaned_data['password1'] !=
                    self.cleaned_data['password2']):
                raise forms.ValidationError(
                    "The two password fields didn't match.")
        return self.cleaned_data

    def save(self):
        country_code, phone_number, password = (
            self.cleaned_data['country_code'],
            self.cleaned_data['phone_number'],
            self.cleaned_data['password1'])
        user = get_user_model().objects.create_user(
            country_code,
            phone_number,
            password)

        ActivationProfile.objects.create_activation(user)

        user.is_active = False
        user.save()

        return user


class ActivationForm(forms.Form):
    """
    Form for activating a new user account.
    """

    phone_number = forms.RegexField(
        regex=r'^[0-9]+$',
        max_length=15,
        widget=forms.TextInput(),
        label="Phone Number",
        error_messages={'invalid': "This value may contain only numbers."})

    validation_code = forms.RegexField(
        regex=r'^[0-9]+$',
        max_length=5,
        widget=forms.TextInput(),
        label="Activation Number",
        error_messages={'invalid': "This value may contain only numbers."})

    def clean_validation_code(self):
        """
        Check if number is correct
        """

        activation = ActivationProfile.objects.filter(
            user__phone_number=self.cleaned_data['phone_number'],
            code=self.cleaned_data['validation_code'])
        if activation:
            self.activation = activation[0]
            self.user = self.activation.user
            return self.cleaned_data
        else:
            raise forms.ValidationError("Invalid confirmation code.")

    def save(self):
        self.activation.delete()
        self.user.is_active = True
        self.user.save()

        return self.user
