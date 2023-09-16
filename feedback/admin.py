from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from feedback.forms import Feedback

#
class FeedbackAdmin(ModelAdmin):
    model = Feedback
    menu_label = " FeedbackForm"
    menu_icon = "comment"
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    inspect_view_enabled = True

modeladmin_register(FeedbackAdmin)
