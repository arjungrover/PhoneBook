from django.db import models
from base.models import BaseModel
from user.models import UserInfo

class ContactInfo(BaseModel, models.Model):
    """
    This model will store details about contacts
    """
    contact_name = models.CharField(verbose_name="Contact Name", max_length=128, blank=False)
    phone_number = models.CharField(verbose_name="Phone Number", max_length=15)

    def __str__(self):
        return "{}:{}".format(self.contact_name, self.phone_number)

class UserContact(BaseModel, models.Model):
    """
    This model will store details about users contacts
    """
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    contact = models.ForeignKey(ContactInfo, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.user.id)

class SpamInfo(BaseModel, models.Model):
    """
    This model will store reported spam numbers by users
    """
    spam_number = models.CharField(verbose_name="Phone number", max_length=15)
    is_spam = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.is_spam)
