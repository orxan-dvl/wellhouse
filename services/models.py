from django.db import models
from django.utils.text import slugify

from ckeditor.fields import RichTextField

from wagtail.models import Page, Orderable, TranslatableMixin
from modelcluster.fields import ParentalKey
from wagtailcache.cache import WagtailCacheMixin
from wagtailmetadata.models import MetadataPageMixin
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.models import TranslatableMixin
from wagtail.core.fields import StreamField
from wagtailsvg.blocks import SvgChooserBlock

from wellhouse.settings.base import WAGTAIL_CONTENT_LANGUAGES as wcl
from core.serializers import (CustomImageSerializer, MultipleImageSerializer,
                              FullPathSerializer, ChildPageSerializer, SearchImageSerializer)

from core.models import AllImages
from seo.models import SEOPage
from aboutindex.blocks import AdvantagesTabBlock
from aboutindex.serializers import AdvantagesTabSerializer
from services.blocks import Service1SectionBlock
from services.serializers import (ChildServiceDataSerializer, Section1TabSerializer,
                                  FAQSerializer, ServiceDataSerializer)


#
class ServiceIndexPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):

    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['home.HomePage']
    subpage_types = ['services.OrientationTourServicePage', 'services.OnlineVisitPage',
                    'services.PostSaleServicePage', 'services.ConsultingPage',
                    'services.SellPropertyPage', 'services.ApartmentExchangePage',]

    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Background Image")
    
    subtitle = models.CharField(max_length=50, null=True, blank=False)

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + [
        FieldPanel('banner_image'),
        FieldPanel('subtitle'),
    ]

    api_fields = SEOPage.api_fields + [
        APIField('slug2'),
        APIField('full_path', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),  
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('subtitle'),
        APIField('orientation_tour_page_information', ChildServiceDataSerializer(source='get_service1')),
        APIField('online_visit_page_information', ChildServiceDataSerializer(source='get_service2')),
        APIField('post_sale_service_page_information', ChildServiceDataSerializer(source='get_service3')),
        APIField('consulting_page_information', ChildServiceDataSerializer(source='get_service4')),
        APIField('sell_property_page_information', ChildServiceDataSerializer(source='get_service5')),
        APIField('apartmentexchange_page_information', ChildServiceDataSerializer(source='get_service6')),
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

    def get_service1(self):
        return OrientationTourServicePage.objects.filter(locale__language_code=self.locale.language_code,
                                                        live=True)
    def get_service2(self):
        return OnlineVisitPage.objects.filter(locale__language_code=self.locale.language_code,
                                                live=True)
    def get_service3(self):
        return PostSaleServicePage.objects.filter(locale__language_code=self.locale.language_code,
                                                live=True)

    def get_service4(self):
        return ConsultingPage.objects.filter(locale__language_code=self.locale.language_code,
                                                live=True)

    def get_service5(self):
        return SellPropertyPage.objects.filter(locale__language_code=self.locale.language_code,
                                                live=True)

    def get_service6(self):
        return ApartmentExchangePage.objects.filter(locale__language_code=self.locale.language_code,
                                                live=True)

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


#-----------------------------------OrientationTourServicePage Section-------------------------

#
class CaruselImagesModel(Orderable ,models.Model):

    page = ParentalKey("services.OrientationTourServicePage", related_name="carusel_images", 
                       on_delete=models.CASCADE)

    image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                on_delete=models.SET_NULL, related_name="+",
                                verbose_name="Image")

#
class OrientationTourServicePage(WagtailCacheMixin, MetadataPageMixin, SEOPage):

    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['services.ServiceIndexPage']
    subpage_types = []
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    service_parent_icon = StreamField([('Service_parent_icon',SvgChooserBlock(), ),], 
                                        use_json_field=True, min_num=1, max_num=1)
    
    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Banner Image")

    subtitle = models.CharField(max_length=50, null=True, blank=False)
    first_content = models.TextField()

    section_tab = StreamField([('Sections',Service1SectionBlock(), ),], 
                              use_json_field=True, min_num=6, max_num=6)
    
    first_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="First Image")

    second_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Second Image")

    second_content = RichTextField()

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + [
        FieldPanel('service_parent_icon'),
        FieldPanel('banner_image'),
        FieldPanel('subtitle'),
        FieldPanel('first_content'),
        FieldPanel('section_tab'),
        FieldPanel('first_image'),
        FieldPanel('second_image'),
        FieldPanel('second_content'),

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
        APIField('first_content'),
        APIField('section_tab', Section1TabSerializer(source='get_section_tab')),
        APIField('first_image', CustomImageSerializer(source='get_first_image')),
        APIField('second_image',  CustomImageSerializer(source='get_second_image')),
        APIField('second_content'),
        APIField('carusel_images', MultipleImageSerializer(source='get_carusel_images')),
        APIField("search_image", SearchImageSerializer(source='get_search_image')),
        APIField("seo_title"),
        APIField("search_description"),
    ]

    def get_service_parent_icon(self):
        return self.service_parent_icon
    
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
    
    def get_first_image(self):
        return self.first_image if self.first_image else None
    
    def get_second_image(self):
        return self.second_image if self.second_image else None
    
    def get_section_tab(self):
        return self.section_tab if self.section_tab else None

    def get_search_image(self):
        return self.search_image

    def get_carusel_images(self):    
        result = None
        special_carusel_obj = self.carusel_images.select_related('image')
        general_carusel_obj = AllImages.objects.first()
    
        if special_carusel_obj :
            result = [image.image for image in special_carusel_obj]
        else:
            if general_carusel_obj:
                result = general_carusel_obj.carusel_images.all()                
        return result    


    def get_full_path(self):
        dad = self.get_parent()
        grand_dad = dad.get_parent()
        return (grand_dad.title, dad.title, self.title)
    
    def get_child_pages(self):
        return self.get_children() if self.get_children() else None

    def save(self, *args, **kwargs):
        # Check if the page is being created for the first time
        if not self.pk:
            #if max_count=1 in current page, then we don't need another variable to slugify it
            self.slug2 = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()
        super().save(*args, **kwargs)    


#--------------------------------------OnlineVisitPage section-----------------------------

#
class CaruselImagesModel2(Orderable ,models.Model):

    page = ParentalKey("services.OnlineVisitPage", related_name="carusel_images2", 
                       on_delete=models.CASCADE)

    image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                on_delete=models.SET_NULL, related_name="+",
                                verbose_name="Image")


#
class OnlineVisitPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):

    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['services.ServiceIndexPage']
    subpage_types = []
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    service_parent_icon = StreamField([('Service_parent_icon',SvgChooserBlock(), ),], 
                                        use_json_field=True, min_num=1, max_num=1)
    
    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Banner Image")

    section1_subtitle = models.CharField(max_length=100, null=True, blank=False)
    section1_content = models.TextField()
    section1_video_link = models.TextField()

    section1_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Section1 Image")

    section2_subtitle = models.CharField(max_length=100, null=True, blank=False)
    section2_content = RichTextField()

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + [
        FieldPanel('service_parent_icon'),
        FieldPanel('banner_image'),
        FieldPanel('section1_subtitle'),
        FieldPanel('section1_content'),
        FieldPanel('section1_video_link'),
        FieldPanel('section1_image'),
        FieldPanel('section2_subtitle'),
        FieldPanel('section2_content'),
        MultiFieldPanel(
            [
                InlinePanel(
                    "carusel_images2",
                    label="Carusel Images",
                ), ], heading="Carusel Images",),
    ]

    api_fields = SEOPage.api_fields + [
        APIField('slug2'),
        APIField('full_path', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),      
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('section1_subtitle'),
        APIField('section1_content'),
        APIField('section1_video_link'),

        APIField('section1_image', CustomImageSerializer(source='get_section1_image')),
        APIField('section2_subtitle'),
        APIField('section2_content'),
        APIField('carusel_images2', MultipleImageSerializer(source='get_carusel_images2')),
        APIField("search_image", serializer=SearchImageSerializer(source='get_search_image')),
        APIField("seo_title"),
        APIField("search_description"),
    ]

    def get_service_parent_icon(self):
        return self.service_parent_icon if self.service_parent_icon else None
    
    
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

    def get_section1_image(self):
        return self.section1_image if self.section1_image else None


    def get_carusel_images2(self):    
        result = None
        special_carusel_obj = self.carusel_images2.select_related('image')
        general_carusel_obj = AllImages.objects.first()
    
        if special_carusel_obj :
            result = [image.image for image in special_carusel_obj]
        else:
            if general_carusel_obj:
                result = general_carusel_obj.carusel_images.all()                
        return result    
    

    def get_search_image(self):
        return self.search_image

    def get_full_path(self):
        dad = self.get_parent()
        grand_dad = dad.get_parent()
        return (grand_dad.title, dad.title, self.title)

    def get_child_pages(self):
        return self.get_children() if self.get_children() else None

    def save(self, *args, **kwargs):
        # Check if the page is being created for the first time
        if not self.pk:
            #if max_count=1 in current page, then we don't need another variable to slugify it
            self.slug2 = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()
        super().save(*args, **kwargs)    


#-----------------------------Post_Sale_Service section--------------------------------------------------

#
class CaruselImagesModel3(Orderable ,models.Model):

    page = ParentalKey("services.PostSaleServicePage", related_name="carusel_images3", 
                       on_delete=models.CASCADE)

    image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                on_delete=models.SET_NULL, related_name="+",
                                verbose_name="Image")

#
class Servicemodel(TranslatableMixin, Orderable, models.Model):
    class Meta:
        unique_together = ('translation_key', 'locale')

    page = ParentalKey(
                        "services.PostSaleServicePage", related_name="post_sale_service_relationship", 
                        on_delete=models.CASCADE
                        )

    name = models.CharField(max_length=50, null=True, blank=False)
    content = models.TextField()
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Banner Image")



    def __str__(self):
        return '{}'.format(self.name)

#
class PostSaleServicePage(WagtailCacheMixin, MetadataPageMixin, SEOPage):

    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['services.ServiceIndexPage']
    subpage_types = []
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    service_parent_icon = StreamField([('Service_parent_icon',SvgChooserBlock(), ),], 
                                        use_json_field=True, min_num=1, max_num=1)
    
    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Banner Image")

    section1_subtitle = models.CharField(max_length=100, null=True, blank=False)
    section1_content = RichTextField()
    section2_subtitle = models.CharField(max_length=100, null=True, blank=False)
    

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + [
        FieldPanel('service_parent_icon'),
        FieldPanel('banner_image'),
        FieldPanel('section1_subtitle'),
        FieldPanel('section1_content'),
        FieldPanel('section2_subtitle'),
        
        MultiFieldPanel(
            [
                InlinePanel(
                    "carusel_images3",
                    label="Carusel Images",
                ), ], heading="Carusel Images",),

        MultiFieldPanel(
            [
                InlinePanel(
                    "post_sale_service_relationship",
                    heading="Post Sale Service",
                    label="Post Sale Service",
                ),
            ]
        ),

    ]

    api_fields = SEOPage.api_fields + [
        APIField('slug2'),
        APIField('full_path', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),     
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('section1_subtitle'),
        APIField('section1_content'),
        APIField('section2_subtitle'),
        APIField('service_data', ServiceDataSerializer(source='get_post_sale_service_data') ),
        APIField('carusel_images3', MultipleImageSerializer(source='get_carusel_images3')),
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
    
    def get_post_sale_service_data(self):
        return self.post_sale_service_relationship.all()
    
    def get_carusel_images3(self):    
        result = None
        special_carusel_obj = self.carusel_images3.select_related('image')
        general_carusel_obj = AllImages.objects.first()    
        if special_carusel_obj :
            result = [image.image for image in special_carusel_obj]
        else:
            if general_carusel_obj:
                result = general_carusel_obj.carusel_images.all()                
        return result    


    def get_search_image(self):
        return self.search_image

    def get_full_path(self):
        dad = self.get_parent()
        grand_dad = dad.get_parent()
        return (grand_dad.title, dad.title, self.title)
    
    def get_child_pages(self):
        return self.get_children() if self.get_children() else None

    def save(self, *args, **kwargs):
        if not self.slug2:
            self.slug2 = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()

        super().save(*args, **kwargs)

#-----------------------------------Consulting Page section------------------------------------------

#
class FAQmodel(TranslatableMixin, Orderable, models.Model):
    class Meta:
        unique_together = ('translation_key', 'locale')

    page = ParentalKey(
        "services.ConsultingPage", related_name="faq_relationship", on_delete=models.CASCADE
    )

    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return '{}'.format(self.question)
    
#
class CaruselImagesModel4(Orderable ,models.Model):

    page = ParentalKey("services.ConsultingPage", related_name="carusel_images4", 
                       on_delete=models.CASCADE)

    image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                on_delete=models.SET_NULL, related_name="+",
                                verbose_name="Image")


#
class ConsultingPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):

    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['services.ServiceIndexPage']
    subpage_types = []
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    service_parent_icon = StreamField([('Service_parent_icon',SvgChooserBlock(), ),], 
                                        use_json_field=True, min_num=1, max_num=1)
    
    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Banner Image")

    section1_subtitle = models.CharField(max_length=50, null=True, blank=False)
    section1_content = RichTextField()
    section1_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Section1 Image")

    promote_panels = SEOPage.promote_panels

    content_panels = Page.content_panels + [
        FieldPanel("banner_image"),
        FieldPanel('service_parent_icon'),
        FieldPanel("section1_subtitle"),
        FieldPanel("section1_content"),
        FieldPanel("section1_image"),

        MultiFieldPanel(
            [
                InlinePanel(
                    "faq_relationship",
                    heading="FAQ",
                    label="FAQ",
                ),
            ]
        ),
    
        MultiFieldPanel(
            [
                InlinePanel(
                    "carusel_images4",
                    label="Carusel Images",
                ), ], heading="Carusel Images",),
    ]

    api_fields = SEOPage.api_fields + [
        APIField('slug2'),
        APIField('full_path', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),    
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('section1_subtitle'),
        APIField('section1_content'),
        APIField('section1_image', CustomImageSerializer(source='get_section1_image')),
        APIField("faq_data", FAQSerializer(source='get_faq_data')),
        APIField('carusel_images4', MultipleImageSerializer(source='get_carusel_images4')),
        APIField("search_image", serializer=SearchImageSerializer(source='get_search_image')),
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
    
    def get_section1_image(self):
        return self.section1_image if self.section1_image else None

    def get_faq_data(self):
        return self.faq_relationship.all()

    def get_carusel_images4(self):    
        result = None
        special_carusel_obj = self.carusel_images4.select_related('image')
        general_carusel_obj = AllImages.objects.first()
        if special_carusel_obj :
            result = [image.image for image in special_carusel_obj]
        else:
            if general_carusel_obj:
                result = general_carusel_obj.carusel_images.all()                
        return result    


    def get_search_image(self):
        return self.search_image

    def get_full_path(self):
        dad = self.get_parent()
        grand_dad = dad.get_parent()
        return (grand_dad.title, dad.title, self.title)

    def get_child_pages(self):
        return self.get_children() if self.get_children() else None

    def save(self, *args, **kwargs):
        # Check if the page is being created for the first time
        if not self.pk:
            #if max_count=1 in current page, then we don't need another variable to slugify it
            self.slug2 = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()
        super().save(*args, **kwargs)    


#--------------------------------SellPropertyPage Section--------------------------------------------

#
class CaruselImagesModel5(Orderable ,models.Model):

    page = ParentalKey("services.SellPropertyPage", related_name="carusel_images5", 
                       on_delete=models.CASCADE)

    image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                on_delete=models.SET_NULL, related_name="+",
                                verbose_name="Image")

#
class SellPropertyPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):

    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['services.ServiceIndexPage']
    subpage_types = []
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    service_parent_icon = StreamField([('Service_parent_icon',SvgChooserBlock(), ),], 
                                        use_json_field=True, min_num=1, max_num=1)
    
    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Banner Image")

    section1_subtitle = models.CharField(max_length=50, null=True, blank=False)
    section1_content = RichTextField()
    section1_first_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Section1 First Image")
    section1_second_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Section1 Second Image")
    section2_content = RichTextField()
    section2_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Section2 Image")

    promote_panels = SEOPage.promote_panels

    content_panels = Page.content_panels + [
        FieldPanel("banner_image"),
        FieldPanel('service_parent_icon'),
        FieldPanel("section1_subtitle"),
        FieldPanel("section1_content"),
        FieldPanel("section1_first_image"),
        FieldPanel("section1_second_image"),
        FieldPanel("section2_content"),
        FieldPanel("section2_image"),

    
        MultiFieldPanel(
            [
                InlinePanel(
                    "carusel_images5",
                    label="Carusel Images",
                ), ], heading="Carusel Images",),
    ]

    api_fields = SEOPage.api_fields + [
        APIField('slug2'),
        APIField('full_path', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),     
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('section1_subtitle'),
        APIField('section1_content'),
        APIField('section1_first_image', CustomImageSerializer(source='get_section1_first_image')),
        APIField('section1_section_image', CustomImageSerializer(source='get_section1_second_image')),
        APIField('section2_content'),
        APIField('section2_image', CustomImageSerializer(source='get_section2_image')),
        APIField('carusel_images5', MultipleImageSerializer(source='get_carusel_images5')),
        APIField("search_image", serializer=SearchImageSerializer(source='get_search_image')),
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

    def get_section1_first_image(self):
        return self.section1_first_image if self.section1_first_image else None
    
    def get_section1_second_image(self):
        return self.section1_second_image if self.section1_second_image else None

    def get_section2_image(self):
        return self.section2_image if self.section2_image else None

    def get_carusel_images5(self):    
        result = None
        special_carusel_obj = self.carusel_images5.select_related('image')
        general_carusel_obj = AllImages.objects.first()
        if special_carusel_obj :
            result = [image.image for image in special_carusel_obj]
        else:
            if general_carusel_obj:
                result = general_carusel_obj.carusel_images.all()                
        return result    


    def get_search_image(self):
        return self.search_image

    def get_full_path(self):
        dad = self.get_parent()
        grand_dad = dad.get_parent()
        return (grand_dad.title, dad.title, self.title)

    def get_child_pages(self):
        return self.get_children() if self.get_children() else None

    def save(self, *args, **kwargs):
        # Check if the page is being created for the first time
        if not self.pk:
            #if max_count=1 in current page, then we don't need another variable to slugify it
            self.slug2 = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()
        super().save(*args, **kwargs)    


#-----------------------------------ApartmentExchangePage Section-------------------------------------

class CaruselImagesModel6(Orderable ,models.Model):

    page = ParentalKey("services.ApartmentExchangePage", related_name="carusel_images6", 
                       on_delete=models.CASCADE)

    image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                on_delete=models.SET_NULL, related_name="+",
                                verbose_name="Image")

#
class ApartmentExchangePage(WagtailCacheMixin, MetadataPageMixin, SEOPage):

    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['services.ServiceIndexPage']
    subpage_types = []
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    service_parent_icon = StreamField([('Service_parent_icon',SvgChooserBlock(), ),], 
                                        use_json_field=True, min_num=1, max_num=1)
    
    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Banner Image")

    subtitle = models.CharField(max_length=50, null=True, blank=False)

    section1_subtitle = models.CharField(max_length=50, null=True, blank=False)
    #section1_content = models.TextField()
    section1_content = StreamField(
                                        [
                                        ("Advantages", AdvantagesTabBlock(), ),
                                         ], use_json_field=True, min_num=1, max_num=1)

    section1_first_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Section1 First Image")

    section1_second_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Section1 Second Image")

    section2_content1 = RichTextField()
    section2_content2 = RichTextField()
    section2_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Section2 Image")

    promote_panels = SEOPage.promote_panels

    content_panels = Page.content_panels + [
        FieldPanel("banner_image"),
        FieldPanel('service_parent_icon'),
        FieldPanel("subtitle"),
        FieldPanel("section1_subtitle"),
        FieldPanel("section1_content"),
        FieldPanel("section1_first_image"),
        FieldPanel("section1_second_image"),
        FieldPanel("section2_content1"),
        FieldPanel("section2_content2"),
        FieldPanel("section2_image"),

        MultiFieldPanel(
            [
                InlinePanel(
                    "carusel_images6",
                    label="Carusel Images",
                ), ], heading="Carusel Images",),
    ]

    api_fields = SEOPage.api_fields + [
        APIField('slug2'),
        APIField('full_path', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),      
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('subtitle'),
        APIField('section1_subtitle'),
        APIField('section1_content', AdvantagesTabSerializer(source='get_section1_content')),
        APIField('section1_first_image', CustomImageSerializer(source='get_section1_first_image')),
        APIField('section1_second_image', CustomImageSerializer(source='get_section1_second_image')),
        APIField('section2_content1'),
        APIField('section2_content2'),
        APIField('section2_image', CustomImageSerializer(source='get_section2_image')),
        APIField('carusel_images6', MultipleImageSerializer(source='get_carusel_images6')),
        APIField("search_image", SearchImageSerializer(source='get_search_image')),
        APIField("seo_title"),
        APIField("search_description"),
    ]

    def get_section1_content(self):
        return self.section1_content if self.section1_content else None
    
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

    def get_section1_first_image(self):
        return self.section1_first_image if self.section1_first_image else None
    
    def get_section1_second_image(self):
        return self.section1_second_image if self.section1_second_image else None

    def get_section2_image(self):
        return self.section2_image if self.section2_image else None

    def get_carusel_images6(self):    
        result = None
        special_carusel_obj = self.carusel_images6.select_related('image')
        general_carusel_obj = AllImages.objects.first()
        if special_carusel_obj :
            result = [image.image for image in special_carusel_obj]
        else:
            if general_carusel_obj:
                result = general_carusel_obj.carusel_images.all()                
        return result  
    

    def get_search_image(self):
        return self.search_image

    def get_full_path(self):
        dad = self.get_parent()
        grand_dad = dad.get_parent()
        return (grand_dad.title, dad.title, self.title)

    def get_child_pages(self):
        return self.get_children() if self.get_children() else None

    def save(self, *args, **kwargs):
        # Check if the page is being created for the first time
        if not self.pk:
            #if max_count=1 in current page, then we don't need another variable to slugify it
            self.slug2 = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()
        super().save(*args, **kwargs)    
