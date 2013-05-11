from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from country import COUNTRY_CHOICES


class MyUserManager(BaseUserManager):
    def create_user(self, country_code, phone_number, password=None):
        """
        Creates and saves a User with the given phone number, country code
        and password.
        """
        if not phone_number:
            raise ValueError('Users must have an phone number')

        user = self.model(
            phone_number=phone_number,
            country_code=country_code,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, country_code, phone_number,
                         full_number, password):
        """
        Creates and saves a superuser with the given phone number,
        country country_code and password.
        """
        user = self.create_user(
            phone_number=phone_number,
            password=password,
            country_code=country_code
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    country_code = models.CharField(max_length=50, choices=COUNTRY_CHOICES)
    phone_number = models.CharField(
        verbose_name='phone number',
        max_length=255,
        db_index=True,
    )

    full_number = models.CharField(
        max_length=255,
        unique=True,
    )  # generated denormalization

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'full_number'
    REQUIRED_FIELDS = ['country_code', 'phone_number']

    def get_full_name(self):
        # The user is identified by their phone number
        return self.phone_number

    def get_short_name(self):
        # The user is identified by their phone number
        return self.phone_number

    def __unicode__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def save(self, *args, **kwargs):
        self.full_number = self.country_code + self.phone_number.lstrip('0')
        return super(MyUser, self).save(*args, **kwargs)
