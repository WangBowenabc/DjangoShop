from django.urls import path,include
from Buyer.views import *
urlpatterns = [


    path('login/', login),
    path('register/', register),
    path('index/', index),
    path('logout/',logout),
    path('good_list/',good_list),

]
urlpatterns+=[
    path('pay_result/', pay_result),
    path('pay_order/', pay_order),
]