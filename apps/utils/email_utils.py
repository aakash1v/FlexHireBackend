import random
from apps.users.models import EmailOTP
from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(to_email, name):
    subject = "Welcome to FlexHire!"
    message = f"Hi {name},\n\nThanks for registering with us.\n\nBest,\nThe FlexHire Team"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [to_email]

    send_mail(subject, message, from_email,
              recipient_list, fail_silently=False)


def send_otp(to_email, name):
    otp = random.randint(100000, 999999)
    subject = f"Your OTP {otp}"
    message = f"Hi {name},\n\nUse {otp} for registration.\n\nBest,\nThe FlexHire Team"
    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, [to_email], fail_silently=False)

    # Save or update OTP record
    EmailOTP.objects.update_or_create(
        email=to_email,
        defaults={"otp": str(otp)}
    )
    return otp
