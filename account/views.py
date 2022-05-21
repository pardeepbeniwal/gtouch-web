from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from account.models import User
from account.serializers import RegisterSerializer, MyTokenObtainPairSerializer, ChangePasswordSerializer, ForgotPasswordSerializer
from rest_framework import generics
from rest_framework.views import APIView
from utils.email_functions import send_email
from django.conf import settings
import uuid

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


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

class ForgotPasswordView(generics.UpdateAPIView):
    """
    An endpoint for forgot password.
    """
    serializer_class = ForgotPasswordSerializer
    model = User
    permission_classes = (AllowAny,)    

    def update(self, request, *args, **kwargs):        
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data.get("email")
            user = User.objects.filter(email=email).first()
            if not user:
                return Response({"message": "User does not exists with this email."}, status=status.HTTP_400_BAD_REQUEST)
            # token = str(uuid.uuid4())
            # user.token = 1
            # user.save()
            # body = "Hi {first_name}, \n \n <a href=\"{site_url}auth/reset-password/{token}\">Click here</a> to reset password.".format(site_url=settings.SITE_URL,first_name=user.first_name, token=token)
            # send_email('Gtouch Reset Password',body,email)
            response = {
                'status': status.HTTP_200_OK,
                'message': "Please use this url for reset password: {}accounts/password_reset/".format(settings.SITE_URL)               
            }

            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView():
    pass
class ExampleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):        
        content = {
            'status': 'request was permitted'
        }
        return Response(content)