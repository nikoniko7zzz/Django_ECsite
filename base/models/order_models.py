from django.db import models
import datetime
from django.contrib.auth import get_user_model

# 注文履歴 基本変更はないもの

def custom_timestamp_id():
    dt = datetime.datetime.now()
    return dt.strftime('%Y%m%d%H%M%S%f') # 日時マイクロ秒


class Order(models.Model):
    # editable=False 管理画面でも修正不可
    id = models.CharField(default=custom_timestamp_id,
                          editable=False, primary_key=True, max_length=50)
    # on_delete=models.CASCADE ユーザーの情報がなくなればこのデータはなくなる
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    uid = models.CharField(editable=False, max_length=50) # ユーザーID
    # class PayCancelView で使う 決済がうまくできたときにtrueにする
    is_confirmed = models.BooleanField(default=False)
    amount = models.PositiveIntegerField(default=0) # 金額
    tax_included = models.PositiveIntegerField(default=0) # 税込
    # アイテムがいくつあるかわからないので、jsonにしている
    items = models.JSONField() # 購入アイテム
    shipping = models.JSONField() # 配送先
    shipped_at = models.DateTimeField(blank=True, null=True) # 発送日
    canceled_at = models.DateTimeField(blank=True, null=True) # キャンセル日
    memo = models.TextField(blank=True) #  管理者画面で見る用のメモ
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id