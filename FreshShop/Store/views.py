import hashlib
from rest_framework import viewsets
from rest_framework import serializers
from Store.serializers import *
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.core.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend  # 导入过滤器

from Store.models import *
from Buyer.models import *


def loginValid(fun):
    def inner(request, *args, **kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/Store/login/")

    return inner


def set_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


def register(request):
    """
    register注册
    返回注册页面
    进行注册数据保存
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            seller = Seller()
            seller.username = username
            seller.password = set_password(password)
            seller.nickname = username
            seller.save()
            return HttpResponseRedirect("/Store/login/")
    return render(request, "store/register.html")


def login(request):
    response = render(request, "store/login.html")
    response.set_cookie("login_from", "login_page")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            # 检验用户名是否存在
            user = Seller.objects.filter(username=username).first()
            if user:
                web_password = set_password(password)
                # 校验请求是否来院于登录页面
                cookies = request.COOKIES.get("login_from")
                # 检验密码是否正确
                if user.password == web_password and cookies == "login_page":
                    response = HttpResponseRedirect("/Store/index/")
                    response.set_cookie("username", username)
                    response.set_cookie("user_id", user.id)
                    # response.set_cookie("user_id",user.id)#cookie提供用户id方便其他功能查询
                    request.session["username"] = username
                    # 检验是否有店铺
                    store = Store.objects.filter(user_id=user.id).first()
                    if store:
                        response.set_cookie("has_store", store.id)
                    else:
                        response.set_cookie("has_store", "")
                    return response
    return response


@loginValid
def index(request):
    return render(request, "store/index.html")


# Create your views here.
def base(request):
    return render(request, "store/base.html")


@loginValid
def register_store(request):
    # 查询店铺类型
    type_list = StoreType.objects.all()
    if request.method == "POST":
        post_data = request.POST  # 接收post数据
        # 获取前端表单数据
        store_name = post_data.get("store_name")
        store_description = post_data.get("store_description")
        store_phone = post_data.get("store_phone")
        store_money = post_data.get("store_money")
        store_address = post_data.get("store_address")
        user_id = int(request.COOKIES.get("user_id"))  # 通过cookie来获得user_id
        type_list = post_data.getlist("type")  # 获得一个类型列表
        store_logo = request.FILES.get("store_logo")
        # 保存多对多数据
        store = Store()
        store.store_name = store_name
        store.store_description = store_description
        store.store_phone = store_phone
        store.store_money = store_money
        store.store_address = store_address
        store.user_id = user_id
        store.store_logo = store_logo  # django 1.8以后可以直接保存图片
        store.save()  # 保存生成了数据库当中的一条数据
        # 类型可选多个，循环类型列表，得到类型id,前端传过来的为类型的id
        for i in type_list:
            store_type = StoreType.objects.get(id=i)  # 查询对应类型
            store.type.add(store_type)  # 添加到类型字段,多对多的映射表
        store.save()
        response = HttpResponseRedirect("/Store/index")
        response.set_cookie("has_store", store.id)  # 保存注册数据后即已经注册店铺，设置cookie为当前商店id
        return response  # 注册完商铺后实现跳转管理界面
    return render(request, "store/register_store.html", locals())


@loginValid
def add_goods(request):
    goodstypelist = GoodsType.objects.all()
    if request.method == "POST":
        post_data = request.POST  # 接收post数据
        goods_name = post_data.get("goods_name")
        goods_price = post_data.get("goods_price")
        goods_number = post_data.get("goods_number")
        goods_description = post_data.get("goods_description")
        goods_date = post_data.get("goods_date")
        goods_safeDate = post_data.get("goods_safeDate")
        goods_image = request.FILES.get("goods_image")
        # store_id = post_data.get("store_id")
        goods_type = post_data.get("type")
        store_id = request.COOKIES.get("has_store")
        # 保存多对多数据
        goods = Goods()
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        #保存多对多字段
        goods.goods_type = GoodsType.objects.get(id=int(goods_type))
        goods.store_id = Store.objects.get(id=int(store_id))
        goods.save()
        return HttpResponseRedirect("/Store/list_goods/up")
    return render(request, "store/add_goods.html", locals())


@loginValid
def list_goods(request, state):
    # 在获取商品列表之前，
    # 先获取到通过get方式获取到keywords和当前页码，
    # 无操作时，默认页码为1,关键字为空
    if state == "up":
        state_num = 1
    else:
        state_num = 0
    keywords = request.GET.get("keywords", "")
    page_num = request.GET.get("page_num", 1)
    store_id = request.COOKIES.get("has_store")
    store = Store.objects.get(id=int(store_id))
    # 如果存在关键词，查询包含关键字的商品信息
    if keywords:
        # 查询商品表中名称包含keywords的商品，反向查询，多键在goods中
        goods_list = store.goods_set.filter(goods_name__contains=keywords, goods_under=state_num)
    # 若不存在，则查询所有商品的信息
    else:
        goods_list = store.goods_set.filter(goods_under=state_num)
        print(goods_list)
    # 将查询出来的商品设置为每页最多显示3条信息
    paginator = Paginator(goods_list, 3)
    # 选择页码对应的页
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request, "store/goods_list.html",
                  {"keywords": keywords, "page": page, "page_range": page_range, "state": state})


@loginValid
def goods(request, goods_id):
    # 通过传入的goods_id来查询对应id的商品并显示详情
    goods_data = Goods.objects.filter(id=goods_id).first()
    return render(request, "store/goods.html", locals())


@loginValid
def update_goods(request, goods_id):
    # 用来传给前台显示前台的数据
    goods_data = Goods.objects.filter(id=goods_id).first()
    if request.method == "POST":
        post_data = request.POST  # 接收post数据
        goods_name = post_data.get("goods_name")
        goods_price = post_data.get("goods_price")
        goods_number = post_data.get("goods_number")
        goods_description = post_data.get("goods_description")
        goods_date = post_data.get("goods_date")
        goods_safeDate = post_data.get("goods_safeDate")
        goods_image = request.FILES.get("goods_image")
        # 保存多对多数据
        goods = Goods.objects.get(id=int(goods_id))
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        if goods_image:
            goods.goods_image = goods_image
        goods.save()
        return HttpResponseRedirect('/Store/Store/%s/' % goods_id)
    return render(request, "store/update_goods.html", locals())


def set_goods(request, state):
    if state == "up":
        state_num = 1
    else:
        state_num = 0
    id = request.GET.get("id")
    referer = request.META.get("HTTP_REFERER")
    if id:
        goods = Goods.objects.filter(id=id).first()
        if state_num == "delete":
            goods.delete()
        else:
            goods.goods_under = state_num
            goods.save()
    return HttpResponseRedirect(referer)
'''
订单状态：
未支付   1
待发货   2
已发货   3
已收货   4
已退货   0
取消订单 5
'''
def set_orders(request, state):
    if state == "no":
        state_num = 5
    else:
        state_num = 3
    id = request.GET.get("id")
    referer = request.META.get("HTTP_REFERER")
    if id:
        order_obj = Order.objects.get(order_id=id)
        if state_num == "delete":
            order_obj.delete()
        else:
            order_obj.order_status=state_num
            order_obj.save()
    return HttpResponseRedirect(referer)
def logout(request):
    response = HttpResponseRedirect("/Store/login/")
    for key in request.COOKIES:
        response.delete_cookie(key)
    return response


@loginValid
def list_goodstype(request):
    goodstypelist = GoodsType.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        picture = request.FILES.get("picture")
        # page_num = request.GET.get("page_num", 1)
        goodstype = GoodsType()
        goodstype.name = name
        goodstype.description = description
        goodstype.picture = picture
        goodstype.save()
        # store_id = request.COOKIES.get("has_store")
        # goodstypelist = goodstypelist.
        # paginator = Paginator(goodstype, 3)
        # # 选择页码对应的页
        # page = paginator.page(int(page_num))
        # page_range = paginator.page_range
        return HttpResponseRedirect("/Store/list_goodstype")

    return render(request, "store/list_goodstype.html", locals())


@loginValid
def delete_type(request):
    type_id = request.GET.get("id")
    type = GoodsType.objects.filter(id=type_id).delete()
    return HttpResponseRedirect('/Store/list_goodstype')


'''
订单状态：
未支付   1
待发货   2
已发货   3
已收货   4
已退货   0
取消订单 5
'''


def set_order(request, state):
    if state == "no":
        order_status = 2
    else:
        order_status = 3
    id = request.GET.get("order_id")
    referer = request.META.get("HTTP_REFERER")
    if id:
        order = OrderDetail.objects.filter(order_id__order_id=id, order_status=order_status).first()
        if state == "delete":
            order.delete()
        elif state == "no":
            order.order_status = 3
            order.save()
        else:
            order.order_status = 5
            order.save()
    return HttpResponseRedirect(referer)


'''
订单状态：
未支付   1
待发货   2
已发货   3
已收货   4
已退货   0
取消订单 5
'''
#获取当前店铺的订单消息
def order_list(request, state):
    if state == "no":
        status_num = 2
    else:
        status_num = 3
    or_list=[]
    store_id = request.COOKIES.get("has_store")
    page_num = request.GET.get("page_num", 1)
    # 查询当前状态的订单信息
    order_list = Order.objects.filter(order_status=status_num)
    for i in order_list:
        #反向查询出当前订单的订单详情信息
        set=i.orderdetail_set.filter(goods_store=store_id)
        or_list.append(set)
    # 分页将查询出来的商品设置为每页最多显示3条信息
    paginator = Paginator(order_list, 3)
    # 选择页码对应的页
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request, "store/order_list.html", locals())


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = Goods.objects.all()  # 具体返回数据
    serializer_class = UserSerializer  # 指定过滤的类
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['goods_name', 'goods_price']


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = Goods.objects.all()
#     serializers_class=UserSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields=['goods_name','goods_price']

class TypeViewSet(viewsets.ModelViewSet):
    """
    返回具体查询的内容
    """
    queryset = GoodsType.objects.all()
    serializer_class = GoodsTypeSerializer


def api_goods_list(request):
    return render(request, "store/api_goods_list.html", locals())


from CeleryTask.tasks import add
from django.http import JsonResponse


def get_add(request):
    add.delay(2, 3)
    return JsonResponse({"status": 200})


# def small_white_views(request):
# # def hello():
# #     return HttpResponse("hello world")
# # rep=HttpResponse("I am rep")
# # rep.render=hello
# # return rep
#     rep=HttpResponse("I AM rep")
#     rep.render=lambda :HttpResponse("hello world")
#     return rep
from django.views.decorators.cache import cache_page
# @cache_page(15*60)
# def small_white_views(request):
#     rep=HttpResponse("I AM REP")
#     return rep
from django.core.cache import cache
def small_white_views(request):
    store_data=cache.get("store_data")
    if store_data:
        store_data=store_data
    else:
        data=Store.objects.all()
        cache.set("store_data",data,30)
        #cache.add("store_data",data,30)
        store_data=data
    return render(request,"store/index.html",locals())

def Test(request):
    return render(request,"store/Test.html",locals())
