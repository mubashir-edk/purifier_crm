from rest_framework import serializers
from purifier.models import Employee, Customer, Test, ServiceWork, CustomerProduct

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['initial_password',]

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['initial_password',]

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class ServiceWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceWork
        fields = '__all__'

class CustomerProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProduct
        fields = '__all__'

