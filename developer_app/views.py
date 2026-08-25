from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from developer_app.models import DeveloperModel
from developer_app.serializers import DeveloperSerializer
from user_app.models import ProfileModel

# Create your views here.
# Developer list view
@api_view(['GET'])
@permission_classes([AllowAny])
def developer_list_view(request):
    developers = DeveloperModel.objects.all()

    # Pass the data to serializer from frontend and backend communication (many= True for multiple objects)
    serializer = DeveloperSerializer(developers, many=True)
    return Response({'message':'All Developers List', 'data':serializer.data}, status=status.HTTP_200_OK)


# Single Developer View
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def developer_view(request, pk):
    try:
        developer = DeveloperModel.objects.get(id=pk)
    except DeveloperModel.DoesNotExist():
        return Response({'detail' : 'Developer not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = DeveloperSerializer(developer)
    return Response({'message':'Developer Detail', 'data':serializer.data}, status=status.HTTP_200_OK)


# Developer Create View
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def developer_create_view(request):
    user = request.user
    serializer = DeveloperSerializer(data=request.data)
    profile = ProfileModel.objects.get(owner=user)

    if not profile.is_verified:
        return Response({'message':'Your profile is not verified. Please contact support.'}, status=status.HTTP_400_BAD_REQUEST)

    if not profile.is_completed:
        return Response({'message':'Complete you profile first.'}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'message':'Developer is created', 'data':serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def developer_update_view(request):
    pass

# Developer delete view
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def developer_delete_view(request, pk):
    user = request.user

    try:
        developer = DeveloperModel.objects.get(id=pk)
    except DeveloperModel.DoesNotExist():
        return Response({'error':'Developer not found'}, status=status.HTTP_404_NOT_FOUND)

    if user != developer.user:
        return Response (status=status.HTTP_403_FORBIDDEN)

    developer.delete()
    return Response({'message':'Developer is deleted'}, status=status.HTTP_200_OK)
