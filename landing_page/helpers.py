import requests
import random
from django.conf import settings
from twilio.rest import Client


class OTPHandler:

    phone_num = None
    otp = None

    def __init__(self, phone_num, otp) -> None:
        self.phone_num = phone_num
        self.otp = otp

    def send_otp_via_message(self):
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
        message = client.messages.create(body=f'Your OTP is:{self.otp}', from_=f'{settings.TWILIO_PHONE_NUMBER}',
                                         to=f'{settings.COUNTRY_CODE}{self.phone_num}')

    # def send_otp_via_whatsapp(self):
    #     client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
    #     message = client.messages.create(body=f'Your OTP is:{self.otp}', from_=f'{settings.TWILIO_WHATSAPP_NUMBER}',
    #                                      to=f'whatsapp:{settings.COUNTRY_CODE}{self.phone_num}')

