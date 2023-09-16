from PIL import Image

from rest_framework.fields import Field
from rest_framework.serializers import ModelSerializer


from wagtail.models import Site
from wagtail.images.api.v2.serializers import ImageDownloadUrlField
from wagtail.images import get_image_model
from wagtail.images.shortcuts import get_rendition_or_not_found

from core.models import SiteSetting, SocialMediaSetting

#from taggit_serializer.serializers import (TagListSerializerField,
#                                           TaggitSerializer)

from wagtailsvg.models import Svg



class CustomSvgSerializer(Field):
    def to_representation(self, svg):
        url = svg.file.url
        page_dict = {
            "id": svg.id,
            "file": url,
            "title": svg.title,
            "tags": svg.tags.names()
        }
        return page_dict


#
class CustomImageSerializer(Field):
    def to_representation(self, background_image):
        page_dict = {
            "id": background_image.id if background_image else None,
            "image": ImageDownloadUrlField().to_representation(background_image) if background_image else None,
            "title": background_image.title if background_image else None,
        }

        return page_dict


#
class SearchImageSerializer(Field):
    def resize_image(self, image, width, height):
        img = Image.open(image.file)
        img = img.resize((width, height), Image.ANTIALIAS)

        # Create a new image model with the resized image
        image_model = get_image_model()
        new_image = image_model.objects.create(
            title=f"{image.title} - {width}x{height}",
            file=image.file,
        )
        new_image.file.save(image.file.name, img)

        return new_image

    def to_representation(self, background_image):
        img_8_4 = get_rendition_or_not_found(background_image, f'fill-{800}x{412}')
        img_120_63 = get_rendition_or_not_found(background_image, f'fill-{1200}x{630}')
        # Construct the URL for the resized image
        page_dict = {'img_800_412':
            {
            "id": background_image.id,
            "image": ImageDownloadUrlField().to_representation(img_8_4) if img_8_4 else None,

            "title": background_image.title,
        },
        'img_1200_630':
            {
            "id": background_image.id,
            "image": ImageDownloadUrlField().to_representation(img_120_63) if img_120_63 else None,

            "title": background_image.title,

            }
        }
        return page_dict



#
class CustomVideoSerializer(Field):
    def to_representation(self, value):
        page_dict = {
            "id": value.id,
            "video": f'http://{Site.objects.filter(is_default_site=True).last().hostname}/media/{value.file}',
            "title": value.title,
        }

        return page_dict


#
class MultipleImageSerializer(Field):
    def to_representation(self, images):
        result = []
        if not images:  # Check if the list is empty
            return result
        
        for image in images:
            image_data = {
                "id": image.id if image else None,
                "image": ImageDownloadUrlField().to_representation(image) if image else None,
                "title": image.title if image else None,
            }
            result.append(image_data)
        
        return {
            "images": result,
        }
    

class SiteSettingSerializer(ModelSerializer):
    favicon = CustomImageSerializer()
    logo = CustomSvgSerializer()
        
    class Meta:
        model = SiteSetting
        fields = '__all__'


class SocialMediaSettingSerializer(ModelSerializer):
    class Meta:
        model = SocialMediaSetting
        fields = '__all__'


class FullPathSerializer(Field):
    def to_representation(self, value):
        
        if value and len(value)==2:
            data = {
                "root": value[0],
                "self_page": value[1],
            }
        elif value and len(value)==3:
            data = {
                "root": value[0],
                "parent": value[1],
                "self_page": value[2],
            }

        elif value and len(value)==1:
            data = {
                "root": value[0],
                "self_page": value[0],
            }

        elif value and len(value)==4:
            data = {
                "root": value[0],
                "grandpa": value[1],
                "parent": value[2],
                "self_page": value[3],
            }

        else:
            data = {
                "message": "unpredictable page tree",
            }

        return data


class ChildPageSerializer(Field):
    def to_representation(self, value):
        data_list = []
        if value:
            for i in value:
                data_list.append({'title': i.title,})
        return data_list