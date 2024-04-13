from datetime import timedelta
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from django_otp.plugins.otp_email.models import EmailDevice
from rest_framework import status
from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from security.handlers import send_otp_verification_email
from security.permissions import AppStaffPermission, AppAuthenticatedPermission
from security.serializers.resend_confirm_email_serializer import ResendConfirmEmailSerializer


class ResendConfirmEmailViewSet(GenericAPIView):
    permission_classes = (
        AppAuthenticatedPermission,
        AppStaffPermission
    )
    serializer_class = ResendConfirmEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data.get('email'))
        resend_limit = 5
        resend_time_window = timezone.now() - timedelta(minutes=30)
        device = EmailDevice.objects.filter(user=user, confirmed=False).order_by('-last_generated_timestamp').first()

        recent_resends_count = EmailDevice.objects.filter(
            user=user,
            last_generated_timestamp__gte=resend_time_window,
            confirmed=False
        ).count()

        if recent_resends_count >= resend_limit:
            time_remaining = (device.last_generated_timestamp + timedelta(minutes=30)) - timezone.now()
            return Response({'success': False,
                             'message': f'Resend limit has been reached. Please try again in {int(time_remaining.total_seconds() // 60)} minutes.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:

            send_otp_verification_email(user)
            return Response({'success': True, 'message': _('Email verification has been sent to your email')},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
