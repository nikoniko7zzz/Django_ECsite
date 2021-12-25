from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from django.conf import settings
from stripe.api_resources import tax_rate
from base.models import Item, Order
import stripe
from django.contrib.auth.mixins import LoginRequiredMixin # ログインしている人だけ(クラス用)
from django.core import serializers # Djangoデータをjson形式に変えてくれる # 今回 追加
import json
from django.contrib import messages


stripe.api_key = settings.STRIPE_API_SECRET_KEY

# 決済完了ページ
class PaySuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/success.html'

    def get(self, request, *args, **kwargs):
				# 今回 追加
        # 最新のOrderオブジェクトを取得し、注文確定に変更
        # ログインユーザーの最新のOrderをorderに入れる
        order = Order.objects.filter(
            user=request.user).order_by('-created_at')[0]
        order.is_confirmed = True  # 注文確定
        order.save()

        # カート情報削除
        del request.session['cart']

        return super().get(request, *args, **kwargs)

# キャンセルした時の処理
class PayCancelView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/cancel.html'

    def get(self, request, *args, **kwargs):
				# 今回 追加
        # 最新のOrderオブジェクトを取得
        order = Order.objects.filter(
            user=request.user).order_by('-created_at')[0]
				# 今回 追加
        # (仮注文時に作成した)在庫数と販売数を元の状態に戻す
        for elem in json.loads(order.items): # json形式をpython形式にする
            item = Item.objects.get(pk=elem['pk'])
            item.sold_count -= elem['quantity']
            item.stock += elem['quantity']
            item.save()
				# 今回 追加
        # is_confirmedがFalseであれば削除（仮オーダー削除）
        if not order.is_confirmed:
            order.delete()

        return super().get(request, *args, **kwargs)


tax_rate = stripe.TaxRate.create(
    display_name='消費税',
    description='消費税',
    country='JP',
    jurisdiction='JP',
    percentage=settings.TAX_RATE * 100,
    inclusive=False,  # 外税を指定（内税の場合はTrue）
)

 # stripeの機能を使う. stripeのserver.pyの動き
def create_line_item(unit_amount, name, quantity):
    return {
        'price_data': {
            'currency': 'JPY', # 通貨の単位:円
            'unit_amount': unit_amount, # 単価(税抜き)
            'product_data': {'name': name, } # 商品データ商品名
        },
        'quantity': quantity, # 数量
        'tax_rates': [tax_rate.id] # 税率
    }

# プロフィールに記載があるか入ってないと
def check_profile_filled(profile):
    # 送付先の名前がNoneか空白の時は、falseを返す
    if profile.name is None or profile.name == '':
        return False
    elif profile.zipcode is None or profile.zipcode == '':
        return False
    elif profile.prefecture is None or profile.prefecture == '':
        return False
    elif profile.city is None or profile.city == '':
        return False
    elif profile.address1 is None or profile.address1 == '':
        return False
    return True


class PayWithStripe(LoginRequiredMixin, View):

    # カートに情報がなければトップページに行く
    def post(self, request, *args, **kwargs):
        # プロフィールが埋まっているかどうか確認
        if not check_profile_filled(request.user.profile):
            messages.error(request, '配送のためプロフィールを埋めてください。')
            return redirect('/profile/')

        cart = request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            messages.error(request, 'カートが空です。')
            return redirect('/')

        items = [] # Orderモデル用に追記 # 今回 追加
        line_items = []
        for item_pk, quantity in cart['items'].items():
            item = Item.objects.get(pk=item_pk)
            # stripeの決済ページに出す内容を作る
            line_item = create_line_item(
                item.price, item.name, quantity)
            line_items.append(line_item)

            # Orderモデル用に追記 # 今回 追加
            items.append({
                'pk': item.pk,
                'name': item.name,
                'image': str(item.image),
                'price': item.price,
                'quantity': quantity,
            })

						# 今回 追加
            # 在庫をこの時点で引いておく、注文キャンセルの場合は在庫を戻す
            # 販売数も加算しておく
            item.stock -= quantity
            item.sold_count += quantity
            item.save()

				# 今回 追加
        # 仮注文を作成（is_confirmed=Flase)
        # いったん仮注文を作成し、成功(PaySuccessView)かキャンセル(PayCancelView)かで処理をする
        Order.objects.create(
            user=request.user,
            uid=request.user.pk,
            items=json.dumps(items),
            # ユーザープロフィールモデルはDjangoデータなので、
            # serializeを使ってjsonにする
            shipping=serializers.serialize("json", [request.user.profile]),
            amount=cart['total'],
            tax_included=cart['tax_included_total']
        )


        # stripeの機能を使う. stripeのserver.pyの動き
        checkout_session = stripe.checkout.Session.create(
            customer_email=request.user.email, # ユーザーモデルのデータを渡す # 今回 追加
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f'{settings.MY_URL}/pay/success/',
            cancel_url=f'{settings.MY_URL}/pay/cancel/',
        )
        return redirect(checkout_session.url)