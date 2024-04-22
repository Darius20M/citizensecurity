
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from security.views.social_login_viewset import SocialLoginViewSet


class GoogleAuthViewSet(SocialLoginViewSet):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'https://portal.ucsd.edu.do/escuela-de-informatica/'
    client_class = OAuth2Client