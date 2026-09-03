from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from service_app.models import ServiceModel
from service_app.serializers import ServiceSerializer
# Create your views here.

# Service list
@api_view(['GET'])
@permission_classes([AllowAny])
def service_list_view(request):
    services = ServiceModel.objects.all()
    serializer = ServiceSerializer(services, many=True)
    return Response({'message':'Service list', 'data':serializer.data}, status=status.HTTP_200_OK)

# Service detail
@api_view(['GET'])
@permission_classes([AllowAny])
def service_detail_view(request, pk):
    try:
        serivce = ServiceModel.objects.get(id=pk)
    except ServiceModel.DoesNotExist:
        return Response({'message':'Service not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ServiceSerializer(serivce)
    return Response({'message':'Service detail', 'data':serializer.data}, status=status.HTTP_200_OK)

