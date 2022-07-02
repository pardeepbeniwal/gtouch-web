from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from account.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from utils.email_functions import send_email


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        data.update({'user_id': self.user.id})
        return data

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )        
        user.set_password(validated_data['password'])
        user.save()
        body = "Hi {first_name}, <br><br> You have registered successfully with Gtouch.".format(first_name=user.first_name)
        send_email('Gtouch User Registration',body,user.email)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ForgotPasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    email = serializers.EmailField(required=True)

def validate_required(value):
        # whatever validation logic you need
        if value == '' or value is None:
            raise serializers.ValidationError('This field is required.')
        
class MobileRegisterSerializer(serializers.ModelSerializer):
    mobile_number = serializers.IntegerField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('mobile_number', 'device', 'device_id' )
        extra_kwargs = {
            'mobile_number': {'required': True},
            'device': {'required': True}
        }
    
   

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )        
        user.set_password(validated_data['password'])
        user.save()
        body = "Hi {first_name}, <br><br> You have registered successfully with Gtouch.".format(first_name=user.first_name)
        send_email('Gtouch User Registration',body,user.email)
        return user

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = User
        exclude = ('password','groups','user_permissions','passcode','last_login','is_superuser')
        read_only_fields = ('username','mobile_number',)
    
    def update(self, instance, validated_data): 
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance
