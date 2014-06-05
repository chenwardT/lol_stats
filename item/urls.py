from django.conf.urls import patterns, url
from item.views import ItemListView

urlpatterns = patterns('item',
   url(r'^all/', 'views.view_items', name='view_items'),
   url(r'^', ItemListView.as_view(template_name='item/item_base.html'), name='item_list'),
)