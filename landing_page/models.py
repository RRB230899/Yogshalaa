from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = PhoneNumberField(default='', blank=False, null=False, unique=True)
    uid = models.CharField(default=uuid.uuid4, max_length=200, unique=True, null=True, blank=True)
    country_code = models.CharField(default='+91', max_length=5)
    is_verified = models.BooleanField(default=False)
    objects = models.Manager()


class TrialClassUserPreferences(models.Model):

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, default=None, null=True)
    phone_num = PhoneNumberField(default='', unique=True, null=False, blank=False)
    focus_choices = models.CharField(default=None, null=True, max_length=200)
    style_choices = models.CharField(default=None, null=True, max_length=200)
    objects = models.Manager()


class YogaUserMorning(models.Model):

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, default=None, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch_choice = models.CharField(default='Batch I', null=False, max_length=10)
    date_of_joining = models.CharField(default='', null=False, max_length=25)
    objects = models.Manager()

    def __str__(self):
        phone_num = str(self.profile.mobile)
        return phone_num
