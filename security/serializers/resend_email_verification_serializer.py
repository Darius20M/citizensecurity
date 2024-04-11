from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers


class ResendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email).first()
        if not user:
            msg = _('No user found with provided email.')
            raise exceptions.ValidationError(msg)

        email = user.emailaddress_set.filter().first()
        attrs['email'] = email

        return attrs
