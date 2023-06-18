from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid
from django.contrib.auth.models import User


class YogaUser(models.Model):

    genderChoices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('NA', 'Prefer not to say')
    ]

    beginner = [
        ('N', 'No'),
        ('Y', 'Yes')
    ]

    packagesOffered = [
        ('M', 'Monthly'),
        ('Q', 'Quarterly')
    ]

    batchTimings = [
        ('M', 'Morning'),
        ('E', 'Evening')
    ]

    paymentModes = [
        ('U', 'UPI'),
        ('A', 'Transfer to account')
    ]

    paymentProcessed = [
        ('P', 'Processed'),
        ('U', 'Unpaid')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullName = models.CharField(max_length=36, blank=False, default='')
    age = models.IntegerField(default='')
    gender = models.CharField(max_length=10, null=False, default='', choices=genderChoices)
    contactNumber = PhoneNumberField(default='', blank=False, null=False, unique=True)
    beginnerAtYoga = models.CharField(max_length=5, default='N', choices=beginner)
    purpose = models.TextField(max_length=256, null=True, blank=True, default='')
    ailment = models.TextField(max_length=100, null=True, blank=True, default='')
    packageSelection = models.CharField(max_length=5, default='M', choices=packagesOffered)
    batchTimingSelection = models.CharField(max_length=10, default='', choices=batchTimings)
    paymentMode = models.CharField(max_length=10, default='U', choices=paymentModes)
    paymentStatus = models.CharField(max_length=5, default='', choices=paymentProcessed)

    def __str__(self):

        first_name = self.fullName.split(' ')[0]
        return first_name


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = PhoneNumberField(default='', blank=False, null=False, unique=True)
    otp = models.CharField(max_length=6, default='******')
    uid = models.CharField(default=uuid.uuid4, max_length=200, unique=True, null=True, blank=True)
    country_code = models.CharField(max_length=50, default='+91')
    objects = models.Manager()
