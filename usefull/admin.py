from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from usefull.models import SubscriberForm

class SubscriberFormAdmin(ModelAdmin):
    model = SubscriberForm
    menu_label = "SubscriberForm"  
    menu_icon = "mail"  
    list_display = ("id",)
    list_filter = ("id", "email",)
    search_fields = ("email", "id")
    inspect_view_enabled = True

modeladmin_register(SubscriberFormAdmin)