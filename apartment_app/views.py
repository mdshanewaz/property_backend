from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from user_app.models import ProfileModel
from apartment_app.models import ApartmentModel
from apartment_app.serializers import ApartmentSerializer

# Create your views here.
# Apartment Post
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_apartment_view(request):
    user = request.user
    serializer = ApartmentSerializer(data=request.data)

    profile = ProfileModel.objects.get(owner=user)

    if not profile.is_completed:
        return Response({'detail' : 'Complete your profile first.'}, status=status.HTTP_400_BAD_REQUEST)

    if not profile.is_verified:
        return Response({'detail' : 'Your profile is not verified. Please contact support.'}, status=status.HTTP_400_BAD_REQUEST)
    


    if serializer.is_valid():
        division = serializer.validated_data.get('division')
        district = serializer.validated_data.get('district')
        
        # Check if the district belongs to the selected division
        if district.division != division:
            return Response({"error": "Selected district does not belong to the selected division."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(user=request.user)
        return Response({'message' : 'Apartment is created successfully', 'data':serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Apartment view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def apartment_view(request, pk):
    
    try:
        apartment = ApartmentModel.objects.get(id=pk)
        
    except ApartmentModel.DoesNotExist:
        return Response({'detail':'Apartment not found.'}, status=status.HTTP_404_NOT_FOUND)
    

    serializer = ApartmentSerializer(apartment)
    return Response({'message' : 'Apartment details', 'data' : serializer.data}, status=status.HTTP_200_OK)


# All Apartments
@api_view(['GET'])
def get_apartment_view(request):
    # All Appertment from the database
    items = ApartmentModel.objects.all()

    # Pass the data to the serializer (many= True for multiple objects)
    apartment_serializer = ApartmentSerializer(items, many=True)

    return Response({'message' : 'All apartments', 'data' : apartment_serializer.data}, status=status.HTTP_200_OK)

# Apartment Edit View
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_apartment(request, pk):
    user = request.user

    try:
        apartment = ApartmentModel.objects.get(id=pk)
    
    except ApartmentModel.DoesNotExist:
        return Response({'detail':'Apartment not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    # Ownership check
    if user != apartment.user:
        return Response({'detail': 'You are not authorized to edit this post'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = ApartmentSerializer(apartment, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({'message' : 'Apartment updated successfully.', 'data' : serializer.data}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
