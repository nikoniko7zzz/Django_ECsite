# base/views/cart_views.py

from django.shortcuts import redirect
from django.conf import settings #税率を取得
from django.views.generic import View, ListView
from base.models import Item
from collections import OrderedDict
from django.contrib.auth.mixins import LoginRequiredMixin # ログインしている人だけ(クラス用)
from django.contrib.auth.decorators import login_required # ログインしている人だけ(def用)


class CartListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'pages/cart.html'

    # カートに追加されたものだけを表示するための処理
    # get_queryset：ListViewが持っているメソッドと同じ名前にしてオーバーライドしている
    # queryset：全てのItemのリスト
    def get_queryset(self):
        cart = self.request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            # カートの中がなかったらトップページに返す
            return redirect('/')
        # querysetの中を初期化
        self.queryset = []
        self.total = 0
        # カートの中にItemがあった時の処理
        # .items()によりcart['items']の中をキーと値を取り出せる
        for item_pk, quantity in cart['items'].items():
            obj = Item.objects.get(pk=item_pk) # item_pkを指定してItemのオブジェクトを取得
            # モデルでデータベースに保存しないで、テンプレート表示用に一時的に定義
            # quantity:数量 subtotal:小計 total:合計(税抜き)
            obj.quantity = quantity
            obj.subtotal = int(obj.price * quantity)
            self.queryset.append(obj)
            self.total += obj.subtotal
        self.tax_included_total = int(self.total * (settings.TAX_RATE + 1)) #合計*1.1
        cart['total'] = self.total
        cart['tax_included_total'] = self.tax_included_total
        self.request.session['cart'] = cart
        # 親クラスに返す
        return super().get_queryset()

    # cart.htmlの下の部分を表示させるための処理
    # <p>小計 - ¥{{total}}</p>
    # <p>税込計 - ¥{{tax_included_total}}</p>
    # get_context_data：ListViewが持っているメソッドと同じ名前にしてオーバーライドしている
    def get_context_data(self, **kwargs):
        # 親のget_context_data＝vart.htmlのobject_list {% for object in object_list %}
        context = super().get_context_data(**kwargs)
        try:
            # 新しくcontext["total"]にdef get_querysetのself.totalを入れる
            context["total"] = self.total
            context["tax_included_total"] = self.tax_included_total
        except Exception:
            pass
        return context

# アイテムを追加するための処理
class AddCartView(LoginRequiredMixin, View):

    # item.html のここが入る <form action="/cart/add/" method="POST" class="" >
    def post(self, request):

        item_pk = request.POST.get('item_pk')
        quantity = int(request.POST.get('quantity'))
        # 'cart'がなかったら、Noneを返す
        cart = request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            # インスタンス化 順序のない辞書を順番が保持される OrderedDict
            items = OrderedDict()
            # itemsの中だけ順序付きの辞書が反映
            cart = {'items': items}
        # カートの中にアイテムがあれば
        if item_pk in cart['items']:
            # 数量を追加する
            cart['items'][item_pk] += quantity
        else:
            # なければ、数量を入れる
            cart['items'][item_pk] = quantity

        request.session['cart'] = cart
        return redirect('/cart/')

# カートから削除するための処理
@login_required
def remove_from_cart(request, pk): # pk:Itempk
    cart = request.session.get('cart', None)
    if cart is not None:
        del cart['items'][pk]
        request.session['cart'] = cart
    return redirect('/cart/')