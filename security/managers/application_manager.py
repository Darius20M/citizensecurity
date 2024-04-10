from django.contrib.auth.models import User
from django.db import models


class ApplicationManager(models.Manager):
    def create_application(self, app_name, username, email, password, **kwargs):
        # Create user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except:
            raise ValueError('The user could not be created')

        if user:
            app = self.model(name=app_name, user=user, is_staff=False)
            app.save()
            return app

    def create_application_user(self, app_name, user_id, **kwargs):

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValueError('The user no exists')

        if user:
            app = self.model(name=app_name, user=user, is_staff=False)
            app.save()
            return app

    def create_application_staff(self, app_name, user_id, **kwargs):

        user = None
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise ValueError('The user no exists')

        if not user.is_active:
            raise ValueError('The user is not active')

        if not user.is_superuser:
            raise ValueError('The user is not super user.')

        app = self.model(name=app_name, user=user, is_staff=True)
        app.save()

        return app