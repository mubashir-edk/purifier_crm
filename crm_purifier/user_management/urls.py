from django.urls import path
from . import views

app_name = 'user_management'

urlpatterns = [
    
    # Login
    path('admin_login/', views.adminLogin, name='admin_login'),

]
