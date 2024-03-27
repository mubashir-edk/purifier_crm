from django.utils import timezone
from datetime import timedelta
from .models import ServiceWork, AdminNotification, CustomerNotification, EmployeeNotification, ServiceAssign
        
def today_works_notification():
    
    today = timezone.now().date()
    service_works_today = ServiceWork.objects \
        .exclude(status='completed') \
        .filter(service_date=today)

    for service_work in service_works_today:
        AdminNotification.objects.create(
            message=f"Today service work: {service_work.service_work_code}",
            message_of="TODAY_WORK"
        )
        
        CustomerNotification.objects.create(
            user=service_work.customer_code,
            message=f"Today service work: {service_work.service_work_code}",
            message_of="TODAY_SERVICES"
        )
        
        service_assigns = ServiceAssign.objects.all()
        
        for service_assign in service_assigns:
            if service_assign.servicer and service_assign.service == service_work:
                EmployeeNotification.objects.create(
                    user=service_assign.servicer.name,
                    message=f"Today service work: {service_work.service_work_code}",
                    message_of="TODAY_SERVICES"
                )

    print(f"Notifications created successfully.")


def tomorrow_works_notification():
    
    tomorrow = timezone.now().date() + timedelta(days=1)
    
    service_works_today = ServiceWork.objects \
        .exclude(status='completed') \
        .filter(service_date=tomorrow)

    for service_work in service_works_today:
        CustomerNotification.objects.create(
            user=service_work.customer_code,
            message=f"Tomorrow service work: {service_work.service_work_code}",
            message_of="TOMORROW_SERVICES"
        )

    print(f"Notifications created successfully.")