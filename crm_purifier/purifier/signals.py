from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employee, ServiceWork, Notification, Customer, CustomerProduct
import string
import random

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# def generate_random_password(length=8):
#     special_character = '@'
#     characters = string.ascii_letters + special_character + string.digits
    
#     # Initialize the password with one lowercase and one uppercase letter
#     password = random.choice(string.ascii_lowercase) + random.choice(string.ascii_uppercase)
#     # Use length - 2 to accommodate for the two letters already added
#     password += ''.join(random.choice(characters) for _ in range(length - 2))
#     # Add one digit
#     password += random.choice(string.digits)
#     # Add one or two special characters
#     password += ''.join(random.choice(special_character) for _ in range(random.randint(1, 2)))
#     # Convert password to a list for shuffling
#     password = list(password)
#     # Shuffle the password
#     random.shuffle(password)
#     # Convert the shuffled list back to a string
#     password = ''.join(password)
    
#     return password

# generate_random_password()

# @receiver(post_save, sender=Employee)
# def create_user(sender, instance, created, **kwargs):
#     if created:
#         username = instance.employee_code
#         email = instance.email
#         random_password = generate_random_password()  # Generate a random password
#         instance.initial_password = random_password
#         instance.save()
#         User.objects.create_user(username=username, password=random_password, email=email)
#         print(f'username: {username} ----- password: {random_password} ----- password: {email} -----')


# @receiver(post_save, sender=User)
# def handle_user_password_update(sender, instance, created, **kwargs):

#     try:
#         employee = Employee.objects.get(email=instance.email)
#     except Employee.DoesNotExist:
#         employee = None
    
#     if employee:
#         if not created and instance.has_usable_password():

#             # Check if the password has been updated
#             if instance.password:
#                 print(employee)
#                 print(employee.initial_password)

#                 employee.initial_password = None
#                 employee.save()
                
                
def send_notification_to_frontend(notification_data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications_group',
        {
            'type': 'send_notification',
            'notification': notification_data
        }
    )
    

@receiver(post_save, sender=ServiceWork)
def service_work_notification(sender, instance, created, **kwargs):

    if instance.status == 'completed':
        
        Notification.objects.create(
            message=f"{instance.service_work_code} completed.",
            message_of="WORK"
        )
        
        send_notification_to_frontend(f"{instance.service_work_code} completed.")


@receiver(post_save, sender=Customer)
def customer_notification(sender, instance, created, **kwargs):
    
    if created:
        
        Notification.objects.create(
            message=f"{instance.customer_code} has been added.",
            message_of="CUSTOMER"
        )
        
        send_notification_to_frontend(f"{instance.customer_code} has been added.")
        

@receiver(post_save, sender=Customer)
def customer_product(sender, instance, created, **kwargs):
    
    if created:
        # Access the installed products associated with the customer instance
        installed_products = instance.installed_product.all()
        for product in installed_products:
            
            CustomerProduct.objects.create(
                customer_code=instance,
                product=product,
            )
            
    if not created:
        
        new_installed_products = instance.installed_product.all()
        
        existing_products = CustomerProduct.objects.filter(customer_code=instance)

        existing_products_list = [existing_product.product for existing_product in existing_products]
        
        for product in new_installed_products:
            
            if product not in existing_products_list:
                
                CustomerProduct.objects.create(
                customer_code=instance,
                product=product,
            )
                
        for existing_product in existing_products:
            
            if existing_product.product not in new_installed_products:
                
                existing_product.delete()