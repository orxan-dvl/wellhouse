from wagtailsvg.blocks import SvgChooserBlock
from wagtail_color_panel.blocks import NativeColorBlock

from wagtail.core.blocks import StructBlock, CharBlock

#
class AdvantagesTabBlock(StructBlock):

    title = CharBlock(required=True)


#
class IconWithBackgroundColorBlock(StructBlock):

    background_color = NativeColorBlock(required=True, max_length=7,  
                                   help_text="Background color for the element")
    text_icon = CharBlock(required=True)

