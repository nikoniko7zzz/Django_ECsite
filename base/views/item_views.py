from django.shortcuts import render
from django.views.generic import ListView, DetailView
from base.models import Item, Category, Tag # 今回 追加

# Itemモデルの全て
class IndexListView(ListView):
    model = Item
    template_name = 'pages/index.html'

'''
*** class IndexListViewをdefで書くとこうなる ***
def index(request):
    object_list = Item.objects.all()
    context = {
      'object_list': object_list,
    }
    return render(request, 'pages/index.html', context)
'''
# Itemモデルのpkをもとに個別データを返す
class ItemDetailView(DetailView):
    model = Item
    template_name = 'pages/item.html'


class CategoryListView(ListView): # 今回 追加
    model = Item # カテゴリモデルではない 指定のカテゴリを持っているアイテム一覧
    template_name = 'pages/list.html'
    paginate_by = 4 # アイテムの表示数を指定

    def get_queryset(self): # get_queryset の上書き
        self.category = Category.objects.get(slug=self.kwargs['pk'])
        # is_published=True 公開設定のものだけ
        return Item.objects.filter(is_published=True, category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Category #{self.category.name}'
        return context


class TagListView(ListView): # 今回 追加
    model = Item
    template_name = 'pages/list.html'
    paginate_by = 4

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['pk'])
        return Item.objects.filter(is_published=True, tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Tag #{self.tag.name}"
        return context