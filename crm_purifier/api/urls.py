from django.urls import path
from .views import LoginAPIView, EmployeeProfileAPIView, PasswordChangeAPIView, PasswordResetRequestAPIView, PasswordResetAPIView, CustomerAPIView, TestAPIView, ServiceWorkAPIView, CustomerProfileAPIView, CustomerServiceWorkAPIView, CustomerProductsAPIView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'api'

urlpatterns = [
    
    path('login/', LoginAPIView.as_view(), name='login'),
    path('password_change/', PasswordChangeAPIView.as_view(), name='password_change'),
    path('password_reset_request/', PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('password_reset/<uidb64>/<token>/', PasswordResetAPIView.as_view(), name='password_reset'),
    
    # for employees
    path('employee_profile/', EmployeeProfileAPIView.as_view(), name='employee_profile'),
    path('customers/', CustomerAPIView.as_view()),
    path('customers/<uuid:id>/', CustomerAPIView.as_view()),
    path('tests/', TestAPIView.as_view()),
    path('tests/<uuid:id>/', TestAPIView.as_view()),
    path('serviceworks/', ServiceWorkAPIView.as_view()),
    path('serviceworks/<uuid:id>/', ServiceWorkAPIView.as_view()),
    
    # for customers
    path('customer_profile/', CustomerProfileAPIView.as_view()),
    path('customer_serviceworks/', CustomerServiceWorkAPIView.as_view()),
    path('customer_products/', CustomerProductsAPIView.as_view()),
]
