import random

from django.conf import settings
from django.core.mail import send_mail

from apps.users.models import EmailOTP


def send_welcome_email(to_email, name):
    subject = "Welcome to FlexHire!"
    message = f"Hi {name},\n\nThanks for registering with us.\n\nBest,\nThe FlexHire Team"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [to_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


def send_otp(to_email, name):
    otp = random.randint(100000, 999999)
    subject = f"Your OTP {otp}"
    message = f"Hi {name},\n\nUse {otp} for registration.\n\nBest,\nThe FlexHire Team"
    from_email = settings.EMAIL_HOST_USER

    send_mail(subject, message, from_email, [to_email], fail_silently=False)

    # Save or update OTP record
    EmailOTP.objects.update_or_create(email=to_email, defaults={"otp": str(otp)})
    return otp


def send_application_status_email(worker_email, worker_name, job_title, status):
    """
    Notify a worker about acceptance or rejection of their job application.

    Args:
        worker_email (str): Email address of the worker.
        worker_name (str): Full name of the worker.
        job_title (str): Title of the job the worker applied for.
        status (str): One of 'accepted' or 'rejected'.

    Returns:
        None
    """
    if status == "accepted":
        subject = f"Your application for '{job_title}' has been accepted!"
        message = (
            f"Hi {worker_name},\n\n"
            f"Congratulations! Your application for the job '{job_title}' has been accepted.\n"
            "Please contact the customer to coordinate further.\n\n"
            "Best,\nFlexHire Team"
        )
    elif status == "rejected":
        subject = f"Your application for '{job_title}' has been rejected"
        message = (
            f"Hi {worker_name},\n\n" f"We regret to inform you that your application for the job '{job_title}' has been rejected.\n\n" "Best,\nFlexHire Team"
        )
    else:
        return  # Invalid status, do nothing

    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [worker_email], fail_silently=False)
