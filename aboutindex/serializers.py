from rest_framework.fields import Field
from rest_framework import serializers
import uuid
#from wagtail.images.api.v2.serializers import ImageSerializer
#from wagtail.models import Site
from core.serializers import CustomImageSerializer, CustomSvgSerializer


#
class HeaderTabSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    image = CustomImageSerializer()

    def to_representation(self, value):
        if value and len(value) > 0:
            header_tab = value[0].value
            result = {
                'title': header_tab.get('title'),
                'content': header_tab.get('content'),
                'image': self.fields['image'].to_representation(header_tab.get('image'))
            }
            return result
        return None

#
class AdvantagesTabSerializer(serializers.Field):
    def to_representation(self, value):
        if value and len(value) > 0:
            advantages_tab = value[0].value
            result = {
                'title': advantages_tab.get('title'),
                'icon': CustomSvgSerializer().to_representation(advantages_tab.get('icon')),
                'advantage_elements': self.serialize_elements(advantages_tab.get('advantage_elements', []))
            }
            return result
        return None

    def serialize_elements(self, elements):
        serialized_elements = []
        for element in elements:
            if isinstance(element, str):
                serialized_elements.append(element)
        return serialized_elements
    
#
class CenterTabSerializer(Field):
    def to_representation(self, value):
        if value and len(value) > 0:
            center_tab = value[0].value
            result = {
                'title': center_tab.get('title'),
                'content': center_tab.get('content').source,
            }
            return result
        return None

#
class FooterTabSerializer(Field):
    def to_representation(self, value):
        if value and len(value) > 0:
            icons = []
            for footer_tab in value:
                footer_tab_data = footer_tab.value
                icon_data = {
#                    'icon': CustomSvgSerializer().to_representation(footer_tab_data.get('icon')),
                    'hover_color': footer_tab_data.get('hover_color'),
                    'text_icon': footer_tab_data.get('text_icon'),
                }
                icons.append(icon_data)
            return icons
        return None

#
class CompanyDetailsTabSerializer(Field):
    def to_representation(self, value):
        if value and len(value) > 0:
            company_details_tab = value[0].value

            result = {
                'title': company_details_tab.get('title'),
                'company_name_title': company_details_tab.get('company_name_title'),
                'company_name_value': company_details_tab.get('company_name_value'),
                'company_address_title': company_details_tab.get('company_address_title'),
                'company_address_value': company_details_tab.get('company_address_value'),
                'tax_administration_title': company_details_tab.get('tax_administration_title'),
                'tax_administration_value': company_details_tab.get('tax_administration_value'),
                'tax_number_title': company_details_tab.get('tax_number_title'),
                'tax_number_value': company_details_tab.get('tax_number_value'),
            }
            return result
        return None

#    
class BankAccountDetailsTabSerializer(Field):
    def to_representation(self, value):
        if value and len(value) > 0:
            company_details_tab = value[0].value

            result = {
                'title': company_details_tab.get('title'),
                'bank_branch_title': company_details_tab.get('bank_branch_title'),
                'bank_branch_value': company_details_tab.get('bank_branch_value'),
                'bank_address_title': company_details_tab.get('bank_address_title'),
                'bank_address_value': company_details_tab.get('bank_address_value'),
                'bank_branch_code_title': company_details_tab.get('bank_branch_code_title'),
                'bank_branch_code_value': company_details_tab.get('bank_branch_code_value'),
                'swift_code_title': company_details_tab.get('swift_code_title'),
                'swift_code_value': company_details_tab.get('swift_code_value'),
                'company_address_title': company_details_tab.get('company_address_title'),
                'company_address_value': company_details_tab.get('company_address_value'),
            }

            return result
        return None


#If you need an unique id for every member of team, you can use this serializer, else, you must
#uncomment lass commented serializer and use it

class SectionAboutMemberSerializer(serializers.Serializer):
    member_image = CustomImageSerializer()
    member_name = serializers.CharField()
    job_description = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    languages_title = serializers.CharField()
    languages = serializers.ListField(child=serializers.CharField())
    id = serializers.SerializerMethodField()
    
    def to_representation(self, value):
        if value and len(value) > 0:
            members = []

            for member in value:
                member_tab = member.value

                member_data = {
                    'id': self.get_id(member_tab),
                    'member_image': CustomImageSerializer().to_representation(member_tab.get('member_image')),
                    'member_name': member_tab.get('member_name'),
                    'job_description': member_tab.get('job_description'),
                    'email': member_tab.get('email'),
                    'phone_number': member_tab.get('phone_number'),
                    'languages_title': member_tab.get('languages_title'),
                    'languages': self.serialize_elements(member_tab.get('languages', []))
                }
                members.append(member_data)
            return members
        return None

    def get_id(self, obj):
        return str(uuid.uuid4())

    def serialize_elements(self, elements):
        serialized_elements = []
        for element in elements:
            if isinstance(element, str):
                serialized_elements.append(element)
        return serialized_elements

#class SectionAboutMemberSerializer(Field):
#    def to_representation(self, value):
#        if value and len(value) > 0:
#            members = []
#
#            for member in value:
#                member_tab = member.value
#
#                member_data = {
#                    'member_image': CustomImageSerializer().to_representation(member_tab.get('member_image')),
#                    'member_name': member_tab.get('member_name'),
#                    'job_description': member_tab.get('job_description'),
#                    'email': member_tab.get('email'),
#                    'phone_number': member_tab.get('phone_number'),
#                    'languages_title': member_tab.get('languages_title'),
#                    'languages': self.serialize_elements(member_tab.get('languages', []))
#
#                }
#                members.append(member_data)
#            return members
#        return None
#
#    def serialize_elements(self, elements):
#        serialized_elements = []
#        for element in elements:
#            if isinstance(element, str):
#                serialized_elements.append(element)
#        return serialized_elements
#
