from rest_framework import serializers
from user_management.models import CustomUser
from purifier.models import Employee, Customer, Test, ServiceWork, CustomerProduct, EmployeeNotification, CustomerNotification, Product

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email',)

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['initial_password',]
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    installed_product = ProductSerializer()
    class Meta:
        model = Customer
        exclude = ['initial_password',]

class TestSerializer(serializers.ModelSerializer):
    customer_code = CustomerSerializer()
    class Meta:
        model = Test
        fields = '__all__'

class ServiceWorkSerializer(serializers.ModelSerializer):
    customer_code = CustomerSerializer()
    product = ProductSerializer()
    class Meta:
        model = ServiceWork
        fields = '__all__'

class CustomerProductSerializer(serializers.ModelSerializer):
    customer_code = CustomerSerializer()
    product = ProductSerializer()
    class Meta:
        model = CustomerProduct
        fields = '__all__'
        
class EmployeeNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeNotification
        fields = '__all__'
        
class CustomerNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerNotification
        fields = '__all__'

