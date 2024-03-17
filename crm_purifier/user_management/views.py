from django.shortcuts import render, redirect
from .backends import CustomUserBackend
from django.contrib.auth import login
from django.core.exceptions import ValidationError

def adminLogin(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        if username_or_email and password:
            if '@' in username_or_email:
                # Assume it's an email
                user = CustomUserBackend().authenticate(request, email=username_or_email, password=password)
                print(f'email {user} password {password}')
            else:
                # Assume it's a username
                user = CustomUserBackend().authenticate(request, username=username_or_email, password=password)
                print(f'username {user} password {password}')

            if user is not None and user.is_superuser:
                # login(request, user)
                login(request, user, backend='user_management.backends.CustomUserBackend')
                return redirect('purifier:view_dashboard')
            else:
                error_message = "Invalid username or password."
                return render(request, 'registration/login.html', {'error_message': error_message})

    return render(request, 'registration/login.html')

