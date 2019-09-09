from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class AppStoreBlock(blocks.StructBlock):
    label = blocks.CharBlock()
    store_name = blocks.CharBlock()
    app_address = blocks.URLBlock()
    store_logo = ImageChooserBlock()

    class Meta:
        template = 'frontend/studio/blocks/app_store_block.html'
