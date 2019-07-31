from django.urls import path, include
from Buyer.views import *

urlpatterns = [

    path('login/', login),
    path('register/', register),
    path('index/', index),
    path('logout/', logout),
    path('good_list/', good_list),
    path('user_order/', user_order),
    path('user_site/', user_site),
    path('user_info/', user_info),
    path('place_order/', place_order),
    path('cart/', cart),
    path('add_cart/', add_cart),
    path('detail/', detail),

]
urlpatterns += [
    path('pay_result/', pay_result),
    path('pay_order/', pay_order),
]
