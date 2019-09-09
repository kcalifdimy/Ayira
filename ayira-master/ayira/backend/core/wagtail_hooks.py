from django.utils.html import format_html
from django.contrib.staticfiles.templatetags.staticfiles import static

from wagtail.core import hooks


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('css/core.min.css'))


@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('css/core.min.css')
    )
