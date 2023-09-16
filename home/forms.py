from django.db import models
from django.utils import timezone


#
class HelpForPropertyChoiceForm(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    surname = models.CharField(max_length=255, null=True, blank=False)
    email = models.EmailField(max_length=255, null=True, blank=False)
    phone_number = models.CharField(max_length=255, null=True, blank=False)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    has_been_read = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.id)
    


#
class AskQuestionForm(models.Model):

    name = models.CharField(max_length=255, null=True, blank=False)
    surname = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=17, null=True, blank=True)
    email = models.EmailField(null=True, blank=False)
    message = models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    has_been_read = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.id)
    
class AskCallForm(models.Model):

    name = models.CharField(max_length=255, null=True, blank=False)
    phone_number = models.CharField(max_length=17, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    has_been_read = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.message)
    
    
