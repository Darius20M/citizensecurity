from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from rest_framework import serializers, exceptions
from django.utils.translation import gettext_lazy as _
from django.urls import exceptions as url_exceptions
from django.conf import settings

from security.models import TwoFactorSettingsModel

# Get the UserModel
UserModel = get_user_model()


class VerificationCodeSerializer(serializers.Serializer):
    token = serializers.CharField(required=True, allow_blank=False)
    otp = serializers.CharField(required=True, allow_blank=False)

    def authenticate_username_or_email(self, username=None, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is not None:
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return None
        else:
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password):
            return user
        return None

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        if email and password:
            user = self.authenticate_username_or_email(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        if email and password:
            user = self.authenticate_username_or_email(email=email, password=password)
        elif username and password:
            user = self.authenticate_username_or_email(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def get_auth_user_using_allauth(self, username, email, password):
        from allauth.account import app_settings as allauth_account_settings

        # Authentication through email
        if allauth_account_settings.AUTHENTICATION_METHOD == allauth_account_settings.AuthenticationMethod.EMAIL:
            return self._validate_email(email, password)

        # Authentication through username
        if allauth_account_settings.AUTHENTICATION_METHOD == allauth_account_settings.AuthenticationMethod.USERNAME:
            return self._validate_username(username, password)

        # Authentication through either username or email
        return self._validate_username_email(username, email, password)

    def get_auth_user_using_orm(self, username, email, password):
        if email:
            try:
                username = UserModel.objects.get(email__iexact=email).get_username()
            except UserModel.DoesNotExist:
                pass

        if username:
            return self._validate_username_email(username, '', password)

        return None

    def get_auth_user(self, username, email, password):
        """
        Retrieve the auth user from given POST payload by using
        either `allauth` auth scheme or bare Django auth scheme.

        Returns the authenticated user instance if credentials are correct,
        else `None` will be returned
        """
        if 'allauth' in settings.INSTALLED_APPS:

            # When `is_active` of a user is set to False, allauth tries to return template html
            # which does not exist. This is the solution for it. See issue #264.
            try:
                return self.get_auth_user_using_allauth(username, email, password)
            except url_exceptions.NoReverseMatch:
                msg = _('Unable to log in with provided credentials.')
                raise exceptions.ValidationError(msg)
        return self.get_auth_user_using_orm(username, email, password)

    @staticmethod
    def validate_auth_user_status(user):
        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.ValidationError(msg)

    @staticmethod
    def validate_email_verification_status(user, email=None):
        from allauth.account import app_settings as allauth_account_settings
        if (
            allauth_account_settings.EMAIL_VERIFICATION == allauth_account_settings.EmailVerificationMethod.MANDATORY
            and not user.emailaddress_set.filter(email=user.email, verified=True).exists()
        ):
            raise serializers.ValidationError(_('E-mail is not verified.'))

    def validate(self, attrs):
        token = attrs.get('token')
        otp = attrs.get('otp')

        two_factor = TwoFactorSettingsModel.objects.filter(token=token).first()

        if two_factor and two_factor.is_blocked():
            msg = _('Your account is temporarily blocked due to multiple failed attempts. Please try again later.')
            raise exceptions.ValidationError(msg)

        if two_factor is None or two_factor.token_expiry is None or two_factor.token_expiry < timezone.now():
            msg = _('Invalid token')
            if two_factor:
                two_factor.register_failed_attempt()
            raise exceptions.ValidationError(msg)

        user = two_factor.user

        self.validate_auth_user_status(user)

        if not (
                two_factor.otp == otp and two_factor.otp_expiry is not None and two_factor.otp_expiry > timezone.now()):
            msg = _('Invalid verification code')
            two_factor.register_failed_attempt()
            raise exceptions.ValidationError(msg)

        if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
            self.validate_email_verification_status(user, email=user.email)

        two_factor.reset_failed_attempts()

        attrs['user'] = user
        return attrs
