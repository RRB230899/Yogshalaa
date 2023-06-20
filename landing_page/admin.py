from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(YogaUser)
class YogshalaaByJJ(admin.ModelAdmin):
    fields = ['fullName', 'age', 'gender', 'contactNumber', 'beginnerAtYoga', 'purpose',
              'ailment', 'packageSelection', 'batchTimingSelection', 'paymentMode', 'paymentStatus']
    list_display = ['fullName', 'contactNumber', 'paymentStatus']
    list_filter = ['paymentStatus', 'paymentMode', 'batchTimingSelection', 'packageSelection']
    search_fields = ['fullName']


# admin.site.register(UserOTP)
@admin.register(Profile)
class Profile(admin.ModelAdmin):
    fields = ['user', 'mobile', 'otp', 'uid', 'country_code']
    list_display = ['user', 'mobile']
    search_fields = ['mobile']


@admin.register(TrialClassUserPreferences)
class TrialClassPreferenceData(admin.ModelAdmin):
    fields = ['profile', 'phone_num', 'focus_choices', 'style_choices']
    list_display = ['phone_num']
    search_fields = ['phone_num']
