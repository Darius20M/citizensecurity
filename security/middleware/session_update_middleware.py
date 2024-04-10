from re import sub

from django.utils import timezone

from security.models import SessionModel


class SessionUpdateMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        header_token = request.META.get('HTTP_AUTHORIZATION', None)

        if header_token is None:
            request.token = request.GET.get('jwt') or request.GET.get('token')
        else:
            token = sub('Bearer ', '', header_token)
            request.token = token

        if request.token is not None:
            SessionModel.objects.filter(token=token).update(last_activity=timezone.now())

        response = self.get_response(request)
        return response