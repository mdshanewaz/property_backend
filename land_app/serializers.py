from rest_framework import serializers
from land_app.models import LandModel

# Create your Serializers here.
class LandSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandModel
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['user']
