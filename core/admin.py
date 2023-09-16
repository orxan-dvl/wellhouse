from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from core.models import AllImages

#
class AllImagesAdmin(ModelAdmin):
    model = AllImages
    menu_label = " AllImages"
    menu_icon = "image"
    list_display = ("id",)
    list_filter = ("id",)
    search_fields = ("id",)
    inspect_view_enabled = True

modeladmin_register(AllImagesAdmin)