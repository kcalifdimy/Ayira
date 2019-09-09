from django.db import models

from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, PageChooserPanel
)
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.snippets.models import register_snippet


class ContactFields(models.Model):
    name_organization = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    telephone_2 = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    email_2 = models.EmailField(blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    post_code = models.CharField(max_length=10, blank=True)

    panels = [
        FieldPanel('name_organization',
                   'The full/formatted name of the person or organisation'),
        FieldPanel('telephone'),
        FieldPanel('telephone_2'),
        FieldPanel('email'),
        FieldPanel('email_2'),
        FieldPanel('address_1'),
        FieldPanel('address_2'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('post_code'),
    ]

    class Meta:
        abstract = True


class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL
    )
    link_document = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        related_name='+',
        on_delete=models.SET_NULL
    )

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True


class Blurb(LinkFields):
    header = models.CharField(max_length=150, blank=True)
    message = RichTextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True)
    messsage_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('header'),
        FieldPanel('message'),
        FieldPanel('icon'),
        ImageChooserPanel('messsage_image'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


class RelatedLink(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


class CarouselItem(RelatedLink):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)
    sub_caption = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel('caption', classname='title'),
        FieldPanel('sub_caption', classname='full'),
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


class ShoutOut(Blurb):
    summary = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(blank=True)

    panels = [
        MultiFieldPanel(Blurb.panels, 'Blurb'),
        FieldPanel('summary'),
        FieldPanel('slug'),
    ]

    class Meta:
        abstract = True


class Banner(LinkFields):
    message = RichTextField()
    title = models.CharField(max_length=50)
    message_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    panels = [
        FieldPanel('message'),
        FieldPanel('title'),
        ImageChooserPanel('message_image')
    ] + LinkFields.panels


class ContentBlock(LinkFields):
    page = models.ForeignKey(
        Page,
        related_name='contentblocks',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=255)
    body = RichTextField()
    summary = RichTextField(blank=True)
    slug = models.SlugField()
    panels = [
        PageChooserPanel('page'),
        FieldPanel('title'),
        FieldPanel('summary'),
        FieldPanel('body', classname="full"),
        FieldPanel('slug'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    def __unicode__(self):
        return u"{0}[{1}]".format(self.title, self.slug)


register_snippet(ContentBlock)


class Client(LinkFields):
    name = models.CharField(max_length=225, default="")
    logo = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='+'
    )
    moto = models.CharField(max_length=100, blank=True, null=True)
    summary = RichTextField(blank=True, null=True)

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('logo'),
        FieldPanel('moto'),
        FieldPanel('summary'),
        MultiFieldPanel(LinkFields.panels, "Link"),

    ]

    def __str__(self):
        return self.name


register_snippet(Client)


class Button(LinkFields):
    name = models.CharField(max_length=55)

    def __str__(self):
        return "{}".format(self.name)
    panels = [
        FieldPanel('name'),
        MultiFieldPanel(LinkFields.panels, "Link")
    ]


register_snippet(Button)


@register_setting
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(
        help_text='Your Facebook page URL', null=True, blank=True)
    instagram = models.URLField(
        max_length=255, help_text='Your Instagram URL', null=True, blank=True)
    twitter_name = models.CharField(
        max_length=255, help_text='Your Twitter Username without @',
        null=True, blank=True)
    youtube = models.URLField(
        help_text='Your YouTube Channel URL', null=True, blank=True)
    linkedin = models.URLField(
        max_length=255, help_text='Your Linkedin URL', null=True, blank=True)
    github = models.URLField(
        max_length=255, help_text='Your Github URL', null=True, blank=True)
    facebook_appid = models.CharField(
        max_length=255, help_text='Your Facbook AppID', null=True, blank=True)

    def __str__(self):
        return "community"


@register_setting
class SiteBranding(BaseSetting):
    site_name = models.CharField(max_length=250, null=True, blank=True, verbose_name="brand name")
    brand_message = models.TextField(null=True, blank=True)
    logo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    panels = [
        FieldPanel('site_name'),
        FieldPanel('brand_message'),
        ImageChooserPanel('logo'),
    ]

    def __str__(self):
        return "brand"
