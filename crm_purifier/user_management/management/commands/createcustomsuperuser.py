# from django.contrib.auth.management.commands import createsuperuser
# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext as _
# from user_management.models import CustomUser

# class Command(createsuperuser.Command):
#     help = 'Create a superuser with a custom user model.'

#     def add_arguments(self, parser):
#         super().add_arguments(parser)
#         parser.add_argument('--email', required=True, help='Specifies the email for the superuser.')

#     def handle(self, *args, **options):
#         self.email = options['email']
#         print(self.email)
#         try:
#             self.UserModel = CustomUser
#             super().handle(*args, **options)
#         except ValidationError as e:
#             self.stderr.write(str(e))
#             return


# myapp/management/commands/create_custom_superuser.py

from django.contrib.auth.management.commands import createsuperuser
from django.core.exceptions import ValidationError
from user_management.models import CustomUser

class Command(createsuperuser.Command):
    help = 'Create a superuser with a custom user model.'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--email', required=True, help='Specifies the email for the superuser.')
        parser.add_argument('--password', required=True, help='Specifies the password for the superuser.')

    def handle(self, *args, **options):
        self.email = options['email']
        try:
            self.UserModel = CustomUser
            username = options[self.UserModel.USERNAME_FIELD]
            password = options['password']
            user_data = {
                'username': username,
                'password': password,
                'email': self.email,
            }
            self.UserModel._default_manager.create_superuser(**user_data)
            if options['verbosity'] >= 1:
                self.stdout.write("Superuser created successfully.")
        except ValidationError as e:
            self.stderr.write(str(e))
            return
