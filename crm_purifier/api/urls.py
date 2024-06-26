from django.urls import path
from .views import LoginAPIView, LogoutAPI, RefreshTokenApi, EmployeeProfileAPIView, PasswordChangeAPIView, PasswordResetRequestAPIView, PasswordResetAPIView, CustomerAPIView, TestAPIView, ServiceWorkAPIView, CustomerProfileAPIView, CustomerServiceWorkAPIView, CustomerProductsAPIView, ServiceWorkDueAPIView, employeeNotificationAPIView, customerNotificationAPIView, ProductAPIView

app_name = 'api'

urlpatterns = [
    
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('refresh_token/', RefreshTokenApi.as_view(), name='refresh_token'),
    path('password_change/', PasswordChangeAPIView.as_view(), name='password_change'),
    path('password_reset_request/', PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('password_reset/<uidb64>/<token>/', PasswordResetAPIView.as_view(), name='password_reset'),
    
    path('products/', ProductAPIView.as_view(), name='product'),
    path('product/<uuid:id>/', ProductAPIView.as_view(), name='product'),
    
    # for employees
    path('employee_profile/', EmployeeProfileAPIView.as_view(), name='employee_profile'),
    path('customers/', CustomerAPIView.as_view()),
    path('customer/<uuid:id>/', CustomerAPIView.as_view()),
    path('tests/', TestAPIView.as_view()),
    path('test/<uuid:id>/', TestAPIView.as_view()),
    path('serviceworks/', ServiceWorkAPIView.as_view()),
    path('servicework/<uuid:id>/', ServiceWorkAPIView.as_view()),
    path('serviceworks_due/', ServiceWorkDueAPIView.as_view()),
    path('employee_notifications/', employeeNotificationAPIView.as_view()),
    
    # for customers
    path('customer_profile/', CustomerProfileAPIView.as_view()),
    path('customer_serviceworks/', CustomerServiceWorkAPIView.as_view()),
    path('customer_servicework/<uuid:id>/', CustomerServiceWorkAPIView.as_view()),
    path('customer_products/', CustomerProductsAPIView.as_view()),
    path('customer_product/<uuid:id>/', CustomerProductsAPIView.as_view()),
    path('customer_notifications/', customerNotificationAPIView.as_view()),
]
