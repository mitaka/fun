from django.conf.urls import url, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from core.urls import urlpatterns as urlpatterns_fun

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^password/change/', auth_views.password_change, name='password_change'),
    url(r'^password/change/done/', auth_views.password_change_done, name='password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^profile/', include('registration.backends.default.urls')),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += urlpatterns_fun

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
