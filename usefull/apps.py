from django.apps import AppConfig


#
class UsefullConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usefull'

    def ready(self):
        import usefull.signals
