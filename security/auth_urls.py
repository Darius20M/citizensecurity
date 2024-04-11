from django.urls import path

from dj_rest_auth.app_settings import api_settings

from security.views import PasswordResetViewSet, PasswordResetConfirmViewSet, LoginViewSet, LogoutViewSet, \
    UserDetailsViewSet, PasswordChangeViewSet, VerifyCodeViewSet, ResendCodeViewSet
from security.views.check_password_viewset import CheckPasswordViewSet

urlpatterns = [
    # URLs that do not require a session or valid token
    path('password/reset/', PasswordResetViewSet.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/<str:user_id>/<str:temp_key>/', PasswordResetConfirmViewSet.as_view(), name='password_reset_confirm'),
    path('login/', LoginViewSet.as_view(), name='rest_login'),
    path('verification_code/', VerifyCodeViewSet.as_view(), name='rest_verification_code'),
    # URLs that require a user to be logged in with a valid session / token.
    path('logout/', LogoutViewSet.as_view(), name='rest_logout'),
    path('user/', UserDetailsViewSet.as_view(), name='rest_user_details'),
    path('check_password/', CheckPasswordViewSet.as_view(), name='check_password'),
    path('password/change/', PasswordChangeViewSet.as_view(), name='rest_password_change'),
    path('resend_verification_code/', ResendCodeViewSet.as_view(), name="resend_verification_code")
]

if api_settings.USE_JWT:
    from rest_framework_simplejwt.views import TokenVerifyView

    from dj_rest_auth.jwt_auth import get_refresh_view

    urlpatterns += [
        path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
        path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    ]
