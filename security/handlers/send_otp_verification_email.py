from datetime import timedelta
from django.utils import timezone
from django_otp.plugins.otp_email.models import EmailDevice



def send_otp_verification_email(user, context={}):
    """
    Genera un código OTP y lo envía al usuario por correo electrónico.
    """
    device = EmailDevice.objects.create(user=user, email=user.email, confirmed=False)
    device.generate_challenge(context)
    device.valid_until = timezone.now() + timedelta(hours=1)
    device.save()
