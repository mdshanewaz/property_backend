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
    class Meta:
        models = DistrictModel
        fields = ['id', 'name', 'division']