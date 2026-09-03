from contact_app.models import ContactModel
from rest_framework import serializers

# Create your Serializers here.

class ContacatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactModel
        exclude = ['created_at']