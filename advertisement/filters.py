from django_filters import rest_framework as django_filters

from rest_framework import filters

from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.filters import (AncestorOfFilter, ChildOfFilter, DescendantOfFilter, FieldsFilter, 
                                    LocaleFilter, OrderingFilter, SearchFilter, TranslationOfFilter, )

from advertisement.models import PropertyDetailPage
from advertisement.modelserializers import PropertyDetailPageSerializer


class PropertyDetailPageFilter(django_filters.FilterSet):

    facility_open_pool = django_filters.BooleanFilter(
                                                field_name='facility_open_pool', 
                                                lookup_expr='exact')
    facility_green_garden = django_filters.BooleanFilter(
                                                field_name='facility_green_garden', 
                                                lookup_expr='exact')
    facility_wireless_internet = django_filters.BooleanFilter(
                                                field_name='facility_wireless_internet', 
                                                lookup_expr='exact')
    facility_satellite_tv = django_filters.BooleanFilter(
                                                field_name='facility_satellite_tv', 
                                                lookup_expr='exact')
    facility_concierge = django_filters.BooleanFilter(
                                                field_name='facility_concierge', 
                                                lookup_expr='exact')
    facility_outdoor_parking =django_filters.BooleanFilter(
                                                field_name='facility_outdoor_parking', 
                                                lookup_expr='exact')
    facility_power_generator = django_filters.BooleanFilter(
                                                field_name='facility_power_generator', 
                                                lookup_expr='exact')
    facility_finnish_sauna = django_filters.BooleanFilter(
                                                field_name='facility_finnish_sauna', 
                                                lookup_expr='exact')
    facility_playground = django_filters.BooleanFilter(
                                                field_name='facility_playground', 
                                                lookup_expr='exact')
    facility_fitness_centre = django_filters.BooleanFilter(
                                                field_name='facility_fitness_centre', 
                                                lookup_expr='exact')
    facility_game_room = django_filters.BooleanFilter(
                                                field_name='facility_game_room', 
                                                lookup_expr='exact')
    facility_gazebos_for_rest = django_filters.BooleanFilter(
                                                field_name='facility_gazebos_for_rest', 
                                                lookup_expr='exact')
    facility_covered_parking = django_filters.BooleanFilter(
                                                field_name='facility_covered_parking', 
                                                lookup_expr='exact')
    facility_aquapark = django_filters.BooleanFilter(
                                                field_name='facility_aquapark', 
                                                lookup_expr='exact')
    facility_amphitheater = django_filters.BooleanFilter(
                                                field_name='facility_amphitheater', 
                                                lookup_expr='exact')
    facility_pool_bar = django_filters.BooleanFilter(
                                                field_name='facility_pool_bar', 
                                                lookup_expr='exact')
    facility_billiards = django_filters.BooleanFilter(
                                                field_name='facility_billiards', 
                                                lookup_expr='exact')
    facility_bowling = django_filters.BooleanFilter(
                                                field_name='facility_bowling', 
                                                lookup_expr='exact')
    facility_jacuzzi = django_filters.BooleanFilter(
                                                field_name='facility_jacuzzi', 
                                                lookup_expr='exact')
    facility_indoor_pool = django_filters.BooleanFilter(
                                                field_name='facility_indoor_pool', 
                                                lookup_expr='exact')
    facility_cafe_restaurant = django_filters.BooleanFilter(
                                                field_name='facility_cafe_restaurant', 
                                                lookup_expr='exact')
    facility_cinema = django_filters.BooleanFilter(
                                                field_name='facility_cinema', 
                                                lookup_expr='exact')
    facility_conference_hall = django_filters.BooleanFilter(
                                                field_name='facility_conference_hall', 
                                                lookup_expr='exact')
    facility_24_hour_security = django_filters.BooleanFilter(
                                                field_name='facility_24_hour_security', 
                                                lookup_expr='exact')
    facility_ice_rink = django_filters.BooleanFilter(
                                                field_name='facility_ice_rink', 
                                                lookup_expr='exact')
    facility_market = django_filters.BooleanFilter(
                                                field_name='facility_market', 
                                                lookup_expr='exact')
    facility_massage_rooms = django_filters.BooleanFilter(
                                                field_name='facility_massage_rooms', 
                                                lookup_expr='exact')
    facility_mini_club = django_filters.BooleanFilter(
                                                field_name='facility_mini_club', 
                                                lookup_expr='exact')
    facility_table_tennis = django_filters.BooleanFilter(
                                                field_name='facility_table_tennis', 
                                                lookup_expr='exact')
    facility_barbershop = django_filters.BooleanFilter(
                                                field_name='facility_barbershop', 
                                                lookup_expr='exact')
    facility_walking_paths = django_filters.BooleanFilter(
                                                field_name='facility_walking_paths', 
                                                lookup_expr='exact')
    facility_roman_steam_room = django_filters.BooleanFilter(
                                                field_name='facility_roman_steam_room', 
                                                lookup_expr='exact')
    facility_private_beach = django_filters.BooleanFilter(
                                                field_name='facility_private_beach', 
                                                lookup_expr='exact')
    facility_tennis_court = django_filters.BooleanFilter(
                                                field_name='facility_tennis_court', 
                                                lookup_expr='exact')
    facility_turkish_hamam = django_filters.BooleanFilter(
                                                field_name='facility_turkish_hamam', 
                                                lookup_expr='exact')
    facility_shuttle_beach = django_filters.BooleanFilter(
                                                field_name='facility_shuttle_beach', 
                                                lookup_expr='exact')
    facility_children_swimming_pool = django_filters.BooleanFilter(
                                                field_name='facility_children_swimming_pool', 
                                                lookup_expr='exact')
    facility_video_surveillance = django_filters.BooleanFilter(
                                                field_name='facility_video_surveillance', 
                                                lookup_expr='exact')
    facility_basketball_playground = django_filters.BooleanFilter(
                                                field_name='facility_basketball_playground', 
                                                lookup_expr='exact')
    facility_rest_and_bbg_areas = django_filters.BooleanFilter(
                                                field_name='facility_rest_and_bbg_areas', 
                                                lookup_expr='exact')
    short_description_furniture = django_filters.BooleanFilter(
                                                field_name='short_description_furniture',
                                                lookup_expr='exact')
    
    short_description_sea_view = django_filters.BooleanFilter(
                                                field_name='short_description_sea_view',
                                                lookup_expr='exact')
    facility_lift = django_filters.BooleanFilter(
                                                field_name='facility_lift', 
                                                lookup_expr='exact')
    facility_terras = django_filters.BooleanFilter(
                                                field_name='facility_terras', 
                                                lookup_expr='exact')


    property_city__name = django_filters.CharFilter(
        method='filter_property_city_name',
        label='Property City Name',)


    class Meta:
        model = PropertyDetailPage
        fields = {

            'property_category__slug2': ['exact'],
            'property_type__slug2': ['exact'],
            'property_region__slug2': ['exact'],
            'property_tags__slug2': ['exact'],
            'short_description_rooms__slug2': ['exact'],
            'short_description_offer__slug2': ['exact'],

            'short_description_floor':['exact', 'gte', 'lte'],
            'short_description_gross_area': ['exact', 'gte', 'lte'],
            'short_description_to_the_sea': ['exact',  'gte', 'lte'],
            'short_description_to_the_center': ['exact', 'gte', 'lte'],
            'short_description_to_the_airport': ['exact', 'gte', 'lte'],
            'short_description_year': ['exact', 'gte', 'lte'],
            'general_cost': ['exact', 'gte', 'lte'],
            'discounted_cost': ['exact', 'gte', 'lte'],
            'discounted_cost_second': ['exact', 'gte', 'lte'],
            'area': ['exact', 'gte', 'lte'],

            # Add other fields as needed
        }

    def filter_property_city_name(self, queryset, name, value):
        # Perform filtering based on property_city__name (non-model field)
        return queryset.filter(property_region__city_rel__name=value)


class PropertyDetailPageListView(PagesAPIViewSet):
    base_serializer_class = PropertyDetailPageSerializer

    filter_backends = [filters.OrderingFilter, filters.SearchFilter, django_filters.DjangoFilterBackend,
                        FieldsFilter, ChildOfFilter, AncestorOfFilter, DescendantOfFilter, OrderingFilter,
                        TranslationOfFilter, LocaleFilter, SearchFilter, ]
  
    ordering_fields = ['publishing_date', 'discounted_cost',]  # Fields to order by
    filterset_class = PropertyDetailPageFilter

    known_query_parameters = PagesAPIViewSet.known_query_parameters.union(
        ['property_type__slug2', 'property_category__slug2', 'property_city__name',
         'property_region__slug2', 'property_tags__slug2', 'short_description_rooms__slug2', 
         'short_description_offer__name', 'general_cost', 'general_cost__lte', 'general_cost__gte',
         'custom_id', 'longitude', 'latitude', 'discounted_cost', 'discounted_cost__gte', 'discounted_cost__lte',
         'area', 'area__gte', 'area__lte',      
         'short_description_floor', 'short_description_floor__gte', 'short_description_floor__lte', 
         'short_description_year', 'short_description_year__lte', 'short_description_year__gte',
         'short_description_to_the_sea', 'short_description_to_the_sea__gte', 'short_description_to_the_sea__lte',
         'short_description_to_the_center', 'short_description_to_the_center__gte', 'short_description_to_the_lte',
         'short_description_to_the_airport', 'short_description_to_the_airport__gte',
         'short_description_to_the_airport__lte', ]
    )


    listing_default_fields = PagesAPIViewSet.listing_default_fields + [
        "title",'slug2', 'slug', 'property_type', 'property_category', 'property_city', 'property_region', 
        'short_description_rooms', 'custom_id', 'area', 'area_2', 'general_cost', 'general_cost_second', 
        'discounted_cost', 'discounted_cost_second', 'first_image', 'longitude', 'latitude',]
    

    def get_queryset(self):
        return PropertyDetailPage.objects.filter(live=True)
    
    def get_property_category(self):
        return self.property_category.all()