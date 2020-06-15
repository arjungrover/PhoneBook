from django.contrib import admin
from contacts.models import ContactInfo, UserContact, SpamInfo

admin.site.register(ContactInfo)
admin.site.register(UserContact)
admin.site.register(SpamInfo)
