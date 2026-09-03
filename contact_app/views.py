from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from contact_app.models import ContactModel
from contact_app.serializers import ContacatSerializer

# Create your views here.
# Contact create
@api_view(['POST'])
@permission_classes([AllowAny])
def create_contact_view(request):
    serializer = ContacatSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Your message has been sent successfully.', 'data': serializer.data}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Contact view
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def contact_view(request, pk):
    try:
        contact = ContactModel.objects.get(id=pk)
    except ContactModel.DoesNotExist:
        return Response({'message' : 'Contact item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ContacatSerializer(contact)
    return Response({'message' : 'Contact details', 'data' : serializer.data}, status=status.HTTP_200_OK)


# All contact list
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def contact_list_view(request):
    contacts = ContactModel.objects.all()
    serializer = ContacatSerializer(contacts, many=True)
    return Response({'message':'All contacts list', 'data':serializer.data}, status=status.HTTP_200_OK)


# Contact Delete