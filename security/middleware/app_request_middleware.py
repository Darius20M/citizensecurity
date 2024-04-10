from security.models import ApplicationModel


class AppRequestMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def extract_credentials(self, request):
        app_key = request.META.get('HTTP_X_APP_KEY', '')

        if not app_key:
            app_key = request.GET.get('app_key') or request.POST.get('app_key')

        return app_key

    def __call__(self, request):
        app_key = self.extract_credentials(request)

        try:
            request.application = ApplicationModel.objects.get(key=app_key)
        except ApplicationModel.DoesNotExist:
            request.application = None
        response = self.get_response(request)
        return response