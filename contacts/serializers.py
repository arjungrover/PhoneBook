from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from contacts.models import ContactInfo, UserContact, SpamInfo
from user.models import UserInfo

class AddContactSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = ContactInfo
        fields = ["contact_name","phone_number", "user_id"]

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        phone_number = validated_data.pop("phone_number")
        contact_object = ContactInfo.objects.get_or_create(contact_name=validated_data.pop("contact_name"), phone_number=phone_number)[0]
        UserContact.objects.get_or_create(user_id=user_id, contact=contact_object)
    
        if( len(SpamInfo.objects.filter(spam_number=phone_number)) == 0 ): 
            SpamInfo.objects.create(spam_number=phone_number, is_spam=False)
        
        return contact_object

class AddSpamSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamInfo
        fields = ["spam_number"]

    def create(self, validated_data):
        spam_object = SpamInfo.objects.get_or_create(spam_number=validated_data.pop('spam_number'))[0]
        spam_object.is_spam = True
        spam_object.save()
        
        return spam_object
