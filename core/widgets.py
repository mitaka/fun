from django.contrib.admin.widgets import AdminFileWidget
from django import forms
from django.utils.safestring import mark_safe
from django.conf import settings

class AdminImageWidget(AdminFileWidget):
    """
    A ImageField Widget for admin that shows a thumbnail.
    """

    def __init__(self, attrs={}):
        super(AdminFileWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            output.append(('<a target="_blank" href="%s%s"><img src="%s%s" style="height: 28px;" /></a> ' % (settings.STATIC_URL, value.url, settings.STATIC_URL, value.url)))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))
