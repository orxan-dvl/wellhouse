from django.core.validators import RegexValidator
from django.forms.widgets import TextInput

from wagtail.core.blocks import CharBlock


#
phone_number_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


#
class PhoneNumberBlock(CharBlock):
    def __init__(self, required=True, help_text=None, validators=(), **kwargs):
        all_validators = [phone_number_validator]
        all_validators.extend(validators)
        super().__init__(
            required=required,
            help_text=help_text,
            validators=all_validators,
            widget=TextInput(attrs={'pattern': r'^\+?[\d-]+$', 'title': "Enter a valid phone number."}),
            **kwargs
        )
