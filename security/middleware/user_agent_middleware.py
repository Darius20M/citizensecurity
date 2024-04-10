from django.utils.functional import SimpleLazyObject

from security.utils import get_user_agent


class UserAgentMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
    # A middleware that adds a "user_agent" object to request

    def __call__(self, request):
        request.user_agent = SimpleLazyObject(lambda: get_user_agent(request))
        response = self.get_response(request)
        return response