from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from user_app.models import ProfileModel, OtpModel
from django.contrib.auth.hashers import make_password


User = get_user_model()

# Create your serializers here.
# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user (
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        
        return user


# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="owner.username", read_only=True)
    class Meta:
        model = ProfileModel
        exclude = ['otp_validated', 'is_verified', 'created']
        read_only_fields = ['owner', 'email']
