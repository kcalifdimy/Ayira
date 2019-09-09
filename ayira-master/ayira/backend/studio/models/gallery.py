from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.core.models import Orderable, Page
from wagtail.core.fields import RichTextField
from wagtail.images.models import Image
from wagtail.search import index
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

from ayira.backend.core.models import CarouselItem


class VideoGalleryPageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('studio.VideoGalleryPage', related_name='carousel_items')


class VideoGalleryPage(Page):
    intro = RichTextField(blank=True)
    feed_image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
    ]


VideoGalleryPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel('carousel_items', label="Carousel items"),

]

VideoGalleryPage.promote_panels = Page.promote_panels + [
    ImageChooserPanel('feed_image'),
]
