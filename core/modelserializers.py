from rest_framework.serializers import ModelSerializer, SerializerMethodField

from wagtail.models import Page


#
class MenuItemSerializer(ModelSerializer):
    slug2 = SerializerMethodField()

    class Meta:
        model = Page
        fields = ['id', 'title', 'slug', 'live', 'url_path', 'content_type', 'locale', 'slug2']

    def get_slug2(self, instance):
        return (str(instance.content_type)).split("|")[1].strip().replace(" ", "").lower()



class WebSiteMapSerializer(ModelSerializer):
    slug2 = SerializerMethodField()
    children = SerializerMethodField()

    class Meta:
        model = Page
        fields = ['id', 'title', 'slug', 'locale', 'url_path', 'content_type', 'slug2', 'children']

    def get_slug2(self, instance):
        return (str(instance.content_type)).split("|")[1].strip().replace(" ", "").lower()

    def get_children(self, instance):
        children = instance.get_children()
        return WebSiteMapSerializer(children, many=True).data  # Serialize descendants using PageSerializer
