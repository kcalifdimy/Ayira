from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import InlinePanel, FieldPanel, StreamFieldPanel
from modelcluster.fields import ParentalKey

from ayira.backend.core.models import Banner
from ayira.backend.core.block import ProcessBlock, BannerBlock, ColumnBlock, TwoColumnBlock


class AboutHero(Banner):
    caption = models.CharField(max_length=255, blank=True, null=True)
    first_button_content = models.CharField(max_length=55, blank=True, null=True)
    second_button_content = models.CharField(max_length=55, blank=True, null=True)
    page = ParentalKey(
        'studio.About',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='about_hero'
    )
    panels = [
        FieldPanel('caption'),
        FieldPanel('first_button_content'),
        FieldPanel('second_button_content')
    ] + Banner.panels


class About(Page):
    body = StreamField([
        ('process', ProcessBlock()),
        ('banner', BannerBlock()),
        ('single_column', ColumnBlock()),
        ('double_column', TwoColumnBlock())
    ], blank=True)

    parent_page_types = ['studio.Home']

    promote_panels = Page.promote_panels + [
        InlinePanel('about_hero', max_num=1, heading='Hero Section')
    ]
    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]

    def __str__(self):
        return "{}".format(self.title)

    def get_template(request, *args, **kwargs):
        return "frontend/studio/about.html"

    class Meta:
        verbose_name = "about studio page"
