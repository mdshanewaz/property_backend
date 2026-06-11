from rest_framework import serializers
from apartment_app.models import ApartmentModel

# Create your Serializers here.
class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentModel
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['user']

