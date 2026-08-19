from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from location_app.models import DivisionModel, DistrictModel
from location_app.serializers import DivisionSerializer, DistrictSerializer

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def division_view(request):
    # All division from the database
    division_list = DivisionModel.objects.all()

    # Pass data to serializer
    division_serializer = DivisionSerializer(division_list, many=True)

    return Response({'message' : 'All Divisions', 'data' : division_serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def district_view(request, pk):
    # All division from the database
    division = get_object_or_404(DivisionModel, id=pk)
    district_list = DistrictModel.objects.filter(division=pk)

    # Pass data to serializer
    district_serializer = DistrictSerializer(district_list ,many=True)

    return Response({'message' : f'All Districts of {division.name}', 'data' : district_serializer.data}, status=status.HTTP_200_OK)


# v = DistrictModel.objects.values_list('name', flat=True)
# for d in v:
#     print(d)


