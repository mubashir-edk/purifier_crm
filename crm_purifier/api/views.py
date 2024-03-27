from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from user_management.permissions import CustomIsAuthenticated, EmployeeIsAuthenticated, CustomerIsAuthenticated

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.exceptions import NotFound

from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from purifier.models import Employee, Customer, Test, ServiceWork, CustomerProduct, ServiceAssign, Servicer, EmployeeNotification, CustomerNotification
from api.models import StoreRefreshToken
from user_management.backends import CustomUserBackend
from .serializers import CustomUserSerializer, EmployeeSerializer, CustomerSerializer, TestSerializer, ServiceWorkSerializer, CustomerProductSerializer,EmployeeNotificationSerializer, CustomerNotificationSerializer
from django.utils import timezone

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username_or_email = request.data.get('username')
        password = request.data.get('password')
        
        print(username_or_email)
        print(password)
        
        user = CustomUserBackend().authenticate(request, username=username_or_email, password=password)
        
        if not user:
            try:
                user = CustomUserBackend().authenticate(request, email=username_or_email, password=password)
            except User.DoesNotExist:
                pass
            
            print(user)

        if user:
            print("user is there")
            # Authentication successful, generate tokens
            token = get_tokens_for_user(user)
            StoreRefreshToken.objects.update_or_create(user=user, defaults={'token': token['refresh']})
            
            user_serializer = CustomUserSerializer(user)
            
            return Response({'access_token': token['access'], 'user': user_serializer.data, 'msg': 'Login successful'})
            
        else:
            # Authentication failed
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutAPI(APIView):
    
    permission_classes = [CustomIsAuthenticated]
    
    def post(self,request):
        
        refresh_token = request.data.get('refresh')
        if refresh_token is None:
            return Response({'error': 'Refresh token is required'})
        
        token = get_object_or_404(StoreRefreshToken, token=refresh_token)
        
        if token:
            token.delete()
            return Response({'success': 'logout successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Refresh token not correct'}, status=status.HTTP_400_BAD_REQUEST)
        
class RefreshTokenApi(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None, *args, **kwargs):
        
        refresh_token = request.data.get('refresh_token')
        user_id = request.data.get('user_id')
        
        custom_refresh_token = StoreRefreshToken.objects.get(user_id=user_id)
        print(custom_refresh_token)
        
        if custom_refresh_token.token == refresh_token:
            
            user = custom_refresh_token.user
            new_tokens = get_tokens_for_user(user)
            custom_refresh_token.token = new_tokens['refresh']
            custom_refresh_token.save()
            
            return Response(new_tokens, status=status.HTTP_200_OK)
        
        else:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        
class PasswordChangeAPIView(APIView):
    permission_classes = [CustomIsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_new_password')

        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        form = PasswordChangeForm(user, {'old_password': current_password, 'new_password1': new_password, 'new_password2': confirm_password})
        
        if form.is_valid():
            form.save()
            return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email address does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Generate password reset token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        print(f"Request Token : {token}")

        # Construct password reset URL
        reset_url = f"{settings.FRONTEND_URL}/api/password_reset/{uid}/{token}/"

        # Send password reset email
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({'detail': 'Password reset link sent to your email.'}, status=status.HTTP_200_OK)

class PasswordResetAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise NotFound('Invalid reset link')
        
        print("UID:", uid)
        print("Token:", token)
        
        print(request.data['password'])
        
        if default_token_generator.check_token(user, token):
            user_instance = get_object_or_404(User, pk=user.id)
            print("Token is valid.")
            form = SetPasswordForm(user_instance, {'new_password1': request.data['password'], 'new_password2': request.data['confirm_password']})
            if form.is_valid():
                form.save()
                return Response({'detail': 'Password reset successful.'}, status=status.HTTP_200_OK)
        
        raise NotFound('Invalid reset link')
    
    
# For Employee    
class EmployeeProfileAPIView(APIView):
    permission_classes = [EmployeeIsAuthenticated]

    def get_object(self):
        
        user = self.request.user
        employee = Employee.objects.filter(employee_code=user.username).first()
        return employee
    
    def get(self, request):
        employee = self.get_object()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

# For Employee
class CustomerAPIView(APIView):
    permission_classes = [EmployeeIsAuthenticated]

    def generate_customer_code(self):
        # Generating Customer Code
        customer_codes_only = Customer.objects.values_list('customer_code', flat=True)
        
        max_customer_code = ''
        
        if customer_codes_only.exists():
            max_customer_code = max(customer_codes_only)
        
        customer_code_loop = True
        customer_code_number = 1
        
        while customer_code_loop:

            customer_code_leading_zeros = 5 - len(str(customer_code_number))
            
            customer_code = "0" * customer_code_leading_zeros + str(customer_code_number)
            
            generated_customer_code = "CUS_" + customer_code
        
            if generated_customer_code in customer_codes_only or generated_customer_code < max_customer_code:
                customer_code_number += 1
            else:
                break
        return generated_customer_code
    
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            # Generate customer code
            generated_customer_code = self.generate_customer_code()
            serializer.save(customer_code=generated_customer_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_all_customers(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def get_customer_by_id(self, request, id):
        customer = get_object_or_404(Customer, pk=id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def get(self, request, id=None):
        if id:
            return self.get_customer_by_id(request, id)
        else:
            return self.get_all_customers(request)

    def put(self, request, id):
        customer = get_object_or_404(Customer, pk=id)
        store_customer_code = customer.customer_code
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.customer_code = store_customer_code
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        customer = get_object_or_404(Customer, pk=id)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# For Employee
class TestAPIView(APIView):
    permission_classes = [EmployeeIsAuthenticated]

    def post(self, request):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_all_tests(self, request):
        tests = Test.objects.all()
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)

    def get_test_by_id(self, request, id):
        test = get_object_or_404(Test, pk=id)
        serializer = TestSerializer(test)
        return Response(serializer.data)

    def get(self, request, id=None):
        if id:
            return self.get_test_by_id(request, id)
        else:
            return self.get_all_tests(request)

    def put(self, request, id):
        test = get_object_or_404(Customer, pk=id)
        serializer = TestSerializer(test, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        test = get_object_or_404(Customer, pk=id)
        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# For Employee
class ServiceWorkAPIView(APIView):
    permission_classes = [EmployeeIsAuthenticated]

    def generate_servicework_code(self):
        # Generating Service Work Code
        servicework_codes_only = ServiceWork.objects.values_list('service_work_code', flat=True)
        
        max_servicework_code = ''
        
        if servicework_codes_only.exists():
            max_servicework_code = max(servicework_codes_only)
        
        servicework_code_loop = True
        servicework_code_number = 1
        
        while servicework_code_loop:

            servicework_code_leading_zeros = 5 - len(str(servicework_code_number))
            
            servicework_code = "0" * servicework_code_leading_zeros + str(servicework_code_number)
            
            generated_servicework_code = "SR_" + servicework_code
        
            if generated_servicework_code in servicework_codes_only or generated_servicework_code < max_servicework_code:
                servicework_code_number += 1
            else:
                break
        return generated_servicework_code
    
    def post(self, request):
        serializer = ServiceWorkSerializer(data=request.data)
        if serializer.is_valid():
            # Generate servicework code
            generated_servicework_code = self.generate_servicework_code()
            serializer.save(service_work_code=generated_servicework_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_all_serviceworks(self, request):
        user = self.request.user
        employee = Servicer.objects.get(name__employee_code=user.username)  
        works_assigned_for_employee = ServiceAssign.objects.filter(servicer=employee)
        serviceworks = []
        
        for work_assigned in works_assigned_for_employee:   
            servicework = get_object_or_404(ServiceWork, service_work_code=work_assigned)
            serviceworks.append(servicework)
        
        serializer = ServiceWorkSerializer(serviceworks, many=True)
        return Response(serializer.data)

    def get_servicework_by_id(self, request, id):
        servicework = get_object_or_404(ServiceWork, pk=id)
        serializer = ServiceWorkSerializer(servicework)
        return Response(serializer.data)

    def get(self, request, id=None):
        if id:
            return self.get_servicework_by_id(request, id)
        else:
            return self.get_all_serviceworks(request)

    def put(self, request, id):
        servicework = get_object_or_404(ServiceWork, pk=id)
        store_servicework_code = servicework.service_work_code
        serializer = ServiceWorkSerializer(servicework, data=request.data)
        if serializer.is_valid():
            serializer.service_work_code = store_servicework_code
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        servicework = get_object_or_404(ServiceWork, pk=id)
        servicework.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# For Employee
class ServiceWorkDueAPIView(APIView):
    permission_classes = [EmployeeIsAuthenticated]

    def get(self, request, id=None):
        today_date = timezone.now().date()
        user = self.request.user
        employee = Servicer.objects.get(name__employee_code=user.username)  
        works_assigned_for_employee = ServiceAssign.objects.filter(servicer=employee)
        serviceworks = []
        
        for work_assigned in works_assigned_for_employee:   
            servicework = get_object_or_404(ServiceWork, service_work_code=work_assigned)
            if servicework.service_date == today_date:
                serviceworks.append(servicework)
        
        serializer = ServiceWorkSerializer(serviceworks, many=True)
        return Response(serializer.data)
    
# For Employee
class employeeNotificationAPIView(APIView):
    permission_classes = [EmployeeIsAuthenticated]
    
    def get(self, request):
        user = self.request.user
        employee = get_object_or_404(Employee, employee_code=user.username)
        notifications = EmployeeNotification.objects.filter(user=employee)
        serializer = EmployeeNotificationSerializer(notifications, many=True)
        return Response(serializer.data)


# For Customer
class customerNotificationAPIView(APIView):
    permission_classes = [CustomerIsAuthenticated]
    
    def get(self, request):
        user = self.request.user
        customer = get_object_or_404(Customer, customer_code=user.username)
        notifications = CustomerNotification.objects.filter(user=customer)
        serializer = CustomerNotificationSerializer(notifications, many=True)
        return Response(serializer.data)        

# For Customer  
class CustomerProfileAPIView(APIView):
    permission_classes = [CustomerIsAuthenticated]

    def get_object(self):
        user = self.request.user
        customer = Customer.objects.filter(customer_code=user.username).first()
        return customer
    
    def get(self, request):
        customer = self.get_object()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    
# For Customer
class CustomerServiceWorkAPIView(APIView):
    permission_classes = [CustomerIsAuthenticated]
    
    def get_all_serviceworks(self, request):
        user = self.request.user
        customer = get_object_or_404(Customer, customer_code=user.username)
        customer_Serviceworks = ServiceWork.objects.filter(customer_code=customer)
        
        serializer = ServiceWorkSerializer(customer_Serviceworks, many=True)
        return Response(serializer.data)

    def get_servicework_by_id(self, request, id):
        servicework = get_object_or_404(ServiceWork, pk=id)
        serializer = ServiceWorkSerializer(servicework)
        return Response(serializer.data)

    def get(self, request, id=None):
        if id:
            return self.get_servicework_by_id(request, id)
        else:
            return self.get_all_serviceworks(request)
    
# For Customer
class CustomerProductsAPIView(APIView):
    permission_classes = [CustomerIsAuthenticated]
    
    def get_all_customerproducts(self, request):
        user = self.request.user
        customer_products =  CustomerProduct.objects.filter(customer_code__customer_code=user)
        serializer = CustomerProductSerializer(customer_products, many=True)
        return Response(serializer.data)

    def get_customerproduct_by_id(self, request, id):
        customer_product = get_object_or_404(CustomerProduct, pk=id)
        serializer = CustomerProductSerializer(customer_product)
        return Response(serializer.data)

    def get(self, request, id=None):
        if id:
            return self.get_customerproduct_by_id(request, id)
        else:
            return self.get_all_customerproducts(request)