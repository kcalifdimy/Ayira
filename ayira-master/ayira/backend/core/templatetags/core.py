from django import template

from wagtail.core.models import Site

from ..models import Client


register = template.Library()


@register.inclusion_tag('frontend/tags/core/clients.html', takes_context=True)
def render_clients(context):
    return {
        'clients': Client.objects.all(),
        'request': context['request'],
    }


@register.inclusion_tag('frontend/tags/core/root_sites.html', takes_context=True)
def root_sites(context):
    return {
        'sites': Site.objects.all()
    }
