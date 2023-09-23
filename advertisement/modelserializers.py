from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField, SerializerMethodField
from rest_framework import serializers

from wagtail.api.v2.serializers import PageSerializer

from advertisement.models import Category, Type, City, Region, Tags, Room , PropertyDetailPage
from advertisement.forms import PropertyRequestTypes, PropertyDetailForm, PropertyDetailOnlineVisitForm
from core.serializers import CustomImageSerializer


#
class TypeSerializer(ModelSerializer):
    locale = SerializerMethodField()

    class Meta:
        model = Type
        fields = ['id', 'name', 'slug2', 'locale', ]

    def get_locale(self, obj):
        return obj.locale.language_code if obj.locale else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['locale'] = self.get_locale(instance)
        return representation


#
class CitySerializer(ModelSerializer):
    locale = serializers.SerializerMethodField()
    
    class Meta:
        model = City
        fields = ('id', 'name', 'slug2', 'locale',)

    def get_locale(self, obj):
        return obj.locale.language_code if obj.locale else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['locale'] = self.get_locale(instance)
        return representation

#
class RegionSerializer(serializers.ModelSerializer):
    city_rel = serializers.SlugRelatedField(slug_field='slug2', queryset=City.objects.all())
    locale = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = ('id', 'name', 'city_rel', 'slug2', 'locale',)

    def get_locale(self, obj):
        return obj.locale.language_code if obj.locale else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['locale'] = self.get_locale(instance)
        return representation


#
class TagSerializer(ModelSerializer):
    locale = SerializerMethodField()

    class Meta:
        model = Tags
        fields  = '__all__'

    def get_locale(self, obj):
        return obj.locale.language_code if obj.locale else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['locale'] = self.get_locale(instance)
        return representation

#
class RoomSerializer(ModelSerializer):

    class Meta:
        model = Room
        fields  = '__all__'

    def get_locale(self, obj):
        return obj.locale.language_code if obj.locale else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['locale'] = self.get_locale(instance)
        return representation


#
class CategorySerializer(serializers.ModelSerializer):
    locale = serializers.SerializerMethodField()
    image = CustomImageSerializer()

    class Meta:
        model = Category
        fields = '__all__'

    def get_locale(self, obj):
        return obj.locale.language_code if obj.locale else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['locale'] = self.get_locale(instance)
        return representation
    

#
class PropertyRequestTypesSerializer(ModelSerializer):
    locale = SerializerMethodField()

    class Meta:
        model = PropertyRequestTypes
        fields = ('id', 'slug2', 'locale', 'name',)

    def get_locale(self, obj):
        return obj.locale.language_code if obj.locale else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['locale'] = self.get_locale(instance)
        return representation
    

#
class PropertyDetailFormSerializer(ModelSerializer):
#    request_choices = PrimaryKeyRelatedField(queryset=PropertyRequestTypes.objects.all())

    class Meta:
        model = PropertyDetailForm
        fields = ('id', 'name', 'surname', 'phone_number', #'request_choices',
                  'email', 'message', 'created_at', 'property_locale', 'property_slug2', 'property_custom_id')

        extra_kwargs = {
            'property_locale': {'write_only': True},
            'property_slug2': {'write_only': True},
            'property_custom_id': {'write_only': True},
        }

    def create(self, validated_data):
        # You can extract the property_locale, property_slug2, and property_custom_id
        # values from the validated_data and save them in the database during object creation.
        property_locale = validated_data.pop('property_locale')
        property_slug2 = validated_data.pop('property_slug2')
        property_custom_id = validated_data.pop('property_custom_id')

        instance = PropertyDetailForm.objects.create(**validated_data,
                                                     property_locale=property_locale,
                                                     property_slug2=property_slug2,
                                                     property_custom_id=property_custom_id)
        return instance
    


#
class PropertyDetailOnlineVisitFormSerializer(ModelSerializer):

    class Meta:
        model = PropertyDetailOnlineVisitForm
        fields = ('id', 'name', 'surname', 'phone_number', 'email', 'message', 'created_at',
                   'has_been_read', 'property_locale', 'property_slug2', 'property_custom_id')

        extra_kwargs = {
            'property_locale': {'write_only': True},
            'property_slug2': {'write_only': True},
            'property_custom_id': {'write_only': True},
        }

    def create(self, validated_data):
        # You can extract the property_locale, property_slug2, and property_custom_id
        # values from the validated_data and save them in the database during object creation.
        property_locale = validated_data.pop('property_locale')
        property_slug2 = validated_data.pop('property_slug2')
        property_custom_id = validated_data.pop('property_custom_id')

        instance = PropertyDetailOnlineVisitForm.objects.create(**validated_data,
                                                     property_locale=property_locale,
                                                     property_slug2=property_slug2,
                                                     property_custom_id=property_custom_id)
        return instance
    


#
class PropertyDetailPageSerializer(PageSerializer):
    property_category = CategorySerializer(many=True)
    property_tags = TagSerializer(many=True)
    short_description_rooms = RoomSerializer(many=True)
    property_type = TypeSerializer() 

    class Meta:
        model = PropertyDetailPage
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['property_category'] = CategorySerializer(instance.property_category.all(), many=True).data
        representation['property_tags'] = TagSerializer(instance.property_tags.all(), many=True).data
        representation['short_description_rooms'] = RoomSerializer(instance.short_description_rooms.all(), 
                                                                   many=True).data

        return representation