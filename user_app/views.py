import jwt
from django.conf import settings
from django.shortcuts import render
from django.db import transaction
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user_app.models import ProfileModel, OtpModel
from user_app.serializers import RegisterSerializer, ProfileSerializer
from user_app.utils import otp_generator, send_otp_mail

# Create your views here.

# Cutom Token Cookies
# Login View
class Custom_TokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        try:

            response = super().post(request, *args, **kwargs)
            tokens = response.data

            access_token = tokens['access']
            refresh_token = tokens['refresh']

            username = request.data.get('username')
            user = User.objects.get(Q(username=username) | Q(email=username))

            if not user.profile.otp_validated:
                return Response({'login': False, 'error': 'Account is not validated. Please contact support.'}, status=status.HTTP_403_FORBIDDEN)

            res = Response()
            
            res.data = {
                'login':True,
                'message': 'Login successful',
                'status': status.HTTP_200_OK,
                }

            res.delete_cookie('temporary_access_token', path='/', samesite='None')

            res.set_cookie(
                key = 'access_token',
                value = access_token,
                httponly = True,
                secure = True,
                samesite='None',
                path='/'
            )

            res.set_cookie(
                key = 'refresh_token',
                value = refresh_token,
                httponly = True,
                secure = True,
                samesite='None',
                path='/'
            )

            return res

        except ProfileModel.DoesNotExist:
            return Response({'login': False, 'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        except:
            return Response({'login':False, 'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Custom Refresh token
class Custom_TokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            request.data['refresh'] = refresh_token

            response = super().post(request, *args, **kwargs)

            tokens = response.data
            access_token = tokens['access']

            res = Response()
            res.data = {'refreshed' : True}
            
            res.set_cookie(
                key = 'access_token',
                value = access_token,
                httponly = True,
                secure = True,
                samesite='None',
                path='/'
            ) 
            
            return res
        except:
            return Response()


# Logout Function
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logoutView(request):
    try:
        res = Response()
        res.data = {'Logout' : True}
        res.delete_cookie('access_token', path='/', samesite='None')
        res.delete_cookie('refresh_token', path='/', samesite='None')
        res.delete_cookie('temporary_access_token', path='/', samesite='None')

        return res
    except:
        return Response({'Logout' : False})


# Check Authenticated
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def is_authenticated_view(request):
    return Response({'Authenticated' : True})


# Register View
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user_view(request):
    serializer = RegisterSerializer(data=request.data)
    try:
        if serializer.is_valid():
            email = serializer.validated_data.get('email')

            if User.objects.filter(email=email).exists():
                return Response({"message": "This email is used already"}, status=status.HTTP_400_BAD_REQUEST) 
            
            with transaction.atomic():
        
                # Create new user
                user = serializer.save()

                # Create linked profile
                ProfileModel.objects.create(
                    owner=user,
                    email=email
                )

                otp = otp_generator()
        
                # Create linked Otp
                OtpModel.objects.create(
                    user = user,
                    otp_code = otp   
                )

                refresh = RefreshToken.for_user(user)
                temporary_token = str(refresh.access_token)

                res = Response(
                    # response body like response.data = {}
                    {
                        'message': "Account created successfully. OTP sent to your email.",
                        'register' : True,
                        'login':False,
                        'status': status.HTTP_200_OK,
                    },

                    # response status
                    status=status.HTTP_201_CREATED
                )
                

                res.set_cookie(
                    key = 'temporary_access_token',
                    value = temporary_token,
                    httponly = True,
                    secure = True,
                    samesite='None',
                    path='/'
                )
                
                send_otp_mail(user.username, email, otp)

                return res
            
                # return Response({"message": "Account created successfully. OTP sent to your email."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as err:
        return Response({'error':str(err)}, status=status.HTTP_400_BAD_REQUEST)


# OTP View
@api_view(['POST'])
@permission_classes([AllowAny])
def otp_validation_view(request):
    temp_token = request.COOKIES.get('temporary_access_token')

    if not temp_token:
        return Response(
            {"detail": "Otp is expried. Contact the support"},
            status=401
        ) 

    payload = jwt.decode(temp_token, settings.SECRET_KEY, algorithms=['HS256'])
    user_id = payload.get('user_id')
    username = User.objects.get(id=user_id)
    otp_entered = request.data.get('otp_code')

    

    if not otp_entered:
        return Response({'detail': 'OTP is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user =  User.objects.get(Q(username=username) | Q(email=username))
            
        otp_object = OtpModel.objects.get(user=user)
        
        if otp_object.otp_code == otp_entered:

            if otp_object.is_expired():
                res = Response(
                {
                    'detail': 'OTP is expired. Contact the Support',
                    'OTP Verified' : True
                }, 
                status=400
                )

                res.delete_cookie('temporary_access_token', path='/', samesite='None')

                return res

            user.profile.otp_validated = True
            user.profile.save()

            # Delete OTP after verification
            otp_object.delete()

            res = Response(
                {
                    'message': 'Email verified successfully.',
                    'OTP Verified' : True
                }, 
                status=status.HTTP_200_OK
            )

            # res.delete_cookie('temporary_access_token', path='/', samesite='None')

            return res
            
        return Response({'detail': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response(
            {'detail': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    except OtpModel.DoesNotExist:
        return Response(
            {'detail': 'OTP not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    except Exception as err:
        return Response({'detail':str(err)}, status=status.HTTP_400_BAD_REQUEST)



# Profile View
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_user_view(request):
    user = request.user
    profile = ProfileModel.objects.get(owner=user)
    serializer = ProfileSerializer(profile)

    return Response(serializer.data)


# Forgot or reset password view
@api_view(['POST'])
@permission_classes([AllowAny])
def email_otp_reset_pass_view(request):
    email = request.data.get('email')
    user = User.objects.filter(email=email).first()
    
    if not email:
        return Response({'detail' : 'Put the email please'}, status=status.HTTP_400_BAD_REQUEST)

    if not user:
        return Response({'detail' : 'The email is wrong'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    otp = otp_generator()

    # Create linked Otp
    OtpModel.objects.create(
        user = user,
        otp_code = otp   
    )

    send_otp_mail(user.username, email, otp)

    refresh = RefreshToken.for_user(user)
    temporary_token = str(refresh.access_token)

    res = Response(
    # response body like response.data = {}
        {
            "message": "OTP sent to your email. To reset password please enter the OTP",
            'login':False,
            'status': status.HTTP_201_CREATED,
        },

        # response status
        status=status.HTTP_201_CREATED
    )
                

    res.set_cookie(
        key = 'temporary_access_token',
        value = temporary_token,
        httponly = True,
        secure = True,
        samesite='None',
        path='/'
    )

    return res


# Reset password view
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_pass_view(request):
    temp_token = request.COOKIES.get('temporary_access_token')

    if not temp_token:
        return Response(
            {"detail": "Otp is expried. Contact the support"},
            status=401
        ) 

    payload = jwt.decode(temp_token, settings.SECRET_KEY, algorithms=['HS256'])
    user_id = payload.get('user_id')
    user = User.objects.get(id=user_id)
    new_pass = request.data.get('password')
    confirm_pass = request.data.get('confirm_password')

    if not new_pass or not confirm_pass:
        return Response({'detail' : 'Both password fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    if confirm_pass != new_pass:
        return Response({'detail' : 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
    
    if len(new_pass) < 8:
            return Response({'detail' : 'Password should be atleast 8 characters long'}, status=status.HTTP_400_BAD_REQUEST)
            
    user.set_password(new_pass)
    user.save()

    res = Response(
        {'message' : 'Your password reset is done.'}, 
        status=status.HTTP_200_OK
    )

    res.delete_cookie('temporary_access_token', path='/', samesite='None')
    return res


# Profile edit view
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def profile_edit_view(request):
    user = request.user

    try:
        profile = ProfileModel.objects.get(owner=user)
    
    except ProfileModel.DoesNotExist:
        return Response({'detail': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProfileSerializer(profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

        return Response({'message' : 'Profile is updated', 'data' : serializer.data}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    



