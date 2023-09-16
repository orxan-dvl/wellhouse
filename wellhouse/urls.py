from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from .api import api_router
from django.conf.urls.i18n import i18n_patterns
from seo.views import sitemap
from core.views import websitemap
import core.views

from employee.views import (LanguagesListView, LanguageDetailView, ProfessionListView, 
                            ProfessionDetailView, EmployeeListView, EmployeeDetailView)


from advertisement.views import (TypeListView, 
                                 TypeDetailView, CategoryListView, CategoryDetailView,  
                                 CityListView, CityDetailView, RegionListView, RegionDetailView, 
                                 PropertyRequestTypesView, PropertyDetailFormView,
                                 PropertyDetailOnlineVisitFormView, RoomListView, RoomDetailView,
                                 TagsDetailView, TagsListView)

from feedback.views import FeedbackView, GenderChoiceListView
from usefull.views import SubscribeAPIView
from services.views import (PostSaleServiceFormView, OrientationFormView, ConsultingFormView,
                            OnlineVisitFormView, ServicemodelView, SellPropertyFormView, 
                            ApartmentExchangeFormView, FinishingChoiceListView)

from home.views import HelpForPropertyView, AskCallFormView, AskQuestionFormView
from currency.views import  currency_data_view
from robots.views import rules_list


schema_view = get_schema_view(
    openapi.Info(
        title="Wellhouse API",
        default_version="v1",
        description="All API endpoints",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="report@traktordetal.az"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("api/v2/search/", search_views.search, name="search"),
    path("__reload__/*", include("django_browser_reload.urls")),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
    re_path(r'^api-doc/$', schema_view.with_ui('swagger', cache_timeout=0),
                name='schema-swagger-ui'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + i18n_patterns(
    path("search/", search_views.search, name="search"),
    path('api/v2/', api_router.urls),
    path('api/v2/sitemap/', sitemap),
    path('api/v2/robots/', rules_list, name='robots_rule_list'),

    path('api/v2/websitemap/', websitemap),
    path("api/v2/menu/", core.views.MenuItemListView.as_view()),
    path('api/v2/image-customize/<int:image_id>/', core.views.image_regenerator),
    path('api/v2/settings/', core.views.BaseSettingsView.as_view()),
    path('api/v2/social-links/', core.views.SocialLinksView.as_view()),
#    path('api/v2/contact/', ContactEmailView.as_view(), name='contact_email'),
#    path('api/v2/models/category_filter_by_locale/', category_filter_by_locale),
#    path('api/v2/models/type_filter_by_locale/', type_filter_by_locale),
#    path('api/v2/models/city_filter_by_locale/', city_filter_by_locale),
#    path('api/v2/models/region_filter_by_city/<slug:city_slug2>/', region_filter_by_city),


    path('api/v2/models/type_list/', TypeListView.as_view(), name='type_list'),
    path('api/v2/models/type/<slug:slug2>/', TypeDetailView.as_view(), name='type_detail'),

    path('api/v2/models/category_list/', CategoryListView.as_view(), name='category_list'),
    path('api/v2/models/category/<slug:slug2>/', CategoryDetailView.as_view(), name='category_detail'),

    path('api/v2/models/city_list/', CityListView.as_view(), name='city_list'),
    path('api/v2/models/city/<slug:slug2>/', CityDetailView.as_view(), name='city_detail'),

    path('api/v2/models/region_list/', RegionListView.as_view(), name='region_list'),
    path('api/v2/models/region/<slug:slug2>/', RegionDetailView.as_view(), name='region_detail'),

    path('api/v2/models/room_list/', RoomListView.as_view(), name='room-list'),
    path('api/v2/models/room/<slug:slug2>/', 
         RoomDetailView.as_view(), name='room-detail'),

    path('api/v2/models/tag_list/', TagsListView.as_view(), name='tag-list'),
    path('api/v2/models/tag/<slug:slug2>/', 
         TagsDetailView.as_view(), name='tag-detail'),


    path('api/v2/models/language_list/', LanguagesListView.as_view(), name='language_list'),
    path('api/v2/models/language/<slug:slug2>/', LanguageDetailView.as_view(), name='language_detail'),

    path('api/v2/models/profession_list/', ProfessionListView.as_view(), name='profession_list'),
    path('api/v2/models/profession/<slug:slug2>/', ProfessionDetailView.as_view(), name='profession_detail'),

    path('api/v2/models/employee_list/', EmployeeListView.as_view(), name='employee_list'),
    path('api/v2/models/employee/<slug:slug2>/', EmployeeDetailView.as_view(), name='employee_detail'),

    path('api/v2/form/feedback/', FeedbackView.as_view(), name='feedback_form'),
    path('api/v2/choices/gender_choices', GenderChoiceListView.as_view(), name='gender_choices_list'),

    path('api/v2/form/post_sale_service_form/', PostSaleServiceFormView.as_view(), name='post_sale_service_form'),
    path('api/v2/models/service_models/', ServicemodelView.as_view(), name='service_model_view'),
    path('api/v2/form/orientation/', OrientationFormView.as_view(), name='orientation_form'),
    path('api/v2/form/consulting/', ConsultingFormView.as_view(), name='consulting_form'),
    path('api/v2/form/online_visit/', OnlineVisitFormView.as_view(), name='online_visit_form'),
    path('api/v2/form/sell_property/', SellPropertyFormView.as_view(), name='sell_property_form'),
    path('api/v2/form/apartment_exchange/', ApartmentExchangeFormView.as_view(), 
                                            name='apartment_exchange_form'),
    
    path('api/v2/choices/finishing_choices', FinishingChoiceListView.as_view(), name='finishing_choices_list'),

    path('api/v2/form/consulting/', ConsultingFormView.as_view(), name='consulting_form'),
    path('api/v2/models/property_request_types/', PropertyRequestTypesView.as_view(), 
                                                    name='property_request_types_view'),

    path('api/v2/forms/property_detail/', PropertyDetailFormView.as_view(), name='property_detail_form'),

    path('api/v2/form/help_for_property/', HelpForPropertyView.as_view(), name='help_for_property_form'),
    path('api/v2/form/ask_call/', AskCallFormView.as_view(), name='ask_a_call_form'),
    path('api/v2/form/ask_question/', AskQuestionFormView.as_view(), name='ask_a_question_form'),

    path('api/v2/form/property_online_visit/', PropertyDetailOnlineVisitFormView.as_view(), 
                                                name='property_online_visit_form'),

    path('api/v2/form/property_orientation_tour/', PropertyDetailOnlineVisitFormView.as_view(), 
                                                    name='property_orientation_tour_form'),

    path('api/v2/form/subscribe/', SubscribeAPIView.as_view(), name='subscribe_form_api'),

    path('api/v2/models/currency', currency_data_view, name='currency_data'),


    path("", include(wagtail_urls)),
    prefix_default_language=False
)
#urlpatterns += staticfiles_urlpatterns()
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)