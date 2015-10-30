from django.contrib.admin.widgets import AdminFileWidget
from django_summernote.widgets import SummernoteInplaceWidget, _static_url
from django.utils.safestring import mark_safe
from django.conf import settings


class SummernoteCustomWidget(SummernoteInplaceWidget):
    class Media:
        extend = False
        css = {'all': ('//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css',
                       '//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.min.css',) + (
            _static_url('django_summernote/summernote.css'),
        )}

        js = ('//code.jquery.com/jquery-1.9.1.min.js',
              '//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js') + (
            _static_url('django_summernote/jquery.ui.widget.js'),
            _static_url('django_summernote/jquery.iframe-transport.js'),
            _static_url('django_summernote/jquery.fileupload.js'),
            _static_url('django_summernote/summernote.min.js'),
        )


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
