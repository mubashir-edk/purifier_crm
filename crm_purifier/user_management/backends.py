from django.contrib.auth.backends import BaseBackend
from .models import CustomUser

class CustomUserBackend(BaseBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        if username:
            user = CustomUser.objects.filter(username=username).first()
            print(user)
        elif email:
            user = CustomUser.objects.filter(email=email).first()
            print(user)
        else:
            return None  # Neither email nor username provided

        # if user and user.check_password(password):
        if user:
            print(f'the data is here already {user}')
            return user  # Return the user object if authentication is successful
        return None  # Return None if authentication fails

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
