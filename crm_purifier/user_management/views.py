# from django.shortcuts import render, redirect
# # from .forms import LoginForm
# from django.contrib.auth import login
# from .backends import CustomUserBackend
# from django.core.validators import validate_email
# from django.core.exceptions import ValidationError
# from django.contrib.auth import authenticate

# # Create your views here.
# def adminLogin(request):
    
#     # login_form = LoginForm()
    
#     if request.method == 'POST':
        
#         username_or_email = request.POST['username']
#         password = request.POST['password']
        
#         print(username_or_email)
#         print(password)
        
#         if username_or_email is not None and password is not None:
            
#             # try:
#                 # validate_email(username_or_email)
#                 # user = CustomUserBackend().authenticate(request, email=username_or_email, password=password)
#             # except ValidationError:
#             user = CustomUserBackend().authenticate(request, username='purifier', password='Water@123')
#             # user = CustomUserBackend().authenticate(request, username=username_or_email, password=password)
            
#             print(user)
                
#             if user is not None and user.is_superuser:
#                 login(request, user)
#                 return redirect('purifier:view_dashboard')
#             else:
#                 error_message = "Invalid username or password."
#                 return render(request, 'registration/login.html', {'error_message': error_message})
    
#     return render(request, 'registration/login.html')




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
                return redirect('user_management:admin_login')

    return render(request, 'registration/login.html')

