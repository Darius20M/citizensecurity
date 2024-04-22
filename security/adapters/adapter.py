
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth.models import User

from security.handlers import send_otp_verification_email


class CustomAccountAdapter(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context, subject=None):
        user = User.objects.get(email=email)
        ctx = {
            'user': user,
        }
        send_otp_verification_email(user=user, context=context)
