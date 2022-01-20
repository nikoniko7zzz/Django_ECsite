# from django.shortcuts import render
# from django.views.generic import ListView, DetailView
# # from django.views.generic import ListView, DetailView
# from base.models import MenuItem, MenuCategory, MenuTag
# # from base.models import MenuItem, MenuCategory, MenuTag # 今回 追加

# class MenuListView(ListView):
#     model = MenuItem
#     context_object_name = 'menus_list'
#     template_name = 'pages/menu_list.html'

#     def get_context_data(self, **kwargs):
#         context = super(MenuListView, self).get_context_data(**kwargs)

#         # ラジオボタン表示
#         context['categorys'] = MenuCategory.objects.all()
#         context['tags'] = MenuTag.objects.all()

#         return context

#     def get_queryset(self):
#         # # デフォルトは全件取得
#         results = self.model.objects.all()

#         # GETのURLクエリパラメータを取得する
#         # 該当のクエリパラメータが存在しない場合は、Noneが返ってくる
#         q_category = self.request.GET.get('categorys_group')
#         q_tag = self.request.GET.get('tags_group')
#         print(q_tag)

#         # 検索条件に合わせてフィルターをかける
#         if q_category != None and  q_tag == 'all':
#             results = results.filter(category=q_category)
#         elif q_category != None and  q_tag != None:
#             results = results.filter(category=q_category, tags=q_tag)
#         elif q_category != None:
#             results = results.filter(category=q_category)
#         elif q_tag != None:
#             results = results.filter(tags=q_tag)

#         return results


# # class MenuSelectListView(ListView):
# #     model = MenuItem
# #     context_object_name = 'menus_list'
# #     template_name = 'pages/menu_list.html'

# #     def get_context_data(self, **kwargs):
# #         context = super(MenuListView, self).get_context_data(**kwargs)

# #         # ラジオボタン表示
# #         context['categorys'] = MenuCategory.objects.all()
# #         context['tags'] = MenuTag.objects.all()

# #         return context


# class MenuDetailView(DetailView):
#     model = MenuItem
#     template_name = 'pages/menu_selectList.html'







