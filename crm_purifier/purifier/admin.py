from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Employee)
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Service)
admin.site.register(Servicer)
admin.site.register(Test)
admin.site.register(ServiceWork)
admin.site.register(ServiceAssign)
admin.site.register(Notification)
admin.site.register(CustomerProduct)