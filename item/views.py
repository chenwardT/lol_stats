from django.shortcuts import render
from django.views.generic import ListView

from api.models import Item


class ItemListView(ListView):
    """
    View to list items based on a query.
    """
    model = Item

    def get_queryset(self):
        # Fetch the queryset from the parent get_queryset.
        queryset = super(ItemListView, self).get_queryset()

        # Get the q GET parameter.
        q = self.request.GET.get('q')
        if q:
            # Return a filtered queryset.
            return queryset.filter(description__icontains=q)

        # Return the base queryset.
        return queryset


def view_items(request):
    """
    View to list all items.
    """
    items = Item.objects.all().order_by('item_id')

    return render(request, 'item/items.html', {'item': items})