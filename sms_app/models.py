from datetime import timedelta
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class Message(models.Model):
    sms_id = models.CharField(max_length=50, null=False, blank=False, primary_key=True)
    number = PhoneNumberField(null=False, blank=False)
    message = models.CharField(max_length=200)
    status = models.CharField(max_length=20)
    date = models.DateTimeField('date sent')
    
    def __str__(self):
        return f"{self.number} | {self.message} | {self.status} | {self.date}"

    def was_sent_recently(self):
        return self.date >= timezone.now() - timedelta(days=1)
