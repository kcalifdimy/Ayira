from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


from ..blocks import AppStoreBlock


class AppCover(Page):
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+'
    )
    header = models.CharField(max_length=255, blank=True, null=True)
    sub_header = models.CharField(max_length=255, blank=True, null=True)
    available_apps = StreamField([
        ('available_app', AppStoreBlock())
    ], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header'),
        FieldPanel('sub_header'),
        StreamFieldPanel('available_apps'),
    ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('cover_image')
    ]

    def get_template(request, *args, **kwargs):
        return "frontend/studio/cover_app.html"

    class Meta:
        verbose_name = "app cover page"
