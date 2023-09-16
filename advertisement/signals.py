from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import AppConfig
from django.utils.text import slugify
from advertisement.models import Type

#@receiver(post_migrate, sender=AppConfig)
#def create_initial_objects(sender, **kwargs):
#    # Check if the Type model already has objects, to avoid creating them again on each migration
#    if Type.objects.exists():
#        return
#
#    # Create the first two objects
#    obj1 = Type(name='Rent')
#    obj1.save()
#
#    obj2 = Type(name='by')
#    obj2.save()