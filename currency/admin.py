from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register


from currency.models import CurrencyModel

class CurrencyModelAdmin(ModelAdmin):
    model = CurrencyModel
    menu_label = "Currency"  
    menu_icon = "table"  
    list_display = ("updated_at",)
    list_filter = ("updated_at",)
    search_fields = ("updated_at")
    inspect_view_enabled = True

modeladmin_register(CurrencyModelAdmin)