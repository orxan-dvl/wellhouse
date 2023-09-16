from django.db import models
from wagtail.models import Page, Orderable, TranslatableMixin, Locale
from wagtailmetadata.models import MetadataPageMixin
from wagtailcache.cache import WagtailCacheMixin
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSiteSetting
from wagtail.contrib.settings.registry import register_setting
from wagtailsvg.models import Svg
from phonenumber_field.modelfields import PhoneNumberField
from wagtail_color_panel.edit_handlers import NativeColorPanel
from wagtail_color_panel.fields import ColorField
from modelcluster.models import ClusterableModel

from wagtail.api import APIField
from seo.models import SEOPage


#----------------------------Repetable Images------------------------------------------------

#Images for Property detail page, if background and carusel images is null images will be retrieved from
#this table

class AllImages( models.Model):
    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Image")

    carusel_images = models.ManyToManyField("wagtailimages.Image", blank=True,
                                            related_name="+", verbose_name="Carusel_Image")


#--------------------------------------Site Settings-----------------------------------------

#Site settings
@register_setting(icon='globe')
class SiteSetting(BaseSiteSetting):

    logo = models.ForeignKey(Svg, on_delete=models.SET_NULL, null=True, 
                            blank=False, related_name="Logo"
    )
    favicon = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Favicon")
    
    number = PhoneNumberField(help_text='Enter your number', null=True, blank=True)
    
    number2 = PhoneNumberField(help_text='Enter your number 2', null=True, blank=True)
    
    number3 = PhoneNumberField(help_text='Enter your number 2', null=True, blank=True)
    
    number4 = PhoneNumberField(help_text='Enter your number 2', null=True, blank=True)
    
    email = models.EmailField(max_length=255, help_text='Enter your E-mail', 
                              null=True, blank=True)
    
    email2 = models.EmailField(max_length=255, help_text='Enter your second E-mail', 
                               null=True, blank=True)
    
    full_address = models.CharField(max_length=255, help_text='Enter your second E-mail',
                                    null=True, blank=True)
    
    color = ColorField(default="#000000")
    iframe = models.TextField(null=True, blank=True)

    panels = [
        FieldPanel('number'),
        FieldPanel('number2'),
        FieldPanel('number3'),
        FieldPanel('number4'),
        FieldPanel('email'),
        FieldPanel('email2'),
        FieldPanel('full_address'),
        FieldPanel('logo'),
        FieldPanel('favicon'),
        NativeColorPanel('color'),
    ]

    def view(request):
        sitesettings = SiteSetting.for_request(request)

    class Meta:
        verbose_name = "Website settings"
        verbose_name_plural = "Websites settings"



#Social media settings
@register_setting(icon='tag')
class SocialMediaSetting(BaseSiteSetting):

    facebook = models.URLField(max_length=255, help_text='Enter your number', 
                               null=True, blank=True)
    
    instagram = models.URLField(max_length=255, help_text='Enter your number 2', 
                                null=True, blank=True)
    
    vk = models.URLField(max_length=255, help_text='Enter your E-mail', null=True, blank=True)

    linkedin = models.URLField(max_length=255, help_text='Enter your second E-mail', 
                               null=True, blank=True)
    
    pinterest = models.URLField(max_length=255, help_text='Enter your second E-mail', 
                                null=True, blank=True)
    
    tiktok = models.URLField(max_length=255, help_text='Enter your second E-mail', 
                             null=True, blank=True)

    whatsapp = models.URLField(max_length=255, help_text='Enter your second E-mail', 
                               null=True, blank=True)
    telegram = models.URLField(max_length=255, help_text='Enter your second E-mail', 
                               null=True, blank=True)
    
    panels = [
        FieldPanel('facebook'),
        FieldPanel('instagram'),
        FieldPanel('vk'),
        FieldPanel('linkedin'),
        FieldPanel('pinterest'),
        FieldPanel('tiktok'),
        FieldPanel('whatsapp'),
        FieldPanel('telegram'),

    ]

    def view(request):
        socialmediasetting = SocialMediaSetting.for_request(request)

    class Meta:
        verbose_name = "Social media setting"
        verbose_name_plural = "Social media settings"




