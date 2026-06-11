from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from land_app.models import LandModel
from land_app.serializers import LandSerializer

# Create your views here.

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_land_view(request):
    serializer = LandSerializer(data=request.data)

    if serializer.is_valid():
        division = serializer.validated_data.get('division')
        district = serializer.validated_data.get('district')

        if district.division != division:
            return Response({"error": "Selected district does not belong to the selected division."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(user=request.user)
        return Response({'message' : 'Land is created successfully', 'data':serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
