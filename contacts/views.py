from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView

from contacts.serializers import AddContactSerializer, AddSpamSerializer
from user.serializers import SignUpSerializer
from contacts.models import ContactInfo, SpamInfo
from user.models import UserInfo

class ContactViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddContactSerializer
    queryset = ContactInfo.objects.all()

class SpamViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddSpamSerializer
    queryset = SpamInfo.objects.all()

class GetUsersByName(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        first_name = request.GET.get('first_name')
        queryset = UserInfo.objects.filter(first_name=first_name)
        serializer = SignUpSerializer(queryset, many=True)

        for e in serializer.data:
            obj = SpamInfo.objects.get(spam_number=e.get('phone_number'))
            e['is_spam'] = obj.is_spam
        
        return Response(serializer.data)

class GetUsersByNumber(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        res = []
        phone_number = request.GET.get('phone_number')
        queryset = UserInfo.objects.filter(phone_number=phone_number)
        serializer = SignUpSerializer(queryset, many=True)
        for dict_obj in serializer.data:
            res.append(dict_obj)

        if(len(ContactInfo.objects.filter(phone_number=phone_number))!=0):
           queryset1 = ContactInfo.objects.filter(phone_number=phone_number)
           for contact_obj in queryset1:
               res.append({"name": contact_obj.contact_name})
            
        return Response(res)
