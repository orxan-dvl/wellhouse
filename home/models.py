from django.db import models
from ckeditor.fields import RichTextField

from wagtail.admin.panels import FieldPanel, FieldRowPanel, InlinePanel, MultiFieldPanel
from wagtailcache.cache import WagtailCacheMixin
from wagtailmetadata.models import MetadataPageMixin
from wagtail.core.fields import StreamField
from wagtail.core.blocks import CharBlock, RichTextBlock

from wagtail.api import APIField

from seo.models import SEOPage
from core.serializers import  (CustomImageSerializer, MultipleImageSerializer, 
                               FullPathSerializer, ChildPageSerializer, SearchImageSerializer)
from home.blocks import AdvantagesTabBlock, IconWithBackgroundColorBlock
from advertisement.models import Tags, OffererPerson, PropertyDetailPage, Category

from advertisement.serializers import (SimilarPropertyDetailSerializer, CategoryListSerializer,
                                       CategoryForPropertyDetailPageSerializer,  )

from home.serializers import (HomeTagsListSerializer, HomeAdvantagesSerializer, HomeEmployeeListSerializer,
                              IconTabSerializer)
from feedback.forms import Feedback
from feedback.serializers import FeedbackIndexSerializer
from usefull.models import BlogPage
from usefull.serializers import BlogsSerializer
from aboutindex.serializers import FooterTabSerializer
from employee.models import Employee

from wellhouse.settings.base import WAGTAIL_CONTENT_LANGUAGES as wcl


#
class HomePage(WagtailCacheMixin, MetadataPageMixin, SEOPage):

    max_count = len(wcl)
    subpage_types = ['aboutindex.AboutIndexPage', 'advertisement.PropertyInTurkeyIndexPage',
                     'contact_us.ContactUsIndexPage', 'feedback.FeedbackIndexPage',
                     'services.ServiceIndexPage', 'usefull.UsefullIndexPage', 'home.PrivacyPolicyIndexPage']

    object_type = "website"
    schemaorg_type = "website"


    slug2 = models.SlugField(max_length=255, editable=False, null=False)

#section filter starts
    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Background Image")

    banner_title = models.CharField(max_length=255, null=True, blank=False)
    banner_content = models.TextField()

#section advantage starts
    advantage_section_title = models.CharField(max_length=255, null=True, blank=False)

    advantages_section_data = StreamField([("Advantages", AdvantagesTabBlock(), ),], 
                                            use_json_field=True, min_num=5, max_num=5)
    
    form_button_title = models.CharField(max_length=50, null=True, blank=False)
    form_button_inline_text = models.CharField(max_length=20, null=True, blank=False)

    advantage_section_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",)
    

#section_ctg_image_menu starts(you can see it in apifields)
    section_ctg_image_menu_title = models.CharField(max_length=255, null=True, blank=False)

#section_new_advertisements starts(you can see it in apifields)
    section_new_advertisments_title = models.CharField(max_length=255, null=True, blank=False)

#section_tag_image_menu starts(you can see it in apifields)
    
    section_tag_image_menu_title = models.CharField(max_length=255, null=True, blank=False)
    section_tag_image_menu_content = models.TextField()

#section_all_properties_menu starts(you can see it in apifields)
    section_all_properties_menu_title = models.CharField(max_length=255, null=True, blank=False)
#section home_feedback_menu starts
    section_feedback_menu_title = models.CharField(max_length=255, null=True, blank=False)
#section home_blogs starts
    section_home_blogs_title = models.CharField(max_length=255, null=True, blank=False)
#section 4 icons starts
    section_icons_title = models.CharField(max_length=255, null=True, blank=False)
    section_icons_content = RichTextField()
    icon_tab = StreamField(
                                        [
                                        ("Icons", (IconWithBackgroundColorBlock()), ),
                                         ], use_json_field=True, min_num=4, max_num=4,)

#section form starts
    section_form_title = models.CharField(max_length=255, null=True, blank=False)
    section_form_content = RichTextField()

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + [
        FieldPanel("banner_image"),
        FieldPanel("banner_title"),
        FieldPanel("banner_content"),
        FieldPanel("advantage_section_title"),
        FieldPanel("advantages_section_data"),
        FieldPanel("form_button_title"),
        FieldPanel("form_button_inline_text"),
        FieldPanel("advantage_section_image"),
#section_ctg_image_menu starts
        FieldPanel("section_ctg_image_menu_title"),
#section_new_advertisements starts (you can see it in apifields)
        FieldPanel("section_new_advertisments_title"),
#section_tag_image_menu starts(you can see it in apifields)
        FieldPanel("section_tag_image_menu_title"),
        FieldPanel("section_tag_image_menu_content"),
#section_all_properties_menu starts(you can see it in apifields)
        FieldPanel("section_all_properties_menu_title"),
#section home_feedback_menu starts
        FieldPanel("section_feedback_menu_title"),
#section home_blogs starts
        FieldPanel("section_home_blogs_title"),
#section 4 icons starts
        FieldPanel("section_icons_title"),
        FieldPanel("section_icons_content"),
        FieldPanel("icon_tab"),
#section form starts
        FieldPanel("section_form_title"),
        FieldPanel("section_form_content"),


    ]

    api_fields = [
        APIField("slug2"),
        APIField("banner_image", CustomImageSerializer(source='get_banner_image')),
        APIField("banner_title"),
        APIField("banner_content"),
        APIField("advantage_section_title"),
        APIField("advantages_section_data", HomeAdvantagesSerializer(source='get_advantages_section_data')),
        APIField("form_button_title"),
        APIField("form_button_inline_text"),
        APIField("advantage_section_image", 
                 CustomImageSerializer(source='get_advantage_section_image')),
#section_ctg_image_menu starts
        APIField("section_ctg_image_menu_title"),
        APIField("home_category_6_list", CategoryListSerializer(source='get_home_category_6_list')),

#section_new_advertisements starts (you can see it in apifields)
        APIField("section_new_advertisments_title"),
        APIField("home_6_new_properties", 
                 SimilarPropertyDetailSerializer(source='get_home_6_new_properties')),

#section_tag_image_menu starts(you can see it in apifields)
        APIField("section_tag_image_menu_title"),
        APIField("section_tag_image_menu_content"),
        APIField("home_tag_6_item_list", HomeTagsListSerializer(source='get_home_tag_6_item_list')),

#section_all_properties_menu starts(you can see it in apifields)
        APIField("section_all_properties_menu_title"),

#section_categories_8 starts
        APIField("home_categories_8_data", CategoryListSerializer(source='get_section2_category_list')),
        APIField("properties_due_section2_ctg_1_len6", 
                 SimilarPropertyDetailSerializer(source='get_properties_due_section2_ctg_1_len6')),
        APIField("properties_due_section2_ctg_2_len6", 
                 SimilarPropertyDetailSerializer(source='get_properties_due_section2_ctg_2_len6')),
        APIField("properties_due_section2_ctg_3_len6", 
                 SimilarPropertyDetailSerializer(source='get_properties_due_section2_ctg_3_len6')),
        APIField("properties_due_section2_ctg_4_len6", 
                 SimilarPropertyDetailSerializer(source='get_properties_due_section2_ctg_4_len6')),
        APIField("properties_due_section2_ctg_5_len6", 
                 SimilarPropertyDetailSerializer(source='get_properties_due_section2_ctg_5_len6')),
        APIField("properties_due_section2_ctg_6_len6", 
                 SimilarPropertyDetailSerializer(source='get_properties_due_section2_ctg_6_len6')),
        APIField("properties_due_section2_ctg_7_len6", 
                 SimilarPropertyDetailSerializer(source='get_properties_due_section2_ctg_7_len6')),
        APIField("properties_due_section2_ctg_8_len6", 
                 SimilarPropertyDetailSerializer(source='get_properties_due_section2_ctg_8_len6')),


#section home_feedback_menu starts
        APIField("section_feedback_menu_title"),
        APIField("home_feedbacks_2", FeedbackIndexSerializer(source='get_home_feedbacks_2')),

#section home_blogs starts
        APIField("section_home_blogs_title"),
        APIField("home_blogs_3", BlogsSerializer(source='get_home_blogs_3')),

#section 4 icons starts
        APIField('section_icons_title'),
        APIField('section_icons_content'),
        APIField('icon_tab', IconTabSerializer(source='get_icon_tab')),
#section form starts
        APIField("section_form_title"),
        APIField("section_form_content"),
        APIField('carusel_employees', HomeEmployeeListSerializer(source='get_carusel_employees')),

        APIField('full_path', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),
        APIField("search_image", SearchImageSerializer(source='get_search_image')),
        APIField("seo_title"),
        APIField("search_description"),
    ]

#------------------------------------other methods--------------------------------

    def get_banner_image(self):
        return self.banner_image if self.banner_image else None
    
    def get_advantages_section_data(self):
        return self.advantages_section_data if self.advantages_section_data else None
    
    def get_advantage_section_image(self):
        return self.advantage_section_image if self.advantage_section_image else None

  
#-----------------------------------section_ctg_image_menu starts------------------------------

    def get_home_category_6_list(self):
        result=None
        queryset = Category.objects.filter(locale__language_code=self.locale.language_code,
                                           existing_in_section_6s=True).order_by('order_number_section_6s')
        if len(queryset)>0:
            if len(queryset)>6:
                result = queryset[:6]
            else:
                result = queryset
        return result


#-------------------------------section_new_advertisements starts----------------------------------------

    def get_home_6_new_properties(self):   #you have to get 6 items
        queryset = PropertyDetailPage.objects.filter(locale__language_code=self.locale.language_code,
                                                     is_sold=False, live=True).order_by('-publishing_date')
        result = None
        if len(queryset)>0:
            if len(queryset) > 6:
                result = queryset[:6]
            else:
                result = queryset
        return result

#--------------------------section_tag_image_menu starts---------------------------------------

#    def get_home_tag_6_item_list(self):
#        queryset_tags = Tags.objects.filter(
#            locale__language_code=self.locale.language_code,
#            existing_in_homepage=True
#        ).order_by('order_number')
#
#        queryset_offerers = OffererPerson.objects.filter(
#            locale__language_code=self.locale.language_code,
#            existing_in_homepage=True
#        ).order_by('order_number')
#
#        result_offerers = None
#        if queryset_offerers:
#            if len(queryset_offerers) > 2:
#                result_offerers = queryset_offerers[:2]
#            else:
#                result_offerers = queryset_offerers
#            result_offerers_list = list(result_offerers)
#        else:
#            result_offerers_list = []
#
#        result_tags = None
#        if len(queryset_tags) > 0:
#            if len(queryset_tags) > 4:
#                result_tags = queryset_tags[:4]
#            else:
#                result_tags = queryset_tags
#            result_tags_list = list(result_tags)
#        else:
#            result_tags_list = []
#
#        result_tags_list.extend(result_offerers_list)
#        return result_tags_list

    def get_home_tag_6_item_list(self):
        tags = Tags.objects.filter(locale__language_code=self.locale.language_code, 
                                   existing_in_homepage=True).order_by('order_number')
        
        offerers = OffererPerson.objects.filter(locale__language_code=self.locale.language_code,
                                                existing_in_homepage=True).order_by('order_number')

        items = []
        items.extend(tags[:4])
        items.extend(offerers)
        return items

#-----------------------------section_all_properties_menu starts----------------------------

    def get_section2_category_list(self):
        result=None
        queryset = Category.objects.filter(locale__language_code=self.locale.language_code,
                                           existing_in_section_8s=True).order_by('order_number_section_8s')
        if len(queryset)>0:
            if len(queryset)>8:
                result = queryset[:8]
            else:
                result = queryset
        return result


    def get_properties_due_section2_ctg_1_len6(self):
    
        ctg_1 = Category.objects.filter(locale__language_code=self.locale.language_code,
                                        existing_in_section_8s=True, order_number_section_8s=1).first()

        queryset = PropertyDetailPage.objects.filter(property_category=ctg_1, is_sold=False,
                                                    property_category__order_number_section_8s=1,
                                                    locale__language_code=self.locale.language_code,
                                                    live=True).order_by('-publishing_date')
        result = None
        if len(queryset) > 0:
            if len(queryset) > 6:
                result = queryset[:6]
            else:
                result = queryset
        return result if queryset else None


    def get_properties_due_section2_ctg_2_len6(self):
        ctg_2 = Category.objects.filter(locale__language_code=self.locale.language_code,
                                        existing_in_section_8s=True, order_number_section_8s=2).first()

        queryset = PropertyDetailPage.objects.filter(property_category=ctg_2, is_sold=False,
                                                    property_category__order_number_section_8s=2,
                                                    locale__language_code=self.locale.language_code,
                                                    live=True).order_by('-publishing_date')
        result = None
        if len(queryset) > 0:
            if len(queryset) > 6:
                result = queryset[:6]
            else:
                result = queryset
        return result if queryset else None


    def get_properties_due_section2_ctg_3_len6(self):
        ctg_3 = Category.objects.filter(locale__language_code=self.locale.language_code,
                                        existing_in_section_8s=True, order_number_section_8s=3).first()

        queryset = PropertyDetailPage.objects.filter(property_category=ctg_3, is_sold=False,
                                                    property_category__order_number_section_8s=3,
                                                    locale__language_code=self.locale.language_code,
                                                    live=True).order_by('-publishing_date')
        result = None
        if len(queryset) > 0:
            if len(queryset) > 6:
                result = queryset[:6]
            else:
                result = queryset
        return result if queryset else None


    def get_properties_due_section2_ctg_4_len6(self):
        ctg_4 = Category.objects.filter(locale__language_code=self.locale.language_code,
                                        existing_in_section_8s=True, order_number_section_8s=4).first()

        queryset = PropertyDetailPage.objects.filter(property_category=ctg_4, is_sold=False,
                                                    property_category__order_number_section_8s=4,
                                                    locale__language_code=self.locale.language_code,
                                                    live=True).order_by('-publishing_date')        
        result = None
        if len(queryset) > 0:
            if len(queryset) > 6:
                result = queryset[:6]
            else:
                result = queryset
        return result if queryset else None


    def get_properties_due_section2_ctg_5_len6(self):
        ctg_5 = Category.objects.filter(locale__language_code=self.locale.language_code,
                                        existing_in_section_8s=True, order_number_section_8s=5).first()

        queryset = PropertyDetailPage.objects.filter(property_category=ctg_5, is_sold=False,
                                                    property_category__order_number_section_8s=5,
                                                    locale__language_code=self.locale.language_code,
                                                    live=True).order_by('-publishing_date')        
        result = None
        if len(queryset) > 0:
            if len(queryset) > 6:
                result = queryset[:6]
            else:
                result = queryset
        return result if queryset else None


    def get_properties_due_section2_ctg_6_len6(self):
        ctg_6 = Category.objects.filter(locale__language_code=self.locale.language_code,
                                        existing_in_section_8s=True, order_number_section_8s=6).first()

        queryset = PropertyDetailPage.objects.filter(property_category=ctg_6, is_sold=False,
                                                    property_category__order_number_section_8s=6,
                                                    locale__language_code=self.locale.language_code,
                                                    live=True).order_by('-publishing_date')        
        result = None
        if len(queryset) > 0:
            if len(queryset) > 6:
                result = queryset[:6]
            else:
                result = queryset
        return result if queryset else None


    def get_properties_due_section2_ctg_7_len6(self):
        ctg_7 = Category.objects.filter(locale__language_code=self.locale.language_code,
                                        existing_in_section_8s=True, order_number_section_8s=7).first()

        queryset = PropertyDetailPage.objects.filter(property_category=ctg_7, is_sold=False,
                                                    property_category__order_number_section_8s=7,
                                                    locale__language_code=self.locale.language_code,
                                                    live=True).order_by('-publishing_date')        
        result = None
        if len(queryset) > 0:
            if len(queryset) > 6:
                result = queryset[:6]
            else:
                result = queryset
        return result if queryset else None


    def get_properties_due_section2_ctg_8_len6(self):
        ctg_8 = Category.objects.filter(locale__language_code=self.locale.language_code,
                                        existing_in_section_8s=True, order_number_section_8s=8).first()

        queryset = PropertyDetailPage.objects.filter(property_category=ctg_8, is_sold=False,
                                                    property_category__order_number_section_8s=8,
                                                    locale__language_code=self.locale.language_code,
                                                    live=True).order_by('-publishing_date')        
        result = None
        if len(queryset) > 0:
            if len(queryset) > 6:
                result = queryset[:6]
            else:
                result = queryset
        return result if queryset else None
    
#------------------------------section home_feedback_menu starts-----------------------------
    def get_home_feedbacks_2(self):
        queryset = Feedback.objects.filter(show_in_homepage=True).order_by('-created_at')
        result = None
        if len(queryset)>0:
            if len(queryset)>2:
                result = queryset[:2]
            else:
                result = queryset
        return result
    
#---------------------------------------section home_blogs starts--------------------------------

    def get_home_blogs_3(self):
        queryset = BlogPage.objects.filter(locale__language_code=self.locale.language_code,
                                           existence_in_homepage=True).order_by('-created_at')
        result = None
        if len(queryset)>0:
            if len(queryset)>3:
                result = queryset[:3]
            else:
                result = queryset
        return result

    
#---------------------------------------section icon methods---------------------------------------
    def get_icon_tab(self):
        return self.icon_tab if self.icon_tab else None

#---------------------------------------employee carusel section---------------------------------------

    def get_carusel_employees(self):
        queryset = Employee.objects.filter(locale__language_code=self.locale.language_code)
        return queryset

#---------------------------------------standart methods----------------------------------------

    def get_full_path(self):
        return self.title if self.title else None

    def get_child_pages(self):
        return None

    def get_search_image(self):
        return self.search_image
    
    def save(self, *args, **kwargs):
        # Check if the page is being created for the first time
        if not self.pk:
            #if max_count=1 in current page, then we don't need another variable to slugify it
            self.slug2 = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()
        super().save(*args, **kwargs)


#------------------------------------------------------------
#Pages for footer

#
class PrivacyPolicyIndexPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):
    
    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Background Image")
    
    subtitle = models.CharField(max_length=100, null=True, blank=False)
    content = models.TextField()

    content = StreamField([("content", RichTextBlock(), ),],
                           use_json_field=True, min_num=1, max_num=1)
    
    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + [

        FieldPanel('banner_image'),
        FieldPanel('subtitle'),
        FieldPanel('content'),
    ]

    api_fields = SEOPage.api_fields +[

        APIField('slug2'),
        APIField('fullpath', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),   
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('subtitle'),
        APIField('content'),
        APIField("search_image", SearchImageSerializer(source='get_search_image')),
        APIField("seo_title"),
        APIField("search_description")
    ]

    def get_full_path(self):
        return self.title
    
    def get_child_pages(self):
        return self.get_children() if self.get_children() else None

    def get_banner_image(self):
        return self.banner_image if self.banner_image else None

    def get_content(self):
        return self.content if self.content else None

    def get_search_image(self):
        return self.search_image

    def save(self, *args, **kwargs):
        # Check if the page is being created for the first time
        if not self.pk:
            #if max_count=1 in current page, then we don't need another variable to slugify it
            self.slug2 = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()
        super().save(*args, **kwargs)
