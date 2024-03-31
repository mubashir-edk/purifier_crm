from rest_framework import serializers
from user_management.models import CustomUser
from purifier.models import Employee, Customer, Test, ServiceWork, CustomerProduct, EmployeeNotification, CustomerNotification, Product, Category, Service

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email',)

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ['initial_password',]
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    services = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all(), many=True)
    
    class Meta:
        model = Product
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        category_instance = instance.category
        if category_instance:
            category_serializer = CategorySerializer(category_instance)
            representation['category_details'] = category_serializer.data
            
        service_instances = instance.installed_product.all()
        if service_instances:
            service_serializer = ServiceSerializer(service_instances, many=True)
            representation['service_details'] = service_serializer.data
            
        return representation

class CustomerSerializer(serializers.ModelSerializer):
    installed_product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    
    class Meta:
        model = Customer
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        products_instances = instance.installed_product.all()
        if products_instances:
            product_serializer = ProductSerializer(products_instances, many=True)
            representation['installed_product_details'] = product_serializer.data
        return representation

class TestSerializer(serializers.ModelSerializer):
    customer_code = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    
    class Meta:
        model = Test
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        customer_instance = instance.customer_code
        if customer_instance:
            customer_serializer = CustomerSerializer(customer_instance)
            representation['customer_details'] = customer_serializer.data
        return representation

class ServiceWorkSerializer(serializers.ModelSerializer):
    customer_code = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = ServiceWork
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Include serialized representation of customer
        customer_instance = instance.customer_code
        if customer_instance:
            customer_serializer = CustomerSerializer(customer_instance)
            representation['customer_details'] = customer_serializer.data
        
        # Include serialized representation of product
        product_instance = instance.product
        if product_instance:
            product_serializer = ProductSerializer(product_instance)
            representation['product_details'] = product_serializer.data
        
        return representation

class CustomerProductSerializer(serializers.ModelSerializer):
    customer_code = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    class Meta:
        model = CustomerProduct
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Include serialized representation of customer
        customer_instance = instance.customer_code
        if customer_instance:
            customer_serializer = CustomerSerializer(customer_instance)
            representation['customer_details'] = customer_serializer.data
        
        # Include serialized representation of product
        product_instance = instance.product
        if product_instance:
            product_serializer = ProductSerializer(product_instance)
            representation['product_details'] = product_serializer.data
        
        return representation
        
class EmployeeNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeNotification
        fields = '__all__'
        
class CustomerNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerNotification
        fields = '__all__'