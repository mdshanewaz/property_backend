from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from land_app.models import LandModel
from user_app.models import ProfileModel
from land_app.serializers import LandSerializer

# Create your views here.
# Land Create
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def create_land_view(request):
    user= request.user
    serializer = LandSerializer(data=request.data)

    profile = ProfileModel.objects.get(owner=user)

    if not profile.is_completed:
        return Response({'message' : 'Complete your profile first.'}, status=status.HTTP_400_BAD_REQUEST)

    if not profile.is_verified:
        return Response({'message' : 'Your profile is not verified. Please contact support.'}, status=status.HTTP_400_BAD_REQUEST)


    if serializer.is_valid():
        division = serializer.validated_data.get('division')
        district = serializer.validated_data.get('district')

        if district.division != division:
            return Response({'error': 'Selected district does not belong to the selected division.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(user=request.user)
        return Response({'message' : 'Land is created successfully', 'data':serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Land View
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def land_view(request, pk):
    try:
        land = LandModel.objects.get(id=pk)

    except LandModel.DoesNotExist:
        return Response({'detail':'Land not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LandSerializer(land)
    return Response({'message': 'Land details', 'data':serializer.data}, status=status.HTTP_200_OK)


# All land's List
@api_view(['GET'])
@permission_classes([AllowAny])
def lands_list_view(request):
    lands = LandModel.objects.all()

    # Pass the data to the serializer (many= True for multiple objects)
    lands_serializer = LandSerializer(lands, many=True)

    return Response({'message' : 'All Lands list', 'data':lands_serializer.data}, status=status.HTTP_200_OK)


# Land Edit View
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def land_update_view(request, pk):
    user = request.user

    try:
        land =LandModel.objects.get(id=pk)

    except LandModel.DoesNotExist:
        return Response({'error' : 'Land not found'}, status=status.HTTP_404_NOT_FOUND)

    if user != land.user:
        return Response({'error': 'You are not authorized to update this Land'}, status=status.HTTP_403_FORBIDDEN)

    serializer = LandSerializer(land, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message':'Land is updated successfully.', 'data':serializer.data}, status=status.HTTP_200_OK)

    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


#Land Delete View
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def land_delete_view(request, pk):
    user = request.user

    try:
        land = LandModel.objects.get(id=pk)

    except LandModel.DoesNotExist:
        return Response({'error':'Land Not Found'}, status=status.HTTP_404_NOT_FOUND)

    if user != land.user:
        return Response({'error':'You are not authorized to delete the Land'}, status=status.HTTP_403_FORBIDDEN)

    land.delete()
    return Response({'message':'Land is deleted'}, status=status.HTTP_200_OK)