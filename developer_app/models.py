from django.db import models
from django.contrib.auth.models import User
from location_app.models import DistrictModel

# Create your models here.
class DeveloperModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='developer')
    area = models.ManyToManyField(DistrictModel, related_name='developers_area')

    # Developer's info
    developer_name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    owner_name = models.CharField(max_length=100, blank=True, null=True)
    phone_1 = models.CharField(max_length=15, null=True, blank=True)
    phone_2 = models.CharField(max_length=15, null=True, blank=True)
    phone_3 = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(max_length=2000, blank=True, null=True)
    license_number = models.CharField(max_length=15, null=True, blank=True)

    # Image documents
    thumbnail = models.ImageField(upload_to='developer_app/img', null=True, blank=True)
    license_img = models.ImageField(upload_to='developer_app/img', null=True, blank=True)
    video = models.FileField(upload_to='developer_app/video', null=True, blank=True)

    # Optional description & timestamp
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.developer_name