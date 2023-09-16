from django.db import models
from django.utils import timezone

from feedback.choices import GENDER_CHOICES


#This class helps us to store Feedback Form responces
class Feedback(models.Model):

    name = models.CharField(max_length=255, null=True, blank=False)
    surname = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True, help_text='Please type your country')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=250)
   
    email = models.EmailField(max_length=255, null=True, blank=False)
    message = models.TextField(null=True, blank=False)

    employee_for_feedback = models.ForeignKey("employee.Employee", null=True, blank=True,
                                on_delete=models.SET_NULL, related_name="+",
                                verbose_name="Employee", help_text='Choose employee')
    
    is_published = models.BooleanField(default=False)
    show_in_homepage = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    has_been_read = models.BooleanField(default=False)



    def __str__(self):
        return "{}".format(self.id)