from rest_framework import serializers
from land_app.models import LandModel
from location_app.models import DivisionModel, DistrictModel

# Create your Serializers here.
class LandSerializer(serializers.ModelSerializer):
    division = serializers.PrimaryKeyRelatedField(
        queryset=DivisionModel.objects.all()
    )

    district = serializers.PrimaryKeyRelatedField(
        queryset=DistrictModel.objects.all()
    )

    division_name = serializers.CharField(source="division.name", read_only=True)
    district_name = serializers.CharField(source="district.name", read_only=True)
    owner_id = serializers.IntegerField(source="user_id", read_only=True)

    class Meta:
        model = LandModel
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['user']
