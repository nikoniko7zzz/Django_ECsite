from django.conf import settings
from base.models import Item, Category, Tag

# 売れてるもの順（在庫が少ない順）
def base(request):
    items = Item.objects.filter(is_published=True)
    categorys = Category.objects.all
    tags = Tag.objects.order_by('name')
    return {
        'TITLE': settings.TITLE,
        'ADDTIONAL_ITEMS': items,
        'POPULAR_ITEMS': items.order_by('-sold_count'),
        'CATEGORY_LISTS' : categorys,
        'TAG_LISTS' : tags
    }

