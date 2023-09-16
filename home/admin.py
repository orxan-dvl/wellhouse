from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from home.forms import HelpForPropertyChoiceForm, AskQuestionForm, AskCallForm


#
class HelpForPropertyChoiceFormAdmin(ModelAdmin):
    model = HelpForPropertyChoiceForm
    menu_label = " HelpForPropertyChoiceForm"
    menu_icon = "mail"
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True

modeladmin_register(HelpForPropertyChoiceFormAdmin)

#
class AskQuestionFormAdmin(ModelAdmin):
    model = AskQuestionForm
    menu_label = " AskQuestionForm"
    menu_icon = "mail"
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True

modeladmin_register(AskQuestionFormAdmin)


#
class AskCallFormAdmin(ModelAdmin):
    model = AskCallForm
    menu_label = " AskCall"
    menu_icon = "mail"
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True

modeladmin_register(AskCallFormAdmin)
