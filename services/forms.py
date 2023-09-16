from django.db import models
from django.utils import timezone

from services.choices import FINISHING_CHOICES
#
class OrientationForm(models.Model):

    name = models.CharField(max_length=255, null=True, blank=False)
    surname = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=17, null=True, blank=True)
    email = models.EmailField(null=True, blank=False)
    arrival_date = models.DateField()
    return_date = models.DateField()
    people_count = models.IntegerField()
    message = models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    has_been_read = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.id)



#
class OnlineVisitForm(models.Model):

    name = models.CharField(max_length=255, null=True, blank=False)
    surname = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=17, null=True, blank=True)
    email = models.EmailField(null=True, blank=False)
    skype = models.CharField(max_length=255, null=True, blank=False)
    visit_date = models.DateField()
    message = models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    updatet_at = models.DateTimeField(auto_now=True)
    has_been_read = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.id)

#
class PostSaleServiceForm(models.Model):

    name = models.CharField(max_length=255, null=True, blank=False)
    surname = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=17, null=True, blank=True)
    email = models.EmailField(null=True, blank=False)
    service_choices = models.ForeignKey('services.Servicemodel', on_delete=models.SET_NULL, 
                                        null=True, blank=True, help_text='Choose service')

    message = models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    has_been_read = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.id)


#    
class ConsultingForm(models.Model):

    name = models.CharField(max_length=255, null=True, blank=False)
    surname = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=17, null=True, blank=True)
    email = models.EmailField(null=True, blank=False)
    message = models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    has_been_read = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.id)
    

#
class SellPropertyForm(models.Model):

    name = models.CharField(max_length=255, null=True, blank=False)
    surname = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=17, null=True, blank=True)
    email = models.EmailField(null=True, blank=False)
    type = models.CharField(max_length=255, null=True, blank=False)
    city = models.CharField(max_length=255, null=True, blank=False)
    required_cost = models.CharField(max_length=255, null=True, blank=False)
    address = models.CharField(max_length=255, null=True, blank=False)
    message = models.TextField(null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    has_been_read = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.id)
#


class ApartmentExchangeForm(models.Model):

    property_category = models.ForeignKey('advertisement.Category', on_delete=models.SET_NULL, 
                                            null=True, blank=True, help_text='Choose service')
    city = models.CharField(max_length=255, null=True, blank=False)
    district = models.CharField(max_length=255, null=True, blank=False)
    construction_year = models.IntegerField()
    number_of_floors = models.CharField(max_length=255, null=True, blank=False)
    floor = models.CharField(max_length=255, null=True, blank=False)
    asseded_value = models.CharField(max_length=255, null=True, blank=False)
    number_of_rooms = models.CharField(max_length=255, null=True, blank=False)
    number_of_bedrooms = models.CharField(max_length=255, null=True, blank=False)
    balcony_porch = models.CharField(max_length=255, null=True, blank=False)
    total_square = models.FloatField(null=True, blank=True)
    finishing = models.CharField(choices=FINISHING_CHOICES, max_length=250)

#additional_parameters
    furniture = models.BooleanField()
    internet = models.BooleanField()
    satellite_tv = models.BooleanField()
    doorphone = models.BooleanField()
    irondoor = models.BooleanField()
    parking_space_garage = models.BooleanField()
    playground = models.BooleanField()
    cctv = models.BooleanField()
    phone = models.BooleanField()
    lift = models.BooleanField()
    signaling = models.BooleanField()
    bathrooms_2_and_more = models.BooleanField()
    open_parking = models.BooleanField()
    underground_parking = models.BooleanField()
    concierge = models.BooleanField()
    security_24_7 = models.BooleanField()

#
    advantages_of_your_offer = models.TextField()
    what_to_excange = models.TextField()
    name = models.CharField(max_length=255, null=True, blank=False)
    phone_number = models.CharField(max_length=17, null=True, blank=True)
    email = models.EmailField(null=True, blank=False)
    skype = models.CharField(max_length=255, null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    has_been_read = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.id)