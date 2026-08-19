from django.db import models
from django.contrib.auth.models import User
from location_app.models import DivisionModel, DistrictModel

# Create your models here.
class RentTypeModel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class RentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rent')
    rent_type = models.ForeignKey(RentTypeModel, on_delete=models.CASCADE, related_name='rent_type')
    division = models.ForeignKey(DivisionModel, on_delete=models.CASCADE, related_name='rent_division')
    district=models.ForeignKey(DistrictModel, on_delete=models.CASCADE, related_name='rent_district')

    # Rent's Info
    rent_name = models.CharField(max_length=100, blank=False, null=False)
    owner_name = models.CharField(max_length=100, blank=True, null=True)
    owner_phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(max_length=2000, blank=True, null=True)
    area_size = models.DecimalField(max_digits=8, decimal_places=2, help_text='Total area in square feet')

    # Extra Features
    has_road = models.BooleanField(default=False)
    has_electricity = models.BooleanField(default=False)
    has_documents_all_ok = models.BooleanField(default=False)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available_from = models.DateField(null=True, blank=True)

    # Image of the Rent
    image1 = models.ImageField(upload_to='rent_app/img', null=True, blank=True)
    image2 = models.ImageField(upload_to='rent_app/img', null=True, blank=True)
    image3 = models.ImageField(upload_to='rent_app/img', null=True, blank=True)
    image4 = models.ImageField(upload_to='rent_app/img', null=True, blank=True)
    image5 = models.ImageField(upload_to='rent_app/img', null=True, blank=True)

    # Video of the Land
    video = models.FileField(upload_to='rent_app/video', null=True, blank=True)

    # Optional description & timestamp
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.rent_name 