from django.conf import settings
import vonage


class OTPHandler:

    phone_num = None
    otp = None

    def __init__(self, phone_num, otp) -> None:
        self.phone_num = phone_num
        self.otp = otp

    def send_otp_via_message(self):
        client = vonage.Client(key=settings.API_KEY, secret=settings.NEXMO_SECRET_KEY)
        sms = vonage.Sms(client)
        message = sms.send_message(
            {
                "from": f'Vonage APIs',
                "to": f'{self.phone_num}',
                "text": f'Hello from Yogshalaa :) Your OTP is: {self.otp}. Your OTP is valid for 10 minutes.',
            })
        print(f'Hello from Yogshalaa :) Your OTP for {self.phone_num} is {self.otp}. '
              f'This OTP is valid for 10 minutes only.')
        return message

    # def send_otp_via_whatsapp(self):
    #     client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
    #     message = client.messages.create(body=f'Your OTP is:{self.otp}', from_=f'{settings.TWILIO_WHATSAPP_NUMBER}',
    #                                      to=f'whatsapp:{settings.COUNTRY_CODE}{self.phone_num}')
