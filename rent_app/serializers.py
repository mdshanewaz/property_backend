from rest_framework import serializers
from rent_app.models import RentModel, RentTypeModel
from location_app.models import DivisionModel, DistrictModel

# Create your Serializers here.
class RentSerializer(serializers.ModelSerializer):
    division = serializers.PrimaryKeyRelatedField(
        queryset=DivisionModel.objects.all()
    )
    
    district = serializers.PrimaryKeyRelatedField(
        queryset=DistrictModel.objects.all()
    )

    rent_type = serializers.PrimaryKeyRelatedField(
        queryset=RentTypeModel.objects.all()
    )


    division_name = serializers.CharField(source="division.name", read_only=True)
    district_name = serializers.CharField(source="district.name", read_only=True)
    rent_type_name = serializers.CharField(source="rent_type.name", read_only=True)
    owner_id = serializers.IntegerField(source="user_id", read_only=True)

    class Meta:
        model = RentModel
        exclude = ['created_at', 'updated_at']