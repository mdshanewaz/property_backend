from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from user_app.models import ProfileModel
from rent_app.models import RentModel
from rent_app.serializers import RentSerializer

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def rent_list_view(request):
    rents = RentModel.objects.all()

    # Pass the data to the serializer (many= True for multiple objects)
    rents_serializer = RentSerializer(rents, many=True)

    return Response({'message':'All rents list', 'data': rents_serializer.data}, status=status.HTTP_200_OK)

