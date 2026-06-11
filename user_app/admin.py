from django.contrib import admin
from user_app.models import ProfileModel, OtpModel

# Register your models here.
admin.site.register(ProfileModel)
admin.site.register(OtpModel)