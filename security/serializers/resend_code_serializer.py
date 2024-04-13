from django.utils import timezone
from rest_framework import serializers, exceptions
from django.utils.translation import gettext_lazy as _

from security.handlers.send_email import send_email
from security.models import TwoFactorSettingsModel


class ResendCodeSerializer(serializers.Serializer):
    token = serializers.CharField(required=True, allow_blank=False)
    phone = serializers.BooleanField(required=False)
    email = serializers.BooleanField(required=False)

    def validate(self, attrs):
        token = attrs.get('token')
        two_factor = TwoFactorSettingsModel.objects.filter(token=token).first()
        if two_factor is None or two_factor.token_expiry is None or two_factor.token_expiry < timezone.now():
            msg = _('Unable to resend code, please login again')
            raise exceptions.ValidationError(msg)

        two_factor.generate()
        attrs['preference'] = two_factor

        send_email(subject="Two Factor Verification Code",
                   html_path='twofactor/two_factor.html',
                   context={
                       'otp': two_factor.otp
                   },
                   obj=two_factor
                   )
        return attrs
