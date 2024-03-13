from django.urls import path
from .views import EmployeeLoginAPIView, EmployeeProfileAPIView, PasswordChangeAPIView, PasswordResetRequestAPIView, PasswordResetAPIView, CustomerAPIView, TestAPIView, ServiceWorkAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'api'

urlpatterns = [
    
    path('employee_login/', EmployeeLoginAPIView.as_view(), name='employee_login'),
    path('employee_profile/', EmployeeProfileAPIView.as_view(), name='employee_profile'),
    path('password_change/', PasswordChangeAPIView.as_view(), name='password_change'),
    path('password_reset_request/', PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('password_reset/<uidb64>/<token>/', PasswordResetAPIView.as_view(), name='password_reset'),
    
    path('customers/', CustomerAPIView.as_view()),
    path('customers/<uuid:id>/', CustomerAPIView.as_view()),
    
    path('tests/', TestAPIView.as_view()),
    path('tests/<uuid:id>/', TestAPIView.as_view()),
    
    path('serviceworks/', ServiceWorkAPIView.as_view()),
    path('serviceworks/<uuid:id>/', ServiceWorkAPIView.as_view()),
]
