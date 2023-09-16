from core.blocks import PhoneNumberBlock
from wagtail.images.blocks import ImageChooserBlock

from wagtail.core.blocks import StructBlock, CharBlock, EmailBlock, RichTextBlock, DecimalBlock

#
class OfficeBlock(StructBlock):
    office_name = CharBlock()
    address = RichTextBlock()
    working_hours = RichTextBlock()
    email = EmailBlock()
    phone_number = PhoneNumberBlock()
    skype_address = CharBlock()
    image = ImageChooserBlock()
    longitude = DecimalBlock(decimal_places=6)
    latitude = DecimalBlock(decimal_places=6)