import hashlib

from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.core.paginator import Paginator
from Store.models import *


def loginValid(fun):
    def inner(request, *args, **kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:
            user = Seller.objects.filter(username=c_user).first()
            if user:
                return fun(request, *args, **kwargs)
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
            user = Seller.objects.filter(username=username).first()
            if user:
                web_password = set_password(password)
                cookies = request.COOKIES.get("login_from")
                if user.password == web_password and cookies == "login_page":
                    response = HttpResponseRedirect("/Store/index/")
                    response.set_cookie("username", username)
                    response.set_cookie("user_id",user.id)#cookie提供用户id方便其他功能查询
                    request.session["username"] = username
                    return response
    return response


@loginValid
def index(request):
    user_id = request.COOKIES.get("user_id")
    if user_id:
        user_id = int(user_id)
    else:
        user_id = 0
    store = Store.objects.filter(user_id=user_id).first()
    if store:
        is_store = 1
    else:
        is_store = 0
    return render(request, "store/index.html", {"is_store": is_store})
# Create your views here.
def base(request):
    return render(request, "store/base.html")


def register_store(request):
    type_list=StoreType.objects.all()
    if request.method=="POST":
        post_data=request.POST#接收post数据
        store_name=post_data.get("store_name")
        store_description=post_data.get("store_description")
        store_phone=post_data.get("store_phone")
        store_money=post_data.get("store_money")
        store_address=post_data.get("store_address")
        user_id=int(request.COOKIES.get("user_id"))#通过cookie来获得user_id
        type_list=post_data.getlist("type")#获得一个类型列表
        store_logo=request.FILES.get("store_logo")
        #保存多对多数据
        store=Store()
        store.store_name=store_name
        store.store_description=store_description
        store.store_phone = store_phone
        store.store_money=store_money
        store.store_address=store_address
        store.user_id = user_id
        store.store_logo=store_logo#django 1.8以后可以直接保存图片
        store.save()#保存生成了数据库当中的一条数据
        for i in type_list:
            store_type=StoreType.objects.get(id=i)
            store.type.add(store_type)
        store.save()
    return render(request,"store/register_store.html",locals())
def add_goods(request):
    if request.method=="POST":
        post_data=request.POST#接收post数据
        goods_name=post_data.get("goods_name")
        goods_price=post_data.get("goods_price")
        goods_number=post_data.get("goods_number")
        goods_description=post_data.get("goods_description")
        goods_date = post_data.get("goods_date")
        goods_safeDate = post_data.get("goods_safeDate")
        goods_image=request.FILES.get("goods_image")
        store_id = post_data.get("store_id")
        #保存多对多数据
        goods=Goods()
        goods.goods_name=goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        goods.save()#保存生成了数据库当中的一条数据
        goods.store_id.add=(
            Store.objects.get(id=int(store_id))
        )
        goods.save()
    return render(request, "store/add_goods.html")
def list_goods(request):
    #在获取商品列表之前，先获取到通过get方式获取到keywords和当前页码，无操作时，默认页码为1.
    keywords=request.GET.get("keywords","")
    page_num=request.GET.get("page_num",1)
    #如果存在关键词
    if keywords:
        # 查询商品表中名称包含keywords的商品
        goods_list=Goods.objects.filter(goods_name__contains=keywords)
    #若不存在，则查询所有商品的信息
    else:
        goods_list=Goods.objects.all()
    # 将查询出来的商品设置为每页最多显示3条信息
    paginator=Paginator(goods_list,3)
    #
    page=paginator.page(int(page_num))
    page_range=paginator.page_range
    print(page_range)

    return render(request, "store/goods_list.html",{"keywords":keywords,"page":page,"page_range":page_range})