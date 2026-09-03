from rest_framework import serializers
from service_app.models import ServiceModel

# Create your Serializers here.
class ServiceSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source="user_id", read_only=True)

    class Meta:
        model = ServiceModel
        exclude = ['created_at']
        read_only_fields = ['user']