from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from core.models import Post

class LastPostsFeed(Feed):
    title = _('Latest posts')
    link = '/feed/'
    description = _('Latest posts')

    def items(self):
        return Post.objects.all()[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content
