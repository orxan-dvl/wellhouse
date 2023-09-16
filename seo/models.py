from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _
from wagtail.api import APIField
from wagtail.search import index
from wagtailmetadata.models import WagtailImageMetadataMixin

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page, Locale, Site

# from seo.serializers import CanonicalSerializer

def get_image_model_string():
    try:
        image_model = settings.WAGTAILIMAGES_IMAGE_MODEL
    except AttributeError:
        image_model = 'wagtailimages.Image'
    return image_model


class SEOPageMixin(WagtailImageMetadataMixin, models.Model):
    search_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL,
        verbose_name=_('Search Image'),
        help_text=_(
            "The image to use on previews of this page on external links and search results. This will also be the image used for blog posts on the index pages.")
    )

    summary = models.TextField(
        null=True,
        blank=True,
        help_text=_(
            "A summary of the page to be used on index pages. If Meta Description is left blank, this text will be used on search results and link previews.")
    )

    search_engine_index = models.BooleanField(
        null=True,
        blank=True,
        default=True,
        verbose_name=_("Allow search engines to index this page?")
    )

    search_engine_changefreq = models.CharField(
        max_length=25,
        choices=[
            ("always", _("Always")),
            ("hourly", _("Hourly")),
            ("daily", _("Daily")),
            ("weekly", _("Weekly")),
            ("monthly", _("Monthly")),
            ("yearly", _("Yearly")),
            ("never", _("Never")),
        ],
        blank=True,
        null=True,
        verbose_name=_("Search Engine Change Frequency (Optional)"),
        help_text=_("How frequently the page is likely to change? (Leave blank for default)")
    )

    search_engine_priority = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        blank=True,
        null=True,
        verbose_name=_("Search Engine Priority (Optional)"),
        help_text=_(
            "The priority of this URL relative to other URLs on your site. Valid values range from 0.0 to 1.0. (Leave blank for default)")
    )
    #slug2 = models.SlugField(max_length=255)
    content_panels = Page.content_panels + [
    ]
    api_fields = [
        # APIField("canonical_url", serializer=CanonicalSerializer(source="get_canonical_urls")),
    ]
    promote_panels = Page.promote_panels + [
        # MultiFieldPanel([
        #     FieldPanel('slug'),
        #     FieldPanel('search_image'),
        #     FieldPanel('seo_title'),
        #     FieldPanel('search_description'),
        #     FieldPanel('show_in_menus'),
        # ], _('SEO page configuration')),
        FieldPanel('search_image'),
        MultiFieldPanel([
            FieldPanel('search_engine_index'),
            FieldPanel('search_engine_changefreq'),
            FieldPanel('search_engine_priority'),
        ], _("Search Engine Indexing")),
    ]

    def get_meta_url(self):
        return self.full_url

    def get_meta_title(self):
        return self.seo_title or self.title

    def get_meta_description(self):
        return self.search_description or self.summary

    def get_meta_image(self):
        return self.search_image

    def detail_url(self, *args, **kwargs):
        return f'http://{Site.objects.filter(is_default_site=True).last().hostname}/api/v2/{self.slug2}/'

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        errors = {}

        len_search_title = len(self.seo_title or self.title)
        if len_search_title < 15 or len_search_title > 70:
            if len_search_title == 0:
                msg = _("empty")
            else:
                msg = _(f"{len_search_title} character{'s' * bool(len_search_title > 1)}")
            if self.seo_title:
                errors['seo_title'] = ErrorList(
                    [_(f'Title tag is {msg}. It should be between 15 and 70 characters for optimum SEO.')])
            else:
                errors['seo_title'] = ErrorList(
                    [_(f'Page title is {msg}. Create a title tag between 15 and 70 characters for optimum SEO.')])

        len_search_description = len(self.search_description)
        if len_search_description < 50 or len_search_description > 160:
            if len_search_description == 0:
                msg = _("empty")
            else:
                msg = _(f"{len_search_description} character{'s' * bool(len_search_description > 1)}")
            if self.search_description:
                errors['search_description'] = ErrorList(
                    [_(f'Meta Description is {msg}. It should be between 50 and 160 characters for optimum SEO.')])
            else:
                errors['search_description'] = ErrorList(
                    [_(f'Summary is {msg}. Create a meta description between 50 and 160 characters for optimum SEO.')])

        # if errors:
        #     raise ValidationError(errors)

    @property
    def lastmod(self):
        return self.last_published_at or self.latest_revision_created_at


    # def get_canonical_urls(self):
    #
    #     hostname = Site.objects.filter(is_default_site=False).last().hostname
    #     path = self.get_url_parts()[2]
    #
    #     full_path = f'https://{hostname}{path}'
    #
    #     trans_pages = self.get_translations(inclusive=True)
    #     if trans_pages.count() > 1:
    #         alt = []
    #         for page in trans_pages:
    #
    #             alt.append({
    #                 'lang_code': page.locale.language_code,
    #                 'location': page.get_custom_full_url()
    #             })
    #
    #     return {
    #         "full_path": full_path,
    #         "alternates": alt
    #     }


    def get_custom_full_url(self):
        #print("saytlar: ",Site.objects.all())
        hostname = Site.objects.filter(is_default_site=False).last().hostname
        path =  self.get_url_parts()[2]

        return f'https://{hostname}{path}'
    def get_sitemap_urls(self, request):
        if self.search_engine_index:

            url_item = {
                "location": self.get_custom_full_url(),
                "lastmod": self.lastmod,
                "alternates": self.get_alternates()
            }
            if self.search_engine_changefreq:
                url_item["changefreq"] = self.search_engine_changefreq
            if self.search_engine_priority:
                url_item["priority"] = self.search_engine_priority

            return url_item
        else:
            return []

    def get_alternates(self):
        # default_locale = Locale.get_default()
        # x_default = None

        trans_pages = self.get_translations(inclusive=True)
        if trans_pages.count() > 1:
            alt = []
            for page in trans_pages:

                alt.append({
                    'lang_code': page.locale.language_code,
                    'location': page.get_custom_full_url()
                })


            #     if page.locale == default_locale:
            #         x_default = page.get_url_parts()
            #
            # if not x_default:  # page not translated to default language, use first trans_page instead
            #     x_default = trans_pages.first().get_url_parts()

            # x-default - strip the language component from the url for the default-lang page
            # https://example.com/en/something/ -> https://example.com/something/
            # x_default = f"{x_default[1]}/{'/'.join(x_default[2].split('/')[2:])}"
            # alt.append({'lang_code': 'x-default', 'location': x_default})

            return alt
        else:
            return None




class SEOPage(SEOPageMixin, Page):

    search_fields = Page.search_fields + [
    ]
    class Meta:
        abstract = True
