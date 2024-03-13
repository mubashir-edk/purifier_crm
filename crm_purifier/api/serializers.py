from rest_framework import serializers
from purifier.models import Employee, Customer, Test, ServiceWork

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['initial_password',]

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class ServiceWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceWork
        fields = '__all__'

