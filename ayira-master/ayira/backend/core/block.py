from django.utils.html import format_html_join

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock


class ContactBlock(blocks.StructBlock):
    contact_options = [
        ('email', 'email'),
        ('phone', 'phone'),
        ('address', 'address')
    ]
    category = blocks.ChoiceBlock(choices=contact_options)
    info = blocks.CharBlock()
    icon = ImageChooserBlock()

    def __str__(self):
        return self.title

    class Meta:
        template = "frontend/core/blocks/contact_block.html"
        icon = 'mail'
        verbose_name = 'Contact'


class ContactListBlock(blocks.ListBlock):

    def render_basic(self, value, context=None):
        children = format_html_join(
            '\n', '<span>{0}</span>',
            [
                (self.child_block.render(child_value, context=context),)
                for child_value in value
            ]
        )
        return children


class BlurbBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    icon = blocks.CharBlock(help_text="icon must be a UNICODE character")
    message = blocks.TextBlock(rows=2)

    class Meta:
        template = "frontend/core/blocks/blurb_block.html"
        icon = 'cogs'


class ProcessBlock(blocks.StructBlock):
    caption = blocks.CharBlock()
    title = blocks.CharBlock()
    process = blocks.ListBlock(BlurbBlock(label="our processes"))

    class Meta:
        template = "frontend/core/blocks/process_block.html"
        icon = 'cogs'


class BannerBlock(blocks.StructBlock):
    caption = blocks.CharBlock()
    title = blocks.CharBlock()
    message = blocks.TextBlock()
    first_image = ImageChooserBlock()
    second_image = ImageChooserBlock(required=False)

    class Meta:
        template = "frontend/core/blocks/banner_block.html"
        icon = 'doc-empty'


class ColumnBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(classname="full title")
    paragraph = blocks.RichTextBlock()
    image = ImageChooserBlock()

    class Meta:
        template = 'frontend/core/blocks/column.html'


class TwoColumnBlock(blocks.StructBlock):

    left_column = ColumnBlock(icon='arrow-right', label='Left column content')
    right_column = ColumnBlock(icon='arrow-right', label='Right column content')

    class Meta:
        template = 'frontend/core/blocks/two_column_block.html'
        icon = 'grip'
        label = 'Two Columns'


class CaseStudyBlock(blocks.StructBlock):
    cover_image = ImageChooserBlock()
    title = blocks.CharBlock()
    link = blocks.PageChooserBlock('craftbox.CraftPost')

    class Meta:
        template = "frontend/core/blocks/case_study_block.html"


class SummaryBlock(blocks.StructBlock):
    caption = blocks.CharBlock()
    title = blocks.CharBlock()
    paragraph = blocks.TextBlock()

    class Meta:
        template = "frontend/core/blocks/summary_block.html"


class ServiceBlock(blocks.StructBlock):
    service = SummaryBlock()
    portfolio = blocks.ListBlock(CaseStudyBlock())

    class Meta:
        template = "frontend/core/blocks/service_block.html"


class FeatureBlock(blocks.StructBlock):
    feature = blocks.CharBlock()
    icon = blocks.CharBlock(
        help_text='Icons must be a UNCODE character',
        default="ti-check",
        ediatble=False)

    class Meta:
        template = "frontend/core/blocks/feature.html"


class PackageBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    icon = ImageChooserBlock()
    features = blocks.ListBlock(FeatureBlock(label='Feature'))
    hire_button = SnippetChooserBlock('core.Button')
    customise_button = blocks.CharBlock(help_text="Customise hire button content")

    class Meta:
        template = "frontend/core/blocks/package.html"


class PlanBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    caption = blocks.CharBlock()
    plan = blocks.ListBlock(PackageBlock(label='plan'))

    class Meta:
        label = "package"
        template = "frontend/core/blocks/plan.html"
