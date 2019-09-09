from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel

from wagtail.contrib.routable_page.models import RoutablePageMixin, route


class CraftHome(RoutablePageMixin, Page):
    header = models.CharField(max_length=255)

    content_panels = Page.content_panels + [
        FieldPanel('header')
    ]
    subpage_types = ['craftbox.CraftPost']

    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def post_by_tag(self, request, tag, *args, **kwargs):
        self.search_type = 'tag'
        self.search_term = tag
        self.posts = self.get_posts().search(tag)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^category/(?P<category>[-\w]+)/$')
    def post_by_category(self, request, category, *args, **kwargs):
        self.search_type = 'post_category'
        self.search_term = category
        self.posts = self.get_posts().filter(craftpost__post_category__name=category.replace('-', ' '))
        return Page.serve(self, request, *args, **kwargs)

    def get_posts(self):
        return self.get_children().live().order_by('-first_published_at')

    def get_featured_post(self):
        post = self.get_posts().filter(craftpost__featured=True).first()
        return post if post else self.get_posts()[:1]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        craft_post = self.get_posts()[:10]
        search_terms = ['post_category']  # TODO: Dynamically compile routing list
        context['posts'] = self.posts if getattr(self, 'search_type', "") in search_terms else {}
        context['search_type'] = getattr(self, 'search_type', "")
        context['search_term'] = getattr(self, 'search_term', "")
        context['craft_post'] = craft_post
        return context

    def get_template(request, *args, **kwargs):
        return "frontend/craftbox/home.html"

    class Meta:
        verbose_name = "craftbox home page"
