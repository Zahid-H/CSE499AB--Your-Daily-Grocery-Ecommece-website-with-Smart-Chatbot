from.models import Category
from django.db.models import Count
from store.models import  Product

#.annotate(product_count=Count('post'))

def menu_links(request):
    links=Category.objects.annotate(product_count=Count('product'))
    context={
        'links' : links,
    }
    return context

