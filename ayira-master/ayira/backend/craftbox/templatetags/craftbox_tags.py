from django import template
from ..models import CraftboxCategory, CraftHome


register = template.Library()


@register.inclusion_tag("frontend/craftbox/tags/craftbox_categories.html", takes_context=True)
def render_craftbox_category(context, page):
    return {
        'craftbox_categories': CraftboxCategory.objects.all(),
        'request': context['request'],
        'page': page,
        'crafthome': CraftHome.objects.first()
    }


@register.inclusion_tag("frontend/craftbox/tags/list_post.html", takes_context=True)
def render_post_previews(context, posts=None, category=None):
    home = CraftHome.objects.first().get_posts() if CraftHome.objects.first() else {}
    home = home.filter(craftpost__post_category__name=category) if category and home else home
    return {
        'request': context['request'],
        'posts': posts if posts else home,
        'category': category
    }
