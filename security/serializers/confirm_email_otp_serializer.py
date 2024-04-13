
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers

class ConfirmEmailOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(max_length=6)


    def validate_otp_code(self, value):
        """
        Check value of OTP code
        """
        if not value.isdigit() or len(value) != 6:
            raise serializers.ValidationError('The OTP code must be a 6-digit number.')
        return value

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            msg = _('No user found with provided email.')
            raise exceptions.ValidationError(msg)

        email = user.emailaddress_set.filter().first()
        if email.verified:
            msg = _('Email already verified.')
            raise exceptions.ValidationError(msg)

        attrs['email'] = email

        return attrs