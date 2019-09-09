from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailcodeblock.blocks import CodeBlock


class ColumnBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(classname="full title")
    paragraph = blocks.RichTextBlock()
    code = CodeBlock()
    image = ImageChooserBlock()

    class Meta:
        template = 'frontend/craftbox/blocks/column.html'


class TwoColumnBlock(blocks.StructBlock):

    left_column = ColumnBlock(
        icon='arrow-right',
        label='Left column content'
    )
    right_column = ColumnBlock(
        icon='arrow-right',
        label='Right column content'
    )

    class Meta:
        template = 'frontend/craftbox/blocks/two_column_block.html'
        icon = 'placeholder'
        label = 'Two Columns'
