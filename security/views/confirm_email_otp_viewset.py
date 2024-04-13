from django.contrib.auth.models import User
from django.utils import timezone
from django_otp import devices_for_user
from django_otp.forms import OTPAuthenticationForm
from django_otp.plugins.otp_email.models import EmailDevice
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from security.permissions import AppAuthenticatedPermission, AppStaffPermission
from security.serializers import ConfirmEmailOTPSerializer


class ConfirmEmailOTPViewSet(GenericAPIView):
    permission_classes = (
        AppAuthenticatedPermission,
        AppStaffPermission,
    )
    serializer_class = ConfirmEmailOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = ConfirmEmailOTPSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data.get('email'))
            otp_code = serializer.validated_data.get('otp_code')

            device = EmailDevice.objects.filter(user=user, confirmed=False).order_by(
                '-last_generated_timestamp').first()
            if not device:
                return Response({'success': False, 'message': 'It does not have a verification code assigned.'},
                                status=status.HTTP_400_BAD_REQUEST)

            if not timezone.now() <= device.valid_until:
                return Response(
                    {'success': False, 'message': 'The OTP code has expired. Please request a new one.'},
                    status=status.HTTP_400_BAD_REQUEST)

            MAX_FAILURE_COUNT = 5
            THROTTLE_PERIOD_MINUTES = 30

            if device.throttling_failure_count >= MAX_FAILURE_COUNT:
                last_failure_time = device.throttling_failure_timestamp
                # We check if the 30 minute waiting period has passed
                if last_failure_time and timezone.now() - last_failure_time < timezone.timedelta(
                        minutes=THROTTLE_PERIOD_MINUTES):
                    minutes= timezone.timedelta(minutes=THROTTLE_PERIOD_MINUTES)-(timezone.now() - last_failure_time)
                    remaining_minutes = int(minutes.total_seconds() // 60)
                    return Response({'success': False, 'message': f'Wait {remaining_minutes} minutes before trying again.'},
                                    status=status.HTTP_429_TOO_MANY_REQUESTS)
                else:
                    # If 30 minutes have passed, we reset the counter of failed attempts
                    device.throttling_failure_count = 0
                    device.save()

            if isinstance(device, EmailDevice) and device.verify_token(otp_code):

                device.confirmed = True
                device.save()
                user.emailaddress_set.filter(email=user.email).update(verified=True)
                return Response({'success': True, 'message': 'Your email has been successfully verified.'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'message': 'The OTP code is incorrect. Try again.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
