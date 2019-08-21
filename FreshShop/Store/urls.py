from django.urls import path, re_path
from Store.views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('index/', index),
    re_path('^$', index),
    path('logout/', logout),
    path('register_store/', register_store),
    path('list_goodstype/', list_goodstype),
    path('delete_type/', delete_type),
    path('add_goods/', add_goods),
    path('get_add/', get_add),
    path('api_goods_list/', api_goods_list),
    path(r'swv/', cache_page(15 * 60)(small_white_views)),
    re_path(r'order_list/(?P<state>\w+)', order_list),
    re_path(r'set_order/(?P<state>\w+)/', set_order),
    re_path(r'list_goods/(?P<state>\w+)', list_goods),
    re_path(r'^Store/(?P<goods_id>\d+)', goods),
    re_path(r'update_goods/(?P<goods_id>\d+)', update_goods),
    re_path(r'set_goods/(?P<state>\w+)/', set_goods),
    re_path(r'set_orders/(?P<state>\w+)/', set_orders),

]
urlpatterns += [
    path('test/', Test),
]
