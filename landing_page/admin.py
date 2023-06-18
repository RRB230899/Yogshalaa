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
admin.site.register(Profile)
