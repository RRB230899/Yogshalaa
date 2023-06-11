from django.conf import settings
from twilio.rest import Client


class OTPHandler:

    phone_num = None
    otp = None
    country_code = None

    def __init__(self, phone_num, otp, country_code) -> None:
        self.phone_num = phone_num
        self.otp = otp

    def send_otp_via_message(self):
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
        message = client.messages.create(
            body=f'Hello from Yogshalaa :) Your OTP is: {self.otp}. Your OTP is valid for 10 minutes.',
            from_=f'{settings.TWILIO_PHONE_NUMBER}',
            to=f'{self.phone_num}')
        print(f'Hello from Yogshalaa :) Your OTP for {self.phone_num} is {self.otp}. '
              f'This OTP is valid for 10 minutes only.')
        return message

    # def send_otp_via_whatsapp(self):
    #     client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
    #     message = client.messages.create(body=f'Your OTP is:{self.otp}', from_=f'{settings.TWILIO_WHATSAPP_NUMBER}',
    #                                      to=f'whatsapp:{settings.COUNTRY_CODE}{self.phone_num}')
