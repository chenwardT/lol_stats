from django.conf.urls import patterns, url

urlpatterns = patterns('item',
   url(r'^all/', 'views.view_items', name='view_items'),
)