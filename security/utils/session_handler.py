from django.conf import settings
from django.utils import timezone
from django.utils.timezone import localtime

from security.models import SessionModel
from security.utils.get_client_ip import get_client_ip


def session_handler(token, user, request):
    # GET IP
    client_ip = get_client_ip(request)
    session_exists = True

    session = SessionModel.objects.filter(user=user, token=token).first()

    if session is None:
        session = SessionModel.objects.filter(token=token).first()

    if session is None:
        session = SessionModel.objects.filter(user=user, ip_address=client_ip, application=request.application).first()

    if session is None:
        session = SessionModel.objects.filter(user=user, application=request.application).first()

    if session is None:
        session_exists = False
        session = SessionModel()
        session.ip_address = client_ip
        session.application = request.application
        session.user = user
        session.offline = True
        session.token = token
        session.device = 'unknown'

        if request.user_agent.device.model is not None:
            session.device = request.user_agent.device.model

        session.browser = request.user_agent.browser.family
        session.browser_version = request.user_agent.browser.version_string
        session.system_operation = request.user_agent.os.family
        session.system_operation_version = request.user_agent.os.version_string
        session.last_activity = timezone.now()
        session.expire = timezone.now() + settings.USER_SESSION_EXPIRE_TIME

        if request.user_agent.is_mobile:
            session.device_type = 'mobile'
        elif request.user_agent.is_pc:
            session.device_type = 'pc'
        elif request.user_agent.is_bot:
            session.device_type = 'bot'
        elif request.user_agent.is_tablet:
            session.device_type = 'tablet'
        elif request.user_agent.is_touch_capable:
            session.device_type = 'touch_capable'
        else:
            session.device_type = 'unknown'

        session.save()

    if session_exists:
        now = localtime(timezone.now())
        session.expire = now + settings.USER_SESSION_EXPIRE_TIME
        session.previous_token = session.token
        session.token = token
        session.last_activity = now
        session.ip_address = client_ip
        session.device = 'unknown'

        if request.user_agent.device.model is not None:
            session.device = request.user_agent.device.model

        session.browser = request.user_agent.browser.family
        session.browser_version = request.user_agent.browser.version_string
        session.system_operation = request.user_agent.os.family
        session.system_operation_version = request.user_agent.os.version_string

        if request.user_agent.is_mobile:
            session.device_type = 'mobile'
        elif request.user_agent.is_pc:
            session.device_type = 'pc'
        elif request.user_agent.is_bot:
            session.device_type = 'bot'
        elif request.user_agent.is_tablet:
            session.device_type = 'tablet'
        elif request.user_agent.is_touch_capable:
            session.device_type = 'touch_capable'
        else:
            session.device_type = 'unknown'
        session.save()

    return session