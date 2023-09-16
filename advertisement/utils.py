#from wagtail_localize.modeladmin.views import TranslatableViewMixin
#from wagtail.contrib.modeladmin.views import CreateView
#from wagtail.models import Locale
#
#class MyTranslatableCreateView(TranslatableViewMixin, CreateView):
#
#    def get(self, request, *args, **kwargs):
#        response = super().get(request, *args, **kwargs)
#        form = response.context_data['form']
#        
#        # Check if the current locale is the default language
#        default_language_code = 'tr'  # Replace with your default language code
#        if self.locale.language_code != default_language_code:
#            for field_name in form.fields:
#                form.fields[field_name].widget.attrs['readonly'] = True
#        
#        return response
#
#    def get_form_kwargs(self):
#        kwargs = super().get_form_kwargs()
#        kwargs["instance"].locale = self.locale
#        return kwargs
#
#    def get_success_url(self):
#        return self.index_url + "?locale=" + self.locale.language_code
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context["translations"] = [
#            {
#                "locale": locale,
#                "url": self.create_url + "?locale=" + locale.language_code,
#            }
#            for locale in Locale.objects.exclude(id=self.locale.id)
#        ]
#        return context
