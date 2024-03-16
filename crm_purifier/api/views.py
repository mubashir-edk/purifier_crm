from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from user_management.permissions import CustomIsAuthenticated

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
from purifier.models import Employee, Customer, Test, ServiceWork
from user_management.models import CustomUser
from user_management.backends import CustomUserBackend
from .serializers import EmployeeSerializer, CustomerSerializer, TestSerializer, ServiceWorkSerializer


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username_or_email = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username_or_email, password=password)
        # user = CustomUserBackend().authenticate(request, username=username_or_email, password=password)
        
        if not user:
            try:
                user = authenticate(email=username_or_email, password=password)
                # user = CustomUserBackend().authenticate(request, email=username_or_email, password=password)
            except User.DoesNotExist:
                pass

        if user:
            # Authentication successful, generate tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class EmployeeProfileAPIView(APIView):
    permission_classes = [CustomIsAuthenticated]

    def get_object(self):
        
        user = self.request.user
        employee = Employee.objects.filter(employee_code=user.username).first()
        return employee
    
    def get(self, request):
        employee = self.get_object()
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
        
class PasswordChangeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        # new_password = request.data.get('new_password')

        # Check if the current password is correct
        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        # Use Django's built-in PasswordChangeForm to validate and change password
        form = PasswordChangeForm(user, {'old_password': request.data['current_password'], 'new_password1': request.data['new_password'], 'new_password2': request.data['confirm_new_password']})
        
        if form.is_valid():
            form.save()
            return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        else:
            # If the form is not valid, return the errors
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # User with this email address does not exist
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

        # Always respond with success to prevent email enumeration
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

class CustomerAPIView(APIView):
    permission_classes = [IsAuthenticated]

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

    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def put(self, request, id):
        customer = get_object_or_404(Customer, pk=id)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        customer = get_object_or_404(Customer, pk=id)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        tests = Test.objects.all()
        serializer = TestSerializer(tests, many=True)
        return Response(serializer.data)

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

class ServiceWorkAPIView(APIView):
    permission_classes = [IsAuthenticated]

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

    def get(self, request):
        serviceworks = ServiceWork.objects.all()
        serializer = ServiceWorkSerializer(serviceworks, many=True)
        return Response(serializer.data)

    def put(self, request, id):
        servicework = get_object_or_404(ServiceWork, pk=id)
        serializer = ServiceWorkSerializer(servicework, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        servicework = get_object_or_404(ServiceWork, pk=id)
        servicework.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
