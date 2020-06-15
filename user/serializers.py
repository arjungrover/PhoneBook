from django.contrib.auth import authenticate

from user.models import UserInfo

from rest_framework import serializers
from phoneBook import settings
import uuid

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['email', 'first_name', 'last_name', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.get('password')
        phone_number = validated_data.get('phone_number')
        instance = super(SignUpSerializer, self).create(validated_data)
        
        if password is not None:
            instance.set_password(password)
            # OTP verification can be included
            instance.save()
            return instance

class LoginSerializer(serializers.Serializer):
    phone_number= serializers.CharField(label="Phone Number")
    password = serializers.CharField(label="Password", style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password)

            if not user:
                msg = ['Unable to Login with Provided Credentials.']
                raise serializers.ValidationError(msg, code='authorization')
            else:
                if(not user.is_verified):
                    msg = ['Please verify your Phone number']
                    raise serializers.ValidationError(
                        msg, code='authorization')
                else:
                    attrs['user'] = user
                    return attrs
