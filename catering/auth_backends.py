from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        identifier = username or kwargs.get(UserModel.USERNAME_FIELD)
        if identifier is None or password is None:
            return None

        try:
            user = UserModel._default_manager.get(email__iexact=identifier)
        except UserModel.DoesNotExist:
            return super().authenticate(
                request, username=identifier, password=password, **kwargs
            )
        except UserModel.MultipleObjectsReturned:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None