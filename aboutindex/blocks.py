from wagtail.images.blocks import ImageChooserBlock
from wagtailsvg.blocks import SvgChooserBlock
from wagtail_color_panel.blocks import NativeColorBlock

from wagtail.core.blocks import (StructBlock, ListBlock, TextBlock, CharBlock,
                                 EmailBlock, RichTextBlock )

from core.blocks import PhoneNumberBlock

#---------------------------About Company Section------------------------------------

#
class IconWithHoverColorBlock(StructBlock):

#    icon = SvgChooserBlock(required=True, help_text="Upload an icon file")
    hover_color = NativeColorBlock(required=True, max_length=7, verbose_name='background_color',  
                                   help_text="Hover color for the element")
    text_icon = CharBlock(required=True)


#
class HeaderTabBlock(StructBlock):

    title = CharBlock(required=True, help_text='')
    content = TextBlock(help_text='')   
    image = ImageChooserBlock(required=True)

#
class AdvantagesTabBlock(StructBlock):

    title = CharBlock(required=True, help_text='')
    icon = SvgChooserBlock()
    advantage_elements = ListBlock(CharBlock())


#
class CenterTabBlock(StructBlock):
    
    title = CharBlock(required=True, help_text='')
    content = RichTextBlock(help_text='')

#
class CompanyDetailsBlock(StructBlock):

    title = CharBlock()

    company_name_title = CharBlock()
    company_name_value = CharBlock()

    company_address_title = CharBlock()
    company_address_value = CharBlock()

    tax_administration_title = CharBlock()
    tax_administration_value = CharBlock()

    tax_number_title = CharBlock()
    tax_number_value = CharBlock()


#
class BankAccountDetailsBlock(StructBlock):
    
    title = CharBlock()

    bank_branch_title = CharBlock()
    bank_branch_value = CharBlock()

    bank_address_title = CharBlock()
    bank_address_value = CharBlock()

    bank_branch_code_title = CharBlock()
    bank_branch_code_value = CharBlock()

    swift_code_title = CharBlock()
    swift_code_value = CharBlock()

    company_address_title = CharBlock()
    company_address_value = CharBlock()


#-------------------------------About Team Section-----------------------------

#
class TeamMemberBlock(StructBlock):

    member_image = ImageChooserBlock(required=False)

    member_name = CharBlock()
    
    job_description = CharBlock()
    
    email = EmailBlock()
    
    phone_number = PhoneNumberBlock()
    
    languages_title = CharBlock()
    languages = ListBlock(CharBlock())

 

