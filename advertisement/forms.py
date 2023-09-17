from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from wagtail.models import Orderable, TranslatableMixin

#
class PropertyRequestTypes(Orderable, TranslatableMixin, models.Model):

    class Meta:
        verbose_name = 'PropertyRequestType'
        unique_together = ('translation_key', 'locale')

    name = models.CharField(max_length=50, null=True, blank=False, unique=True)
    slug2 = models.SlugField(max_length=255, editable=False, null=False)


    def __str__(self):
        return '{}'.format(self.name)
    
    def save(self, *args, **kwargs):
        if not self.slug2:
            # my_data is classname of the page, which was generated from classname
            my_data = (str(self.__class__)).replace('<class', '').replace('>', '').replace("'", "").replace(" ", "") \
                                                .replace(".models", "").lower().replace(".", "_")

            base_slug = slugify(my_data)
            existing_slugs = PropertyRequestTypes.objects.filter(locale=self.locale).union\
                                                (PropertyRequestTypes.objects.filter(locale=self.locale))\
                                                    .values_list('slug2', flat=True)
            count = 1
            new_slug = base_slug
            while new_slug in existing_slugs:
                count += 1
                new_slug = f"{base_slug}-{count}"
            self.slug2 = new_slug

        super().save(*args, **kwargs)
 

#
class PropertyDetailForm(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    surname = models.CharField(max_length=255, null=True, blank=False)
    phone_number = models.CharField(max_length=17, null=True, blank=False)
    email = models.EmailField(null=True, blank=False)
    #request_choices = models.ForeignKey('advertisement.PropertyRequestTypes', on_delete=models.SET_NULL,
    #                                    null=True, blank=False)
    
    message = models.TextField()
    property_slug2 = models.CharField(max_length=255, null=True, blank=False)
    property_locale = models.CharField(max_length=255, null=True, blank=False)
    property_custom_id = models.CharField(max_length=255, null=True, blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    has_been_read = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.id)
    

class PropertyDetailOnlineVisitForm(models.Model):
    name = models.CharField(max_length=255, null=True, blank=False)
    surname = models.CharField(max_length=255, null=True, blank=False)
    phone_number = models.CharField(max_length=17, null=True, blank=False)
    email = models.EmailField(null=True, blank=False)
#altdaki 3 fieldi front avtomatik tutub vermelidi
    property_custom_id = models.CharField(max_length=255, null=True, blank=False)
    property_slug2 = models.CharField(max_length=255, null=True, blank=False)
    property_locale = models.CharField(max_length=255, null=True, blank=False)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    has_been_read = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.id)

#PropertyOrientationTourForm is the same with PropertyDetailOnlineVisitForm
