from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer


from wagtail.models import Locale, Page
from wagtail.models import Site
from wagtail.images import get_image_model
from wagtail.images.shortcuts import get_rendition_or_not_found

from core.models import SiteSetting, SocialMediaSetting
from core.serializers import SiteSettingSerializer, SocialMediaSettingSerializer
from core.modelserializers import MenuItemSerializer, WebSiteMapSerializer
from core.utils import get_slug2


#
class MenuItemListView(ListAPIView):
    model = Page
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        try:
            locale_id = Locale.objects.filter(language_code=self.request.GET.get("locale")).last()
            return self.model.objects.filter(show_in_menus=True,
                                             locale_id=locale_id.id, live=True)
        except Exception:
            return Response({"error_message": "Please added locale type"})



#
@api_view(['GET'])
def websitemap(request):
    lang_param = request.GET.get('locale')

    pages = Page.objects.live().public().filter(locale__language_code=lang_param)
    result = []

    for page in pages:
        slug2 = get_slug2(page)
        main_pages = ('aboutindexpage', 'homepage', 'propertyinturkeyindexpage', 'usefullindexpage',
                      'serviceindexpage', 'feedbackindexpage', 'contactusindexpage')
        if slug2 in main_pages:
            serialized_page = WebSiteMapSerializer(page).data  # Serialize the Page object
            result.append(serialized_page)

    return Response(result)


#It returns svg url for our site, (Icons)

def get_svg_url(file):
    site = Site.objects.filter(is_default_site=True).last()
    return f'http://{site.hostname}{file.url}'


#
def image_regenerator(request, image_id):
    # try:
    image_model = get_image_model()
    image = image_model.objects.filter(id=image_id).last()
    image_format = request.GET.get("image_format")
    image_width = request.GET.get("image_width")
    image_height = request.GET.get("image_height")
    url = ''
    if image_width and image_height:
        url = image.get_rendition(f'fill-{image_width}x{image_height}|format-{image_format}').url

    elif image_width:
        url = image.get_rendition(f'width-{image_width}|format-{image_format}').url

    elif image_height:
        url = image.get_rendition(f'height-{image_height}|format-{image_format}').url

    return JsonResponse({"image": f'https://{Site.objects.filter(is_default_site=True).last().hostname}{url}'})

#--------------------------------------------------------------------------

#
class BaseSettingsView(ListAPIView):
    queryset = SiteSetting.objects.filter(site__is_default_site=True)
    serializer_class = SiteSettingSerializer

#
class SocialLinksView(ListAPIView):
    queryset = SocialMediaSetting.objects.filter(site__is_default_site=True)
    serializer_class = SocialMediaSettingSerializer

