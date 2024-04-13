from dj_rest_auth.models import get_token_model
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.generics import GenericAPIView
from dj_rest_auth.utils import jwt_encode

from security.models import TwoFactorSettingsModel
from security.permissions import AppAuthenticatedPermission, AppStaffPermission
from security.serializers import VerificationCodeSerializer
from dj_rest_auth.views import sensitive_post_parameters_m
from django.contrib.auth import login as django_login
from dj_rest_auth.app_settings import api_settings
from rest_framework.response import Response
from rest_framework import status

from security.utils.session_handler import session_handler


class VerifyCodeViewSet(GenericAPIView):
    permission_classes = (
        AppAuthenticatedPermission,
        AppStaffPermission,
    )
    serializer_class = VerificationCodeSerializer
    throttle_scope = 'dj_rest_auth'

    user = None
    access_token = None
    token = None
    preference = None

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def get_response_serializer(self):
        if api_settings.USE_JWT:
            if api_settings.JWT_AUTH_RETURN_EXPIRATION:
                response_serializer = api_settings.JWT_SERIALIZER_WITH_EXPIRATION
            else:
                response_serializer = api_settings.JWT_SERIALIZER

        else:
            response_serializer = api_settings.TOKEN_SERIALIZER
        return response_serializer

    def login(self):
        self.user: User = self.serializer.validated_data['user']
        self.preference, created = TwoFactorSettingsModel.objects.get_or_create(user=self.user)
        self.preference.otp = ''
        self.preference.otp_expiry = None
        self.preference.token = ''
        self.preference.token_expiry = None
        self.preference.save()

        token_model = get_token_model()

        if api_settings.USE_JWT:
            self.access_token, self.refresh_token = jwt_encode(self.user)
            session_handler(token=self.access_token, user=self.user, request=self.request)
        elif token_model:
            self.token = api_settings.TOKEN_CREATOR(token_model, self.user, self.serializer)

        if api_settings.SESSION_LOGIN:
            self.process_login()

    def get_response(self):
        serializer_class = self.get_response_serializer()
        if api_settings.USE_JWT:
            from rest_framework_simplejwt.settings import (
                api_settings as jwt_settings,
            )
            access_token_expiration = (timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME)
            refresh_token_expiration = (timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME)
            return_expiration_times = api_settings.JWT_AUTH_RETURN_EXPIRATION
            auth_httponly = api_settings.JWT_AUTH_HTTPONLY

            data = {
                'user': self.user,
                'access': self.access_token,
            }

            if not auth_httponly:
                data['refresh'] = self.refresh_token
            else:
                # Wasnt sure if the serializer needed this
                data['refresh'] = ""

            if return_expiration_times:
                data['access_expiration'] = access_token_expiration
                data['refresh_expiration'] = refresh_token_expiration

            serializer = serializer_class(
                instance=data,
                context=self.get_serializer_context(),
            )
        elif self.token:
            serializer = serializer_class(
                instance=self.token,
                context=self.get_serializer_context(),
            )
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

        response = Response(serializer.data, status=status.HTTP_200_OK)
        if api_settings.USE_JWT:
            from dj_rest_auth.jwt_auth import set_jwt_cookies
            set_jwt_cookies(response, self.access_token, self.refresh_token)
        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()
