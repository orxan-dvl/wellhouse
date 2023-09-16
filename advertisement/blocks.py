from wagtail.images.blocks import ImageChooserBlock

from wagtail.core.blocks import CharBlock, StructBlock, BooleanBlock, StreamBlock, RichTextBlock


class CustomCharBlock(StructBlock):
    field_name = CharBlock(help_text="""Please enter name of the the field. 
                            For example: If you want to add information about the cost of property,
                            you can add just "Cost"  """)
    
    value = CharBlock(help_text="""Please enter the value. 
                            If you want add information about the cost of property,
                            you can add just value of cost. For example:(100000$ or etc.)""")


class CustomBooleanBlock(StructBlock):

    field_name = CharBlock(help_text="""Please enter name of the the field. 
                            For example: If you want to add the information about the existence of
                            "Furniture" in the property, you can add just "Furniture"  """)
    
    field_value = BooleanBlock(help_text="""Please enter the value
                                If you want to add the information about the existence of
                                "Furniture" in the property, you must check the chekbox or skip it
                                due to the value of existence of "Furniture" in the property """)


class OtherViewTabBlock(StructBlock):
    title = CharBlock(required=True)
    content = RichTextBlock()

# StreamBlocks
class ImageGalleryBlock(StreamBlock):
    image = ImageChooserBlock()
