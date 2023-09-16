from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from services.forms import (PostSaleServiceForm, OrientationForm, OnlineVisitForm, ConsultingForm,
                            SellPropertyForm, ApartmentExchangeForm)

# Register your models here.

class PostSaleServiceFormAdmin(ModelAdmin):
    model = PostSaleServiceForm
    menu_label = " PostSaleServiceForm"  # ditch this to use verbose_name_plural from model
    menu_icon = "mail"  # change as required
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True

modeladmin_register(PostSaleServiceFormAdmin)

#
class OrientationFormAdmin(ModelAdmin):
    model = OrientationForm
    menu_label = "OrientationForm"  
    menu_icon = "mail"  
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True

modeladmin_register(OrientationFormAdmin)


#
class OnlineVisitFormAdmin(ModelAdmin):
    model = OnlineVisitForm
    menu_label = "OnlineVisitPageForm"  
    menu_icon = "mail"  
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True

modeladmin_register(OnlineVisitFormAdmin)


#
class SellPropertyFormAdmin(ModelAdmin):
    model = SellPropertyForm
    menu_label = "SellPropertyForm"  
    menu_icon = "mail"  
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True

modeladmin_register(SellPropertyFormAdmin)



#
class ConsultingFormAdmin(ModelAdmin):
    model = ConsultingForm
    menu_label = "ConsultingForm"  
    menu_icon = "mail"  
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True

modeladmin_register(ConsultingFormAdmin)


#
class ApartmentExchangeFormAdmin(ModelAdmin):
    model = ApartmentExchangeForm
    menu_label = "ApartmentExchangeForm"  
    menu_icon = "mail"  
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True

modeladmin_register(ApartmentExchangeFormAdmin)

