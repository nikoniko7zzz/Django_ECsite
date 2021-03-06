"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base import views
from django.contrib.auth.views import LogoutView # 追加 viewは自作せずdjangoの機能を使う

urlpatterns = [
    path('admin/', admin.site.urls),

    # headerからのパス
    path('massagemenu/', views.massagemenu, name='massagemenu'),
    path('items/', views.items, name='items'),
    path('information/', views.information, name='information'),

    # Account
    path('login/', views.Login.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', views.SignUpView.as_view()),
    path('account/', views.AccountUpdateView.as_view()),
    path('profile/', views.ProfileUpdateView.as_view()),

    # Contact
    # path('contact/', views.ContactView.as_view()), # 追記
    path('contact/', views.contact),

    # Order
    path('orders/<str:pk>/', views.OrderDetailView.as_view()),
    path('orders/', views.OrderIndexView.as_view()),

    # Pay
    path('pay/checkout/', views.PayWithStripe.as_view()),
    path('pay/success/', views.PaySuccessView.as_view()),
    path('pay/cancel/', views.PayCancelView.as_view()),

    # Cart
    path('cart/remove/<str:pk>/', views.remove_from_cart),
    path('cart/add/', views.AddCartView.as_view()),
    path('cart/', views.CartListView.as_view()),  # カートページ

    # Items
    path('items/<str:pk>/', views.ItemDetailView.as_view()),  # アイテム詳細ページ
    path('categories/<str:pk>/', views.CategoryListView.as_view()), # 特定のカテゴリのページ カテゴリのpk(slug)
    path('tags/<str:pk>/', views.TagListView.as_view()),

    # Menu
    path('menu/', views.MenuListView.as_view()), # メニュー一覧
    path('menu/<str:pk>/', views.MenuDetailView.as_view()), # セレクトメニュー

    # # calendar
    # path('staff/<int:pk>/calendar/', views.StaffCalendar.as_view(), name='calendar'),
    # path('calendar/<int:year>/<int:month>/<int:day>/', views.Calendar.as_view()),

    path('', views.IndexListView.as_view()),  # トップページ
]
