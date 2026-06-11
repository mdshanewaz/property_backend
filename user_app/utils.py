import random, string
from django.conf import settings
from django.core.mail import send_mail

# OTP generation
def otp_generator():
    length=6
    character = string.ascii_letters + string.digits
    otp = ''.join(random.choices(character, k=length))

    return otp


# OTP sending by mail
def send_otp_mail(user, email, otp):
    subject = 'OTP from Luxora Estates'
    message = f'Hello {user}, Your OTP is : {otp}'
    from_email = settings.EMAIL_HOST_USER
    to_email = email

    send_mail(subject, message, from_email, [to_email])
