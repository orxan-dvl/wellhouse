from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail_localize.modeladmin.options import TranslatableModelAdmin

from advertisement.models import Category, Type, Region, City, OffererPerson, Tags, Room
from advertisement.forms import PropertyDetailForm, PropertyRequestTypes, PropertyDetailOnlineVisitForm

from advertisement.utils import MyTranslatableCreateView


class RoomAdmin(TranslatableModelAdmin):

    model = Room
    menu_label = "Room"
    menu_icon = "tag"
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True
    create_view_class = MyTranslatableCreateView



modeladmin_register(RoomAdmin)


class CategoryAdmin(TranslatableModelAdmin):
    model = Category
    menu_label = "Categories"
    menu_icon = "tag"
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True
    create_view_class = MyTranslatableCreateView


modeladmin_register(CategoryAdmin)


#
class TypeAdmin(TranslatableModelAdmin):
    model = Type
    menu_label = " Types"
    menu_icon = "tag"
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True
    create_view_class = MyTranslatableCreateView


modeladmin_register(TypeAdmin)


#
class CityAdmin(TranslatableModelAdmin):
    model = City
    menu_label = " Cities"
    menu_icon = "globe"
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True
    create_view_class = MyTranslatableCreateView

modeladmin_register(CityAdmin)


#
class RegionAdmin(TranslatableModelAdmin):
    model = Region
    menu_label = " Regions"
    menu_icon = "globe"
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True
    create_view_class = MyTranslatableCreateView

modeladmin_register(RegionAdmin)



#
class OffererPersonAdmin(TranslatableModelAdmin):
    model = OffererPerson
    menu_label = " OffererPerson"
    menu_icon = "user"
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True
    create_view_class = MyTranslatableCreateView

modeladmin_register(OffererPersonAdmin)

#
class TagsAdmin(TranslatableModelAdmin):
    model = Tags
    menu_label = "Tags"
    menu_icon = "tag"
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True
    create_view_class = MyTranslatableCreateView

modeladmin_register(TagsAdmin)

#
class PropertyRequestTypesAdmin(TranslatableModelAdmin):
    model = PropertyRequestTypes
    menu_label = " PropertyRequestTypes"
    menu_icon = "cogs"
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True
    create_view_class = MyTranslatableCreateView

modeladmin_register(PropertyRequestTypesAdmin)


#
class PropertyDetailFormAdmin(ModelAdmin):
    model = PropertyDetailForm
    menu_label = "PropertyDetailForm"  
    menu_icon = "mail"  
    list_display = ("property_custom_id",)
    list_filter = ("property_custom_id", "name",)
    search_fields = ("name", "property_custom_id")
    inspect_view_enabled = True
    create_view_class = MyTranslatableCreateView

modeladmin_register(PropertyDetailFormAdmin)


#
class PropertyDetailOnlineVisitFormAdmin(ModelAdmin):
    model = PropertyDetailOnlineVisitForm
    menu_label = "PropertyDetailOnlineVisitForm"  
    menu_icon = "mail"  
    list_display = ("property_custom_id",)
    list_filter = ("property_custom_id", "name",)
    search_fields = ("name", "property_custom_id")
    inspect_view_enabled = True

modeladmin_register(PropertyDetailOnlineVisitFormAdmin)


