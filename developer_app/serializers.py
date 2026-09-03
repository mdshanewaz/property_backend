import json
from rest_framework import serializers
from developer_app.models import DeveloperModel
from location_app.models import DistrictModel

# Create your Serializers here.
class DeveloperSerializer(serializers.ModelSerializer):
    area = serializers.PrimaryKeyRelatedField(queryset=DistrictModel.objects.all(), many=True)
    area_name = serializers.SerializerMethodField(method_name="get_area_name")
    owner_id = serializers.IntegerField(source="user_id", read_only=True)

    class Meta:
        model = DeveloperModel
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['user']

    def get_area_name(self, obj):
        return [{'district_name':distrcit.name, 'district_id':distrcit.id} for distrcit in obj.area.all()]

    def to_internal_value(self, data):
            data = data.copy()
            area = data.get("area")

            if isinstance(area, str):    
                data["area"] = json.loads(area)
    
            return super().to_internal_value(data)