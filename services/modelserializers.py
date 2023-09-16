from rest_framework.serializers import (ModelSerializer, SerializerMethodField, 
                                        PrimaryKeyRelatedField, ChoiceField, Serializer, CharField)

from services.models import Servicemodel
from services.forms import PostSaleServiceForm, ApartmentExchangeForm
from services.choices import FINISHING_CHOICES
from advertisement.models import Category

#
class ServicemodelSerializer(ModelSerializer):
    locale = SerializerMethodField()

    class Meta:
        model = Servicemodel
        fields = ('id', 'content', 'locale', 'name',)

    def get_locale(self, obj):
        return obj.locale.language_code if obj.locale else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['locale'] = self.get_locale(instance)
        return representation
    

#Serializer for PostSaleServiceForm model
class PostSaleServiceFormSerializer(ModelSerializer):
    service_choices = PrimaryKeyRelatedField(queryset=Servicemodel.objects.all())

    class Meta:
        model = PostSaleServiceForm
        fields = ('id', 'name', 'surname', 'phone_number', 'service_choices',
                  'email', 'message', 'created_at', 'has_been_read')


#
class ApartmentExchangeFormSerializer(ModelSerializer):
    property_category = PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = ApartmentExchangeForm
        fields = ('id', 'name',  'email', 'phone_number', 'skype', 'city', 'district', 
                  'construction_year', 'number_of_floors', 'floor', 'asseded_value', 
                  'number_of_rooms', 'number_of_bedrooms', 'balcony_porch', 'total_square', 
                  'finishing', 'furniture', 'internet', 'satellite_tv', 'doorphone', 
                  'irondoor', 'parking_space_garage', 'playground', 'cctv', 'lift',
                  'phone', 'signaling', 'bathrooms_2_and_more', 'open_parking', 
                  'underground_parking', 'concierge', 'security_24_7', 'advantages_of_your_offer',
                   'what_to_excange', 'property_category', 'created_at', 'has_been_read')

    finishing = ChoiceField(choices=FINISHING_CHOICES)


#
class FinishingChoiceSerializer(Serializer):
    choice = CharField()
