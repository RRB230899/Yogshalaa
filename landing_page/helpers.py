import requests
import random
from django.conf import settings


class OTPHandler:

    phone_num = None
    otp = None

    def __int__(self, phone_num, otp):
        self.phone_num = phone_num
        self.otp = otp

