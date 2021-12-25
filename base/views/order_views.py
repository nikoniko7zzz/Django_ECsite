from django.views.generic import ListView, DetailView
from base.models import Order
import json
from django.contrib.auth.mixins import LoginRequiredMixin


# 注文一覧表示
class OrderIndexView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'pages/orders.html'
    # created_atに-をつけているので、新しい注文順に並べる
    ordering = '-created_at'

    # 現在ログインしているユーザーの情報だけを表示
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# 個別の注文詳細ページ
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'pages/order.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object() # pkで個別を取得
        # json to dict
        context["items"] = json.loads(obj.items)
        context["shipping"] = json.loads(obj.shipping)
        return context