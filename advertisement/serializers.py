from rest_framework.serializers import Field

from core.serializers import CustomImageSerializer


#This serializer is used in the APIField s of the
# (RentPropertyIndexPage.all_types, ByPropertyIndexPage.all_types, PropertyIndexPage.all_types ) 
class CityForPropertyIndexPageSerializer(Field):
    def to_representation(self, value):
        data_list = []
        for i in value:
            data = {
                'locale': i.locale.language_code,
                'slug2': i.slug2,
                'name': i.name,
                'id': i.id,
            }
            data_list.append(data)
        return data_list


#This serializer is used in the APIField s of the
# (RentPropertyIndexPage.all_types, ByPropertyIndexPage.all_types, PropertyIndexPage.all_types ) 
class TypeForPropertyIndexPageSerializer(Field):
    def to_representation(self, value):
        data_list = []
        for i in value:
            data = {
                'locale': i.locale.language_code,
                'slug2': i.slug2,
                'name': i.name,
                'id': i.id,
            }
            data_list.append(data)
        return data_list


#This serializer is used in the APIField s of the
#(HomePage.home_category_6_list, RentPropertyIndexPage.all_categories, ByPropertyIndexPage.all_categories,
#PropertyDetailPage.property_tags, PropertyDetailPage.property_categories)
class CategoryListSerializer(Field):
    def to_representation(self, value):
        category_list = []
        if value:
            for ctg in value:
                if isinstance(ctg, dict):
                    data = {
                        'locale': ctg['locale'],
                        'slug2': ctg['slug2'],
                        'name': None,
                        'id': None,
                        'image': None,
                        'existing_in_homepage': None,
                        'order_number': None,
                        'message': ctg['message'],
                    }
                else:
                    if ctg.slug2.startswith('advertisement_category'):
                        data = {
                        'locale': ctg.locale.language_code,
                        'slug2': ctg.slug2,
                        'name': ctg.name,
                        'id': ctg.id,
                        'image': CustomImageSerializer().to_representation(ctg.image) if ctg.image else None,
                        'existing_in_section_6s': ctg.existing_in_section_6s,
                        'order_number_section_6s': ctg.order_number_section_6s,
                        'existing_in_section_8s': ctg.existing_in_section_8s,
                        'order_number_section_8s': ctg.order_number_section_8s,
                        'message': None,
                        }

                    elif ctg.slug2.startswith('advertisement_tags'):
                        data = {
                        'locale': ctg.locale.language_code,
                        'slug2': ctg.slug2,
                        'name': ctg.name,
                        'id': ctg.id,
                        'image': CustomImageSerializer().to_representation(ctg.image) if ctg.image else None,
                        'existing_in_homepage': ctg.existing_in_homepage,
                        'order_number': ctg.order_number,
                        'message': None,

                        }
                    elif ctg.slug2.startswith('advertisement_offererperson'):
                        data = {
                        'locale': ctg.locale.language_code,
                        'slug2': ctg.slug2,
                        'name': ctg.name,
                        'id': ctg.id,
                        'image': CustomImageSerializer().to_representation(ctg.image) if ctg.image else None,
                        'existing_in_homepage': ctg.existing_in_homepage,
                        'order_number': ctg.order_number,
                        'message': None,
                        }
                category_list.append(data)
        return category_list

#------------------Field level serializers for PropertyDetailPage-----------------------
#
class CustomIdSerializer(Field):
    def to_representation(self, value):
        custom_id=None
        if value=='propertydetailpage':
            custom_id = 1
        else:
            custom_id = value.replace('propertydetailpage-','')
        return custom_id


#This serializer is used in the APIField s of the
# (PropertyDetailPage.property_city, PropertyDetailPage.property_region)
class PropertyDetailForeingkey2FieldSerializer(Field):
    def to_representation(self, value):
        data = None
        if value:
            if isinstance(value, dict):
                data = {
                    'locale': value['locale'],
                    'slug2': value['slug2'],
                    'id': None,
                    'name': None,
                    'message': value['message']
                }
            else:
                data = {
                    'locale': value.locale.language_code,
                    'slug2': value.slug2,
                    'id': value.id,
                    'name': value.name,
                    'message': None
                }
        return data


##This serializer is used in the APIField s of the (PropertyDetailPage.short_description_offer)
class PropertyOffererSerializer(Field):
    #def to_representation(self, value):
    #    if value:
    #        data = {
    #            'locale': value.locale.language_code,
    #            'slug2': value.slug2,
    #            'id': value.id,
    #            'name': value.name,
    #            'existing_in_homepage': value.existing_in_homepage,
    #            'order_number': value.order_number,
    #        }
    #    else:
    #        data = None
    #    return data

    def to_representation(self, value):
        data = None
        if value:
            if isinstance(value, dict):
                data = {
                    'locale': value['locale'],
                    'slug2': value['slug2'],
                    'id': None,
                    'name': None,
                    'existing_in_homepage': None,
                    'order_number': None,
                    'message': value['message'],
                }
            else:
                data = {
                    'locale': value.locale.language_code,
                    'slug2': value.slug2,
                    'id': value.id,
                    'name': value.name,
                    'existing_in_homepage': value.existing_in_homepage,
                    'order_number': value.order_number,
                    'message': None,
                }
        return data


#()
class CategoryForPropertyDetailPageSerializer(Field):
    def to_representation(self, value):
        if value:
            data = {
                'locale': value.locale.language_code,
                'slug2': value.slug2,
                'name': value.name,
                'id': value.id,
                'image': CustomImageSerializer().to_representation(value.image) if value.image else None,
                'existing_in_section_6s': value.existing_in_section_6s,
                'order_number_section_6s': value.order_number_section_6s,
                'existing_in_section_8s': value.existing_in_section_8s,
                'order_number_section_8s': value.order_number_section_8s,
            }
        return data



#This serializer is used in the APIField s of the 
# (PropertyDetailPage.similar_property_for_geo,RentPropertyIndexPage.rent_properties, 
# ByPropertyIndexPage.by_properties, PropertyIndexPage.all_properties,
# Homepage.home_all_advertisement_list, Homepage.home_ctg_1_properties, Homepage.home_ctg_2_properties,
# Homepage.home_ctg_3_properties, Homepage.home_ctg_4_properties,Homepage.home_ctg_5_properties, 
# Homepage.home_ctg_6_properties)

class SimilarPropertyDetailSerializer(Field):
    def to_representation(self, value):
        data_list = []
        for i in value:
            data = {
                'slug2': i.slug2,
                'id': i.id,
                'locale': i.locale.language_code,
                'title': i.title,
                'first_image': CustomImageSerializer().to_representation(i.first_image) if i.first_image else None,
                'property_city': i.property_region.city_rel.name,
                'property_region': i.property_region.name,
                'property_category': CategoryListSerializer().to_representation(i.property_category.all()),
                'area': i.area,
                'area_2': i.area_2,
                'short_description_rooms': HomeRoomSerialzer().to_representation(i.short_description_rooms.all()),
                'custom_id': CustomIdSerializer().to_representation(i.slug2),
                'general_cost': i.general_cost,
                'general_cost_second': i.general_cost_second,
                'discounted_cost': i.discounted_cost,
                'discounted_cost_second': i.discounted_cost_second,
                'longitude': i.longitude,
                'latitude': i.latitude,
            }
            data_list.append(data)
        return data_list

#class SimilarPropertyDetailSerializer(Field):
#    def to_representation(self, value):
#        data_list = []
#        for i in value:
#            data = {
#                'slug2': i.slug2,
#                'id': i.id,
#                'locale': i.locale.language_code,
#                'title': i.title,
#                'image': CustomImageSerializer().to_representation(i.first_image) if i.first_image else None,
#                'city': i.property_region.city_rel.name,
#                'region': i.property_region.name,
#                'categories': CategoryListSerializer().to_representation(i.property_category.all()),
#                'area': i.area,
#                'area_2': i.area_2,
#                'rooms_count': HomeRoomSerialzer().to_representation(i.short_description_rooms.all()),
#                'custom_id': CustomIdSerializer().to_representation(i.slug2),
#                'general_cost': i.general_cost,
#                'general_cost_second': i.general_cost_second,
#                'discounted_cost': i.discounted_cost,
#                'discounted_cost_second': i.discounted_cost_second,
#                'longitude': i.longitude,
#                'latitude': i.latitude,
#            }
#            data_list.append(data)
#        return data_list


#This serializer is used in the APIField s of the 
# (PropertyDetailPage.unit_cost, PropertyDetailPage.unit_discounted_cost )
class CostSerialzer(Field):
    def to_representation(self, value):
        return value
    


#
class HomeRoomSerialzer(Field):
    def to_representation(self, value):
        home_room_list = []
        if value:
            for i in value:
                if isinstance(i, dict):
                    data = {
                        'locale': i['locale'],
                        'slug2': i['slug2'],
                        'name': None,
                        'id': None,
                        'message': i['message'],
                    }
                else:
                    data = {
                    'locale': i.locale.language_code,
                    'slug2': i.slug2,
                    'name': i.name,
                    'id': i.id,
                    'message': None,
                    }
                home_room_list.append(data)
        return home_room_list