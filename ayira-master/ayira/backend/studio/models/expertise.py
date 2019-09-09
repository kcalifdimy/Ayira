from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import InlinePanel, FieldPanel, StreamFieldPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.models import ParentalKey

from ayira.backend.core.models import Banner
from ayira.backend.core.block import PlanBlock, ServiceBlock


class ExpertiseHero(Banner):
    page = ParentalKey(
        'studio.Expertise',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='expertise_hero'
    )

    caption = models.CharField(max_length=255, blank=True, null=True)
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+'
    )

    panels = [
        FieldPanel('caption'),
        ImageChooserPanel('cover_image')
    ] + Banner.panels


class ExpertiseClient(Orderable, models.Model):
    page = ParentalKey(
        'studio.Expertise',
        on_delete=models.CASCADE,
        related_name='expertise_client'
    )
    client = models.ForeignKey(
        'core.Client',
        on_delete=models.CASCADE,
        related_name='+'
    )

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    panels = [
        SnippetChooserPanel('client')
    ]


class Expertise(Page):
    services = StreamField([
        ('services', ServiceBlock())
    ], blank=True)
    mvp_plans = StreamField([
        ('plans', PlanBlock())
    ], blank=True)

    parent_page_types = ['studio.Home']

    content_panels = Page.content_panels + [
        StreamFieldPanel('services'),
        StreamFieldPanel('mvp_plans', classname="collapsible collapse"),
        InlinePanel(
            'expertise_client',
            max_num=5,
            label='Client',
            heading="Our Clientele"
        )
    ]
    promote_panels = Page.promote_panels + [
        InlinePanel(
            'expertise_hero',
            heading="Expertise Hero Section",
            label="Hero", max_num=1
        )
    ]

    def get_template(request, *args, **kwargs):
        return "frontend/studio/expertise.html"

    class Meta:
        verbose_name = "studio expertise page"
