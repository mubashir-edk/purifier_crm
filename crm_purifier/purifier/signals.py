from django.db.models.signals import post_save, m2m_changed, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from user_management.models import CustomUser
from .models import Employee, ServiceWork, Customer, CustomerProduct, ServiceAssign, AdminNotification, EmployeeNotification, CustomerNotification
import string
import random

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def generate_random_password(length=8):
    special_character = '@'
    characters = string.ascii_letters + special_character + string.digits
    
    # Initialize the password with one lowercase and one uppercase letter
    password = random.choice(string.ascii_lowercase) + random.choice(string.ascii_uppercase)
    # Use length - 2 to accommodate for the two letters already added
    password += ''.join(random.choice(characters) for _ in range(length - 2))
    # Add one digit
    password += random.choice(string.digits)
    # Add one or two special characters
    password += ''.join(random.choice(special_character) for _ in range(random.randint(1, 2)))
    # Convert password to a list for shuffling
    password = list(password)
    # Shuffle the password
    random.shuffle(password)
    # Convert the shuffled list back to a string
    password = ''.join(password)
    
    return password

generate_random_password()

@receiver(post_save, sender=Employee)
def create_user(sender, instance, created, **kwargs):
    print("EMPLOYEE POSTED")
    if created:
        print("EMPLOYEE CREATED")
        username = instance.employee_code
        email = instance.email
        
        random_password = generate_random_password()  # Generate a random password
        instance.initial_password = random_password
        instance.save()
        CustomUser.objects.create_employee(username=username, email=email, password=random_password)
        print(f'username: {username} ----- password: {random_password} ----- password: {email} -----')


@receiver(post_save, sender=Customer)
def create_user(sender, instance, created, **kwargs):
    print("CUSTOMER POSTED")
    if created:
        print("CUSTOMER CREATED")
        username = instance.customer_code
        email = instance.email
        
        random_password = generate_random_password()  # Generate a random password
        instance.initial_password = random_password
        print(instance.initial_password)
        instance.save()
        CustomUser.objects.create_customer(username=username, email=email, password=random_password)
        print(f'username: {username} ----- password: {random_password} ----- password: {email} -----')


@receiver(post_save, sender=CustomUser)
def handle_user_password_update(sender, instance, created, **kwargs):

    if instance.is_employee:
        employee = Employee.objects.get(email=instance.email)
    else:
        employee = None
    
    if instance.is_customer:
        customer = Customer.objects.get(email=instance.email)
    else:
        customer = None
        
    
    if employee:
        if not created and instance.has_usable_password():
            if instance.password:
                employee.initial_password = None
                employee.save()
    
    if customer:
        if not created and instance.has_usable_password():
            if instance.password:
                customer.initial_password = None
                customer.save()
        

@receiver(m2m_changed, sender=Customer.installed_product.through)
def customer_product(sender, instance, action, **kwargs):
    
    if action == 'post_add' or action == 'post_remove':
        
        installed_products = instance.installed_product.all()
        
        existing_products = CustomerProduct.objects.filter(customer_code=instance)

        existing_products_list = [existing_product.product for existing_product in existing_products]
        
        for product in installed_products:
            
            if product not in existing_products_list:
                
                CustomerProduct.objects.create(
                customer_code=instance,
                product=product,
            )
                
        for existing_product in existing_products:
            
            if existing_product.product not in installed_products:
                
                existing_product.delete()


@receiver(pre_delete, sender=Employee)
def delete_user_employee(sender, instance, **kwargs):
    CustomUser.objects.filter(email=instance.email).delete()


@receiver(pre_delete, sender=Customer)
def delete_user_customer(sender, instance, **kwargs):
    CustomUser.objects.filter(email=instance.email).delete()
    
    
    
@receiver(post_save, sender=ServiceWork)
def service_work_notification(sender, instance, created, **kwargs):

    if instance.status == 'completed':
        
        AdminNotification.objects.create(
            message=f"{instance.service_work_code} completed.",
            message_of="SERVICE_WORK_COMPLETED"
        )
        
        CustomerNotification.objects.create(
            user=instance.customer_code,
            message=f"Your service work {instance.service_work_code} has completed.",
            message_of="SERVICE_COMPLETED"
        )
        
    if created:
        
        CustomerNotification.objects.create(
            user=instance.customer_code,
            message=f"New service work {instance.service_work_code} has created for product {instance.product}.",
            message_of="SERVICE_NEW"
        )
        

@receiver(post_save, sender=ServiceAssign)
def serviceassign_notification(sender, instance, created, **kwargs):
    
    if instance.servicer:
        
        EmployeeNotification.objects.create(
            user=instance.servicer.name,
            message=f"Your new assigned work is {instance.service}.",
            message_of="SERVICE_ASSIGNED"
        )


@receiver(post_save, sender=Customer)
def customer_notification(sender, instance, created, **kwargs):
    
    if created:
        
        AdminNotification.objects.create(
            message=f"{instance.customer_code} has been added.",
            message_of="NEW_CUSTOMER"
        )