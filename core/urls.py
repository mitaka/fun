from django.conf.urls import patterns, include, url
from core.feeds import LastPostsFeed
from core.views import PostListView, PostDetailView, PostCreateView, AuthorDetailView, AuthorUpdateView
from django.views.generic.base import TemplateView
from registration.backends.default.views import ActivationView
from registration.backends.default.views import RegistrationView

urlpatterns = patterns('core.views',
    url(r'^$', PostListView.as_view(), name='index'),
    url(r'^post/add/$', PostCreateView.as_view(), name='add_post'),
    url(r'^post/(?P<pk>\d+)/(?P<slug>[-_\w]+)/$', PostDetailView.as_view(), name='post'),
    url(r'^feed/', LastPostsFeed()),
    url(r'^profile/(?P<pk>\d+)/$', AuthorDetailView.as_view(), name='profile'),
    url(r'^profile/(?P<pk>\d+)/edit/$', AuthorUpdateView.as_view(), name='edit_profile'),
    url(r'^activate/complete/$', TemplateView.as_view(template_name='registration/activation_complete.html'), name='registration_activation_complete'),
    url(r'^activate/(?P<activation_key>\w+)/$', ActivationView.as_view(), name='registration_activate'),
    url(r'^register/$', RegistrationView.as_view(), name='registration_register'),
    url(r'^register/complete/$', TemplateView.as_view(template_name='registration/registration_complete.html'), name='registration_complete'),
    url(r'^rating/up/$', 'rating_up', name='rating_up'),
    url(r'^rating/down/$', 'rating_down', name='rating_down'),
)
