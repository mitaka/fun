from django.conf.urls import patterns, include, url
from core.feeds import LastPostsFeed
from core.views import PostListView, PostDetailView, PostEditView, PostCreateView, CategoryCreateView,AuthorDetailView, AuthorUpdateView, CategoryListPostsView
from core.forms import CaptchaRegistrationForm
from core.sitemap import PostSitemap
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views import sitemap
from registration.backends.default.views import ActivationView
from registration.backends.default.views import RegistrationView

from django.views.decorators.cache import cache_page

sitemaps = {
    'fun': PostSitemap,
}

urlpatterns = patterns('core.views',
    #url(r'^$', cache_page(60 * 15)(PostListView.as_view()), name='index'),
    url(r'^$', PostListView.as_view(), name='index'),
    url(r'^post/add/$', login_required(PostCreateView.as_view()), name='add_post'),
    url(r'^category/add/$', login_required(CategoryCreateView.as_view()), name='add_category'),
    url(r'^category/(?P<name>[-_\w]+)/$', CategoryListPostsView.as_view(), name='list_category_posts'),
    #url(r'^post/(?P<pk>\d+)/(?P<slug>[-_\w]+)/$', cache_page(60 * 15)(PostDetailView.as_view()), name='post'),
    url(r'^post/(?P<pk>\d+)/(?P<slug>[-_\w]+)/$', PostDetailView.as_view(), name='post'),
    url(r'^post/edit/(?P<pk>\d+)/$', login_required(PostEditView.as_view()), name='edit_post'),
    url(r'^feed/', LastPostsFeed(), name='feed'),
    url(r'^profile/(?P<pk>\d+)/$', login_required(AuthorDetailView.as_view()), name='profile'),
    url(r'^profile/(?P<pk>\d+)/edit/$', login_required(AuthorUpdateView.as_view()), name='edit_profile'),
    url(r'^activate/complete/$', TemplateView.as_view(template_name='registration/activation_complete.html'), name='registration_activation_complete'),
    url(r'^activate/(?P<activation_key>\w+)/$', ActivationView.as_view(), name='registration_activate'),
    url(r'^register/$', RegistrationView.as_view(form_class=CaptchaRegistrationForm), name='registration_register'),
    url(r'^register/complete/$', TemplateView.as_view(template_name='registration/registration_complete.html'), name='registration_complete'),
    url(r'^rating/(?P<id>\d+)/(?P<slug>[-_\w]+)/up/$', 'rating_up', name='rating_up'),
    url(r'^rating/(?P<id>\d+)/(?P<slug>[-_\w]+)/down/$', 'rating_down', name='rating_down'),
    url(r'^search_results/', 'search', name='search'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
)
