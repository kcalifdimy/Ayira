from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (FieldPanel,
                                         MultiFieldPanel, InlinePanel
                                         )
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

from ayira.backend.core.models import CarouselItem, ShoutOut, Blurb


class HeroSlide(Orderable, CarouselItem):
    page = ParentalKey('studio.Home', related_name='hero_slide')


class Welcome(Orderable, Blurb):
    page = ParentalKey('studio.Home', related_name='welcome_blurbs')


class HomeContentItem(ShoutOut):
    page = ParentalKey('studio.Home', related_name='content_items')


class ProjectSpecFormField(AbstractFormField):
    page = ParentalKey(
        'studio.Home',
        on_delete=models.SET_NULL,
        null=True,
        related_name='project_spec_form_fields'
    )


class Home(AbstractEmailForm, Page):
    feed_image = models.ForeignKey(
        Image,
        help_text="An optional image to represent the page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro = RichTextField(blank=True, null=True)

    welcome_title = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Title'
    )
    welcome_intro = RichTextField(blank=True, null=True, verbose_name='Intro')

    indexed_fields = (
        'welcome_title',
        'welcome_intro',
        'intro',
        'title'
    )

    subpage_types = ['studio.Contact', 'studio.About', 'studio.Expertise']

    def get_template(request, *args, **kwargs):
        return "frontend/studio/home.html"

    def get_form_fields(self):
        return self.project_spec_form_fields.all()

    class Meta:
        verbose_name = "studio home page"


Home.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname='full'),
    MultiFieldPanel(
        [
            InlinePanel(
                'hero_slide',
                label="Slide Item"
            )
        ], heading="Hero Section", classname="collapsible collapsed"
    ),
    MultiFieldPanel([
        FieldPanel('welcome_title', classname="full title"),
        FieldPanel(
            'welcome_intro',
            classname="g-font-size-32--xs g-font-size-36--md"
        ),
        InlinePanel('welcome_blurbs', label='Blurbs')
    ], heading='Welcome Section', classname="collapsible collapsed"),
    MultiFieldPanel(
        [InlinePanel('content_items', label="Content Item")],
        classname="collapsible collapsed", heading="Shoutout Section"
    ),
]


Home.promote_panels = [
    MultiFieldPanel(
        Page.promote_panels + [ImageChooserPanel('feed_image')],
        "Common page configuration"
    ),
    InlinePanel(
        'project_spec_form_fields',
        label="Field",
        heading="project spec form"
    )
]
