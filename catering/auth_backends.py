from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self, request, **credentials):
        UserModel = get_user_model()
        email = credentials.get('email')
        password = credentials.get('password')
        if email is None or password is None:
            return None

        try:
            user = UserModel._default_manager.get(email__iexact=email)
        except UserModel.DoesNotExist:
            return None
        except UserModel.MultipleObjectsReturned:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None