from rest_framework.fields import Field
from rest_framework.serializers import ModelSerializer

from wagtail.models import Site

from core.serializers import CustomSvgSerializer, CustomImageSerializer
from services.forms import OrientationForm, ConsultingForm, OnlineVisitForm, SellPropertyForm


#This serializer helps to serialize icon data of every servicedetailpage for serviceindexpage
class ChildSvgSerializer(Field):
    def to_representation(self, value):
        if value and len(value) > 0:
            svg_block = value[0].value
            url = svg_block.file.url
            page_dict = {
                "id": svg_block.id,
                "file": url,
                "title": svg_block.title,
                "tags": svg_block.tags.names()
            }
            return page_dict
        return None



#This serializer helps to give data(icon, page_titles) from child service detail pages into service index page
class ChildServiceDataSerializer(Field):
    def to_representation(self, value):
        if value and len(value) > 0:
            #x = value[0].value
            for footer_tab in value:
                data = {
                    'slug2': footer_tab.slug2,
                    'locale': footer_tab.locale.language_code,
                    'title': footer_tab.title,
                    'icon1': ChildSvgSerializer().to_representation(footer_tab.service_parent_icon),
                }
            return data
        
        return None


#This serializer helps to serialize OrientationTourServicePage.section_tab field
class Section1TabSerializer(Field):
    def to_representation(self, value):
        if value and len(value) > 0:
            x = value[0].value
            icons = []
            for section_tab in value:
                section_tab_data = section_tab.value
                icon_data = {
                    'icon': CustomSvgSerializer().to_representation(section_tab_data.get('icon')),
                    'text_icon': section_tab_data.get('text_icon'),
                }
                icons.append(icon_data)
            return icons
        return None
    

#This class help to serialize Post_Sale_Service.service_data (inline fields) field
class ServiceDataSerializer(Field):
    def to_representation(self, value):
        data_list = []
        for i in value:
            data = {
                "service_name": i.name,
                "service_content": i.content,
                "service_image": CustomImageSerializer().to_representation(i.image)
            }
            data_list.append(data)
        return data_list


#This class help to serialize Post_Sale_Service.section2_contents field
class Section4TabSerializer(Field):

    def to_representation(self, value):
        if value and len(value):
            sections = []
            x = value[0].value
            for section_tab in value:
                section_tab_data = section_tab.value
                data = {
                    "service_name": section_tab_data.get("service_name"),
                    "service_content": section_tab_data.get('service_content'),
                    "service_image": CustomImageSerializer().to_representation(x.get('service_image')),
                }
                sections.append(data)
            return sections
        return None

#    
class FAQSerializer(Field):
    def to_representation(self, child_pages):
        return_pages = []
        for child in child_pages:
            page_dict = {
                "id": child.id,
                "question": child.question,
                "answer": child.answer,
            }
            return_pages.append(page_dict)

        return return_pages
    
#--------------------------------------FormSerializers---------------------------------------------

#
class OrientationFormSerializer(ModelSerializer):

    class Meta:
        model = OrientationForm
        fields = '__all__'

#
class ConsultingFormSerializer(ModelSerializer):
    class Meta:
        model = ConsultingForm
        fields = '__all__'


#
class OnlineVisitFormSerializer(ModelSerializer):
    class Meta:
        model = OnlineVisitForm
        fields = '__all__'


#
class SellPropertyFormSerializer(ModelSerializer):
    class Meta:
        model = SellPropertyForm
        fields = '__all__'






