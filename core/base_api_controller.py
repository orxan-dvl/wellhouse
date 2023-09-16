from django.urls import re_path, path
from django.http import JsonResponse

from rest_framework.fields import Field
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView


from wagtail.models import Locale, Page
from wagtail.models import Site
from wagtail.images import get_image_model
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.serializers import PageSerializer


from home.models import HomePage, PrivacyPolicyIndexPage
from aboutindex.models import AboutIndexPage
from contact_us.models import ContactUsIndexPage
from feedback.models import FeedbackIndexPage
from services.models import (ServiceIndexPage, OrientationTourServicePage, OnlineVisitPage, 
                             PostSaleServicePage, ConsultingPage, SellPropertyPage, 
                             ApartmentExchangePage)

from usefull.models import (BlogIndexPage, BlogPage, NewsIndexPage, NewsPage, 
                            RealEstateRegistrationPage, UsefullIndexPage)

from advertisement.models import (PropertyInTurkeyIndexPage, PropertyIndexPage, PropertyDetailPage, 
                                  ByPropertyIndexPage, RentPropertyIndexPage)




#Serializer for all Pages
class CustomPageSerializer(PageSerializer):

    def get_fields(self):
        fields = super().get_fields()
        fields['detail_url'] = serializers.SerializerMethodField()
        return fields
    
    def get_detail_url(self, obj):
        url = self._get_page_url(obj)
        return url

    def _get_page_url(self, obj):
        for model in self.get_page_models():
            if isinstance(obj.specific, model):
                url = self._construct_page_url(obj.specific)
                return url

        return None

    def get_page_models(self):

        return (HomePage, AboutIndexPage, PrivacyPolicyIndexPage, ServiceIndexPage, 
                OrientationTourServicePage, OnlineVisitPage, PostSaleServicePage, 
                ConsultingPage, SellPropertyPage, ApartmentExchangePage, BlogIndexPage,
                BlogPage, NewsIndexPage, NewsPage, RealEstateRegistrationPage, ContactUsIndexPage,
                FeedbackIndexPage, PropertyInTurkeyIndexPage, PropertyIndexPage, PropertyDetailPage, 
                ByPropertyIndexPage, RentPropertyIndexPage, UsefullIndexPage)


    def _construct_page_url(self, obj):
        url = self.context['request'].build_absolute_uri\
            (obj.slug2 + '/?locale=' + obj.locale.language_code)
        return url


#-------------------------------------------------------------------------------------------------------

#
class CustomPageViewSet(PagesAPIViewSet):
    lookup_field = 'slug2'

    model = (HomePage, AboutIndexPage, PrivacyPolicyIndexPage, ServiceIndexPage, 
            OrientationTourServicePage, OnlineVisitPage, PostSaleServicePage, 
            ConsultingPage, SellPropertyPage, ApartmentExchangePage, BlogIndexPage,
            BlogPage, NewsIndexPage, NewsPage, RealEstateRegistrationPage, ContactUsIndexPage,
            FeedbackIndexPage, PropertyInTurkeyIndexPage, PropertyIndexPage, PropertyDetailPage, 
            ByPropertyIndexPage, RentPropertyIndexPage, UsefullIndexPage)

    base_serializer_class = CustomPageSerializer

    body_fields = [
        "title",
        "id",
        "slug",
        "slug2",
        "content_type_id",
        "locale",
    ]

    def get_object(self):
        locale_code = self.request.GET.get("locale")
        locale = Locale.objects.filter(language_code=locale_code).last()

        if not locale:
            raise NotFound(detail=f"No Locale found for language code '{locale_code}'")

        slug2 = self.kwargs[self.lookup_field]

        try:
            obj = None
            for model in self.model:
                try:
                    obj = model.objects.get(slug2=slug2, locale_id=locale.id,live=True)
                    break
                except model.DoesNotExist:
                    pass
            if not obj:
                raise NotFound(detail=f"No page found with slug2 '{slug2}' and locale '{locale_code}'")
        except Page.DoesNotExist:
            raise NotFound(detail=f"No page found with slug2 '{slug2}' and locale '{locale_code}'")

        return obj.specific



    def detail_view(self, request, slug2):
        instance = self.get_object()
        if isinstance(instance, (BlogPage, NewsPage)):
            instance.increment_view_count()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)



    @classmethod
    def get_urlpatterns(cls):
        return [
            path("", cls.as_view({"get": "listing_view"}), name="listing"),
            re_path(r"^(?P<slug2>[-\w]+)/$", cls.as_view({"get": "detail_view"}), name="detail"),
            path("find/", cls.as_view({"get": "find_view"}), name="find"),
        ]
