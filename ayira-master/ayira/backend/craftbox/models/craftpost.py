from django.db import models

from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from taggit.managers import TaggableManager
from modelcluster.models import ClusterableModel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtailcodeblock.blocks import CodeBlock
from wagtail.search import index


class CraftPostTag(TaggedItemBase):
    content_object = ParentalKey('craftbox.CraftPost', on_delete=models.CASCADE, blank=True, null=True)


class CraftPostCategoryTag(TaggedItemBase):
    content_object = ParentalKey(
        'craftbox.CraftboxCategory',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='category_tags')


class CraftboxCategory(ClusterableModel):
    name = models.CharField(max_length=225, unique=True)
    tags = TaggableManager(through=CraftPostCategoryTag, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('tags'),
    ]

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = "Craftbox Category"
        verbose_name_plural = "craftbox Categories"


register_snippet(CraftboxCategory)


class CraftPost(Page):
    author = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField("Post date")
    featured = models.BooleanField(default=False)
    body = StreamField([
        ('content', blocks.RichTextBlock()),
        ('quote', blocks.BlockQuoteBlock()),
        ('image', ImageChooserBlock(template="frontend/craftbox/blocks/image.html")),
        ('embed', EmbedBlock()),
        ('code', CodeBlock())
    ])
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        help_text="An optional image to represent the page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
        )
    excerpt = StreamField([
        ('qoute', blocks.BlockQuoteBlock())]
        )
    tags = ClusterTaggableManager(through=CraftPostTag, blank=True)
    post_category = models.ForeignKey(
        CraftboxCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('featured'),
        index.SearchField('body'),
        index.SearchField('tags'),
        index.SearchField('post_category', boost=4)
    ]

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        StreamFieldPanel('body'),
    ]
    promote_panels = Page.promote_panels + [
        FieldPanel('date'),
        FieldPanel('featured'),
        ImageChooserPanel('cover_image'),
        StreamFieldPanel('excerpt'),
        FieldPanel('tags'),
        SnippetChooserPanel('post_category'),
    ]

    parent_page_types = ['craftbox.CraftHome']
    subpage_types = []

    def get_template(request, *args, **kwargs):
        return "frontend/craftbox/post.html"

    class Meta:
        verbose_name = "craft post page"
