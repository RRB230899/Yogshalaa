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
    

class Pricing(models.Model):
    COUNTRY_CHOICES = [
        ("+44", "United Kingdom"),
        ("+91", "India"),
        ("+1", "United States"),
        ("+31", "Netherlands"),
        ("+49", "Germany"),
        ("+33", "France"),
        ("+39", "Italy"),
        ("+34", "Spain"),
    ]

    country_code = models.CharField(max_length=5, choices=COUNTRY_CHOICES)
    currency_symbol = models.CharField(max_length=5, default="₹")
    discount = models.CharField(max_length=20, blank=True, null=True)

    # Stripe Price IDs
    weekend_flow_price_id = models.CharField(max_length=100, blank=True, null=True)
    personalized_flow_price_id = models.CharField(max_length=100, blank=True, null=True)
    morning_monthly_price_id = models.CharField(max_length=100, blank=True, null=True)
    morning_quarterly_price_id = models.CharField(max_length=100, blank=True, null=True)

    # Local display prices
    regular_monthly = models.DecimalField(max_digits=10, decimal_places=2)
    regular_quarterly = models.DecimalField(max_digits=10, decimal_places=2)
    personalized_sessions = models.DecimalField(max_digits=10, decimal_places=2)
    weekend_flow = models.DecimalField(max_digits=10, decimal_places=2)

    batch_timing1 = models.CharField(max_length=100, blank=True, null=True)
    batch_timing2 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Pricing for {self.get_country_code_display()}"
