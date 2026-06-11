import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
# Profile Model
class ProfileModel(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=100, null=True, blank=True, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    father_name = models.CharField(max_length=50, null=True, blank=True)
    mother_name = models.CharField(max_length=50, null=True, blank=True)
    nid_num = models.CharField(max_length=20, null=True, blank=True)
    photo = models.ImageField(upload_to='user_app/img', null=True, blank=True)
    nid_photo = models.FileField(upload_to='user_app/nid', null=True, blank=True)
    permanent_address = models.TextField(null=True, blank=True)

    dob = models.DateField(null=True, blank=True)
    otp_validated = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def profile_percentage(self):

        fields = [
            self.owner,
            self.email,
            self.name,
            self.father_name,
            self.mother_name,
            self.nid_num,
            self.photo,
            self.nid_photo,
            self.permanent_address,
            self.dob,
            self.otp_validated,
            self.is_verified,
            self.created,
        ]

        filled = sum(1 for field in fields if field)

        return round((filled / len(fields)) * 100)
    
    @property
    def is_completed(self):
        return self.profile_percentage() >= 60

    def __str__(self):
        return self.owner.username


# OTP Model
class OtpModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='otp')
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    expires_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at =  timezone.now() + datetime.timedelta(minutes=5)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return self.otp_code