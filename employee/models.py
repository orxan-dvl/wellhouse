from django.db import models
from django.utils.text import slugify

from wagtail.models import TranslatableMixin, Orderable
from wagtail.admin.panels import FieldPanel

from wellhouse.custom_localize_field import LocalizedSelectPanel


#
class Profession(Orderable, TranslatableMixin, models.Model):

    class Meta:
        verbose_name = 'Employee Profession'
        verbose_name_plural = 'Employee Professions'
        unique_together = ('translation_key', 'locale')

    profession = models.CharField(max_length=255, null=True, blank=False)
    slug2 = models.SlugField(max_length=255, editable=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return "{}".format(self.profession)
    
    def save(self, *args, **kwargs):
        if not self.slug2:
            # my_data is classname of the page, which was generated from classname
            my_data = (str(self.__class__)).replace('<class', '').replace('>', '').replace("'", "").replace(" ", "") \
                                                .replace(".models", "").lower().replace(".", "_")

            base_slug = slugify(my_data)
            existing_slugs = Profession.objects.filter(locale=self.locale).union\
                                                (Profession.objects.filter(locale=self.locale))\
                                                    .values_list('slug2', flat=True)
            count = 1
            new_slug = base_slug
            while new_slug in existing_slugs:
                count += 1
                new_slug = f"{base_slug}-{count}"
            self.slug2 = new_slug

        super().save(*args, **kwargs)


#
class Languages(Orderable, TranslatableMixin, models.Model):

    class Meta:
        verbose_name = 'Employee Language'
        verbose_name_plural = 'Employee Languages'
        unique_together = ('translation_key', 'locale')

    language_name = models.CharField(max_length=255, null=True, blank=False)
    slug2 = models.SlugField(max_length=255, editable=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.language_name)

    def save(self, *args, **kwargs):
        if not self.slug2:
            # my_data is classname of the page, which was generated from classname
            my_data = (str(self.__class__)).replace('<class', '').replace('>', '').replace("'", "").replace(" ", "") \
                                                .replace(".models", "").lower().replace(".", "_")

            base_slug = slugify(my_data)
            existing_slugs = Languages.objects.filter(locale=self.locale).union\
                                                (Languages.objects.filter(locale=self.locale))\
                                                    .values_list('slug2', flat=True)
            count = 1
            new_slug = base_slug
            while new_slug in existing_slugs:
                count += 1
                new_slug = f"{base_slug}-{count}"
            self.slug2 = new_slug

        super().save(*args, **kwargs)



#
class Employee(Orderable, TranslatableMixin, models.Model):

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        unique_together = ('translation_key', 'locale')

    slug2 = models.SlugField(max_length=255, editable=False, null=False)
    fullname = models.CharField(max_length=255, null=True, blank=False)
    profession = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=False)
    email = models.EmailField()
    image = models.ForeignKey("wagtailimages.Image", null=True, blank=True,
                                on_delete=models.SET_NULL, related_name="+",
                                verbose_name="Image")

    languages_spoken = models.ManyToManyField(Languages, blank=False,
                                                related_name='employees_languages_spoken')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    panels = [
        FieldPanel("fullname"),
        LocalizedSelectPanel("profession"),
        FieldPanel("phone_number"),
        FieldPanel("email"),
        FieldPanel("image"),
        LocalizedSelectPanel("languages_spoken"),
    ]

    def __str__(self):
        return "{}".format(self.fullname)

    def save(self, *args, **kwargs):
        if not self.slug2:
            # my_data is classname of the page, which was generated from classname
            my_data = (str(self.__class__)).replace('<class', '').replace('>', '').replace("'", "").replace(" ", "") \
                                                .replace(".models", "").lower().replace(".", "_")

            base_slug = slugify(my_data)
            existing_slugs = Employee.objects.filter(locale=self.locale).union\
                                                (Employee.objects.filter(locale=self.locale))\
                                                    .values_list('slug2', flat=True)
            count = 1
            new_slug = base_slug
            while new_slug in existing_slugs:
                count += 1
                new_slug = f"{base_slug}-{count}"
            self.slug2 = new_slug

        super().save(*args, **kwargs)
