from django.db import models
from user_management.models import CustomUser

# Create your models here.
class StoreRefreshToken(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=1024)
    
    def __str__(self):
        return f'Refresh token for {self.user}'
