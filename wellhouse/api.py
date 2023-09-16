from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
from wagtail.api.v2.views import PagesAPIViewSet
from advertisement.filters import PropertyDetailPageListView
from core.base_api_controller import CustomPageViewSet

api_router = WagtailAPIRouter('wagtailapi')

# wagtail default api routers
api_router.register_endpoint('item',  PropertyDetailPageListView)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)
api_router.register_endpoint('pages', CustomPageViewSet)


