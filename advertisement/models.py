from django.db import models
from django.utils.text import slugify

from wagtail.models import Page, Orderable, TranslatableMixin
from modelcluster.fields import ParentalKey
from modelcluster.fields import ParentalManyToManyField

from wagtailcache.cache import WagtailCacheMixin
from wagtailmetadata.models import MetadataPageMixin
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.api import APIField
from wagtail.models import TranslatableMixin
from ckeditor.fields import RichTextField
from wellhouse.settings.base import WAGTAIL_CONTENT_LANGUAGES as wcl
from wellhouse.custom_localize_field import LocalizedSelectPanel


from core.serializers import (FullPathSerializer, CustomImageSerializer, 
                              ChildPageSerializer, MultipleImageSerializer, SearchImageSerializer)

from core.models import AllImages

from advertisement.serializers import (CityForPropertyIndexPageSerializer, TypeForPropertyIndexPageSerializer,
                            CustomIdSerializer, CategoryForPropertyDetailPageSerializer, CostSerialzer,
                            PropertyDetailForeingkey2FieldSerializer, SimilarPropertyDetailSerializer,
                            CategoryListSerializer, PropertyOffererSerializer, HomeRoomSerialzer)

from seo.models import SEOPage
#



#Room model
class Room(Orderable, TranslatableMixin, models.Model):
    class Meta:
        verbose_name = 'Room'
        unique_together = ('translation_key', 'locale')

    name = models.CharField(max_length=50, null=True, blank=False)
    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.slug2:
            # my_data is classname of the page, which was generated from classname
            my_data = (str(self.__class__)).replace('<class', '').replace('>', '').replace("'", "").replace(" ", "") \
                                                .replace(".models", "").lower().replace(".", "_")

            base_slug = slugify(my_data)
            existing_slugs = Room.objects.filter(locale=self.locale).union\
                                                (Room.objects.filter(locale=self.locale))\
                                                    .values_list('slug2', flat=True)
            count = 1
            new_slug = base_slug
            while new_slug in existing_slugs:
                count += 1
                new_slug = f"{base_slug}-{count}"
            self.slug2 = new_slug

        super().save(*args, **kwargs)


#rent, by
class Type(Orderable, TranslatableMixin, models.Model):

    class Meta:
        verbose_name = 'Type'
        unique_together = ('translation_key', 'locale')

    name = models.CharField(max_length=50, null=True, blank=False)
    slug2 = models.SlugField(max_length=255, editable=False, null=True)


    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.slug2:
            # my_data is classname of the page, which was generated from classname
            my_data = (str(self.__class__)).replace('<class', '').replace('>', '').replace("'", "").replace(" ", "") \
                                                .replace(".models", "").lower().replace(".", "_")

            base_slug = slugify(my_data)
            existing_slugs = Type.objects.filter(locale=self.locale).union\
                                                (Type.objects.filter(locale=self.locale))\
                                                    .values_list('slug2', flat=True)
            count = 1
            new_slug = base_slug
            while new_slug in existing_slugs:
                count += 1
                new_slug = f"{base_slug}-{count}"
            self.slug2 = new_slug

        super().save(*args, **kwargs)


#
class City(Orderable, TranslatableMixin, models.Model):

    class Meta:
        verbose_name = 'City'
        unique_together = ('translation_key', 'locale')

    name = models.CharField(max_length=50, null=True, blank=False)
    slug2 = models.SlugField(max_length=255, editable=False, null=False)


    def __str__(self):
        return '{}'.format(self.name)
    
    def save(self, *args, **kwargs):
        if not self.slug2:
            # my_data is classname of the page, which was generated from classname
            my_data = (str(self.__class__)).replace('<class', '').replace('>', '').replace("'", "").replace(" ", "") \
                                                .replace(".models", "").lower().replace(".", "_")

            base_slug = slugify(my_data)
            existing_slugs = City.objects.filter(locale=self.locale).union\
                                                (City.objects.filter(locale=self.locale))\
                                                    .values_list('slug2', flat=True)
            count = 1
            new_slug = base_slug
            while new_slug in existing_slugs:
                count += 1
                new_slug = f"{base_slug}-{count}"
            self.slug2 = new_slug

        super().save(*args, **kwargs)


#
class Region(Orderable, TranslatableMixin, models.Model):

    class Meta:
        verbose_name = 'Region'
        unique_together = ('translation_key', 'locale')

    name = models.CharField(max_length=50, null=True, blank=False)
    city_rel = models.ForeignKey('City', on_delete=models.CASCADE)
    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    panels = [        
        FieldPanel("name"),
        LocalizedSelectPanel("city_rel"),
        ]


    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.slug2:
            # my_data is classname of the page, which was generated from classname
            my_data = (str(self.__class__)).replace('<class', '').replace('>', '').replace("'", "").replace(" ", "") \
                                                .replace(".models", "").lower().replace(".", "_")

            base_slug = slugify(my_data)
            existing_slugs = Region.objects.filter(locale=self.locale).union\
                                                (Region.objects.filter(locale=self.locale))\
                                                    .values_list('slug2', flat=True)
            count = 1
            new_slug = base_slug
            while new_slug in existing_slugs:
                count += 1
                new_slug = f"{base_slug}-{count}"
            self.slug2 = new_slug

        super().save(*args, **kwargs)


#
class Category(Orderable, TranslatableMixin, models.Model):

    class Meta:
        verbose_name = 'Category'
        unique_together = ('translation_key', 'locale')

    name = models.CharField(max_length=50, null=True, blank=False)
    slug2 = models.SlugField(max_length=255, editable=False, null=False)
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                on_delete=models.SET_NULL, related_name="+",
                                verbose_name="Image")

    existing_in_section_6s = models.BooleanField(default=True)
    order_number_section_6s = models.IntegerField(null=True, blank=False,)
    existing_in_section_8s = models.BooleanField(default=False)
    order_number_section_8s = models.IntegerField(null=True, blank=False)

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.slug2:
            # my_data is classname of the page, which was generated from classname
            my_data = (str(self.__class__)).replace('<class', '').replace('>', '').replace("'", "").replace(" ", "") \
                                                .replace(".models", "").lower().replace(".", "_")

            base_slug = slugify(my_data)
            existing_slugs = Category.objects.filter(locale=self.locale).union\
                                                (Category.objects.filter(locale=self.locale))\
                                                    .values_list('slug2', flat=True)
            count = 1
            new_slug = base_slug
            while new_slug in existing_slugs:
                count += 1
                new_slug = f"{base_slug}-{count}"
            self.slug2 = new_slug

        super().save(*args, **kwargs)



#
class OffererPerson(Orderable, TranslatableMixin, models.Model):

    class Meta:
        verbose_name = 'OffererPerson'
        unique_together = ('translation_key', 'locale')

    name = models.CharField(max_length=50, null=True, blank=False)
    slug2 = models.SlugField(max_length=255, editable=False, null=False)
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                on_delete=models.SET_NULL, related_name="+",
                                verbose_name="Image")

    existing_in_homepage = models.BooleanField(default=False)
    order_number = models.IntegerField(null=True, blank=False)


    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.slug2:
            # my_data is classname of the page, which was generated from classname
            my_data = (str(self.__class__)).replace('<class', '').replace('>', '').replace("'", "").replace(" ", "") \
                                                .replace(".models", "").lower().replace(".", "_")

            base_slug = slugify(my_data)
            existing_slugs = OffererPerson.objects.filter(locale=self.locale).union\
                                                (OffererPerson.objects.filter(locale=self.locale))\
                                                    .values_list('slug2', flat=True)
            count = 1
            new_slug = base_slug
            while new_slug in existing_slugs:
                count += 1
                new_slug = f"{base_slug}-{count}"
            self.slug2 = new_slug

        super().save(*args, **kwargs)


#Can create more than 4 objects, but only can choose 4 of them as existed in homepage
class Tags(Orderable, TranslatableMixin, models.Model):

    class Meta:
        verbose_name = 'Tags'
        unique_together = ('translation_key', 'locale')

    name = models.CharField(max_length=50, null=True, blank=False)
    slug2 = models.SlugField(max_length=255, editable=False, null=False)
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                on_delete=models.SET_NULL, related_name="+",
                                verbose_name="Image")

    existing_in_homepage = models.BooleanField(default=False)
    order_number = models.IntegerField(null=True, blank=False)

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        if not self.slug2:
            # my_data is classname of the page, which was generated from classname
            my_data = (str(self.__class__)).replace('<class', '').replace('>', '').replace("'", "").replace(" ", "") \
                                                .replace(".models", "").lower().replace(".", "_")

            base_slug = slugify(my_data)
            existing_slugs = Tags.objects.filter(locale=self.locale).union\
                                                (Tags.objects.filter(locale=self.locale))\
                                                    .values_list('slug2', flat=True)
            count = 1
            new_slug = base_slug
            while new_slug in existing_slugs:
                count += 1
                new_slug = f"{base_slug}-{count}"
            self.slug2 = new_slug

        super().save(*args, **kwargs)




#----------------------------------------Pages-----------------------------------------------------------

#
class PropertyInTurkeyIndexPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):

    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['home.HomePage']
    subpage_types = ['advertisement.ByPropertyIndexPage', 'advertisement.RentPropertyIndexPage',
                     'advertisement.PropertyIndexPage']
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + []

    api_fields = SEOPage.api_fields +[

        APIField('slug2'),
        APIField('all_properties', SimilarPropertyDetailSerializer(source='get_all_properties')),
        APIField('fullpath', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),   
        APIField("seo_title"),
        APIField("search_image", SearchImageSerializer(source='get_search_image')),
        APIField("search_description")
    ]

    def get_all_properties(self):
        my_queryset = PropertyDetailPage.objects.filter(locale__language_code=self.locale.language_code,
                                                        live=True, is_sold=False)\
                                                        .order_by('-publishing_date')
        return my_queryset

    def get_full_path(self):
        return (self.get_parent().title, self.title) 

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


#
class ByPropertyIndexPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):

    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['advertisement.PropertyInTurkeyIndexPage']
    subpage_types = []
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + []

    api_fields = SEOPage.api_fields +[

        APIField('slug2'),
        APIField('fullpath', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),   
        APIField('all_cities', CityForPropertyIndexPageSerializer(source='get_all_cities')),
        APIField('all_types', TypeForPropertyIndexPageSerializer(source='get_all_types')),
        APIField('all_categories', CategoryListSerializer(source='get_all_categories')),

        APIField('by_properties', SimilarPropertyDetailSerializer(source='get_properties_by')),

        APIField("seo_title"),
        APIField("search_image", SearchImageSerializer(source='get_search_image')),
        APIField("search_description")
    ]

    def get_full_path(self):
        parent = self.get_parent()
        grandpa = parent.get_parent()
        return (grandpa.title, parent.title, self.title)
    
    def get_child_pages(self):
        return self.get_children() if self.get_children() else None

    def get_search_image(self):
        return self.search_image
    
    def get_all_cities(self):
        my_queryset = City.objects.filter(locale__language_code=self.locale.language_code)
        return my_queryset if my_queryset else None

    def get_all_categories(self):
        my_queryset = Category.objects.filter(locale__language_code=self.locale.language_code)
        return my_queryset if my_queryset else None

    def get_all_types(self):
        my_queryset = Type.objects.filter(locale__language_code=self.locale.language_code)
        return my_queryset if my_queryset else None
    
    def get_properties_by(self):
        type_by = Type.objects.filter(locale__language_code=self.locale.language_code).first()
        queryset = []
        if type_by:
            queryset = PropertyDetailPage.objects.filter(locale__language_code=self.locale.language_code, 
                                                         property_type=type_by, is_sold=False)\
                                                        .order_by('-publishing_date')
        return queryset

    def save(self, *args, **kwargs):
        # Check if the page is being created for the first time
        if not self.pk:
            #if max_count=1 in current page, then we don't need another variable to slugify it
            self.slug2 = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()
        super().save(*args, **kwargs)




#
class RentPropertyIndexPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):

    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['advertisement.PropertyInTurkeyIndexPage']
    subpage_types = []
    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + []

    api_fields = SEOPage.api_fields +[

        APIField('slug2'),
        APIField('fullpath', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),   
        APIField('all_cities', CityForPropertyIndexPageSerializer(source='get_all_cities')),
        APIField('all_types', TypeForPropertyIndexPageSerializer(source='get_all_types')),
        APIField('all_categories', CategoryListSerializer(source='get_all_categories')),

        APIField('rent_properties', SimilarPropertyDetailSerializer(source='get_properties_rent')),

        APIField("seo_title"),
        APIField("search_image", SearchImageSerializer(source='get_search_image')),
        APIField("search_description")
    ]

    def get_full_path(self):
        parent = self.get_parent()
        grandpa = parent.get_parent()
        return (grandpa.title, parent.title, self.title)

    def get_child_pages(self):
        return self.get_children() if self.get_children() else None

    def get_search_image(self):
        return self.search_image
    
    def get_all_cities(self):
        my_queryset = City.objects.filter(locale__language_code=self.locale.language_code)#.last()
        return my_queryset if my_queryset else None
    
    def get_all_types(self):
        my_queryset = Type.objects.filter(locale__language_code=self.locale.language_code)#.last()
        return my_queryset if my_queryset else None

    def get_all_categories(self):
        my_queryset = Category.objects.filter(locale__language_code=self.locale.language_code)
        return my_queryset if my_queryset else None

    def get_properties_rent(self):
        type_rent = Type.objects.filter(locale__language_code=self.locale.language_code).last()
        queryset = []
        if type_rent:

            queryset = PropertyDetailPage.objects.filter(locale__language_code=self.locale.language_code, 
                                                        live=True, property_type=type_rent, is_sold=False)\
                                                        .order_by('-publishing_date')
        return queryset


    def save(self, *args, **kwargs):
        # Check if the page is being created for the first time
        if not self.pk:
            #if max_count=1 in current page, then we don't need another variable to slugify it
            self.slug2 = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()
        super().save(*args, **kwargs)



#
class PropertyIndexPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):

    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['advertisement.PropertyInTurkeyIndexPage']
    subpage_types = ['advertisement.PropertyDetailPage']

    max_count = len(wcl)

    slug2 = models.SlugField(max_length=255, editable=False, null=False)
    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Background Image")


    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + [
        FieldPanel('banner_image'),
    ]

    api_fields = SEOPage.api_fields +[

        APIField('slug2'),
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('fullpath', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),   
        APIField('all_cities', CityForPropertyIndexPageSerializer(source='get_all_cities')),
        APIField('all_types', TypeForPropertyIndexPageSerializer(source='get_all_types')),
        APIField('all_properties', SimilarPropertyDetailSerializer(source='get_all_properties')),

        APIField("seo_title", ),
        APIField("search_image", SearchImageSerializer(source='get_search_image')),
        APIField("search_description")
    ]

    def get_banner_image(self):
        return self.banner_image if self.banner_image else None

    def get_full_path(self):
        parent = self.get_parent()
        grandpa = parent.get_parent()
        return (grandpa.title, parent.title, self.title)

    def get_child_pages(self):
        return self.get_children().live() if self.get_children().live() else None

    def get_search_image(self):
        return self.search_image
    
    def get_all_cities(self):
        my_queryset = City.objects.filter(locale__language_code=self.locale.language_code)#.last()
        return my_queryset if my_queryset else None
    
    def get_all_types(self):
        my_queryset = Type.objects.filter(locale__language_code=self.locale.language_code)#.last()
        return my_queryset if my_queryset else None
    
    def get_all_properties(self):
        my_queryset = PropertyDetailPage.objects.filter(locale__language_code=self.locale.language_code,
                                                        live=True, is_sold=False)\
                                                        .order_by('-publishing_date')
        return my_queryset


    def save(self, *args, **kwargs):
        # Check if the page is being created for the first time
        if not self.pk:
            #if max_count=1 in current page, then we don't need another variable to slugify it
            self.slug2 = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()
        super().save(*args, **kwargs)


#-----------------------------------------Property Detail Page--------------------------------------

#
class AdvertisementImagesModel(Orderable ,models.Model):

    page = ParentalKey("advertisement.PropertyDetailPage", related_name="additional_images", 
                       on_delete=models.CASCADE)

    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                on_delete=models.SET_NULL, related_name="+",
                                verbose_name="Background Image")

#
class AdvertisementCaruselImagesModel(Orderable ,models.Model):

    page = ParentalKey("advertisement.PropertyDetailPage", related_name="advertisement_carusel_images", 
                       on_delete=models.CASCADE)

    image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                on_delete=models.SET_NULL, related_name="+",
                                verbose_name="Image")


#
from wagtail_localize.fields import TranslatableField, SynchronizedField

class PropertyDetailPage(WagtailCacheMixin, MetadataPageMixin, SEOPage):

    object_type = "website"
    schemaorg_type = "website"

    parent_page_types = ['advertisement.PropertyIndexPage']
    subpage_types = []

    slug2 = models.SlugField(max_length=255, editable=False, null=False)

#banner section starts
    banner_image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Background Image")


#property foreingkey section starts

    property_category = ParentalManyToManyField('advertisement.Category', blank=True, 
                                                related_name='property_category')


    property_type = models.ForeignKey("advertisement.Type", on_delete=models.SET_NULL,
                                        null=True, blank=False,
                                        related_name='property_type',)

    property_region = models.ForeignKey("advertisement.Region", on_delete=models.SET_NULL,
                                        null=True, blank=False,
                                        related_name='property_region',)
    
    property_tags = ParentalManyToManyField('advertisement.Tags', blank=True, 
                                            related_name='property_tags')
    


#property image section starts

    first_image = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Image")
    
    image_2 = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Image 2")
    
    image_3 = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Image 3")
    
    image_4 = models.ForeignKey("wagtailimages.Image", null=True, blank=False,
                                    on_delete=models.SET_NULL, related_name="+",
                                    verbose_name="Image 4")
#property detail information section starts
    existence_in_homepage = models.BooleanField(default=False)

    short_description_floor = models.IntegerField(null=True, blank=False)
    short_description_gross_area = models.FloatField(null=True, blank=True)
    short_description_rooms = ParentalManyToManyField('advertisement.Room', blank=True, 
                                                        related_name='property_rooms')

    hot_deals = models.BooleanField(default=False)

    short_description_furniture = models.BooleanField(default=False)
    short_description_sea_view = models.BooleanField(default=False)
    short_description_to_the_sea = models.FloatField(null=True, blank=True)
    short_description_to_the_center = models.FloatField(null=True, blank=True)
    short_description_to_the_airport = models.FloatField(null=True, blank=True)
    short_description_offer = models.ForeignKey("advertisement.OffererPerson", on_delete=models.SET_NULL,
                                        null=True, blank=False, related_name='property_oferrer_person',)

    short_description_year = models.SmallIntegerField(null=True, blank=False)

    general_cost = models.FloatField(null=True, blank=False)
    general_cost_second = models.FloatField(null=True, default=0.0)
    discounted_cost = models.FloatField(null=True, default=0.0)
    discounted_cost_second = models.FloatField(null=True, default=0.0)
    
    area = models.FloatField(null=True, blank=False, default=0)
    area_2 = models.FloatField(null=True, blank=True)
    is_sold = models.BooleanField(default=False)

#facility_infrastructure starts
    facility_open_pool = models.BooleanField(default=False, verbose_name='Open Pool')
    facility_green_garden = models.BooleanField(default=False, verbose_name='Green Garden')
    facility_wireless_internet = models.BooleanField(default=False, verbose_name='Wireless Internet')
    facility_satellite_tv = models.BooleanField(default=False, verbose_name='Satellite TV')
    facility_concierge = models.BooleanField(default=False, verbose_name='Concierge')
    facility_outdoor_parking = models.BooleanField(default=False, verbose_name='Outdoor Parking')
    facility_power_generator = models.BooleanField(default=False, verbose_name='Power Generator')
    facility_finnish_sauna = models.BooleanField(default=False, verbose_name='Finnish Sauna')
    facility_playground = models.BooleanField(default=False, verbose_name='Playground')
    facility_fitness_centre = models.BooleanField(default=False, verbose_name='Fitness Centre')
    facility_game_room = models.BooleanField(default=False, verbose_name='Game Room')
    facility_gazebos_for_rest = models.BooleanField(default=False, verbose_name='Gazebos for Rest')
    facility_covered_parking = models.BooleanField(default=False, verbose_name='Covered Parking')
    facility_aquapark = models.BooleanField(default=False, verbose_name='Aquapark')
    facility_amphitheater = models.BooleanField(default=False, verbose_name='Amphitheater')
    facility_pool_bar = models.BooleanField(default=False, verbose_name='Pool bar')
    facility_billiards = models.BooleanField(default=False, verbose_name='Billiards')
    facility_bowling = models.BooleanField(default=False, verbose_name='Bowling')
    facility_jacuzzi = models.BooleanField(default=False, verbose_name='jacuzzi')
    facility_indoor_pool = models.BooleanField(default=False, verbose_name='Indoor Pool')
    facility_cafe_restaurant = models.BooleanField(default=False, verbose_name='Cafe/Restaurant')
    facility_cinema = models.BooleanField(default=False, verbose_name='Cinema')
    facility_conference_hall = models.BooleanField(default=False, verbose_name='Conference Hall')
    facility_24_hour_security = models.BooleanField(default=False, verbose_name='24-hour Security')
    facility_ice_rink = models.BooleanField(default=False, verbose_name='Ice Rink')
    facility_market = models.BooleanField(default=False, verbose_name='Market')
    facility_massage_rooms = models.BooleanField(default=False, verbose_name='Massage Rooms')
    facility_mini_club = models.BooleanField(default=False, verbose_name='Mini-club')
    facility_table_tennis = models.BooleanField(default=False, verbose_name='Table Tennis')
    facility_barbershop = models.BooleanField(default=False, verbose_name='Barbershop')
    facility_walking_paths = models.BooleanField(default=False, verbose_name='Walking paths')
    facility_roman_steam_room = models.BooleanField(default=False, verbose_name='Roman Steam Room')
    facility_private_beach = models.BooleanField(default=False, verbose_name='Private Beach')
    facility_tennis_court = models.BooleanField(default=False, verbose_name='Tennis Court')
    facility_turkish_hamam = models.BooleanField(default=False, verbose_name='Turkish Hamam')
    facility_shuttle_beach = models.BooleanField(default=False, verbose_name='Shuttle to the beach')
    facility_children_swimming_pool = models.BooleanField(default=False, verbose_name='Children Swimming Pool')
    facility_video_surveillance = models.BooleanField(default=False, verbose_name='Video Surveillance 24/7')
    facility_basketball_playground = models.BooleanField(default=False, verbose_name='Basketball Playground')
    facility_rest_and_bbg_areas = models.BooleanField(default=False, verbose_name='Rest and BBQ Areas')

    facility_lift = models.BooleanField(default=False, verbose_name='Lift')
    facility_terras = models.BooleanField(default=False, verbose_name='Terras')
    otherview_content = RichTextField()
    publishing_date = models.DateTimeField(auto_now=True)

    video = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=False)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=False)

    promote_panels = SEOPage.promote_panels

    content_panels = SEOPage.content_panels + [
        FieldPanel("banner_image"),
        LocalizedSelectPanel('property_category'),
        LocalizedSelectPanel('property_type'),
        LocalizedSelectPanel('property_region'),
        LocalizedSelectPanel('short_description_offer'),
        LocalizedSelectPanel('property_tags'),

        FieldPanel('general_cost'),
        FieldPanel('general_cost_second'),
        FieldPanel('discounted_cost'),
        FieldPanel('discounted_cost_second'),
        FieldPanel('hot_deals'),

        FieldPanel('area'),
        FieldPanel('area_2'),
        FieldPanel('is_sold'),

        FieldPanel('first_image'),
        FieldPanel('image_2'),
        FieldPanel('image_3'),
        FieldPanel('image_4'),

        MultiFieldPanel(
            [
                InlinePanel(
                    "additional_images",
                    label="Additional Images",
                ), ], heading="Additional Images",),

        MultiFieldPanel(
            [
                InlinePanel(
                    "advertisement_carusel_images",
                    label="Advertisement Carusel Images",
                ), ], heading="Advertisement Carusel Images",),

        FieldPanel('existence_in_homepage'),
        FieldPanel('short_description_floor'),
        FieldPanel('short_description_gross_area'),

        LocalizedSelectPanel('short_description_rooms'),

        FieldPanel('short_description_furniture'),
        FieldPanel('short_description_sea_view'),
        FieldPanel('short_description_to_the_sea'),
        FieldPanel('short_description_to_the_center'),
        FieldPanel('short_description_to_the_airport'),
        FieldPanel('short_description_year'),

        FieldPanel('facility_open_pool'),
        FieldPanel('facility_children_swimming_pool'),
        FieldPanel('facility_green_garden'),
        FieldPanel('facility_wireless_internet'),
        FieldPanel('facility_satellite_tv'),
        FieldPanel('facility_concierge'),
        FieldPanel('facility_outdoor_parking'),
        FieldPanel('facility_power_generator'),
        FieldPanel('facility_finnish_sauna'),
        FieldPanel('facility_playground'),
        FieldPanel('facility_video_surveillance'),
        FieldPanel('facility_fitness_centre'),
        FieldPanel('facility_game_room'),
        FieldPanel('facility_gazebos_for_rest'),
        FieldPanel('facility_covered_parking'),
        FieldPanel('facility_rest_and_bbg_areas'),
        FieldPanel('facility_aquapark'),
        FieldPanel('facility_amphitheater'),
        FieldPanel('facility_pool_bar'),
        FieldPanel('facility_billiards'),
        FieldPanel('facility_bowling'),
        FieldPanel('facility_jacuzzi'),
        FieldPanel('facility_indoor_pool'),
        FieldPanel('facility_cafe_restaurant'),
        FieldPanel('facility_cinema'),
        FieldPanel('facility_conference_hall'),
        FieldPanel('facility_24_hour_security'),
        FieldPanel('facility_ice_rink'),
        FieldPanel('facility_market'),
        FieldPanel('facility_massage_rooms'),
        FieldPanel('facility_mini_club'),
        FieldPanel('facility_table_tennis'),
        FieldPanel('facility_barbershop'),
        FieldPanel('facility_walking_paths'),
        FieldPanel('facility_roman_steam_room'),
        FieldPanel('facility_private_beach'),
        FieldPanel('facility_tennis_court'),
        FieldPanel('facility_turkish_hamam'),
        FieldPanel('facility_shuttle_beach'),
        FieldPanel('facility_basketball_playground'),
        FieldPanel('facility_lift'),
        FieldPanel('facility_terras'),

        FieldPanel('otherview_content'),
        FieldPanel('video'),
        FieldPanel('longitude'),
        FieldPanel('latitude'),
    ]

    translatable_fields = [
        TranslatableField("title"),
        TranslatableField("otherview_content"),
        SynchronizedField("slug"),

    ]

    api_fields = SEOPage.api_fields + [
        APIField('slug2'),
        APIField('banner_image', CustomImageSerializer(source='get_banner_image')),
        APIField('advertisement_carusel_images', MultipleImageSerializer(source='get_advertisement_carusel_images')),

        APIField('fullpath', FullPathSerializer(source='get_full_path')),
        APIField('child_pages', ChildPageSerializer(source='get_child_pages')),   
        APIField("property_categories", CategoryListSerializer(source='get_property_categories')),
        APIField("property_type", PropertyDetailForeingkey2FieldSerializer(source='get_property_type')),
#        APIField("property_type"),
 
        APIField("property_city", 
                 PropertyDetailForeingkey2FieldSerializer(source='get_property_city')),

        APIField('property_tags', CategoryListSerializer(source='get_property_tags')),
        APIField("property_region", PropertyDetailForeingkey2FieldSerializer(source='get_property_region')),
        APIField("general_cost"),
        APIField("general_cost_second"),
        APIField("discounted_cost"),
        APIField("discounted_cost_second"),
        APIField('hot_deals'),

        APIField("area"),
        APIField('area_2'),
        APIField("is_sold"),
        APIField("first_image", CustomImageSerializer(source='get_first_image')),
        APIField("image_2", CustomImageSerializer(source='get_image_2')),
        APIField("image_3", CustomImageSerializer(source='get_image_3')),
        APIField("image_4", CustomImageSerializer(source='get_image_4')),

        APIField("additional_images", MultipleImageSerializer(source='get_additional_images')),
        APIField("custom_id", CustomIdSerializer(source='get_custom_id')),
        APIField('existence_in_homepage'),
        APIField('short_description_floor'),
        APIField('short_description_gross_area'),
        APIField('short_description_rooms', HomeRoomSerialzer(source='get_short_description_rooms')),
        APIField('short_description_furniture'),
        APIField('short_description_sea_view'),
        APIField('short_description_to_the_sea'),
        APIField('short_description_to_the_center'),
        APIField('short_description_to_the_airport'),
        APIField('short_description_year'),
        APIField('short_description_offer', 
                 PropertyOffererSerializer(source='get_offerer_person')),

        APIField('facility_open_pool'),
        APIField('facility_children_swimming_pool'),
        APIField('facility_green_garden'),
        APIField('facility_wireless_internet'),
        APIField('facility_satellite_tv'),
        APIField('facility_concierge'),
        APIField('facility_outdoor_parking'),
        APIField('facility_power_generator'),
        APIField('facility_finnish_sauna'),
        APIField('facility_playground'),
        APIField('facility_video_surveillance'),
        APIField('facility_fitness_centre'),
        APIField('facility_game_room'),
        APIField('facility_gazebos_for_rest'),
        APIField('facility_covered_parking'),
        APIField('facility_rest_and_bbg_areas'),
        APIField('facility_aquapark'),
        APIField('facility_amphitheater'),
        APIField('facility_pool_bar'),
        APIField('facility_billiards'),
        APIField('facility_bowling'),
        APIField('facility_jacuzzi'),
        APIField('facility_indoor_pool'),
        APIField('facility_cafe_restaurant'),
        APIField('facility_cinema'),
        APIField('facility_conference_hall'),
        APIField('facility_24_hour_security'),
        APIField('facility_ice_rink'),
        APIField('facility_market'),
        APIField('facility_massage_rooms'),
        APIField('facility_mini_club'),
        APIField('facility_table_tennis'),
        APIField('facility_barbershop'),
        APIField('facility_walking_paths'),
        APIField('facility_roman_steam_room'),
        APIField('facility_private_beach'),
        APIField('facility_tennis_court'),
        APIField('facility_turkish_hamam'),
        APIField('facility_shuttle_beach'),
        APIField('facility_basketball_playground'),
        APIField('facility_lift'),
        APIField('facility_terras'),

        APIField('otherview_content'),
        APIField('video'),
        APIField('longitude'),
        APIField('latitude'),
        APIField('publishing_date'),

        APIField('similar_properties_for_geo', 
                 SimilarPropertyDetailSerializer(source='get_similar_property_for_geo')),

        APIField('similar_property_for_cost', 
                 SimilarPropertyDetailSerializer(source='get_similar_property_for_cost')),

        APIField("seo_title"),
        APIField("search_image", SearchImageSerializer(source='get_search_image')),
        APIField("search_description"),
    ]

    def get_custom_id(self):
        return self.slug2
    

    def get_property_categories(self):
        translated_obj_list = []
        base_page = PropertyDetailPage.objects.filter(locale__language_code=wcl[0][0], slug2=self.slug2).first()

        for obj in base_page.property_category.all():
            if self.locale.language_code==wcl[0][0]:
                data = obj
            else:
                if obj.get_translation_or_none(self.locale.id):
                    data = obj.get_translation_or_none(self.locale.id)
                else:
                    data = {
                        'slug2': obj.slug2,
                        'locale': self.locale.language_code,
                        'message': """There is not translation for object that slug2=={}, locale=={}"""\
                                        .format(obj.slug2, self.locale.id),
                        }
            translated_obj_list.append(data)
        return translated_obj_list




#because it related with manytomanyfield    
    def get_property_tags(self):
        translated_obj_list = []
        base_page = PropertyDetailPage.objects.filter(locale__language_code=wcl[0][0], slug2=self.slug2).first()

        for obj in base_page.property_tags.all():
            if self.locale.language_code==wcl[0][0]:
                data = obj
            else:
                if obj.get_translation_or_none(self.locale.id):
                    data = obj.get_translation_or_none(self.locale.id)
                else:
                    data = {
                        'slug2': obj.slug2,
                        'locale': self.locale.language_code,
                        'message': """There is not translation for object that slug2=={}, locale=={}"""\
                                        .format(obj.slug2, self.locale.id),
                        }
            translated_obj_list.append(data)
        return translated_obj_list

    
##because it related with manytomanyfield    
    def get_short_description_rooms(self):
        translated_obj_list = []
        base_page = PropertyDetailPage.objects.filter(locale__language_code=wcl[0][0], slug2=self.slug2).first()

        for obj in base_page.short_description_rooms.all():
            if self.locale.language_code==wcl[0][0]:
                data = obj
            else:
                if obj.get_translation_or_none(self.locale.id):
                    data = obj.get_translation_or_none(self.locale.id)
                else:
                    data = {
                        'slug2': obj.slug2,
                        'locale': self.locale.language_code,
                        'message': """There is not translation for object that slug2=={}, locale=={}"""\
                                        .format(obj.slug2, self.locale.id),
                        }
            translated_obj_list.append(data)
        return translated_obj_list


    def get_property_type(self):
        base_page = PropertyDetailPage.objects.filter(locale__language_code=wcl[0][0], slug2=self.slug2).first()
        foreingkey_field = base_page.property_type

        if self.locale.language_code==wcl[0][0]:
            data = foreingkey_field if base_page.property_type else None 
        else:
            if foreingkey_field.get_translation_or_none(self.locale.id):
                data = foreingkey_field.get_translation_or_none(self.locale.id)
            else:
                data = {
                    'locale': self.locale.language_code,
                    'slug2': foreingkey_field.slug2,
                    'message': """There is not translation for object that slug2=={}, locale=={}"""\
                                        .format(foreingkey_field.slug2, self.locale.id),
                }
        return data

    

    def get_property_region(self):
        base_page = PropertyDetailPage.objects.filter(locale__language_code=wcl[0][0], slug2=self.slug2).first()
        foreingkey_field = base_page.property_region

        if self.locale.language_code==wcl[0][0]:
            data = foreingkey_field if base_page.property_region else None 
        else:
            if foreingkey_field.get_translation_or_none(self.locale.id):
                data = foreingkey_field.get_translation_or_none(self.locale.id)
            else:
                data = {
                    'locale': self.locale.language_code,
                    'slug2': foreingkey_field.slug2,
                    'message': """There is not translation for object that slug2=={}, locale=={}"""\
                                        .format(foreingkey_field.slug2, self.locale.id),
                }
        return data

    def get_property_city(self):
        base_page = PropertyDetailPage.objects.filter(locale__language_code=wcl[0][0], slug2=self.slug2).first()
        foreingkey_field = base_page.property_region.city_rel

        if self.locale.language_code==wcl[0][0]:
            data = foreingkey_field if base_page.property_region else None 
        else:
            if foreingkey_field.get_translation_or_none(self.locale.id):
                data = foreingkey_field.get_translation_or_none(self.locale.id)
            else:
                data = {
                    'locale': self.locale.language_code,
                    'slug2': foreingkey_field.slug2,
                    'message': """There is not translation for object that slug2=={}, locale=={}"""\
                                        .format(foreingkey_field.slug2, self.locale.id),
                }
        return data



    def get_offerer_person(self):
        base_page = PropertyDetailPage.objects.filter(locale__language_code=wcl[0][0], slug2=self.slug2).first()
        foreingkey_field = base_page.short_description_offer

        if self.locale.language_code==wcl[0][0]:
            data = foreingkey_field if base_page.short_description_offer else None 
        else:
            if foreingkey_field.get_translation_or_none(self.locale.id):
                data = foreingkey_field.get_translation_or_none(self.locale.id)
            else:
                data = {
                    'locale': self.locale.language_code,
                    'slug2': foreingkey_field.slug2,
                    'message': """There is not translation for object that slug2=={}, locale=={}"""\
                                        .format(foreingkey_field.slug2, self.locale.id),
                }
        return data


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
    
    def get_image_2(self):
        return self.image_2 if self.image_2 else None

    def get_image_3(self):
        return self.image_3 if self.image_3 else None

    def get_image_4(self):
        return self.image_4 if self.image_4 else None

    
    def get_additional_images(self):
        result = None
        if self.additional_images:
            extra__img_obj = self.additional_images.all().select_related('image')
            result = [image.image for image in extra__img_obj]
        return result

    def get_advertisement_carusel_images(self):
        result = None
        general_carusel_obj = AllImages.objects.first()
        special_carusel_obj =  self.advertisement_carusel_images.all().select_related('image')
        special_carusel = [image.image for image in special_carusel_obj]
        if len(special_carusel) > 0:
            result = special_carusel
        else:
            if general_carusel_obj:
                result = general_carusel_obj.carusel_images.all()
        return result

    def get_full_path(self):
        parent = self.get_parent()
        grandpa = parent.get_parent()
        return (grandpa.title, parent.title, self.title)

    def get_child_pages(self):
        return self.get_children().live() if self.get_children().live() else None

    def get_search_image(self):
        return self.search_image
    
    def get_all_cities(self):
        my_queryset = City.objects.filter(locale__language_code=self.locale.language_code)
        return my_queryset if my_queryset else None
    
    def get_all_types(self):
        my_queryset = Type.objects.filter(locale__language_code=self.locale.language_code)
        return my_queryset if my_queryset else None
    
    def get_similar_property_for_geo(self):
        result = None
        
        region_equal = PropertyDetailPage.objects.filter(locale__language_code=self.locale.language_code,
                                                        property_region=self.property_region, live=True)\
                                                        .exclude(slug2=self.slug2).order_by('-publishing_date')

        if len(region_equal) > 4:
            result = region_equal[:4]
        elif 4 < len(region_equal) > 0:
            result = region_equal
        return result

        
    def get_unit_discounted_cost(self):
        result = None
        if self.discounted_cost and self.discounted_cost_second is None:
            result = round((self.discounted_cost / self.area), 2)
        elif self.discounted_cost and self.discounted_cost_second:
            result = [round(self.discounted_cost / self.area, 2),
                      round(self.discounted_cost_second / self.area, 2)] 
        return result
    
    def get_unit_cost(self):
        result = None
        if self.general_cost and self.general_cost_second is None:
            result = round((self.general_cost/self.area), 2)
        elif self.general_cost and self.general_cost_second:
            result = [round(self.general_cost/self.area, 2),
                      round(self.general_cost_second/self.area,2)]
        return result
    
    def get_similar_property_for_cost(self):
        result = None
        
        cost_equal = PropertyDetailPage.objects.filter(locale__language_code=self.locale.language_code,
                                                        general_cost=self.general_cost, live=True)\
                                                        .exclude(slug2=self.slug2).order_by('-publishing_date')
        
        if len(cost_equal) < 4:
            result = cost_equal[:4]
        else:
            indeks = 4-len(cost_equal)
            cost_similar = PropertyDetailPage.objects.filter(locale__language_code=self.locale.language_code,
                                                            general_cost__gte=self.general_cost*0.95, live=True,
                                                            general_cost__lte=self.general_cost*1.05)\
                                                            .exclude(slug2=self.slug2)\
                                                            .order_by('publishing_date')[:indeks]
            result = cost_equal + cost_similar
        return result



    def save(self, *args, **kwargs):

#        if self.discounted_cost is None:
#            self.discounted_cost = self.general_cost
#
#        # Check if discounted_cost_second is not provided, then set it to general_cost_second
#        if self.discounted_cost_second is None:
#            self.discounted_cost_second = self.general_cost_second


        if not self.slug2:
            #my data is classname of the page, which was generated from django_model content_type
            my_data = (str(self.content_type)).split("|")[1].strip().replace(" ", "").lower()
            base_slug = slugify(my_data)  
            existing_slugs = PropertyDetailPage.objects.filter\
                                            (locale=self.locale).values_list('slug2', flat=True)
            
            count = 1
            new_slug = base_slug

            while new_slug in existing_slugs:
                count += 1
                new_slug = f"{base_slug}-{count}"

            self.slug2 = new_slug

        super().save(*args, **kwargs)




    