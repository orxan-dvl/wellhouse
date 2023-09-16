from django.db import models

from wagtail.models import Page, Orderable, TranslatableMixin, Site
from modelcluster.fields import ParentalKey
from wagtail.fields import RichTextField
from wagtail.admin.panels import (FieldPanel, InlinePanel, MultiFieldPanel )
from modelcluster.fields import ParentalKey
from wagtailcache.cache import WagtailCacheMixin
from wagtailmetadata.models import MetadataPageMixin
from wagtail.api import APIField

from wellhouse.settings.base import WAGTAIL_CONTENT_LANGUAGES as wcl
from feedback.choices import GENDER_CHOICES
from seo.models import SEOPage

from feedback.forms import Feedback
from core.models import AllImages
from core.serializers import (MultipleImageSerializer, CustomImageSerializer, 
                              FullPathSerializer, ChildPageSerializer, SearchImageSerializer)

from feedback.serializers import FeedbackIndexSerializer



#
class CaruselImagesModel(Orderable ,models.Model):

    page = ParentalKey("feedback.FeedbackIndexPage", related_name="carusel_images", 
                       on_delete=models.CASCADE)

    image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                on_delete=models.SET_NULL, related_name="+",
                                verbose_name="Image")


class FeedbackIndexPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):

    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Background Image")
    
    content = models.TextField()
    
    subtitle = models.CharField(max_length=250, null=True, blank=False)
    section2_title = models.CharField(max_length=250, null=True, blank=False)
    section2_content = RichTextField()

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + [
        FieldPanel('banner_image'),
        FieldPanel('subtitle'),
        FieldPanel('content'),
        FieldPanel('section2_title'),
        FieldPanel('section2_content'),

        MultiFieldPanel(
            [
                InlinePanel(
                    "carusel_images",
                    label="Carusel Images",
                ), ], heading="Carusel Images",),

    ]

    api_fields = SEOPage.api_fields + [
        APIField('slug2'),
        APIField('full_path', FullPathSerializer(source='get_full_path')), 
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),     
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('subtitle'),
        APIField('content'),
        APIField('section2_title'),
        APIField('section2_content'),
        APIField('carusel_images', MultipleImageSerializer(source='get_carusel_images')),
        APIField('feedback_list', FeedbackIndexSerializer(source='get_published_feedbacks')),
        APIField("seo_title"),
        APIField("search_description"),
        APIField("search_image", SearchImageSerializer(source='get_search_image')),
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

    def get_search_image(self):
        return self.search_image

    def get_carusel_images(self):
        result = None
        general_carusel = (AllImages.objects.first()).carusel_images.all()
        special_carusel_obj =  self.carusel_images.all().select_related('image')
        special_carusel = [image.image for image in special_carusel_obj]
        if len(special_carusel) > 0:
            result = special_carusel
        else:
            if len(general_carusel) > 0:
                result = general_carusel
        return result
    
    def get_published_feedbacks(self):
        return Feedback.objects.filter(is_published=True)

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

