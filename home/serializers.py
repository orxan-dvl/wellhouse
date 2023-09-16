from rest_framework.serializers import Field

from core.serializers import CustomImageSerializer, CustomSvgSerializer
from employee.serializers import ProfessionSerializer, LanguagesSerializer


#This serializer is used in the APIField s of the
# (RentPropertyIndexPage.all_types, ByPropertyIndexPage.all_types, PropertyIndexPage.all_types ) 
class HomeTagsListSerializer(Field):
    def to_representation(self, value):
        data_list = []
        if value:
            for i in value:
                data = {
                    'locale': i.locale.language_code,
                    'slug2': i.slug2,
                    'id': i.id,
                    'name': i.name,
                    'image': CustomImageSerializer().to_representation(i.image) if i.image else None,
                    'existing_in_homepage': i.existing_in_homepage,
                    'order_number': i.order_number,
                }
                data_list.append(data)
        return data_list


#(HomePage.advantages_section_data)
class HomeAdvantagesSerializer(Field):
    def to_representation(self, value):
        if value and len(value) > 0:
            icons = []
            for advantage in value:
                advantage_data = advantage.value
                icon_data = {
                    'title_icon': advantage_data.get('title'),
                }
                icons.append(icon_data)
            return icons
        return None
    
#
class HomeEmployeeListSerializer(Field):
    def to_representation(self, value):
        data_list = []
        if value:
            for i in value:
                data = {
                    'locale': i.locale.language_code,
                    'slug2': i.slug2,
                    'id': i.id,
                    'fullname': i.fullname,
                    'profession': ProfessionSerializer().to_representation(i.profession) if i.profession else None,

                    'phone_number': i.phone_number,
                    'email': i.email, 
                    'image': CustomImageSerializer().to_representation(i.image) if i.image else None,
                    'languages_spoken': LanguagesSerializer(many=True).to_representation(i.languages_spoken.all()),
                    'created_at': i.created_at,
                    'updated_at': i.updated_at,
                }
                data_list.append(data)
        return data_list


#( Homepage.icon_tab ) APIField
class IconTabSerializer(Field):
    def to_representation(self, value):
        if value and len(value) > 0:
            icons = []
            for icon_tab in value:
                icon_tab_data = icon_tab.value
                icon_data = {
                    'background_color': icon_tab_data.get('background_color'),
                    'text_icon': icon_tab_data.get('text_icon'),
                }
                icons.append(icon_data)
            return icons
        return None