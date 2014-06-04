from django.shortcuts import render

# Create your views here.
from api.models import Item


def view_items(request):
    """
    View to display all items.
    """
    items = Item.objects.all().order_by('item_id')

    return render(request, 'items.html', {'items': items})