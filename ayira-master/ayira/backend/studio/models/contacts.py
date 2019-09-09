from django.db import models

from wagtail.core.models import Page
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from modelcluster.fields import ParentalKey
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel

from ayira.backend.core.block import ContactBlock, ContactListBlock


class CantactFormField(AbstractFormField):
    page = ParentalKey(
        'studio.Contact',
        on_delete=models.SET_NULL,
        null=True,
        related_name='contact_form_fields',
        blank=True
    )


class Contact(AbstractEmailForm):
    caption = models.CharField(max_length=255, blank=True, null=True)
    subcaption = models.CharField(max_length=255, blank=True, null=True)
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
        blank=True
    )
    contacts = StreamField([
        ('contacts', ContactListBlock(ContactBlock(label="office contacts")))
    ], blank=True)

    parent_page_types = ['studio.Home']

    content_panels = Page.content_panels + [
        FieldPanel('caption'),
        FieldPanel('subcaption'),
        StreamFieldPanel('contacts'),
        InlinePanel('contact_form_fields', label="Field", heading="contact form")
    ]

    promote_panels = Page.promote_panels + [
        ImageChooserPanel('cover_image')
    ]

    def get_template(request, *args, **kwargs):
        return "frontend/studio/contact.html"

    def get_form_fields(self):
        return self.contact_form_fields.all()

    class Meta:
        verbose_name = "studio contact page"
