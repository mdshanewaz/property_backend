from django.db import models
from location_app.models import *
from django.contrib.auth.models import User

# Create your models here.

# Model for Apartment
class ApartmentModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apartment')
    division = models.ForeignKey(DivisionModel, on_delete=models.CASCADE, related_name='apartment_division')
    district = models.ForeignKey(DistrictModel, on_delete=models.CASCADE, related_name='apartment_district')
    
    # Apartment's location Info
    building_name = models.CharField(max_length=100, blank=True, null=True)
    owner_name = models.CharField(max_length=100, blank=True, null=True)
    owner_phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(max_length=2000, blank=True, null=True)
    floor_number = models.IntegerField(help_text='Which floor the apartment is on')
    area_sqft = models.DecimalField(max_digits=8, decimal_places=2, help_text='Total area in square feet')
    
    # Rooms
    master_bedrooms = models.PositiveIntegerField(default=1)
    common_bedrooms = models.PositiveIntegerField(default=0)
    drawing_rooms = models.PositiveIntegerField(default=0)
    dining_rooms = models.PositiveIntegerField(default=1)
    kitchens = models.PositiveIntegerField(default=1)
    wash_rooms = models.PositiveIntegerField(default=1)
    balconies = models.PositiveIntegerField(default=0)
    store_rooms = models.PositiveIntegerField(default=0)
    servant_rooms = models.PositiveIntegerField(default=0)

    # Extra Features
    has_parking = models.BooleanField(default=False)
    has_lift_access = models.BooleanField(default=True)
    has_generator_backup = models.BooleanField(default=False)
    has_security_guard = models.BooleanField(default=True)
    is_furnished = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available_from = models.DateField(null=True, blank=True)

    # Image of the Apartment
    image1 = models.ImageField(upload_to='apartment_app/img', null=True, blank=True)
    image2 = models.ImageField(upload_to='apartment_app/img', null=True, blank=True)
    image3 = models.ImageField(upload_to='apartment_app/img', null=True, blank=True)
    image4 = models.ImageField(upload_to='apartment_app/img', null=True, blank=True)
    image5 = models.ImageField(upload_to='apartment_app/img', null=True, blank=True)
    image6 = models.ImageField(upload_to='apartment_app/img', null=True, blank=True)
    image7 = models.ImageField(upload_to='apartment_app/img', null=True, blank=True)
    image8 = models.ImageField(upload_to='apartment_app/img', null=True, blank=True)
    image9 = models.ImageField(upload_to='apartment_app/img', null=True, blank=True)
    image10 = models.ImageField(upload_to='apartment_app/img', null=True, blank=True)

    # Video of the Apartment
    video = models.FileField(upload_to='apartment_app/video', null=True, blank=True)

    # Optional description & timestamp
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.building_name

