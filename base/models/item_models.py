from django.db import models
from django.utils.crypto import get_random_string #ランダム文字列作成 id用
import os # 画像へのパス用

def create_id():
    return get_random_string(22) # 22文字のランダムな文字列を作る
# idをランダムにすると、ユーザーに予測がされにくくい

def upload_image_to(instance, filename):
    item_id = str(instance.id) # =Item.id
		# item_id = instance.id　？？？？
    return os.path.join('static', 'items', item_id, filename)
    # パス static/items/item_id/filename(ファイル名)
    # デプロイの時はパスを変える


class Tag(models.Model):
    slug = models.CharField(max_length=32, primary_key=True) # slug:id
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


# class Itemで使うので、class Itemより上に記述
class Category(models.Model):
    slug = models.CharField(max_length=32, primary_key=True) # slug:id
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Item(models.Model):
		# default=create_id 関数を呼び出す
		# editable=False 修正不可(管理画面でも)
    id = models.CharField(default=create_id, primary_key=True,
                          max_length=22, editable=False)
    name = models.CharField(default='', max_length=50)
    # PositiveIntegerField 正の整数
    price = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=0) # 在庫
		# TextFieldはCharFieldより長い文章がOK  blank=True ->空白OK
    description = models.TextField(default='', blank=True) # 説明(詳細)
    sold_count = models.PositiveIntegerField(default=0) # 販売数(ちがうテーブルでもいいかも)
    # is_published True=公開 False=未公開(下書き状態)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) # 作成日 自動作成
    updated_at = models.DateTimeField(auto_now=True) ## 更新日 自動作成
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
		# upload_to=upload_image_to アップロードするときは、upload_image_to関数を実行
    image = models.ImageField(
        default="", blank=True, upload_to=upload_image_to)
		# ForeignKey とは
    # クラスCategoryの中から選ぶ 多対1
		# on_delete=models.SET_NULL 親データが削除されると子データにNullをセットする
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    # ManyToManyField	多対多
    tags = models.ManyToManyField(Tag) # タグは複数付けれるので複数形


    def __str__(self):
        return self.name