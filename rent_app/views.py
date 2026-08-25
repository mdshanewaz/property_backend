from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from user_app.models import ProfileModel
from rent_app.models import RentModel
from rent_app.serializers import RentSerializer

# Create your views here.
# Rent Create 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rent_create_view(request):
    user = request.user
    serializer = RentSerializer(data=request.data)

    profile = ProfileModel.objects.get(owner=user)

    if not profile.is_verified:
        return Response({'message':'Your profile is not verified. Please contact support.'}, status=status.HTTP_400_BAD_REQUEST)

    if not profile.is_completed:
        return Response({'message' : 'Complete your profile first.'}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        division = serializer.validated_data.get('division')
        district = serializer.validated_data.get('district')

        if district.division != division:
            return Response({'error' : 'Selected district does not belong to the selected division.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user)
        return Response({'message' : 'Rent is created successfully.', 'data' : serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Rent View
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rent_view(request, pk):
    try:
        rent = RentModel.objects.get(id=pk)

    except RentModel.DoesNotExist:
        return Response({'detail' : 'Rent not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RentSerializer(rent)
    return Response({'message':'Rent Detail', 'data':serializer.data}, status=status.HTTP_200_OK)


# All Rent's List 
@api_view(['GET'])
@permission_classes([AllowAny])
def rent_list_view(request):
    rents = RentModel.objects.all()

    # Pass the data to the serializer (many= True for multiple objects)
    rents_serializer = RentSerializer(rents, many=True)

    return Response({'message':'All rents list', 'data': rents_serializer.data}, status=status.HTTP_200_OK)


# Land Update View
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def rent_update_view(request, pk):
    user = request.user

    try:
        rent = RentModel.objects.get(id=pk)

    except RentModel.DoesNotExist:
        return Response({'error' : 'Rent not found'}, status=status.HTTP_404_NOT_FOUND)

    if user != rent.user:
        return Response({'error':'You are not authorized to updated this Rent'}, status=status.HTTP_403_FORBIDDEN)

    serializer = RentSerializer(rent, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message':'Rent is updated successfully.', 'data':serializer.data}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Rent Delete View    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def rent_delete_view(request, pk):
    user = request.user

    try:
        rent = RentModel.objects.get(id=pk)
    except RentModel.DoesNotExist:
        return Response({'error':'Rent not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if user != rent.user:
        return Response({'error' : 'You are not authorized to delete the Rent'}, status=status.HTTP_403_FORBIDDEN)

    rent.delete()
    return Response({'message':'Rent is deleted'}, status=status.HTTP_200_OK)