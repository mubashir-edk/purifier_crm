from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from .models import ServiceWork, Notification
        
def today_works():
    
    today = timezone.now().date()
    service_works_today = ServiceWork.objects.filter(service_date=today)

    for service_work in service_works_today:
        Notification.objects.create(
            message=f"Today service work: {service_work.service_work_code}",
            message_of="TODAY_WORK"
        )

    print(f"Notifications created successfully.")
    

def delete_read_notifications():
    
    five_days_ago = timezone.now() - timedelta(days=5)
    notifications_to_delete = Notification.objects.filter(is_read=True, timestamp__lte=five_days_ago)
    
    for notification in notifications_to_delete:
        notification.delete()