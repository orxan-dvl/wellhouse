from wagtailsvg.blocks import SvgChooserBlock
from wagtail.core.blocks import TextBlock, StructBlock


#Used for section_tab field of OrientationTourServicePage model
class Service1SectionBlock(StructBlock):
    icon = SvgChooserBlock(required=True, help_text="Upload an icon file")
    text_icon = TextBlock()

