from wagtail.contrib.modeladmin.options import modeladmin_register, ModelAdmin
from wagtail_localize.modeladmin.options import TranslatableModelAdmin

from wagtail_localize.modeladmin.options import TranslatableCreateView
from wagtail.contrib.modeladmin.views import CreateView


from employee.models import Languages, Employee, Profession

#



class ProfessionAdmin(TranslatableModelAdmin):

    model = Profession
    menu_label = " Professions"
    menu_icon = "user"
    list_display = ("profession",)
    list_filter = ("profession",)
    search_fields = ("profession",)
    inspect_view_enabled = True

    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        if request.method == 'GET' and 'add' in perms:
            default_locale = self.model.get_default_locale()
            if request.LANGUAGE_CODE != default_locale:
                perms['add'] = False
        return perms


modeladmin_register(ProfessionAdmin)


#
class EmployeeLanguagesAdmin(TranslatableModelAdmin):
    model = Languages
    menu_label = " Employee Languages"
    menu_icon = "user"
    list_display = ("language_name",)
    list_filter = ("language_name",)
    search_fields = ("language_name",)
    inspect_view_enabled = True

modeladmin_register(EmployeeLanguagesAdmin)


#
class EmployeeAdmin(TranslatableModelAdmin):
    model = Employee
    menu_label = " Employee"
    menu_icon = "user"
    list_display = ("fullname",)
    list_filter = ("fullname", "created_at", "profession", "languages_spoken")
    search_fields = ("fullname", "created_at", "profession", "languages_spoken")
    inspect_view_enabled = True

modeladmin_register(EmployeeAdmin)