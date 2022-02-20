# users/custom_backends.py
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class NdoptorAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, *args, **kwargs):

        # username_eng = kwargs.get('name_eng')
        # username_bng = kwargs.get('name_bng')
        is_active = kwargs.get('is_active')

        # if not username_eng:
        #     if username_bng:
        #         username_eng = username_bng
        #     else:
        #         username_eng = username

        try:
            user = User.objects.get(username=username)
            # user.username_eng = username_eng
            # user.save()
        except User.DoesNotExist:
            user = User.objects.create(username=username, is_active=is_active)
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
