from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # Don't care about API versioning b/c it will only be called by our domain's AJAX.
    url(r'^api/', include('api.urls')),
    url(r'^summoner/', include('summoner.urls')),
    url(r'^item/', include('item.urls')),

    #url(r'^items/', 'api.views.view_items', name='view_items'),
)
