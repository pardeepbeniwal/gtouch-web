from rest_framework import status
import requests
import datetime
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from account.models import User, UserSession
from account.serializers import (MobileRegisterSerializer, RegisterSerializer, 
                                MyTokenObtainPairSerializer,
                                ChangePasswordSerializer, ForgotPasswordSerializer, 
                                UserSerializer )
from rest_framework import generics
from rest_framework.views import APIView
from utils.email_functions import send_email
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from account.utils import generateOTP
import uuid
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import validate_email
from django.utils import timezone

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

#https://api.taggteleservices.com/api/v2/SendSMS?SenderId=GINRXP&Is_Unicode=false&Is_Flash=false&Message=%22Dear%20Customer%2C%20Your%20OTP%20for%20registration%20is%20%7B%23var%23%7D.%20Use%20this%20OTP%20to%20complete%20your%20registration.%20Thank%20You.%5CnRegards%2C%5CnGTOUCH%22&MobileNumbers=918920216687&ApiKey=tEdQKm5TUIUgsjERx2hj8OYqC%2FfjjzeQLbkKCNCGA3w%3D&ClientId=7aceda54-a70b-497c-8284-e78242de9b7d
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"message": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            body = "Hi {first_name}, <br> Your password has been updated successfully.".format(first_name=self.object.first_name)
            send_email('Gtouch Password update',body,self.object.email)
            response = {
                'status': status.HTTP_200_OK,
                'message': 'Password updated successfully'
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ForgotPasswordView(generics.UpdateAPIView):
#     """
#     An endpoint for forgot password.
#     """
#     serializer_class = ForgotPasswordSerializer
#     model = User
#     permission_classes = (AllowAny,)    

#     def update(self, request, *args, **kwargs):        
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             email = serializer.data.get("email")
#             user = User.objects.filter(email=email).first()
#             if not user:
#                 return Response({"message": "User does not exists with this email."}, status=status.HTTP_400_BAD_REQUEST)
#             # token = str(uuid.uuid4())
#             # user.token = 1
#             # user.save()
#             # body = "Hi {first_name}, \n \n <a href=\"{site_url}auth/reset-password/{token}\">Click here</a> to reset password.".format(site_url=settings.SITE_URL,first_name=user.first_name, token=token)
#             # send_email('Gtouch Reset Password',body,email)
#             response = {
#                 'status': status.HTTP_200_OK,
#                 'message': "Please use this url for reset password: {}accounts/password_reset/".format(settings.SITE_URL)               
#             }

#             return Response(response)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        if data.get("email"):
            user = User.objects.filter(email=data.get('email')).first()
            if user:
                subject = "Gtouch Password Reset Requested"
                uid =  urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                body = "You're receiving this email because you requested a password reset for your user account at {site_url}.<br/><br/></br/>\
                        Please go to the following page and choose a new password:<br/><br/>\
                        {site_url}accounts/reset/{uid}/{token}/".format(site_url=settings.SITE_URL,uid=uid,token=token)
                send_email(subject,body,user.email)
                message = "We’ve emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly.\
                            If you don’t receive an email, please make sure you’ve entered the address you registered with, and check your spam folder."
                return Response({'message': message}, status=status.HTTP_200_OK)
            else:
                return Response({'email': 'User email does not exists.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'email': 'User email field is required.'}, status=status.HTTP_400_BAD_REQUEST)


class ExampleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):        
        content = {
            'status': 'request was permitted'
        }
        return Response(content)


class MobileRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = MobileRegisterSerializer

    def post(self, request):
        data  = request.data
        if not data.get('mobile_number'):
            return Response({"message": "Mobile number is required"}, status=status.HTTP_400_BAD_REQUEST)
        if len(str(data.get('mobile_number'))) < 10:
            return Response({"message": "Mobile number should be 10 digits."}, status=status.HTTP_400_BAD_REQUEST)
        elif len(str(data.get('mobile_number'))) > 10:
            return Response({"message": "Mobile number should be 10 digits."}, status=status.HTTP_400_BAD_REQUEST)
        if not data.get('device'):
            return Response({"message": "Device type is required"}, status=status.HTTP_400_BAD_REQUEST)

        otp = generateOTP()
        try:
            user = User.objects.get(mobile_number = data.get('mobile_number'))
            timediff = timezone.now()-user.opt_created_at
            if timediff.total_seconds() < 50:
                rem = int(50-timediff.total_seconds())
                return Response({"message": "Please wait for {} seconds to get OTP".format(rem)}, status=status.HTTP_400_BAD_REQUEST)
            user.passcode = otp
            user.opt_created_at = timezone.now()
            user.save()
        except Exception as e:
            mob_no = data.get('mobile_number')
            User.objects.create(passcode=otp,device=data.get('device'),mobile_number=mob_no,username=mob_no,opt_created_at = timezone.now())
        mobile_number = '91'+str(data.get('mobile_number'))
        url = settings.SMS_API_URL+"&Is_Unicode=false&Is_Flash=false&Message=%22Dear%20Customer%2C%20Your%20OTP%20for%20registration%20is%20{}.%20Use%20this%20OTP%20to%20complete%20your%20registration.%20Thank%20You.%5CnRegards%2C%5CnGTOUCH%22&MobileNumbers={}&ApiKey=tEdQKm5TUIUgsjERx2hj8OYqC%2FfjjzeQLbkKCNCGA3w%3D&ClientId={}".format(otp,mobile_number,settings.SMS_CLIENT_ID)
        requests.get(url)
        return Response({"message":"Your One Time Password has been sent on your mobile."}, status=status.HTTP_200_OK)

class MobileLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        if not data.get('mobile_number'):
            return Response({"message": "Mobile number is required"}, status=status.HTTP_400_BAD_REQUEST)
        if len(str(data.get('mobile_number'))) < 10:
            return Response({"message": "Mobile number should be 10 digits."}, status=status.HTTP_400_BAD_REQUEST)
        elif len(str(data.get('mobile_number'))) > 10:
            return Response({"message": "Mobile number should be 10 digits."}, status=status.HTTP_400_BAD_REQUEST)
        elif not data.get('otp'):
            return Response({"message": "OTP is required to login"}, status=status.HTTP_400_BAD_REQUEST)
        elif not data.get('device_name'):
            return Response({"message": "Device name is required to login"}, status=status.HTTP_400_BAD_REQUEST)
        elif not data.get('device_id'):
            return Response({"message": "Device Id is required to login"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(mobile_number = data.get('mobile_number'))
            # user.passcode=123
            # user.save()
            opt_time_expired = False
            timediff = timezone.now()-user.opt_created_at
            if timediff.total_seconds() > 60:
               opt_time_expired = True
            if str(user.passcode) != str(data.get('otp')) or opt_time_expired:
                return Response({"message": "Given otp is not valid or expired"}, status=status.HTTP_400_BAD_REQUEST)
            user.passcode = None
            user.save()
            refresh = RefreshToken.for_user(user)
            raw_token = str(refresh.access_token)
            refresh_token = str(refresh)
            UserSession.objects.create(access_token=raw_token,user_id=user,device_name=data.get('device_name'),device_id=data.get('device_id'),status=1)
            return Response({"user_id":user.id,"access": raw_token,"refresh":refresh_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Mobile number doest not exists","error":str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MobileLogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            access_token = request.META['HTTP_AUTHORIZATION'].replace('Bearer ','')
            session = UserSession.objects.filter(access_token=access_token).first()
            if session:
                session.status = 0
                session.save()
                return Response({"message":"Logout Successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"Your token has been expired"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        user = User.objects.get(id=request.user.id)
        data['id'] = user.id
        if data.get('email'):
            try:
               validate_email(data.get('email'))
            except:
              return Response({"message":"Email is not valid"},status=status.HTTP_400_BAD_REQUEST)
        if data.get('dob'):
            try:
                datetime.datetime.strptime(data.get('dob'), '%Y-%m-%d')
            except ValueError:
                return Response({"message":"Incorrect dob format, should be YYYY-MM-DD"},status=status.HTTP_400_BAD_REQUEST)
        if data.get('gender'):
            if data.get('gender') not in ["M", "F"]:
                return Response({"message":"Incorrect gender value, should be Male for M and Female for F"},status=status.HTTP_400_BAD_REQUEST)
        obj = UserSerializer(data=data)
        if obj.is_valid(raise_exception=True):
            obj.update(user,data)
        data["message"] = "Profile has been updated successfully."
        return Response(data, status=status.HTTP_200_OK)
    
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        data = UserSerializer(user).data
        return Response(data)