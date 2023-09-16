from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.core.cache import cache

from wagtail.models import Page, Orderable, TranslatableMixin, Locale, Site
from modelcluster.fields import ParentalKey
from wagtailcache.cache import WagtailCacheMixin
from wagtailmetadata.models import MetadataPageMixin
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.api import APIField
from ckeditor.fields import RichTextField
from wagtail.core.fields import StreamField

from wellhouse.settings.base import WAGTAIL_CONTENT_LANGUAGES as wcl
from core.models import AllImages
from core.serializers import (CustomImageSerializer, MultipleImageSerializer, 
                              FullPathSerializer, ChildPageSerializer, SearchImageSerializer)
from usefull.serializers import BlogsSerializer, NewsSerializer
from wagtail.core.fields import StreamField
from usefull.blocks import EstateRegisterSectionBlock
from usefull.serializers import RealEstateSectionTabSerializer

from seo.models import SEOPage

#----------------------------------BlogIndexPage Section---------------------------------------------

#
class UsefullIndexPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):
    
    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['home.HomePage']
    subpage_types = ['usefull.BlogIndexPage', 'usefull.NewsIndexPage',
                     'usefull.RealEstateRegistrationPage']
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + []

    api_fields = SEOPage.api_fields + [
        APIField('slug2'),
        APIField('full_path', FullPathSerializer(source='get_full_path')), 
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),   
        APIField("search_image", serializer=SearchImageSerializer(source='get_search_image')),
        APIField("seo_title"),
        APIField("search_description"),
    ]

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


#
class BlogIndexPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):
    
    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['usefull.UsefullIndexPage']
    subpage_types = ['usefull.BlogPage']
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Banner Image")
  
    subtitle = models.CharField(max_length=50, null=True, blank=False)
    content = models.TextField()

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + [
        FieldPanel('banner_image'),
        FieldPanel('subtitle'),
        FieldPanel('content'),
    ]

    api_fields = SEOPage.api_fields + [
        APIField('slug2'),
        APIField('full_path', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),      
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('subtitle'),
        APIField('content'),
        APIField('blogs', BlogsSerializer(source='get_blogs')),
#        APIField('all_blogs', BlogsSerializer(source='get_all_blogs')),
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
    
    def get_blogs(self):
        return BlogPage.objects.filter(locale__language_code=self.locale.language_code,
                                           live=True)
    

    def get_search_image(self):
        return self.search_image
    
    def get_full_path(self):
        parent = self.get_parent()
        grandpa = parent.get_parent()
        return (grandpa.title, parent.title, self.title)
    
    def get_child_pages(self):
        return self.get_children() if self.get_children() else None

    def save(self, *args, **kwargs):
        # Check if the page is being created for the first time
        if not self.pk:
            #if max_count=1 in current page, then we don't need another variable to slugify it
            self.slug2 = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()
        super().save(*args, **kwargs)



#------------------------------BlogPage Section---------------------------------------------

class BlogPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):
    
    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['usefull.BlogIndexPage']
    subpage_types = []

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Banner Image")
        
    subtitle = models.CharField(max_length=250, null=True, blank=False)
    content = RichTextField()
    blog_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Blog Image")

    existence_in_homepage = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveBigIntegerField(default=0)

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + [
        FieldPanel('banner_image'),
        FieldPanel('subtitle'),
        FieldPanel('content'),
        FieldPanel('blog_image'),
        FieldPanel('existence_in_homepage'),
    ]

    api_fields = SEOPage.api_fields + [
        APIField('slug2'),
        APIField('full_path', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),   
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('subtitle'),
        APIField('content'),
        APIField('blog_image', CustomImageSerializer(source='get_blog_image')),
        APIField('existence_in_homepage'),
        APIField('created_at'),
        APIField('updated_at'),
        APIField('view_count'),
        APIField("search_image", serializer=SearchImageSerializer(source='get_search_image')),
        APIField("seo_title"),
        APIField("search_description"),
    ]

    def increment_view_count(self):
        # Increment the view count
        self.view_count += 1
        self.save()

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

    def get_blog_image(self):
        return self.blog_image if self.blog_image else None

    def get_search_image(self):
        return self.search_image
    
    def get_full_path(self):
        dad = self.get_parent()
        grand_dad = dad.get_parent()
        root = grand_dad.get_parent()
        return (root.title, grand_dad.title, dad.title, self.title)
    
    def get_child_pages(self):
        return self.get_children() if self.get_children() else None

    def save(self, *args, **kwargs):
        if not self.slug2:
            #my data is classname of the page, which was generated from django_model content_type
            my_data = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()
            base_slug = slugify(my_data)  
            existing_slugs = BlogPage.objects.filter\
                                            (locale=self.locale).values_list('slug2', flat=True)
            
            count = 1
            new_slug = base_slug

            while new_slug in existing_slugs:
                count += 1
                new_slug = f"{base_slug}-{count}"
            self.slug2 = new_slug

        super().save(*args, **kwargs)


#------------------------------------------NewsIndexPage Section-------------------------------------

#
class NewsIndexPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):
    
    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['usefull.UsefullIndexPage']
    subpage_types = ['usefull.NewsPage']
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Banner Image")
    
    subtitle = models.CharField(max_length=50, null=True, blank=False)
    content = models.TextField()

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + [
        FieldPanel('banner_image'),
        FieldPanel('subtitle'),
        FieldPanel('content'),
    ]

    api_fields = SEOPage.api_fields + [
        APIField('slug2'),
        APIField('full_path', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),   
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('subtitle'),
        APIField('content'),
        APIField('news', NewsSerializer(source='get_news')),

        APIField("seo_title"),
        APIField("search_description"),
        APIField('search_image', SearchImageSerializer(source='get_search_image'))
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
    
    def get_news(self):
        return NewsPage.objects.filter(locale__language_code=self.locale.language_code,
                                           live=True)

    def get_full_path(self):
        parent = self.get_parent()
        grandpa = parent.get_parent()
        return (grandpa.title, parent.title, self.title)
    
    def get_child_pages(self):
        return self.get_children() if self.get_children() else None
    
    def get_search_image(self):
        return self.search_image

    def save(self, *args, **kwargs):
        # Check if the page is being created for the first time
        if not self.pk:
            #if max_count=1 in current page, then we don't need another variable to slugify it
            self.slug2 = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()
        super().save(*args, **kwargs)


#----------------------------------NewsPage Section--------------------------------------

#
class NewsPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):
    
    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['usefull.NewsIndexPage']
    subpage_types = []

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Banner Image")
        
    subtitle = models.CharField(max_length=250, null=True, blank=False)
    content = RichTextField()
    news_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="News Image")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveBigIntegerField(default=0)

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + [
        FieldPanel('banner_image'),
        FieldPanel('subtitle'),
        FieldPanel('content'),
        FieldPanel('news_image'),
    ]

    api_fields = SEOPage.api_fields + [
        APIField('slug2'),
        APIField('full_path', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),    
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('subtitle'),
        APIField('content'),
        APIField('news_image', CustomImageSerializer(source='get_news_image')),
        APIField('created_at'),
        APIField('updated_at'),
        APIField('view_count'),
        APIField("search_image", serializer=SearchImageSerializer(source='get_search_image')),
        APIField("seo_title"),
        APIField("search_description"),
    ]

    def increment_view_count(self):
        # Increment the view count
        self.view_count += 1
        self.save()

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

    def get_news_image(self):
        return self.news_image if self.news_image else None

    def get_search_image(self):
        return self.search_image

    def get_full_path(self):
        dad = self.get_parent()
        grand_dad = dad.get_parent()
        root = grand_dad.get_parent()
        return (root.title, grand_dad.title, dad.title, self.title)
    
    def get_child_pages(self):
        return self.get_children() if self.get_children() else None

    def save(self, *args, **kwargs):
        if not self.slug2:
            #my data is classname of the page, which was generated from django_model content_type
            my_data = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()
            base_slug = slugify(my_data)  
            existing_slugs = NewsPage.objects.filter\
                                            (locale=self.locale).values_list('slug2', flat=True)
            
            count = 1
            new_slug = base_slug

            while new_slug in existing_slugs:
                count += 1
                new_slug = f"{base_slug}-{count}"

            self.slug2 = new_slug

        super().save(*args, **kwargs)


#---------------------------------------RealEstateRegistrationPage---------------------------------

#
class RealEstateRegistrationPageImagesModel(Orderable ,models.Model):

    page = ParentalKey("usefull.RealEstateRegistrationPage", related_name="estate_carusel_images", 
                       on_delete=models.CASCADE)

    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                on_delete=models.SET_NULL, related_name="+",
                                verbose_name="Image")


#
class RealEstateRegistrationPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):
    
    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['usefull.UsefullIndexPage']
    subpage_types = []
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Banner Image")

    content = models.TextField()
    tab1_subtitle = models.CharField(max_length=250, null=True, blank=False)
    tab1_content = RichTextField()
    tab2_subtitle = models.CharField(max_length=250, null=True, blank=False)
    tab2_content = RichTextField()
    section_title = models.CharField(max_length=250, null=True, blank=False)
    section_tab = StreamField([('Section_Tab',EstateRegisterSectionBlock(), ),], 
                              use_json_field=True)

    last_tab_title = models.CharField(max_length=250, null=True, blank=False)
    last_tab_content = RichTextField()
    last_tab_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Last Tab Image")

    
    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + [
        FieldPanel('banner_image'),
        FieldPanel('content'),

        FieldPanel('tab1_subtitle'),
        FieldPanel('tab1_content'),
        FieldPanel('tab2_subtitle'),
        FieldPanel('tab2_content'),
        FieldPanel('section_title'),
        FieldPanel('section_tab'),
        FieldPanel('last_tab_title'),
        FieldPanel('last_tab_content'),
        FieldPanel('last_tab_image'),

        MultiFieldPanel(
            [
                InlinePanel(
                    "estate_carusel_images",
                    label="Carusel Images",
                ), ], heading="Carusel Images",),
    ]

    api_fields = SEOPage.api_fields + [
        APIField('slug2'),
        APIField('full_path', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),    
        APIField('content'),
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('tab1_subtitle'),
        APIField('tab1_content'),
        APIField('tab2_subtitle'),
        APIField('tab2_content'),
        APIField('section_title'),
        APIField('section_tab', RealEstateSectionTabSerializer(source='get_section_tab')),
        APIField('last_tab_title'),
        APIField('last_tab_content'),
        APIField('last_tab_image', CustomImageSerializer(source='get_last_tab_image')),
        APIField('estate_carusel_images', MultipleImageSerializer(source='get_carusel_images')),
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
    
    def get_last_tab_image(self):
        return self.last_tab_image if self.last_tab_image else None 
    
    
    def get_carusel_images(self):    
        result = None
        special_carusel_obj = self.estate_carusel_images.select_related('image')
        general_carusel_obj = AllImages.objects.first()
        if special_carusel_obj:
            result = [image.image for image in special_carusel_obj]
        else:
            if general_carusel_obj:
                result = general_carusel_obj.carusel_images.all()                
        return result  
 


    def get_section_tab(self):
        return self.section_tab if self.section_tab else None

    def get_search_image(self):
        return self.search_image
    
    def get_full_path(self):
        parent = self.get_parent()
        grandpa = parent.get_parent()
        return (grandpa.title, parent.title, self.title)
    
    def get_child_pages(self):
        return self.get_children() if self.get_children() else None

    def save(self, *args, **kwargs):

        # Check if the page is being created for the first time
        if not self.pk:
            # If max_count=1 in current page, then we don't need another variable to slugify it
            self.slug2 = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()

        super().save(*args, **kwargs)


#
class SubscriberForm(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{}'.format(self.email)
