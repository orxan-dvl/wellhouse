from wagtail.core.blocks import CharBlock, TextBlock, StructBlock, RichTextBlock

class EstateRegisterSectionBlock(StructBlock):
    title = CharBlock()
    content = RichTextBlock()