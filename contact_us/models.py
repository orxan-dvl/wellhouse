from django.db import models

from wagtailmetadata.models import MetadataPageMixin
from wagtailcache.cache import WagtailCacheMixin
from wagtail.admin.panels import FieldPanel
from wagtail.core.fields import StreamField
from wagtail.api import APIField

from wellhouse.settings.base import WAGTAIL_CONTENT_LANGUAGES as wcl
from seo.models import SEOPage
from core.models import AllImages
from core.serializers import (CustomImageSerializer, FullPathSerializer, ChildPageSerializer, 
                              SearchImageSerializer)
from contact_us.blocks import OfficeBlock
from contact_us.serializers import OfficesSerializer


class ContactUsIndexPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):

    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Background Image")
    
    banner_subtitle = models.CharField(max_length=50, null=True, blank=False)
    banner_content = models.TextField()
    
    offices = StreamField([('Offices', OfficeBlock(), ), ], 
                          use_json_field=True)

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + [

        FieldPanel('banner_image'),
        FieldPanel('banner_subtitle'),
        FieldPanel('banner_content'),
        FieldPanel('offices'),
    ]

    api_fields = SEOPage.api_fields +[
        APIField('slug2'),
        APIField('full_path', FullPathSerializer(source='get_full_path')), 
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),     
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('banner_subtitle'),
        APIField('offices', OfficesSerializer(source='get_offices')),
        APIField("search_image", SearchImageSerializer(source='get_search_image')),
        APIField("seo_title"),
        APIField("search_description"),
    ]

    def get_banner_image(self):
        result = None
        general_banner_obj = AllImages.objects.first()
        special_banner_image = self.banner_image
        if self.banner_image:
            result = special_banner_image
        else:
            if general_banner_obj:
                result = general_banner_obj.banner_image
        return result
   
    def get_offices(self):
        return self.offices if self.offices else None

    def get_search_image(self):
        return self.search_image
    
    def get_full_path(self):
        return (self.get_parent().title, self.title)
    
    def get_child_pages(self):
        return self.get_children() if self.get_children() else None

    def save(self, *args, **kwargs):
        # Check if the page is being created for the first time
        if not self.pk:
            #if max_count=1 in current page, then we don't need another variable to slugify it
            self.slug2 = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()
        super().save(*args, **kwargs)    



