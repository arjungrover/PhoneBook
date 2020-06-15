from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import UserInfo, Token
from contacts.models import SpamInfo
from user.serializers import SignUpSerializer, LoginSerializer

class SignupViewSet(viewsets.ModelViewSet):
    serializer_class = SignUpSerializer
    queryset = UserInfo.objects.all()

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        phone_number = serializer.validated_data['phone_number']
        if(len(SpamInfo.objects.filter(spam_number=phone_number)) == 0 ):
            SpamInfo.objects.create(spam_number=phone_number, is_spam=False)

        token = Token.objects.get_or_create(user=user)[0]
        return Response(
            {
                'token': token.key,
            }
        )
