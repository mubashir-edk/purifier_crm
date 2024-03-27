from django.db import models
import uuid

# Create your models here.
class Employee(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    profile = models.ImageField(null=True, blank=True, upload_to="employee_profiles/")
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20)
    address = models.TextField()
    employee_code = models.CharField(max_length=50, blank=True, unique=True)
    initial_password = models.CharField(max_length=150, blank=True, null=True)
    
    created_on = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.employee_code
    
class Category(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    image = models.ImageField(null=True, blank=True, upload_to="category_images/")
    name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.name
    
class Service(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=180)
    
    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    product_serial = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to="product_images/")
    services = models.ManyToManyField(Service, blank=True)
    
    created_on = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name

class Customer(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    profile = models.ImageField(null=True, blank=True, upload_to="customer_profiles/")
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    address = models.TextField()
    mobile = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20)
    installed_product = models.ManyToManyField(Product, blank=True)
    customer_code = models.CharField(max_length=50, blank=True, unique=True)
    location = models.CharField(max_length=250, null=True, blank=True)
    initial_password = models.CharField(max_length=150, blank=True, null=True)
    
    created_on = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.customer_code
    
class Servicer(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    name= models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name.employee_code

class Test(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    customer_code = models.ForeignKey(Customer, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=150)
    ph_value = models.CharField(max_length=30)
    tds_value = models.CharField(max_length=30)
    iron_value = models.CharField(max_length=30)
    hardness_value = models.CharField(max_length=30)
    turbuet_value = models.CharField(max_length=30)
    
    created_on = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.test_name

class ServiceWork(models.Model):
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('working', 'Working'),
        ('completed', 'Completed'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    service_work_code = models.CharField(max_length=50, blank=True, unique=True)
    customer_code = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    service_name = models.ManyToManyField(Service)
    comment_section = models.TextField(null=True, blank=True)
    service_date = models.DateField()
    remark_section = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    servicer = models.ForeignKey(Servicer, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_on = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.service_work_code
    
class ServiceAssign(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    service = models.ForeignKey(ServiceWork, on_delete=models.CASCADE, blank=True)
    servicer = models.ForeignKey(Servicer, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return str(self.service)
    
class CustomerProduct(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    customer_code = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_purchase_date = models.DateField(auto_now_add=True)
    product_service_history = models.TextField(null=True, blank=True)
    
    created_on = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer_code}, {self.product}"
    
class AdminNotification(models.Model):
    
    STATUS_CHOICES = (
        ('SERVICE_WORK_COMPLETED', 'SERVICE_WORK_COMPLETED'),
        ('NEW_CUSTOMER', 'NEW_CUSTOMER'),
        ('TODAY_WORK', 'TODAY_WORK'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    message = models.TextField()
    message_of = models.CharField(max_length=30, choices=STATUS_CHOICES, default='')
    once_passed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.message)

class EmployeeNotification(models.Model):
    
    STATUS_CHOICES = (
        ('SERVICE_ASSIGNED', 'SERVICE_ASSIGNED'),
        ('TODAY_WORKS', 'TODAY_WORKS'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    message = models.TextField()
    message_of = models.CharField(max_length=30, choices=STATUS_CHOICES, default='')
    once_passed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.message)

class CustomerNotification(models.Model):
    
    STATUS_CHOICES = (
        ('SERVICE_COMPLETED', 'SERVICE_COMPLETED'),
        ('SERVICE_NEW', 'SERVICE_NEW'),
        ('TOMORROW_SERVICES', 'TOMORROW_SERVICES'),
        ('TODAY_SERVICES', 'TODAY_SERVICES'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    message_of = models.CharField(max_length=30, choices=STATUS_CHOICES, default='')
    once_passed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.message)