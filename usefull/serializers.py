from rest_framework.fields import Field
from wagtail.models import Site
from core.serializers import CustomImageSerializer
from usefull.blocks import EstateRegisterSectionBlock

#
class BlogsSerializer(Field):
    def to_representation(self, value):
        result = []
        for item in value:
            page_dict = {
                'slug':item.slug,
                'slug2': item.slug2,
                'locale': item.locale.language_code,
                'title': item.title,
                'content': (item.content)[:90],
                'datetime': item.updated_at,
                'image': CustomImageSerializer().to_representation(item.blog_image) if item.blog_image else None,
            }
            result.append(page_dict)
        return result

#    
class NewsSerializer(Field):
    def to_representation(self, value):
        result = []
        for item in value:
            page_dict = {
                'slug': item.slug,
                'slug2': item.slug2,
                'locale': item.locale.language_code,
                'title': item.title,
                'content':(item.content)[:90],
                'datetime': item.updated_at,
                'image':  CustomImageSerializer().to_representation(item.news_image) if item.news_image else None, }

            result.append(page_dict)
        return result
    


#
class RealEstateSectionTabSerializer(Field):
    def to_representation(self, value):
        if value and len(value):
            sections = []
            for index, section_tab in enumerate(value, start=1):
                section_tab_data = section_tab.value
                data = {
                    "index": index,
                    "title": section_tab_data.get("title"),
                    "content": section_tab_data.get("content").source,
                }
                sections.append(data)
            return sections
        return None