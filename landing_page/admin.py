from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(YogaUserMorning)
class YogshalaaByJJ(admin.ModelAdmin):
    fields = ['profile', 'batch_choice', 'date_of_joining']
    list_display = ['batch_choice', 'date_of_joining']
    list_filter = ['batch_choice', 'date_of_joining']


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    fields = ['user', 'mobile', 'uid', 'country_code', 'is_verified']
    list_display = ['user', 'mobile', 'is_verified']
    search_fields = ['mobile']


@admin.register(TrialClassUserPreferences)
class TrialClassPreferenceData(admin.ModelAdmin):
    fields = ['profile', 'phone_num', 'focus_choices', 'style_choices']
    list_display = ['phone_num']
    search_fields = ['phone_num']
