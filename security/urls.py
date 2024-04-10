from django.urls import re_path
from rest_framework.routers import DefaultRouter

from security.views import ApplicationViewSet, UserViewSet

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [

]
urlpatterns += router.urls