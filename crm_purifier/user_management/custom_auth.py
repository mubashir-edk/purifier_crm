# from django.contrib.auth.backends import ModelBackend
# from django.contrib.auth import get_user_model

# class EmailOrUsernameModelBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         User = get_user_model()
#         try:
#             # Check if the input is an email address
#             user = User.objects.get(email=username)
#         except User.DoesNotExist:
#             try:
#                 # Check if the input is a username
#                 user = User.objects.get(username=username)
#             except User.DoesNotExist:
#                 # Neither username nor email exists
#                 return None
#         # Check the password
#         if user.check_password(password):
#             return user
#         return None
