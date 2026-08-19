from rest_framework import serializers
from location_app.models import *

# Create your Serializers here.
# Division Serializer
class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DivisionModel
        fields = ['id', 'name']

# District Serializer
class DistrictSerializer(serializers.ModelSerializer):
    # division = serializers.CharField(source="division.name", read_only=True)
    class Meta:
        model = DistrictModel
        fields = ['id', 'name', 'division']