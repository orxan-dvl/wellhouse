import json
from datetime import datetime

from django.template.response import TemplateResponse
from django.utils.http import http_date
from rest_framework.decorators import api_view
from wagtail.models import Page, Site

from wellhouse.settings.base import BASE_DIR


@api_view(('GET',))
def sitemap(request):
    site = Site.find_for_request(request)
    root_page = Page.objects.defer_streamfields().get(id=site.root_page_id)

    urlset = []
    for locale_home in root_page.get_translations(inclusive=True).defer_streamfields().live().public().specific():
        urlset.append(locale_home.get_sitemap_urls(request))
        for child_page in locale_home.get_descendants().defer_streamfields().live().public().specific():
            urlset.append(child_page.get_sitemap_urls(request))
    try:
        urlset.remove([])
    except:
        pass
    try:
        last_modified = max([x[0]['lastmod'] if type(x) == list else x['lastmod'] for x in urlset])

    except Exception as e:
        # either urlset is empty or lastmod fields not present, set last modified to now
        print(f"\n{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}\n")
        last_modified = datetime.now()

    # return Response(data={
    #     "urlset": urlset,
    #     "last_modified": last_modified,
    # }, status=status.HTTP_200_OK)

    return TemplateResponse(
        request,
        template=f'{BASE_DIR}/seo/templates/sitemap.xml',
        context={'urlset': urlset},
        content_type='application/xml',
        headers={
            "X-Robots-Tag": "noindex, noodp, noarchive",
            "last-modified": http_date(last_modified.timestamp()),
            "vary": "Accept-Encoding",
            }
        )