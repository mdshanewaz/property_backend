from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ServiceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service')
    service_name = models.CharField(max_length=300)
    service_price = models.IntegerField()
    service_description = models.TextField(max_length=1000)
    service_img = models.ImageField(upload_to='service_app/img', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.service_name

