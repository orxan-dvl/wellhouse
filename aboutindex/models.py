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


from aboutindex.serializers import (HeaderTabSerializer, AdvantagesTabSerializer,
                                    FooterTabSerializer, CompanyDetailsTabSerializer, 
                                    BankAccountDetailsTabSerializer, CenterTabSerializer, 
                                    SectionAboutMemberSerializer)

from aboutindex.blocks import (HeaderTabBlock, AdvantagesTabBlock, CenterTabBlock, 
                               IconWithHoverColorBlock, CompanyDetailsBlock, 
                               BankAccountDetailsBlock, TeamMemberBlock)


class AboutIndexPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):

    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['home.HomePage']
    subpage_types = []
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Banner Image")
   
    banner_subtitle = models.CharField(max_length=50, null=True, blank=False)
    banner_content = models.TextField()

#starts section_about company
    header_tab = StreamField(
                                        [
                                        ("Header", HeaderTabBlock(), ),
                                         ], use_json_field=True, min_num=1, max_num=1)
    
    advantages_tab = StreamField(
                                        [
                                        ("Advantages", AdvantagesTabBlock(), ),
                                         ], use_json_field=True, min_num=1, max_num=1)

    center_tab = StreamField(
                                        [
                                        ("Center", CenterTabBlock(), ),
                                         ], use_json_field=True, min_num=1, max_num=1)

    footer_tab = StreamField(
                                        [
                                        ("Icons", IconWithHoverColorBlock(), ),
                                         ], use_json_field=True, min_num=4, max_num=4, 
                                         help_text='You must add 4 icons with their hover color')
  

    company_details_tab = StreamField(
                                        [
                                        ('Company_Details',CompanyDetailsBlock(), ),
                                         ], use_json_field=True, min_num=1, max_num=1)

    bank_account_details_tab = StreamField(
                                        [
                                        ('BankAccountDetails', BankAccountDetailsBlock(), ),    
                                         ], use_json_field=True, min_num=1, max_num=1)

#section2 starts

    section_about_title = models.CharField(max_length=255, null=True, blank=False)

    section_about_member = StreamField(
                                        [
                                        ('Members', TeamMemberBlock(), ),
                                        ], use_json_field=True)

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + [

        FieldPanel('banner_image'),
        FieldPanel('banner_subtitle'),
        FieldPanel('banner_content'),
        FieldPanel('header_tab'),
        FieldPanel('advantages_tab'),
        FieldPanel('center_tab'),
        FieldPanel('footer_tab'),
        FieldPanel('company_details_tab'),
        FieldPanel('bank_account_details_tab'),
        FieldPanel('section_about_title'),
        FieldPanel('section_about_member'),
    ]

    api_fields = SEOPage.api_fields +[
        APIField('slug2'),
        APIField('full_path', FullPathSerializer(source='get_full_path')), 
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),     
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('banner_subtitle'),
        APIField('banner_content'),
        APIField('header_tab', HeaderTabSerializer(source='get_header_tab')),
        APIField('advantages_tab', AdvantagesTabSerializer(source='get_advantages_tab')),
        APIField('center_tab', CenterTabSerializer(source='get_center_tab')),
        APIField('footer_tab', FooterTabSerializer(source='get_footer_tab')),
        APIField('company_details_tab', CompanyDetailsTabSerializer(source='get_company_details_tab')),
        APIField('bank_account_details_tab', 
                 BankAccountDetailsTabSerializer(source='get_bank_account_details_tab')),

        APIField('section_about_title'),
        APIField('section_about_member', SectionAboutMemberSerializer(source='get_section_about_member')),
        APIField("search_image", serializer=SearchImageSerializer(source='get_search_image')),
        APIField("seo_title"),
        APIField("search_description"),
    ]

    def get_header_tab(self):
        return self.header_tab if self.header_tab else None
    
    def get_advantages_tab(self):
        return self.advantages_tab if self.advantages_tab else None

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

    def get_center_tab(self):
        return self.center_tab if self.center_tab else None
    
    def get_footer_tab(self):
        return self.footer_tab if self.footer_tab else None
    
    def get_company_details_tab(self):
        return self.company_details_tab if self.company_details_tab else None

    def get_bank_account_details_tab(self):
        return self.bank_account_details_tab if self.bank_account_details_tab else None
    
    def get_section_about_member(self):
        return self.section_about_member if self.section_about_member else None

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



